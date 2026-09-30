# -*- coding: utf-8 -*-
"""Verifica i conteggi dichiarati in prosa contro le tabelle e la struttura reale del .docx,
e segnala i riferimenti pendenti (OP-nn, PC-n, RF-n, RNF-n, [Rn]) citati ma non definiti.

    /usr/bin/python3 "Documenti finali/verifica-conteggi.py" "Documenti finali/ANALISI_....docx"

Esce con codice 1 se trova almeno una discordanza: si può inserire in un controllo automatico.
Nasce dal fatto che i numeri scritti in prosa non si aggiornano da soli quando si aggiunge una
riga a una tabella, ed è la classe di errore piu' frequente su questo documento.
"""
import re
import sys
import unicodedata

import docx

# ------------------------------------------------------------------ numeri
PAROLE = {
    'un': 1, 'uno': 1, 'una': 1, 'due': 2, 'tre': 3, 'quattro': 4, 'cinque': 5, 'sei': 6,
    'sette': 7, 'otto': 8, 'nove': 9, 'dieci': 10, 'undici': 11, 'dodici': 12, 'tredici': 13,
    'quattordici': 14, 'quindici': 15, 'sedici': 16, 'diciassette': 17, 'diciotto': 18,
    'diciannove': 19, 'venti': 20, 'ventuno': 21, 'ventidue': 22, 'ventitre': 23,
    'ventiquattro': 24, 'venticinque': 25, 'ventisei': 26, 'ventisette': 27, 'ventotto': 28,
    # NB: le varianti accentate servono alla REGEX, che si costruisce dalle chiavi;
    # valore() normalizzerebbe da solo, ma se la parola non e' fra le chiavi non viene
    # nemmeno agganciata nel testo.
    'ventitré': 23, 'ventitrè': 23, 'trentatré': 33, 'quarantatré': 43,
    'ventinove': 29, 'trenta': 30, 'trentuno': 31, 'quaranta': 40, 'quarantacinque': 45,
    'quarantotto': 48, 'cinquanta': 50, 'cinquantasette': 57, 'novanta': 90, 'cento': 100,
    'centoundici': 111,
}
# Il lookbehind impedisce di agganciare la coda di una parola piu' lunga:
# senza, in 'quarantotto' la regex trovava 'otto' e leggeva 8.
NUM = (r'(?<![0-9A-Za-z\u00c0-\u017f])(?:\d[\d.]*|'
       + '|'.join(sorted(PAROLE, key=len, reverse=True)) + r')')


def valore(testo):
    t = unicodedata.normalize('NFKD', testo.strip().lower())
    t = ''.join(c for c in t if not unicodedata.combining(c))
    if t in PAROLE:
        return PAROLE[t]
    cifre = t.replace('.', '')
    return int(cifre) if cifre.isdigit() else None


# ------------------------------------------------------------------ accesso
class Doc:
    def __init__(self, path):
        self.d = docx.Document(path)
        self.paragrafi = [p for p in self.d.paragraphs if p.text.strip()]
        self.prosa = '\n'.join(p.text for p in self.paragrafi)
        # La Storia del Documento cita per mestiere le formulazioni superate («…prima diceva X…»):
        # scandirla produrrebbe una discordanza a ogni riga di changelog. Va esclusa.
        self.storia = self._storia()
        # NB: document.tables restituisce un oggetto Table nuovo a ogni accesso, quindi il
        # confronto per identità non funziona: si confronta l'elemento XML sottostante.
        escluso = self.storia._tbl if self.storia is not None else None
        self.celle = '\n'.join(c.text for t in self.d.tables if t._tbl is not escluso
                               for r in t.rows for c in r.cells)
        self.testo = self.prosa + '\n' + self.celle

    def _storia(self):
        for t in self.d.tables:
            testa = ' | '.join(c.text.strip().lower() for c in t.rows[0].cells)
            if 'versione' in testa and 'sintesi dei cambiamenti' in testa:
                return t
        return None

    def h1(self):
        return [p.text.strip() for p in self.paragrafi if p.style.name == 'Heading 1']

    def heading(self, livello):
        return [p.text.strip() for p in self.paragrafi
                if p.style.name == f'Heading {livello}']

    def tabella(self, *intestazioni):
        """Prima tabella la cui riga di intestazione contiene tutte le stringhe date."""
        for t in self.d.tables:
            testa = ' | '.join(c.text.strip() for c in t.rows[0].cells)
            if all(i.lower() in testa.lower() for i in intestazioni):
                return t
        return None

    def righe(self, *intestazioni, filtro=None, colonna=0):
        t = self.tabella(*intestazioni)
        if t is None:
            return None
        corpo = t.rows[1:]
        if filtro:
            corpo = [r for r in corpo if filtro(r.cells[colonna].text.strip(), r)]
        return len(corpo)


