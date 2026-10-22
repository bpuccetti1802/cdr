-- ============================================================================
-- Dominio dei profili: le tabelle di roma-capitale-management su Oracle
-- Traduzione delle DDL PostgreSQL dello schema «management» in esercizio
-- (management-schema.sql). Tabelle, colonne, chiavi, unicità, valori predefiniti
-- e commenti sono quelli dello schema; cambiano i tipi e i nomi dei vincoli, che
-- in Oracle devono essere unici nello schema (fra parentesi il nome originale).
-- Gli indici sulle chiavi esterne, ruoli, utenza applicativa e tracciamento sono
-- raccomandazioni. Nomi di proprietario, utenze, ruoli e tablespace sono proposte
-- da concordare (PI-40). Richiede Oracle 18c o successivo.
-- Non si migrano le cinque tabelle di copia, senza chiavi e senza uso nel servizio:
--   utente_10032026, utente_ante_sostituzione_cf, utente_prod,
--   marco_vav, uten_prof_produzione (DS-14, PI-42).
-- ============================================================================

-- 1. Tablespace cifrato e proprietario senza accesso (eseguito dai DBA)
CREATE TABLESPACE TS_PROFILI DATAFILE SIZE 1G AUTOEXTEND ON NEXT 256M
  ENCRYPTION USING 'AES256' DEFAULT STORAGE (ENCRYPT);   -- richiede TDE [DA VERIFICARE]
CREATE USER PROFILI_OWN NO AUTHENTICATION
  DEFAULT TABLESPACE TS_PROFILI QUOTA UNLIMITED ON TS_PROFILI;

-- 2. Le otto sequenze dello schema, con il valore iniziale dichiarato.
--    Nella migrazione START WITH = valore corrente della sequenza PostgreSQL + 1.
-- 32 caratteri: serve Oracle 12.2 o successivo
CREATE SEQUENCE PROFILI_OWN.abilitazione_id_abilitazione_seq
  START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE PROFILI_OWN.avvisi_id_avviso_seq
  START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE PROFILI_OWN.menu_id_menu_seq
  START WITH 175 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE PROFILI_OWN.nodo_struttura_id_nodo_seq
  START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE PROFILI_OWN.profilo_id_profilo_seq
  START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE PROFILI_OWN.struttura_id_struttura_seq
  START WITH 27 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE PROFILI_OWN.utente_id_utente_seq
  START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE PROFILI_OWN.visibilita_id_visibilita_seq
  START WITH 45 INCREMENT BY 1 NOCACHE NOCYCLE;

-- 3. Tabelle, nell’ordine imposto dalle chiavi esterne

CREATE TABLE PROFILI_OWN.profilo (
  id_profilo          NUMBER(19)
                      DEFAULT PROFILI_OWN.profilo_id_profilo_seq.NEXTVAL NOT NULL,
  ds_profilo          VARCHAR2(50 CHAR) NOT NULL,
  fg_profilo_default  CHAR(1)           DEFAULT 'N' NOT NULL,
  cd_ruolo_profilo    VARCHAR2(50 CHAR),
  nm_valore           NUMBER(10),
  cd_ambito           CHAR(2),
  cd_applicazione     VARCHAR2(15 CHAR),
  ds_user_ins_dt      VARCHAR2(50 CHAR) NOT NULL,
  ts_ins_dt           TIMESTAMP,
  ds_user_ult_agg_dt  VARCHAR2(50 CHAR),
  ts_ult_agg_dt       TIMESTAMP,
  ds_note_dt          VARCHAR2(50 CHAR),
  cod_pro             VARCHAR2(50 CHAR),
  area_pro            VARCHAR2(30 CHAR),
  descr               VARCHAR2(50 CHAR),
  gruppo              VARCHAR2(20 CHAR),
  flag_speciale       NUMBER,
  cd_profilo          VARCHAR2(50 CHAR),
  CONSTRAINT PK_PROFILO PRIMARY KEY (id_profilo),   -- (profilo_pk)
  CONSTRAINT UK_PROFILO_CODICE UNIQUE (cd_profilo)   -- (cd_profilo_uk, indice univoco)
) TABLESPACE TS_PROFILI;
-- così nello schema: non descrive la tabella
COMMENT ON TABLE PROFILI_OWN.profilo IS 'Piano nazionale';
COMMENT ON COLUMN PROFILI_OWN.profilo.id_profilo IS 'Identificativo del profilo';
COMMENT ON COLUMN PROFILI_OWN.profilo.ds_profilo IS 'Descrizione del profilo';
COMMENT ON COLUMN PROFILI_OWN.profilo.fg_profilo_default IS 'Profilo di default S/N';
COMMENT ON COLUMN PROFILI_OWN.profilo.cd_ruolo_profilo IS
  'Codice Ruolo associato al profilo - utilizzato da tributi';
COMMENT ON COLUMN PROFILI_OWN.profilo.nm_valore IS
  'Valore associato al profilo - utilizzato da tributi';
COMMENT ON COLUMN PROFILI_OWN.profilo.cd_ambito IS 'Codice ambito';
COMMENT ON COLUMN PROFILI_OWN.profilo.cd_applicazione IS 'Codice applicazione';
COMMENT ON COLUMN PROFILI_OWN.profilo.ds_user_ins_dt IS 'Utente che ha inserito la riga';
COMMENT ON COLUMN PROFILI_OWN.profilo.ts_ins_dt IS 'Timestamp inserimento';
COMMENT ON COLUMN PROFILI_OWN.profilo.ds_user_ult_agg_dt IS
  'Utente che per ultimo ha aggiornato la riga';
COMMENT ON COLUMN PROFILI_OWN.profilo.ts_ult_agg_dt IS 'Timestamp ultimo aggiornamento';
COMMENT ON COLUMN PROFILI_OWN.profilo.ds_note_dt IS
  'Descrizione contesto ultimo aggiornamento';

