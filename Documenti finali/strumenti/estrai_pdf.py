#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Estrae il testo da un PDF, anche quando `pdftotext` non c'è.

Perché esiste: i PDF del committente (per esempio
`Sorgenti Documentali/Interazione IAM/RMCAP-IAM-MAN - Integrazione applicativa IAM.pdf`)
usano font con sottoinsiemi e stringhe esadecimali, quindi **non sono raggiungibili da
grep** e nemmeno da un'estrazione ingenua delle stringhe fra parentesi: quella restituisce
byte di immagini. Il testo si ricava solo decodificando i CMap `ToUnicode` di ciascun font,
pagina per pagina.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/estrai_pdf.py file.pdf
    ... estrai_pdf.py file.pdf -o testo.txt -p 11-15
    ... estrai_pdf.py file.pdf --interno        # ignora pdftotext anche se installato

Usa `pdftotext -layout` quando è disponibile (resa migliore delle tabelle); altrimenti
ricade sul decodificatore interno, che usa **solo la libreria standard**.

⚠️ Due trappole scoperte scrivendolo, che è il motivo per cui non va riscritto a mano
ogni volta:
  · l'ordine degli oggetti PDF **non è** l'ordine delle pagine: l'ordine vero sta
    nell'albero `/Root → /Pages → /Kids`, e va risolto ricorsivamente;
  · i CMap `ToUnicode` di questi file **non sono compressi**, mentre i flussi di
    contenuto lo sono: provare `zlib` e ricadere sul dato grezzo, non assumere.
Una mappa `code → carattere` unica per tutto il documento **non funziona**: fra i 14 font
del manuale IAM ci sono 67 codici in conflitto e il testo esce con lettere sbagliate
(`iv-portal-groups` diventa `iQ-porPMl-groups`). La mappa va tenuta **per font**.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import zlib


# --------------------------------------------------------------------------- oggetti
def _oggetti(raw):
    """Mappa numero → corpo dell'oggetto indiretto."""
    out = {}
    for m in re.finditer(rb'(\d+)\s+\d+\s+obj(.*?)endobj', raw, re.S):
        out[int(m.group(1))] = m.group(2)
    return out


def _riferimento(valore):
    m = re.match(rb'\s*(\d+)\s+\d+\s+R', valore or b'')
    return int(m.group(1)) if m else None


def _risolvi(objs, valore):
    n = _riferimento(valore)
    return objs.get(n, b'') if n is not None else (valore or b'')


def _flusso(objs, n):
    """Il contenuto del flusso dell'oggetto n, decompresso se serve."""
    corpo = objs.get(n, b'')
    m = re.search(rb'stream\r?\n', corpo)
    if not m:
        return b''
    dati = corpo[m.end(): corpo.rfind(b'endstream')]
    try:
        return zlib.decompress(dati)
    except zlib.error:
        return dati


def _dizionario(corpo, chiave):
    """Il valore grezzo di una chiave: riferimento, dizionario in linea o vettore."""
    m = re.search(rb'/' + chiave + rb'\s*(\d+\s+\d+\s+R|<<|\[)', corpo)
    if not m:
        return b''
    if m.group(1) not in (b'<<', b'['):
        return m.group(1)
    apre, chiude = (b'<<', b'>>') if m.group(1) == b'<<' else (b'[', b']')
    i = m.start(1)
    livello = 0
    while i < len(corpo):
        if corpo[i:i + len(apre)] == apre:
            livello += 1
            i += len(apre)
        elif corpo[i:i + len(chiude)] == chiude:
            livello -= 1
            i += len(chiude)
            if livello == 0:
                return corpo[m.start(1):i]
        else:
            i += 1
    return corpo[m.start(1):]


# --------------------------------------------------------------------------- font
def _carattere(hex_dst):
    """La destinazione di un bfchar è UTF-16BE: va decodificata come tale.

    ⚠️ Non `chr(int(..., 16))` per ogni gruppo di quattro cifre: le coppie surrogate
    produrrebbero caratteri surrogati isolati, che poi non si possono nemmeno scrivere
    su un file UTF-8 (`surrogates not allowed`).
    """
    if len(hex_dst) % 2:
        hex_dst = '0' + hex_dst
    try:
        return bytes.fromhex(hex_dst).decode('utf-16-be', 'replace')
    except ValueError:
        return ''


