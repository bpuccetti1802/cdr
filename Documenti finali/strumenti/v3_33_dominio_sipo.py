# -*- coding: utf-8 -*-
"""ANALISI_Integrazione-ANSC v3.32 → v3.33 (07/10/2026).

Nuova tabella ANSC_CFG_DOMINIO_SIPO: il catalogo che dichiara, una volta sola, dove vive
in SIPO un dominio di decodifica di ANSC. Finora la relazione esisteva solo implicita,
ripetuta su ogni riga di RICONCILIAZ_DIZIONARI e di ANSC_CFG_CAMPO.

⚠️ Non risolve un problema nuovo: la scheda di RICONCILIAZ_DIZIONARI.DECODIFICA dichiara
già che «nella sorgente ha due forme — ANSC_01 oppure conf_diff_sposi.ANSC_32 — e vanno
normalizzate prima del carico». Questa tabella è quella normalizzazione, resa un dato.

Decisioni del committente recepite:
  · accesso **per valore e, in alternativa, per chiave**: RICONCILIAZ_DIZIONARI conserva
    DECODIFICA e guadagna ID_DOMINIO_SIPO;
  · **COD_ORIGINE non si reinserisce** in ANSC_CFG_CAMPO: si toglie invece il CHECK
    orfano, che rendeva la CREATE non eseguibile (ORA-00904). OP-65, che già tracciava
    l'asimmetria, registra la decisione;
  · algoritmo di DECODIFICA: schema se valorizzato, altrimenti si parte dalla tabella.

⚠️ Due difetti trovati verificando e corretti qui:
  · VARCHAR2(100) non basta: schema(30)+tabella(30)+campo(30)+separatori+ANSC_nnn fanno
    **101** caratteri nel caso peggiore. Si porta a 110.
  · ⚠️ NON usare LPAD(ID_DOMINIO, 2, '0'): con i domini a tre cifre TRONCA — LPAD('100',
    2,'0') dà '10', cioè un dominio diverso, senza errore. I domini arrivano a 183.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_33_dominio_sipo.py
"""
import os
import shutil
import subprocess
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIN = os.path.join(BASE, 'Documenti finali')
SRC = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.32.docx')
DST = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.33.docx')
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')

DDL = """CREATE TABLE ANSC_USR.ANSC_CFG_DOMINIO_SIPO (
  ID_DOMINIO_SIPO      NUMBER GENERATED ALWAYS AS IDENTITY,
  ID_DOMINIO           NUMBER             NOT NULL,
  NM_DOMINIO           VARCHAR2(50 CHAR)  NOT NULL,
  SCHEMA_SIPO          VARCHAR2(30 CHAR),
  TABELLA_SIPO         VARCHAR2(30 CHAR)  NOT NULL,
  CAMPO_SIPO           VARCHAR2(30 CHAR)  NOT NULL,
  DECODIFICA           VARCHAR2(110 CHAR) GENERATED ALWAYS AS (
                         CASE WHEN SCHEMA_SIPO IS NOT NULL
                              THEN SCHEMA_SIPO || '.' END
                         || TABELLA_SIPO || '.' || CAMPO_SIPO || '.ANSC_'
                         || CASE WHEN ID_DOMINIO < 10 THEN '0' END
                         || TO_CHAR(ID_DOMINIO)
                       ) VIRTUAL,
  DATA_INS             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  DATA_UPD             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  UTENTE_INS           VARCHAR2(40 CHAR),
  UTENTE_UPD           VARCHAR2(40 CHAR),
  CONSTRAINT PK_CFG_DOMINIO_SIPO PRIMARY KEY (ID_DOMINIO_SIPO),
  CONSTRAINT UK_CFG_DOMINIO_SIPO UNIQUE (DECODIFICA)
) TABLESPACE ANSC_USR;

COMMENT ON TABLE ANSC_USR.ANSC_CFG_DOMINIO_SIPO IS
  'Dove vive in SIPO un dominio di decodifica di ANSC: una riga per ciascuna
   corrispondenza in uso. Normalizza le due forme con cui la sorgente scrive la
   decodifica.';
COMMENT ON COLUMN ANSC_USR.ANSC_CFG_DOMINIO_SIPO.SCHEMA_SIPO IS
  'Facoltativo. Se valorizzato entra nella decodifica generata, altrimenti la stringa
   parte dalla tabella.';
COMMENT ON COLUMN ANSC_USR.ANSC_CFG_DOMINIO_SIPO.DECODIFICA IS
  'Colonna virtuale: non si scrive, si calcola. ATTENZIONE: non usare LPAD per
   l allineamento del numero di dominio, perche sui domini a tre cifre tronca.';""".split('\n')

