# -*- coding: utf-8 -*-
"""Inventario delle stampe JasperReports di SIPO.

Quattro generatori, due modi di tenere il modello:
  - stato civile (common/pdf-gen-sc): il modello sta nella tabella Oracle TEMPLATE e una copia
    dei sorgenti .jrxml/.jasper sta in jasper_templates/, con l'ID_TEMPLATE come prefisso del nome;
  - anagrafe/certificati (common/pdf-generator), elettorale (common/pdf-gen-elett) e nomine dei
    componenti di seggio (cross/Signps): il modello sta SOLO nella tabella TEMPLATE; il catalogo
    si ricava dalle costanti ID_DOC_* / ID_TEMPLATE_* con cui il codice lo sceglie.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/inventario_stampe_jasper.py
"""
import html
import os
import re
import sys
from collections import defaultdict

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(QUI))
OUT = os.path.join(os.path.dirname(QUI), sys.argv[1] if len(sys.argv) > 1
                   else 'INVENTARIO_Stampe-Jasper_SIPO_v0.2.xlsx')
SC = os.path.join(RADICE, 'common/pdf-gen-sc/PdfGen/src/main/resources/jasper_templates')
CONST_ANA = os.path.join(RADICE, 'common/pdf-generator/GeneraDocumento/src/main/java/it/romaCapitale/'
                                 'sipo/generaDocumento/common/ConstantDoc.java')
CONST_ELE = os.path.join(RADICE, 'common/pdf-gen-elett/GeneraDocumentoElettorale/src/main/java/it/'
                                 'romacapitale/sipo/generadocumentoelettorale/common/ConstantDoc.java')
CONST_SIG = os.path.join(RADICE, 'cross/Signps')

AREA = {'.': 'Varie (radice della cartella)', 'Nascite': 'Nascite', 'Decessi': 'Decessi',
        'Matrimoni': 'Matrimoni', 'Unioni': 'Unioni civili', 'Divozi': 'Divorzi e separazioni',
        'Cittadinanza': 'Cittadinanza', 'Annotazioni': 'Annotazioni e registri',
        'Esponente': 'Chiusura dei registri', 'Estratto': 'Estratti',
        'PubblicazioniStampaModelli': 'Pubblicazioni di matrimonio', 'Spalla': 'Atto (corpo)'}

# categoria: (espressione sul nome, etichetta, a che cosa serve)
CATEGORIE = [
    (r'^\d*_?(Art\d|Art_|Riacquisto|Rinuncia|Perdita|Oriundi|Acquisto cittadinanza|13_C_|Art4Comma2)',
     'Atto di cittadinanza', 'Testo dell’atto di cittadinanza per l’articolo di legge del caso '
     '(acquisto, riacquisto, rinuncia, perdita, attestazione); «1_2», «2_2» indicano la pagina'),
    (r'StampaAccertamento', 'Atto di cittadinanza', 'Accertamento di cittadinanza a testo libero'),
    (r'TutelaMinori|IscrizioneAnagrafica', 'Comunicazione',
     'Comunicazione dell’evento a un altro ufficio o ente'),
    (r'Testimoni', 'Documenti dei testimoni', 'Stampa dei dati e documenti dei testimoni (2 o 4)'),
    (r'Pubblicazione|Delega|Promessa|Affissione', 'Pubblicazioni di matrimonio',
     'Atti della pubblicazione di matrimonio (atto, affissione, delega, promessa)'),
    (r'A4_DivorziItaliani', 'Impaginato dell’atto', 'Impaginato A4 dell’atto di divorzio (art. 39)'),
    (r'Spalla|Scheletro|Blank_A4|^Full$|GenericPDF|Estratti_Blank', 'Impaginato dell’atto',
     'Modello di pagina su cui si stampa il testo dell’atto (intestazione, corpo, annotazioni a '
     'spalla); il testo lo compone PKG_FORMULARI'),
    (r'COPIA_CONFORME', 'Copia conforme', 'Impaginato della copia conforme dell’atto'),
    (r'Estratto|Plurilingue', 'Estratto / certificato', 'Estratto dell’atto o certificato '
     '(anche plurilingue) rilasciato a chi lo richiede'),
    (r'Bassott', 'Cartellino anagrafico («bassottino»)', 'Cartellino per lo schedario anagrafico '
     'con i dati della variazione di cittadinanza'),
    (r'PropostaAnnot|Proposta di annotazione|Proposta(Roma|AltroComune)', 'Proposta di annotazione',
     'Proposta di annotazione inviata all’ufficio (di Roma o di altro comune) che detiene l’atto da '
     'annotare'),
    (r'Annotazione|Riconciliazione|CessazioneDellaSeparazione', 'Annotazione',
     'Testo o comunicazione di un’annotazione sull’atto'),
    (r'RichiestaAnnotazione', 'Richiesta di annotazione', 'Richiesta di annotazione ad altro comune'),
    (r'ComunicazioniEntiVari', 'Comunicazione agli enti', 'Comunicazione dell’evento di cittadinanza '
     'agli enti interessati'),
    (r'Comunicazion|ComuneDiResidenza|Avviso|Risposta', 'Comunicazione',
     'Comunicazione dell’evento a un altro ufficio o ente'),
    (r'Lettera|Promemoria|Indicatore', 'Lettera', 'Lettera di accompagnamento o di avviso'),
    (r'Ricevuta', 'Ricevuta', 'Ricevuta rilasciata al cittadino o all’incaricato'),
    (r'Busta', 'Busta', 'Busta per la spedizione'),
    (r'Cartellin', 'Cartellina', 'Cartellina del fascicolo della pratica'),
    (r'Verbale|Formula|Giuramento|Attestazion|Attestato|Certificazione|Certificato',
     'Verbale / formula / attestazione', 'Documento che si legge o si firma durante il procedimento'),
    (r'Permesso|Autorizzazione', 'Autorizzazione', 'Autorizzazione rilasciata dall’ufficiale'),
    (r'Trascrizione|Conferma', 'Trascrizione', 'Documento della trascrizione di un atto o della sua '
     'conferma'),
    (r'Richiesta|Nulla', 'Richiesta / nulla osta', 'Richiesta ad altro ufficio o nulla osta'),
    (r'Timbro|timbro|Copertina|Chiusura|foglioAggiuntivo|Registri', 'Registri e timbri',
     'Stampa di servizio per i registri (timbri, copertine, chiusure, fogli aggiuntivi)'),
]


