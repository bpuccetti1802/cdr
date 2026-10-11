# -*- coding: utf-8 -*-
"""ANALISI_Integrazione-ANSC v3.34 → v3.35 (10/10/2026).

SOGGETTI_USECASE, ricevuta dal sistema Side del Comune di Milano il 09/10/2026 come sola
definizione (`Sorgenti Documentali/Tabella SOGGETTI_USECASE.ddl`, PostgreSQL, schema atti).

⚠️ Che cosa si è potuto ricavare e che cosa no — verificato prima di scrivere:
  * la tabella NON è citata in nessuno dei documenti di processo di Side disponibili (allegati
    v1.5, attestato di conformità v1.1, numerazione comunale v1.0, atti gemellari v1.4,
    notifiche v2), né altrove nel workspace: le API con cui Milano la gestisce NON si
    ricavano, e il documento lo dice invece di proporne;
  * i tre trigger richiamano funzioni il cui corpo non è fra le sorgenti: non si riportano;
  * i ruoli (dichiarante, comparente, firmatario) NON stanno nel mapping di ANSC: 374 file,
    sette colonne, 226 nomi di sezione, nessuna colonna di ruolo. È il valore aggiunto
    della tabella, e il motivo per cui si compila invece di importarsi;
  * ty_presenza e ty_configurazione hanno valori documentati da Side solo per ALLEGATI_USECASE
    (O/F/C00n; BASE/D.LIB.M.01): per i soggetti restano [DA VERIFICARE].

Correzioni collaterali, dichiarate nella storia:
  * nel DDL di ALLEGATI_USECASE era rimasto un secondo CREATE INDEX con lo stesso nome, sulla
    colonna ID_UC che la tabella non ha, e due COMMENT su colonne inesistenti (DESCRIZIONE,
    FLG_ATT_CONFORMITA): residui di una stesura precedente, che rendevano lo script non
    eseguibile (ORA-00955);
  * nell'ERD la scheda della baseline nominava CFG_CAMPO, che non porta ID_VERSIONE, e taceva
    RICONCILIAZ_DIZIONARI, che la porta; lo store di stato mostrava come FK un riferimento
    per valore.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/diagrammi_erd.py
    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_35_soggetti.py
"""
import os
import shutil
import subprocess
import sys

import docx
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIN = os.path.join(BASE, 'Documenti finali')
SRC = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.34.docx')
DST = os.path.join(FIN, 'ANALISI_Integrazione-ANSC_v3.35.docx')
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')


def commenti(p):
    return int(subprocess.run(
        ['bash', '-c', "unzip -p %s word/comments.xml 2>/dev/null | "
                       "grep -o '<w:comment ' | wc -l" % repr(p)],
        capture_output=True, text=True).stdout.strip() or 0)


COLONNE = [
    ('Colonna', 'Tipo', 'Note'),
    ('cd_usecase', 'VARCHAR2(20) (PK)',
     'Codice dell’UC come ANSC lo pubblica. Riferimento per valore al catalogo degli UC, come '
     'in ALLEGATI_USECASE e per la stessa ragione; dieci caratteri nella struttura di origine, '
     'venti qui perché i codici non hanno lunghezza fissa.'),
    ('cd_soggetto', 'VARCHAR2(50) (PK)',
     'Codice del soggetto all’interno dell’UC. [DA VERIFICARE: i valori in uso in Side. Se '
     'coincidessero con la radice del blocco nel modello evento — evento.madre, '
     'evento.interprete — la riga si raccorderebbe da sé ad ANSC_CFG_SEZIONE; la definizione '
     'ricevuta non lo dice (OP-69).]'),
    ('id_versione', 'NUMBER (PK, FK)',
     'Baseline di appartenenza (ANSC_CFG_VERSIONE). Aggiunta rispetto alla struttura di '
     'origine, come in ALLEGATI_USECASE: senza, due baseline non possono dichiarare soggetti '
     'diversi per lo stesso UC.'),
    ('ty_soggetto', 'VARCHAR2(30)',
     'Tipo del soggetto. [DA VERIFICARE: il dominio dei valori non è dichiarato (OP-69).]'),
    ('nm_soggetto', 'VARCHAR2(250)',
     'Nome del soggetto come si presenta all’operatore. Obbligatorio nella struttura di '
     'origine.'),
    ('ty_presenza', 'VARCHAR2(10)',
     'Presenza richiesta del soggetto. Omonima della colonna di ALLEGATI_USECASE, per la quale '
     'la documentazione di Side dichiara O (obbligatorio), F (facoltativo) e C001…C004 '
     '(obbligatorio a condizione di un valore dei dati di nascita). [DA VERIFICARE: se per i '
     'soggetti i valori siano gli stessi (OP-69).]'),
    ('ty_configurazione', 'VARCHAR2(10)',
     'Negli allegati Side la usa per scegliere l’elemento di interfaccia: BASE, a descrizione '
     'fissa, oppure D.LIB.M.01, a descrizione libera e ripetibile. [DA VERIFICARE: il '
     'significato per i soggetti (OP-69).]'),
    ('fg_dichiarante', 'CHAR(1)', '0/1: il soggetto rende la dichiarazione.'),
    ('fg_comparente', 'CHAR(1)', '0/1: il soggetto compare davanti all’ufficiale.'),
    ('fg_firmatario', 'CHAR(1)',
     '0/1: il soggetto sottoscrive l’atto. È l’informazione che decide se, dopo la '
     'validazione, l’atto attende la firma di qualcuno prima di quella dell’ufficiale.'),
    ('nr_ordinamento', 'NUMBER(5)', 'Ordine di presentazione all’operatore.'),
    ('fg_operante', 'CHAR(1)',
     '0/1: se la riga è in esercizio. Stesso significato che in ALLEGATI_USECASE: il Comune '
     'disattiva una configurazione senza cancellarla.'),
    ('tx_note', 'CLOB', 'Testo libero a disposizione di chi configura.'),
    ('cd_ope_ins_dt / ts_ins_dt / cd_ope_ult_agg_dt / ts_ult_agg_dt / ds_note_dt',
     'CHAR(6) / TIMESTAMP',
     'Campi tecnici nella convenzione di Side, come per ALLEGATO e ALLEGATI_USECASE.'),
]