# ------------------------------------------------------------------ regole
def pod_certi(doc):
    return doc.righe('Componente', 'Unità di deployment',
                     filtro=lambda n, r: r.cells[-1].text.strip().lower().startswith('s')
                     and 'eventuale' not in r.cells[-1].text.lower())


def concentratori(doc):
    return doc.righe('Componente', 'Responsabilità',
                     filtro=lambda n, r: n.lower().startswith('concentratore'))


def operazioni_appendice(doc):
    tot = 0
    for t in doc.d.tables:
        if t.rows[0].cells[0].text.strip().lower().startswith('metodo e percorso'):
            tot += len(t.rows) - 1
    return tot or None


def responsabilita_concentratore(doc):
    """Conta gli elementi elencati nella frase «Il concentratore ha N responsabilità: a; b; e c»."""
    m = re.search(r'concentratore ha \w+ responsabilità[^:]*:(.+?)(?<!ecc)\.\s', doc.prosa, re.S)
    if not m:
        return None
    return m.group(1).count(';') + 1


def _decodifiche(pattern):
    """Conteggi verificati sul repository ANSC, se raggiungibile dalla cartella del documento."""
    import glob
    import os
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = sorted(glob.glob(os.path.join(base, 'ansc', 'docs', 'Decodifiche', '*.csv')))
    if not files:
        return None
    if pattern == 'file':
        return len(files)
    if pattern == 'identificativi':
        return len({os.path.basename(f).split('_', 1)[0] for f in files})
    if pattern == 'righe':
        tot = 0
        for f in files:
            righe = [r for r in open(f, encoding='utf-8-sig', errors='replace')
                     .read().splitlines() if r.strip()]
            tot += max(0, len(righe) - 1)
        return tot
    return None


def _mapping(cosa):
    """Conteggi verificati sul mapping ufficiale dei casi d'uso ANSC."""
    import csv
    import glob
    import os
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    radice = os.path.join(base, 'ansc', 'docs', 'Mapping_casi_uso')
    files = sorted(glob.glob(os.path.join(radice, '*', '*.csv')))
    if not files:
        return None
    if cosa == 'casi':
        return len(files)
    blocchi, collegati, due_intestatari, obbligatori = set(), 0, 0, 0
    all_uc, all_righe, all_obbl, all_cond, all_desc = 0, 0, 0, 0, set()
    formula_uc = 0
    recupero = 0  # mapping in cui evento.motivoRecupero e' dichiarato obbligatorio
    for f in files:
        testo = open(f, encoding='utf-8-sig', errors='replace').read()
        if re.search(r'evento\.(eventoCollegato|eventoPrimario|attiCollegati)', testo):
            collegati += 1
        if re.search(r'intestatari\[1\]', testo):
            due_intestatari += 1
        obbl_recupero = False
        ha_allegato = ha_formula = False
        for r in csv.DictReader(open(f, encoding='utf-8-sig', errors='replace')):
            sezione = (r.get('Sezione') or '').strip().lower()
            if sezione == 'allegati':
                ha_allegato = True
                all_righe += 1
                all_desc.add((r.get('Campo') or '').strip())
                if (r.get('Obbligatorio') or '').strip().upper() in ('SI', 'SÌ', 'S'):
                    all_obbl += 1
                if (r.get("Condizioni obbligatorieta'") or
                        r.get("Si puo' ignorare la sezione per") or '').strip():
                    all_cond += 1
            elif sezione == 'formula':
                ha_formula = True
            if (r.get('Obbligatorio') or '').strip().upper() in ('SI', 'SÌ', 'S', 'X', 'TRUE'):
                obbligatori += 1
                if 'motivoRecupero' in (r.get('Binding Field') or ''):
                    obbl_recupero = True
            m = re.match(r'evento\.([A-Za-z]+)', (r.get('Binding Object') or '').strip())
            if m:
                blocchi.add(m.group(1))
        recupero += 1 if obbl_recupero else 0
        all_uc += 1 if ha_allegato else 0
        formula_uc += 1 if ha_formula else 0
    return {'blocchi': len(blocchi), 'collegati': collegati,
            'due': due_intestatari, 'obbligatori': obbligatori,
            'recupero': recupero, 'all_uc': all_uc, 'all_righe': all_righe,
            'all_obbl': all_obbl, 'all_cond': all_cond, 'all_desc': len(all_desc),
            'formula_uc': formula_uc}.get(cosa)


