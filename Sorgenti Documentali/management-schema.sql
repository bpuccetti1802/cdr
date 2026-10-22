-- DROP SCHEMA management;
 
CREATE SCHEMA management AUTHORIZATION management;
 
-- DROP SEQUENCE management.abilitazione_id_abilitazione_seq;
 
CREATE SEQUENCE management.abilitazione_id_abilitazione_seq

	INCREMENT BY 1

	MINVALUE 1

	MAXVALUE 9223372036854775807

	START 1

	CACHE 1

	NO CYCLE;

-- DROP SEQUENCE management.avvisi_id_avviso_seq;
 
CREATE SEQUENCE management.avvisi_id_avviso_seq

	INCREMENT BY 1

	MINVALUE 1

	MAXVALUE 9223372036854775807

	START 1

	CACHE 1

	NO CYCLE;

-- DROP SEQUENCE management.menu_id_menu_seq;
 
CREATE SEQUENCE management.menu_id_menu_seq

	INCREMENT BY 1

	MINVALUE 1

	MAXVALUE 9223372036854775807

	START 175

	CACHE 1

	NO CYCLE;

-- DROP SEQUENCE management.nodo_struttura_id_nodo_seq;
 
CREATE SEQUENCE management.nodo_struttura_id_nodo_seq

	INCREMENT BY 1

	MINVALUE 1

	MAXVALUE 9223372036854775807

	START 1

	CACHE 1

	NO CYCLE;

-- DROP SEQUENCE management.profilo_id_profilo_seq;
 
CREATE SEQUENCE management.profilo_id_profilo_seq

	INCREMENT BY 1

	MINVALUE 1

	MAXVALUE 9223372036854775807

	START 1

	CACHE 1

	NO CYCLE;

-- DROP SEQUENCE management.struttura_id_struttura_seq;
 
CREATE SEQUENCE management.struttura_id_struttura_seq

	INCREMENT BY 1

	MINVALUE 1

	MAXVALUE 9223372036854775807

	START 27

	CACHE 1

	NO CYCLE;

-- DROP SEQUENCE management.utente_id_utente_seq;
 
CREATE SEQUENCE management.utente_id_utente_seq

	INCREMENT BY 1

	MINVALUE 1

	MAXVALUE 9223372036854775807

	START 1

	CACHE 1

	NO CYCLE;

-- DROP SEQUENCE management.visibilita_id_visibilita_seq;
 
CREATE SEQUENCE management.visibilita_id_visibilita_seq

	INCREMENT BY 1

	MINVALUE 1

	MAXVALUE 9223372036854775807

	START 45

	CACHE 1

	NO CYCLE;-- management.ambito definition
 
-- Drop table
 
-- DROP TABLE management.ambito;
 
CREATE TABLE management.ambito ( cd_ambito bpchar(2) NOT NULL, ds_ambito varchar(50) NOT NULL, CONSTRAINT ambito_pk PRIMARY KEY (cd_ambito));

COMMENT ON TABLE management.ambito IS 'Area funzionale';
 
-- Column comments
 
COMMENT ON COLUMN management.ambito.cd_ambito IS 'Codice ambito';

COMMENT ON COLUMN management.ambito.ds_ambito IS 'Descrizione ambito';
 
 
-- management.ente definition
 
-- Drop table
 
-- DROP TABLE management.ente;
 
CREATE TABLE management.ente ( id_ente int4 NOT NULL, cd_ente int4 NOT NULL, ds_ente varchar(250) NULL, CONSTRAINT ente_pk PRIMARY KEY (id_ente));

COMMENT ON TABLE management.ente IS 'Ente';
 
-- Column comments
 
COMMENT ON COLUMN management.ente.id_ente IS 'Identificativo ente';

COMMENT ON COLUMN management.ente.cd_ente IS 'Codice ente';

COMMENT ON COLUMN management.ente.ds_ente IS 'Descrizione ente';
 
 
-- management.marco_vav definition
 
-- Drop table
 
-- DROP TABLE management.marco_vav;
 
CREATE TABLE management.marco_vav ( id_utente int8 NULL, id_profilo int8 NULL, codice_struttura_ged varchar(25) NULL, ds_user_ins_dt varchar(50) NULL, ts_ins_dt timestamp NULL, ds_user_ult_agg_dt varchar(50) NULL, ts_ult_agg_dt timestamp NULL, ds_note_dt varchar(50) NULL);
 
 
-- management.menu definition
 
-- Drop table
 
-- DROP TABLE management.menu;
 
CREATE TABLE management.menu ( id_menu serial4 NOT NULL, cd_menu varchar(50) NOT NULL, ds_menu varchar(100) NULL, id_applicazione_sa int4 NULL, CONSTRAINT menu_pk PRIMARY KEY (id_menu));

COMMENT ON TABLE management.menu IS 'Menu di macro funzioni - usato da tributi';
 
-- Column comments
 
COMMENT ON COLUMN management.menu.id_menu IS 'Identificativo macro funzione';

COMMENT ON COLUMN management.menu.cd_menu IS 'Codice Menu';

COMMENT ON COLUMN management.menu.ds_menu IS 'Descrizione menu';

