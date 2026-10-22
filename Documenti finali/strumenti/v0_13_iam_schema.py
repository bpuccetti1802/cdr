# -*- coding: utf-8 -*-
"""ANALISI_Identita-Profilazione-IAM v0.12 → v0.13 (20/10/2026).

Richiesta dell'utente: in «Sorgenti Documentali/management-schema.sql» ci sono le DDL PostgreSQL
dello schema di L4 (roma-capitale-management). Leggerle, trasformarle per Oracle e verificare che
il documento riporti le informazioni giuste, eliminando dove serve quelle dedotte dalla mappatura
JPA (v0.10, strumenti/v0_10_iam_strutture.py).

Il capitolo «Le strutture dati del servizio di profilazione» si riscrive per intero: tutto ciò che
vi si dice delle tabelle viene da schema_management.leggi() — la stessa lettura alimenta tabelle
descrittive e DDL per Oracle, così non possono divergere. La mappatura JPA resta solo come
riscontro (le differenze sono riportate perché toccano il servizio).

Che cosa ha cambiato lo schema vero rispetto alla ricostruzione:
  · 24 tabelle, non 16 + 1 vista: 2 tabelle senza classe (applicazione_padre,
    utente_profilo_per_applicazione) e 5 copie di lavoro senza chiavi, 3 delle quali copiano
    utente con password e codice fiscale; v_str_organizzativa è una TABELLA con chiave primaria;
  · 23 chiavi esterne dichiarate (3 delle 4 «proposte» c'erano; le 2 «dedotte dal nome» e quella
    profilo→applicazione no) e 5 unicità (le 3 proposte c'erano, più cd_profilo); nessun CHECK;
  · lunghezze e obbligatorietà diverse su molte colonne; colonne di tracciatura su 9 tabelle;
  · 8 sequenze: manca ente_id_ente_seq (nessuna operazione inserisce enti) e quella dei nodi si
    chiama nodo_struttura_id_nodo_seq mentre la classe chiede nodoStruttura_id_nodo_seq.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v0_13_iam_schema.py
"""
import os
import re
import shutil
import sys

import docx
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D          # noqa: E402
import diagrammi_iam             # noqa: E402
import schema_management as SM   # noqa: E402
import v0_10_iam_strutture as JPA  # noqa: E402  (solo la specifica, per il riscontro)

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIN = os.path.join(BASE, 'Documenti finali')
IMG = os.path.join(FIN, 'strumenti', 'img')
SRC = os.path.join(FIN, 'ANALISI_Identita-Profilazione-IAM_v0.12.docx')
DST = os.path.join(FIN, 'ANALISI_Identita-Profilazione-IAM_v0.13.docx')
SQL_OUT = os.path.join(FIN, 'DDL_Profili-Oracle_v0.2.sql')

OWN, APP, TS = JPA.OWN, JPA.APP, JPA.TS
RL_W, RL_R = JPA.RL_W, JPA.RL_R
TITOLO = JPA.TITOLO
FONTE = '[F14]'

TAB, SEQ = SM.leggi()
PAROLE = {2: 'due', 3: 'tre', 4: 'quattro', 5: 'cinque', 6: 'sei', 7: 'sette', 8: 'otto',
          9: 'nove', 10: 'dieci', 11: 'undici', 12: 'dodici'}
LARGHEZZA = 92               # caratteri di una riga di DDL in Courier 8 nella pagina

# ------------------------------------------------------------------------------ i gruppi
NUCLEO = JPA.NUCLEO
ALTRE = ['ente', 'menu', 'struttura', 'nodo_struttura', 'visibilita', 'nodo_per_visibilita',
         'configurazione', 'avviso', 'utente_per_profilo_get', 'v_str_organizzativa']
SENZA_CLASSE = ['applicazione_padre', 'utente_profilo_per_applicazione']
COPIE = ['utente_10032026', 'utente_ante_sostituzione_cf', 'utente_prod', 'marco_vav',
         'uten_prof_produzione']
MIGRATE = NUCLEO + ALTRE + SENZA_CLASSE
assert sorted(MIGRATE + COPIE) == sorted(TAB), set(TAB) ^ set(MIGRATE + COPIE)

CLASSE = {t['nome']: t['classe'] for t in JPA.TABELLE}
CLASSE['v_str_organizzativa'] = JPA.VISTA['classe']
GRUPPO = {t['nome']: t['gruppo'] for t in JPA.TABELLE}
GRUPPO['v_str_organizzativa'] = 'Di una sola applicazione'
GRUPPO['applicazione_padre'] = 'Catalogo'
GRUPPO['utente_profilo_per_applicazione'] = 'Utenti'
DESC = {t['nome']: t['desc'] for t in JPA.TABELLE}
DESC['v_str_organizzativa'] = ('L’organigramma delle strutture del protocollo, a cui si legano '
                               'le assegnazioni dello sportello unico.')
DESC['applicazione_padre'] = ('Le coppie applicazione figlia – applicazione padre, come '
                              'associazione a sé.')
DESC['utente_profilo_per_applicazione'] = ('Per un’assegnazione di profilo, le applicazioni su '
                                           'cui vale.')
DESC['profilo'] = 'Un insieme di abilitazioni di un’applicazione, con un codice di ruolo.'

# Note che vengono dalla LETTURA DEL CODICE (non dalla mappatura): restano.
NOTE_CODICE = {
    ('applicazione', 'ds_context_root'): 'È ciò che il service mesh risolve a ogni instradamento.',
    ('applicazione', 'ty_auth'): 'Con G l’applicazione unisce le abilitazioni delle figlie.',
    ('profilo', 'cd_ruolo_profilo'): 'Il posto del ruolo di SIPO.',
    ('utente', 'ds_password'): 'Cifrata in modo reversibile (UtenteDomain.java:185); vedi DS-08.',
    ('utente', 'cd_fiscale'): 'Il login dei dipendenti cerca l’utente per codice fiscale.',
    ('utente', 'dt_ultimo_login'): 'Regge la disattivazione dopo sei mesi di inattività.',
    ('utente_per_profilo', 'id_nodo'): 'Nessuna operazione la scrive (MA-03).',
}
# Commenti dello schema che non descrivono la tabella o la colonna: si riportano come sono, si
# segnalano.
COMMENTI_ERRATI = {
    ('profilo', None): 'Piano nazionale',
    ('visibilita', None): 'Profili associati ad un utente',
    ('nodo_per_visibilita', None): 'Profili associati ad un utente',
    ('utente', 'fg_cambio_password'): 'Scadenza password S/N',
}
for (t, c), atteso in COMMENTI_ERRATI.items():
    reale = TAB[t]['commento'] if c is None else \
        next(x['commento'] for x in TAB[t]['col'] if x['nome'] == c)
    assert reale == atteso, (t, c, reale)

TRACCIATURA = ['ds_user_ins_dt', 'ts_ins_dt', 'ds_user_ult_agg_dt', 'ts_ult_agg_dt', 'ds_note_dt']

# ------------------------------------------------------------------------------ nomi Oracle
ABBR = {'utente_per_profilo': 'UPP', 'utente_per_profilo_get': 'UPPG',
        'utente_profilo_per_applicazione': 'UPPA', 'profilo_per_abilitazione': 'PPA',
        'nodo_per_visibilita': 'NPV'}