TESTO = [
    ('Heading 2', 'I soggetti previsti dall’UC'),
    ('Normal',
     'Accanto ai documenti, il sistema Side del Comune di Milano configura per caso d’uso anche '
     'le persone che l’atto coinvolge. La struttura è SOGGETTI_USECASE, ricevuta come '
     'definizione insieme alle altre strutture di Side [R12] e adottata, come '
     'ALLEGATI_USECASE, con i nomi di origine: una riga per ciascun soggetto previsto da un UC, '
     'con il suo nome, la presenza richiesta e tre contrassegni di ruolo — dichiarante, '
     'comparente, firmatario.'),
    ('Normal',
     '⚠️ I ruoli sono l’unica informazione di questa configurazione che il mapping di ANSC non '
     'contiene affatto. Il mapping raggruppa i campi in sezioni — 226 nomi distinti sui 374 UC, '
     'fra i quali le persone, da «Madre» e «Padre» a «Testimone 1» e «Comparente 2», stanno '
     'accanto a blocchi che persone non sono, come «Formula» o «Dati generali» — e ne dichiara '
     'l’obbligatorietà; ma nelle sue sette colonne nulla dice chi, fra le persone di un atto, '
     'rende la dichiarazione, chi compare davanti all’ufficiale e chi firma. Per questo i '
     'contrassegni non si importano: si compilano, una volta per UC, come il contrassegno '
     'dell’attestazione di conformità sui documenti.'),
    ('Normal',
     'Il ruolo serve in due punti del percorso. Il primo è la firma. La documentazione di '
     'processo di Side sull’attestato di conformità [R12] distingue gli atti con dichiaranti '
     'da quelli senza: nei primi l’attestato si presenta dopo la firma dei dichiaranti, nei '
     'secondi subito dopo la validazione. Quali soggetti firmino è ciò che fg_firmatario '
     'dichiara per UC; che sia questa colonna a governare il passaggio in Side, la '
     'documentazione ricevuta non lo afferma. Il secondo è la raccolta dei dati: le maschere '
     'di SIPO non chiedono tutte le persone che ANSC prevede — nel foglio di lavoro del pilota, '
     'Morte_001, 80 righe su 218 appartengono a soggetti che la maschera dei decessi non '
     'raccoglie, fra cui i comparenti — e una tabella che elenca per UC i soggetti attesi rende '
     'quel divario dichiarato, invece di lasciarlo scoprire al deposito.'),
    ('Normal', 'SOGGETTI_USECASE'),
    ('TABELLA', None),
    ('Normal',
     'Il significato dei tre contrassegni di ruolo è quello che il nome dichiara: la '
     'definizione ricevuta non porta commenti sulle colonne. Dichiarante e comparente non sono '
     'sinonimi, e la distinzione che Side vi applica va confermata sui dati.'),
    ('Normal',
     'Le scelte di adozione sono quelle già fatte per ALLEGATI_USECASE: nomi di origine; la '
     'baseline in chiave, con chiave esterna verso ANSC_CFG_VERSIONE; il codice dell’UC come '
     'riferimento per valore, portato a venti caratteri. I nomi dei vincoli sono accorciati '
     'entro i trenta caratteri ammessi da Oracle, che quelli di origine superano. ⚠️ Non si '
     'aggiunge invece il richiamo al catalogo delle logiche che ALLEGATI_USECASE ha ricevuto: '
     'per i soggetti la condizione che rende necessaria una persona è già dichiarata, a '
     'livello di sezione, in ANSC_CFG_SEZIONE, e una seconda sede per la stessa condizione è '
     'proprio ciò che il catalogo esiste per evitare.'),
    ('Normal',
     '⚠️ Ne discende una sovrapposizione da governare, non da nascondere. Che una persona sia '
     'prevista dall’UC lo dicono ora due tabelle: SOGGETTI_USECASE con ty_presenza, e '
     'ANSC_CFG_SEZIONE con la logica di attivazione della sezione. La prima è la scelta di '
     'Side, la seconda nasce dal mapping di ANSC; se divergono, il pre-filtro chiede una '
     'persona che la costruzione del payload non prevede, o la tace quando invece serve. Va '
     'deciso quale delle due governi la presenza e come si raccordino le righe, il che '
     'dipende dai valori di cd_soggetto (OP-69).'),
    ('Normal',
     'La definizione di origine porta tre trigger, su inserimento, modifica e cancellazione, '
     'che richiamano funzioni — registra_soggetti_usecase_insert, _update e _delete — il cui '
     'corpo non è fra le sorgenti. Non si riportano. Il nome fa pensare alla registrazione '
     'delle modifiche, che qui è già assicurata dal versionamento della baseline; ma senza il '
     'codice non si può dire se facciano soltanto questo.'),
    ('Normal',
     '⚠️ Le sorgenti ricevute non contengono le interfacce con cui Side legge e aggiorna la '
     'tabella: né un contratto né la descrizione di una pagina che la governi. '
     'SOGGETTI_USECASE non è citata in alcuno dei documenti di processo di Side disponibili. '
     'Il presente documento non ne propone di proprie e non integra l’Appendice B; le '
     'interfacce, e il contenuto della tabella per gli UC che Milano ha già configurato, sono '
     'da richiedere al Comune di Milano (OP-69). Per la stessa ragione la manutenzione della '
     'tabella dal back-office non è ancora disegnata.'),
]