COMMENT ON COLUMN management.menu.id_applicazione_sa IS 'Identificativo applicazione del sistema d''area';
 
 
-- management.profilo definition
 
-- Drop table
 
-- DROP TABLE management.profilo;
 
CREATE TABLE management.profilo ( id_profilo bigserial NOT NULL, ds_profilo varchar(50) NOT NULL, fg_profilo_default bpchar(1) DEFAULT 'N'::bpchar NOT NULL, cd_ruolo_profilo varchar(50) NULL, nm_valore int4 NULL, cd_ambito bpchar(2) NULL, cd_applicazione varchar(15) NULL, ds_user_ins_dt varchar(50) NOT NULL, ts_ins_dt timestamp NULL, ds_user_ult_agg_dt varchar(50) NULL, ts_ult_agg_dt timestamp NULL, ds_note_dt varchar(50) NULL, cod_pro varchar(50) NULL, area_pro varchar(30) NULL, descr varchar(50) NULL, gruppo varchar(20) NULL, flag_speciale numeric NULL, cd_profilo varchar(50) NULL, CONSTRAINT profilo_pk PRIMARY KEY (id_profilo));

CREATE UNIQUE INDEX cd_profilo_uk ON management.profilo USING btree (cd_profilo);

COMMENT ON TABLE management.profilo IS 'Piano nazionale';
 
-- Column comments
 
COMMENT ON COLUMN management.profilo.id_profilo IS 'Identificativo del profilo';

COMMENT ON COLUMN management.profilo.ds_profilo IS 'Descrizione del profilo';

COMMENT ON COLUMN management.profilo.fg_profilo_default IS 'Profilo di default S/N';

COMMENT ON COLUMN management.profilo.cd_ruolo_profilo IS 'Codice Ruolo associato al profilo - utilizzato da tributi';

COMMENT ON COLUMN management.profilo.nm_valore IS 'Valore associato al profilo - utilizzato da tributi';

COMMENT ON COLUMN management.profilo.cd_ambito IS 'Codice ambito';

COMMENT ON COLUMN management.profilo.cd_applicazione IS 'Codice applicazione';

COMMENT ON COLUMN management.profilo.ds_user_ins_dt IS 'Utente che ha inserito la riga';

COMMENT ON COLUMN management.profilo.ts_ins_dt IS 'Timestamp inserimento';

COMMENT ON COLUMN management.profilo.ds_user_ult_agg_dt IS 'Utente che per ultimo ha aggiornato la riga';

COMMENT ON COLUMN management.profilo.ts_ult_agg_dt IS 'Timestamp ultimo aggiornamento';

COMMENT ON COLUMN management.profilo.ds_note_dt IS 'Descrizione contesto ultimo aggiornamento';
 
 
-- management.struttura definition
 
-- Drop table
 
-- DROP TABLE management.struttura;
 
CREATE TABLE management.struttura ( id_struttura serial4 NOT NULL, nm_struttura varchar(200) NOT NULL, ds_struttura varchar(1000) NOT NULL, CONSTRAINT struttura_pk PRIMARY KEY (id_struttura));

COMMENT ON TABLE management.struttura IS 'Struttura in ambito Roma Capitale';
 
-- Column comments
 
COMMENT ON COLUMN management.struttura.id_struttura IS 'Identificativo struttura';

COMMENT ON COLUMN management.struttura.nm_struttura IS 'nome struttura';

COMMENT ON COLUMN management.struttura.ds_struttura IS 'Descrizione struttura';
 
 
-- management.uten_prof_produzione definition
 
-- Drop table
 
-- DROP TABLE management.uten_prof_produzione;
 
CREATE TABLE management.uten_prof_produzione ( aa varchar(128) NULL);
 
 
-- management.utente_10032026 definition
 
-- Drop table
 
-- DROP TABLE management.utente_10032026;
 
CREATE TABLE management.utente_10032026 ( id_utente int8 NULL, ds_username varchar(50) NULL, ds_password varchar(100) NULL, ds_nome varchar(60) NULL, ds_cognome varchar(60) NULL, cd_fiscale bpchar(16) NULL, nm_telefono varchar(20) NULL, ds_email varchar(255) NULL, ds_ufficio varchar(255) NULL, dt_ultimo_login date NULL, fg_attivo_sn bpchar(1) NULL, nm_tentativi_pin int2 NULL, nm_tentativi_login int2 NULL, fg_scad_account bpchar(1) NULL, fg_scad_password bpchar(1) NULL, fg_cambio_password bpchar(1) NULL, ts_agg_password timestamp NULL, cd_cnt int2 NULL, cd_stato bpchar(1) NULL, ty_utente bpchar(1) NULL, id_ente int2 NULL, ds_user_ins_dt varchar(50) NULL, ts_ins_dt timestamp NULL, ds_user_ult_agg_dt varchar(50) NULL, ts_ult_agg_dt timestamp NULL, ds_note_dt varchar(50) NULL);
 
 
-- management.utente_ante_sostituzione_cf definition
 
-- Drop table
 
-- DROP TABLE management.utente_ante_sostituzione_cf;
 