CREATE TABLE PROFILI_OWN.ambito (
  cd_ambito  CHAR(2)           NOT NULL,
  ds_ambito  VARCHAR2(50 CHAR) NOT NULL,
  CONSTRAINT PK_AMBITO PRIMARY KEY (cd_ambito)   -- (ambito_pk)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.ambito IS 'Area funzionale';
COMMENT ON COLUMN PROFILI_OWN.ambito.cd_ambito IS 'Codice ambito';
COMMENT ON COLUMN PROFILI_OWN.ambito.ds_ambito IS 'Descrizione ambito';

CREATE TABLE PROFILI_OWN.ente (
  id_ente  NUMBER(10)         NOT NULL,
  cd_ente  NUMBER(10)         NOT NULL,
  ds_ente  VARCHAR2(250 CHAR),
  CONSTRAINT PK_ENTE PRIMARY KEY (id_ente)   -- (ente_pk)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.ente IS 'Ente';
COMMENT ON COLUMN PROFILI_OWN.ente.id_ente IS 'Identificativo ente';
COMMENT ON COLUMN PROFILI_OWN.ente.cd_ente IS 'Codice ente';
COMMENT ON COLUMN PROFILI_OWN.ente.ds_ente IS 'Descrizione ente';

CREATE TABLE PROFILI_OWN.menu (
  id_menu             NUMBER(10)
                      DEFAULT PROFILI_OWN.menu_id_menu_seq.NEXTVAL NOT NULL,
  cd_menu             VARCHAR2(50 CHAR)  NOT NULL,
  ds_menu             VARCHAR2(100 CHAR),
  id_applicazione_sa  NUMBER(10),
  CONSTRAINT PK_MENU PRIMARY KEY (id_menu)   -- (menu_pk)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.menu IS 'Menu di macro funzioni - usato da tributi';
COMMENT ON COLUMN PROFILI_OWN.menu.id_menu IS 'Identificativo macro funzione';
COMMENT ON COLUMN PROFILI_OWN.menu.cd_menu IS 'Codice Menu';
COMMENT ON COLUMN PROFILI_OWN.menu.ds_menu IS 'Descrizione menu';
COMMENT ON COLUMN PROFILI_OWN.menu.id_applicazione_sa IS
  'Identificativo applicazione del sistema d''area';

CREATE TABLE PROFILI_OWN.struttura (
  id_struttura  NUMBER(10)
                DEFAULT PROFILI_OWN.struttura_id_struttura_seq.NEXTVAL NOT NULL,
  nm_struttura  VARCHAR2(200 CHAR)  NOT NULL,
  ds_struttura  VARCHAR2(1000 CHAR) NOT NULL,
  CONSTRAINT PK_STRUTTURA PRIMARY KEY (id_struttura)   -- (struttura_pk)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.struttura IS 'Struttura in ambito Roma Capitale';
COMMENT ON COLUMN PROFILI_OWN.struttura.id_struttura IS 'Identificativo struttura';
COMMENT ON COLUMN PROFILI_OWN.struttura.nm_struttura IS 'nome struttura';
COMMENT ON COLUMN PROFILI_OWN.struttura.ds_struttura IS 'Descrizione struttura';

CREATE TABLE PROFILI_OWN.nodo_struttura (
  id_nodo        NUMBER(10)          NOT NULL,
  id_struttura   NUMBER(10)          NOT NULL,
  id_nodo_padre  NUMBER(10),
  cd_nodo        VARCHAR2(50 CHAR)   NOT NULL,
  nm_nodo        VARCHAR2(200 CHAR)  NOT NULL,
  ds_nodo        VARCHAR2(1000 CHAR),
  CONSTRAINT PK_NODO_STRUTTURA PRIMARY KEY (id_nodo),   -- (nodo_struttura_pk)
  CONSTRAINT FK_NODO_STRUTTURA FOREIGN KEY (id_struttura)
    REFERENCES PROFILI_OWN.struttura (id_struttura)   -- (nodo_struttura_per_struttura_fk)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.nodo_struttura IS 'Nodo struttura';
COMMENT ON COLUMN PROFILI_OWN.nodo_struttura.id_nodo IS 'Identificativo nodo';
COMMENT ON COLUMN PROFILI_OWN.nodo_struttura.id_struttura IS 'Identificativo struttura';
COMMENT ON COLUMN PROFILI_OWN.nodo_struttura.id_nodo_padre IS 'Identificativo nodo padre';
COMMENT ON COLUMN PROFILI_OWN.nodo_struttura.cd_nodo IS 'Codice del nodo';
COMMENT ON COLUMN PROFILI_OWN.nodo_struttura.nm_nodo IS 'Nome del nodo';
COMMENT ON COLUMN PROFILI_OWN.nodo_struttura.ds_nodo IS 'Descrizione del nodo';

CREATE TABLE PROFILI_OWN.visibilita (
  id_visibilita  NUMBER(5)
                 DEFAULT PROFILI_OWN.visibilita_id_visibilita_seq.NEXTVAL NOT NULL,
  nm_tabella     VARCHAR2(256 CHAR),
  nm_colonna     VARCHAR2(100 CHAR)  NOT NULL,
  ds_valore      VARCHAR2(1000 CHAR) NOT NULL,
  ds_visibilita  VARCHAR2(1000 CHAR) NOT NULL,
  ds_breve       VARCHAR2(50 CHAR)   NOT NULL,
  dipendenza     NUMBER(5),
  CONSTRAINT PK_VISIBILITA PRIMARY KEY (id_visibilita),   -- (visibilita_pk)
  CONSTRAINT FK_VISIBILITA_DIPENDENZA FOREIGN KEY (dipendenza)
    REFERENCES PROFILI_OWN.visibilita (id_visibilita)   -- (visibilita_dipendenza_fk)
) TABLESPACE TS_PROFILI;
-- così nello schema: non descrive la tabella
COMMENT ON TABLE PROFILI_OWN.visibilita IS 'Profili associati ad un utente';
COMMENT ON COLUMN PROFILI_OWN.visibilita.id_visibilita IS 'Identificativo visibilita';
COMMENT ON COLUMN PROFILI_OWN.visibilita.nm_tabella IS 'Nome tabella';
COMMENT ON COLUMN PROFILI_OWN.visibilita.nm_colonna IS 'Nome colonna';
COMMENT ON COLUMN PROFILI_OWN.visibilita.ds_valore IS 'Valore';
COMMENT ON COLUMN PROFILI_OWN.visibilita.ds_visibilita IS 'Descrizione visibilita';
COMMENT ON COLUMN PROFILI_OWN.visibilita.ds_breve IS 'Descrizione visibilita breve';
COMMENT ON COLUMN PROFILI_OWN.visibilita.dipendenza IS
  'Riferimento ad una riga di visibilità per esprimere una dipendenza';

CREATE TABLE PROFILI_OWN.nodo_per_visibilita (
  id_nodo        NUMBER(10) NOT NULL,
  id_visibilita  NUMBER(5)  NOT NULL,
  -- (ufficio_per_visibilita_pk)
  CONSTRAINT PK_NODO_PER_VISIBILITA PRIMARY KEY (id_nodo, id_visibilita),
  CONSTRAINT FK_NPV_NODO FOREIGN KEY (id_nodo)
    REFERENCES PROFILI_OWN.nodo_struttura (id_nodo),   -- (nodo_per_visibilita_fk)
  CONSTRAINT FK_NPV_VISIBILITA FOREIGN KEY (id_visibilita)
    REFERENCES PROFILI_OWN.visibilita (id_visibilita)   -- (visibilita_per_nodo_fk)
) TABLESPACE TS_PROFILI;
-- così nello schema: non descrive la tabella
COMMENT ON TABLE PROFILI_OWN.nodo_per_visibilita IS 'Profili associati ad un utente';
COMMENT ON COLUMN PROFILI_OWN.nodo_per_visibilita.id_nodo IS
  'Identificativo nodo struttura';
COMMENT ON COLUMN PROFILI_OWN.nodo_per_visibilita.id_visibilita IS
  'Identificativo visibilita';

CREATE TABLE PROFILI_OWN.v_str_organizzativa (
  codice               VARCHAR2(25 CHAR)  NOT NULL,
  descrizione          VARCHAR2(255 CHAR),
  descrizione_breve    VARCHAR2(255 CHAR),
  codice_str_padre     VARCHAR2(25 CHAR),
  ordine_organigramma  VARCHAR2(50 CHAR),
  codice_responsabile  NUMBER(16),
  CONSTRAINT PK_V_STR_ORGANIZZATIVA PRIMARY KEY (codice)   -- (pk_v_str_organizzativa)
) TABLESPACE TS_PROFILI;

CREATE TABLE PROFILI_OWN.utente (
  id_utente           NUMBER(19)
                      DEFAULT PROFILI_OWN.utente_id_utente_seq.NEXTVAL NOT NULL,
  ds_username         VARCHAR2(50 CHAR)  NOT NULL,
  ds_password         VARCHAR2(100 CHAR),
  ds_nome             VARCHAR2(60 CHAR)  NOT NULL,
  ds_cognome          VARCHAR2(60 CHAR)  NOT NULL,
  cd_fiscale          CHAR(16)           NOT NULL,
  nm_telefono         VARCHAR2(20 CHAR),
  ds_email            VARCHAR2(255 CHAR),
  ds_ufficio          VARCHAR2(255 CHAR),
  dt_ultimo_login     DATE,
  fg_attivo_sn        CHAR(1)            NOT NULL,
  nm_tentativi_pin    NUMBER(5)          DEFAULT 0 NOT NULL,
  nm_tentativi_login  NUMBER(5)          DEFAULT 0 NOT NULL,
  fg_scad_account     CHAR(1)            DEFAULT 'N' NOT NULL,
  fg_scad_password    CHAR(1)            DEFAULT 'N' NOT NULL,
  fg_cambio_password  CHAR(1)            DEFAULT 'N' NOT NULL,
  ts_agg_password     TIMESTAMP,
  cd_cnt              NUMBER(5),
  cd_stato            CHAR(1),
  ty_utente           CHAR(1),
  id_ente             NUMBER(5),
  ds_user_ins_dt      VARCHAR2(50 CHAR)  NOT NULL,
  ts_ins_dt           TIMESTAMP,
  ds_user_ult_agg_dt  VARCHAR2(50 CHAR),
  ts_ult_agg_dt       TIMESTAMP,
  ds_note_dt          VARCHAR2(50 CHAR),
  CONSTRAINT PK_UTENTE PRIMARY KEY (id_utente),   -- (utente_pk)
  CONSTRAINT UK_UTENTE_USERNAME UNIQUE (ds_username),   -- (utente_username_idx2)
  CONSTRAINT UK_UTENTE_CF UNIQUE (cd_fiscale),   -- (utente_cdfiscale_idx3, indice univoco)
  CONSTRAINT FK_UTENTE_ENTE FOREIGN KEY (id_ente)
    REFERENCES PROFILI_OWN.ente (id_ente)   -- (utente_per_ente_fk)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.utente IS 'Utente dell''applicazione';
COMMENT ON COLUMN PROFILI_OWN.utente.id_utente IS 'Identificativo dell''utente';
COMMENT ON COLUMN PROFILI_OWN.utente.ds_username IS 'Username';
COMMENT ON COLUMN PROFILI_OWN.utente.ds_password IS 'password';
COMMENT ON COLUMN PROFILI_OWN.utente.ds_nome IS 'Nome utente';
COMMENT ON COLUMN PROFILI_OWN.utente.ds_cognome IS 'Cognome utente';
COMMENT ON COLUMN PROFILI_OWN.utente.cd_fiscale IS 'Codice fiscale';
COMMENT ON COLUMN PROFILI_OWN.utente.nm_telefono IS 'Numero di telefono utente';
COMMENT ON COLUMN PROFILI_OWN.utente.ds_email IS 'Email istituzionale dell''utente';
COMMENT ON COLUMN PROFILI_OWN.utente.ds_ufficio IS 'Ufficio d''appartenenza utente';
COMMENT ON COLUMN PROFILI_OWN.utente.dt_ultimo_login IS
  'Data ultimo login effettuato dall''utente';
COMMENT ON COLUMN PROFILI_OWN.utente.fg_attivo_sn IS 'Flag utente attivo S/N';
COMMENT ON COLUMN PROFILI_OWN.utente.nm_tentativi_pin IS
  'Numero tentativi PIN - usi futuri';
COMMENT ON COLUMN PROFILI_OWN.utente.nm_tentativi_login IS
  'Numero tentativi di login errati';
COMMENT ON COLUMN PROFILI_OWN.utente.fg_scad_account IS 'Scadenza account S/N';
COMMENT ON COLUMN PROFILI_OWN.utente.fg_scad_password IS 'Scadenza password S/N';
COMMENT ON COLUMN PROFILI_OWN.utente.fg_cambio_password IS
  'Scadenza password S/N';   -- così nello schema: è il commento della colonna precedente
COMMENT ON COLUMN PROFILI_OWN.utente.ts_agg_password IS
  'Timestamp ultimo aggiornamento password';
COMMENT ON COLUMN PROFILI_OWN.utente.cd_cnt IS
  'Codice contatore - usato da tributi - valori previsti NULL e 0';
COMMENT ON COLUMN PROFILI_OWN.utente.cd_stato IS
  'Codice stato - usato da tributi - valori previsti NULL A e B';
COMMENT ON COLUMN PROFILI_OWN.utente.ty_utente IS
  'Tipo utente - usato da tributi - valori previsti NULL e F';
COMMENT ON COLUMN PROFILI_OWN.utente.id_ente IS 'Identificativo ente di appartenenza';
COMMENT ON COLUMN PROFILI_OWN.utente.ds_user_ins_dt IS 'Utente che ha inserito la riga';
COMMENT ON COLUMN PROFILI_OWN.utente.ts_ins_dt IS 'Timestamp inserimento';
COMMENT ON COLUMN PROFILI_OWN.utente.ds_user_ult_agg_dt IS
  'Utente che per ultimo ha aggiornato la riga';
COMMENT ON COLUMN PROFILI_OWN.utente.ts_ult_agg_dt IS 'Timestamp ultimo aggiornamento';
COMMENT ON COLUMN PROFILI_OWN.utente.ds_note_dt IS
  'Descrizione contesto ultimo aggiornamento';

CREATE TABLE PROFILI_OWN.utente_per_profilo (
  id_utente           NUMBER(19)        NOT NULL,
  id_profilo          NUMBER(19)        NOT NULL,
  id_nodo             NUMBER(10),
  ds_user_ins_dt      VARCHAR2(50 CHAR) NOT NULL,
  ts_ins_dt           TIMESTAMP,
  ds_user_ult_agg_dt  VARCHAR2(50 CHAR),
  ts_ult_agg_dt       TIMESTAMP,
  ds_note_dt          VARCHAR2(50 CHAR),
  -- (utente_per_profilo_pk)
  CONSTRAINT PK_UTENTE_PER_PROFILO PRIMARY KEY (id_utente, id_profilo),
  CONSTRAINT FK_UPP_PROFILO FOREIGN KEY (id_profilo)
    REFERENCES PROFILI_OWN.profilo (id_profilo),   -- (profilo_per_utente_fk)
  CONSTRAINT FK_UPP_NODO FOREIGN KEY (id_nodo)
    REFERENCES PROFILI_OWN.nodo_struttura (id_nodo),   -- (profilo_utente_nodo_fk)
  CONSTRAINT FK_UPP_UTENTE FOREIGN KEY (id_utente)
    REFERENCES PROFILI_OWN.utente (id_utente)   -- (utente_per_profilo_fk)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.utente_per_profilo IS
  'Applicazione sulla quale è abilitato l''utente con relativo profilo';
COMMENT ON COLUMN PROFILI_OWN.utente_per_profilo.id_utente IS 'Identificativo dell''utente';
COMMENT ON COLUMN PROFILI_OWN.utente_per_profilo.id_profilo IS 'Identificativo del profilo';
COMMENT ON COLUMN PROFILI_OWN.utente_per_profilo.id_nodo IS
  'Identificativo del nodo struttura - serve a tributi';
COMMENT ON COLUMN PROFILI_OWN.utente_per_profilo.ds_user_ins_dt IS
  'Utente che ha inserito la riga';
COMMENT ON COLUMN PROFILI_OWN.utente_per_profilo.ts_ins_dt IS 'Timestamp inserimento';
COMMENT ON COLUMN PROFILI_OWN.utente_per_profilo.ds_user_ult_agg_dt IS
  'Utente che per ultimo ha aggiornato la riga';
COMMENT ON COLUMN PROFILI_OWN.utente_per_profilo.ts_ult_agg_dt IS
  'Timestamp ultimo aggiornamento';
COMMENT ON COLUMN PROFILI_OWN.utente_per_profilo.ds_note_dt IS
  'Descrizione contesto ultimo aggiornamento';

CREATE TABLE PROFILI_OWN.applicazione (
  cd_ambito              CHAR(2)            NOT NULL,
  cd_applicazione        VARCHAR2(15 CHAR)  NOT NULL,
  ds_applicazione        VARCHAR2(60 CHAR)  NOT NULL,
  ds_endpoint            VARCHAR2(150 CHAR),
  ds_context_root        VARCHAR2(125 CHAR),
  cd_cloud               CHAR(1)            DEFAULT '1' NOT NULL,
  ds_service             VARCHAR2(50 CHAR),
  ds_label               VARCHAR2(30 CHAR),
  nm_ordine              NUMBER(10),
  id_applicazione_sa     NUMBER(10),
  cd_ambito_padre        CHAR(2),
  cd_applicazione_padre  VARCHAR2(15 CHAR),
  ty_login               CHAR(1),
  ty_auth                CHAR(1),
  fg_anonymous           CHAR(1),
  fg_lista_strutture     CHAR(1),
  cd_doc_manuale         VARCHAR2(36 CHAR),
  -- (applicazione_pk)
  CONSTRAINT PK_APPLICAZIONE PRIMARY KEY (cd_ambito, cd_applicazione),
  CONSTRAINT UK_APPLICAZIONE_SA UNIQUE (id_applicazione_sa),   -- (id_applicazione_sa_uk)
  -- (applicazione_padre_fk)
  CONSTRAINT FK_APPLICAZIONE_PADRE FOREIGN KEY (cd_ambito_padre, cd_applicazione_padre)
    REFERENCES PROFILI_OWN.applicazione (cd_ambito, cd_applicazione),
  CONSTRAINT FK_APPLICAZIONE_AMBITO FOREIGN KEY (cd_ambito)
    REFERENCES PROFILI_OWN.ambito (cd_ambito)   -- (applicazione_per_ambito_fk)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.applicazione IS 'Applicazione';
COMMENT ON COLUMN PROFILI_OWN.applicazione.cd_ambito IS 'Codice ambito';
COMMENT ON COLUMN PROFILI_OWN.applicazione.cd_applicazione IS 'Codice applicazione';
COMMENT ON COLUMN PROFILI_OWN.applicazione.ds_applicazione IS 'Descrizione applicazione';
COMMENT ON COLUMN PROFILI_OWN.applicazione.ds_endpoint IS 'Endpoint del microservizio';
COMMENT ON COLUMN PROFILI_OWN.applicazione.ds_context_root IS
  'Context root del microservizio';
COMMENT ON COLUMN PROFILI_OWN.applicazione.cd_cloud IS
  'Codice Cloud: "1": ecaas mirantis, "2": rancher on-premise, "3": cloud PSN';
COMMENT ON COLUMN PROFILI_OWN.applicazione.ds_service IS
  'Nome del servizio - usato da tributi';
COMMENT ON COLUMN PROFILI_OWN.applicazione.ds_label IS
  'Label dell''applicazione - usato da tributi';
COMMENT ON COLUMN PROFILI_OWN.applicazione.nm_ordine IS
  'Numero ordine di apparizione in un elenco - usato da tributi';
COMMENT ON COLUMN PROFILI_OWN.applicazione.id_applicazione_sa IS
  'id applicazione come Sistema d''area';
COMMENT ON COLUMN PROFILI_OWN.applicazione.cd_ambito_padre IS
  'Codice ambito dell''applicazione di riferimento (max 2 livelli)';
COMMENT ON COLUMN PROFILI_OWN.applicazione.cd_applicazione_padre IS
  'Codice applicazione di riferimento (max 2 livelli)';
COMMENT ON COLUMN PROFILI_OWN.applicazione.ty_login IS 'Tipo di login: I=IAM, D=Database';
COMMENT ON COLUMN PROFILI_OWN.applicazione.ty_auth IS
  'Tipo di autorizzazione: G=Gruppo Applicazioni, P=Singolo profilo';
COMMENT ON COLUMN PROFILI_OWN.applicazione.fg_anonymous IS
  'Indicatore che dice se l''applicazione prevede il login anonimo S=SI, N=NO';
COMMENT ON COLUMN PROFILI_OWN.applicazione.fg_lista_strutture IS
  'Indicatore che dice se l''applicazione prevede il login con la lista delle strutture S=SI, N=NO';

CREATE TABLE PROFILI_OWN.configurazione (
  cd_ambito           CHAR(2)            NOT NULL,
  cd_applicazione     VARCHAR2(15 CHAR)  NOT NULL,
  des_nome_parametro  VARCHAR2(100 CHAR) NOT NULL,
  des_val_parametro   CLOB,
  ty_parametro        CHAR(1),
  -- (configurazione_pk)
  CONSTRAINT PK_CONFIGURAZIONE PRIMARY KEY (cd_ambito, cd_applicazione, des_nome_parametro),
  -- (configurazione_per_applicazione_fk)
  CONSTRAINT FK_CONFIGURAZIONE_APPLICAZ FOREIGN KEY (cd_ambito, cd_applicazione)
    REFERENCES PROFILI_OWN.applicazione (cd_ambito, cd_applicazione)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.configurazione IS 'Parametri di configurazione';
COMMENT ON COLUMN PROFILI_OWN.configurazione.cd_ambito IS 'Codice ambito';
COMMENT ON COLUMN PROFILI_OWN.configurazione.cd_applicazione IS 'Codice applicazione';
COMMENT ON COLUMN PROFILI_OWN.configurazione.des_nome_parametro IS 'Nome del parametro';
COMMENT ON COLUMN PROFILI_OWN.configurazione.des_val_parametro IS 'Valore del parametro';
COMMENT ON COLUMN PROFILI_OWN.configurazione.ty_parametro IS
  'Tipo parametro: "S"=String, "I"=Integer, "B"=Boolean';

CREATE TABLE PROFILI_OWN.avviso (
  id_avviso           NUMBER(19)
                      DEFAULT PROFILI_OWN.avvisi_id_avviso_seq.NEXTVAL NOT NULL,
  cd_ambito           CHAR(2)            NOT NULL,
  cd_applicazione     VARCHAR2(15 CHAR)  NOT NULL,
  ds_titolo_avviso    VARCHAR2(100 CHAR) NOT NULL,
  ds_avviso           CLOB               NOT NULL,
  dt_inizio           TIMESTAMP          NOT NULL,
  dt_fine             TIMESTAMP          NOT NULL,
  nm_priorita         NUMBER(5)          DEFAULT 2 NOT NULL,
  ds_user_ins_dt      VARCHAR2(50 CHAR)  NOT NULL,
  ts_ins_dt           TIMESTAMP,
  ds_user_ult_agg_dt  VARCHAR2(50 CHAR),
  ts_ult_agg_dt       TIMESTAMP,
  ds_note_dt          VARCHAR2(50 CHAR),
  fl_attivo           NUMBER(1)          DEFAULT 1 NOT NULL,
  CONSTRAINT PK_AVVISO PRIMARY KEY (id_avviso),   -- (avvisi_pk)
  -- (avvisi_per_applicazione_fk)
  CONSTRAINT FK_AVVISO_APPLICAZIONE FOREIGN KEY (cd_ambito, cd_applicazione)
    REFERENCES PROFILI_OWN.applicazione (cd_ambito, cd_applicazione),
  CONSTRAINT CK_AVVISO_FL_ATTIVO CHECK (fl_attivo IN (0,1))   -- booleano
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.avviso IS 'Avvisi agli utenti';
COMMENT ON COLUMN PROFILI_OWN.avviso.id_avviso IS
  'Identificativo univoco dell''avviso, autoincrementale';
COMMENT ON COLUMN PROFILI_OWN.avviso.cd_ambito IS 'Codice ambito';
COMMENT ON COLUMN PROFILI_OWN.avviso.cd_applicazione IS 'Codice applicazione';
COMMENT ON COLUMN PROFILI_OWN.avviso.ds_titolo_avviso IS 'Titolo dell''avviso';
COMMENT ON COLUMN PROFILI_OWN.avviso.ds_avviso IS 'Testo dell''avviso';
COMMENT ON COLUMN PROFILI_OWN.avviso.dt_inizio IS
  'Timestamp a partire dal quale l''avviso sarà pubblicato';
COMMENT ON COLUMN PROFILI_OWN.avviso.dt_fine IS
  'Timestamp a partire dal quale l''avviso non sarà più visualizzato';
COMMENT ON COLUMN PROFILI_OWN.avviso.nm_priorita IS
  'Priorità 0=Critica,1=alta,2=media,3=bassa';
COMMENT ON COLUMN PROFILI_OWN.avviso.ds_user_ins_dt IS 'Utente che ha inserito la riga';
COMMENT ON COLUMN PROFILI_OWN.avviso.ts_ins_dt IS 'Timestamp inserimento';
COMMENT ON COLUMN PROFILI_OWN.avviso.ds_user_ult_agg_dt IS
  'Utente che per ultimo ha aggiornato la riga';
COMMENT ON COLUMN PROFILI_OWN.avviso.ts_ult_agg_dt IS 'Timestamp ultimo aggiornamento';
COMMENT ON COLUMN PROFILI_OWN.avviso.ds_note_dt IS
  'Descrizione contesto ultimo aggiornamento';

CREATE TABLE PROFILI_OWN.utente_per_profilo_get (
  id_utente             NUMBER(19)        NOT NULL,
  id_profilo            NUMBER(19)        NOT NULL,
  codice_struttura_ged  VARCHAR2(25 CHAR) NOT NULL,
  ds_user_ins_dt        VARCHAR2(50 CHAR),
  ts_ins_dt             TIMESTAMP,
  ds_user_ult_agg_dt    VARCHAR2(50 CHAR),
  ts_ult_agg_dt         TIMESTAMP,
  ds_note_dt            VARCHAR2(50 CHAR),
  -- (pk_upg)
  CONSTRAINT PK_UTENTE_PER_PROFILO_GET PRIMARY KEY (id_utente, id_profilo,
                                                    codice_struttura_ged),
  CONSTRAINT FK_UPPG_PROFILO FOREIGN KEY (id_profilo)
    REFERENCES PROFILI_OWN.profilo (id_profilo),   -- (fk_profilo)
  CONSTRAINT FK_UPPG_STRUTTURA_GED FOREIGN KEY (codice_struttura_ged)
    REFERENCES PROFILI_OWN.v_str_organizzativa (codice),   -- (fk_upg_struttura_ged)
  CONSTRAINT FK_UPPG_UTENTE FOREIGN KEY (id_utente)
    REFERENCES PROFILI_OWN.utente (id_utente)   -- (fk_utente)
) TABLESPACE TS_PROFILI;

CREATE TABLE PROFILI_OWN.applicazione_padre (
  cd_ambito_figlio        CHAR(2)           NOT NULL,
  cd_applicazione_figlio  VARCHAR2(15 CHAR) NOT NULL,
  cd_ambito_padre         CHAR(2)           NOT NULL,
  cd_applicazione_padre   VARCHAR2(15 CHAR) NOT NULL,
  ds_user_ins_dt          VARCHAR2(50 CHAR) NOT NULL,
  ts_ins_dt               TIMESTAMP,
  ds_user_ult_agg_dt      VARCHAR2(50 CHAR),
  ts_ult_agg_dt           TIMESTAMP,
  ds_note_dt              VARCHAR2(50 CHAR),
  -- (pk_applicazione_padre)
  CONSTRAINT PK_APPLICAZIONE_PADRE PRIMARY KEY (cd_ambito_figlio, cd_applicazione_figlio,
                                                cd_ambito_padre, cd_applicazione_padre),
  -- (fk_appadre_figlio)
  CONSTRAINT FK_APPADRE_FIGLIO FOREIGN KEY (cd_ambito_figlio, cd_applicazione_figlio)
    REFERENCES PROFILI_OWN.applicazione (cd_ambito, cd_applicazione),
  CONSTRAINT FK_APPADRE_PADRE FOREIGN KEY (cd_ambito_padre, cd_applicazione_padre)
    REFERENCES PROFILI_OWN.applicazione (cd_ambito, cd_applicazione)   -- (fk_appadre_padre)
) TABLESPACE TS_PROFILI;

CREATE TABLE PROFILI_OWN.utente_profilo_per_applicazione (
  id_utente           NUMBER(19)        NOT NULL,
  id_profilo          NUMBER(19)        NOT NULL,
  cd_ambito           CHAR(2)           NOT NULL,
  cd_applicazione     VARCHAR2(15 CHAR) NOT NULL,
  ds_user_ins_dt      VARCHAR2(50 CHAR) NOT NULL,
  ts_ins_dt           TIMESTAMP,
  ds_user_ult_agg_dt  VARCHAR2(50 CHAR),
  ts_ult_agg_dt       TIMESTAMP,
  ds_note_dt          VARCHAR2(50 CHAR),
  -- (utente_profilo_per_applicazione_pk)
  CONSTRAINT PK_UPPA PRIMARY KEY (id_utente, id_profilo, cd_ambito, cd_applicazione),
  CONSTRAINT FK_UPPA_APPLICAZIONE FOREIGN KEY (cd_ambito, cd_applicazione)
    REFERENCES PROFILI_OWN.applicazione (cd_ambito, cd_applicazione),   -- (applicazione_fk)
  -- (utente_per_profilo_fk)
  CONSTRAINT FK_UPPA_UPP FOREIGN KEY (id_utente, id_profilo)
    REFERENCES PROFILI_OWN.utente_per_profilo (id_utente, id_profilo)
) TABLESPACE TS_PROFILI;
COMMENT ON COLUMN PROFILI_OWN.utente_profilo_per_applicazione.id_utente IS
  'Identificativo dell''utente';
COMMENT ON COLUMN PROFILI_OWN.utente_profilo_per_applicazione.id_profilo IS
  'Identificativo del profilo';
COMMENT ON COLUMN PROFILI_OWN.utente_profilo_per_applicazione.cd_ambito IS 'Codice ambito';
COMMENT ON COLUMN PROFILI_OWN.utente_profilo_per_applicazione.cd_applicazione IS
  'Codice applicazione';
COMMENT ON COLUMN PROFILI_OWN.utente_profilo_per_applicazione.ds_user_ins_dt IS
  'Utente che ha inserito la riga';
COMMENT ON COLUMN PROFILI_OWN.utente_profilo_per_applicazione.ts_ins_dt IS
  'Timestamp inserimento';
COMMENT ON COLUMN PROFILI_OWN.utente_profilo_per_applicazione.ds_user_ult_agg_dt IS
  'Utente che per ultimo ha aggiornato la riga';
COMMENT ON COLUMN PROFILI_OWN.utente_profilo_per_applicazione.ts_ult_agg_dt IS
  'Timestamp ultimo aggiornamento';
COMMENT ON COLUMN PROFILI_OWN.utente_profilo_per_applicazione.ds_note_dt IS
  'Descrizione contesto ultimo aggiornamento';

CREATE TABLE PROFILI_OWN.abilitazione (
  id_abilitazione     NUMBER(19)
                      DEFAULT PROFILI_OWN.abilitazione_id_abilitazione_seq.NEXTVAL NOT NULL,
  cd_ambito           CHAR(2)            NOT NULL,
  cd_applicazione     VARCHAR2(15 CHAR)  NOT NULL,
  cd_abilitazione     VARCHAR2(100 CHAR) NOT NULL,
  ds_abilitazione     VARCHAR2(100 CHAR) NOT NULL,
  id_menu             NUMBER(10),
  cd_esterno          VARCHAR2(100 CHAR),
  link                VARCHAR2(200 CHAR),
  ordine              NUMBER,
  ds_user_ins_dt      VARCHAR2(50 CHAR)  NOT NULL,
  ts_ins_dt           TIMESTAMP,
  ds_user_ult_agg_dt  VARCHAR2(50 CHAR),
  ts_ult_agg_dt       TIMESTAMP,
  ds_note_dt          VARCHAR2(50 CHAR),
  CONSTRAINT PK_ABILITAZIONE PRIMARY KEY (id_abilitazione),   -- (abilitazione_pk)
  -- (cd_abilitazione_uk)
  CONSTRAINT UK_ABILITAZIONE_CODICE UNIQUE (cd_ambito, cd_applicazione, cd_abilitazione),
  -- (abilitazione_per_applicazione_fk)
  CONSTRAINT FK_ABILITAZIONE_APPLICAZ FOREIGN KEY (cd_ambito, cd_applicazione)
    REFERENCES PROFILI_OWN.applicazione (cd_ambito, cd_applicazione),
  CONSTRAINT FK_ABILITAZIONE_MENU FOREIGN KEY (id_menu)
    REFERENCES PROFILI_OWN.menu (id_menu)   -- (abilitazione_per_menu_fk)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.abilitazione IS 'Abilitazione previste per area funzionale';
COMMENT ON COLUMN PROFILI_OWN.abilitazione.id_abilitazione IS 'Identificativo abilitazione';
COMMENT ON COLUMN PROFILI_OWN.abilitazione.cd_ambito IS 'Codice ambito';
COMMENT ON COLUMN PROFILI_OWN.abilitazione.cd_applicazione IS 'Codice applicazione';
COMMENT ON COLUMN PROFILI_OWN.abilitazione.cd_abilitazione IS 'Codice abilitazione';
COMMENT ON COLUMN PROFILI_OWN.abilitazione.ds_abilitazione IS 'Descrizione Abilitazione';
COMMENT ON COLUMN PROFILI_OWN.abilitazione.id_menu IS
  'Codice macro funzione - usato su tributi';
COMMENT ON COLUMN PROFILI_OWN.abilitazione.cd_esterno IS
  'Codice esterno - usato su tributi';
COMMENT ON COLUMN PROFILI_OWN.abilitazione.ds_user_ins_dt IS
  'Utente che ha inserito la riga';
COMMENT ON COLUMN PROFILI_OWN.abilitazione.ts_ins_dt IS 'Timestamp inserimento';
COMMENT ON COLUMN PROFILI_OWN.abilitazione.ds_user_ult_agg_dt IS
  'Utente che per ultimo ha aggiornato la riga';
COMMENT ON COLUMN PROFILI_OWN.abilitazione.ts_ult_agg_dt IS
  'Timestamp ultimo aggiornamento';
COMMENT ON COLUMN PROFILI_OWN.abilitazione.ds_note_dt IS
  'Descrizione contesto ultimo aggiornamento';

CREATE TABLE PROFILI_OWN.profilo_per_abilitazione (
  id_profilo          NUMBER(19)        NOT NULL,
  id_abilitazione     NUMBER(19)        NOT NULL,
  ds_user_ins_dt      VARCHAR2(50 CHAR) NOT NULL,
  ts_ins_dt           TIMESTAMP,
  ds_user_ult_agg_dt  VARCHAR2(50 CHAR),
  ts_ult_agg_dt       TIMESTAMP,
  ds_note_dt          VARCHAR2(50 CHAR),
  -- (profilo_per_abilitazione_pk)
  CONSTRAINT PK_PROFILO_PER_ABILITAZIONE PRIMARY KEY (id_profilo, id_abilitazione),
  -- (abilitazione_per_profilo_fk)
  CONSTRAINT FK_PPA_ABILITAZIONE FOREIGN KEY (id_abilitazione)
    REFERENCES PROFILI_OWN.abilitazione (id_abilitazione),
  CONSTRAINT FK_PPA_PROFILO FOREIGN KEY (id_profilo)
    REFERENCES PROFILI_OWN.profilo (id_profilo)   -- (profilo_per_abilitazione_fk)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.profilo_per_abilitazione IS
  'Abilitazioni associate al profilo';
COMMENT ON COLUMN PROFILI_OWN.profilo_per_abilitazione.id_profilo IS
  'Identificativo del profilo';
COMMENT ON COLUMN PROFILI_OWN.profilo_per_abilitazione.id_abilitazione IS
  'Identificativo abilitazione';
COMMENT ON COLUMN PROFILI_OWN.profilo_per_abilitazione.ds_user_ins_dt IS
  'Utente che ha inserito la riga';
COMMENT ON COLUMN PROFILI_OWN.profilo_per_abilitazione.ts_ins_dt IS 'Timestamp inserimento';
COMMENT ON COLUMN PROFILI_OWN.profilo_per_abilitazione.ds_user_ult_agg_dt IS
  'Utente che per ultimo ha aggiornato la riga';
COMMENT ON COLUMN PROFILI_OWN.profilo_per_abilitazione.ts_ult_agg_dt IS
  'Timestamp ultimo aggiornamento';
COMMENT ON COLUMN PROFILI_OWN.profilo_per_abilitazione.ds_note_dt IS
  'Descrizione contesto ultimo aggiornamento';

-- 4. Indici sulle chiavi esterne non coperte da chiave primaria o unicità.
--    Non sono nello schema PostgreSQL: in Oracle una chiave esterna senza indice
--    blocca l’intera tabella figlia quando si cancella o si modifica il padre.
CREATE INDEX PROFILI_OWN.IX_NODO_STRUTTURA
  ON PROFILI_OWN.nodo_struttura (id_struttura) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_VISIBILITA_DIPENDENZA
  ON PROFILI_OWN.visibilita (dipendenza) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_NPV_VISIBILITA
  ON PROFILI_OWN.nodo_per_visibilita (id_visibilita) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_UTENTE_ENTE
  ON PROFILI_OWN.utente (id_ente) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_UPP_PROFILO
  ON PROFILI_OWN.utente_per_profilo (id_profilo) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_UPP_NODO
  ON PROFILI_OWN.utente_per_profilo (id_nodo) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_APPLICAZIONE_PADRE
  ON PROFILI_OWN.applicazione (cd_ambito_padre, cd_applicazione_padre)
    TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_AVVISO_APPLICAZIONE
  ON PROFILI_OWN.avviso (cd_ambito, cd_applicazione) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_UPPG_PROFILO
  ON PROFILI_OWN.utente_per_profilo_get (id_profilo) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_UPPG_STRUTTURA_GED
  ON PROFILI_OWN.utente_per_profilo_get (codice_struttura_ged) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_APPADRE_PADRE
  ON PROFILI_OWN.applicazione_padre (cd_ambito_padre, cd_applicazione_padre)
    TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_UPPA_APPLICAZIONE
  ON PROFILI_OWN.utente_profilo_per_applicazione (cd_ambito, cd_applicazione)
    TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_ABILITAZIONE_MENU
  ON PROFILI_OWN.abilitazione (id_menu) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_PPA_ABILITAZIONE
  ON PROFILI_OWN.profilo_per_abilitazione (id_abilitazione) TABLESPACE TS_PROFILI;

-- 5. Ruoli: scrittura per il servizio, sola lettura per la revisione degli accessi
CREATE ROLE RL_PROFILI_SCRITTURA;
CREATE ROLE RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.profilo
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.profilo TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.ambito
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.ambito TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.ente
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.ente TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.menu
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.menu TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.struttura
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.struttura TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.nodo_struttura
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.nodo_struttura TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.visibilita
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.visibilita TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.nodo_per_visibilita
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.nodo_per_visibilita TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.v_str_organizzativa
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.v_str_organizzativa TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.utente
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.utente TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.utente_per_profilo
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.utente_per_profilo TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.applicazione
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.applicazione TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.configurazione
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.configurazione TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.avviso
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.avviso TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.utente_per_profilo_get
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.utente_per_profilo_get TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.applicazione_padre
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.applicazione_padre TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.utente_profilo_per_applicazione
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.utente_profilo_per_applicazione TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.abilitazione
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.abilitazione TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.profilo_per_abilitazione
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.profilo_per_abilitazione TO RL_PROFILI_LETTURA;
GRANT SELECT ON PROFILI_OWN.abilitazione_id_abilitazione_seq TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.avvisi_id_avviso_seq TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.menu_id_menu_seq TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.nodo_struttura_id_nodo_seq TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.profilo_id_profilo_seq TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.struttura_id_struttura_seq TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.utente_id_utente_seq TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.visibilita_id_visibilita_seq TO RL_PROFILI_SCRITTURA;

-- 6. Utenza applicativa: solo sessione e ruolo, nessun privilegio di sistema.
--    La parola chiave sta nel gestore dei segreti, mai nella configurazione versionata.
CREATE USER PROFILI_APP IDENTIFIED BY "<dal gestore dei segreti>"
  PROFILE <profilo con scadenza e blocco dei tentativi> ACCOUNT UNLOCK;
GRANT CREATE SESSION TO PROFILI_APP;
GRANT RL_PROFILI_SCRITTURA TO PROFILI_APP;
ALTER USER PROFILI_APP DEFAULT ROLE ALL;
-- Le classi non nominano lo schema: con i sinonimi privati il codice non cambia.
CREATE SYNONYM PROFILI_APP.profilo
  FOR PROFILI_OWN.profilo;
CREATE SYNONYM PROFILI_APP.ambito
  FOR PROFILI_OWN.ambito;
CREATE SYNONYM PROFILI_APP.ente
  FOR PROFILI_OWN.ente;
CREATE SYNONYM PROFILI_APP.menu
  FOR PROFILI_OWN.menu;
CREATE SYNONYM PROFILI_APP.struttura
  FOR PROFILI_OWN.struttura;
CREATE SYNONYM PROFILI_APP.nodo_struttura
  FOR PROFILI_OWN.nodo_struttura;
CREATE SYNONYM PROFILI_APP.visibilita
  FOR PROFILI_OWN.visibilita;
CREATE SYNONYM PROFILI_APP.nodo_per_visibilita
  FOR PROFILI_OWN.nodo_per_visibilita;
CREATE SYNONYM PROFILI_APP.v_str_organizzativa
  FOR PROFILI_OWN.v_str_organizzativa;
CREATE SYNONYM PROFILI_APP.utente
  FOR PROFILI_OWN.utente;
CREATE SYNONYM PROFILI_APP.utente_per_profilo
  FOR PROFILI_OWN.utente_per_profilo;
CREATE SYNONYM PROFILI_APP.applicazione
  FOR PROFILI_OWN.applicazione;
CREATE SYNONYM PROFILI_APP.configurazione
  FOR PROFILI_OWN.configurazione;
CREATE SYNONYM PROFILI_APP.avviso
  FOR PROFILI_OWN.avviso;
CREATE SYNONYM PROFILI_APP.utente_per_profilo_get
  FOR PROFILI_OWN.utente_per_profilo_get;
CREATE SYNONYM PROFILI_APP.applicazione_padre
  FOR PROFILI_OWN.applicazione_padre;
CREATE SYNONYM PROFILI_APP.utente_profilo_per_applicazione
  FOR PROFILI_OWN.utente_profilo_per_applicazione;
CREATE SYNONYM PROFILI_APP.abilitazione
  FOR PROFILI_OWN.abilitazione;
CREATE SYNONYM PROFILI_APP.profilo_per_abilitazione
  FOR PROFILI_OWN.profilo_per_abilitazione;
CREATE SYNONYM PROFILI_APP.abilitazione_id_abilitazione_seq
  FOR PROFILI_OWN.abilitazione_id_abilitazione_seq;
CREATE SYNONYM PROFILI_APP.avvisi_id_avviso_seq
  FOR PROFILI_OWN.avvisi_id_avviso_seq;
CREATE SYNONYM PROFILI_APP.menu_id_menu_seq
  FOR PROFILI_OWN.menu_id_menu_seq;
CREATE SYNONYM PROFILI_APP.nodo_struttura_id_nodo_seq
  FOR PROFILI_OWN.nodo_struttura_id_nodo_seq;
CREATE SYNONYM PROFILI_APP.profilo_id_profilo_seq
  FOR PROFILI_OWN.profilo_id_profilo_seq;
CREATE SYNONYM PROFILI_APP.struttura_id_struttura_seq
  FOR PROFILI_OWN.struttura_id_struttura_seq;
CREATE SYNONYM PROFILI_APP.utente_id_utente_seq
  FOR PROFILI_OWN.utente_id_utente_seq;
CREATE SYNONYM PROFILI_APP.visibilita_id_visibilita_seq
  FOR PROFILI_OWN.visibilita_id_visibilita_seq;

-- 7. Tracciamento delle modifiche (Unified Auditing), conservato fuori dal dominio
CREATE AUDIT POLICY POL_PROFILI_MODIFICHE
  ACTIONS INSERT ON PROFILI_OWN.utente,
          UPDATE ON PROFILI_OWN.utente,
          DELETE ON PROFILI_OWN.utente,
          INSERT ON PROFILI_OWN.utente_per_profilo,
          UPDATE ON PROFILI_OWN.utente_per_profilo,
          DELETE ON PROFILI_OWN.utente_per_profilo,
          INSERT ON PROFILI_OWN.utente_profilo_per_applicazione,
          UPDATE ON PROFILI_OWN.utente_profilo_per_applicazione,
          DELETE ON PROFILI_OWN.utente_profilo_per_applicazione,
          INSERT ON PROFILI_OWN.utente_per_profilo_get,
          UPDATE ON PROFILI_OWN.utente_per_profilo_get,
          DELETE ON PROFILI_OWN.utente_per_profilo_get,
          INSERT ON PROFILI_OWN.profilo,
          UPDATE ON PROFILI_OWN.profilo,
          DELETE ON PROFILI_OWN.profilo,
          INSERT ON PROFILI_OWN.profilo_per_abilitazione,
          UPDATE ON PROFILI_OWN.profilo_per_abilitazione,
          DELETE ON PROFILI_OWN.profilo_per_abilitazione,
          INSERT ON PROFILI_OWN.abilitazione,
          UPDATE ON PROFILI_OWN.abilitazione,
          DELETE ON PROFILI_OWN.abilitazione,
          INSERT ON PROFILI_OWN.applicazione,
          UPDATE ON PROFILI_OWN.applicazione,
          DELETE ON PROFILI_OWN.applicazione,
          INSERT ON PROFILI_OWN.applicazione_padre,
          UPDATE ON PROFILI_OWN.applicazione_padre,
          DELETE ON PROFILI_OWN.applicazione_padre;
AUDIT POLICY POL_PROFILI_MODIFICHE;
-- Le modifiche di struttura e di permesso sono rare: si tracciano per tutte le utenze.
CREATE AUDIT POLICY POL_PROFILI_STRUTTURA
  ACTIONS CREATE TABLE, ALTER TABLE, DROP TABLE, CREATE INDEX, DROP INDEX,
          CREATE SEQUENCE, ALTER SEQUENCE, DROP SEQUENCE, CREATE SYNONYM,
          DROP SYNONYM, GRANT, REVOKE, ALTER USER;
AUDIT POLICY POL_PROFILI_STRUTTURA;