DDL = [
    'CREATE TABLE ANSC_USR.SOGGETTI_USECASE (',
    '  cd_usecase           VARCHAR2(20 CHAR)  NOT NULL,',
    '  cd_soggetto          VARCHAR2(50 CHAR)  NOT NULL,',
    '  id_versione          NUMBER             NOT NULL,',
    '  ty_soggetto          VARCHAR2(30 CHAR)  NOT NULL,',
    '  nm_soggetto          VARCHAR2(250 CHAR) NOT NULL,',
    '  ty_presenza          VARCHAR2(10 CHAR)  NOT NULL,',
    '  ty_configurazione    VARCHAR2(10 CHAR)  NOT NULL,',
    '  fg_dichiarante       CHAR(1 CHAR)       NOT NULL,',
    '  fg_comparente        CHAR(1 CHAR)       NOT NULL,',
    '  fg_firmatario        CHAR(1 CHAR)       NOT NULL,',
    '  nr_ordinamento       NUMBER(5)          NOT NULL,',
    '  fg_operante          CHAR(1 CHAR)       NOT NULL,',
    '  tx_note              CLOB,',
    '  cd_ope_ins_dt        CHAR(6 CHAR)       NOT NULL,',
    '  ts_ins_dt            TIMESTAMP,',
    '  cd_ope_ult_agg_dt    CHAR(6 CHAR),',
    '  ts_ult_agg_dt        TIMESTAMP,',
    '  ds_note_dt           VARCHAR2(50 CHAR),',
    '  CONSTRAINT soggetti_usecase_pk',
    '    PRIMARY KEY (cd_usecase, cd_soggetto, id_versione),',
    '  CONSTRAINT soggetti_usecase_versione_fk',
    '    FOREIGN KEY (id_versione) REFERENCES ANSC_USR.ANSC_CFG_VERSIONE (ID_VERSIONE),',
    "  CONSTRAINT soggetti_uc_dichiarante_ck CHECK (fg_dichiarante IN ('0','1')),",
    "  CONSTRAINT soggetti_uc_comparente_ck  CHECK (fg_comparente  IN ('0','1')),",
    "  CONSTRAINT soggetti_uc_firmatario_ck  CHECK (fg_firmatario  IN ('0','1')),",
    "  CONSTRAINT soggetti_uc_operante_ck    CHECK (fg_operante    IN ('0','1'))",
    ') TABLESPACE ANSC_USR;',
    'CREATE INDEX ANSC_USR.IX_SOGGETTI_USECASE_UC',
    '  ON ANSC_USR.SOGGETTI_USECASE (id_versione, cd_usecase) TABLESPACE ANSC_USR;',
    'COMMENT ON TABLE ANSC_USR.SOGGETTI_USECASE IS',
    "  'Soggetti previsti da ciascun UC e loro ruolo. Struttura ereditata dal sistema Side",
    '   con i nomi di origine; aggiunta id_versione (baseline). I tre trigger di origine non',
    "   sono riportati: il corpo delle funzioni non e fra le sorgenti (OP-69).';",
    'COMMENT ON COLUMN ANSC_USR.SOGGETTI_USECASE.cd_soggetto IS',
    "  'DA VERIFICARE: valori in uso in Side (OP-69).';",
    'COMMENT ON COLUMN ANSC_USR.SOGGETTI_USECASE.fg_firmatario IS',
    "  '0/1: il soggetto sottoscrive l''atto. Il mapping ANSC non lo dichiara: si compila.';",
    '',
]

