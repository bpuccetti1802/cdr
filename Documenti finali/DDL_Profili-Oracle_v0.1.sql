-- ============================================================================
-- Dominio dei profili: le tabelle di roma-capitale-management su Oracle
-- Ricostruita dalla mappatura JPA del servizio (versione 1.0.20), in attesa delle
-- DDL dello schema PostgreSQL «management» (PI-39). Vincoli marcati «proposta» o
-- «dedotta» non sono dichiarati nel codice. Nomi di proprietario, utenze, ruoli e
-- tablespace sono proposte da concordare (PI-40). Richiede Oracle 18c o successivo.
-- ============================================================================

-- 1. Tablespace cifrato e proprietario senza accesso (eseguito dai DBA)
CREATE TABLESPACE TS_PROFILI DATAFILE SIZE 1G AUTOEXTEND ON NEXT 256M
  ENCRYPTION USING 'AES256' DEFAULT STORAGE (ENCRYPT);   -- richiede TDE [DA VERIFICARE]
CREATE USER PROFILI_OWN NO AUTHENTICATION
  DEFAULT TABLESPACE TS_PROFILI QUOTA UNLIMITED ON TS_PROFILI;

-- 2. Sequenze: nomi e passo come nella mappatura (allocationSize = 1).
--    Nella migrazione START WITH = massimo identificativo esistente + 1.
CREATE SEQUENCE PROFILI_OWN.menu_id_menu_seq
  START WITH 1 INCREMENT BY 1 NOCYCLE;
-- 32 caratteri: serve Oracle 12.2 o successivo
CREATE SEQUENCE PROFILI_OWN.abilitazione_id_abilitazione_seq
  START WITH 1 INCREMENT BY 1 NOCYCLE;
CREATE SEQUENCE PROFILI_OWN.profilo_id_profilo_seq
  START WITH 1 INCREMENT BY 1 NOCYCLE;
CREATE SEQUENCE PROFILI_OWN.ente_id_ente_seq
  START WITH 1 INCREMENT BY 1 NOCYCLE;
CREATE SEQUENCE PROFILI_OWN.utente_id_utente_seq
  START WITH 1 INCREMENT BY 1 NOCYCLE;
CREATE SEQUENCE PROFILI_OWN.struttura_id_struttura_seq
  START WITH 1 INCREMENT BY 1 NOCYCLE;
CREATE SEQUENCE PROFILI_OWN.nodoStruttura_id_nodo_seq
  START WITH 1 INCREMENT BY 1 NOCYCLE;
CREATE SEQUENCE PROFILI_OWN.visibilita_id_visibilita_seq
  START WITH 1 INCREMENT BY 1 NOCYCLE;
CREATE SEQUENCE PROFILI_OWN.avvisi_id_avviso_seq
  START WITH 1 INCREMENT BY 1 NOCYCLE;

-- 3. Tabelle, nell’ordine imposto dalle chiavi esterne