def _nascite(cosa):
    """Conteggi verificati sulla ricognizione delle nascite (Sorgenti Documentali).

    Il foglio ha due blocchi: la mappa UC-Modello (righe 3..N) e la mappatura dei campi
    (dalla riga che porta 'SIPO' in colonna A). Si legge solo il primo.
    """
    import glob
    import os
    try:
        import openpyxl
    except ImportError:
        return None
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    trovati = [f for f in glob.glob(os.path.join(base, 'Sorgenti Documentali',
                                                 'Nascite_ANSC_*.xlsx'))
               if not os.path.basename(f).startswith('~$')]
    if not trovati:
        return None
    wb = openpyxl.load_workbook(sorted(trovati)[-1], data_only=True)
    uc, con_modello, modelli = set(), set(), set()
    for foglio in wb.sheetnames[1:]:
        ws = wb[foglio]
        fine = next((r for r in range(4, 60)
                     if str(ws.cell(row=r, column=1).value).strip() == 'SIPO'), 25)
        for r in range(3, fine - 1):
            codice = ws.cell(row=r, column=2).value
            if not codice:
                continue
            uc.add(str(codice))
            modello = ws.cell(row=r, column=9).value
            if modello is not None:
                con_modello.add(str(codice))
                modelli.add(str(modello).strip())
    return {'uc': len(uc), 'con_modello': len(con_modello), 'modelli': len(modelli),
            'senza_modello': len(uc) - len(con_modello)}.get(cosa)


def _changelog(cosa):
    """Conteggi verificati sui changelog che ANSC pubblica a ogni rilascio.

    Sono la fonte del capitolo sul versionamento della configurazione: il changelog del
    mapping e' generato, quindi i conteggi si ricavano dalla sua grammatica fissa.
    """
    import glob
    import os
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    radice = os.path.join(base, 'ansc', 'docs')
    if cosa == 'rilasci':
        f = os.path.join(radice, 'Changelog.md')
        if not os.path.exists(f):
            return None
        testo = open(f, encoding='utf-8', errors='replace').read()
        return len(re.findall(r'^## \[[0-9.]+\s*-\s*\d{2}-\d{2}-\d{4}\]', testo, re.M))
    files = sorted(glob.glob(os.path.join(radice, 'Mapping_casi_uso', 'changelog_mapping*.md')))
    if not files:
        return None
    testo = '\n'.join(open(f, encoding='utf-8', errors='replace').read() for f in files)
    if cosa == 'revisioni':
        return len(re.findall(r'^#Changelog mappatura casi uso', testo, re.M))
    if cosa == 'uc_toccati':
        return len(set(re.findall(r'^### Modifiche per il caso uso (\S+)', testo, re.M)))
    if cosa == 'ritirati':
        return sum(int(n) for n in re.findall(r'^## Casi uso rimossi\s*:\s*(\d+)', testo, re.M))
    return None