CREATE TABLE management.utente_ante_sostituzione_cf ( id_utente int8 NULL, ds_username varchar(50) NULL, ds_password varchar(100) NULL, ds_nome varchar(60) NULL, ds_cognome varchar(60) NULL, cd_fiscale bpchar(16) NULL, nm_telefono varchar(20) NULL, ds_email varchar(255) NULL, ds_ufficio varchar(255) NULL, dt_ultimo_login date NULL, fg_attivo_sn bpchar(1) NULL, nm_tentativi_pin int2 NULL, nm_tentativi_login int2 NULL, fg_scad_account bpchar(1) NULL, fg_scad_password bpchar(1) NULL, fg_cambio_password bpchar(1) NULL, ts_agg_password timestamp NULL, cd_cnt int2 NULL, cd_stato bpchar(1) NULL, ty_utente bpchar(1) NULL, id_ente int2 NULL, ds_user_ins_dt varchar(50) NULL, ts_ins_dt timestamp NULL, ds_user_ult_agg_dt varchar(50) NULL, ts_ult_agg_dt timestamp NULL, ds_note_dt varchar(50) NULL);
 
 
-- management.utente_prod definition
 
-- Drop table
 
-- DROP TABLE management.utente_prod;
 
CREATE TABLE management.utente_prod ( id_utente int8 NULL, ds_username varchar(50) NULL, ds_password varchar(100) NULL, ds_nome varchar(60) NULL, ds_cognome varchar(60) NULL, cd_fiscale bpchar(16) NULL, nm_telefono varchar(20) NULL, ds_email varchar(255) NULL, ds_ufficio varchar(255) NULL, dt_ultimo_login date NULL, fg_attivo_sn bpchar(1) NULL, nm_tentativi_pin int2 NULL, nm_tentativi_login int2 NULL, fg_scad_account bpchar(1) NULL, fg_scad_password bpchar(1) NULL, fg_cambio_password bpchar(1) NULL, ts_agg_password timestamp NULL, cd_cnt int2 NULL, cd_stato bpchar(1) NULL, ty_utente bpchar(1) NULL, id_ente int2 NULL, ds_user_ins_dt varchar(50) NULL, ts_ins_dt timestamp NULL, ds_user_ult_agg_dt varchar(50) NULL, ts_ult_agg_dt timestamp NULL, ds_note_dt varchar(50) NULL);
 
 
-- management.v_str_organizzativa definition
 
-- Drop table
 
-- DROP TABLE management.v_str_organizzativa;
 
CREATE TABLE management.v_str_organizzativa ( codice varchar(25) NOT NULL, descrizione varchar(255) NULL, descrizione_breve varchar(255) NULL, codice_str_padre varchar(25) NULL, ordine_organigramma varchar(50) NULL, codice_responsabile numeric(16) NULL, CONSTRAINT pk_v_str_organizzativa PRIMARY KEY (codice));
 
 
-- management.applicazione definition
 
-- Drop table
 
-- DROP TABLE management.applicazione;
 
CREATE TABLE management.applicazione ( cd_ambito bpchar(2) NOT NULL, cd_applicazione varchar(15) NOT NULL, ds_applicazione varchar(60) NOT NULL, ds_endpoint varchar(150) NULL, ds_context_root varchar(125) NULL, cd_cloud bpchar(1) DEFAULT '1'::bpchar NOT NULL, ds_service varchar(50) NULL, ds_label varchar(30) NULL, nm_ordine int4 NULL, id_applicazione_sa int4 NULL, cd_ambito_padre bpchar(2) NULL, cd_applicazione_padre varchar(15) NULL, ty_login bpchar(1) NULL, ty_auth bpchar(1) NULL, fg_anonymous bpchar(1) NULL, fg_lista_strutture bpchar(1) NULL, cd_doc_manuale varchar(36) NULL, CONSTRAINT applicazione_pk PRIMARY KEY (cd_ambito, cd_applicazione), CONSTRAINT id_applicazione_sa_uk UNIQUE (id_applicazione_sa), CONSTRAINT applicazione_padre_fk FOREIGN KEY (cd_ambito_padre,cd_applicazione_padre) REFERENCES management.applicazione(cd_ambito,cd_applicazione), CONSTRAINT applicazione_per_ambito_fk FOREIGN KEY (cd_ambito) REFERENCES management.ambito(cd_ambito));

COMMENT ON TABLE management.applicazione IS 'Applicazione';
 
-- Column comments
 
COMMENT ON COLUMN management.applicazione.cd_ambito IS 'Codice ambito';

COMMENT ON COLUMN management.applicazione.cd_applicazione IS 'Codice applicazione';

COMMENT ON COLUMN management.applicazione.ds_applicazione IS 'Descrizione applicazione';

COMMENT ON COLUMN management.applicazione.ds_endpoint IS 'Endpoint del microservizio';

COMMENT ON COLUMN management.applicazione.ds_context_root IS 'Context root del microservizio';

COMMENT ON COLUMN management.applicazione.cd_cloud IS 'Codice Cloud: "1": ecaas mirantis, "2": rancher on-premise, "3": cloud PSN';

COMMENT ON COLUMN management.applicazione.ds_service IS 'Nome del servizio - usato da tributi';