def categoria(nome):
    for rx, cat, scopo in CATEGORIE:
        if re.search(rx, nome):
            return cat, scopo
    return 'Altro', ''


def parole(nome):
    """`869_AutorizzazioneAllaSepoltura_VERTICALE` -> `Autorizzazione alla sepoltura`."""
    n = re.sub(r'^\d+_', '', nome)
    n = re.sub(r'_(VERTICALE|VUOTO)$', '', n)
    n = n.replace('_', ' ')
    n = re.sub(r'(?<=[a-zàèéìòù])(?=[A-Z])', ' ', n)
    n = re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', ' ', n)
    n = re.sub(r'\s+', ' ', n).strip()
    return n[:1].upper() + n[1:].lower() if n.isupper() is False and len(n) > 1 else n


def leggi_jrxml(path):
    s = open(path, encoding='utf-8', errors='replace').read()
    testa = re.search(r'<jasperReport[^>]*', s).group(0)
    attr = dict(re.findall(r'(\w+)="([^"]*)"', testa))
    w, h = int(attr.get('pageWidth', 0) or 0), int(attr.get('pageHeight', 0) or 0)
    formato = {(595, 842): 'A4', (842, 595): 'A4', (842, 1190): 'A3', (1190, 842): 'A3',
               (420, 595): 'A5', (595, 420): 'A5'}.get((w, h), '%dx%d' % (w, h))
    verso = 'orizzontale' if w > h else 'verticale'
    testi = [html.unescape(re.sub('<[^>]+>', ' ', x)) for x in
             re.findall(r'<text><!\[CDATA\[(.*?)\]\]>', s, re.S)]
    testi += [html.unescape(re.sub('<[^>]+>', ' ', x)) for x in
              re.findall(r'"([^"$]{6,})"', ' '.join(
                  re.findall(r'<textFieldExpression><!\[CDATA\[(.*?)\]\]>', s, re.S)))]
    oggetto = ''
    for t in testi:
        m = re.search(r'OGGETTO\s*:?\s*(.+)', t, re.I)
        if m and len(m.group(1).strip()) > 3:
            oggetto = re.sub(r'\s+', ' ', m.group(1)).strip()[:200]
            break
    return {'report': attr.get('name', ''), 'formato': formato + ' ' + verso,
            'campi': len(re.findall(r'<field ', s)), 'oggetto': oggetto}