def _contratti(cosa):
    """Conteggi verificati sui contratti OpenAPI pubblicati da ANSC."""
    import glob
    import os
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    radice = os.path.join(base, 'ansc', 'docs', 'openapi')
    if cosa == 'errori':
        try:
            import openpyxl
        except ImportError:
            return None
        f = os.path.join(radice, "Codici d'errore.xlsx")
        if not os.path.exists(f):
            return None
        ws = openpyxl.load_workbook(f)['Sheet1']
        return sum(1 for r in ws.iter_rows(min_row=2, values_only=True) if r[0])
    try:
        import yaml
    except ImportError:
        return None
    if cosa in ('evento', 'deprecate'):
        f = os.path.join(radice, 'model_evento.yaml')
        if not os.path.exists(f):
            return None
        if cosa == 'deprecate':
            return open(f, encoding='utf-8').read().count('deprecated: true')
        d = yaml.safe_load(open(f, encoding='utf-8'))
        return len(d['components']['schemas']['ModelEvento']['properties'])
    files = sorted(glob.glob(os.path.join(radice, 'R*.yaml')))
    if not files:
        return None
    ops = []
    for f in files:
        d = yaml.safe_load(open(f, encoding='utf-8'))
        for percorso, voci in (d.get('paths') or {}).items():
            for metodo in voci:
                if metodo in ('get', 'post', 'put', 'delete', 'patch'):
                    ops.append(percorso)
    if cosa == 'operazioni':
        return len(ops)
    if cosa == 'contratti':
        return len(files)
    if cosa == 'schede':
        # i servizi con una scheda di sviluppo: tutti tranne i due del canale sanitario
        return len({os.path.basename(f).split('_')[0] for f in files}) - 2
    if cosa == 'deposito':
        return sum(1 for p in ops if 'validazione' in p and not p.startswith('/dmnm'))
    return None