NOME_VINCOLO = {   # nome nello schema in esercizio → nome Oracle (prefissi, ≤ 30 byte)
    'id_applicazione_sa_uk': 'UK_APPLICAZIONE_SA',
    'applicazione_padre_fk': 'FK_APPLICAZIONE_PADRE',
    'applicazione_per_ambito_fk': 'FK_APPLICAZIONE_AMBITO',
    'fk_appadre_figlio': 'FK_APPADRE_FIGLIO',
    'fk_appadre_padre': 'FK_APPADRE_PADRE',
    'avvisi_per_applicazione_fk': 'FK_AVVISO_APPLICAZIONE',
    'configurazione_per_applicazione_fk': 'FK_CONFIGURAZIONE_APPLICAZ',
    'nodo_struttura_per_struttura_fk': 'FK_NODO_STRUTTURA',
    'utente_username_idx2': 'UK_UTENTE_USERNAME',
    'utente_cdfiscale_idx3': 'UK_UTENTE_CF',
    'utente_per_ente_fk': 'FK_UTENTE_ENTE',
    'cd_profilo_uk': 'UK_PROFILO_CODICE',
    'profilo_per_utente_fk': 'FK_UPP_PROFILO',
    'profilo_utente_nodo_fk': 'FK_UPP_NODO',
    ('utente_per_profilo', 'utente_per_profilo_fk'): 'FK_UPP_UTENTE',
    'fk_profilo': 'FK_UPPG_PROFILO',
    'fk_upg_struttura_ged': 'FK_UPPG_STRUTTURA_GED',
    'fk_utente': 'FK_UPPG_UTENTE',
    'applicazione_fk': 'FK_UPPA_APPLICAZIONE',
    ('utente_profilo_per_applicazione', 'utente_per_profilo_fk'): 'FK_UPPA_UPP',
    'visibilita_dipendenza_fk': 'FK_VISIBILITA_DIPENDENZA',
    'cd_abilitazione_uk': 'UK_ABILITAZIONE_CODICE',
    'abilitazione_per_applicazione_fk': 'FK_ABILITAZIONE_APPLICAZ',
    'abilitazione_per_menu_fk': 'FK_ABILITAZIONE_MENU',
    'nodo_per_visibilita_fk': 'FK_NPV_NODO',
    'visibilita_per_nodo_fk': 'FK_NPV_VISIBILITA',
    'abilitazione_per_profilo_fk': 'FK_PPA_ABILITAZIONE',
    'profilo_per_abilitazione_fk': 'FK_PPA_PROFILO',
}


def nome_ora(tabella, originale):
    return NOME_VINCOLO.get((tabella, originale)) or NOME_VINCOLO[originale]


def pk_ora(t):
    n = f'PK_{t.upper()}'
    return n if len(n) <= 30 else f'PK_{ABBR[t]}'


# ------------------------------------------------------------------------------ tipi
SERIAL = {'serial4': 'int4', 'bigserial': 'int8', 'smallserial': 'int2'}
NUMERICI = {'int2': 'NUMBER(5)', 'int4': 'NUMBER(10)', 'int8': 'NUMBER(19)'}


def tipo_ora(pg):
    base = SERIAL.get(pg, pg)
    if base in NUMERICI:
        return NUMERICI[base]
    m = re.match(r'(\w+)(?:\((\d+)\))?$', pg)
    nome, n = m.group(1), m.group(2)
    if nome == 'varchar':
        return f'VARCHAR2({n} CHAR)'
    if nome == 'bpchar':
        return f'CHAR({n})'
    if nome == 'numeric':
        return f'NUMBER({n})' if n else 'NUMBER'
    return {'text': 'CLOB', 'timestamp': 'TIMESTAMP', 'date': 'DATE', 'bool': 'NUMBER(1)'}[nome]


def seq_di(tabella, col):
    """La sequenza che alimenta la colonna, se lo schema la lega (serial o nextval)."""
    if col['tipo'] in SERIAL:
        s = f'{tabella}_{col["nome"]}_seq'
        assert s in SEQ, s
        return s
    if col['default'] and col['default'].startswith('nextval'):
        return re.search(r"nextval\('(\w+)'", col['default']).group(1)
    return None


def default_ora(tabella, col):
    s = seq_di(tabella, col)
    if s:
        return f'{OWN}.{s}.NEXTVAL'
    d = col['default']
    if d is None:
        return None
    if d in ('true', 'false'):
        return '1' if d == 'true' else '0'
    return re.sub(r'::\w+$', '', d)


# ------------------------------------------------------------------------------ riscontro JPA
def jpa_col(tabella, col):
    for t in JPA.TABELLE:
        if t['nome'] == tabella:
            for c in t['col']:
                if c[0] == col:
                    return c
    return None


def nota_jpa(tabella, col):
    """Che cosa dice la mappatura, solo se diverso dallo schema."""
    if tabella not in CLASSE:
        return ''
    if tabella == 'v_str_organizzativa':
        return ''
    c = jpa_col(tabella, col['nome'])
    if c is None:
        return 'Nella classe base comune.' if col['nome'] in TRACCIATURA else \
            'Non mappata dal servizio.'
    _, jt, _, jobbl, _ = c
    diff = []
    ml = re.search(r'\((\d+)\)', jt)
    rl = re.search(r'\((\d+)\)', col['tipo'])
    if ml and rl and ml.group(1) != rl.group(1):
        diff.append(f'lunghezza {ml.group(1)}')
    if jobbl != col['obbl']:
        diff.append('obbligatoria' if jobbl else 'facoltativa')
    return ('Nella mappatura: ' + ', '.join(diff) + '.') if diff else ''


# ------------------------------------------------------------------------------ ordine e DDL
def ordine():
    """Ordine di creazione imposto dalle chiavi esterne (le autoreferenze non contano)."""
    fatti, out = set(), []
    while len(out) < len(MIGRATE):
        for n in MIGRATE:
            if n in fatti:
                continue
            dip = {f[2] for f in TAB[n]['fk']} - {n}
            if dip <= fatti:
                fatti.add(n)
                out.append(n)
    return out


def controlla():
    nomi = []
    for n in MIGRATE:
        t = TAB[n]
        nomi.append(pk_ora(n))
        nomi += [nome_ora(n, u[0]) for u in t['uk']] + [nome_ora(n, f[0]) for f in t['fk']]
    assert all(len(x) <= 30 for x in nomi), [x for x in nomi if len(x) > 30]
    assert len(nomi) == len(set(nomi)), 'nomi di vincolo ripetuti'
    for c in COPIE:
        assert TAB[c]['pk'] is None and not TAB[c]['fk']