def stato_civile():
    righe = []
    for cart in sorted(os.listdir(SC)) + ['.']:
        p = os.path.join(SC, cart)
        if cart != '.' and not os.path.isdir(p):
            continue
        nomi = defaultdict(set)
        for f in os.listdir(p):
            b, e = os.path.splitext(f)
            if e in ('.jrxml', '.jasper'):
                nomi[b].add(e[1:])
        for b in sorted(nomi, key=lambda x: (int(re.match(r'\d*', x).group(0) or 10 ** 6), x)):
            m = re.match(r'(\d+)_', b)
            info = leggi_jrxml(os.path.join(p, b + '.jrxml')) if 'jrxml' in nomi[b] else {}
            cat, scopo = categoria(b)
            nota = []
            if b.endswith('_VERTICALE'):
                nota.append('variante verticale')
            if re.search(r'VUOTO|Test_|Scheletro', b):
                nota.append('modello di prova o vuoto')
            if not m:
                nota.append('senza ID nel nome')
            righe.append([AREA.get(cart, cart), int(m.group(1)) if m else None, b, parole(b), cat,
                          scopo, info.get('oggetto', ''), info.get('formato', ''),
                          info.get('campi', ''), ' + '.join(sorted(nomi[b])),
                          '; '.join(nota),
                          os.path.relpath(os.path.join(p, b), RADICE)])
    return righe


_INDICE = {}


def indice(radici):
    """Una sola passata sui sorgenti Java: costante ID_* -> moduli che la citano."""
    chiave = tuple(radici)
    if chiave in _INDICE:
        return _INDICE[chiave]
    idx = defaultdict(set)
    rx = re.compile(r'\b(ID_(?:DOC_)?\w+)\b')
    for rad in radici:
        for dirp, dirs, fs in os.walk(os.path.join(RADICE, rad)):
            dirs[:] = [d for d in dirs if d not in ('target', 'node_modules', '.git')]
            for f in fs:
                if not f.endswith('.java') or f in ('ConstantDoc.java', 'Constant.java'):
                    continue
                try:
                    s = open(os.path.join(dirp, f), encoding='utf-8', errors='replace').read()
                except OSError:
                    continue
                if 'ConstantDoc' not in s:
                    continue
                pz = os.path.relpath(dirp, RADICE).split(os.sep)
                mod = '/'.join(pz[:3] if pz[0] == 'sipo-root' and pz[1] == 'sipo-elezioni' else pz[:2])
                for c in set(rx.findall(s)):
                    idx[c].add(mod)
    _INDICE[chiave] = idx
    return idx


def moduli_che_usano(costante, radici):
    return ', '.join(sorted(m for m in indice(radici).get(costante, ())
                          if m not in ('common/pdf-generator', 'common/pdf-gen-elett',
                                        'sipo-root/sipo-elezioni/pdf-gen-elett-elezioni')))


def catalogo(path, radici):
    s = open(path, encoding='utf-8').read()
    ids = re.findall(r'int\s+(ID_\w+)\s*=\s*(\d+)', s)
    files = dict(re.findall(r'String\s+(FILENAME_\w+)\s*=\s*"([^"]*)"', s))
    righe = []
    for nome, val in ids:
        chiave = nome.replace('ID_DOC_', '').replace('ID_', '')
        fn = ''
        for k, v in files.items():
            if k.replace('FILENAME_DOC_', '').replace('FILENAME_', '').strip('_') == chiave:
                fn = v
                break
        righe.append([int(val), nome, parole(chiave.title().replace('_', '')).capitalize(), fn,
                      moduli_che_usano(nome, radici)])
    return sorted(righe)


SIGLE = {'PRES': 'presidente', 'SCRUT': 'scrutatore', 'OR': 'sezione ordinaria',
         'SP': 'sezione speciale', 'BAL': 'ballottaggio', 'SUPPLETIVE': 'elezioni suppletive',
         'SUP': 'suppletive', 'AIRE': 'AIRE'}


def leggibile_signps(nome):
    p = nome[len('ID_TEMPLATE_'):].split('_')
    return ' '.join(SIGLE.get(x, x.lower()) for x in p).capitalize()


def signps():
    righe = []
    for dirp, _, fs in os.walk(CONST_SIG):
        for f in fs:
            if f == 'Constant.java':
                s = open(os.path.join(dirp, f), encoding='utf-8', errors='replace').read()
                for nome, val in re.findall(r'Integer\s+(ID_TEMPLATE_\w+)\s*=\s*(\d+)', s):
                    righe.append([int(val), nome, leggibile_signps(nome), 'cross/Signps'])
    return sorted(set(map(tuple, righe)))