OP69 = ('OP-69', 'Soggetti per UC ereditati da Side',
        'SOGGETTI_USECASE è adottata dalla sola definizione. Da richiedere al Comune di Milano: '
        'i valori di cd_soggetto, ty_soggetto, ty_presenza e ty_configurazione; le interfacce '
        'con cui Side legge e aggiorna la tabella e il corpo delle tre funzioni richiamate dai '
        'trigger; il contenuto già compilato per gli UC configurati. Va poi deciso se la '
        'presenza di un soggetto la governi ty_presenza oppure la logica di attivazione della '
        'sezione in ANSC_CFG_SEZIONE, che oggi la dichiarano entrambe.',
        'Aperto', 'Analisi / Cliente', 'Media')

R12 = ('R12',
       'Sorgenti Documentali/ — strutture e documenti di processo del sistema Side del Comune '
       'di Milano',
       'Definizioni ricevute (ALLEGATO, ALLEGATI_USECASE, dizionari, SOGGETTI_USECASE) e '
       'documenti di analisi «CdMI SIDe MI_ANSC»: gestione degli allegati v1.5, attestato di '
       'conformità v1.1, numerazione comunale v1.0, numeri degli atti gemellari v1.4, '
       'gestione delle notifiche v2. Le strutture sono adottate con i nomi di origine.')

STORIA = (
    '10/10/2026', '3.35',
    'Costruzione del payload (nuovo «I soggetti previsti dall’UC») · Adeguamenti database · '
    'Modello dati (ERD) · Appendice A · Riferimenti · Open Point',
    'Adottata SOGGETTI_USECASE, ricevuta dal sistema Side del Comune di Milano: i soggetti '
    'previsti da ciascun UC, con i contrassegni di dichiarante, comparente e firmatario, che il '
    'mapping di ANSC non dichiara e che perciò si compilano invece di importarsi. Stesse scelte '
    'di ALLEGATI_USECASE — nomi di origine, baseline in chiave, UC per valore — senza il '
    'richiamo al catalogo delle logiche, perché la condizione di presenza sta già nella sezione. '
    'Dichiarata la sovrapposizione con ANSC_CFG_SEZIONE e la mancanza, fra le sorgenti, delle '
    'interfacce con cui Side gestisce la tabella e del corpo dei suoi trigger: nessuna '
    'interfaccia è proposta (OP-69). ERD rigenerato; corretti nella figura l’elenco delle '
    'tabelle che richiamano la baseline e il riferimento per valore dello store di stato. Tolti '
    'dal DDL di ALLEGATI_USECASE un secondo indice omonimo e due commenti su colonne '
    'inesistenti, residui che rendevano lo script non eseguibile. Aggiunto [R12].')