def ddl():
    L = []
    a = L.append
    a('-- ============================================================================')
    a('-- Dominio dei profili: le tabelle di roma-capitale-management su Oracle')
    a('-- Traduzione delle DDL PostgreSQL dello schema «management» in esercizio')
    a('-- (management-schema.sql). Tabelle, colonne, chiavi, unicità, valori predefiniti')
    a('-- e commenti sono quelli dello schema; cambiano i tipi e i nomi dei vincoli, che')
    a('-- in Oracle devono essere unici nello schema (fra parentesi il nome originale).')
    a('-- Gli indici sulle chiavi esterne, ruoli, utenza applicativa e tracciamento sono')
    a('-- raccomandazioni. Nomi di proprietario, utenze, ruoli e tablespace sono proposte')
    a('-- da concordare (PI-40). Richiede Oracle 18c o successivo.')
    a('-- Non si migrano le cinque tabelle di copia, senza chiavi e senza uso nel servizio:')
    a('--   ' + ', '.join(COPIE[:3]) + ',')
    a('--   ' + ', '.join(COPIE[3:]) + ' (DS-14, PI-42).')
    a('-- ============================================================================')
    a('')
    a('-- 1. Tablespace cifrato e proprietario senza accesso (eseguito dai DBA)')
    a(f'CREATE TABLESPACE {TS} DATAFILE SIZE 1G AUTOEXTEND ON NEXT 256M')
    a("  ENCRYPTION USING 'AES256' DEFAULT STORAGE (ENCRYPT);   -- richiede TDE [DA VERIFICARE]")
    a(f'CREATE USER {OWN} NO AUTHENTICATION')
    a(f'  DEFAULT TABLESPACE {TS} QUOTA UNLIMITED ON {TS};')
    a('')
    a('-- 2. Le otto sequenze dello schema, con il valore iniziale dichiarato.')
    a('--    Nella migrazione START WITH = valore corrente della sequenza PostgreSQL + 1.')
    for s, start in SEQ.items():
        if len(s) > 30:
            a(f'-- {len(s)} caratteri: serve Oracle 12.2 o successivo')
        a(f'CREATE SEQUENCE {OWN}.{s}')
        a(f'  START WITH {start} INCREMENT BY 1 NOCACHE NOCYCLE;')
    a('')
    a('-- 3. Tabelle, nell’ordine imposto dalle chiavi esterne')
    for n in ordine():
        t = TAB[n]
        a('')
        a(f'CREATE TABLE {OWN}.{n} (')
        voci = []
        w = max(len(c['nome']) for c in t['col'])
        tw = max(len(tipo_ora(c['tipo'])) for c in t['col'])
        for c in t['col']:
            dflt = default_ora(n, c)
            riga = f'  {c["nome"].ljust(w)}  {tipo_ora(c["tipo"]).ljust(tw)}'
            coda = (f' DEFAULT {dflt}' if dflt else '') + (' NOT NULL' if c['obbl'] else '')
            if len(riga + coda) <= LARGHEZZA:
                voci.append(([(riga + coda).rstrip()], ''))
            else:                              # il valore predefinito va a capo
                voci.append(([riga.rstrip(), '   ' + ' ' * w + coda], ''))
        voci.append(([f'  CONSTRAINT {pk_ora(n)} PRIMARY KEY ({", ".join(t["pk"])})'],
                     f'   -- ({t["pk_nome"]})'))
        for un, cc, specie in t['uk']:
            voci.append(([f'  CONSTRAINT {nome_ora(n, un)} UNIQUE ({", ".join(cc)})'],
                         f'   -- ({un}{", indice univoco" if specie == "indice" else ""})'))
        for fn, cc, rif, rc in t['fk']:
            voci.append(([f'  CONSTRAINT {nome_ora(n, fn)} FOREIGN KEY ({", ".join(cc)})',
                          f'    REFERENCES {OWN}.{rif} ({", ".join(rc)})'], f'   -- ({fn})'))
        for c in t['col']:
            if c['tipo'] == 'bool':
                voci.append(([f'  CONSTRAINT CK_{n.upper()}_{c["nome"].upper()}'
                              f' CHECK ({c["nome"]} IN (0,1))'], '   -- booleano'))
        for i, (righe, nota) in enumerate(voci):
            for r in righe[:-1]:
                a(r)
            a(righe[-1] + ('' if i == len(voci) - 1 else ',') + nota)
        a(f') TABLESPACE {TS};')
        if t['commento']:
            segno = '   -- così nello schema: non descrive la tabella' \
                if (n, None) in COMMENTI_ERRATI else ''
            a(f"COMMENT ON TABLE {OWN}.{n} IS '{t['commento'].replace(chr(39), chr(39) * 2)}';"
              + segno)
        for c in t['col']:
            if c['commento']:
                segno = '   -- così nello schema: è il commento della colonna precedente' \
                    if (n, c['nome']) in COMMENTI_ERRATI else ''
                testa = f'COMMENT ON COLUMN {OWN}.{n}.{c["nome"]} IS'
                corpo = f"'{c['commento'].replace(chr(39), chr(39) * 2)}';"
                if len(testa + ' ' + corpo) <= LARGHEZZA and not segno:
                    a(testa + ' ' + corpo)
                else:
                    a(testa)
                    a('  ' + corpo + segno)
    a('')
    a('-- 4. Indici sulle chiavi esterne non coperte da chiave primaria o unicità.')
    a('--    Non sono nello schema PostgreSQL: in Oracle una chiave esterna senza indice')
    a('--    blocca l’intera tabella figlia quando si cancella o si modifica il padre.')
    for n in ordine():
        t = TAB[n]
        coperte = [t['pk']] + [u[1] for u in t['uk']]
        for fn, cc, _, _ in t['fk']:
            if any(cc == k[:len(cc)] for k in coperte):
                continue
            ix = 'IX_' + nome_ora(n, fn)[3:]
            assert len(ix) <= 30, ix
            a(f'CREATE INDEX {OWN}.{ix}')
            a(f'  ON {OWN}.{n} ({", ".join(cc)}) TABLESPACE {TS};')
    a('')
    a('-- 5. Ruoli: scrittura per il servizio, sola lettura per la revisione degli accessi')
    a(f'CREATE ROLE {RL_W};')
    a(f'CREATE ROLE {RL_R};')
    for n in ordine():
        a(f'GRANT SELECT, INSERT, UPDATE, DELETE ON {OWN}.{n}')
        a(f'  TO {RL_W};')
        a(f'GRANT SELECT ON {OWN}.{n} TO {RL_R};')
    for s in SEQ:
        a(f'GRANT SELECT ON {OWN}.{s} TO {RL_W};')
    a('')
    a('-- 6. Utenza applicativa: solo sessione e ruolo, nessun privilegio di sistema.')
    a('--    La parola chiave sta nel gestore dei segreti, mai nella configurazione versionata.')
    a(f'CREATE USER {APP} IDENTIFIED BY "<dal gestore dei segreti>"')
    a('  PROFILE <profilo con scadenza e blocco dei tentativi> ACCOUNT UNLOCK;')
    a(f'GRANT CREATE SESSION TO {APP};')
    a(f'GRANT {RL_W} TO {APP};')
    a(f'ALTER USER {APP} DEFAULT ROLE ALL;')
    a('-- Le classi non nominano lo schema: con i sinonimi privati il codice non cambia.')
    for n in ordine():
        a(f'CREATE SYNONYM {APP}.{n}')
        a(f'  FOR {OWN}.{n};')
    for s in SEQ:
        a(f'CREATE SYNONYM {APP}.{s}')
        a(f'  FOR {OWN}.{s};')
    a('')
    a('-- 7. Tracciamento delle modifiche (Unified Auditing), conservato fuori dal dominio')
    a('CREATE AUDIT POLICY POL_PROFILI_MODIFICHE')
    traccia = ['utente', 'utente_per_profilo', 'utente_profilo_per_applicazione',
               'utente_per_profilo_get', 'profilo', 'profilo_per_abilitazione', 'abilitazione',
               'applicazione', 'applicazione_padre']
    voci = [f'{az} ON {OWN}.{n}' for n in traccia for az in ('INSERT', 'UPDATE', 'DELETE')]
    for i, v in enumerate(voci):
        a(('  ACTIONS ' if i == 0 else '          ') + v + (';' if i == len(voci) - 1 else ','))
    a('AUDIT POLICY POL_PROFILI_MODIFICHE;')
    a('-- Le modifiche di struttura e di permesso sono rare: si tracciano per tutte le utenze.')
    a('CREATE AUDIT POLICY POL_PROFILI_STRUTTURA')
    a('  ACTIONS CREATE TABLE, ALTER TABLE, DROP TABLE, CREATE INDEX, DROP INDEX,')
    a('          CREATE SEQUENCE, ALTER SEQUENCE, DROP SEQUENCE, CREATE SYNONYM,')
    a('          DROP SYNONYM, GRANT, REVOKE, ALTER USER;')
    a('AUDIT POLICY POL_PROFILI_STRUTTURA;')
    return impagina(L)