def foglio(wb, titolo, testata, righe, larghezze):
    ws = wb.create_sheet(titolo)
    ws.append(testata)
    for r in righe:
        ws.append(list(r))
    for i, w in enumerate(larghezze, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for c in ws[1]:
        c.font = Font(bold=True, color='FFFFFF')
        c.fill = PatternFill('solid', fgColor='8C0029')
        c.alignment = Alignment(wrap_text=True, vertical='top')
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical='top')
    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = ws.dimensions
    return ws


sc = stato_civile()
ana = catalogo(CONST_ANA, ['back-end', 'front-end', 'common'])
ele = catalogo(CONST_ELE, ['back-end', 'front-end', 'common', 'sipo-root'])
sig = signps()

# ------------------------------------------------------------ elenco unico: stampa e modulo
FE_SC = {'Nascite': 'Nascite (nascita-web)', 'Decessi': 'Decessi (decessi-web)',
         'Matrimoni': 'Matrimoni (matrim-web)', 'PubblicazioniStampaModelli': 'Matrimoni (matrim-web)',
         'Unioni': 'Unioni civili (unioni-web)', 'Divozi': 'Divorzi (divorzi-web)',
         'Cittadinanza': 'Cittadinanza (cittadinanza-web)',
         'Annotazioni': 'Annotazioni (annotazioni-web)', 'Esponente': 'Esponente (esponente-web)',
         'Estratto': 'Stato civile (statocivile-web)', 'Spalla': 'Stato civile, tutte le aree (statocivile-web)'}


def modulo_sc(percorso, nome):
    cart = percorso.split('/')[-2]
    if cart == 'jasper_templates':
        cart = '.'
    if cart == '.':
        if re.search(r'Matrimon|Pubblicazione|Promessa|NullaOsta|Giuramento|Parroco', nome):
            fe = 'Matrimoni (matrim-web)'
        elif 'Seppelliment' in nome:
            fe = 'Decessi (decessi-web)'
        elif 'Annotazione' in nome:
            fe = 'Annotazioni (annotazioni-web)'
        elif 'Agenda' in nome:
            fe = 'Agenda di stato civile (agendasc-web)'
        else:
            fe = 'Stato civile, tutte le aree (statocivile-web)'
    else:
        fe = FE_SC.get(cart, cart)
    if 'Bassott' in nome:
        be = 'cittadinanza-be'
    elif re.match(r'(1022_)?Annotazione', nome) or nome.startswith('1022_'):
        be = 'annotazioni-be'
    elif cart == 'Esponente':
        be = 'esponente-be'
    elif 'Agenda' in nome:
        be = 'statocivile-be / matrim-be'
    else:
        be = 'statocivile-be'
    return fe, be


def moduli(usata):
    m = [x.split('/')[-1] for x in (usata or '').split(', ') if x]
    web = lambda x: '-web' in x
    fe = ', '.join(x for x in m if web(x))
    be = ', '.join(x for x in m if not web(x))
    return fe or '—', be or ('generata dal front-end' if fe else '—')


elenco = []
for r in sc:
    fe, be = modulo_sc(r[11], r[2])
    elenco.append([r[2], fe, be, 'Stato civile (pdf-gen-sc)', r[1], r[10]])
for r in ana:
    fe, be = moduli(r[4])
    nota = 'manuale in PDF, non una stampa' if 'MANUALE' in r[1] or 'FORMAZIONE' in r[1] else (
        '' if r[4] else 'costante non usata fuori dal generatore')
    elenco.append([r[3] or r[2], fe, be, 'Anagrafe (pdf-generator)', r[0], nota])
for r in ele:
    fe, be = moduli(r[4])
    elenco.append([r[3] or r[2], fe, be, 'Elettorale (pdf-gen-elett)', r[0],
                   '' if r[4] else 'costante non usata fuori dal generatore'])
for r in sig:
    elenco.append([r[2], 'Albo e nomine di seggio (Signps)', 'Signps', 'Seggi (Signps)', r[0],
                   'manuale in PDF, non una stampa' if 'MANUALE' in r[1] else ''])