COMMENT ON COLUMN management.applicazione.ds_label IS 'Label dell''applicazione - usato da tributi';

COMMENT ON COLUMN management.applicazione.nm_ordine IS 'Numero ordine di apparizione in un elenco - usato da tributi';

COMMENT ON COLUMN management.applicazione.id_applicazione_sa IS 'id applicazione come Sistema d''area';

COMMENT ON COLUMN management.applicazione.cd_ambito_padre IS 'Codice ambito dell''applicazione di riferimento (max 2 livelli)';

COMMENT ON COLUMN management.applicazione.cd_applicazione_padre IS 'Codice applicazione di riferimento (max 2 livelli)';

COMMENT ON COLUMN management.applicazione.ty_login IS 'Tipo di login: I=IAM, D=Database';

COMMENT ON COLUMN management.applicazione.ty_auth IS 'Tipo di autorizzazione: G=Gruppo Applicazioni, P=Singolo profilo';

COMMENT ON COLUMN management.applicazione.fg_anonymous IS 'Indicatore che dice se l''applicazione prevede il login anonimo S=SI, N=NO';

COMMENT ON COLUMN management.applicazione.fg_lista_strutture IS 'Indicatore che dice se l''applicazione prevede il login con la lista delle strutture S=SI, N=NO';
 
 
-- management.applicazione_padre definition
 
-- Drop table
 
-- DROP TABLE management.applicazione_padre;
 
CREATE TABLE management.applicazione_padre ( cd_ambito_figlio bpchar(2) NOT NULL, cd_applicazione_figlio varchar(15) NOT NULL, cd_ambito_padre bpchar(2) NOT NULL, cd_applicazione_padre varchar(15) NOT NULL, ds_user_ins_dt varchar(50) NOT NULL, ts_ins_dt timestamp NULL, ds_user_ult_agg_dt varchar(50) NULL, ts_ult_agg_dt timestamp NULL, ds_note_dt varchar(50) NULL, CONSTRAINT pk_applicazione_padre PRIMARY KEY (cd_ambito_figlio, cd_applicazione_figlio, cd_ambito_padre, cd_applicazione_padre), CONSTRAINT fk_appadre_figlio FOREIGN KEY (cd_ambito_figlio,cd_applicazione_figlio) REFERENCES management.applicazione(cd_ambito,cd_applicazione), CONSTRAINT fk_appadre_padre FOREIGN KEY (cd_ambito_padre,cd_applicazione_padre) REFERENCES management.applicazione(cd_ambito,cd_applicazione));
 
 
-- management.avviso definition
 
-- Drop table
 
-- DROP TABLE management.avviso;
 
CREATE TABLE management.avviso ( id_avviso int8 DEFAULT nextval('avvisi_id_avviso_seq'::regclass) NOT NULL, cd_ambito bpchar(2) NOT NULL, cd_applicazione varchar(15) NOT NULL, ds_titolo_avviso varchar(100) NOT NULL, ds_avviso text NOT NULL, dt_inizio timestamp NOT NULL, dt_fine timestamp NOT NULL, nm_priorita int2 DEFAULT 2 NOT NULL, ds_user_ins_dt varchar(50) NOT NULL, ts_ins_dt timestamp NULL, ds_user_ult_agg_dt varchar(50) NULL, ts_ult_agg_dt timestamp NULL, ds_note_dt varchar(50) NULL, fl_attivo bool DEFAULT true NOT NULL, CONSTRAINT avvisi_pk PRIMARY KEY (id_avviso), CONSTRAINT avvisi_per_applicazione_fk FOREIGN KEY (cd_ambito,cd_applicazione) REFERENCES management.applicazione(cd_ambito,cd_applicazione));

COMMENT ON TABLE management.avviso IS 'Avvisi agli utenti';
 
-- Column comments
 
COMMENT ON COLUMN management.avviso.id_avviso IS 'Identificativo univoco dell''avviso, autoincrementale';

COMMENT ON COLUMN management.avviso.cd_ambito IS 'Codice ambito';

COMMENT ON COLUMN management.avviso.cd_applicazione IS 'Codice applicazione';

COMMENT ON COLUMN management.avviso.ds_titolo_avviso IS 'Titolo dell''avviso';

COMMENT ON COLUMN management.avviso.ds_avviso IS 'Testo dell''avviso';

COMMENT ON COLUMN management.avviso.dt_inizio IS 'Timestamp a partire dal quale l''avviso sarà pubblicato';

COMMENT ON COLUMN management.avviso.dt_fine IS 'Timestamp a partire dal quale l''avviso non sarà più visualizzato';

COMMENT ON COLUMN management.avviso.nm_priorita IS 'Priorità 0=Critica,1=alta,2=media,3=bassa';

COMMENT ON COLUMN management.avviso.ds_user_ins_dt IS 'Utente che ha inserito la riga';

COMMENT ON COLUMN management.avviso.ts_ins_dt IS 'Timestamp inserimento';

COMMENT ON COLUMN management.avviso.ds_user_ult_agg_dt IS 'Utente che per ultimo ha aggiornato la riga';

COMMENT ON COLUMN management.avviso.ts_ult_agg_dt IS 'Timestamp ultimo aggiornamento';