CREATE TABLE PROFILI_OWN.ambito (
  cd_ambito  VARCHAR2(2 CHAR) NOT NULL,
  ds_ambito  VARCHAR2(50 CHAR) NOT NULL,
  CONSTRAINT PK_AMBITO PRIMARY KEY (cd_ambito)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.ambito IS
  'Gli ambiti della piattaforma (per esempio un''area dell''ente).';

CREATE TABLE PROFILI_OWN.applicazione (
  cd_ambito              VARCHAR2(2 CHAR) NOT NULL,
  cd_applicazione        VARCHAR2(10 CHAR) NOT NULL,
  ds_applicazione        VARCHAR2(60 CHAR) NOT NULL,
  ds_endpoint            VARCHAR2(125 CHAR) NOT NULL,
  ds_context_root        VARCHAR2(125 CHAR) NOT NULL,
  cd_doc_manuale         VARCHAR2(36 CHAR),
  cd_cloud               CHAR(1) NOT NULL,
  ds_service             VARCHAR2(50 CHAR) NOT NULL,
  ds_label               VARCHAR2(30 CHAR) NOT NULL,
  nm_ordine              NUMBER(19),
  id_applicazione_sa     NUMBER(19) NOT NULL,
  cd_ambito_padre        VARCHAR2(2 CHAR),
  cd_applicazione_padre  VARCHAR2(10 CHAR),
  ty_login               CHAR(1),
  ty_auth                CHAR(1),
  fg_anonymous           CHAR(1),
  fg_lista_strutture     CHAR(1),
  CONSTRAINT PK_APPLICAZIONE PRIMARY KEY (cd_ambito, cd_applicazione),
  CONSTRAINT UK_APPLICAZIONE_SA UNIQUE (id_applicazione_sa),
  CONSTRAINT FK_APPLICAZIONE_AMBITO FOREIGN KEY (cd_ambito)
    REFERENCES PROFILI_OWN.ambito (cd_ambito),
  CONSTRAINT FK_APPLICAZIONE_PADRE FOREIGN KEY (cd_ambito_padre, cd_applicazione_padre)
    REFERENCES PROFILI_OWN.applicazione (cd_ambito, cd_applicazione),
  CONSTRAINT CK_APPLICAZIONE_TY_AUTH CHECK (ty_auth IN ('G','P'))
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.applicazione IS
  'Le applicazioni, con indirizzo, contesto, cloud e modalità di accesso.';

CREATE TABLE PROFILI_OWN.menu (
  id_menu             NUMBER(19) NOT NULL,
  cd_menu             VARCHAR2(50 CHAR) NOT NULL,
  ds_menu             VARCHAR2(100 CHAR),
  id_applicazione_sa  NUMBER(19),
  CONSTRAINT PK_MENU PRIMARY KEY (id_menu),
  CONSTRAINT FK_MENU_APPLICAZIONE FOREIGN KEY (id_applicazione_sa)
    REFERENCES PROFILI_OWN.applicazione (id_applicazione_sa)   /* dedotta dal nome */
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.menu IS
  'Le voci di menu a cui un''abilitazione può corrispondere.';

CREATE TABLE PROFILI_OWN.abilitazione (
  id_abilitazione  NUMBER(19) NOT NULL,
  cd_ambito        VARCHAR2(2 CHAR) NOT NULL,
  cd_applicazione  VARCHAR2(10 CHAR) NOT NULL,
  cd_abilitazione  VARCHAR2(255 CHAR) NOT NULL,
  ds_abilitazione  VARCHAR2(10 CHAR) NOT NULL,
  cd_esterno       VARCHAR2(100 CHAR),
  id_menu          NUMBER(19),
  CONSTRAINT PK_ABILITAZIONE PRIMARY KEY (id_abilitazione),
  CONSTRAINT UK_ABILITAZIONE_CODICE UNIQUE (cd_ambito, cd_applicazione, cd_abilitazione),   /* proposta */
  CONSTRAINT FK_ABILITAZIONE_APPLICAZ FOREIGN KEY (cd_ambito, cd_applicazione)
    REFERENCES PROFILI_OWN.applicazione (cd_ambito, cd_applicazione),
  CONSTRAINT FK_ABILITAZIONE_MENU FOREIGN KEY (id_menu)
    REFERENCES PROFILI_OWN.menu (id_menu)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.abilitazione IS
  'Il diritto elementare di un''applicazione, citato per codice nel token.';

CREATE TABLE PROFILI_OWN.profilo (
  id_profilo          NUMBER(19) NOT NULL,
  ds_profilo          VARCHAR2(50 CHAR) NOT NULL,
  fg_profilo_default  CHAR(1) NOT NULL,
  cd_ruolo_profilo    VARCHAR2(50 CHAR),
  nm_valore           NUMBER(19),
  cd_ambito           VARCHAR2(2 CHAR),
  cd_applicazione     VARCHAR2(10 CHAR),
  CONSTRAINT PK_PROFILO PRIMARY KEY (id_profilo),
  CONSTRAINT FK_PROFILO_APPLICAZIONE FOREIGN KEY (cd_ambito, cd_applicazione)
    REFERENCES PROFILI_OWN.applicazione (cd_ambito, cd_applicazione)   /* proposta */
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.profilo IS
  'Un insieme di abilitazioni di un''applicazione, con un codice di ruolo.';

CREATE TABLE PROFILI_OWN.profilo_per_abilitazione (
  id_profilo       NUMBER(19) NOT NULL,
  id_abilitazione  NUMBER(19) NOT NULL,
  CONSTRAINT PK_PROFILO_PER_ABILITAZIONE PRIMARY KEY (id_profilo, id_abilitazione),
  CONSTRAINT FK_PPA_PROFILO FOREIGN KEY (id_profilo)
    REFERENCES PROFILI_OWN.profilo (id_profilo),
  CONSTRAINT FK_PPA_ABILITAZIONE FOREIGN KEY (id_abilitazione)
    REFERENCES PROFILI_OWN.abilitazione (id_abilitazione)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.profilo_per_abilitazione IS
  'Quali abilitazioni compongono un profilo.';

CREATE TABLE PROFILI_OWN.ente (
  id_ente  NUMBER(19) NOT NULL,
  cd_ente  NUMBER(19) NOT NULL,
  ds_ente  VARCHAR2(250 CHAR),
  CONSTRAINT PK_ENTE PRIMARY KEY (id_ente)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.ente IS
  'L''ente di appartenenza dell''utente.';

CREATE TABLE PROFILI_OWN.utente (
  id_utente           NUMBER(19) NOT NULL,
  ds_username         VARCHAR2(50 CHAR) NOT NULL,
  ds_password         VARCHAR2(260 CHAR) NOT NULL,
  ds_nome             VARCHAR2(60 CHAR) NOT NULL,
  ds_cognome          VARCHAR2(60 CHAR) NOT NULL,
  cd_fiscale          VARCHAR2(16 CHAR) NOT NULL,
  nm_telefono         VARCHAR2(20 CHAR) NOT NULL,
  ds_email            VARCHAR2(255 CHAR) NOT NULL,
  ds_ufficio          VARCHAR2(255 CHAR) NOT NULL,
  dt_ultimo_login     TIMESTAMP,
  fg_attivo_sn        CHAR(1) NOT NULL,
  nm_tentativi_pin    NUMBER(19),
  nm_tentativi_login  NUMBER(19),
  fg_scad_account     CHAR(1),
  fg_scad_password    CHAR(1),
  fg_cambio_password  CHAR(1),
  ts_agg_password     TIMESTAMP,
  cd_cnt              NUMBER(19),
  cd_stato            CHAR(1),
  ty_utente           CHAR(1),
  id_ente             NUMBER(19),
  CONSTRAINT PK_UTENTE PRIMARY KEY (id_utente),
  CONSTRAINT UK_UTENTE_USERNAME UNIQUE (ds_username),   /* proposta */
  CONSTRAINT UK_UTENTE_CF UNIQUE (cd_fiscale),   /* proposta */
  CONSTRAINT FK_UTENTE_ENTE FOREIGN KEY (id_ente)
    REFERENCES PROFILI_OWN.ente (id_ente),
  CONSTRAINT CK_UTENTE_ATTIVO CHECK (fg_attivo_sn IN ('S','N'))
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.utente IS
  'Gli utenti della piattaforma, con i dati di contatto e lo stato dell''utenza.';

CREATE TABLE PROFILI_OWN.struttura (
  id_struttura  NUMBER(19) NOT NULL,
  nm_struttura  VARCHAR2(200 CHAR) NOT NULL,
  ds_struttura  VARCHAR2(1000 CHAR) NOT NULL,
  CONSTRAINT PK_STRUTTURA PRIMARY KEY (id_struttura)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.struttura IS
  'Gli alberi organizzativi.';

CREATE TABLE PROFILI_OWN.nodo_struttura (
  id_nodo        NUMBER(19) NOT NULL,
  id_struttura   NUMBER(19) NOT NULL,
  id_nodo_padre  NUMBER(19),
  cd_nodo        VARCHAR2(50 CHAR) NOT NULL,
  nm_nodo        VARCHAR2(200 CHAR) NOT NULL,
  ds_nodo        VARCHAR2(1000 CHAR),
  CONSTRAINT PK_NODO_STRUTTURA PRIMARY KEY (id_nodo),
  CONSTRAINT FK_NODO_STRUTTURA FOREIGN KEY (id_struttura)
    REFERENCES PROFILI_OWN.struttura (id_struttura),
  CONSTRAINT FK_NODO_PADRE FOREIGN KEY (id_nodo_padre)
    REFERENCES PROFILI_OWN.nodo_struttura (id_nodo)   /* dedotta dal nome */
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.nodo_struttura IS
  'I nodi di un albero organizzativo.';

CREATE TABLE PROFILI_OWN.visibilita (
  id_visibilita  NUMBER(19) NOT NULL,
  nm_tabella     VARCHAR2(250 CHAR),
  nm_colonna     VARCHAR2(100 CHAR) NOT NULL,
  ds_valore      VARCHAR2(1000 CHAR) NOT NULL,
  ds_visibilita  VARCHAR2(1000 CHAR) NOT NULL,
  ds_breve       VARCHAR2(50 CHAR) NOT NULL,
  dipendenza     NUMBER(19),
  CONSTRAINT PK_VISIBILITA PRIMARY KEY (id_visibilita),
  CONSTRAINT FK_VISIBILITA_DIPENDENZA FOREIGN KEY (dipendenza)
    REFERENCES PROFILI_OWN.visibilita (id_visibilita)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.visibilita IS
  'Le regole di visibilità sui dati: tabella, colonna, valore.';

CREATE TABLE PROFILI_OWN.nodo_per_visibilita (
  id_nodo        NUMBER(19) NOT NULL,
  id_visibilita  NUMBER(19) NOT NULL,
  CONSTRAINT PK_NODO_PER_VISIBILITA PRIMARY KEY (id_nodo, id_visibilita),
  CONSTRAINT FK_NPV_NODO FOREIGN KEY (id_nodo)
    REFERENCES PROFILI_OWN.nodo_struttura (id_nodo),   /* proposta */
  CONSTRAINT FK_NPV_VISIBILITA FOREIGN KEY (id_visibilita)
    REFERENCES PROFILI_OWN.visibilita (id_visibilita)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.nodo_per_visibilita IS
  'Quali regole di visibilità porta un nodo.';

CREATE TABLE PROFILI_OWN.utente_per_profilo (
  id_utente   NUMBER(19) NOT NULL,
  id_profilo  NUMBER(19) NOT NULL,
  id_nodo     NUMBER(19),
  CONSTRAINT PK_UTENTE_PER_PROFILO PRIMARY KEY (id_utente, id_profilo),
  CONSTRAINT FK_UPP_UTENTE FOREIGN KEY (id_utente)
    REFERENCES PROFILI_OWN.utente (id_utente),   /* proposta */
  CONSTRAINT FK_UPP_PROFILO FOREIGN KEY (id_profilo)
    REFERENCES PROFILI_OWN.profilo (id_profilo),
  CONSTRAINT FK_UPP_NODO FOREIGN KEY (id_nodo)
    REFERENCES PROFILI_OWN.nodo_struttura (id_nodo)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.utente_per_profilo IS
  'L''assegnazione di un profilo a un utente, eventualmente su un nodo organizzativo.';

CREATE TABLE PROFILI_OWN.utente_per_profilo_get (
  id_utente             NUMBER(19) NOT NULL,
  id_profilo            NUMBER(19) NOT NULL,
  codice_struttura_ged  VARCHAR2(25 CHAR) NOT NULL,
  CONSTRAINT PK_UTENTE_PER_PROFILO_GET PRIMARY KEY (id_utente, id_profilo, codice_struttura_ged),
  CONSTRAINT FK_UPPG_UTENTE FOREIGN KEY (id_utente)
    REFERENCES PROFILI_OWN.utente (id_utente),   /* proposta */
  CONSTRAINT FK_UPPG_PROFILO FOREIGN KEY (id_profilo)
    REFERENCES PROFILI_OWN.profilo (id_profilo)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.utente_per_profilo_get IS
  'Le assegnazioni legate alle strutture del protocollo, per lo sportello unico.';

CREATE TABLE PROFILI_OWN.configurazione (
  cd_ambito           VARCHAR2(2 CHAR) NOT NULL,
  cd_applicazione     VARCHAR2(10 CHAR) NOT NULL,
  des_nome_parametro  VARCHAR2(100 CHAR) NOT NULL,
  des_val_parametro   CLOB NOT NULL,
  ty_parametro        CHAR(1),
  CONSTRAINT PK_CONFIGURAZIONE PRIMARY KEY (cd_ambito, cd_applicazione, des_nome_parametro),
  CONSTRAINT FK_CONFIGURAZIONE_APPLICAZ FOREIGN KEY (cd_ambito, cd_applicazione)
    REFERENCES PROFILI_OWN.applicazione (cd_ambito, cd_applicazione)
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.configurazione IS
  'La configurazione remota dei servizi, per applicazione.';

CREATE TABLE PROFILI_OWN.avviso (
  id_avviso         NUMBER(19) NOT NULL,
  cd_ambito         VARCHAR2(2 CHAR) NOT NULL,
  cd_applicazione   VARCHAR2(10 CHAR) NOT NULL,
  ds_titolo_avviso  VARCHAR2(100 CHAR) NOT NULL,
  ds_avviso         CLOB NOT NULL,
  dt_inizio         TIMESTAMP NOT NULL,
  dt_fine           TIMESTAMP NOT NULL,
  nm_priorita       NUMBER(5) NOT NULL,
  fl_attivo         NUMBER(1) NOT NULL,
  CONSTRAINT PK_AVVISO PRIMARY KEY (id_avviso),
  CONSTRAINT FK_AVVISO_APPLICAZIONE FOREIGN KEY (cd_ambito, cd_applicazione)
    REFERENCES PROFILI_OWN.applicazione (cd_ambito, cd_applicazione),
  CONSTRAINT CK_AVVISO_ATTIVO CHECK (fl_attivo IN (0,1))
) TABLESPACE TS_PROFILI;
COMMENT ON TABLE PROFILI_OWN.avviso IS
  'Gli avvisi agli utenti, per applicazione.';

-- 4. Indici sulle colonne delle chiavi esterne non coperte dalla chiave primaria
CREATE INDEX PROFILI_OWN.IX_APPLICAZIONE_PADRE
  ON PROFILI_OWN.applicazione (cd_ambito_padre, cd_applicazione_padre) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_MENU_APPLICAZIONE
  ON PROFILI_OWN.menu (id_applicazione_sa) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_ABILITAZIONE_APPLICAZ
  ON PROFILI_OWN.abilitazione (cd_ambito, cd_applicazione) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_ABILITAZIONE_MENU
  ON PROFILI_OWN.abilitazione (id_menu) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_PROFILO_APPLICAZIONE
  ON PROFILI_OWN.profilo (cd_ambito, cd_applicazione) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_PPA_ABILITAZIONE
  ON PROFILI_OWN.profilo_per_abilitazione (id_abilitazione) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_UTENTE_ENTE
  ON PROFILI_OWN.utente (id_ente) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_NODO_STRUTTURA
  ON PROFILI_OWN.nodo_struttura (id_struttura) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_NODO_PADRE
  ON PROFILI_OWN.nodo_struttura (id_nodo_padre) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_VISIBILITA_DIPENDENZA
  ON PROFILI_OWN.visibilita (dipendenza) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_NPV_VISIBILITA
  ON PROFILI_OWN.nodo_per_visibilita (id_visibilita) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_UPP_PROFILO
  ON PROFILI_OWN.utente_per_profilo (id_profilo) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_UPP_NODO
  ON PROFILI_OWN.utente_per_profilo (id_nodo) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_UPPG_PROFILO
  ON PROFILI_OWN.utente_per_profilo_get (id_profilo) TABLESPACE TS_PROFILI;
CREATE INDEX PROFILI_OWN.IX_AVVISO_APPLICAZIONE
  ON PROFILI_OWN.avviso (cd_ambito, cd_applicazione) TABLESPACE TS_PROFILI;

-- 5. La vista dell’organigramma: la definizione non è fra le sorgenti [DA VERIFICARE]
-- CREATE OR REPLACE VIEW PROFILI_OWN.v_str_organizzativa AS
--   SELECT codice, descrizione, descrizione_breve,
--          codice_str_padre, ordine_organigramma, codice_responsabile
--     FROM <origine dell’organigramma del protocollo>;
--   colonne attese:
--     codice               VARCHAR2(25 CHAR)
--     descrizione          VARCHAR2(255 CHAR)
--     descrizione_breve    VARCHAR2(255 CHAR)
--     codice_str_padre     VARCHAR2(25 CHAR)
--     ordine_organigramma  VARCHAR2(50 CHAR)
--     codice_responsabile  NUMBER(19)

-- 6. Ruoli: scrittura per il servizio, sola lettura per la revisione degli accessi
CREATE ROLE RL_PROFILI_SCRITTURA;
CREATE ROLE RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.ambito
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.ambito TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.applicazione
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.applicazione TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.menu
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.menu TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.abilitazione
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.abilitazione TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.profilo
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.profilo TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.profilo_per_abilitazione
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.profilo_per_abilitazione TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.ente
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.ente TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.utente
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.utente TO RL_PROFILI_LETTURA;
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
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.utente_per_profilo
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.utente_per_profilo TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.utente_per_profilo_get
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.utente_per_profilo_get TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.configurazione
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.configurazione TO RL_PROFILI_LETTURA;
GRANT SELECT, INSERT, UPDATE, DELETE ON PROFILI_OWN.avviso
  TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.avviso TO RL_PROFILI_LETTURA;
GRANT SELECT ON PROFILI_OWN.menu_id_menu_seq TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.abilitazione_id_abilitazione_seq TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.profilo_id_profilo_seq TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.ente_id_ente_seq TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.utente_id_utente_seq TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.struttura_id_struttura_seq TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.nodoStruttura_id_nodo_seq TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.visibilita_id_visibilita_seq TO RL_PROFILI_SCRITTURA;
GRANT SELECT ON PROFILI_OWN.avvisi_id_avviso_seq TO RL_PROFILI_SCRITTURA;

-- 7. Utenza applicativa: solo sessione e ruolo, nessun privilegio di sistema.
--    La parola chiave sta nel gestore dei segreti, mai nella configurazione versionata.
CREATE USER PROFILI_APP IDENTIFIED BY "<dal gestore dei segreti>"
  PROFILE <profilo con scadenza e blocco dei tentativi> ACCOUNT UNLOCK;
GRANT CREATE SESSION TO PROFILI_APP;
GRANT RL_PROFILI_SCRITTURA TO PROFILI_APP;
ALTER USER PROFILI_APP DEFAULT ROLE ALL;
-- Le classi non nominano lo schema: con i sinonimi privati il codice non cambia.
CREATE SYNONYM PROFILI_APP.ambito
  FOR PROFILI_OWN.ambito;
CREATE SYNONYM PROFILI_APP.applicazione
  FOR PROFILI_OWN.applicazione;
CREATE SYNONYM PROFILI_APP.menu
  FOR PROFILI_OWN.menu;
CREATE SYNONYM PROFILI_APP.abilitazione
  FOR PROFILI_OWN.abilitazione;
CREATE SYNONYM PROFILI_APP.profilo
  FOR PROFILI_OWN.profilo;
CREATE SYNONYM PROFILI_APP.profilo_per_abilitazione
  FOR PROFILI_OWN.profilo_per_abilitazione;
CREATE SYNONYM PROFILI_APP.ente
  FOR PROFILI_OWN.ente;
CREATE SYNONYM PROFILI_APP.utente
  FOR PROFILI_OWN.utente;
CREATE SYNONYM PROFILI_APP.struttura
  FOR PROFILI_OWN.struttura;
CREATE SYNONYM PROFILI_APP.nodo_struttura
  FOR PROFILI_OWN.nodo_struttura;
CREATE SYNONYM PROFILI_APP.visibilita
  FOR PROFILI_OWN.visibilita;
CREATE SYNONYM PROFILI_APP.nodo_per_visibilita
  FOR PROFILI_OWN.nodo_per_visibilita;
CREATE SYNONYM PROFILI_APP.utente_per_profilo
  FOR PROFILI_OWN.utente_per_profilo;
CREATE SYNONYM PROFILI_APP.utente_per_profilo_get
  FOR PROFILI_OWN.utente_per_profilo_get;
CREATE SYNONYM PROFILI_APP.configurazione
  FOR PROFILI_OWN.configurazione;
CREATE SYNONYM PROFILI_APP.avviso
  FOR PROFILI_OWN.avviso;
CREATE SYNONYM PROFILI_APP.menu_id_menu_seq
  FOR PROFILI_OWN.menu_id_menu_seq;
CREATE SYNONYM PROFILI_APP.abilitazione_id_abilitazione_seq
  FOR PROFILI_OWN.abilitazione_id_abilitazione_seq;
CREATE SYNONYM PROFILI_APP.profilo_id_profilo_seq
  FOR PROFILI_OWN.profilo_id_profilo_seq;
CREATE SYNONYM PROFILI_APP.ente_id_ente_seq
  FOR PROFILI_OWN.ente_id_ente_seq;
CREATE SYNONYM PROFILI_APP.utente_id_utente_seq
  FOR PROFILI_OWN.utente_id_utente_seq;
CREATE SYNONYM PROFILI_APP.struttura_id_struttura_seq
  FOR PROFILI_OWN.struttura_id_struttura_seq;
CREATE SYNONYM PROFILI_APP.nodoStruttura_id_nodo_seq
  FOR PROFILI_OWN.nodoStruttura_id_nodo_seq;
CREATE SYNONYM PROFILI_APP.visibilita_id_visibilita_seq
  FOR PROFILI_OWN.visibilita_id_visibilita_seq;
CREATE SYNONYM PROFILI_APP.avvisi_id_avviso_seq
  FOR PROFILI_OWN.avvisi_id_avviso_seq;

-- 8. Tracciamento delle modifiche (Unified Auditing), conservato fuori dal dominio
CREATE AUDIT POLICY POL_PROFILI_MODIFICHE
  ACTIONS INSERT ON PROFILI_OWN.utente,
          UPDATE ON PROFILI_OWN.utente,
          DELETE ON PROFILI_OWN.utente,
          INSERT ON PROFILI_OWN.utente_per_profilo,
          UPDATE ON PROFILI_OWN.utente_per_profilo,
          DELETE ON PROFILI_OWN.utente_per_profilo,
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
          DELETE ON PROFILI_OWN.applicazione;
AUDIT POLICY POL_PROFILI_MODIFICHE;
-- Le modifiche di struttura e di permesso sono rare: si tracciano per tutte le utenze.
CREATE AUDIT POLICY POL_PROFILI_STRUTTURA
  ACTIONS CREATE TABLE, ALTER TABLE, DROP TABLE, CREATE INDEX, DROP INDEX,
          CREATE SEQUENCE, ALTER SEQUENCE, DROP SEQUENCE, CREATE SYNONYM,
          DROP SYNONYM, GRANT, REVOKE, ALTER USER;
AUDIT POLICY POL_PROFILI_STRUTTURA;