REGOLE = [
    ('UC nascite con Modello (back-office)', rf'UC da catalogare[^0-9]*({NUM})',
     lambda d: _nascite('con_modello'), 'UC con Modello nella ricognizione nascite'),
    ('UC censiti nelle nascite', rf'censisce ({NUM}) UC',
     lambda d: _nascite('uc'), 'codici UC distinti nella ricognizione delle nascite'),
    ('UC con Modello', rf'dei quali ({NUM}) riconducibili',
     lambda d: _nascite('con_modello'), 'UC con ID_MODELLO_ATTO valorizzato'),
    ('Modelli distinti', rf'riconducibili a ({NUM}) Modelli distinti',
     lambda d: _nascite('modelli'), 'valori distinti di ID_MODELLO_ATTO'),
    ('UC senza Modello', rf'({NUM}) UC non hanno alcun Modello',
     lambda d: _nascite('senza_modello'), 'UC senza ID_MODELLO_ATTO'),
    ('casi d\'uso pubblicati', rf'mapping ufficiale per ({NUM}) UC',
     lambda d: _mapping('casi'), 'file .csv in ansc/docs/Mapping_casi_uso/'),
    ('blocchi del modello evento', rf'({NUM}) blocchi distinti',
     lambda d: _mapping('blocchi'), 'radici «evento.<blocco>» distinte nel mapping'),
    ('casi con evento collegato', rf'({NUM}) UC su {NUM} valorizzano un evento collegato',
     lambda d: _mapping('collegati'), 'casi d’uso che citano eventoCollegato/eventoPrimario/attiCollegati'),
    ('casi con due intestatari', rf'({NUM}) UC su {NUM} valorizzano un secondo soggetto',
     lambda d: _mapping('due'), 'casi d’uso che valorizzano intestatari[1]'),
    ('campi obbligatori dichiarati', rf'({NUM}) campi obbligatori dichiarati',
     lambda d: _mapping('obbligatori'), 'righe con Obbligatorio = SI nel mapping'),
    ('flussi di traffico', rf'Si distinguono ({NUM}) flussi',
     lambda d: d.righe('Flusso', 'Direzione'), 'righe della tabella dei flussi'),
    ('unità di deployment nuove', rf'({NUM}) unità di deployment nuove',
     pod_certi, 'righe «Sì» non eventuali nella tabella dei componenti'),
    ('unità applicative nuove', rf'unità applicative nuove sono ({NUM})',
     pod_certi, 'righe «Sì» non eventuali nella tabella dei componenti'),
    ('concentratori', rf'({NUM}) sono concentratori',
     concentratori, 'righe «Concentratore…» nella tabella dei componenti'),
    # regola nata dall'errore della v2.6: §4.1 dichiarava «due componenti nuovi» mentre la
    # tabella ne marcava quattro come nuovi, e il processo di automazione non vi compariva
    ('componenti nuovi', rf'({NUM}) componenti nuovi',
     lambda d: d.righe('Componente', 'Responsabilità',
                       filtro=lambda n, r: '(nuovo' in n.lower()),
     'righe marcate «(nuovo)» nella tabella dei componenti'),
    ('responsabilità del concentratore', rf'concentratore ha ({NUM}) responsabilità',
     responsabilita_concentratore, 'elementi separati da punto e virgola nella stessa frase'),
    ('open point', rf'Open Point[,:]? ({NUM}) voci',
     lambda d: d.righe('Tema', 'Questione'), 'righe del registro degli open point'),
    ('requisiti funzionali', rf'RF-1…\s*(?:\*\*)?RF-({NUM})',
     lambda d: d.righe('ID', 'Requisito', 'Nota'), 'righe dei requisiti funzionali'),
    ('operazioni in appendice', rf'operazioni passano da {NUM} a ({NUM})',
     operazioni_appendice, 'righe delle tabelle di inventario delle operazioni'),
    ('categorie di eccezione', rf'({NUM}) categorie di eccezione',
     lambda d: d.righe('Categoria', 'Stato reale'), 'righe della tabella delle categorie'),
    ('capitoli', rf'(?:consta di|si compone di|si articola in|comprende) ({NUM}) capitoli',
     lambda d: len(d.h1()), 'heading di primo livello'),
    ('file di decodifica pubblicati', rf'pubblica ({NUM}) file di decodifica',
     lambda d: _decodifiche('file'), 'file .csv in ansc/docs/Decodifiche/'),
    ('identificativi di decodifica distinti', rf'su ({NUM}) identificativi distinti',
     lambda d: _decodifiche('identificativi'), 'prefissi numerici distinti dei file .csv'),
    ('righe di decodifica', rf'per ({NUM}) righe di dato',
     lambda d: _decodifiche('righe'), 'righe dei .csv al netto delle intestazioni'),
    ('rilasci ANSC datati', rf'Rilasci ANSC datati[^0-9]*({NUM})',
     lambda d: _changelog('rilasci'), 'intestazioni datate in Changelog.md'),
    ('revisioni del mapping', rf'({NUM}), pari a circa {NUM} l’anno',
     lambda d: _changelog('revisioni'), 'revisioni nei changelog del mapping'),
    ('UC toccati almeno una volta', rf'({NUM}) su {NUM}, il {NUM} % del catalogo',
     lambda d: _changelog('uc_toccati'), 'UC distinti citati nei changelog del mapping'),
    ('UC ritirati', rf'UC ritirati dall’avvio del sistema[^0-9]*({NUM})',
     lambda d: _changelog('ritirati'), 'casi uso rimossi dichiarati nei changelog'),
    ('operazioni dei servizi ANSC (prosa)', rf'Fra le ({NUM}) operazioni',
     lambda d: _contratti('operazioni'), 'operazioni nei contratti ansc/docs/openapi/'),
    ('operazioni dei servizi ANSC (tabella)', rf'Operazioni complessive[^0-9]*({NUM})',
     lambda d: _contratti('operazioni'), 'operazioni nei contratti ansc/docs/openapi/'),
    ('contratti ANSC', rf'Contratti pubblicati[^0-9]*({NUM})',
     lambda d: _contratti('contratti'), 'file R*.yaml in ansc/docs/openapi/'),
    ('proprieta del modello evento', rf'({NUM}) proprietà di primo livello',
     lambda d: _contratti('evento'), 'proprietà di primo livello di ModelEvento'),
    ('proprieta deprecate', rf'({NUM}) proprietà sono dichiarate deprecate',
     lambda d: _contratti('deprecate'), 'occorrenze di «deprecated: true» in model_evento.yaml'),
    ('codici di errore ANSC', rf'codici di errore pubblicati sono ({NUM})',
     lambda d: _contratti('errori'), "righe del foglio Codici d'errore.xlsx"),
    ('operazioni di deposito', rf'dentro ANSC sono ({NUM})',
     lambda d: _contratti('deposito'), 'percorsi di validazione evento, escluso il canale DMNM'),
    ('servizi con scheda di sviluppo', rf'schede coprono quindi ({NUM}) servizi',
     lambda d: _contratti('schede'), 'contratti R*.yaml meno i due del canale sanitario'),
    ('UC che dichiarano allegati', rf'almeno un allegato[^0-9]*({NUM})',
     lambda d: _mapping('all_uc'), 'mapping con almeno una riga «Allegati»'),
    ('righe di allegato', rf'Righe di allegato complessive[^0-9]*({NUM})',
     lambda d: _mapping('all_righe'), 'righe «Allegati» nei mapping'),
    ('allegati obbligatori', rf'Righe con allegato obbligatorio[^0-9]*({NUM})',
     lambda d: _mapping('all_obbl'), 'righe «Allegati» con Obbligatorio = SI'),
    ('allegati condizionati', rf'Righe con obbligatorietà condizionata[^0-9]*({NUM})',
     lambda d: _mapping('all_cond'), 'righe «Allegati» con una condizione'),
    ('descrizioni di allegato', rf'Descrizioni di allegato distinte[^0-9]*({NUM})',
     lambda d: _mapping('all_desc'), 'descrizioni distinte nei mapping'),
    ('UC con formule', rf'presenti in ({NUM}) UC su',
     lambda d: _mapping('formula_uc'), 'mapping con almeno una riga «Formula»'),
    ('mapping con motivo del recupero obbligatorio',
     rf'motivo del recupero è obbligatorio in\s+({NUM})',
     lambda d: _mapping('recupero'), 'mapping con evento.motivoRecupero obbligatorio'),
]