COMMENT ON COLUMN management.avviso.ds_note_dt IS 'Descrizione contesto ultimo aggiornamento';
 
 
-- management.configurazione definition
 
-- Drop table
 
-- DROP TABLE management.configurazione;
 
CREATE TABLE management.configurazione ( cd_ambito bpchar(2) NOT NULL, cd_applicazione varchar(15) NOT NULL, des_nome_parametro varchar(100) NOT NULL, des_val_parametro text NULL, ty_parametro bpchar(1) NULL, CONSTRAINT configurazione_pk PRIMARY KEY (cd_ambito, cd_applicazione, des_nome_parametro), CONSTRAINT configurazione_per_applicazione_fk FOREIGN KEY (cd_ambito,cd_applicazione) REFERENCES management.applicazione(cd_ambito,cd_applicazione));

COMMENT ON TABLE management.configurazione IS 'Parametri di configurazione';
 
-- Column comments
 
COMMENT ON COLUMN management.configurazione.cd_ambito IS 'Codice ambito';

COMMENT ON COLUMN management.configurazione.cd_applicazione IS 'Codice applicazione';

COMMENT ON COLUMN management.configurazione.des_nome_parametro IS 'Nome del parametro';

COMMENT ON COLUMN management.configurazione.des_val_parametro IS 'Valore del parametro';

COMMENT ON COLUMN management.configurazione.ty_parametro IS 'Tipo parametro: "S"=String, "I"=Integer, "B"=Boolean';
 
 
-- management.nodo_struttura definition
 
-- Drop table
 
-- DROP TABLE management.nodo_struttura;
 
CREATE TABLE management.nodo_struttura ( id_nodo int4 NOT NULL, id_struttura int4 NOT NULL, id_nodo_padre int4 NULL, cd_nodo varchar(50) NOT NULL, nm_nodo varchar(200) NOT NULL, ds_nodo varchar(1000) NULL, CONSTRAINT nodo_struttura_pk PRIMARY KEY (id_nodo), CONSTRAINT nodo_struttura_per_struttura_fk FOREIGN KEY (id_struttura) REFERENCES management.struttura(id_struttura));

COMMENT ON TABLE management.nodo_struttura IS 'Nodo struttura';
 
-- Column comments
 
COMMENT ON COLUMN management.nodo_struttura.id_nodo IS 'Identificativo nodo';

COMMENT ON COLUMN management.nodo_struttura.id_struttura IS 'Identificativo struttura';

COMMENT ON COLUMN management.nodo_struttura.id_nodo_padre IS 'Identificativo nodo padre';

COMMENT ON COLUMN management.nodo_struttura.cd_nodo IS 'Codice del nodo';

COMMENT ON COLUMN management.nodo_struttura.nm_nodo IS 'Nome del nodo';

COMMENT ON COLUMN management.nodo_struttura.ds_nodo IS 'Descrizione del nodo';
 
 
-- management.utente definition
 
-- Drop table
 
-- DROP TABLE management.utente;
 
CREATE TABLE management.utente ( id_utente bigserial NOT NULL, ds_username varchar(50) NOT NULL, ds_password varchar(100) NULL, ds_nome varchar(60) NOT NULL, ds_cognome varchar(60) NOT NULL, cd_fiscale bpchar(16) NOT NULL, nm_telefono varchar(20) NULL, ds_email varchar(255) NULL, ds_ufficio varchar(255) NULL, dt_ultimo_login date NULL, fg_attivo_sn bpchar(1) NOT NULL, nm_tentativi_pin int2 DEFAULT 0 NOT NULL, nm_tentativi_login int2 DEFAULT 0 NOT NULL, fg_scad_account bpchar(1) DEFAULT 'N'::bpchar NOT NULL, fg_scad_password bpchar(1) DEFAULT 'N'::bpchar NOT NULL, fg_cambio_password bpchar(1) DEFAULT 'N'::bpchar NOT NULL, ts_agg_password timestamp NULL, cd_cnt int2 NULL, cd_stato bpchar(1) NULL, ty_utente bpchar(1) NULL, id_ente int2 NULL, ds_user_ins_dt varchar(50) NOT NULL, ts_ins_dt timestamp NULL, ds_user_ult_agg_dt varchar(50) NULL, ts_ult_agg_dt timestamp NULL, ds_note_dt varchar(50) NULL, CONSTRAINT utente_pk PRIMARY KEY (id_utente), CONSTRAINT utente_username_idx2 UNIQUE (ds_username), CONSTRAINT utente_per_ente_fk FOREIGN KEY (id_ente) REFERENCES management.ente(id_ente));

CREATE UNIQUE INDEX utente_cdfiscale_idx3 ON management.utente USING btree (cd_fiscale);

COMMENT ON TABLE management.utente IS 'Utente dell''applicazione';
 
-- Column comments
 
COMMENT ON COLUMN management.utente.id_utente IS 'Identificativo dell''utente';

COMMENT ON COLUMN management.utente.ds_username IS 'Username';

COMMENT ON COLUMN management.utente.ds_password IS 'password';

COMMENT ON COLUMN management.utente.ds_nome IS 'Nome utente';