def main():
    if os.path.exists(DST):
        raise SystemExit(f'{os.path.basename(DST)} esiste già: non si sovrascrive')
    shutil.copy(SRC, DST)
    prima = commenti(DST)
    d = docx.Document(DST)
    fatti = []

    # ------------------------------------------------ 1. capitolo del payload
    ancora = D.h(d, 2, 'Punto di attenzione: i documenti e la loro firma')._p
    modello = next(t for t in d.tables
                   if t.rows[0].cells[0].text.strip() == 'Colonna'
                   and any(r.cells[0].text.strip() == 'ty_allegato' for r in t.rows))
    larghezze = [c.width.inches if c.width else None for c in modello.rows[0].cells]
    larghezze = larghezze if all(larghezze) else None
    for stile, testo in TESTO:
        if stile == 'TABELLA':
            D.tabella(d, ancora, COLONNE, modello, larghezze)
        else:
            D.para(d, ancora, testo, stile=stile)
    fatti.append('nuova sezione «I soggetti previsti dall’UC» con la tabella delle colonne')

    # ------------------------------------------------ 2. elenco delle tabelle
    t = D.trova_tabella(d, 'Oggetto', 'Ruolo')
    assert t.rows[-1].cells[0].text.strip() == 'ALLEGATI_USECASE'
    assert not D.ha_commenti(t.rows[-1]._tr)
    D.clona_riga(t, (
        'SOGGETTI_USECASE', 'Soggetti previsti da ciascun UC e loro ruolo.',
        'Ereditata da Side con i nomi di origine; pende dall’UC per valore e appartiene alla '
        'baseline, come ALLEGATI_USECASE. Porta i contrassegni di dichiarante, comparente e '
        'firmatario, che il mapping ufficiale non dichiara: non si importa, si compila.'))
    fatti.append('riga SOGGETTI_USECASE nell’elenco delle tabelle')

    # ------------------------------------------------ 3. didascalia dell'ERD + figura
    D.sostituisci(d, 'il codice dell’UC su ANSC_CFG_UC e su ALLEGATI_USECASE',
                  'il codice dell’UC su ANSC_CFG_UC, su ALLEGATI_USECASE e su SOGGETTI_USECASE',
                  attese=1, fatti=fatti, etichetta='didascalia dell’ERD')
    D.sostituisci_immagine(d, 'Schema ANSC_USR, con ALLEGATO',
                           os.path.join(IMG, 'erd_ansc_usr.png'))
    fatti.append('ERD sostituito')

    # ------------------------------------------------ 4. Appendice A
    corpo = list(d.element.body.iterchildren())
    # ⚠️ non itertext(): sugli elementi di questo documento restituisce il testo ripetuto
    testi = [Paragraph(x, d).text if x.tag.endswith('}p') else '' for x in corpo]
    idx = [i for i, s in enumerate(testi)
           if s.strip() == 'CREATE INDEX ANSC_USR.IX_ALLEGATI_USECASE_UC']
    if len(idx) != 2:
        raise SystemExit(f'attesi 2 CREATE INDEX IX_ALLEGATI_USECASE_UC, trovati {len(idx)}')
    fine = testi.index("  'Scelta del Comune: il mapping non la dichiara.';")
    da_togliere = corpo[idx[1]:fine + 1]
    if fine + 1 < len(corpo) and not testi[fine + 1].strip():
        da_togliere.append(corpo[fine + 1])          # la riga vuota che li seguiva
    if len(da_togliere) != 10:
        raise SystemExit(f'residuo di ALLEGATI_USECASE: attesi 10 elementi, {len(da_togliere)}')
    for el in da_togliere:
        if D.ha_commenti(el):
            raise SystemExit('un residuo da togliere porta un commento')
        el.getparent().remove(el)
    fatti.append('tolti dal DDL di ALLEGATI_USECASE l’indice duplicato e due COMMENT orfani')

    versione = D.h(d, 3, 'ANSC_CFG_VERSIONE', esatto=True)._p
    D.para(d, versione, 'SOGGETTI_USECASE', stile='Heading 3')
    D.ddl(d, versione, DDL)
    fatti.append('DDL di SOGGETTI_USECASE in Appendice A')

    # ------------------------------------------------ 5. Riferimenti, Open Point, storia
    t = D.trova_tabella(d, 'ID', 'Riferimento')
    assert t.rows[-1].cells[0].text.strip() == 'R11'
    D.clona_riga(t, R12)
    t = next(t for t in d.tables if t.rows[0].cells[0].text.strip() == '#'
             and t.rows[-1].cells[0].text.strip() == 'OP-68')
    assert not D.ha_commenti(t.rows[-1]._tr)
    D.clona_riga(t, OP69)
    D.storia(d, *STORIA)
    fatti.append('[R12], OP-69 e riga di storia')

    d.save(DST)
    dopo = commenti(DST)
    if dopo != prima:
        raise SystemExit(f'commenti: {prima} prima, {dopo} dopo')
    print('\n'.join('· ' + f for f in fatti))
    print(f'commenti preservati: {dopo}')


if __name__ == '__main__':
    main()
