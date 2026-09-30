# -*- coding: utf-8 -*-
"""ANALISI_Integrazione-ANSC v3.30 → v3.31 (29/09/2026).

Recepisce i due rilievi emersi disegnando il back-office (BO-13 e BO-14), entrambi
verificati sul contratto R901 e sul tracciato dei CSV pubblicati da ANSC.

  · DOMINIO_DECODIFICA acquisisce «cd_versione»: R901 la restituisce ed è l'unico modo
    per accorgersi che una decodifica è cambiata senza riscaricarla.
  · VALORE_DOMINIO perde «cd_valore» — il tracciato ha un solo identificativo — e
    acquisisce «tx_attributi» per le due colonne aggiuntive di consolati e casi d'uso.
  · RICONCILIAZ_DIZIONARI acquisisce SCHEMA_SIPO, TABELLA_SIPO e CAMPO_SIPO: il raccordo
    con le tabelle del Comune era descritto in prosa e non era un dato.

⚠️ Si modifica IL FILE REALE: la v3.30 porta 22 commenti di Word da preservare.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/diagrammi_erd.py img
    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_31_dizionari_e_raccordo.py
"""
import os
import shutil
import sys
import zipfile

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(BASE, 'Documenti finali', 'ANALISI_Integrazione-ANSC_v3.30.docx')
DST = os.path.join(BASE, 'Documenti finali', 'ANALISI_Integrazione-ANSC_v3.31.docx')
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')


def commenti(percorso):
    return zipfile.ZipFile(percorso).read('word/comments.xml').decode().count('<w:comment ')


def indice_ddl(d, tabella):
    """L'indice del paragrafo «CREATE TABLE … <tabella> (»."""
    for i, p in enumerate(d.paragraphs):
        if p.text.strip().startswith('CREATE TABLE') and tabella in p.text:
            return i
    raise SystemExit('DDL non trovata: ' + tabella)


def riga_dopo(d, dal_indice, testo):
    """Il primo paragrafo con quel testo esatto a partire da un indice: resta dentro il blocco."""
    for p in d.paragraphs[dal_indice:]:
        if p.text.rstrip() == testo.rstrip():
            return p
    raise SystemExit('riga non trovata dopo %d: %r' % (dal_indice, testo))


def inserisci_prima(d, par, righe):
    """Inserisce righe di DDL (carattere fisso) prima del paragrafo indicato."""
    for r in righe:
        D.para(d, par._p, r, mono=True)


def riga_di(tab, prima_cella):
    for r in tab.rows:
        if r.cells[0].text.strip() == prima_cella:
            return r
    raise SystemExit('riga di tabella non trovata: ' + prima_cella)


def scheda_con(d, *colonne):
    """La tabella «Colonna | Tipo | Note» che contiene quelle colonne."""
    for t in d.tables:
        if [c.text.strip() for c in t.rows[0].cells][:2] != ['Colonna', 'Tipo']:
            continue
        prime = [r.cells[0].text.strip() for r in t.rows]
        if all(c in prime for c in colonne):
            return t
    raise SystemExit('scheda non trovata per: ' + ', '.join(colonne))