def impagina(L):
    """Righe entro LARGHEZZA: il commento in coda sale sopra l'istruzione, le liste lunghe
    vanno a capo. Un letterale di commento non si spezza (resta lungo, se lo è)."""
    out = []
    for r in L:
        if len(r) <= LARGHEZZA or r.lstrip().startswith('--'):
            out.append(r)
            continue
        rientro = ' ' * (len(r) - len(r.lstrip()))
        if '   -- ' in r:
            codice, nota = r.split('   -- ', 1)
            # la nota sale sopra: sopra la riga di REFERENCES va sopra la sua FOREIGN KEY
            dove = len(out) - 1 if codice.lstrip().startswith('REFERENCES') else len(out)
            rif = out[dove] if dove < len(out) else codice
            out.insert(dove, ' ' * (len(rif) - len(rif.lstrip())) + '-- ' + nota)
            r = codice
            if len(r) <= LARGHEZZA:
                out.append(r)
                continue
        if ' TABLESPACE ' in r and r.lstrip().startswith('ON '):
            a, b = r.split(' TABLESPACE ', 1)
            out += [a, rientro + '  TABLESPACE ' + b]
        elif r.startswith('COMMENT ON TABLE') and " IS '" in r:
            a, b = r.split(" IS '", 1)
            out += [a + ' IS', "  '" + b]
        elif ' KEY (' in r or ' UNIQUE (' in r:
            k = r.index('(') + 1
            taglio = r.rindex(', ', 0, LARGHEZZA) + 1
            out += [r[:taglio], rientro + ' ' * (k - len(rientro)) + r[taglio:].lstrip()]
        else:
            out.append(r)
    return out


# ------------------------------------------------------------------------------ i testi
def conteggi():
    m = [TAB[n] for n in MIGRATE]
    return dict(fk=sum(len(t['fk']) for t in m), uk=sum(len(t['uk']) for t in m),
                trac=sum(1 for t in m if all(c in [x['nome'] for x in t['col']]
                                             for c in TRACCIATURA)))


CONTENUTO = [
    ['Gruppo', 'Tabelle', 'Nel servizio'],
    ['Nucleo (7)', ', '.join(NUCLEO), 'Una classe ciascuna.'],
    ['Altre tabelle del servizio (10)', ', '.join(ALTRE), 'Una classe ciascuna; '
     'v_str_organizzativa in sola lettura.'],
    ['Senza classe (2)', ', '.join(SENZA_CLASSE), 'Nessuna classe e nessuna interrogazione: il '
     'servizio non le legge né le scrive.'],
    ['Copie di lavoro (5)', ', '.join(COPIE), 'Nessuna classe; nessuna chiave né vincolo.'],
]

TIPI = [
    ['In PostgreSQL', 'In Oracle', 'Note'],
    ['int2, int4, int8', 'NUMBER(5), NUMBER(10), NUMBER(19)', ''],
    ['smallserial, serial4, bigserial', 'Gli stessi NUMBER, con DEFAULT dalla sequenza',
     'La sequenza che PostgreSQL lega alla colonna diventa esplicita (Oracle 12c).'],
    ['varchar(n)', 'VARCHAR2(n CHAR)', 'Lunghezza in caratteri, come in PostgreSQL.'],
    ['bpchar(n)', 'CHAR(n)', 'Stesso riempimento a destra con spazi.'],
    ['numeric, numeric(n)', 'NUMBER, NUMBER(n)', ''],
    ['text', 'CLOB', 'Due colonne: il testo dell’avviso e il valore di un parametro.'],
    ['timestamp', 'TIMESTAMP', ''],
    ['date', 'DATE', 'In Oracle porta anche l’ora: per la data dell’ultimo accesso è '
     'indifferente.'],
    ['bool', 'NUMBER(1) con vincolo 0/1', 'Una colonna; BOOLEAN dalla versione 23ai.'],
    ["Valori predefiniti 'N'::bpchar, 0, true", "'N', 0, 1", ''],
]