def controlla_conteggi(doc):
    esiti = []
    for nome, pattern, calcolo, nota in REGOLE:
        for m in re.finditer(pattern, doc.testo, re.IGNORECASE):
            dichiarato = valore(m.group(1))
            if dichiarato is None:
                continue
            atteso = calcolo(doc) if calcolo else None
            frase = re.sub(r'\s+', ' ', doc.testo[max(0, m.start() - 60):m.end() + 60]).strip()
            if atteso is None:
                esiti.append(('?', nome, dichiarato, '—', nota, frase))
            elif atteso != dichiarato:
                esiti.append(('KO', nome, dichiarato, atteso, nota, frase))
            else:
                esiti.append(('OK', nome, dichiarato, atteso, nota, frase))
    return esiti


# ------------------------------------------------- riferimenti pendenti
def definiti(doc, prefisso, intestazioni):
    t = doc.tabella(*intestazioni)
    if t is None:
        return set()
    return {c.text.strip().upper() for r in t.rows[1:]
            for c in (r.cells[0],) if c.text.strip().upper().startswith(prefisso)}


def controlla_riferimenti(doc):
    problemi = []

    coppie = [
        ('OP-', r'\bOP-(\d{1,3})\b', definiti(doc, 'OP-', ('Tema', 'Questione'))),
        ('RF-', r'\bRF-(\d{1,2})\b', definiti(doc, 'RF-', ('ID', 'Requisito', 'Nota'))),
        ('RNF-', r'\bRNF-(\d{1,2})\b', definiti(doc, 'RNF-', ('ID', 'Requisito', 'Valore'))),
    ]
    for prefisso, pattern, noti in coppie:
        if not noti:
            problemi.append(('?', f'tabella di definizione di {prefisso} non trovata', ''))
            continue
        citati = {f'{prefisso}{int(n):02d}' if prefisso == 'OP-' else f'{prefisso}{n}'
                  for n in re.findall(pattern, doc.testo)}
        normalizza = lambda s: s.replace('-0', '-').upper()
        mancanti = sorted({c for c in citati if normalizza(c) not in
                           {normalizza(x) for x in noti}})
        for m in mancanti:
            problemi.append(('KO', f'{m} citato ma non definito nella tabella', ''))

    # punti controversi: definiti come heading «PC-n — …»
    pc_def = {re.match(r'(PC-\d+)', h).group(1)
              for h in doc.heading(2) if re.match(r'PC-\d+', h)}
    pc_cit = set(re.findall(r'\bPC-\d+\b', doc.testo))
    for m in sorted(pc_cit - pc_def):
        problemi.append(('KO', f'{m} citato ma non esiste il paragrafo corrispondente', ''))

    # riferimenti bibliografici [Rn]
    rif = definiti(doc, 'R', ('ID', 'Riferimento', 'Contenuto'))
    if rif:
        cit = set(re.findall(r'\[(R\d+)\]', doc.testo))
        for m in sorted(cit - {r.upper() for r in rif}):
            problemi.append(('KO', f'[{m}] citato ma non presente in Riferimenti', ''))
    return problemi