COMMENT ON COLUMN management.utente.ds_cognome IS 'Cognome utente';

COMMENT ON COLUMN management.utente.cd_fiscale IS 'Codice fiscale';

COMMENT ON COLUMN management.utente.nm_telefono IS 'Numero di telefono utente';

COMMENT ON COLUMN management.utente.ds_email IS 'Email istituzionale dell''utente';

COMMENT ON COLUMN management.utente.ds_ufficio IS 'Ufficio d''appartenenza utente';

COMMENT ON COLUMN management.utente.dt_ultimo_login IS 'Data ultimo login effettuato dall''utente';

COMMENT ON COLUMN management.utente.fg_attivo_sn IS 'Flag utente attivo S/N';

COMMENT ON COLUMN management.utente.nm_tentativi_pin IS 'Numero tentativi PIN - usi futuri';

COMMENT ON COLUMN management.utente.nm_tentativi_login IS 'Numero tentativi di login errati';

COMMENT ON COLUMN management.utente.fg_scad_account IS 'Scadenza account S/N';

COMMENT ON COLUMN management.utente.fg_scad_password IS 'Scadenza password S/N';

COMMENT ON COLUMN management.utente.fg_cambio_password IS 'Scadenza password S/N';

COMMENT ON COLUMN management.utente.ts_agg_password IS 'Timestamp ultimo aggiornamento password';

COMMENT ON COLUMN management.utente.cd_cnt IS 'Codice contatore - usato da tributi - valori previsti NULL e 0';

COMMENT ON COLUMN management.utente.cd_stato IS 'Codice stato - usato da tributi - valori previsti NULL A e B';

COMMENT ON COLUMN management.utente.ty_utente IS 'Tipo utente - usato da tributi - valori previsti NULL e F';

COMMENT ON COLUMN management.utente.id_ente IS 'Identificativo ente di appartenenza';

COMMENT ON COLUMN management.utente.ds_user_ins_dt IS 'Utente che ha inserito la riga';

COMMENT ON COLUMN management.utente.ts_ins_dt IS 'Timestamp inserimento';

COMMENT ON COLUMN management.utente.ds_user_ult_agg_dt IS 'Utente che per ultimo ha aggiornato la riga';

COMMENT ON COLUMN management.utente.ts_ult_agg_dt IS 'Timestamp ultimo aggiornamento';

COMMENT ON COLUMN management.utente.ds_note_dt IS 'Descrizione contesto ultimo aggiornamento';
 
 
-- management.utente_per_profilo definition
 
-- Drop table
 
-- DROP TABLE management.utente_per_profilo;
 
CREATE TABLE management.utente_per_profilo ( id_utente int8 NOT NULL, id_profilo int8 NOT NULL, id_nodo int4 NULL, ds_user_ins_dt varchar(50) NOT NULL, ts_ins_dt timestamp NULL, ds_user_ult_agg_dt varchar(50) NULL, ts_ult_agg_dt timestamp NULL, ds_note_dt varchar(50) NULL, CONSTRAINT utente_per_profilo_pk PRIMARY KEY (id_utente, id_profilo), CONSTRAINT profilo_per_utente_fk FOREIGN KEY (id_profilo) REFERENCES management.profilo(id_profilo), CONSTRAINT profilo_utente_nodo_fk FOREIGN KEY (id_nodo) REFERENCES management.nodo_struttura(id_nodo), CONSTRAINT utente_per_profilo_fk FOREIGN KEY (id_utente) REFERENCES management.utente(id_utente));

COMMENT ON TABLE management.utente_per_profilo IS 'Applicazione sulla quale è abilitato l''utente con relativo profilo';
 
-- Column comments
 
COMMENT ON COLUMN management.utente_per_profilo.id_utente IS 'Identificativo dell''utente';

COMMENT ON COLUMN management.utente_per_profilo.id_profilo IS 'Identificativo del profilo';

COMMENT ON COLUMN management.utente_per_profilo.id_nodo IS 'Identificativo del nodo struttura - serve a tributi';

COMMENT ON COLUMN management.utente_per_profilo.ds_user_ins_dt IS 'Utente che ha inserito la riga';

COMMENT ON COLUMN management.utente_per_profilo.ts_ins_dt IS 'Timestamp inserimento';

COMMENT ON COLUMN management.utente_per_profilo.ds_user_ult_agg_dt IS 'Utente che per ultimo ha aggiornato la riga';

COMMENT ON COLUMN management.utente_per_profilo.ts_ult_agg_dt IS 'Timestamp ultimo aggiornamento';

COMMENT ON COLUMN management.utente_per_profilo.ds_note_dt IS 'Descrizione contesto ultimo aggiornamento';
 
 
-- management.utente_per_profilo_get definition
 
-- Drop table
 
-- DROP TABLE management.utente_per_profilo_get;
 