def differenze():
    c = conteggi()
    return [
        ['Aspetto', 'Mappatura del servizio [F13]', 'Schema in esercizio ' + FONTE,
         'Che cosa comporta'],
        ['Tabelle', 'Diciassette classi.', 'Ventiquattro tabelle: le diciassette, due senza '
         'classe e cinque copie di lavoro.', 'Le due senza classe si migrano; le copie no '
         '(DS-14).'],
        ['L’organigramma', 'Una classe in sola lettura su v_str_organizzativa, che il nome fa '
         'pensare a una vista.', 'È una tabella, con chiave primaria e una chiave esterna che '
         'la raggiunge da utente_per_profilo_get.', 'Si migra come tabella; chi la alimenta non '
         'è fra le sorgenti (PI-43).'],
        ['Colonne di tracciatura', 'Assenti dalle classi: autore e data di inserimento e di '
         'ultimo aggiornamento, nota del contesto.', f'Presenti su {c["trac"]} tabelle, con '
         'l’autore dell’inserimento obbligatorio.', 'Le sette classi che le hanno estendono la '
         'classe base di una libreria comune, non fra le sorgenti, che le mappa. Le altre due '
         'tabelle sono quelle senza classe.'],
        ['Colonne che il servizio ignora', 'Non mappate.', 'In profilo: cod_pro, area_pro, '
         'descr, gruppo, flag_speciale e cd_profilo, univoca. In abilitazione: link e ordine.',
         'Le alimenta chi carica i dati fuori dal servizio; un profilo creato dal servizio le '
         'lascia vuote (PI-43).'],
        ['Lunghezze', 'Codice dell’applicazione di 10 caratteri, descrizione dell’abilitazione '
         'di 10, indirizzo del servizio di 125, password di 260, nome di tabella della '
         'visibilità di 250.', 'Rispettivamente 15, 100, 150, 100 e 256.', 'Fa fede lo schema. '
         'La password cifrata deve stare in 100 caratteri, altrimenti l’inserimento fallisce '
         '(PI-44).'],
        ['Obbligatorietà', 'Più severa su dieci colonne: indirizzo, contesto, servizio ed '
         'etichetta dell’applicazione, il suo identificativo esterno, password, telefono, posta '
         'e ufficio dell’utente, valore del parametro.', 'Facoltative. Sono invece obbligatorie, '
         'con un valore predefinito, le cinque colonne dei tentativi e delle scadenze '
         'dell’utente.', 'Fa fede lo schema; le predefinite le valorizza anche il servizio '
         '(UtenteMapper.java:20).'],
        ['Sequenze', 'Nove.', 'Otto: manca quella degli enti, e quella dei nodi si chiama '
         'nodo_struttura_id_nodo_seq.', 'Gli enti non si inseriscono mai dal servizio. Per i '
         'nodi la classe chiede nodoStruttura_id_nodo_seq, che PostgreSQL legge in minuscolo e '
         'non trova: la creazione di un nodo dovrebbe fallire (PI-44).'],
        ['Vincoli', 'Solo chiavi primarie e una colonna univoca.', f'{c["fk"]} chiavi esterne e '
         f'{c["uk"]} vincoli di unicità, fra cui nome utente, codice fiscale e codice '
         'dell’abilitazione nella sua applicazione. Nessun vincolo di valore.', 'La DDL per '
         'Oracle li riporta tutti, e solo quelli.'],
        ['Valori ammessi', 'Nessuno.', 'Solo nei commenti: tipo di login I/D, autorizzazione '
         'G/P, cloud 1/2/3, tipo di parametro S/I/B, priorità dell’avviso da 0 a 3, contrassegni '
         'S/N; per i campi dei tributi stato A/B, tipo utente F, contatore 0.', 'Nessun vincolo '
         'li impone (DS-12).'],
        ['Commenti', '—', 'Tre commenti di tabella non descrivono la tabella (profilo «Piano '
         'nazionale», visibilita e nodo_per_visibilita «Profili associati ad un utente»); '
         'fg_cambio_password ripete quello della scadenza della password.', 'La DDL li riporta '
         'come sono e li segnala.'],
    ]


SENZA_CLASSE_TESTO = [
    ('applicazione_padre. ', 'Rappresenta la relazione fra un’applicazione e la sua '
     'applicazione padre come associazione a sé, con la tracciatura. Ma la stessa relazione sta '
     'già nelle colonne cd_ambito_padre e cd_applicazione_padre di applicazione, ed è quella che '
     'il servizio legge per l’autorizzazione di gruppo (ApplicazioneEntity.java:59-86). Sono due '
     'modi di dire la stessa cosa: se divergono, vince la colonna.'),
    ('utente_profilo_per_applicazione. ', 'Per un’assegnazione di profilo dice su quali '
     'applicazioni valga, e pende dall’assegnazione con una chiave esterna. È il posto per un '
     'profilo valido solo su alcune applicazioni di un gruppo; oggi nessuna operazione la legge, '
     'e se contiene righe la cancellazione di un profilo o la modifica di un utente — che '
     'cancellano le assegnazioni — viene rifiutata dalla chiave esterna.'),
]

COPIE_TAB = [
    ['Tabella', 'Che cosa contiene', 'Chiavi'],
    ['utente_10032026', 'Le colonne di utente, comprese password e codice fiscale.', 'Nessuna'],
    ['utente_ante_sostituzione_cf', 'Le colonne di utente, comprese password e codice fiscale.',
     'Nessuna'],
    ['utente_prod', 'Le colonne di utente, comprese password e codice fiscale.', 'Nessuna'],
    ['marco_vav', 'Le colonne di utente_per_profilo_get: utente, profilo, struttura.',
     'Nessuna'],
    ['uten_prof_produzione', 'Una sola colonna di testo, «aa».', 'Nessuna'],
]
for r in COPIE_TAB[1:4]:
    assert [c['nome'] for c in TAB[r[0]]['col']] == [c['nome'] for c in TAB['utente']['col']]
assert [c['nome'] for c in TAB['marco_vav']['col']] == \
    [c['nome'] for c in TAB['utente_per_profilo_get']['col']]

PASSAGGIO = [
    ['Punto', 'Che cosa tocca', 'Effetto sul servizio'],
    ['Driver e indirizzo', 'Il progetto dichiara il driver PostgreSQL (pom.xml:113) e '
     'l’indirizzo della base dati porta lo schema nel parametro di connessione '
     '(application.properties:9).', 'Driver Oracle al posto di quello PostgreSQL e nuovo '
     'indirizzo: è un rilascio del servizio.'],
    ['Dialetto', 'Non dichiarato: lo strato di persistenza lo ricava dalla connessione.',
     'Nessuno.'],
    ['Interrogazioni', 'Tutte in linguaggio di interrogazione degli oggetti, in file separati; '
     'nessuna interrogazione nativa.', 'Portabili. Alcune applicano la conversione in minuscolo '
     'anche a colonne numeriche (Applicazione.xml:42, 47): Oracle le converte da sé, ma va '
     'provato in collaudo [DA VERIFICARE].'],
    ['Schema', 'Le classi non nominano lo schema; oggi lo sceglie l’indirizzo di connessione.',
     'Sinonimi privati dell’utenza applicativa, già nella DDL: il codice non cambia.'],
    ['Nomi dei vincoli', 'In PostgreSQL sono unici per tabella: utente_per_profilo_fk compare '
     'su due tabelle, e {lunghi} nomi superano i trenta caratteri.', 'Rinominati con i prefissi; '
     'il servizio non li nomina, quindi nessun effetto. Il nome originale resta nella DDL '
     'accanto a ciascuno.'],
    ['Sequenze', 'Otto; quella delle abilitazioni ha un nome di 32 caratteri. Quella dei nodi '
     'non ha il nome che la classe chiede.', 'Serve Oracle 12.2 o successivo. In Oracle i nomi '
     'non tra virgolette diventano maiuscoli, e quindi la sequenza dei nodi chiesta dalla classe '
     'non si trova nemmeno lì: va rinominata la sequenza o corretta la classe (PI-44).'],
    ['Testi lunghi e contrassegni', 'Due colonne «text» e un booleano.', 'CLOB e NUMBER(1). La '
     'lettura del CLOB come stringa e del booleano come numero va provata [DA VERIFICARE].'],
    ['Chiavi esterne', 'Sono già nello schema PostgreSQL: la cancellazione di un’abilitazione, '
     'un’applicazione, un menu, un ambito, una struttura o una regola di visibilità ancora '
     'usati è già oggi rifiutata.', 'Nessun cambiamento di comportamento: Oracle rifiuta le '
     'stesse cancellazioni. Gli indici aggiunti evitano che la verifica blocchi le tabelle '
     'figlie.'],
    ['Dati esistenti', 'Lo schema PostgreSQL in esercizio, senza le copie di lavoro.',
     'Migrazione dei dati e riallineamento delle sequenze al valore corrente più uno.'],
    ['Titolarità', 'Il servizio e la sua base dati sono della piattaforma, che serve anche '
     'altre aree dell’ente.', 'La scelta di Oracle va presa con il titolare (PI-41).'],
]