def main():
    atteso = commenti(SRC)
    if os.path.exists(DST):
        os.remove(DST)
    shutil.copy(SRC, DST)
    d = docx.Document(DST)
    fatti = []

    # ───────────────────────────── 1. DOMINIO_DECODIFICA: la versione da R901
    i = indice_ddl(d, 'DOMINIO_DECODIFICA')
    inserisci_prima(d, riga_dopo(d, i, '  CONSTRAINT dominio_decodifica_pk PRIMARY KEY '
                                       '(id_dominio, nm_dominio)'),
                    ['  cd_versione          VARCHAR2(20 CHAR),'])
    fatti.append('DDL DOMINIO_DECODIFICA: aggiunta cd_versione')

    t = scheda_con(d, 'id_dominio', 'nm_dominio')
    D.clona_riga(t, ('cd_versione', 'VARCHAR2(20)',
                     'Versione della tabella dichiarata da ANSC nell’elenco di R901 '
                     '(es. «1.4.0»). ⚠️ È il solo modo per accorgersi che una decodifica è '
                     'cambiata senza riscaricarla e confrontarla riga per riga: una sola '
                     'chiamata leggera al posto di centoquarantacinque scarichi.'))
    fatti.append('scheda DOMINIO_DECODIFICA: riga cd_versione')

    # ─────────────── 2. VALORE_DOMINIO: via cd_valore, dentro gli attributi
    i = indice_ddl(d, 'VALORE_DOMINIO')
    p = riga_dopo(d, i, '  cd_valore            VARCHAR2(10 CHAR),')
    D.testo_di(p, '  tx_attributi         CLOB,')
    # la virgola va in coda alla riga precedente: il documento usa lo stile a virgola finale
    rif = riga_dopo(d, i, '    REFERENCES ANSC_USR.DOMINIO_DECODIFICA (id_dominio, nm_dominio)')
    D.testo_di(rif, '    REFERENCES ANSC_USR.DOMINIO_DECODIFICA (id_dominio, nm_dominio),')
    inserisci_prima(
        d, riga_dopo(d, i, ') TABLESPACE ANSC_USR;'),
        ['  CONSTRAINT valore_dominio_attributi_ck CHECK (tx_attributi IS JSON)'])
    fatti.append('DDL VALORE_DOMINIO: cd_valore → tx_attributi, con vincolo IS JSON')

    t = scheda_con(d, 'id_valore', 'cd_valore')
    r = riga_di(t, 'cd_valore')
    D.riscrivi_cella(r.cells[0], 'tx_attributi')
    D.riscrivi_cella(r.cells[1], 'CLOB (IS JSON)')
    D.riscrivi_cella(r.cells[2],
                     'Le colonne che due sole tabelle su centoquarantacinque portano in più '
                     'rispetto al tracciato comune: l’identificativo del tipo di contenuto '
                     'nei casi d’uso e il codice del consolato nei consolati. ⚠️ Sostituisce '
                     '«cd_valore», che il tracciato non alimenta: il CSV restituito da R901 '
                     'ha un solo identificativo per riga, non due.')
    fatti.append('scheda VALORE_DOMINIO: cd_valore sostituita da tx_attributi')

    # ─────────── 3. RICONCILIAZ_DIZIONARI: il raccordo diventa un dato
    i = indice_ddl(d, 'RICONCILIAZ_DIZIONARI')
    inserisci_prima(
        d, riga_dopo(d, i, '  DATA_INIZIO_VALIDITA DATE DEFAULT SYSDATE            NOT NULL,'),
        ['  SCHEMA_SIPO          VARCHAR2(30 CHAR),',
         '  TABELLA_SIPO         VARCHAR2(30 CHAR),',
         '  CAMPO_SIPO           VARCHAR2(30 CHAR),'])
    fatti.append('DDL RICONCILIAZ_DIZIONARI: schema, tabella e campo di SIPO')

    # ⚠️ l'obbligatorietà passa al lato ANSC, che è il dato certo: prima le sue colonne,
    # e la chiave di unicità si sposta su di esse più il campo di SIPO. Senza questa
    # inversione una riga «valore ANSC non ancora mappato» non sarebbe rappresentabile.
    # ⚠️ i quattro paragrafi si prendono PRIMA di riscriverli: sostituendoli uno per uno
    # per testo, la ricerca successiva riaggancerebbe la riga appena scritta e le due
    # descrizioni finirebbero scambiate.
    quattro = [riga_dopo(d, i, t) for t in (
        '  VALORE_SIPO          VARCHAR2(30 CHAR)  NOT NULL,',
        '  DESCRIZIONE_SIPO     VARCHAR2(400 CHAR),',
        '  VALORE_ANSC          VARCHAR2(30 CHAR),',
        '  DESCRIZIONE_ANSC     VARCHAR2(400 CHAR),')]
    for par, nuovo in zip(quattro, (
            '  VALORE_ANSC          VARCHAR2(30 CHAR)  NOT NULL,',
            '  DESCRIZIONE_ANSC     VARCHAR2(400 CHAR),',
            '  VALORE_SIPO          VARCHAR2(30 CHAR),',
            '  DESCRIZIONE_SIPO     VARCHAR2(400 CHAR),')):
        D.testo_di(par, nuovo)

    for vecchio, nuovo in (
        ('    UNIQUE (ID_VERSIONE, DECODIFICA, VALORE_SIPO, DATA_INIZIO_VALIDITA)',
         '    UNIQUE (ID_VERSIONE, DECODIFICA, VALORE_ANSC, CAMPO_SIPO, '
         'DATA_INIZIO_VALIDITA)'),
        ("  'Come un valore di SIPO si traduce nel corrispondente valore di ANSC. I dizionari",
         "  'Quale valore di SIPO corrisponde a ciascun valore ammesso da ANSC. I dizionari"),
        ("   dicono quali valori ANSC ammette, non quale valore locale vi corrisponde.';",
         "   dicono che cosa ANSC ammette; qui il corrispondente locale, che può mancare.';"),
    ):
        D.testo_di(riga_dopo(d, i, vecchio), nuovo)
    fatti.append('DDL RICONCILIAZ_DIZIONARI: obbligatorietà e chiave portate sul lato ANSC')

    # ─────────────────────────────── 4. la prosa che accompagna le strutture
    D.sostituisci(
        d,
        'Vincolo di unicità su (ID_VERSIONE, DECODIFICA, VALORE_SIPO, '
        'DATA_INIZIO_VALIDITA): una sola traduzione per valore, dentro una baseline e per '
        'un periodo.',
        'Vincolo di unicità su (ID_VERSIONE, DECODIFICA, VALORE_ANSC, CAMPO_SIPO, '
        'DATA_INIZIO_VALIDITA): un solo corrispondente locale per ciascun valore ammesso da '
        'ANSC, dentro una baseline, per un campo e per un periodo. ⚠️ Dalla v3.31 '
        '**l’obbligatorietà sta sul lato ANSC**: VALORE_ANSC è richiesta, VALORE_SIPO può '
        'mancare. È l’inversione che rende rappresentabile la riga «questo valore di ANSC '
        'non ha ancora corrispondente», che è poi il lavoro che la pagina di riconciliazione '
        'mostra.',
        attese=1, etichetta='vincolo di unicità portato sul lato ANSC', fatti=fatti)

    D.sostituisci(
        d,
        '⚠️ Resta fuori ciò che nessuna tabella può dire: quali valori di SIPO non abbiano '
        'alcun corrispondente in ANSC.',
        '⚠️ L’inversione sposta anche ciò che resta fuori. Ora la tabella dice quali valori '
        'di ANSC non abbiano ancora un corrispondente locale — ed è il dato che serve a '
        'condurre il lavoro. Non dice più, per contro, quali valori di SIPO non abbiano '
        'alcun corrispondente in ANSC.',
        attese=1, etichetta='inversione di ciò che la tabella non dice', fatti=fatti)

    for p in d.paragraphs:
        if p.text.strip().startswith('⚠️ L’inversione sposta anche ciò che resta fuori'):
            D.para(d, p._p,
                   'Dalla v3.31 la riga dichiara anche **dove** sta il valore locale: '
                   'SCHEMA_SIPO, TABELLA_SIPO e CAMPO_SIPO, con gli stessi nomi già usati da '
                   'ANSC_CFG_CAMPO. Il raccordo con le tabelle del Comune era finora '
                   'descritto in prosa e riportato in una tabella di questo documento: '
                   'utile a leggere, inservibile a eseguire. ⚠️ Lo schema è indispensabile '
                   'perché le tabelle di configurazione stanno in schemi diversi e in SIPO '
                   'esistono tabelle omonime in schemi distinti — ATTO ne è l’esempio noto.')
            D.para(d, p._p,
                   '⚠️ Il prezzo della scelta va detto: legando la riga anche al campo, **la '
                   'stessa decodifica usata da due campi diversi richiede due righe**. È '
                   'stato accettato perché rende la corrispondenza verificabile sul dato '
                   'reale e perché è la grana con cui la configurazione dei campi già '
                   'descrive il lato SIPO.')
            fatti.append('prosa della riconciliazione: il raccordo diventa un dato')
            break

    for p in d.paragraphs:
        if p.text.strip().startswith('Il raccordo fra le decodifiche da riconciliare e le '
                                     'tabelle di SIPO'):
            D.para(d, p._p,
                   '⚠️ **Questa tabella è ora il contenuto iniziale di tre colonne, non più '
                   'un allegato del documento.** Ciò che qui è riportato per esteso va '
                   'caricato in SCHEMA_SIPO e TABELLA_SIPO al primo popolamento della '
                   'riconciliazione; il campo si aggiunge man mano che la configurazione lo '
                   'individua.')
            fatti.append('nota sul contenuto iniziale del raccordo')
            break

    # ─────────────────── 5. che cosa R901 restituisce davvero
    for p in d.paragraphs:
        if p.text.strip().startswith('I dizionari dicono quali valori ANSC ammette'):
            D.para(d, p._p,
                   '**Che cosa R901 restituisce, verificato sul contratto.** L’operazione di '
                   'elenco restituisce per ciascuna tabella **tre soli dati** — '
                   'identificativo, nome e versione — e l’operazione di dettaglio non '
                   'restituisce una struttura ma **un CSV codificato in base64 e compresso '
                   'per impostazione predefinita**, con le colonne ID, DESCRIZIONE, '
                   'DATAINIZIOVALIDITA, DATAFINEVALIDITA e ORDINAMENTO. Centoquaranta file '
                   'su centoquarantacinque hanno esattamente quel tracciato; tre ne hanno '
                   'solo le prime due colonne e due ne portano una in più.')
            D.para(d, p._p,
                   '⚠️ Il confronto fra ciò che il servizio dà e ciò che il modello '
                   'prevedeva ha prodotto due correzioni, recepite in questa versione: '
                   '**«cd_valore» non aveva fonte** — il tracciato ha un solo identificativo '
                   'per riga — e **la versione della tabella non veniva conservata**, pur '
                   'essendo l’appiglio che rende l’intercetto delle revisioni una sola '
                   'chiamata leggera invece di centoquarantacinque scarichi.')
            fatti.append('prosa dei dizionari: che cosa R901 restituisce')
            break

    # ─────────────────────────────────────── 6. l'ERD e il punto aperto
    D.sostituisci_immagine(d, 'Schema ANSC_USR. Le frecce piene',
                           os.path.join(IMG, 'erd_ansc_usr.png'))
    fatti.append('ERD rigenerato con le colonne modificate')

    t = D.trova_tabella(d, '#', 'tema', 'questione')
    # ⚠️ il numero si ricava dal massimo esistente, non dal conteggio delle righe: la serie
    # ha buchi e contare le righe darebbe un identificativo già distante dal vero.
    import re as _re
    esistenti = [int(m.group(1)) for r in t.rows
                 for m in [_re.match(r'^OP-(\d+)$', r.cells[0].text.strip())] if m]
    numero = 'OP-%d' % (max(esistenti) + 1)
    D.clona_riga(t, (
        numero, 'Corrispondenze molti-a-uno nella riconciliazione',
        'Con la chiave di unicità portata sul lato ANSC — decisione recepita in questa '
        'versione — **a ciascun valore ammesso da ANSC corrisponde un solo valore di SIPO '
        'per campo**. ⚠️ Resta da accertare se in SIPO esistano decodifiche in cui due valori '
        'locali distinti debbano confluire nello stesso valore di ANSC: è il caso tipico di '
        'un archivio che si è stratificato nel tempo, con un codice vecchio e uno nuovo che '
        'significano la stessa cosa. Se esistesse anche un solo caso, la chiave andrebbe '
        'allargata al valore di SIPO e si perderebbe la garanzia che la traduzione inversa '
        'sia univoca. La verifica si fa sulle tabelle CONF_* raccordate, non sul contratto '
        'di ANSC.',
        'Aperto', 'Analisi / Cliente', 'Media'))
    fatti.append(numero + ' aperto sull’orientamento della riconciliazione')

    # ────────────────────────────────────────────── 7. testata e storia
    for tab in d.tables:
        if tab.rows[0].cells[0].text.strip().lower().startswith(('area organizzativa',
                                                                 'progetto')):
            for r in tab.rows:
                v = {'Data consegna': '29/09/2026',
                     'Versione': '3.31'}.get(r.cells[0].text.strip())
                if v:
                    D.riscrivi_cella(r.cells[1], v)
            break
    D.storia(d, '29/09/2026', '3.31',
             'Gestione dei dizionari · Modello dati · App. A · Open Point',
             'Recepite due correzioni emerse dal disegno del back-office e verificate sul '
             'contratto R901. DOMINIO_DECODIFICA acquisisce la versione della tabella, che '
             'il servizio restituisce e che il modello non conservava: è l’appiglio che '
             'rende l’intercetto delle revisioni una sola chiamata. VALORE_DOMINIO perde '
             '«cd_valore», che il tracciato del CSV non alimenta, e acquisisce un attributo '
             'in formato JSON per le due colonne aggiuntive di consolati e casi d’uso. '
             'RICONCILIAZ_DIZIONARI acquisisce schema, tabella e campo di SIPO: il raccordo '
             'con le tabelle del Comune era descritto in prosa e non era un dato. Aperto un '
             'punto sull’orientamento della riconciliazione, che la struttura attuale '
             'dichiara opposto a quello del back-office.')
    fatti.append('testata e storia aggiornate')

    # grassetti: `para` non interpreta «**…**»
    def grassetti(par):
        if '**' not in par.text or D.ha_commenti(par._p):
            return 0
        pezzi = D.segmenta('', par.text)
        for r in list(par.runs):
            r._r.getparent().remove(r._r)
        for testo, gr in pezzi:
            run = par.add_run(testo)
            run.bold = gr
        return 1
    n = sum(grassetti(p) for p in d.paragraphs)
    for tab in d.tables:
        for r in tab.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    n += grassetti(p)
    fatti.append('%d paragrafi con grassetto applicato' % n)

    d.save(DST)
    trovati = commenti(DST)
    assert trovati == atteso, 'commenti persi: %d invece di %d' % (trovati, atteso)
    print('\n'.join(' · ' + f for f in fatti))
    print('commenti preservati:', trovati)
    print('capitoli/tabelle/immagini:', D.riepilogo(DST))
    print('scritto:', os.path.relpath(DST, BASE))


if __name__ == '__main__':
    main()