COLONNE = [
    ['Colonna', 'Tipo', 'Note'],
    ['ID_DOMINIO_SIPO', 'NUMBER (PK)',
     'Chiave surrogata. È ciò che RICONCILIAZ_DIZIONARI può citare al posto della '
     'stringa, quando conviene l’accesso per chiave.'],
    ['ID_DOMINIO', 'NUMBER',
     'Identificativo del dominio come lo pubblica ANSC. ⚠️ Insieme al nome forma la '
     'chiave vera di DOMINIO_DECODIFICA: «ANSC_01» non è un valore memorizzato da alcuna '
     'parte, è una forma di presentazione.'],
    ['NM_DOMINIO', 'VARCHAR2(50)',
     'Nome della tabella di decodifica (es. dec_stato_evento). ⚠️ Serve perché due domini '
     'condividono l’identificativo: 134 e 135.'],
    ['SCHEMA_SIPO', 'VARCHAR2(30)',
     '**Facoltativo.** Se valorizzato apre la decodifica generata; se manca, la stringa '
     'parte dalla tabella. ⚠️ Trenta caratteri sono il limite di Oracle per un '
     'identificativo: più larga non servirebbe e nasconderebbe un errore.'],
    ['TABELLA_SIPO', 'VARCHAR2(30)', 'La tabella di SIPO che contiene il valore locale.'],
    ['CAMPO_SIPO', 'VARCHAR2(30)',
     'La colonna. ⚠️ Entra nella chiave perché la stessa decodifica si traduce '
     'diversamente secondo la colonna di partenza: è il caso che la sorgente scrive come '
     '«conf_diff_sposi.ANSC_32».'],
    ['DECODIFICA', 'VARCHAR2(110) — virtuale',
     '**Generata, non immessa.** `[schema.]tabella.campo.ANSC_nn`. Porta il vincolo di '
     'unicità, perché è il valore con cui la riconciliazione si aggancia. ⚠️ 110 e non '
     '100: nel caso peggiore la stringa è lunga 101 caratteri.'],
]