CREATE TABLE management.utente_per_profilo_get ( id_utente int8 NOT NULL, id_profilo int8 NOT NULL, codice_struttura_ged varchar(25) NOT NULL, ds_user_ins_dt varchar(50) NULL, ts_ins_dt timestamp NULL, ds_user_ult_agg_dt varchar(50) NULL, ts_ult_agg_dt timestamp NULL, ds_note_dt varchar(50) NULL, CONSTRAINT pk_upg PRIMARY KEY (id_utente, id_profilo, codice_struttura_ged), CONSTRAINT fk_profilo FOREIGN KEY (id_profilo) REFERENCES management.profilo(id_profilo), CONSTRAINT fk_upg_struttura_ged FOREIGN KEY (codice_struttura_ged) REFERENCES management.v_str_organizzativa(codice), CONSTRAINT fk_utente FOREIGN KEY (id_utente) REFERENCES management.utente(id_utente));
 
 
-- management.utente_profilo_per_applicazione definition
 
-- Drop table
 
-- DROP TABLE management.utente_profilo_per_applicazione;
 
CREATE TABLE management.utente_profilo_per_applicazione ( id_utente int8 NOT NULL, id_profilo int8 NOT NULL, cd_ambito bpchar(2) NOT NULL, cd_applicazione varchar(15) NOT NULL, ds_user_ins_dt varchar(50) NOT NULL, ts_ins_dt timestamp NULL, ds_user_ult_agg_dt varchar(50) NULL, ts_ult_agg_dt timestamp NULL, ds_note_dt varchar(50) NULL, CONSTRAINT utente_profilo_per_applicazione_pk PRIMARY KEY (id_utente, id_profilo, cd_ambito, cd_applicazione), CONSTRAINT applicazione_fk FOREIGN KEY (cd_ambito,cd_applicazione) REFERENCES management.applicazione(cd_ambito,cd_applicazione), CONSTRAINT utente_per_profilo_fk FOREIGN KEY (id_utente,id_profilo) REFERENCES management.utente_per_profilo(id_utente,id_profilo));
 
-- Column comments
 
COMMENT ON COLUMN management.utente_profilo_per_applicazione.id_utente IS 'Identificativo dell''utente';

COMMENT ON COLUMN management.utente_profilo_per_applicazione.id_profilo IS 'Identificativo del profilo';

COMMENT ON COLUMN management.utente_profilo_per_applicazione.cd_ambito IS 'Codice ambito';

COMMENT ON COLUMN management.utente_profilo_per_applicazione.cd_applicazione IS 'Codice applicazione';

COMMENT ON COLUMN management.utente_profilo_per_applicazione.ds_user_ins_dt IS 'Utente che ha inserito la riga';

COMMENT ON COLUMN management.utente_profilo_per_applicazione.ts_ins_dt IS 'Timestamp inserimento';

COMMENT ON COLUMN management.utente_profilo_per_applicazione.ds_user_ult_agg_dt IS 'Utente che per ultimo ha aggiornato la riga';

COMMENT ON COLUMN management.utente_profilo_per_applicazione.ts_ult_agg_dt IS 'Timestamp ultimo aggiornamento';

COMMENT ON COLUMN management.utente_profilo_per_applicazione.ds_note_dt IS 'Descrizione contesto ultimo aggiornamento';
 
 
-- management.visibilita definition
 
-- Drop table
 
-- DROP TABLE management.visibilita;
 
CREATE TABLE management.visibilita ( id_visibilita smallserial NOT NULL, nm_tabella varchar(256) NULL, nm_colonna varchar(100) NOT NULL, ds_valore varchar(1000) NOT NULL, ds_visibilita varchar(1000) NOT NULL, ds_breve varchar(50) NOT NULL, dipendenza int2 NULL, CONSTRAINT visibilita_pk PRIMARY KEY (id_visibilita), CONSTRAINT visibilita_dipendenza_fk FOREIGN KEY (dipendenza) REFERENCES management.visibilita(id_visibilita));

COMMENT ON TABLE management.visibilita IS 'Profili associati ad un utente';
 
-- Column comments
 
COMMENT ON COLUMN management.visibilita.id_visibilita IS 'Identificativo visibilita';

COMMENT ON COLUMN management.visibilita.nm_tabella IS 'Nome tabella';

COMMENT ON COLUMN management.visibilita.nm_colonna IS 'Nome colonna';

COMMENT ON COLUMN management.visibilita.ds_valore IS 'Valore';

COMMENT ON COLUMN management.visibilita.ds_visibilita IS 'Descrizione visibilita';

COMMENT ON COLUMN management.visibilita.ds_breve IS 'Descrizione visibilita breve';

COMMENT ON COLUMN management.visibilita.dipendenza IS 'Riferimento ad una riga di visibilità per esprimere una dipendenza';
 
 
-- management.abilitazione definition
 
-- Drop table
 
-- DROP TABLE management.abilitazione;
 
CREATE TABLE management.abilitazione ( id_abilitazione bigserial NOT NULL, cd_ambito bpchar(2) NOT NULL, cd_applicazione varchar(15) NOT NULL, cd_abilitazione varchar(100) NOT NULL, ds_abilitazione varchar(100) NOT NULL, id_menu int4 NULL, cd_esterno varchar(100) NULL, link varchar(200) NULL, ordine numeric NULL, ds_user_ins_dt varchar(50) NOT NULL, ts_ins_dt timestamp NULL, ds_user_ult_agg_dt varchar(50) NULL, ts_ult_agg_dt timestamp NULL, ds_note_dt varchar(50) NULL, CONSTRAINT abilitazione_pk PRIMARY KEY (id_abilitazione), CONSTRAINT cd_abilitazione_uk UNIQUE (cd_ambito, cd_applicazione, cd_abilitazione), CONSTRAINT abilitazione_per_applicazione_fk FOREIGN KEY (cd_ambito,cd_applicazione) REFERENCES management.applicazione(cd_ambito,cd_applicazione), CONSTRAINT abilitazione_per_menu_fk FOREIGN KEY (id_menu) REFERENCES management.menu(id_menu));