RACC_MODIFICHE = {
    'DS-08': ['DS-08', 'Le **password come impronta**, e solo dove servono.', 'Oggi sono cifrate '
              'in modo reversibile con una chiave unica. Per i dipendenti l’accesso passa da IAM '
              'e la password locale non serve: la colonna è già facoltativa nello schema.',
              'Impronta con sale calcolata dal servizio, non dal database; colonna vuota per chi '
              'entra da IAM.'],
    'DS-12': ['DS-12', '**Integrità nel database**, non solo nel codice.', 'Lo schema dichiara '
              'già chiavi esterne e unicità, che impediscono assegnazioni a profili inesistenti e '
              'codici duplicati. Mancano i vincoli sui valori ammessi, che stanno solo nei '
              'commenti, e il legame del nodo con il nodo padre e del menu con l’applicazione.',
              'La DDL riporta i vincoli dello schema; quelli mancanti si aggiungono dopo aver '
              'verificato i dati, d’accordo con il titolare.'],
}
DS14 = ['DS-14', '**Niente copie di lavoro nel dominio**.', 'Lo schema in esercizio contiene '
        'cinque copie senza chiavi, tre delle quali con le colonne di password e codice fiscale '
        'degli utenti: se popolate, sono dati personali fuori da ogni vincolo e ciclo di vita.', 'Non si '
        'migrano; nello schema attuale si cancellano, dopo averne accertato l’uso (PI-42). Le '
        'copie di salvataggio vanno nelle copie di sicurezza, non nello schema.']

PI_NUOVI = [
    ('PI-42', 'Le cinque copie di lavoro dello schema (utente_10032026, '
     'utente_ante_sostituzione_cf, utente_prod, marco_vav, uten_prof_produzione): chi le ha '
     'create, se contengono dati di produzione e se possono essere cancellate. Tre hanno le '
     'colonne di password e codice fiscale.', 'Titolare della piattaforma'),
    ('PI-43', 'Chi alimenta ciò che il servizio non scrive: le tabelle applicazione_padre e '
     'utente_profilo_per_applicazione, l’organigramma v_str_organizzativa, e in profilo e '
     'abilitazione le colonne che le classi non mappano; e quale delle due rappresentazioni '
     'dell’applicazione padre faccia fede.', 'Titolare della piattaforma'),
    ('PI-44', 'Due verifiche in collaudo: la creazione di un nodo organizzativo, che chiede una '
     'sequenza con un nome diverso da quella esistente, e la lunghezza della password cifrata, '
     'che la colonna limita a cento caratteri.', 'Titolare della piattaforma / Collaudo'),
]

PI39_CHIUSO = ('Chiuso. Le DDL dello schema «management» in esercizio, per esempio l’estrazione '
               'della sola struttura dal catalogo PostgreSQL. Ricevute ' + FONTE + ': il '
               'capitolo delle strutture dati e la DDL per Oracle sono costruiti su di esse.')

SOSTITUZIONI = [
    ('Ne ricostruisce infine le strutture dati, che in attesa delle DDL sono estratte dalla '
     'mappatura JPA del codice, ne propone la DDL per Oracle',
     'Ne descrive infine le strutture dati, sulle DDL dello schema in esercizio, ne dà la '
     'traduzione per Oracle', 1),
    ('Le strutture dati del servizio dei profili, in attesa delle DDL dello schema, sono state '
     'ricostruite dalla mappatura JPA del codice. Ne discendono una DDL per Oracle',
     'Le strutture dati del servizio dei profili sono descritte sulle DDL dello schema in '
     'esercizio, che contiene anche cinque copie di lavoro, tre con le colonne di password e '
     'codice fiscale, da non portare con sé. Ne discendono una DDL per Oracle', 1),
    ('In assenza delle DDL è la fonte delle strutture dati del servizio dei profili.',
     'Per le strutture dati del servizio dei profili fa fede lo schema in esercizio ' + FONTE +
     '; la mappatura serve a riscontro.', 1),
    ('17, in uno schema PostgreSQL proprio.',
     '17 classi, su uno schema PostgreSQL proprio di 24 tabelle: due senza classe e cinque '
     'copie di lavoro ' + FONTE + '.', 1),
    ('cancellare un’abilitazione lascia le associazioni ai profili.',
     'cancellare un’abilitazione ancora usata da un profilo è rifiutato dalla chiave esterna '
     'dello schema, e il servizio non lo controlla prima: l’operatore riceve un errore '
     'invece di un messaggio.', 1),
    ('Dichiarazioni incoerenti nel modello: la descrizione dell’abilitazione è di dieci '
     'caratteri, e la password è obbligatoria anche per chi entra soltanto da IAM [DA VERIFICARE '
     'sulla DDL].',
     'Il modello delle classi non descrive la base dati: la descrizione dell’abilitazione è di '
     'dieci caratteri contro cento, il codice dell’applicazione di dieci contro quindici, la '
     'password obbligatoria e di 260 caratteri contro facoltativa e di cento, e mancano otto '
     'colonne di profilo e abilitazione. Finché lo schema non si genera dal codice non c’è '
     'errore, ma chi legge le classi si sbaglia.', 1),
    ('Il codice dell’applicazione ha al massimo dieci caratteri (PI-35).',
     'Il codice dell’applicazione ha al massimo quindici caratteri nello schema, dieci nelle '
     'classi del servizio: conviene restare nei dieci (PI-35).', 1),
    ('I codici sono di due e di dieci caratteri.',
     'I codici sono di due e di quindici caratteri nello schema, di due e di dieci nelle classi '
     'del servizio.', 1),
    ('e come sia valorizzata la colonna della password, che il modello dichiara obbligatoria, '
     'per gli utenti che entrano soltanto da IAM.',
     'e se per gli utenti che entrano soltanto da IAM la colonna della password resti vuota: lo '
     'schema la ammette, le classi del servizio la dichiarano obbligatoria.', 1),
]

GLOSSARIO_NUOVO = [
    ('Copia di lavoro', 'Nello schema dei profili, una tabella creata copiando un’altra, senza '
     'chiavi né vincoli e senza uso nel servizio. Non si migra.'),
]