# ------------------------------------------------------------ struttura
def controlla_struttura(doc):
    note = []
    hs = [p for p in doc.paragrafi if p.style.name.startswith('Heading')]
    lunghi = [h.text for h in hs if len(h.text) > 110]
    for t in lunghi:
        note.append(('KO', 'heading anomalo: contenuto finito in un titolo', t[:90]))
    for i, t in enumerate(doc.d.tables):
        vuote = [j for j, r in enumerate(t.rows[1:], 1)
                 if not any(c.text.strip() for c in r.cells)]
        if vuote:
            note.append(('KO', f'tabella {i}: righe completamente vuote',
                         f'righe {vuote} — intestazione «{t.rows[0].cells[0].text.strip()}»'))
    return note


# ------------------------------------------------------------------ main
def main(path):
    doc = Doc(path)
    print(f'Documento: {path}')
    print(f'  {len(doc.h1())} capitoli · {len(doc.d.tables)} tabelle · '
          f'{len(doc.d.inline_shapes)} immagini · {len(doc.paragrafi)} paragrafi\n')

    ko = 0
    print('CONTEGGI DICHIARATI IN PROSA')
    esiti = controlla_conteggi(doc)
    if not esiti:
        print('  nessuna affermazione numerica riconosciuta')
    for stato, nome, dich, att, nota, frase in esiti:
        simbolo = {'OK': '  ok  ', 'KO': '  KO  ', '?': '  ?   '}[stato]
        print(f'{simbolo}{nome}: dichiarato {dich}, atteso {att}   ({nota})')
        if stato != 'OK':
            print(f'        «…{frase}…»')
        ko += stato == 'KO'

    print('\nRIFERIMENTI')
    problemi = controlla_riferimenti(doc)
    if not problemi:
        print('  ok   nessun riferimento pendente')
    for stato, testo, extra in problemi:
        print(f'  {"KO" if stato == "KO" else "? "}   {testo}' + (f' — {extra}' if extra else ''))
        ko += stato == 'KO'

    print('\nSTRUTTURA')
    note = controlla_struttura(doc)
    if not note:
        print('  ok   nessun heading anomalo, nessuna riga di tabella vuota')
    for stato, testo, extra in note:
        print(f'  KO   {testo} — {extra}')
        ko += 1

    print(f'\n{"DISCORDANZE: " + str(ko) if ko else "Nessuna discordanza."}')
    return 1 if ko else 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