wb = openpyxl.Workbook()
leg = wb.active
leg.title = 'Legenda'
for r in [
    ['Inventario delle stampe JasperReports di SIPO'],
    [],
    ['Generatore', 'Modulo', 'Dove sta il modello', 'Stampe'],
    ['Stato civile', 'common/pdf-gen-sc (PdfGenerator)', 'tabella TEMPLATE (blob), scelto per area e '
     'modello da CONF_TIPO_MODELLO_ATTO, CONF_TIPO_STAMPA, CONF_TIPO_COMUNICAZIONI_MATR o per ID nel '
     'codice; copia dei sorgenti in jasper_templates/', '%d modelli su file' % len(sc)],
    ['Anagrafe, certificati, leva, AIRE, irreperibilità', 'common/pdf-generator (GeneraDocumento)',
     'solo tabella TEMPLATE; ID dalle costanti ConstantDoc.ID_DOC_*', '%d ID' % len(ana)],
    ['Elettorale', 'common/pdf-gen-elett (GeneraDocumentoElettorale) e la copia in sipo-root/'
     'sipo-elezioni', 'solo tabella TEMPLATE; ID dalle costanti ConstantDoc.ID_DOC_*',
     '%d ID' % len(ele)],
    ['Albo e nomine dei componenti di seggio', 'cross/Signps (GeneraPdf)',
     'tabella TEMPLATE per elezione e tipo (getTemplateByIdElezioneEIdTipoTempalte)', '%d ID' % len(sig)],
    ['Annotazioni', 'back-end/annotazioni-be (PdfGenerator proprio)', 'tabella TEMPLATE, come lo '
     'stato civile', 'modelli in jasper_templates/Annotazioni'],
    [],
    ['Avvertenze'],
    ['1. Il contenuto della tabella TEMPLATE e delle tabelle di configurazione non è fra le sorgenti: '
     'non si può dire quali modelli siano in esercizio. I file di jasper_templates/ non sono letti '
     'dal codice (nessun riferimento): sono la copia di lavoro di ciò che si carica nella tabella.'],
    ['2. Nello stato civile il numero in testa al nome del file è l’ID_TEMPLATE (verificato: 8 = '
     'verbale delle unioni e 9 = divorzi italiani art. 39 in ScConstantsBE).'],
    ['3. La colonna «A che cosa serve» è ricavata dal nome del modello e dalla riga «OGGETTO» del '
     'modello quando c’è: è un’indicazione, non la descrizione ufficiale della stampa.'],
    ['4. Anteprima e atto definitivo sono lo stesso modello: cambia lo sfondo (filigrana «ANTEPRIMA» '
     'o foglio bianco).'],
    ['5. Per anagrafe ed elettorale la colonna «Usata da» elenca i moduli che citano la costante.'],
]:
    leg.append(r)
leg['A1'].font = Font(bold=True, size=14)
for c in leg[3]:
    c.font = Font(bold=True)
for col, w in zip('ABCD', (38, 45, 70, 20)):
    leg.column_dimensions[col].width = w
for row in leg.iter_rows():
    for c in row:
        c.alignment = Alignment(wrap_text=True, vertical='top')

foglio(wb, 'Elenco completo', ['Stampa (modello o file prodotto)', 'Modulo (front-end)', 'Back-end che la genera', 'Generatore', 'ID_TEMPLATE', 'Note'], elenco, (55, 40, 40, 26, 12, 34))
foglio(wb, 'Stato civile', ['Area', 'ID_TEMPLATE', 'Modello', 'Nome leggibile', 'Categoria',
                            'A che cosa serve', 'OGGETTO nel modello', 'Pagina', 'Campi',
                            'File', 'Note', 'Percorso'],
       sc, (22, 11, 42, 40, 24, 50, 45, 16, 7, 13, 22, 60))
foglio(wb, 'Anagrafe e certificati', ['ID_TEMPLATE', 'Costante', 'Stampa', 'Nome del file prodotto',
                                      'Usata da'], ana, (11, 42, 45, 45, 60))
foglio(wb, 'Elettorale', ['ID_TEMPLATE', 'Costante', 'Stampa', 'Nome del file prodotto', 'Usata da'],
       ele, (11, 48, 45, 45, 60))
foglio(wb, 'Seggi (Signps)', ['ID tipo template', 'Costante', 'Stampa', 'Modulo'], sig,
       (14, 48, 45, 20))
wb.save(OUT)
print('elenco', len(elenco), '· stato civile', len(sc), '· anagrafe', len(ana), '· elettorale', len(ele), '· seggi', len(sig))
print('scritto', os.path.relpath(OUT, RADICE))