def _cmap(testo):
    """La mappa code → carattere di un CMap ToUnicode."""
    mp = {}
    for blocco in re.findall(r'beginbfchar(.*?)endbfchar', testo, re.S):
        for src, dst in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blocco):
            mp[int(src, 16)] = _carattere(dst)
    for blocco in re.findall(r'beginbfrange(.*?)endbfrange', testo, re.S):
        for a, b, c in re.findall(
                r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blocco):
            a, b = int(a, 16), int(b, 16)
            base = int(c, 16)
            for k in range(a, b + 1):
                mp[k] = _carattere('%04X' % (base + k - a))
        # forma a vettore: <inizio> <fine> [ <d1> <d2> ... ]
        for a, b, vet in re.findall(
                r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*\[(.*?)\]', blocco, re.S):
            a = int(a, 16)
            for i, d in enumerate(re.findall(r'<([0-9A-Fa-f]+)>', vet)):
                mp[a + i] = _carattere(d)
    return mp


def _font_del_documento(objs):
    """numero oggetto del font → (mappa, byte per codice)."""
    out = {}
    for n, corpo in objs.items():
        if b'/ToUnicode' not in corpo:
            continue
        rif = _riferimento(_dizionario(corpo, b'ToUnicode'))
        if rif is None:
            continue
        mp = _cmap(_flusso(objs, rif).decode('latin-1'))
        larghezza = 2 if (b'/Type0' in corpo or max(mp or {0: 0}) > 255) else 1
        out[n] = (mp, larghezza)
    return out


# --------------------------------------------------------------------------- pagine
def _ordine_pagine(objs, raw):
    """I numeri d'oggetto delle pagine, nell'ordine vero dell'albero /Pages."""
    radice = None
    m = re.search(rb'/Root\s+(\d+)\s+\d+\s+R', raw)
    if m:
        radice = _riferimento(_dizionario(objs.get(int(m.group(1)), b''), b'Pages'))
    ordine, visti = [], set()

    def scendi(n, prof=0):
        if n in visti or prof > 50:
            return
        visti.add(n)
        corpo = objs.get(n, b'')
        if re.search(rb'/Type\s*/Page[^s]', corpo):
            ordine.append(n)
            return
        kids = _dizionario(corpo, b'Kids')
        for k in re.findall(rb'(\d+)\s+\d+\s+R', kids):
            scendi(int(k), prof + 1)

    if radice is not None:
        scendi(radice)
    if not ordine:                      # ripiego: ordine degli oggetti
        ordine = sorted(n for n, c in objs.items()
                        if re.search(rb'/Type\s*/Page[^s]', c))
    return ordine


def _font_della_pagina(objs, corpo_pagina, font_doc):
    risorse = _risolvi(objs, _dizionario(corpo_pagina, b'Resources'))
    blocco = _risolvi(objs, _dizionario(risorse, b'Font'))
    fonts = {}
    for nome, num in re.findall(rb'/([A-Za-z0-9_.+-]+)\s+(\d+)\s+\d+\s+R', blocco):
        fonts[nome.decode('latin-1')] = font_doc.get(int(num), ({}, 1))
    return fonts


def _testo_del_contenuto(contenuto, fonts):
    t = contenuto.decode('latin-1')
    corrente = ({}, 1)
    pezzi = []
    passo = re.compile(
        r'/([A-Za-z0-9_.+-]+)\s+[-\d.]+\s+Tf'      # 1: cambio font
        r'|\[(.*?)\]\s*TJ'                          # 2: vettore
        r'|(\((?:\\.|[^()\\])*\)|<[0-9A-Fa-f\s]*>)\s*(?:Tj|\')'   # 3: stringa
        r'|(ET|T\*)', re.S)
    for m in passo.finditer(t):
        if m.group(1):
            corrente = fonts.get(m.group(1), ({}, 1))
            continue
        if m.group(4):
            pezzi.append('\n')
            continue
        corpo = m.group(2) or m.group(3) or ''
        mappa, larghezza = corrente
        for s in re.finditer(r'<([0-9A-Fa-f\s]+)>|\((?:\\.|[^()\\])*\)', corpo):
            if s.group(1) is not None:
                h = re.sub(r'\s', '', s.group(1))
                passoh = larghezza * 2
                for i in range(0, len(h) - passoh + 1, passoh):
                    pezzi.append(mappa.get(int(h[i:i + passoh], 16), ''))
            else:
                grezzo = s.group(0)[1:-1]
                grezzo = (grezzo.replace(r'\(', '(').replace(r'\)', ')')
                                .replace('\\\\', '\\'))
                for ch in grezzo:
                    pezzi.append(mappa.get(ord(ch), ch if mappa else ch))
    return ''.join(pezzi)


# --------------------------------------------------------------------------- interfaccia
def estrai_interno(percorso, pagine=None):
    """Il testo del PDF, pagina per pagina, con la sola libreria standard."""
    raw = open(percorso, 'rb').read()
    objs = _oggetti(raw)
    font_doc = _font_del_documento(objs)
    ordine = _ordine_pagine(objs, raw)
    out = []
    for indice, n in enumerate(ordine, 1):
        if pagine and indice not in pagine:
            continue
        corpo = objs.get(n, b'')
        fonts = _font_della_pagina(objs, corpo, font_doc)
        cont = _dizionario(corpo, b'Contents')
        numeri = [int(x) for x in re.findall(rb'(\d+)\s+\d+\s+R', cont)]
        contenuto = b'\n'.join(_flusso(objs, x) for x in numeri)
        out.append('===== PAGINA %d =====\n%s'
                   % (indice, _testo_del_contenuto(contenuto, fonts)))
    return '\n'.join(out)


def estrai(percorso, pagine=None, forza_interno=False):
    """Il testo del PDF: `pdftotext -layout` se c'è, altrimenti il decodificatore."""
    if not forza_interno and shutil.which('pdftotext'):
        cmd = ['pdftotext', '-layout', '-enc', 'UTF-8']
        if pagine:
            cmd += ['-f', str(min(pagine)), '-l', str(max(pagine))]
        esito = subprocess.run(cmd + [percorso, '-'], capture_output=True)
        if esito.returncode == 0 and esito.stdout.strip():
            # pdftotext separa le pagine con un avanzamento modulo: lo si traduce
            # nello stesso intestatore del decodificatore interno, così `--cerca`
            # riporta il numero di pagina in entrambe le modalità.
            prima = min(pagine) if pagine else 1
            fogli = esito.stdout.decode('utf-8', 'replace').split('\f')
            if fogli and not fogli[-1].strip():
                fogli.pop()
            return '\n'.join('===== PAGINA %d =====\n%s' % (prima + i, f)
                             for i, f in enumerate(fogli))
    return estrai_interno(percorso, pagine)


def _intervallo(spec):
    """"11-15" oppure "3" oppure "3,7,11-12" → insieme di numeri di pagina."""
    numeri = set()
    for pezzo in spec.split(','):
        pezzo = pezzo.strip()
        if '-' in pezzo:
            a, b = pezzo.split('-', 1)
            numeri.update(range(int(a), int(b) + 1))
        elif pezzo:
            numeri.add(int(pezzo))
    return numeri


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('pdf')
    ap.add_argument('-o', '--output', help='file di uscita (default: standard output)')
    ap.add_argument('-p', '--pagine', help='pagine da estrarre, es. 11-15 oppure 3,7')
    ap.add_argument('--interno', action='store_true',
                    help='ignora pdftotext e usa il decodificatore interno')
    ap.add_argument('--cerca', metavar='TERMINE',
                    help='stampa solo le righe che contengono il termine, con la pagina')
    a = ap.parse_args()

    if not os.path.exists(a.pdf):
        sys.exit('non trovo %s' % a.pdf)
    testo = estrai(a.pdf, _intervallo(a.pagine) if a.pagine else None, a.interno)

    if a.cerca:
        pagina = '?'
        righe = []
        for riga in testo.splitlines():
            m = re.match(r'===== PAGINA (\d+) =====', riga)
            if m:
                pagina = m.group(1)
            elif a.cerca.lower() in riga.lower():
                righe.append('p.%s  %s' % (pagina, riga.strip()))
        testo = '\n'.join(righe)

    if a.output:
        open(a.output, 'w', encoding='utf-8').write(testo)
        print('scritto %s (%d caratteri)' % (a.output, len(testo)))
    else:
        sys.stdout.write(testo)


if __name__ == '__main__':
    main()