COMMENT ON TABLE management.abilitazione IS 'Abilitazione previste per area funzionale';
 
-- Column comments
 
COMMENT ON COLUMN management.abilitazione.id_abilitazione IS 'Identificativo abilitazione';

COMMENT ON COLUMN management.abilitazione.cd_ambito IS 'Codice ambito';

COMMENT ON COLUMN management.abilitazione.cd_applicazione IS 'Codice applicazione';

COMMENT ON COLUMN management.abilitazione.cd_abilitazione IS 'Codice abilitazione';

COMMENT ON COLUMN management.abilitazione.ds_abilitazione IS 'Descrizione Abilitazione';

COMMENT ON COLUMN management.abilitazione.id_menu IS 'Codice macro funzione - usato su tributi';

COMMENT ON COLUMN management.abilitazione.cd_esterno IS 'Codice esterno - usato su tributi';

COMMENT ON COLUMN management.abilitazione.ds_user_ins_dt IS 'Utente che ha inserito la riga';

COMMENT ON COLUMN management.abilitazione.ts_ins_dt IS 'Timestamp inserimento';

COMMENT ON COLUMN management.abilitazione.ds_user_ult_agg_dt IS 'Utente che per ultimo ha aggiornato la riga';

COMMENT ON COLUMN management.abilitazione.ts_ult_agg_dt IS 'Timestamp ultimo aggiornamento';

COMMENT ON COLUMN management.abilitazione.ds_note_dt IS 'Descrizione contesto ultimo aggiornamento';
 
 
-- management.nodo_per_visibilita definition
 
-- Drop table
 
-- DROP TABLE management.nodo_per_visibilita;
 
CREATE TABLE management.nodo_per_visibilita ( id_nodo int4 NOT NULL, id_visibilita int2 NOT NULL, CONSTRAINT ufficio_per_visibilita_pk PRIMARY KEY (id_nodo, id_visibilita), CONSTRAINT nodo_per_visibilita_fk FOREIGN KEY (id_nodo) REFERENCES management.nodo_struttura(id_nodo), CONSTRAINT visibilita_per_nodo_fk FOREIGN KEY (id_visibilita) REFERENCES management.visibilita(id_visibilita));

COMMENT ON TABLE management.nodo_per_visibilita IS 'Profili associati ad un utente';
 
-- Column comments
 
COMMENT ON COLUMN management.nodo_per_visibilita.id_nodo IS 'Identificativo nodo struttura';

COMMENT ON COLUMN management.nodo_per_visibilita.id_visibilita IS 'Identificativo visibilita';
 
 
-- management.profilo_per_abilitazione definition
 
-- Drop table
 
-- DROP TABLE management.profilo_per_abilitazione;
 
CREATE TABLE management.profilo_per_abilitazione ( id_profilo int8 NOT NULL, id_abilitazione int8 NOT NULL, ds_user_ins_dt varchar(50) NOT NULL, ts_ins_dt timestamp NULL, ds_user_ult_agg_dt varchar(50) NULL, ts_ult_agg_dt timestamp NULL, ds_note_dt varchar(50) NULL, CONSTRAINT profilo_per_abilitazione_pk PRIMARY KEY (id_profilo, id_abilitazione), CONSTRAINT abilitazione_per_profilo_fk FOREIGN KEY (id_abilitazione) REFERENCES management.abilitazione(id_abilitazione), CONSTRAINT profilo_per_abilitazione_fk FOREIGN KEY (id_profilo) REFERENCES management.profilo(id_profilo));

COMMENT ON TABLE management.profilo_per_abilitazione IS 'Abilitazioni associate al profilo';
 
-- Column comments
 
COMMENT ON COLUMN management.profilo_per_abilitazione.id_profilo IS 'Identificativo del profilo';

COMMENT ON COLUMN management.profilo_per_abilitazione.id_abilitazione IS 'Identificativo abilitazione';

COMMENT ON COLUMN management.profilo_per_abilitazione.ds_user_ins_dt IS 'Utente che ha inserito la riga';

COMMENT ON COLUMN management.profilo_per_abilitazione.ts_ins_dt IS 'Timestamp inserimento';

COMMENT ON COLUMN management.profilo_per_abilitazione.ds_user_ult_agg_dt IS 'Utente che per ultimo ha aggiornato la riga';

COMMENT ON COLUMN management.profilo_per_abilitazione.ts_ult_agg_dt IS 'Timestamp ultimo aggiornamento';

COMMENT ON COLUMN management.profilo_per_abilitazione.ds_note_dt IS 'Descrizione contesto ultimo aggiornamento';
 
 