def main():
    if os.path.exists(DST):
        os.remove(DST)
    shutil.copy(SRC, DST)

    def commenti(p):
        return int(subprocess.run(
            ['bash', '-c', "unzip -p %s word/comments.xml 2>/dev/null | "
                           "grep -o '<w:comment ' | wc -l" % repr(p)],
            capture_output=True, text=True).stdout.strip() or 0)
    prima = commenti(DST)

    d = docx.Document(DST)
    fatti = []

    # ------------------------------------------------ 1. la tabella nuova
    ancora = D.h(d, 3, 'RICONCILIAZ_DIZIONARI')
    D.para(d, ancora._p, 'ANSC_CFG_DOMINIO_SIPO', stile='Heading 3')
    D.ddl(d, ancora._p, DDL)
    D.para(d, ancora._p, '')
    D.tabella(d, ancora._p, COLONNE, modello=d.tables[37], larghezze=[1.4, 1.5, 3.4])
    D.para(d, ancora._p, '')
    fatti.append('nuova tabella ANSC_CFG_DOMINIO_SIPO con DDL e scheda delle colonne')

    # ------------------------------------------------ 2. la prosa che la motiva
    cap = D.h(d, 2, 'La riconciliazione dei valori fra SIPO e ANSC')
    nxt = cap._p.getnext()
    D.para(d, nxt,
           '⚠️ **Dalla v3.33 la corrispondenza fra un dominio di ANSC e il posto in cui '
           'vive in SIPO è dichiarata una volta sola**, nella tabella '
           'ANSC_CFG_DOMINIO_SIPO, invece di essere riscritta su ogni riga. Non è un '
           'problema nuovo: la scheda della colonna DECODIFICA dichiarava già che nella '
           'sorgente la decodifica ha **due forme** — il solo identificativo oppure la '
           'colonna di SIPO che lo precede — e che «vanno normalizzate prima del carico». '
           'Questa tabella è quella normalizzazione, resa un dato invece che un’istruzione.')
    D.para(d, nxt,
           '**La chiave non è il dominio: è la terna dominio, tabella e campo.** Lo stesso '
           'dominio di ANSC si traduce diversamente secondo la colonna da cui si parte, ed '
           'è la ragione per cui una relazione uno-a-uno fra dominio e tabella sarebbe '
           'sbagliata. Il catalogo ha quindi una riga per ciascuna corrispondenza in uso, '
           'e la stringa che le dà nome — `[schema.]tabella.campo.ANSC_nn` — **non si '
           'immette: si calcola**, come colonna virtuale. Lo schema è facoltativo: se c’è '
           'apre la stringa, se manca la stringa parte dalla tabella.')
    D.para(d, nxt,
           '**La riconciliazione vi accede in due modi, e per ora li conserva entrambi**: '
           'per valore, confrontando la propria colonna DECODIFICA con quella generata, '
           'come fa oggi; e per chiave, citando ID_DOMINIO_SIPO. ⚠️ Finché convivono, la '
           'stessa informazione sta in due posti e può divergere: la regola è che **il '
           'catalogo è la fonte** e che schema, tabella e campo sulla riga di '
           'riconciliazione si scrivono da lì, mai a mano.')
    fatti.append('motivazione e regola d’uso nel capitolo della riconciliazione')

    # ------------------------------------------------ 3. la riconciliazione si aggancia
    D.sostituisci(
        d, '  DECODIFICA           VARCHAR2(100 CHAR) NOT NULL,',
        '  DECODIFICA           VARCHAR2(110 CHAR) NOT NULL,\n'
        '  ID_DOMINIO_SIPO      NUMBER,',
        attese=1, etichetta='DECODIFICA portata a 110 e aggiunta ID_DOMINIO_SIPO',
        fatti=fatti)
    D.sostituisci(
        d, '  CONSTRAINT UK_RICONCILIAZ_DIZIONARI',
        '  CONSTRAINT FK_RICONC_DIZ_DOMINIO_SIPO\n'
        '    FOREIGN KEY (ID_DOMINIO_SIPO)\n'
        '    REFERENCES ANSC_USR.ANSC_CFG_DOMINIO_SIPO (ID_DOMINIO_SIPO),\n'
        '  CONSTRAINT UK_RICONCILIAZ_DIZIONARI',
        attese=1, etichetta='chiave esterna verso il catalogo', fatti=fatti)
    for r in d.tables[37].rows:
        if r.cells[0].text.strip() == 'DECODIFICA':
            D.riscrivi_cella(r.cells[1], 'VARCHAR2(110)')
            D.riscrivi_cella(
                r.cells[2], 'La decodifica ANSC interessata, nella forma '
                            '[schema.]tabella.campo.ANSC_nn. ⚠️ Dalla v3.33 la forma è '
                            'quella generata da ANSC_CFG_DOMINIO_SIPO: le due grafie che '
                            'convivevano nella sorgente si normalizzano caricando il '
                            'catalogo. La larghezza passa da 100 a 110 perché nel caso '
                            'peggiore la stringa è lunga 101 caratteri.')
            break
    fatti.append('scheda della colonna DECODIFICA riscritta')

    # ------------------------------------------------ 4. il CHECK orfano
    D.sostituisci(
        d, "  CONSTRAINT CK_ANSC_CFG_CAMPO_OPERATIVO CHECK (OPERATIVO IN ('0','1')),",
        "  CONSTRAINT CK_ANSC_CFG_CAMPO_OPERATIVO CHECK (OPERATIVO IN ('0','1'))",
        attese=1, etichetta='tolta la virgola prima del vincolo rimosso', fatti=fatti)
    ps = d.paragraphs
    k = next(i for i, p in enumerate(ps)
             if p.text.strip() == 'CONSTRAINT CK_ANSC_CFG_CAMPO_ORIG')
    for p in (ps[k], ps[k + 1]):
        if D.ha_commenti(p._p):
            raise SystemExit('il vincolo orfano porta un commento: non si elimina')
        p._p.getparent().remove(p._p)
    fatti.append('rimosso il CHECK orfano su COD_ORIGINE: la CREATE ora è eseguibile')

    to = D.trova_tabella(d, '#', 'Questione')
    for r in to.rows[1:]:
        if r.cells[0].text.strip() == 'OP-65':
            D.riscrivi_cella(
                r.cells[1], r.cells[1].text.strip() + ' ⚠️ Deciso di non reinserire la '
                'colonna: nella v3.33 è stato rimosso il vincolo che la richiamava e che '
                'rendeva la CREATE non eseguibile. L’asimmetria con sezioni, allegati e '
                'formule resta, e con essa la domanda su come la reimportazione distingua '
                'le righe proposte da quelle confermate per i campi.')
            break
    else:
        raise SystemExit('OP-65 non trovato')
    fatti.append('OP-65 aggiornato con la decisione')

    # ------------------------------------------------ 5. l'ERD
    D.sostituisci_immagine(d, 'Schema ANSC_USR', os.path.join(IMG, 'erd_ansc_usr.png'))
    fatti.append('ERD rigenerato con ANSC_CFG_DOMINIO_SIPO e i suoi due legami')

    # ------------------------------------------------ 6. testata e storia
    for tb in d.tables:
        if tb.rows[0].cells[0].text.strip().lower().startswith('area organizzativa'):
            for r in tb.rows:
                v = {'Versione': '3.33',
                     'Documento': 'ANALISI_Integrazione-ANSC_v3.33'}.get(
                        r.cells[0].text.strip())
                if v:
                    D.riscrivi_cella(r.cells[1], v)
            break
    D.storia(d, '07/10/2026', '3.33',
             'Modello dati (nuova ANSC_CFG_DOMINIO_SIPO, RICONCILIAZ_DIZIONARI, '
             'ANSC_CFG_CAMPO, ERD) · Appendice DDL · Open Point',
             'Introdotto il catalogo delle corrispondenze fra un dominio di decodifica di '
             'ANSC e il posto in cui il valore vive in SIPO. Finora la relazione esisteva '
             'solo implicita, ripetuta su ogni riga della riconciliazione e della '
             'configurazione dei campi; il documento ne dichiarava la necessità senza '
             'realizzarla. La chiave è la terna dominio, tabella e campo, perché lo stesso '
             'dominio si traduce diversamente secondo la colonna di partenza; la stringa '
             'che la nomina è una colonna virtuale, calcolata e non immessa. La '
             'riconciliazione vi accede per valore e, in alternativa, per chiave. Decisa '
             'inoltre la sorte del vincolo orfano su COD_ORIGINE in ANSC_CFG_CAMPO: la '
             'colonna non si reinserisce e il vincolo è stato rimosso, perché rendeva la '
             'CREATE non eseguibile. Corretta la larghezza della colonna che accoglie la '
             'decodifica, che nel caso peggiore era di un carattere insufficiente.')
    fatti.append('testata e storia aggiornate')

    # ------------------------------------------------ 7. grassetti
    def grassetti(p):
        if '**' not in p.text or D.ha_commenti(p._p):
            return 0
        pezzi = D.segmenta('', p.text)
        for r in list(p.runs):
            r._r.getparent().remove(r._r)
        for testo, gr in pezzi:
            run = p.add_run(testo)
            run.bold = gr
        return 1
    n = sum(grassetti(p) for p in d.paragraphs)
    for tb in d.tables:
        for r in tb.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    n += grassetti(p)
    fatti.append('%d paragrafi con grassetto applicato' % n)

    d.save(DST)
    dopo = commenti(DST)
    if dopo != prima:
        raise SystemExit('COMMENTI PERSI: erano %d, sono %d' % (prima, dopo))
    fatti.append('commenti di Word conservati: %d → %d' % (prima, dopo))

    print('\n'.join(' · ' + f for f in fatti))
    print('capitoli/tabelle/immagini:', D.riepilogo(DST))
    print('scritto:', os.path.relpath(DST, BASE))


if __name__ == '__main__':
    main()