def main():
    controlla()
    if os.path.exists(DST):
        os.remove(DST)                         # solo un'esecuzione precedente di questo script
    shutil.copy(SRC, DST)
    d = docx.Document(DST)
    modello = d.tables[3]
    fatti = []
    c = conteggi()
    righe_ddl = ddl()

    # ------------------------------------------------ fuori dal capitolo
    for vecchio, nuovo, n in SOSTITUZIONI:
        D.sostituisci(d, vecchio, nuovo, attese=n, fatti=fatti)
    pa = D.trova_tabella(d, '#', 'Questione', 'A chi compete')
    r39 = [r for r in pa.rows if r.cells[0].text.strip() == 'PI-39']
    assert len(r39) == 1
    D.riscrivi_cella(r39[0].cells[1], PI39_CHIUSO)
    assert pa.rows[-1].cells[0].text.strip() == 'PI-41', pa.rows[-1].cells[0].text
    for r in PI_NUOVI:
        D.clona_riga(pa, r)
    fatti.append('PI-39 chiuso; nuovi PI-42…PI-44')
    gl = D.trova_tabella(d, 'Termine', 'Significato in questo documento')
    for r in GLOSSARIO_NUOVO:
        D.clona_riga(gl, r)
    fo = D.trova_tabella(d, '#', 'Riferimento', 'Natura')
    assert fo.rows[-1].cells[0].text.strip() == '[F13]', fo.rows[-1].cells[0].text
    D.clona_riga(fo, (FONTE, 'management-schema.sql — estrazione della sola struttura dello '
                      'schema PostgreSQL «management» di roma-capitale-management in esercizio: '
                      '24 tabelle, 8 sequenze, vincoli e commenti, nessun dato',
                      'Struttura della base dati'))
    fatti.append(f'fonte {FONTE}')

    # ------------------------------------------------ il capitolo: si svuota e si riscrive
    blocco = D.sezione(d, TITOLO, livello=1)
    assert blocco, TITOLO
    for el in blocco[1:]:
        assert not D.ha_commenti(el)
        el.getparent().remove(el)
    fine = D.h(d, 1, 'Punti aperti')._p

    def p(testo):
        D.para(d, fine, pezzi=D.segmenta('', testo)) if '**' in testo else D.para(d, fine, testo)

    def h2(testo):
        D.para(d, fine, testo, stile='Heading 2')

    def tab(righe, larghezze):
        return D.tabella(d, fine, righe, modello, larghezze)

    p('**Le strutture di questo capitolo sono quelle dello schema PostgreSQL «management» in '
      f'esercizio, ricevute come DDL {FONTE}.** La mappatura JPA del servizio [F13] serve a '
      'riscontro: dove dice altro, fa fede lo schema, e le differenze sono riportate perché '
      'toccano il servizio.')
    p('Il servizio non genera lo schema dal codice e non ha script di creazione né di '
      'migrazione: la base dati è gestita a parte. roma-capitale-auth e il service mesh non '
      'hanno tabelle proprie e leggono management attraverso i suoi percorsi interni: le '
      'strutture di questo capitolo sono quindi tutte quelle del servizio dei profili.')

    h2('Che cosa contiene lo schema')
    p(f'Lo schema ha {len(TAB)} tabelle e {len(SEQ)} sequenze. Diciassette tabelle hanno una '
      f'classe nel servizio; due non ne hanno; cinque sono copie di lavoro. Lo schema dichiara '
      f'{c["fk"]} chiavi esterne e {c["uk"]} vincoli di unicità, nessun vincolo sui valori e '
      f'nessun indice oltre a quelli delle chiavi.')
    tab(CONTENUTO, [1.5, 3.2, 1.8])

    h2('Utenti, profili e abilitazioni, colonna per colonna')
    p('Le sette tabelle del nucleo sono quelle che decidono che cosa un operatore può fare: '
      'l’utente riceve profili, il profilo raccoglie abilitazioni, l’abilitazione appartiene a '
      'un’applicazione di un ambito. Per ciascuna colonna: il tipo nello schema e in Oracle, '
      'l’obbligatorietà, il commento dello schema, e ciò che dice la mappatura quando è diverso. '
      'Le cinque colonne di tracciatura — ds_user_ins_dt, obbligatoria, ts_ins_dt, '
      'ds_user_ult_agg_dt, ts_ult_agg_dt e ds_note_dt: autore e momento dell’inserimento e '
      'dell’ultimo aggiornamento, nota sul contesto — sono uguali in ogni tabella che le ha e '
      'non si ripetono; nel servizio le mappa la classe base comune.')
    for n in NUCLEO:
        t = TAB[n]
        trac = all(x in [k['nome'] for k in t['col']] for x in TRACCIATURA)
        D.titolo_ddl(d, fine, f'{n} — {DESC[n]} Classe {CLASSE[n]}.'
                     + (' Più le cinque colonne di tracciatura.' if trac else ''))
        righe = [['Colonna', 'PostgreSQL', 'Oracle', 'Obbl.', 'Note']]
        for col in t['col']:
            if col['nome'] in TRACCIATURA:
                continue
            note = []
            if col['commento']:
                note.append(f'«{col["commento"].replace(chr(39), chr(8217))}».')
            if col['default'] and not seq_di(n, col):
                note.append(f'Predefinito {default_ora(n, col)}.')
            if seq_di(n, col):
                note.append(f'Da {seq_di(n, col)}.')
            if NOTE_CODICE.get((n, col['nome'])):
                note.append(NOTE_CODICE[(n, col['nome'])])
            nj = nota_jpa(n, col)
            if nj:
                note.append(nj)
            righe.append([col['nome'], col['tipo'], tipo_ora(col['tipo']),
                          'sì' if col['obbl'] else '', ' '.join(note)])
        tz = tab(righe, [1.5, 0.9, 1.3, 0.45, 2.35])
        for r in tz.rows[1:]:
            for run in r.cells[0].paragraphs[0].runs:
                run.text = run.text.replace('_', '_​')
    p('Le chiavi del nucleo: utente ha come univoci il nome utente e il codice fiscale; '
      'abilitazione il codice nella sua applicazione; profilo il codice cd_profilo, che il '
      'servizio non usa. Le assegnazioni pendono da utente e profilo; le abilitazioni di un '
      'profilo stanno in profilo_per_abilitazione, che pende da entrambi; l’abilitazione pende '
      'dall’applicazione e l’applicazione dall’ambito. Il profilo, invece, non pende dall’applicazione: lo schema non lo vincola.')

    h2('Le altre tabelle')
    p('Le altre dieci tabelle del servizio e le due senza classe completano lo schema: l’ente '
      'dell’utente, l’organizzazione e la visibilità sui dati, il registro della piattaforma e '
      'la parte specifica dello sportello unico.')
    righe = [['Tabella', 'Gruppo', 'Chiave', 'Riferimenti', 'Classe']]
    for n in ALTRE + SENZA_CLASSE:
        t = TAB[n]
        rif = '; '.join(f'{", ".join(cc)} → {r}' for _, cc, r, _ in t['fk']) or '—'
        righe.append([n, GRUPPO[n], ', '.join(t['pk']), rif, CLASSE.get(n, 'nessuna')])
    tz = tab(righe, [1.6, 1.1, 1.3, 1.9, 1.5])
    tz._tbl.tblPr.append(docx.oxml.parse_xml(
        '<w:tblLayout xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'w:type="fixed"/>'))
    for r in tz.rows[1:]:
        for cc in (r.cells[0], r.cells[2], r.cells[3], r.cells[4]):
            for run in cc.paragraphs[0].runs:
                run.text = run.text.replace('_', '_​').replace('Entity', '​Entity')
    p('**Due tabelle non hanno classe**, e il servizio non le legge né le scrive:')
    for testa, corpo in SENZA_CLASSE_TESTO:
        D.voce(d, fine, testa, corpo)
    p('Chi le alimenti, insieme all’organigramma e alle colonne che le classi ignorano, non è '
      'fra le sorgenti (PI-43). Si migrano come sono, perché sono parte dello schema.')

    h2('Le copie di lavoro')
    assert all(TAB[k]['commento'] is None and not any(x['commento'] for x in TAB[k]['col'])
               for k in COPIE)
    p('Cinque tabelle sono copie di altre: non hanno chiave primaria, né vincoli, '
      'né commenti, e nessuna classe le nomina. I nomi fanno pensare a copie di salvataggio prese '
      'prima di interventi sui dati: una porta la data del 10 marzo 2026, una è precedente alla '
      '«sostituzione» del codice fiscale, due si dicono «di produzione». **Tre di esse hanno tutte le colonne della tabella degli utenti, '
      'comprese password e codice fiscale**: se sono popolate, e il file delle DDL non lo dice, '
      'sono dati personali fuori da ogni vincolo e da ogni ciclo di vita.')
    tab(COPIE_TAB, [1.9, 3.6, 1.0])
    p('Non si migrano e non entrano nella DDL per Oracle; nello schema attuale vanno cancellate, '
      'dopo averne accertato l’uso con il titolare (DS-14, PI-42).')

    h2('Che cosa dice lo schema che la mappatura non dice')
    dif = differenze()
    p(f'Il confronto fra lo schema e le classi del servizio dà {PAROLE[len(dif) - 1]} differenze. Nessuna '
      f'impedisce il funzionamento ordinario; due vanno provate in collaudo (PI-44).')
    tab(dif, [1.1, 1.7, 1.9, 1.8])

    h2('I tipi, da PostgreSQL a Oracle')
    tab(TIPI, [1.8, 2.1, 2.6])

    h2('Il passaggio a Oracle: che cosa tocca il servizio')
    p('Portare le tabelle su Oracle non richiede di riscrivere il servizio, perché le '
      'interrogazioni non dipendono dalla base dati; richiede però un rilascio, e alcune prove.')
    lunghi = sum(1 for n in MIGRATE for x in [TAB[n]['pk_nome']] + [u[0] for u in TAB[n]['uk']]
                 + [f[0] for f in TAB[n]['fk']] if len(x) > 30)
    passaggio = [[cella.replace('{lunghi}', PAROLE[lunghi]) for cella in r] for r in PASSAGGIO]
    tab(passaggio, [1.3, 2.4, 2.7])

    h2('La DDL per Oracle')
    nseq = len(SEQ)
    p(f'La DDL traduce lo schema in esercizio nell’ordine imposto dalle chiavi esterne: '
      f'tablespace e proprietario, le {nseq} sequenze, le {len(MIGRATE)} tabelle con chiavi, '
      f'unicità, valori predefiniti e commenti, poi gli indici sulle chiavi esterne, i ruoli, '
      f'l’utenza applicativa con i sinonimi e il tracciamento. Nomi di tabelle e colonne sono '
      f'quelli dello schema, perché il servizio li usa così; i nomi dei vincoli seguono i '
      f'prefissi PK_, UK_, FK_, CK_, IX_, stanno nei trenta caratteri e portano accanto il nome '
      f'originale. **Non aggiunge vincoli che lo schema non abbia**, salvo quello che traduce '
      f'il booleano. Le cinque copie di lavoro non ci sono. I nomi di proprietario ({OWN}), '
      f'utenza ({APP}), ruoli e tablespace sono proposte da concordare (PI-40). La stessa DDL è '
      f'nel file DDL_Profili-Oracle_v0.2.sql.')
    D.ddl(d, fine, righe_ddl)

    h2('Un dominio a parte: le raccomandazioni di sicurezza')
    p('Queste tabelle non sono dati di un’applicazione fra le altre: dicono chi può entrare in '
      'ciascuna applicazione della piattaforma, e con quali diritti. Per questo **vanno '
      'collocate in un dominio a parte**, con un perimetro proprio. Le raccomandazioni valgono '
      'su Oracle e varrebbero anche se la base dati restasse PostgreSQL.')
    nfig = max(int(m.group(1)) for q in d.paragraphs
               for m in [re.match(r'Figura (\d+)', q.text.strip())] if m) + 1
    png = os.path.join(IMG, diagrammi_iam.dominio(IMG))
    D.immagine(d, fine, png, 6.3,
               f'Figura {nfig} — Il dominio dei profili: le tabelle del servizio in un perimetro '
               f'proprio, raggiunto da una sola utenza applicativa, senza collegamenti diretti '
               f'con gli schemi di SIPO.')
    racc = [r[:] for r in JPA.RACCOMANDAZIONI]
    for i, r in enumerate(racc):
        if r[0] in RACC_MODIFICHE:
            racc[i] = RACC_MODIFICHE[r[0]]
    racc.append(DS14)
    tab(racc, [0.6, 1.8, 2.2, 1.8])
    p('Il minimo è lo schema dedicato in un tablespace cifrato, con il proprietario senza accesso, '
      'una sola utenza applicativa, nessun collegamento con gli schemi di SIPO e nessuna copia di '
      'lavoro (DS-01…DS-07, DS-14). Il raccomandato è la base dati collegabile dedicata, che '
      'aggiunge un confine di istanza, copie di sicurezza e amministrazione separate. Quale delle '
      'due sia praticabile dipende dalla versione e dalle opzioni di Oracle dell’ente (PI-40).')
    fatti.append(f'capitolo riscritto sullo schema: {len(TAB)} tabelle ({len(MIGRATE)} migrate, '
                 f'{len(COPIE)} copie), {c["fk"]} FK, {c["uk"]} UK, DDL di {len(righe_ddl)} '
                 f'righe, DS-14, Figura {nfig}')

    D.storia(d, '20/10/2026', '0.13',
             'Scopo · Executive summary · Il servizio di profilazione della piattaforma · '
             'Gli interventi di manutenzione · Le strutture dati del servizio di profilazione · '
             'Glossario · Punti aperti · Fonti',
             'Le strutture dati del servizio dei profili sono riscritte sulle DDL dello schema '
             'in esercizio, che sostituiscono la ricostruzione dalla mappatura JPA: '
             'ventiquattro tabelle, di cui due senza classe e cinque copie di lavoro con '
             'colonne di password e codice fiscale da non migrare; l’organigramma è una tabella; chiavi '
             'esterne e unicità sono quelle dello schema. Riportate le differenze fra schema e '
             'classi del servizio. La DDL per Oracle traduce lo schema senza vincoli aggiunti. '
             'Nuova raccomandazione DS-14; PI-39 chiuso, nuovi PI-42…PI-44.')
    for f in D.frontespizio(d, '0.13', 'ANALISI_Identita-Profilazione-IAM_v0.13'):
        fatti.append(f)

    d.save(DST)
    with open(SQL_OUT, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(righe_ddl) + '\n')
    print('\n'.join('  · ' + f for f in fatti))
    cap, ntab, fig = D.riepilogo(DST)
    print(f'  capitoli {cap}, tabelle {ntab}, immagini {fig}')
    print('  scritto', DST)


if __name__ == '__main__':
    main()
