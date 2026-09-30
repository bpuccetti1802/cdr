CREATE TABLE ANAG_USR.ALTRI_RESIDENTI
(
  ID_ACCERTAMENTO     NUMBER                    NOT NULL,
  ID_SOGGETTO         NUMBER                    NOT NULL,
  FLG_PARENTE         CHAR(1 CHAR),
  ID                  NUMBER                    NOT NULL,
  CODICE_INDIVIDUALE  NUMBER(10)                NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.ALTRI_RESIDENTI IS 'La tabella contiene i soggetti residenti ad un indirizzo in cui è stata effettuata una richiesta di cambio di residenza/domicilio.';

COMMENT ON COLUMN ANAG_USR.ALTRI_RESIDENTI.ID_ACCERTAMENTO IS 'Identificativo dell''accertamento per il quale sono stati riscontrati altri individui già residenti all''indirizzo dichiarato nel cambio di residenza/domicilio';

COMMENT ON COLUMN ANAG_USR.ALTRI_RESIDENTI.ID_SOGGETTO IS 'Id del soggetto già residente all''indirizzo dichiarato all''atto del cambio di residenza';

COMMENT ON COLUMN ANAG_USR.ALTRI_RESIDENTI.FLG_PARENTE IS 'S-> SI se il soggetto ha una parentela con l''individuo che ha richiesto il cambio di residenza/domicilio
N-> NO se il soggetto non  ha una parentela con l''individuo che ha richiesto il cambio di residenza/domicilio';



CREATE UNIQUE INDEX ANAG_USR.ALTRI_RESIDENTI_PK ON ANAG_USR.ALTRI_RESIDENTI
(ID)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.ALTRI_RESIDENTI ADD (
  CONSTRAINT ALTRI_RESIDENTI_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.ALTRI_RESIDENTI_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.ALTRI_RESIDENTI ADD (
  CONSTRAINT ACCERTAMENTO_FKV1 
  FOREIGN KEY (ID_ACCERTAMENTO) 
  REFERENCES ANAG_USR.ACCERTAMENTO_ISCRIZIONE (ID_ACCERTAMENTO_ISCRIZIONE)
  ENABLE VALIDATE,
  CONSTRAINT SOG_RES_FK 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.ANNULLAMENTO
(
  ID_ANNULLAMENTO      NUMBER                   NOT NULL,
  ID_ATTO              NUMBER,
  MOTIVO_ANNULLAMENTO  NUMBER,
  ID_SENTENZA          NUMBER,
  ID_MATRIMONIO        NUMBER,
  ID_OPERAZIONE_ANPR   NUMBER,
  ID_TIPO_RICHIESTA    NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.ANNULLAMENTO IS 'La tabella contiene gli annullamenti di atti di stato civile.';

COMMENT ON COLUMN ANAG_USR.ANNULLAMENTO.ID_ANNULLAMENTO IS 'Identificato dell''annullamento';

COMMENT ON COLUMN ANAG_USR.ANNULLAMENTO.ID_ATTO IS 'FK verso l''atto relativo all''annullamento';

COMMENT ON COLUMN ANAG_USR.ANNULLAMENTO.MOTIVO_ANNULLAMENTO IS 'Motivazione che ha condotto all''annullamento';

COMMENT ON COLUMN ANAG_USR.ANNULLAMENTO.ID_SENTENZA IS 'FK verso la sentenza di annullamento prodotta da un organo accreditato';

COMMENT ON COLUMN ANAG_USR.ANNULLAMENTO.ID_MATRIMONIO IS 'Identificativo del matrimonio per il quale è stato emesso l'' annullamento.';

COMMENT ON COLUMN ANAG_USR.ANNULLAMENTO.ID_OPERAZIONE_ANPR IS 'Identificativo dell''operazione ANPR';

COMMENT ON COLUMN ANAG_USR.ANNULLAMENTO.ID_TIPO_RICHIESTA IS 'Identificativo del tipo richiesta di divorzio';



CREATE UNIQUE INDEX ANAG_USR.ANNULLAMENTO_PK ON ANAG_USR.ANNULLAMENTO
(ID_ANNULLAMENTO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE INDEX ANAG_USR.IDX_ANNULLAMENTO_IDATTO ON ANAG_USR.ANNULLAMENTO
(ID_ATTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE INDEX ANAG_USR.IDX_ANNULLAMENTO_IDMATRIMONIO ON ANAG_USR.ANNULLAMENTO
(ID_MATRIMONIO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.ANNULLAMENTO ADD (
  CONSTRAINT ANNULLAMENTO_PK
  PRIMARY KEY
  (ID_ANNULLAMENTO)
  USING INDEX ANAG_USR.ANNULLAMENTO_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.ANNULLAMENTO ADD (
  CONSTRAINT ANNULLAMENTO_ATTO_FK 
  FOREIGN KEY (ID_ATTO) 
  REFERENCES ANAG_USR.ATTO (ID_ATTO)
  ENABLE VALIDATE,
  CONSTRAINT ANNULLAMENTO_FK1 
  FOREIGN KEY (MOTIVO_ANNULLAMENTO) 
  REFERENCES ANAG_USR.CONF_TIPO_CESS_MATRIMONIO (ID_TIPO_CESS_MATRIMONIO)
  ENABLE VALIDATE,
  CONSTRAINT ANNULLAMENTO_MATRIMONIO 
  FOREIGN KEY (ID_MATRIMONIO) 
  REFERENCES ANAG_USR.MATRIMONIO (ID_MATRIMONIO)
  ENABLE VALIDATE,
  CONSTRAINT ANNULLAMENTO_SENTENZA_FK 
  FOREIGN KEY (ID_SENTENZA) 
  REFERENCES ANAG_USR.SENTENZA (ID_SENTENZA)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.ASSOCIAZ_SENZA_FISSA_DIMORA
(
  ID_ASSOCIAZIONE    NUMBER(4)                  NOT NULL,
  NOME_ASSOCIAZIONE  VARCHAR2(250 BYTE),
  ID_TOPONIMO        NUMBER                     NOT NULL,
  ID_CIVICO          NUMBER                     NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.ASSOCIAZ_SENZA_FISSA_DIMORA IS 'La tabella contiene le anagrafiche delle associazioni dei senza fissa dimora.';

COMMENT ON COLUMN ANAG_USR.ASSOCIAZ_SENZA_FISSA_DIMORA.ID_ASSOCIAZIONE IS 'Identificativo dell''associazione ';

COMMENT ON COLUMN ANAG_USR.ASSOCIAZ_SENZA_FISSA_DIMORA.NOME_ASSOCIAZIONE IS 'nome dell''associazione';

COMMENT ON COLUMN ANAG_USR.ASSOCIAZ_SENZA_FISSA_DIMORA.ID_TOPONIMO IS 'Toponimo dell''indirizzo dell''associazione';

COMMENT ON COLUMN ANAG_USR.ASSOCIAZ_SENZA_FISSA_DIMORA.ID_CIVICO IS 'civico dell''indirizzo dell''associazione.';



CREATE UNIQUE INDEX ANAG_USR.CONF_ASS_SENZA_FISSA_DIMORA_PK ON ANAG_USR.ASSOCIAZ_SENZA_FISSA_DIMORA
(ID_ASSOCIAZIONE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.ASSOCIAZ_SENZA_FISSA_DIMORA ADD (
  CONSTRAINT CONF_ASS_SENZA_FISSA_DIMORA_PK
  PRIMARY KEY
  (ID_ASSOCIAZIONE)
  USING INDEX ANAG_USR.CONF_ASS_SENZA_FISSA_DIMORA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.ASSOCIAZ_SENZA_FISSA_DIMORA ADD (
  CONSTRAINT CIVICO_FK 
  FOREIGN KEY (ID_CIVICO) 
  REFERENCES ANAG_USR.CIVICO (ID_CIVICO)
  ENABLE VALIDATE,
  CONSTRAINT TOPONIMO_FK 
  FOREIGN KEY (ID_TOPONIMO) 
  REFERENCES ANAG_USR.TOPONIMO (ID_TOPONIMO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.ATTO
(
  ID_ATTO                 NUMBER CONSTRAINT NNC_ATTO__ID_ATTO NOT NULL,
  ID_COMUNE_ISCRIZIONE    NUMBER,
  ANNO                    NUMBER(4),
  PARTE                   VARCHAR2(5 BYTE),
  SERIE                   VARCHAR2(10 BYTE),
  VOLUME                  VARCHAR2(5 BYTE),
  UFFICIO                 VARCHAR2(50 BYTE),
  DATA_FORMAZIONE         DATE,
  TRASCRITTO              NUMBER,
  TIPO_PROTOCOLLO         VARCHAR2(10 BYTE),
  NUMERO_PROTOCOLLO       NUMBER,
  ANNO_PROTOCOLLO         NUMBER(4),
  NUMERO_PRATICA          NUMBER,
  ANNO_PRATICA            NUMBER(4),
  ID_STATO_PRATICA        NUMBER,
  ID_TIPO_ATTO            NUMBER(2),
  CODICE_TIPO_PROTOCOLLO  VARCHAR2(10 BYTE),
  ID_COMUNE_TRASCRIZIONE  NUMBER,
  ESPONENTE               VARCHAR2(20 BYTE),
  ATTO_AGGIOR             VARCHAR2(20 BYTE),
  NUMERO_ATTO             VARCHAR2(20 BYTE),
  ID_ATTO_ANSC            VARCHAR2(100 BYTE),
  ANNO_ANSC               VARCHAR2(4 BYTE),
  ID_COMUNE               NUMBER,
  NUMERO_NAZIONALE        VARCHAR2(30 BYTE),
  NUMERO_COMUNALE         VARCHAR2(30 BYTE),
  DATA_ANSC               DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.ATTO IS 'La tabella contiene le informazioni rilevanti (es. anno, parte, serie, volume, ecc.) relative ad un atto di stato civile.';

COMMENT ON COLUMN ANAG_USR.ATTO.ID_ATTO IS 'Campo che indica l''id dell''atto.';

COMMENT ON COLUMN ANAG_USR.ATTO.ID_COMUNE_ISCRIZIONE IS 'Indica il comune in cui si registra l''atto. ';

COMMENT ON COLUMN ANAG_USR.ATTO.ANNO IS 'Campo che indica l''anno in cui si registra l''atto.';

COMMENT ON COLUMN ANAG_USR.ATTO.PARTE IS 'Campo che indica il numero della parte dell''atto.';

COMMENT ON COLUMN ANAG_USR.ATTO.SERIE IS 'Campo che indica la serie dell''atto.';

COMMENT ON COLUMN ANAG_USR.ATTO.VOLUME IS 'Campo che indica il volume dove si trova l''atto.';

COMMENT ON COLUMN ANAG_USR.ATTO.UFFICIO IS 'Campo che indica l''ufficio in cui si registra l''atto.';

COMMENT ON COLUMN ANAG_USR.ATTO.DATA_FORMAZIONE IS 'Campo che indica la data di formazione dell''atto.';

COMMENT ON COLUMN ANAG_USR.ATTO.TRASCRITTO IS 'Flag che indica se l''atto è iscritto o trascritto.
0 se iscritto (originale), 1 se trascritto.';

COMMENT ON COLUMN ANAG_USR.ATTO.TIPO_PROTOCOLLO IS 'Codice che identific univocamente l''ente protocollante dell''atto';

COMMENT ON COLUMN ANAG_USR.ATTO.NUMERO_PROTOCOLLO IS 'Campo che indica il numero del protocollo.';

COMMENT ON COLUMN ANAG_USR.ATTO.ANNO_PROTOCOLLO IS 'Campo che indica l''anno del protocollo.';

COMMENT ON COLUMN ANAG_USR.ATTO.NUMERO_PRATICA IS 'Campo che indica il numero della pratica.';

COMMENT ON COLUMN ANAG_USR.ATTO.ANNO_PRATICA IS 'Campo che indica il l''anno della pratica.';

COMMENT ON COLUMN ANAG_USR.ATTO.ID_STATO_PRATICA IS 'Campo che indica lo stato della pratica.';

COMMENT ON COLUMN ANAG_USR.ATTO.ID_TIPO_ATTO IS 'Codice identificativo della tipologia di atto.';

COMMENT ON COLUMN ANAG_USR.ATTO.CODICE_TIPO_PROTOCOLLO IS 'Codice identificativo dell''ente protocollante dell''atto.';

COMMENT ON COLUMN ANAG_USR.ATTO.ESPONENTE IS 'Campo che indica l''esponente dell''atto';

COMMENT ON COLUMN ANAG_USR.ATTO.ATTO_AGGIOR IS 'campo che indica l''identificativo dell''atto usato da aggior. concatenazione di numero parte e serie';



CREATE INDEX ANAG_USR.ATTO__IX3 ON ANAG_USR.ATTO
(NUMERO_ATTO, ANNO, PARTE, SERIE, ESPONENTE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.ATTO__PK ON ANAG_USR.ATTO
(ID_ATTO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.ATTO__UNV1 ON ANAG_USR.ATTO
(CODICE_TIPO_PROTOCOLLO, ANNO_PROTOCOLLO, NUMERO_PROTOCOLLO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.ATTO__UNV2 ON ANAG_USR.ATTO
(NUMERO_PRATICA, ANNO_PRATICA)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE TRIGGER ANAG_USR.LOG_TRG 
AFTER INSERT OR UPDATE OR DELETE
  ON ANAG_USR.ATTO 
FOR EACH ROW
DISABLE
BEGIN
    if (1=2 ) then --disabilitato
    
      IF INSERTING and :new.data_formazione > to_date('31122022','ddmmyyyy') THEN
        INSERT INTO ANAG_STORICO.ATTO VALUES     
        (:new.ID_ATTO ,:new.ID_COMUNE_ISCRIZIONE ,:new.NUMERO_ATTO ,:new.ANNO ,:new.PARTE ,:new.SERIE ,:new.VOLUME ,:new.UFFICIO ,:new.DATA_FORMAZIONE ,:new.TRASCRITTO ,:new.TIPO_PROTOCOLLO ,:new.NUMERO_PROTOCOLLO ,:new.ANNO_PROTOCOLLO ,:new.NUMERO_PRATICA ,:new.ANNO_PRATICA ,:new.ID_STATO_PRATICA ,:new.ID_TIPO_ATTO ,:new.CODICE_TIPO_PROTOCOLLO ,:new.ID_COMUNE_TRASCRIZIONE ,:new.ESPONENTE ,:new.ATTO_AGGIOR);
      
      ELSIF UPDATING and :new.data_formazione > to_date('31122022','ddmmyyyy') THEN
        update anag_storico.atto set 
            ID_COMUNE_ISCRIZIONE = :new.ID_COMUNE_ISCRIZIONE
            ,ANNO = :new.ANNO
            ,PARTE = :new.PARTE
            ,SERIE = :new.SERIE
            ,VOLUME = :new.VOLUME
            ,UFFICIO = :new.UFFICIO
            ,DATA_FORMAZIONE = :new.DATA_FORMAZIONE
            ,TRASCRITTO = :new.TRASCRITTO
            ,TIPO_PROTOCOLLO = :new.TIPO_PROTOCOLLO
            ,NUMERO_PROTOCOLLO = :new.NUMERO_PROTOCOLLO
            ,ANNO_PROTOCOLLO = :new.ANNO_PROTOCOLLO
            ,NUMERO_PRATICA = :new.NUMERO_PRATICA
            ,ANNO_PRATICA = :new.ANNO_PRATICA
            ,ID_STATO_PRATICA = :new.ID_STATO_PRATICA
            ,ID_TIPO_ATTO = :new.ID_TIPO_ATTO
            ,CODICE_TIPO_PROTOCOLLO = :new.CODICE_TIPO_PROTOCOLLO
            ,ID_COMUNE_TRASCRIZIONE = :new.ID_COMUNE_TRASCRIZIONE
            ,ESPONENTE = :new.ESPONENTE
            ,ATTO_AGGIOR = :new.ATTO_AGGIOR
            ,NUMERO_ATTO = :new.NUMERO_ATTO
        where ID_ATTO = :new.ID_ATTO;
        
      ELSIF DELETING and :old.data_formazione > to_date('31122022','ddmmyyyy') THEN
      
        DELETE FROM  ANAG_STORICO.ATTO@ANAG_USR_TO_STORICO  WHERE ID_ATTO = :old.ID_ATTO;
        
      END IF;
      
  end if;
END;
/


CREATE OR REPLACE SYNONYM ELET_USR.ATTO FOR ANAG_USR.ATTO;


ALTER TABLE ANAG_USR.ATTO ADD (
  CONSTRAINT ATTO__PK
  PRIMARY KEY
  (ID_ATTO)
  USING INDEX ANAG_USR.ATTO__PK
  ENABLE VALIDATE,
  CONSTRAINT ATTO__UNV1
  UNIQUE (CODICE_TIPO_PROTOCOLLO, ANNO_PROTOCOLLO, NUMERO_PROTOCOLLO)
  USING INDEX ANAG_USR.ATTO__UNV1
  ENABLE VALIDATE,
  CONSTRAINT ATTO__UNV2
  UNIQUE (NUMERO_PRATICA, ANNO_PRATICA)
  USING INDEX ANAG_USR.ATTO__UNV2
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.ATTO ADD (
  CONSTRAINT ATTO_CONF_TIPO_ATTO_FK 
  FOREIGN KEY (ID_TIPO_ATTO) 
  REFERENCES ANAG_USR.CONF_TIPO_ATTO (ID_TIPO_ATTO)
  ENABLE VALIDATE,
  CONSTRAINT ATTO_CONF_TIPO_PROTOCOLLO_FK 
  FOREIGN KEY (CODICE_TIPO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE,
  CONSTRAINT ATTO_FK1 
  FOREIGN KEY (ID_COMUNE_TRASCRIZIONE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT ATTO_FK2 
  FOREIGN KEY (ID_COMUNE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT ATTO__COMUNE_FK 
  FOREIGN KEY (ID_COMUNE_ISCRIZIONE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT ATTO__CONF_STATO_PRATICA_FK 
  FOREIGN KEY (ID_STATO_PRATICA) 
  REFERENCES ANAG_USR.CONF_STATO_PRATICA (ID_STATO_PRATICA)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO
(
  ID_CAMBIO_RESIDENZA_DOMICILIO  NUMBER         NOT NULL,
  CONTEGGIO                      CHAR(1 BYTE),
  TIPO_ISTANZA                   CHAR(1 BYTE),
  DATA_IMMIGRAZIONE              DATE,
  NOTE                           VARCHAR2(4000 BYTE),
  ID_RESIDENZA                   NUMBER,
  ID_FAMIGLIA_CONVIVENZA         NUMBER,
  CODICE_TIPO_PROTOCOLLO         VARCHAR2(10 BYTE),
  ANNO_PROTOCOLLO                NUMBER(4),
  NUMERO_PROTOCOLLO              NUMBER,
  ID_TIPO_RICHIESTA_CAMBIO       NUMBER,
  ID_COMUNE_PROVENIENZA          NUMBER,
  ID_STATO_PRATICA               NUMBER,
  NUMERO_PRATICA                 NUMBER,
  ANNO_PRATICA                   INTEGER,
  DATA_AGGIORNAMENTO             DATE,
  TIPOLOGIA_CAMBIO               CHAR(1 BYTE),
  ID_RECAPITO                    NUMBER,
  ID_STATO_ESTERO                NUMBER,
  ID_CONTRATTO_ABITATIVO         NUMBER,
  ID_LOCALITA                    NUMBER,
  CHK_PROVENIENZA                CHAR(1 BYTE),
  CHK_DICHIARANTE                CHAR(1 BYTE),
  CHK_INDIRIZZO                  CHAR(1 BYTE),
  CHK_FAMIGLIA_RES               CHAR(1 BYTE),
  CHK_FAMILIARI                  CHAR(1 BYTE),
  CHK_CONTRATTO_AB               CHAR(1 BYTE),
  CHK_RECAPITI                   CHAR(1 BYTE),
  CHK_ALLEGATI                   CHAR(1 BYTE),
  FLAG_ENTRATA_FAMIGLIA          NUMBER,
  ID_SOGGETTO_RESIDENTE          NUMBER,
  ID_OPERAZIONE_ANPR             VARCHAR2(20 BYTE),
  DATA_DEFINIZIONE_PRATICA       DATE,
  FLG_ACCERTAMENTO               NUMBER,
  DICHIARAZIONE                  BLOB,
  NOME_DICHIARAZIONE             VARCHAR2(80 BYTE),
  FLAG_FAMIGLIA_COABITANTE       NUMBER,
  ID_CODICE_LEGAME               NUMBER,
  PDF_FINE_PROCEDIMENTO          BLOB,
  NOME_PDF_FINE_PROC             VARCHAR2(80 BYTE),
  PDF_INIZIO_PROCEDIMENTO        BLOB,
  NOME_PDF_INIZIO_PROC           VARCHAR2(80 BYTE),
  ID_MOTIVO_PROVENIENZA          NUMBER,
  CHK_FAMIGLIE                   CHAR(1 BYTE),
  ID_UTENTE                      NUMBER,
  PDF_COMUNICAZ_POP_TEMP         BLOB,
  NOME_PDF_COMUNICAZ_POP_TEMP    VARCHAR2(80 BYTE),
  ID_RESIDENZA_PROVENIENZA       NUMBER,
  NUMERO_PRATICA_ANPR            VARCHAR2(10 BYTE),
  ID_FAMIGLIA_FINALE             INTEGER,
  TOT_FAM_FINALE                 NUMBER,
  TOT_FAM_PROV                   NUMBER,
  DATA_RIPRISTINO                DATE,
  OPERATORE_RIPRISTINO           NUMBER,
  ID_CAMBIO_ONLINE               NUMBER,
  NOTE_RIGETTO                   VARCHAR2(4000 BYTE),
  TUTELA_A                       CHAR(1 BYTE),
  TUTELA_B                       CHAR(1 BYTE)
)
LOB (PDF_COMUNICAZ_POP_TEMP) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
LOB (DICHIARAZIONE) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
LOB (PDF_FINE_PROCEDIMENTO) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
LOB (PDF_INIZIO_PROCEDIMENTO) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO IS 'La tabella contiene le pratiche di cambio di residenza o domicilio.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ID_CAMBIO_RESIDENZA_DOMICILIO IS 'Campo che identifica univocamente un cambio di residenza o domicillio.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.CONTEGGIO IS 'Flag che indica se il cambio di residenza ha valenza ai fini del conteggio.

valorizzato con S se vale per il conteggio, N  altrimenti.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.TIPO_ISTANZA IS 'Flag che descrive la tipologia di istanza del cambio di domicilio:
- P istanza di parte;
- U istanza d''ufficio.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.DATA_IMMIGRAZIONE IS 'Data in cui è stato effettuato il cambio di residenza o domicilio.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.NOTE IS 'Campo in cui è possibile salvare delle note relative al cambio di residenza o abitazione.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ID_RESIDENZA IS 'Codice identificativo della residenza associata al cambio di residenza o domicilio.

Identifica la residenza di immigrazione.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ID_FAMIGLIA_CONVIVENZA IS 'Codice identificativo della famiglia o convivenza in cui intende entrare il soggetto immigrante relativo al cambio di residenza o domicilio.
';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.CODICE_TIPO_PROTOCOLLO IS 'Codice che identifica univocamente l''ente protocollante associato al cambio di residenza o domicilio.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ANNO_PROTOCOLLO IS 'Anno di riferimento del protocollo associato al cambio di residenza o domicilio.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.NUMERO_PROTOCOLLO IS 'Numero che identifica il protocollo associato al cambio di residenza o domicilio';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ID_TIPO_RICHIESTA_CAMBIO IS 'Codice identificativo della tipologia di richiesta con il quale è pervenuto il relativo cambio di residenza o domicilio.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ID_COMUNE_PROVENIENZA IS 'Codice identificativo del comune di provenienza del soggetto immigrante del relativo cambio di residenza o domicilio.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ID_STATO_PRATICA IS 'Codice identificativo dello stato di avanzamento della pratica collegata al cambio di residenza o domicilio.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.NUMERO_PRATICA IS 'Numero associato alla pratica relativa cambio di residenza o domicilio.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ANNO_PRATICA IS 'Anno in cui è stata lavorata la pratica associata al relativo cambio di residenza o domicilio.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.DATA_AGGIORNAMENTO IS 'Data in cui la pratica di cambio residenza domicilio ha subito l''ultima modifica.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.TIPOLOGIA_CAMBIO IS 'Flag che indica se la pratica è un cambio di residenza o un cambio di abitazione. R se cambio di residenza, A se cambio di abitazione';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ID_RECAPITO IS 'Codice identificativo del recapito.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ID_STATO_ESTERO IS 'In alternativa a Id_localita.Codice che identifica lo stato estero di provenienza';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ID_CONTRATTO_ABITATIVO IS 'Campo che identifica il contratto abitativo';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ID_LOCALITA IS 'Codice identificativo della Località estera di provenienza

Da inserire in alternativa al comune di provenienza.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.CHK_PROVENIENZA IS 'Campo che indica se la pagina Provenienza è stata completata: 0 -> no, 1 -> si.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.CHK_DICHIARANTE IS 'Campo che indica se la pagina Dichiarante è stata completata: 0 -> no, 1 -> si.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.CHK_INDIRIZZO IS 'Campo che indica se la pagina Indirizzo è stata completata: 0 -> no, 1 -> si.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.CHK_FAMIGLIA_RES IS 'Campo che indica se la pagina Famiglia residente è stata completata: 0 -> no, 1 -> si.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.CHK_FAMILIARI IS 'Campo che indica se la pagina Familiari è stata completata: 0 -> no, 1 -> si.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.CHK_CONTRATTO_AB IS 'Campo che indica se la pagina Contratto abitativo è stata completata: 0 -> no, 1 -> si.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.CHK_RECAPITI IS 'Campo che indica se la pagina recapiti è stata completata: 0 -> no, 1 -> si.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.CHK_ALLEGATI IS 'Campo che indica se la pagina allegati è stata completata: 0 -> no, 1 -> si.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.FLAG_ENTRATA_FAMIGLIA IS 'Campo che indica se in dichiarante entra in una famiglia esistente 1 -> no, 2 -> si, 3-> senza fissa dimora.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ID_SOGGETTO_RESIDENTE IS 'identificativo del soggetto residente alla residenza in cui il dichiarante vuole immigrare';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ID_OPERAZIONE_ANPR IS 'identificativo dell''operazione effettuata per la notifica ad ANPR dell''avvenutoCRICA';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.FLG_ACCERTAMENTO IS 'Campo che indica se l''accertamento per il cambio di residenza è in corso. 1->In corso, 2 altrimenti';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.DICHIARAZIONE IS 'Campo che contiene il file della dichiarazione di residenza';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.NOME_DICHIARAZIONE IS 'Campo che contiene il nome della dichiarazione di residenza.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.FLAG_FAMIGLIA_COABITANTE IS 'Campo che indica se la pratica riguarda una famiglia coabitante.1-> famiglia coabitante flaggato, 0 -> non flaggato';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ID_CODICE_LEGAME IS 'Campo che indica il tipo di legame tra il dichiarante e il soggetto residente';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.PDF_FINE_PROCEDIMENTO IS 'Campo contenente il documento di fine procedimento iscrizione';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.NOME_PDF_FINE_PROC IS 'Campo che identifica il nome del file Fine procedimento';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.PDF_INIZIO_PROCEDIMENTO IS 'Campo contenente il documento di inizio procedimento per cambio d''bitazione o iscrizione';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.NOME_PDF_INIZIO_PROC IS 'Campo che identifica il nome del file inizio procedimento';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.CHK_FAMIGLIE IS 'Campo che indica se il flusso del cri ha settato le famiglie da sistemare: 0 -> no, 1 -> si.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ID_UTENTE IS 'Campo che identifica l''utente che ha lavorato la pratica.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.PDF_COMUNICAZ_POP_TEMP IS 'Campo contenente il pdf della comunicazione verso comune di provenienza per pratica popolazione temporanea';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.NOME_PDF_COMUNICAZ_POP_TEMP IS 'Campo contenente il nome della comunicazione verso comune di provenienza per pratica pop temporanea';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ID_RESIDENZA_PROVENIENZA IS 'Indirizzo di provenienza del dichiarante della pratica';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.NUMERO_PRATICA_ANPR IS 'Indica il numero della pratica per anpr.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ID_FAMIGLIA_FINALE IS 'La famiglia del soggetto alla fine del cambio';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.TOT_FAM_FINALE IS 'Numero di familiari nella famiglia finale alla fine della pratica';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.TOT_FAM_PROV IS 'Numero di familiari nella famiglia di provenienza alla fine della pratica';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.ID_CAMBIO_ONLINE IS 'Indica l''id del cambio residenza online';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.NOTE_RIGETTO IS 'Campo contenente le note per il rigetto della pratica anpr online ';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.TUTELA_A IS 'Flag che indica se è stata selezionata l''opzione "Persone che fanno parte di nuclei che sono seguiti da servizi sociali di Roma Capitale o del Comune di provenienza anagrafica, ovvero in condizione di particolare fragilità e vulnerabilità sociale quali la presenza di disabili, figli minori o persone ultrasessantacinquenni."';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO.TUTELA_B IS 'Flag che indica se è stata selezionata l''opzione "Persone che fanno parte di nuclei con un reddito inferiore al limite stabilito in applicazione dell’art. 11 della legge della Regione Lazio 6 agosto 1999, n. 12 e aggiornato con cadenza biennale sulla base della variazione assoluta dell’indice ISTAT dei prezzi al consumo per le famiglie degli operai e degli impiegati, da ultimo fissato a 21.190,14 euro (Determinazione della Regione Lazio n. GR 4103 del 24 agosto 2021)."';



CREATE UNIQUE INDEX ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO__UN ON ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO
(NUMERO_PRATICA, ANNO_PRATICA)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.CAMBI_RESIDENZA_DOMICILIO_PK ON ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO
(ID_CAMBIO_RESIDENZA_DOMICILIO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CAMBIO_RESIDENZA_DOMICILIO FOR ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO;


ALTER TABLE ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO ADD (
  CONSTRAINT CAMBI_RESIDENZA_DOMICILIO_PK
  PRIMARY KEY
  (ID_CAMBIO_RESIDENZA_DOMICILIO)
  USING INDEX ANAG_USR.CAMBI_RESIDENZA_DOMICILIO_PK
  ENABLE VALIDATE,
  CONSTRAINT CAMBIO_RESIDENZA_DOMICILIO__UN
  UNIQUE (NUMERO_PRATICA, ANNO_PRATICA)
  USING INDEX ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO__UN
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO ADD (
  CONSTRAINT CAMBIO_RESIDENZA_DOMICILI_FK1 
  FOREIGN KEY (ID_MOTIVO_PROVENIENZA) 
  REFERENCES ANAG_USR.CONF_MOTIVO_PROVENIENZA (ID_MOTIVO)
  ENABLE VALIDATE,
  CONSTRAINT CAMBIO_RESIDENZA_ONLINE_FK2 
  FOREIGN KEY (ID_CAMBIO_ONLINE) 
  REFERENCES ANAG_USR.CAMBIO_RESIDENZA_ONLINE (ID_CAMBIO_RESIDENZA_ONLINE)
  ENABLE VALIDATE,
  CONSTRAINT COMUNE_FK 
  FOREIGN KEY (ID_COMUNE_PROVENIENZA) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT CONF_STATO_PRATICA_FK 
  FOREIGN KEY (ID_STATO_PRATICA) 
  REFERENCES ANAG_USR.CONF_STATO_PRATICA (ID_STATO_PRATICA)
  ENABLE VALIDATE,
  CONSTRAINT CONF_TIPO_PROTOCOLLO_FK 
  FOREIGN KEY (CODICE_TIPO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE,
  CONSTRAINT CONF_TIPO_RICHIESTA_CAMBIO_FK 
  FOREIGN KEY (ID_TIPO_RICHIESTA_CAMBIO) 
  REFERENCES ANAG_USR.CONF_TIPO_RICHIESTA_CAMBIO (ID_TIPO_RICHIESTA_CAMBIO)
  ENABLE VALIDATE,
  CONSTRAINT FAMIGLIA_CONV_FK 
  FOREIGN KEY (ID_FAMIGLIA_CONVIVENZA) 
  REFERENCES ANAG_USR.FAMIGLIA_CONVIVENZA (ID_FAMIGLIA_CONV)
  ENABLE VALIDATE,
  CONSTRAINT ID_CODICE_LEGAME_FK1 
  FOREIGN KEY (ID_CODICE_LEGAME) 
  REFERENCES ANAG_USR.CONF_CODICE_LEGAME (ID_CODICE_LEGAME)
  ENABLE VALIDATE,
  CONSTRAINT ID_CONTRATTO_ABITATIVO_FK1 
  FOREIGN KEY (ID_CONTRATTO_ABITATIVO) 
  REFERENCES ANAG_USR.CONTRATTO_ABITATIVO (ID_CONTRATTO_ABITATIVO)
  ENABLE VALIDATE,
  CONSTRAINT ID_RESIDENZA_PROVENIENZA_FK 
  FOREIGN KEY (ID_RESIDENZA_PROVENIENZA) 
  REFERENCES ANAG_USR.RESIDENZA (ID_RESIDENZA)
  ENABLE VALIDATE,
  CONSTRAINT ID_SOGGETTO_RESIDENTE_FK 
  FOREIGN KEY (ID_SOGGETTO_RESIDENTE) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT ID_UTENTE_FK 
  FOREIGN KEY (ID_UTENTE) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE,
  CONSTRAINT LOCALITA_FK1 
  FOREIGN KEY (ID_LOCALITA) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE,
  CONSTRAINT RECAPITO_FK1 
  FOREIGN KEY (ID_RECAPITO) 
  REFERENCES ANAG_USR.RECAPITI (ID_RECAPITO)
  ENABLE VALIDATE,
  CONSTRAINT RESIDENZA_FKV2 
  FOREIGN KEY (ID_RESIDENZA) 
  REFERENCES ANAG_USR.RESIDENZA (ID_RESIDENZA)
  ENABLE VALIDATE,
  CONSTRAINT STATO_ESTERO_FK 
  FOREIGN KEY (ID_STATO_ESTERO) 
  REFERENCES ANAG_USR.CONF_STATO_ESTERO (ID_STATO_ESTERO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CARTA_IDENTITA
(
  NUMERO_CARTA_IDENTITA      VARCHAR2(20 BYTE)  NOT NULL,
  DATA_RILASCIO              DATE,
  DATA_SCADENZA              DATE,
  ESPATRIO                   VARCHAR2(1 BYTE),
  TIPOLOGIA                  VARCHAR2(1 BYTE),
  ID_CONSOLATO               NUMBER,
  ID_COMUNE                  NUMBER,
  ID_STATO_VALIDITA          NUMBER,
  ALTEZZA                    VARCHAR2(4 BYTE),
  SEGNI_PARTICOLARI          VARCHAR2(250 BYTE),
  ID_MODALITA_RILASCIO_CI    NUMBER,
  ID_CONSENSO_RILASCIO_CI    NUMBER,
  CHK_CARTA_STAMPATA         VARCHAR2(1 BYTE),
  ID_MOTIVO_ANNULLAMENTO     NUMBER,
  DATA_ANNULLAMENTO          DATE,
  ID_UTENTE                  NUMBER,
  DONAZIONE_ORGANI           VARCHAR2(1 BYTE),
  STAMPA_DONAZIONE           VARCHAR2(1 BYTE),
  ID_MODALITA_RILASCIO_CIE   NUMBER,
  ID_MOTIVO_ANN_REV_CIE      NUMBER,
  ID_CAPELLI                 NUMBER,
  ID_OCCHI                   NUMBER,
  STAMPA_STATO_CIVILE        VARCHAR2(1 BYTE),
  ID_LOCALITA                NUMBER,
  ID_SEDE_MUNICIPIO          NUMBER,
  ALTRO_MOTIVO_ANNULLAMENTO  VARCHAR2(4000 BYTE),
  PROTEZIONE_INTERNAZIONALE  VARCHAR2(1 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CARTA_IDENTITA IS 'La tabella contiene le informazioni relative alle carte d''identità di un soggetto.';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.NUMERO_CARTA_IDENTITA IS 'Numero identificatico della carta d''identità.';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.DATA_RILASCIO IS 'Data in cui la carta d''identita è stata rilasciata.';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.DATA_SCADENZA IS 'Data di fine validità della carta d''identità.';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.ESPATRIO IS 'Flag che indica se la carta d''identità è valida per l''espatrio. 

Avrà valore "S" se è valida per l''espatrio, alrimenti "N". ';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.TIPOLOGIA IS 'Flag che indica se la carta d''identità è cartacea o elettronica.

Il campo avrà valora 0 per cartacea e 1 per elettronica.';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.ID_CONSOLATO IS 'Codice identificativo del consoltato che ha rilasciato la carta d''identita.

';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.ID_COMUNE IS 'Codice identificativo del comune di rilascio della carta d''identità.';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.ID_STATO_VALIDITA IS 'Identificativo dello stato di validità della carta d''identità';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.SEGNI_PARTICOLARI IS 'Campo che identifica i segni particolari del soggetto.';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.ID_MODALITA_RILASCIO_CI IS 'Campo che identifica la modalita di rilascio della carta d''identita.';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.ID_CONSENSO_RILASCIO_CI IS 'Campo che identifica il consenso al rilascio della carta d''identita.';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.CHK_CARTA_STAMPATA IS 'Campo che indica se una carta è stata stampata. N -> NO , S -> SI';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.ID_MOTIVO_ANNULLAMENTO IS 'Identificativo del motivo di annullamento della carta d''identità.';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.DATA_ANNULLAMENTO IS 'Data in cui la carta d''identita è stata annullata.';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.ID_UTENTE IS 'Campo che identifica l''utente che ha rilasciato la carta.';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.DONAZIONE_ORGANI IS 'S->SI N->NO X->PREFERENZA NON ESPRESSA';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.STAMPA_DONAZIONE IS 'S->SI, N->NO';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.ID_MODALITA_RILASCIO_CIE IS 'Campo che identifica la modalita di rilascio della CIE';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.ID_MOTIVO_ANN_REV_CIE IS 'Identificativo del motivo di annullamento della CIE';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.ID_CAPELLI IS 'Identificativo del colore dei capelli';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.ID_OCCHI IS 'Identificativo del colore degli occhi';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.STAMPA_STATO_CIVILE IS 'S->Mostra info stato civile sulla carta N->Non mostra info su stato civile';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.ID_LOCALITA IS 'località di rilascio della carta --migrata in mancanza di codice consolato di rilascio';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.ALTRO_MOTIVO_ANNULLAMENTO IS 'Campo per la memorizzazione dei motivi di annullamento custom';

COMMENT ON COLUMN ANAG_USR.CARTA_IDENTITA.PROTEZIONE_INTERNAZIONALE IS 'S->SI, N->NO';



CREATE UNIQUE INDEX ANAG_USR.CARTAIDENTITA_PK ON ANAG_USR.CARTA_IDENTITA
(NUMERO_CARTA_IDENTITA)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CARTA_IDENTITA FOR ANAG_USR.CARTA_IDENTITA;


ALTER TABLE ANAG_USR.CARTA_IDENTITA ADD (
  CONSTRAINT CARTAIDENTITA_PK
  PRIMARY KEY
  (NUMERO_CARTA_IDENTITA)
  USING INDEX ANAG_USR.CARTAIDENTITA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CARTA_IDENTITA ADD (
  CONSTRAINT CARTAIDENTITA_COMUNE_FK 
  FOREIGN KEY (ID_COMUNE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT CARTA_IDENTITA_CONSOLATO_FK 
  FOREIGN KEY (ID_CONSOLATO) 
  REFERENCES ANAG_USR.CONSOLATO (ID_CONSOLATO)
  ENABLE VALIDATE,
  CONSTRAINT CARTA_IDENTITA_FK1 
  FOREIGN KEY (ID_LOCALITA) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE,
  CONSTRAINT CARTA_IDENTITA_FK2 
  FOREIGN KEY (ID_SEDE_MUNICIPIO) 
  REFERENCES ANAG_USR.CONF_SEDE_MUNICIPIO (ID_SEDE_MUNICIPIO)
  ENABLE VALIDATE,
  CONSTRAINT CARTA_IDENTITA_VALIDITA_FK 
  FOREIGN KEY (ID_CONSOLATO) 
  REFERENCES ANAG_USR.CONF_STATO_VALIDITA_CARTA (ID_STATO_VALIDITA_CARTA)
  ENABLE VALIDATE,
  CONSTRAINT CONSENSO_RILASCIO_CI_FK1 
  FOREIGN KEY (ID_CONSENSO_RILASCIO_CI) 
  REFERENCES ANAG_USR.CONSENSO_RILASCIO_CI (ID_CONSENSO_RILASCIO_CI)
  ENABLE VALIDATE,
  CONSTRAINT FKN0XL5S1FCH53I400YB0BERX33 
  FOREIGN KEY (ID_STATO_VALIDITA) 
  REFERENCES ANAG_USR.CONF_STATO_VALIDITA_CARTA (ID_STATO_VALIDITA_CARTA)
  ENABLE VALIDATE,
  CONSTRAINT ID_CAPELLI_FK 
  FOREIGN KEY (ID_CAPELLI) 
  REFERENCES ANAG_USR.CONF_CAPELLI_CI (ID)
  ENABLE VALIDATE,
  CONSTRAINT ID_OCCHI_FK 
  FOREIGN KEY (ID_OCCHI) 
  REFERENCES ANAG_USR.CONF_OCCHI_CI (ID)
  ENABLE VALIDATE,
  CONSTRAINT ID_UTENTE_FK1 
  FOREIGN KEY (ID_UTENTE) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE,
  CONSTRAINT MODALITA_RILASCIO_CIE_FK 
  FOREIGN KEY (ID_MODALITA_RILASCIO_CIE) 
  REFERENCES ANAG_USR.CONF_MODALITA_RILASCIO_CIE (ID_CONF_MODALITA_RILASCIO_CIE)
  ENABLE VALIDATE,
  CONSTRAINT MODALITA_RILASCIO_CI_FK1 
  FOREIGN KEY (ID_MODALITA_RILASCIO_CI) 
  REFERENCES ANAG_USR.CONF_MODALITA_RILASCIO_CI (ID_CONF_MODALITA_RILASCIO_CI)
  ENABLE VALIDATE,
  CONSTRAINT MOTIVO_ANNULLAMENTO_FK1 
  FOREIGN KEY (ID_MOTIVO_ANNULLAMENTO) 
  REFERENCES ANAG_USR.CONF_MOTIVO_ANNULLAMENTO_CARTA (ID_MOTIVO_ANNULLAMENTO_CARTA)
  ENABLE VALIDATE,
  CONSTRAINT MOTIVO_ANN_REV_CIE_FK 
  FOREIGN KEY (ID_MOTIVO_ANN_REV_CIE) 
  REFERENCES ANAG_USR.CONF_MOTIVO_ANNULL_REVOCA_CIE (ID_MOTIVO_ANN_REV_CIE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CENSIMENTO
(
  ID_CENSIMENTO          NUMBER                 NOT NULL,
  ANNO_CENSIMENTO        NUMBER(4)              NOT NULL,
  SEZIONE_CENSIMENTO     VARCHAR2(30 BYTE)      NOT NULL,
  FOGLIO_CENSIMENTO      VARCHAR2(30 BYTE)      NOT NULL,
  DATA_REGOLARIZZAZIONE  DATE,
  MOTIVO_COMPILAZIONE    VARCHAR2(240 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CENSIMENTO IS 'La tabella contiene gli estremi di un censimento.';

COMMENT ON COLUMN ANAG_USR.CENSIMENTO.ID_CENSIMENTO IS 'Identificativo del censimento associato al soggetto';

COMMENT ON COLUMN ANAG_USR.CENSIMENTO.ANNO_CENSIMENTO IS 'Anno in cui è avvenuto il censimento.';

COMMENT ON COLUMN ANAG_USR.CENSIMENTO.SEZIONE_CENSIMENTO IS 'Sezione del censimento';

COMMENT ON COLUMN ANAG_USR.CENSIMENTO.FOGLIO_CENSIMENTO IS 'Numero del foglio di censimento.';

COMMENT ON COLUMN ANAG_USR.CENSIMENTO.DATA_REGOLARIZZAZIONE IS 'Data nella quale il cittadino regolarizza la propria posizione in caso di mancata compilazione del questionario.';

COMMENT ON COLUMN ANAG_USR.CENSIMENTO.MOTIVO_COMPILAZIONE IS 'Motivo della mancata compilazione in formato di testo.';



CREATE UNIQUE INDEX ANAG_USR.CENSIMENTO_PK ON ANAG_USR.CENSIMENTO
(ID_CENSIMENTO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.CENSIMENTO__UN ON ANAG_USR.CENSIMENTO
(ANNO_CENSIMENTO, SEZIONE_CENSIMENTO, FOGLIO_CENSIMENTO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CENSIMENTO ADD (
  CONSTRAINT CENSIMENTO_PK
  PRIMARY KEY
  (ID_CENSIMENTO)
  USING INDEX ANAG_USR.CENSIMENTO_PK
  ENABLE VALIDATE,
  CONSTRAINT CENSIMENTO__UN
  UNIQUE (ANNO_CENSIMENTO, SEZIONE_CENSIMENTO, FOGLIO_CENSIMENTO)
  USING INDEX ANAG_USR.CENSIMENTO__UN
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CERTIFICATI
(
  ID_CERTIFICATO          NUMBER                NOT NULL,
  ID_PRATICA_CERTIFICATI  NUMBER,
  COD_TIPO_PROTOCOLLO     VARCHAR2(10 CHAR),
  ANNO_PROTOCOLLO         NUMBER,
  NUMERO_PROTOCOLLO       NUMBER,
  DATA_RICHIESTA          DATE,
  DATA_EMISSIONE          DATE,
  NOME_FILE_CERTIFICATO   VARCHAR2(200 CHAR),
  FLG_PAGAMENTO           CHAR(1 CHAR),
  DATA_PAGAMENTO          DATE,
  ID_SOGGETTO_INT         NUMBER,
  ID_CONF_CERTIFICATO     NUMBER,
  DOCUMENTO_CERTIFICATO   BLOB,
  FLG_SEMPLICE_BOLLATA    CHAR(1 BYTE),
  ID_ESENZIONE            NUMBER
)
LOB (DOCUMENTO_CERTIFICATO) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CERTIFICATI IS 'La tabella contiene le richieste di certificazione effettuate da un soggetto ed emesse da Roma Capitale.';

COMMENT ON COLUMN ANAG_USR.CERTIFICATI.ID_CERTIFICATO IS 'Identificativo del certificato';

COMMENT ON COLUMN ANAG_USR.CERTIFICATI.ID_PRATICA_CERTIFICATI IS 'Identificativo della pratica a cui questo certificato fa riferimento';

COMMENT ON COLUMN ANAG_USR.CERTIFICATI.COD_TIPO_PROTOCOLLO IS 'Codice del protocollo relativo alla richiesta di un certificato';

COMMENT ON COLUMN ANAG_USR.CERTIFICATI.ANNO_PROTOCOLLO IS 'Anno del protocollo relativo alla richiesta di un certificato';

COMMENT ON COLUMN ANAG_USR.CERTIFICATI.NUMERO_PROTOCOLLO IS 'Numero del protocollo relativo alla richiesta di un certificato';

COMMENT ON COLUMN ANAG_USR.CERTIFICATI.DATA_RICHIESTA IS 'Data di richiesta del certificato';

COMMENT ON COLUMN ANAG_USR.CERTIFICATI.DATA_EMISSIONE IS 'Data di emissione del certificato.';

COMMENT ON COLUMN ANAG_USR.CERTIFICATI.NOME_FILE_CERTIFICATO IS 'Rappresenta il nome del file del certificato emesso.';

COMMENT ON COLUMN ANAG_USR.CERTIFICATI.FLG_PAGAMENTO IS 'S -> Pagamento effettuato
N -> Pagamento da effettuare
G -> Certificato Gratuito';

COMMENT ON COLUMN ANAG_USR.CERTIFICATI.DATA_PAGAMENTO IS 'Data di avvenuto pagamento';

COMMENT ON COLUMN ANAG_USR.CERTIFICATI.ID_SOGGETTO_INT IS 'Id dell''intestatario del certificato.';

COMMENT ON COLUMN ANAG_USR.CERTIFICATI.ID_CONF_CERTIFICATO IS 'identificativo delle conf_certificato';

COMMENT ON COLUMN ANAG_USR.CERTIFICATI.DOCUMENTO_CERTIFICATO IS 'File del certificato';

COMMENT ON COLUMN ANAG_USR.CERTIFICATI.FLG_SEMPLICE_BOLLATA IS 'S->semplice, B-> bollata';

COMMENT ON COLUMN ANAG_USR.CERTIFICATI.ID_ESENZIONE IS 'Identificato dell''esenzione';



CREATE UNIQUE INDEX ANAG_USR.CERTIFICATI_PK ON ANAG_USR.CERTIFICATI
(ID_CERTIFICATO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CERTIFICATI ADD (
  CONSTRAINT CERTIFICATI_PK
  PRIMARY KEY
  (ID_CERTIFICATO)
  USING INDEX ANAG_USR.CERTIFICATI_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CERTIFICATI ADD (
  CONSTRAINT CONF_TIPO_PROTOCOLLO_FK3 
  FOREIGN KEY (COD_TIPO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE,
  CONSTRAINT ID_CONF_CERTIFICATO 
  FOREIGN KEY (ID_CONF_CERTIFICATO) 
  REFERENCES ANAG_USR.CONF_CERTIFICATO (ID_CONF_CERTIFICATO)
  ENABLE VALIDATE,
  CONSTRAINT ID_ESENZIONE_FK 
  FOREIGN KEY (ID_ESENZIONE) 
  REFERENCES ANAG_USR.CONF_ESENZIONE_CERTIFICATO (ID_ESENZIONE)
  ENABLE VALIDATE,
  CONSTRAINT ID_PRATICA_CERTIFICATI_FK 
  FOREIGN KEY (ID_PRATICA_CERTIFICATI) 
  REFERENCES ANAG_USR.PRATICA_CERTIFICATI (ID_PRATICA_CERTIFICATI)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_INT_FK 
  FOREIGN KEY (ID_SOGGETTO_INT) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CITTADINANZA
(
  ID_CITTADINANZA    NUMBER                     NOT NULL,
  DESCRIZIONE_STATO  VARCHAR2(250 BYTE),
  CODICE_STATO       NUMBER(3)                  NOT NULL,
  NOTE               VARCHAR2(250 BYTE),
  COMUNITARIO        CHAR(1 BYTE)               NOT NULL,
  SIGLA_NAZIONE      VARCHAR2(3 BYTE),
  CODICE_ISO3166     VARCHAR2(3 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CITTADINANZA IS 'La tabella contiene le informazioni sulla cittadinanza di un soggetto.';

COMMENT ON COLUMN ANAG_USR.CITTADINANZA.ID_CITTADINANZA IS 'Campo che  identifica univocamente la cittadinanza.';

COMMENT ON COLUMN ANAG_USR.CITTADINANZA.DESCRIZIONE_STATO IS 'Campo che indica la denominazione dello Stato.';

COMMENT ON COLUMN ANAG_USR.CITTADINANZA.CODICE_STATO IS 'Codice numerico identificativo dello Stato.';

COMMENT ON COLUMN ANAG_USR.CITTADINANZA.NOTE IS 'Campo in cui è possibile inserire delle note riguardanti la cittadinanza.';

COMMENT ON COLUMN ANAG_USR.CITTADINANZA.COMUNITARIO IS 'Flag che indica se lo Stato a cui è assiciata la cittadinanza fa parte dell''Unione Europea.

 Avrà valore 1 se lo stato è comunitario, 0 altrimenti.';

COMMENT ON COLUMN ANAG_USR.CITTADINANZA.CODICE_ISO3166 IS 'Codice ISO3166 di tre caratteri identificativi dello stato.';



CREATE UNIQUE INDEX ANAG_USR.CITTADINANZA_PK ON ANAG_USR.CITTADINANZA
(ID_CITTADINANZA)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.CITTADINANZA__UN ON ANAG_USR.CITTADINANZA
(CODICE_STATO, DESCRIZIONE_STATO, NOTE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CITTADINANZA FOR ANAG_USR.CITTADINANZA;


ALTER TABLE ANAG_USR.CITTADINANZA ADD (
  CONSTRAINT CITTADINANZA_PK
  PRIMARY KEY
  (ID_CITTADINANZA)
  USING INDEX ANAG_USR.CITTADINANZA_PK
  ENABLE VALIDATE,
  CONSTRAINT CITTADINANZA__UN
  UNIQUE (CODICE_STATO, DESCRIZIONE_STATO, NOTE)
  USING INDEX ANAG_USR.CITTADINANZA__UN
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CIVICO
(
  ID_CIVICO      NUMBER                         NOT NULL,
  CODICE_CIVICO  VARCHAR2(10 BYTE),
  CIVICO_FONTE   NUMBER(1),
  NUMERO         NUMBER(20),
  METRICO        NUMBER(6),
  PROG_SNC       NUMBER(5),
  LETTERA        VARCHAR2(10 BYTE),
  ESPONENTE      VARCHAR2(20 BYTE),
  COLORE         NUMBER(1),
  COD_TOPONIMO   VARCHAR2(6 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CIVICO IS 'La tabella contiene le informazioni relative ai numeri civici.';

COMMENT ON COLUMN ANAG_USR.CIVICO.ID_CIVICO IS 'Campo che indica il codice identificatvo del civico.';

COMMENT ON COLUMN ANAG_USR.CIVICO.CODICE_CIVICO IS 'Campo che indica il codice identificatvo attribuito al numero civico nella banca dati comunale/nazionale.';

COMMENT ON COLUMN ANAG_USR.CIVICO.CIVICO_FONTE IS 'Campo che indica il la provenienza del codice civico.
Vale 1 se ricavato dalla tabella nazionale, 2 se ricavato dalla tabella comunale.';

COMMENT ON COLUMN ANAG_USR.CIVICO.NUMERO IS 'Campo che indica il numero del civico.';

COMMENT ON COLUMN ANAG_USR.CIVICO.METRICO IS 'Campo che indica la distanza tra l''accesso e il punto di riferimento prestabilito, espresso in metri.';

COMMENT ON COLUMN ANAG_USR.CIVICO.PROG_SNC IS 'Campo che indica il progressivo dopo l''ultimo civico presente.';

COMMENT ON COLUMN ANAG_USR.CIVICO.LETTERA IS 'Campo che indica la lettera del civico.';

COMMENT ON COLUMN ANAG_USR.CIVICO.ESPONENTE IS 'Campo che indica l''esponente del civico.';

COMMENT ON COLUMN ANAG_USR.CIVICO.COLORE IS 'Campo che indica il colore del civico.';

COMMENT ON COLUMN ANAG_USR.CIVICO.COD_TOPONIMO IS 'identificativo che indica il toponimo al quale il civico è associato';



CREATE UNIQUE INDEX ANAG_USR.CIVICO_PK ON ANAG_USR.CIVICO
(ID_CIVICO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CIVICO_SIN FOR ANAG_USR.CIVICO;


ALTER TABLE ANAG_USR.CIVICO ADD (
  CONSTRAINT CIVICO_PK
  PRIMARY KEY
  (ID_CIVICO)
  USING INDEX ANAG_USR.CIVICO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CIVICO_INTERNO
(
  ID_CIVICO_INTERNO    NUMBER                   NOT NULL,
  CORTE                VARCHAR2(4 BYTE),
  SCALA                VARCHAR2(4 BYTE),
  INTENRO1             VARCHAR2(4 BYTE),
  ESP_INTERNO1         VARCHAR2(20 BYTE),
  INTERNO2             VARCHAR2(4 BYTE),
  ESP_INTERNO2         VARCHAR2(20 BYTE),
  SCALA_ESTERNA        VARCHAR2(10 BYTE),
  SECONDARIO           CHAR(1 BYTE),
  PIANO                VARCHAR2(5 BYTE),
  NUI                  VARCHAR2(3 BYTE),
  ISOLATO              VARCHAR2(10 BYTE),
  FLG_PALAZZINA_UNICA  VARCHAR2(1 BYTE),
  LOTTO                VARCHAR2(20 BYTE),
  PALAZZINA            VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CIVICO_INTERNO IS 'La tabella contiene le informazioni relative ai numeri civici interni.';

COMMENT ON COLUMN ANAG_USR.CIVICO_INTERNO.ID_CIVICO_INTERNO IS 'Campo che indica il codice identificatvo del civico interno.';

COMMENT ON COLUMN ANAG_USR.CIVICO_INTERNO.CORTE IS 'Campo che indica la corte del civico interno.';

COMMENT ON COLUMN ANAG_USR.CIVICO_INTERNO.SCALA IS 'Campo che indica la scala del civico interno.';

COMMENT ON COLUMN ANAG_USR.CIVICO_INTERNO.INTENRO1 IS 'Campo che indica l''interno del civico interno.';

COMMENT ON COLUMN ANAG_USR.CIVICO_INTERNO.ESP_INTERNO1 IS 'Campo che indica l''esponente del civico interno.';

COMMENT ON COLUMN ANAG_USR.CIVICO_INTERNO.INTERNO2 IS 'Campo che indica il secondo interno del civico interno.';

COMMENT ON COLUMN ANAG_USR.CIVICO_INTERNO.ESP_INTERNO2 IS 'Campo che indica l''esponente del secondo interno del civico interno.';

COMMENT ON COLUMN ANAG_USR.CIVICO_INTERNO.SCALA_ESTERNA IS 'Campo che indica la scala esterna del civico interno.';

COMMENT ON COLUMN ANAG_USR.CIVICO_INTERNO.SECONDARIO IS 'Lettera che indica il numero secondario del civico interno.';

COMMENT ON COLUMN ANAG_USR.CIVICO_INTERNO.PIANO IS 'Campo che indica il piano del civico interno.';

COMMENT ON COLUMN ANAG_USR.CIVICO_INTERNO.NUI IS 'Campo che indica il numero dell''unità immobiliare del civico interno.';

COMMENT ON COLUMN ANAG_USR.CIVICO_INTERNO.ISOLATO IS 'Campo che indica il numero dell''isolato del civico interno.';

COMMENT ON COLUMN ANAG_USR.CIVICO_INTERNO.FLG_PALAZZINA_UNICA IS 'S - Palazzina Unica; N o null altrimenti
';



CREATE UNIQUE INDEX ANAG_USR.CIVICOINTERNO_PK ON ANAG_USR.CIVICO_INTERNO
(ID_CIVICO_INTERNO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CIVICO_INTERNO_SIN FOR ANAG_USR.CIVICO_INTERNO;


ALTER TABLE ANAG_USR.CIVICO_INTERNO ADD (
  CONSTRAINT CIVICOINTERNO_PK
  PRIMARY KEY
  (ID_CIVICO_INTERNO)
  USING INDEX ANAG_USR.CIVICOINTERNO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.COMUNE
(
  ID_COMUNE             NUMBER                  NOT NULL,
  NOME_COMUNE           VARCHAR2(80 BYTE)       DEFAULT '',
  ISTAT_COMUNE          VARCHAR2(6 BYTE),
  DESCRIZIONE_LOCALITA  VARCHAR2(120 BYTE),
  ID_PROVINCIA          NUMBER,
  DATA_ISTITUZIONE      DATE,
  DATA_CESSAZIONE       DATE,
  ALTRA_DENOMINAZIONE   VARCHAR2(80 BYTE),
  FLAG_SUBENTRATO       VARCHAR2(1 BYTE)        DEFAULT 'N',
  E_MAIL                VARCHAR2(80 BYTE),
  CODICE_AGGIOR         VARCHAR2(5 BYTE),
  CODICE_CATASTALE      VARCHAR2(4 BYTE),
  CAP_GENERALE          VARCHAR2(5 CHAR)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.COMUNE IS 'La tabella contiene l''anagrafica dei comuni italiani.';

COMMENT ON COLUMN ANAG_USR.COMUNE.ID_COMUNE IS 'Identificativo univoco del comune.';

COMMENT ON COLUMN ANAG_USR.COMUNE.NOME_COMUNE IS 'Campo che indica il nome del comune.';

COMMENT ON COLUMN ANAG_USR.COMUNE.ISTAT_COMUNE IS 'Campo che indica il codice ISTAT del comune';

COMMENT ON COLUMN ANAG_USR.COMUNE.DESCRIZIONE_LOCALITA IS 'Campo che indica la descrizione della localita.Non deve essere indicato se coincide con il comune.';

COMMENT ON COLUMN ANAG_USR.COMUNE.ID_PROVINCIA IS 'Identificativo della provincia in cui si trova il comune.';

COMMENT ON COLUMN ANAG_USR.COMUNE.DATA_ISTITUZIONE IS 'Campo che indica la data di istituzione del comune.';

COMMENT ON COLUMN ANAG_USR.COMUNE.DATA_CESSAZIONE IS 'Campo che indica la data di cessazione del comune.';

COMMENT ON COLUMN ANAG_USR.COMUNE.ALTRA_DENOMINAZIONE IS 'Campo che indica un''altra denominazione del comune.';

COMMENT ON COLUMN ANAG_USR.COMUNE.FLAG_SUBENTRATO IS 'S il comune è subentrato in ANPR, N viceversa';

COMMENT ON COLUMN ANAG_USR.COMUNE.E_MAIL IS 'E-mail a cui inviare le comunicazioni';

COMMENT ON COLUMN ANAG_USR.COMUNE.CODICE_AGGIOR IS 'Identificativo AGGIOR';

COMMENT ON COLUMN ANAG_USR.COMUNE.CODICE_CATASTALE IS 'Codice (Belfiore o nazionale) del comune';

COMMENT ON COLUMN ANAG_USR.COMUNE.CAP_GENERALE IS 'CAP generale del comune (es. Roma 00100)';



CREATE UNIQUE INDEX ANAG_USR.COMUNE_PK ON ANAG_USR.COMUNE
(ID_COMUNE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.COMUNE__UN ON ANAG_USR.COMUNE
(NOME_COMUNE, ISTAT_COMUNE, ID_COMUNE, DESCRIZIONE_LOCALITA)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.COMUNE FOR ANAG_USR.COMUNE;


ALTER TABLE ANAG_USR.COMUNE ADD (
  CONSTRAINT COMUNE_PK
  PRIMARY KEY
  (ID_COMUNE)
  USING INDEX ANAG_USR.COMUNE_PK
  ENABLE VALIDATE,
  CONSTRAINT COMUNE__UN
  UNIQUE (NOME_COMUNE, ISTAT_COMUNE, ID_COMUNE, DESCRIZIONE_LOCALITA)
  USING INDEX ANAG_USR.COMUNE__UN
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.COMUNE ADD (
  CONSTRAINT COMUNE_PROVINCIA_FK 
  FOREIGN KEY (ID_PROVINCIA) 
  REFERENCES ANAG_USR.PROVINCIA (ID_PROVINCIA)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.COMUNICAZIONI
(
  ID                      NUMBER                NOT NULL,
  DATA_COMUNICAZIONE      DATE                  NOT NULL,
  OGGETTO                 VARCHAR2(100 CHAR)    NOT NULL,
  TESTO                   VARCHAR2(4000 CHAR)   NOT NULL,
  MITTENTE_COMUNICAZIONE  VARCHAR2(50 CHAR)     NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.COMUNICAZIONI IS 'Tabella che contiene le comunicazioni inserite a sistema per notificare ad un utente un determinato evento.';

COMMENT ON COLUMN ANAG_USR.COMUNICAZIONI.ID IS 'Identificativo della comunicazione';

COMMENT ON COLUMN ANAG_USR.COMUNICAZIONI.DATA_COMUNICAZIONE IS 'Data di inserimento della comunicazione';

COMMENT ON COLUMN ANAG_USR.COMUNICAZIONI.OGGETTO IS 'Oggetto della comunicazione.';

COMMENT ON COLUMN ANAG_USR.COMUNICAZIONI.TESTO IS 'Testo della comunicazione';

COMMENT ON COLUMN ANAG_USR.COMUNICAZIONI.MITTENTE_COMUNICAZIONE IS 'Identifica il mittente della comunicazione';



CREATE UNIQUE INDEX ANAG_USR.COMUNICAZIONI_PK ON ANAG_USR.COMUNICAZIONI
(ID)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.COMUNICAZIONI ADD (
  CONSTRAINT COMUNICAZIONI_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.COMUNICAZIONI_PK
  ENABLE VALIDATE);

GRANT DELETE, INSERT, SELECT, UPDATE ON ANAG_USR.COMUNICAZIONI TO MATR_USR;
CREATE TABLE ANAG_USR.CONF_AMBITO
(
  ID_AMBITO    NUMBER                           NOT NULL,
  DESCRIZIONE  VARCHAR2(20 CHAR)                NOT NULL
)
TABLESPACE SYSTEM
RESULT_CACHE (MODE DEFAULT)
PCTUSED    40
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_AMBITO_PK ON ANAG_USR.CONF_AMBITO
(ID_AMBITO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_AMBITO ADD (
  CONSTRAINT CONF_AMBITO_PK
  PRIMARY KEY
  (ID_AMBITO)
  USING INDEX ANAG_USR.CONF_AMBITO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_AREE_TEMATICHE
(
  ID_AREE_TEMATICHE  NUMBER                     NOT NULL,
  DESCRIZIONE        VARCHAR2(50 CHAR)          NOT NULL,
  ID_AMBITO          NUMBER,
  URL_PAGE           VARCHAR2(400 BYTE),
  ORDINE             NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_AREE_TEMATICHE IS 'Tabella tipologica che contiene le varie aree tematiche assimilabili ai vari casi d''uso implementati dal sistema.';

COMMENT ON COLUMN ANAG_USR.CONF_AREE_TEMATICHE.ID_AREE_TEMATICHE IS 'Identificativo dell''area tematica.';

COMMENT ON COLUMN ANAG_USR.CONF_AREE_TEMATICHE.DESCRIZIONE IS 'Descrizione dell''area tematica.';

COMMENT ON COLUMN ANAG_USR.CONF_AREE_TEMATICHE.URL_PAGE IS 'Url della pagina associata all''area tematica';



CREATE UNIQUE INDEX ANAG_USR.CONF_AREE_TEMATICHE_PK ON ANAG_USR.CONF_AREE_TEMATICHE
(ID_AREE_TEMATICHE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CONF_AREE_TEMATICHE FOR ANAG_USR.CONF_AREE_TEMATICHE;


ALTER TABLE ANAG_USR.CONF_AREE_TEMATICHE ADD (
  CONSTRAINT CONF_AREE_TEMATICHE_PK
  PRIMARY KEY
  (ID_AREE_TEMATICHE)
  USING INDEX ANAG_USR.CONF_AREE_TEMATICHE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONF_AREE_TEMATICHE ADD (
  CONSTRAINT ID_AMBITO_FK 
  FOREIGN KEY (ID_AMBITO) 
  REFERENCES ANAG_USR.CONF_AMBITO (ID_AMBITO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_CATEGORIA_PENSIONE
(
  ID_CATEGORIA  VARCHAR2(20 BYTE)               NOT NULL,
  DESCRIZIONE   VARCHAR2(50 BYTE)
)
TABLESPACE SYSTEM
RESULT_CACHE (MODE DEFAULT)
PCTUSED    40
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_CATEGORIA_PENSIONE_PK ON ANAG_USR.CONF_CATEGORIA_PENSIONE
(ID_CATEGORIA)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_CATEGORIA_PENSIONE ADD (
  CONSTRAINT CONF_CATEGORIA_PENSIONE_PK
  PRIMARY KEY
  (ID_CATEGORIA)
  USING INDEX ANAG_USR.CONF_CATEGORIA_PENSIONE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_CERTIFICABILITA
(
  ID_CERTIFICABILITA  NUMBER                    NOT NULL,
  DESCRIZIONE         VARCHAR2(250 CHAR)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_CERTIFICABILITA IS 'Tipologica che contiene le condizioni di certificabilità.';

COMMENT ON COLUMN ANAG_USR.CONF_CERTIFICABILITA.ID_CERTIFICABILITA IS 'Codice identificativo della tipologia di certificabilità che è possibile emettere ad un soggetto.';

COMMENT ON COLUMN ANAG_USR.CONF_CERTIFICABILITA.DESCRIZIONE IS 'Descrizione della tipologia di certificabilità che è possibile emettere ad un soggetto.';



CREATE UNIQUE INDEX ANAG_USR.CONF_CERTIFICABILITA_PK ON ANAG_USR.CONF_CERTIFICABILITA
(ID_CERTIFICABILITA)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_CERTIFICABILITA ADD (
  CONSTRAINT CONF_CERTIFICABILITA_PK
  PRIMARY KEY
  (ID_CERTIFICABILITA)
  USING INDEX ANAG_USR.CONF_CERTIFICABILITA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_CODICE_LEGAME
(
  ID_CODICE_LEGAME        NUMBER(2)             NOT NULL,
  ID_CODICE_LEGAME_ANPR   NUMBER(2)             NOT NULL,
  DESCRIZIONE             VARCHAR2(80 BYTE)     NOT NULL,
  ID_TIPO_LEGAME          NUMBER(2)             NOT NULL,
  ID_MOTIVO_COSTITUZIONE  NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_CODICE_LEGAME IS 'Tabella tipologica che contiene l''elenco dei legami di parentela che sussistono tra soggetti';

COMMENT ON COLUMN ANAG_USR.CONF_CODICE_LEGAME.ID_CODICE_LEGAME IS 'Il codice del legame del soggetto con la famiglia o con la convivenza.';

COMMENT ON COLUMN ANAG_USR.CONF_CODICE_LEGAME.ID_CODICE_LEGAME_ANPR IS 'Il codicedel legame del soggetto con la famiglia o con la convivenza utilizzato da ANPR.';

COMMENT ON COLUMN ANAG_USR.CONF_CODICE_LEGAME.DESCRIZIONE IS 'Descizione del  legame del soggetto con la famiglia o con la convivenza';

COMMENT ON COLUMN ANAG_USR.CONF_CODICE_LEGAME.ID_TIPO_LEGAME IS 'Codice identificavo della tipologia di legame. ';

COMMENT ON COLUMN ANAG_USR.CONF_CODICE_LEGAME.ID_MOTIVO_COSTITUZIONE IS 'Identificativo del motivo di costituzione associato al codice legame';



CREATE UNIQUE INDEX ANAG_USR.CODICE_LEGAME_PK ON ANAG_USR.CONF_CODICE_LEGAME
(ID_CODICE_LEGAME)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_CODICE_LEGAME ADD (
  CONSTRAINT CODICE_LEGAME_PK
  PRIMARY KEY
  (ID_CODICE_LEGAME)
  USING INDEX ANAG_USR.CODICE_LEGAME_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONF_CODICE_LEGAME ADD (
  CONSTRAINT CONF_MOTIVO_COSTITUZIONE_FL 
  FOREIGN KEY (ID_MOTIVO_COSTITUZIONE) 
  REFERENCES ANAG_USR.CONF_MOTIVO_COSTITUZIONE (ID_MOTIVO_COSTITUZIONE)
  ENABLE VALIDATE,
  CONSTRAINT CONF_TIPO_LEGAME_FK 
  FOREIGN KEY (ID_TIPO_LEGAME) 
  REFERENCES ANAG_USR.CONF_TIPO_LEGAME (ID_TIPO_LEGAME)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_COND_NON_PROFESSIONALE
(
  ID_COND_NON_PROFESSIONALE_ANPR  NUMBER(2)     NOT NULL,
  ID_POS_PROFESSIONALE_APR        NUMBER(2),
  DESCRIZIONE                     VARCHAR2(250 CHAR) NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_COND_NON_PROFESSIONALE IS 'Tabella tipologica che contiene l''elenco delle condizioni non professionali';

COMMENT ON COLUMN ANAG_USR.CONF_COND_NON_PROFESSIONALE.ID_COND_NON_PROFESSIONALE_ANPR IS 'codice identificativo della condizione non professionale usato in ANPR.';

COMMENT ON COLUMN ANAG_USR.CONF_COND_NON_PROFESSIONALE.ID_POS_PROFESSIONALE_APR IS 'Codice identificativo della condizione non professionale usato in APR.';

COMMENT ON COLUMN ANAG_USR.CONF_COND_NON_PROFESSIONALE.DESCRIZIONE IS 'Descrizione della condizione non professionale.';



CREATE UNIQUE INDEX ANAG_USR.COND_NON_PROFESSIONALE_PK ON ANAG_USR.CONF_COND_NON_PROFESSIONALE
(ID_COND_NON_PROFESSIONALE_ANPR)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_COND_NON_PROFESSIONALE ADD (
  CONSTRAINT COND_NON_PROFESSIONALE_PK
  PRIMARY KEY
  (ID_COND_NON_PROFESSIONALE_ANPR)
  USING INDEX ANAG_USR.COND_NON_PROFESSIONALE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_ENTE_RILASCIO_PATENTE
(
  ID_ENTE_RILASCIO_PATENTE  NUMBER(2)           NOT NULL,
  DESCRIZIONE               VARCHAR2(50 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_ENTE_RILASCIO_PATENTE IS 'Tabella tipologica che contiene l''elenco degli enti abilitati al rilascio della patente di guida.';

COMMENT ON COLUMN ANAG_USR.CONF_ENTE_RILASCIO_PATENTE.ID_ENTE_RILASCIO_PATENTE IS 'Identificatio dell''ente di rilascio patenti';

COMMENT ON COLUMN ANAG_USR.CONF_ENTE_RILASCIO_PATENTE.DESCRIZIONE IS 'descrizione dell''entedi rilascio patenti';



CREATE UNIQUE INDEX ANAG_USR.CONF_ENTE_RILASCIO_PATENTE_PK ON ANAG_USR.CONF_ENTE_RILASCIO_PATENTE
(ID_ENTE_RILASCIO_PATENTE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_ENTE_RILASCIO_PATENTE ADD (
  CONSTRAINT CONF_ENTE_RILASCIO_PATENTE_PK
  PRIMARY KEY
  (ID_ENTE_RILASCIO_PATENTE)
  USING INDEX ANAG_USR.CONF_ENTE_RILASCIO_PATENTE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_ENTE_RILASCIO_PENSIONE
(
  ID_ENTE_RILASCIO_PENSIONE  NUMBER(2)          NOT NULL,
  DESCRIZIONE                VARCHAR2(20 CHAR)
)
TABLESPACE SYSTEM
RESULT_CACHE (MODE DEFAULT)
PCTUSED    40
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_ENTE_RILASCIO_PENSION_PK ON ANAG_USR.CONF_ENTE_RILASCIO_PENSIONE
(ID_ENTE_RILASCIO_PENSIONE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_ENTE_RILASCIO_PENSIONE ADD (
  CONSTRAINT CONF_ENTE_RILASCIO_PENSION_PK
  PRIMARY KEY
  (ID_ENTE_RILASCIO_PENSIONE)
  USING INDEX ANAG_USR.CONF_ENTE_RILASCIO_PENSION_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_ESITO_DIC_CONVIVENZA
(
  ID           NUMBER                           NOT NULL,
  DESCRIZIONE  VARCHAR2(50 CHAR)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_ESITO_DIC_CONVIVENZA IS 'Tabella tipologica che contiene l''elenco degli esiti possibili per una dichiarazione di convivenza';

COMMENT ON COLUMN ANAG_USR.CONF_ESITO_DIC_CONVIVENZA.ID IS 'Identificativo dell''esito della dichiarazione di convivenza';

COMMENT ON COLUMN ANAG_USR.CONF_ESITO_DIC_CONVIVENZA.DESCRIZIONE IS 'Descrizione dell''esito della dichiarazione di convivenza';



CREATE UNIQUE INDEX ANAG_USR.CONF_ESITO_DIC_CONVIVENZA_PK ON ANAG_USR.CONF_ESITO_DIC_CONVIVENZA
(ID)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_ESITO_DIC_CONVIVENZA ADD (
  CONSTRAINT CONF_ESITO_DIC_CONVIVENZA_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_ESITO_DIC_CONVIVENZA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_FUNZIONALITA
(
  ID                NUMBER                      NOT NULL,
  DESCRIZIONE       VARCHAR2(50 CHAR)           NOT NULL,
  ID_AREA_TEMATICA  NUMBER                      NOT NULL,
  URL_PAGE          VARCHAR2(400 BYTE)          NOT NULL,
  ORDINE            NUMBER                      NOT NULL,
  CITTADINO         NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_FUNZIONALITA IS 'Tabella tipologica che contiene le varie funzionalità associate ad una specifica area tematica.';

COMMENT ON COLUMN ANAG_USR.CONF_FUNZIONALITA.ID IS 'Identificativo univoco della funzionalità';

COMMENT ON COLUMN ANAG_USR.CONF_FUNZIONALITA.DESCRIZIONE IS 'Descrizione della funzionalità';

COMMENT ON COLUMN ANAG_USR.CONF_FUNZIONALITA.ID_AREA_TEMATICA IS 'Identificativo dell''area tematica a cui la funzionalità è associata.';

COMMENT ON COLUMN ANAG_USR.CONF_FUNZIONALITA.URL_PAGE IS 'Url della pagina associata alla funzionalita';

COMMENT ON COLUMN ANAG_USR.CONF_FUNZIONALITA.CITTADINO IS '1- Funzionalità per cittadino non professionista. 0- Funzionalità per cittadino professionista o dipendente';



CREATE UNIQUE INDEX ANAG_USR.CONF_FUNZIONALITA_PK ON ANAG_USR.CONF_FUNZIONALITA
(ID)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_FUNZIONALITA ADD (
  CONSTRAINT CONF_FUNZIONALITA_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_FUNZIONALITA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONF_FUNZIONALITA ADD (
  CONSTRAINT FUNZ_AREE_TEMATICHE_FK 
  FOREIGN KEY (ID_AREA_TEMATICA) 
  REFERENCES ANAG_USR.CONF_AREE_TEMATICHE (ID_AREE_TEMATICHE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_IMPORTI_DOVUTI
(
  ID            NUMBER                          NOT NULL,
  DESCRIZIONE   VARCHAR2(200 CHAR),
  IMPORTO       NUMBER(11,2),
  RATE          NUMBER,
  CODICE_CNC    VARCHAR2(10 CHAR),
  ID_POSIZIONE  NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_IMPORTI_DOVUTI IS 'Tabella tipologica che contiene l''elenco degli importi dovuti per ciascun certificato.';

COMMENT ON COLUMN ANAG_USR.CONF_IMPORTI_DOVUTI.ID IS 'Identificativo dell''importo';

COMMENT ON COLUMN ANAG_USR.CONF_IMPORTI_DOVUTI.DESCRIZIONE IS 'Descrizione dell''importo dovuto.';

COMMENT ON COLUMN ANAG_USR.CONF_IMPORTI_DOVUTI.IMPORTO IS 'Importo economico dovuto.';

COMMENT ON COLUMN ANAG_USR.CONF_IMPORTI_DOVUTI.RATE IS '80 - Rata Intera';

COMMENT ON COLUMN ANAG_USR.CONF_IMPORTI_DOVUTI.CODICE_CNC IS 'Codice utilizzato per l''integrazione SIR';

COMMENT ON COLUMN ANAG_USR.CONF_IMPORTI_DOVUTI.ID_POSIZIONE IS 'FK(CONF_POSIZIONI)';



CREATE UNIQUE INDEX ANAG_USR.CONF_IMPORTI_DOVUTI_PK ON ANAG_USR.CONF_IMPORTI_DOVUTI
(ID)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_IMPORTI_DOVUTI ADD (
  CONSTRAINT CONF_IMPORTI_DOVUTI_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_IMPORTI_DOVUTI_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONF_IMPORTI_DOVUTI ADD (
  CONSTRAINT CONF_IMPORTI_DOVUTI_FK1 
  FOREIGN KEY (ID_POSIZIONE) 
  REFERENCES ANAG_USR.CONF_POSIZIONI (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_MOTIVAZIONE_CHIUSURA
(
  ID           NUMBER                           NOT NULL,
  DESCRIZIONE  VARCHAR2(50 CHAR),
  ID_ANPR      NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_MOTIVAZIONE_CHIUSURA IS 'Tabella tipologica che contiene l''elenco delle motivazioni ammesse dal sistema per la chiusura di una dichiarazione di convivenza.';

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVAZIONE_CHIUSURA.ID IS 'Identificativo della motivazione di chiusura di una dichiarazione di convivenza';

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVAZIONE_CHIUSURA.DESCRIZIONE IS 'Descrizione della motivazione di chiusura di una dichiarazione di convivenza';

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVAZIONE_CHIUSURA.ID_ANPR IS 'id per operazione anpr';



CREATE UNIQUE INDEX ANAG_USR.CONF_MOTIVAZIONE_CHIUSURA_PK ON ANAG_USR.CONF_MOTIVAZIONE_CHIUSURA
(ID)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_MOTIVAZIONE_CHIUSURA ADD (
  CONSTRAINT CONF_MOTIVAZIONE_CHIUSURA_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_MOTIVAZIONE_CHIUSURA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_MOTIVO_ISCRIZIONE_APR
(
  ID_MOTIVO_ISCRIZIONE_APR  NUMBER(2)           NOT NULL,
  DESCRIZIONE               VARCHAR2(120 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_MOTIVO_ISCRIZIONE_APR IS 'Tabella tipologica che contiene l''elenco delle motivazioni ammesse per l''iscrizione nell''APR del Comune di Roma';

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_ISCRIZIONE_APR.ID_MOTIVO_ISCRIZIONE_APR IS 'Codice identificativo della motivazione per cui il soggetto è iscritto all''apr.';

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_ISCRIZIONE_APR.DESCRIZIONE IS 'Descrizione della motivazione per cui il soggetto è iscritto all''apr.
';



CREATE UNIQUE INDEX ANAG_USR.CONF_MOTIVO_ISCRIZIONE_APR_PK ON ANAG_USR.CONF_MOTIVO_ISCRIZIONE_APR
(ID_MOTIVO_ISCRIZIONE_APR)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_MOTIVO_ISCRIZIONE_APR ADD (
  CONSTRAINT CONF_MOTIVO_ISCRIZIONE_APR_PK
  PRIMARY KEY
  (ID_MOTIVO_ISCRIZIONE_APR)
  USING INDEX ANAG_USR.CONF_MOTIVO_ISCRIZIONE_APR_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_POSIZIONE_PROFESSIONALE
(
  ID_POS_PROFESSIONALE_ANPR  VARCHAR2(5 BYTE)   NOT NULL,
  ID_POS_PROFESSIONALE_APR   NUMBER(2),
  DESCRIZIONE                VARCHAR2(80 BYTE)  NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_POSIZIONE_PROFESSIONALE IS 'Tabella tipologica contenente l''elenco delle posizioni professionali gestite dal sistema.';

COMMENT ON COLUMN ANAG_USR.CONF_POSIZIONE_PROFESSIONALE.ID_POS_PROFESSIONALE_ANPR IS 'codice identificativo della posizione professionale usato in ANPR.';

COMMENT ON COLUMN ANAG_USR.CONF_POSIZIONE_PROFESSIONALE.ID_POS_PROFESSIONALE_APR IS 'Codice identificativo della posizione professionale usato in APR.';

COMMENT ON COLUMN ANAG_USR.CONF_POSIZIONE_PROFESSIONALE.DESCRIZIONE IS 'Descrizione della posizione professionale.';



CREATE UNIQUE INDEX ANAG_USR.POSIZIONE_PROFESSIONALE_PK ON ANAG_USR.CONF_POSIZIONE_PROFESSIONALE
(ID_POS_PROFESSIONALE_ANPR)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_POSIZIONE_PROFESSIONALE ADD (
  CONSTRAINT CONF_POSIZIONE_PROFESSIONA_PK
  PRIMARY KEY
  (ID_POS_PROFESSIONALE_ANPR)
  USING INDEX ANAG_USR.POSIZIONE_PROFESSIONALE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_RUOLI
(
  ID           NUMBER                           NOT NULL,
  DESCRIZIONE  VARCHAR2(50 CHAR)                NOT NULL,
  RUOLO        VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_RUOLI IS 'Tabella tipologica che contiene i vari Ruoli associabili ad un utente.';

COMMENT ON COLUMN ANAG_USR.CONF_RUOLI.ID IS 'Identificativo del ruolo.';

COMMENT ON COLUMN ANAG_USR.CONF_RUOLI.DESCRIZIONE IS 'Descrizione del Ruolo.';



CREATE UNIQUE INDEX ANAG_USR.CONF_RUOLI_PK ON ANAG_USR.CONF_RUOLI
(ID)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CONF_RUOLI FOR ANAG_USR.CONF_RUOLI;


ALTER TABLE ANAG_USR.CONF_RUOLI ADD (
  CONSTRAINT CONF_RUOLI_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_RUOLI_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_SCELTA_PATRIMONIALE
(
  ID           NUMBER                           NOT NULL,
  DESCRIZIONE  VARCHAR2(50 CHAR)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_SCELTA_PATRIMONIALE IS 'Tabella tipologica che contiene l''elenco delle possibili scelte di regime patrimoniale';

COMMENT ON COLUMN ANAG_USR.CONF_SCELTA_PATRIMONIALE.ID IS 'Identificativo della scelta patrimoniale';

COMMENT ON COLUMN ANAG_USR.CONF_SCELTA_PATRIMONIALE.DESCRIZIONE IS 'Descrizione della scelta patrimoniale';



CREATE UNIQUE INDEX ANAG_USR.CONF_SCELTA_PATRIMONIALE_PK ON ANAG_USR.CONF_SCELTA_PATRIMONIALE
(ID)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_SCELTA_PATRIMONIALE ADD (
  CONSTRAINT CONF_SCELTA_PATRIMONIALE_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_SCELTA_PATRIMONIALE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_STATO_CIVILE
(
  ID_STATO_CIVILE  NUMBER(2)                    NOT NULL,
  DESCRIZIONE      VARCHAR2(80 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_STATO_CIVILE IS 'Tabella tipologica contenente l''elenco degli stati civili che un soggetto può acquisire.';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_CIVILE.ID_STATO_CIVILE IS 'Identificativo dello stato civilie attribuito ad un soggetto';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_CIVILE.DESCRIZIONE IS 'Descrizione dello stato civile attribuito ad un soggetto';



CREATE UNIQUE INDEX ANAG_USR.CONF_STATO_CIVILE_PK ON ANAG_USR.CONF_STATO_CIVILE
(ID_STATO_CIVILE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CONF_STATO_CIVILE FOR ANAG_USR.CONF_STATO_CIVILE;


ALTER TABLE ANAG_USR.CONF_STATO_CIVILE ADD (
  CONSTRAINT CONF_STATO_CIVILE_PK
  PRIMARY KEY
  (ID_STATO_CIVILE)
  USING INDEX ANAG_USR.CONF_STATO_CIVILE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_STATO_ESTERO
(
  ID_STATO_ESTERO   NUMBER                      NOT NULL,
  DESCRIZIONE       VARCHAR2(200 BYTE),
  COMUNITARIO       VARCHAR2(1 CHAR),
  SIGLA_NAZIONE     VARCHAR2(3 BYTE),
  CODICE_CATASTALE  VARCHAR2(4 BYTE),
  CODICE_ANPR       VARCHAR2(20 BYTE)
)
TABLESPACE SYSTEM
RESULT_CACHE (MODE DEFAULT)
PCTUSED    40
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_STATO_ESTERO.ID_STATO_ESTERO IS 'Codice ISTAT identificativo dello Stato Estero';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_ESTERO.DESCRIZIONE IS 'Nome dello Stato Estero';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_ESTERO.COMUNITARIO IS 'Flag che identifica se lo Stato è comunitario. Valore S per indicare COMUNITARIO, N indica NON COMUNITARIO';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_ESTERO.SIGLA_NAZIONE IS 'Sigla dello stato';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_ESTERO.CODICE_CATASTALE IS 'Codice catastale (belfiore) di quattro cifre dello stato.';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_ESTERO.CODICE_ANPR IS 'codice ISTAT indentificativo dello Stato Estero con codifica ANPR';



CREATE UNIQUE INDEX ANAG_USR.CONF_STATO_ESTERO_PK ON ANAG_USR.CONF_STATO_ESTERO
(ID_STATO_ESTERO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CONF_STATO_ESTERO FOR ANAG_USR.CONF_STATO_ESTERO;


ALTER TABLE ANAG_USR.CONF_STATO_ESTERO ADD (
  CONSTRAINT CONF_STATO_ESTERO_PK
  PRIMARY KEY
  (ID_STATO_ESTERO)
  USING INDEX ANAG_USR.CONF_STATO_ESTERO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_STATO_PRATICA
(
  ID_STATO_PRATICA  NUMBER                      NOT NULL,
  DESCRIZIONE       VARCHAR2(250 BYTE),
  IS_CRI            VARCHAR2(1 BYTE)            DEFAULT 'N',
  IS_IRR            VARCHAR2(1 BYTE)            DEFAULT 'N',
  IS_AIRE           VARCHAR2(1 BYTE)            DEFAULT 'N',
  IS_CERT           VARCHAR2(1 BYTE)            DEFAULT 'N',
  IS_ACC            VARCHAR2(1 BYTE)            DEFAULT 'N',
  IS_CRE            VARCHAR2(1 BYTE)            DEFAULT 'N',
  IS_DICH           VARCHAR2(1 BYTE)            DEFAULT 'N',
  IS_CONTR          VARCHAR2(1 BYTE)            DEFAULT 'N',
  IS_PPT            VARCHAR2(1 BYTE)            DEFAULT 'N',
  IS_CDI            VARCHAR2(1 BYTE)            DEFAULT 'N',
  IS_RICH           VARCHAR2(1 BYTE)            DEFAULT 'N'
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_STATO_PRATICA IS 'Tabella tipologica contenente gli stati in cui una pratica può trovarsi nel corso della sua istruttoria.';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_PRATICA.ID_STATO_PRATICA IS 'Numero identificativo dello stato di lavorazione della pratica.';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_PRATICA.DESCRIZIONE IS 'Il campo descrive lo stato di avanzamento della pratica.';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_PRATICA.IS_CRI IS 'flag che identifica se lo stato pratica è utilizzato nella pratica cri. S si, N no';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_PRATICA.IS_IRR IS 'flag che identifica se lo stato pratica è utilizzato nella pratica di Irreperibilità. S si, N no';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_PRATICA.IS_AIRE IS 'flag che identifica se lo stato pratica è utilizzato nella pratica di AIRE. S si, N no';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_PRATICA.IS_CERT IS 'flag che identifica se lo stato pratica è utilizzato nella pratica di certificati. S si, N no';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_PRATICA.IS_ACC IS 'flag che identifica se lo stato pratica è utilizzato nelle pratiche di accertamento. S si, N no';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_PRATICA.IS_CRE IS 'flag che identifica se lo stato pratica è utilizzato nella pratica CRE. S si, N no';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_PRATICA.IS_DICH IS 'flag che identifica se lo stato pratica è utilizzato nella pratica DICHIARAZIONE. S si, N no';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_PRATICA.IS_CONTR IS 'flag che identifica se lo stato pratica è utilizzato nella pratica CONTRATTO. S si, N no';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_PRATICA.IS_PPT IS 'flag che identifica se lo stato pratica è utilizzato nella pratica per la popolazione temporanea. S si, N no';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_PRATICA.IS_CDI IS 'flag che identifica se lo stato pratica è utilizzato nella pratica per la cancellazione per duplice iscrizione. S si, N no';



CREATE UNIQUE INDEX ANAG_USR.CONF_STATO_PRATICA_PK ON ANAG_USR.CONF_STATO_PRATICA
(ID_STATO_PRATICA)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CONF_STATO_PRATICA FOR ANAG_USR.CONF_STATO_PRATICA;


ALTER TABLE ANAG_USR.CONF_STATO_PRATICA ADD (
  CONSTRAINT CONF_STATO_PRATICA_PK
  PRIMARY KEY
  (ID_STATO_PRATICA)
  USING INDEX ANAG_USR.CONF_STATO_PRATICA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_STATO_VALIDITA_PATENTE
(
  ID_STATO_VALIDITA_PATENTE       NUMBER(1)     NOT NULL,
  DESCRIZIONE_STATO_VALIDITA_PAT  VARCHAR2(20 CHAR)
)
TABLESPACE SYSTEM
RESULT_CACHE (MODE DEFAULT)
PCTUSED    40
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_STATO_VALIDITA_PATENT_PK ON ANAG_USR.CONF_STATO_VALIDITA_PATENTE
(ID_STATO_VALIDITA_PATENTE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_STATO_VALIDITA_PATENTE ADD (
  CONSTRAINT CONF_STATO_VALIDITA_PATENT_PK
  PRIMARY KEY
  (ID_STATO_VALIDITA_PATENTE)
  USING INDEX ANAG_USR.CONF_STATO_VALIDITA_PATENT_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_STRUTTURE_CONV
(
  ID           NUMBER                           NOT NULL,
  DESCRIZIONE  VARCHAR2(50 CHAR)                NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_STRUTTURE_CONV IS 'Tabella tipologica che contiene le strutture convenzionate con l''Amministrazione di Roma Capitale.';

COMMENT ON COLUMN ANAG_USR.CONF_STRUTTURE_CONV.ID IS 'Identificativo della struttura convenzionata.';

COMMENT ON COLUMN ANAG_USR.CONF_STRUTTURE_CONV.DESCRIZIONE IS 'Descrizione della struttura convenzionata.';



CREATE UNIQUE INDEX ANAG_USR.CONF_STRUTTURE_CONV_PK ON ANAG_USR.CONF_STRUTTURE_CONV
(ID)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_STRUTTURE_CONV ADD (
  CONSTRAINT CONF_STRUTTURE_CONV_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_STRUTTURE_CONV_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_STRUTTURE_INTERNE_RC
(
  ID                          NUMBER            NOT NULL,
  CODICE_STRUTTURA            VARCHAR2(10 CHAR) NOT NULL,
  DESCRIZIONE_STRUTTURA       VARCHAR2(200 CHAR) NOT NULL,
  CODICE_RESPONSABILE         NUMBER            NOT NULL,
  NOME_RESPONSABILE           VARCHAR2(20 CHAR) NOT NULL,
  COGNOME_RESPONSABILE        VARCHAR2(20 CHAR) NOT NULL,
  CODICE_PROCEDURA_CHIAMANTE  VARCHAR2(20 BYTE),
  CODICE_DOCUMENTO            NUMBER,
  TIPO_PROTOCOLLO             VARCHAR2(20 BYTE),
  INTESTAZIONE_DIP            VARCHAR2(450 BYTE) NOT NULL,
  INTESTAZIONE_U_O_APP        VARCHAR2(450 BYTE),
  FLG_ATTIVO                  NUMBER            NOT NULL,
  FLG_GRUPPO_VIGILI           NUMBER,
  SETTORE                     VARCHAR2(10 CHAR),
  CENTRO_RICAVO               VARCHAR2(20 CHAR),
  NUMERO_STRUTTURA            NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_STRUTTURE_INTERNE_RC IS 'Tabella tipologica contenente l''elenco delle strutture interne di Roma Capitale';

COMMENT ON COLUMN ANAG_USR.CONF_STRUTTURE_INTERNE_RC.ID IS 'Identificativo della struttura interna di Roma Capitale';

COMMENT ON COLUMN ANAG_USR.CONF_STRUTTURE_INTERNE_RC.CODICE_STRUTTURA IS 'Codice della struttura utilizzato per la protocollazione';

COMMENT ON COLUMN ANAG_USR.CONF_STRUTTURE_INTERNE_RC.DESCRIZIONE_STRUTTURA IS 'Descrizione della struttura interna di Roma Capitale';

COMMENT ON COLUMN ANAG_USR.CONF_STRUTTURE_INTERNE_RC.CODICE_RESPONSABILE IS 'Codice del responsabile della struttura';

COMMENT ON COLUMN ANAG_USR.CONF_STRUTTURE_INTERNE_RC.NOME_RESPONSABILE IS 'Nome del responsabile della struttura';

COMMENT ON COLUMN ANAG_USR.CONF_STRUTTURE_INTERNE_RC.COGNOME_RESPONSABILE IS 'Cognome del responsabile della struttura';

COMMENT ON COLUMN ANAG_USR.CONF_STRUTTURE_INTERNE_RC.CODICE_PROCEDURA_CHIAMANTE IS 'Codice procedura chiamante';

COMMENT ON COLUMN ANAG_USR.CONF_STRUTTURE_INTERNE_RC.CODICE_DOCUMENTO IS 'Codice documento';

COMMENT ON COLUMN ANAG_USR.CONF_STRUTTURE_INTERNE_RC.TIPO_PROTOCOLLO IS 'Tipo protocollo';

COMMENT ON COLUMN ANAG_USR.CONF_STRUTTURE_INTERNE_RC.INTESTAZIONE_DIP IS 'Intestazione dipartimento';

COMMENT ON COLUMN ANAG_USR.CONF_STRUTTURE_INTERNE_RC.SETTORE IS 'Campo utilizzato per l''integrazione SIR.';

COMMENT ON COLUMN ANAG_USR.CONF_STRUTTURE_INTERNE_RC.CENTRO_RICAVO IS 'Campo utilizzato per l''integrazione SIR.';

COMMENT ON COLUMN ANAG_USR.CONF_STRUTTURE_INTERNE_RC.NUMERO_STRUTTURA IS 'Campo utilizzato per l''integrazione AGGIOR';



CREATE UNIQUE INDEX ANAG_USR.CONF_STRUTTURE_INTERNE_RC_PK ON ANAG_USR.CONF_STRUTTURE_INTERNE_RC
(ID)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CONF_STRUTTURE_INTERNE_RC FOR ANAG_USR.CONF_STRUTTURE_INTERNE_RC;


ALTER TABLE ANAG_USR.CONF_STRUTTURE_INTERNE_RC ADD (
  CONSTRAINT CONF_STRUTTURE_INTERNE_RC_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_STRUTTURE_INTERNE_RC_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_ALLOGGIO
(
  ID           NUMBER                           NOT NULL,
  DESCRIZIONE  VARCHAR2(50 CHAR)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_TIPO_ALLOGGIO IS 'Tabella tipologica contenente l''elenco delle tipologie di alloggio ammesse.';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_ALLOGGIO.ID IS 'Identificativo della tipologia di alloggio';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_ALLOGGIO.DESCRIZIONE IS 'Descrizione della tipologia di alloggio';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_ALLOGGIO_PK ON ANAG_USR.CONF_TIPO_ALLOGGIO
(ID)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_ALLOGGIO ADD (
  CONSTRAINT CONF_TIPO_ALLOGGIO_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_TIPO_ALLOGGIO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_ATTO
(
  ID_TIPO_ATTO  NUMBER(2)                       NOT NULL,
  DESCRIZIONE   VARCHAR2(100 CHAR)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_TIPO_ATTO IS 'Tabella tipologica contenente l''elenco delle tipologie di atto di stato civile gestite dal sistema.';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_ATTO.ID_TIPO_ATTO IS 'Codice identificativo della tipologia di atto.';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_ATTO.DESCRIZIONE IS 'Campo che descrive la tipologia di atto.';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_ATTO_PK ON ANAG_USR.CONF_TIPO_ATTO
(ID_TIPO_ATTO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_ATTO ADD (
  CONSTRAINT CONF_TIPO_ATTO_PK
  PRIMARY KEY
  (ID_TIPO_ATTO)
  USING INDEX ANAG_USR.CONF_TIPO_ATTO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_CERTIFICATO
(
  ID_CONF_TIPO_CERTIFICATO  NUMBER              NOT NULL,
  DESCRIZIONE               VARCHAR2(200 CHAR)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_TIPO_CERTIFICATO IS 'Tabella tipologica contenente le tipologie di certificato gestite dal sistema.';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_CERTIFICATO.ID_CONF_TIPO_CERTIFICATO IS 'Identificativo della tipologia di certificato';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_CERTIFICATO.DESCRIZIONE IS 'Descrizione della tipologia di certificato';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_CERTIFICATO_PK ON ANAG_USR.CONF_TIPO_CERTIFICATO
(ID_CONF_TIPO_CERTIFICATO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_CERTIFICATO ADD (
  CONSTRAINT CONF_TIPO_CERTIFICATO_PK
  PRIMARY KEY
  (ID_CONF_TIPO_CERTIFICATO)
  USING INDEX ANAG_USR.CONF_TIPO_CERTIFICATO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_LEGAME
(
  ID_TIPO_LEGAME    NUMBER(2)                   NOT NULL,
  DESCRIZIONE       VARCHAR2(250 CHAR)          NOT NULL,
  TIPO_SCHEDA_ANPR  NUMBER(1)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_TIPO_LEGAME IS 'Tabella tipologica contenente l''elenco delle tipologie di legame di parentela che sussiste tra due soggetti.';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_LEGAME.ID_TIPO_LEGAME IS 'Codice identificavo della tipologia di legame. ';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_LEGAME.DESCRIZIONE IS 'Descrizione della tipologia di legame. ';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_LEGAME.TIPO_SCHEDA_ANPR IS 'Identificativo anpr relativo al tipo scheda di una famiglia';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_LEGAME_PK ON ANAG_USR.CONF_TIPO_LEGAME
(ID_TIPO_LEGAME)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_LEGAME ADD (
  CONSTRAINT CONF_TIPO_LEGAME_PK
  PRIMARY KEY
  (ID_TIPO_LEGAME)
  USING INDEX ANAG_USR.CONF_TIPO_LEGAME_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_MOVIMENTAZIONE
(
  ID_TIPO_MOVIMENTAZIONE  NUMBER(2)             NOT NULL,
  DESCRIZIONE             VARCHAR2(100 BYTE)    NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_TIPO_MOVIMENTAZIONE IS 'Tabella tipologica contenente l''elenco delle tipologie di movimentazioni.';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_MOVIMENTAZIONE.ID_TIPO_MOVIMENTAZIONE IS 'Identificativo del tipod i movimentazione che ha costituito la famiglia.';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_MOVIMENTAZIONE.DESCRIZIONE IS 'Descrizione del tipo d i movimentazione che ha costituito la famiglia.';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_MOVIMENTAZIONE_PK ON ANAG_USR.CONF_TIPO_MOVIMENTAZIONE
(ID_TIPO_MOVIMENTAZIONE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_MOVIMENTAZIONE ADD (
  CONSTRAINT CONF_TIPO_MOVIMENTAZIONE_PK
  PRIMARY KEY
  (ID_TIPO_MOVIMENTAZIONE)
  USING INDEX ANAG_USR.CONF_TIPO_MOVIMENTAZIONE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_PRATICA_AIRE
(
  ID_TIPO_PRATICA_AIRE     NUMBER               NOT NULL,
  DESCRIZIONE              VARCHAR2(200 CHAR),
  ID_OGGETTO_PRATICA_AIRE  NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_TIPO_PRATICA_AIRE IS 'Tabella tipologica contenente l''elenco delle tipologie di pratiche AIRE gestite dal sistema.';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_PRATICA_AIRE.ID_TIPO_PRATICA_AIRE IS 'Identificativo della tipologia pratica AIRE';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_PRATICA_AIRE.DESCRIZIONE IS 'Descrizione della tipologia di pratica AIRE';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_PRATICA_AIRE.ID_OGGETTO_PRATICA_AIRE IS 'identificativo delle tipologie di oggetto che può essere associato ad una pratica aire';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_PRATICA_AIRE_PK ON ANAG_USR.CONF_TIPO_PRATICA_AIRE
(ID_TIPO_PRATICA_AIRE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE INDEX ANAG_USR.ID_PRATICA_AIRE_FK ON ANAG_USR.CONF_TIPO_PRATICA_AIRE
(ID_OGGETTO_PRATICA_AIRE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_PRATICA_AIRE ADD (
  CONSTRAINT CONF_TIPO_PRATICA_AIRE_PK
  PRIMARY KEY
  (ID_TIPO_PRATICA_AIRE)
  USING INDEX ANAG_USR.CONF_TIPO_PRATICA_AIRE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONF_TIPO_PRATICA_AIRE ADD (
  CONSTRAINT CONF_TIPO_PRATICA_AIRE_FK1 
  FOREIGN KEY (ID_OGGETTO_PRATICA_AIRE) 
  REFERENCES ANAG_USR.OGGETTO_PRATICA_AIRE (ID_OGGETTO_PRATICA_AIRE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_PROTOCOLLO
(
  CODICE_TIPO_PROTOCOLLO  VARCHAR2(10 BYTE)     NOT NULL,
  DESCRIZIONE             VARCHAR2(250 BYTE),
  SIGLA_TIPO_PROTOCOLLO   VARCHAR2(20 BYTE),
  TIPO_PROT_PL            NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_TIPO_PROTOCOLLO IS 'Tabella tipologica contenente l''elenco delle tipologie di protocollo gestite dal sistema.';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_PROTOCOLLO.CODICE_TIPO_PROTOCOLLO IS 'Codice identificativo dell''ente protocollante.';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_PROTOCOLLO.DESCRIZIONE IS 'Campo che descrive l''ente protocollante.';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_PROTOCOLLO_PK ON ANAG_USR.CONF_TIPO_PROTOCOLLO
(CODICE_TIPO_PROTOCOLLO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_PROTOCOLLO ADD (
  CONSTRAINT CONF_TIPO_PROTOCOLLO_PK
  PRIMARY KEY
  (CODICE_TIPO_PROTOCOLLO)
  USING INDEX ANAG_USR.CONF_TIPO_PROTOCOLLO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_RICHIESTA_CAMBIO
(
  ID_TIPO_RICHIESTA_CAMBIO  NUMBER CONSTRAINT NNC_ID_TIPO_RICHIESTA_CAMBIO NOT NULL,
  DESCRIZIONE               VARCHAR2(250 BYTE),
  FLAG_ABITAZIONE           VARCHAR2(1 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_TIPO_RICHIESTA_CAMBIO IS 'Tabella tipologica contenente l''elenco delle tipologie di richiesta di cambio di residenza/domicilio.';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_RICHIESTA_CAMBIO.ID_TIPO_RICHIESTA_CAMBIO IS 'Identificativo unico del tipo di richiesta del cambio di residenza o domicilio.';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_RICHIESTA_CAMBIO.DESCRIZIONE IS 'Descrizione della tipologia di richiesta dei cambi di residenza o abitazione';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_RICHIESTA_CAMBIO.FLAG_ABITAZIONE IS 'S se è una tipologia di richiesta cambio ammessa per il cambio di abitazione   
E se è una tipologia di richiesta cambio ammessa SOLO per il cambio di abitazione
';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_RICHIESTA_CAMBIO_PK ON ANAG_USR.CONF_TIPO_RICHIESTA_CAMBIO
(ID_TIPO_RICHIESTA_CAMBIO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_RICHIESTA_CAMBIO ADD (
  CONSTRAINT CONF_TIPO_RICHIESTA_CAMBIO_PK
  PRIMARY KEY
  (ID_TIPO_RICHIESTA_CAMBIO)
  USING INDEX ANAG_USR.CONF_TIPO_RICHIESTA_CAMBIO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_SOGGIORNO
(
  ID_TIPO_SOGGIORNO       NUMBER(2)             NOT NULL,
  DESCRIZIONE             VARCHAR2(40 BYTE),
  ID_TIPO_SOGGIORNO_ANPR  VARCHAR2(2 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_TIPO_SOGGIORNO IS 'Tabella tipologica contenente l''elenco delle tipologie di permesso o attestato di soggiorno registrabili a sistema.';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_SOGGIORNO.ID_TIPO_SOGGIORNO IS 'Identificativo della tipologia di soggiorno.';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_SOGGIORNO.DESCRIZIONE IS 'Descrizione della tipologia di permesso di soggiorno.';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_SOGGIORNO.ID_TIPO_SOGGIORNO_ANPR IS 'IDENTIFICATIVO DI TRANSCODIFICA ANPR TABELLA 8';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_SOGGIORNO_PK ON ANAG_USR.CONF_TIPO_SOGGIORNO
(ID_TIPO_SOGGIORNO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_SOGGIORNO ADD (
  CONSTRAINT CONF_TIPO_SOGGIORNO_PK
  PRIMARY KEY
  (ID_TIPO_SOGGIORNO)
  USING INDEX ANAG_USR.CONF_TIPO_SOGGIORNO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_VEICOLO
(
  ID_TIPO_VEICOLO  NUMBER(2)                    NOT NULL,
  DESCRIZIONE      VARCHAR2(100 BYTE)
)
TABLESPACE SYSTEM
RESULT_CACHE (MODE DEFAULT)
PCTUSED    40
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_VEICOLO_PK ON ANAG_USR.CONF_TIPO_VEICOLO
(ID_TIPO_VEICOLO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_VEICOLO ADD (
  CONSTRAINT CONF_TIPO_VEICOLO_PK
  PRIMARY KEY
  (ID_TIPO_VEICOLO)
  USING INDEX ANAG_USR.CONF_TIPO_VEICOLO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TITOLI_STUDIO
(
  ID_TITOLO_STUDIO_ANPR  VARCHAR2(5 BYTE)       NOT NULL,
  ID_TITOLO_STUDIO_APR   NUMBER(2),
  DESCRIZIONE            VARCHAR2(80 BYTE)      NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_TITOLI_STUDIO IS 'Tabella tipologica contenente l''elenco dei titoli di studio gestiti dal sistema.';

COMMENT ON COLUMN ANAG_USR.CONF_TITOLI_STUDIO.ID_TITOLO_STUDIO_ANPR IS 'codice identificativo della posizione professionale usato in ANPR.';

COMMENT ON COLUMN ANAG_USR.CONF_TITOLI_STUDIO.ID_TITOLO_STUDIO_APR IS 'Codice identificativo del titolo di studio usato in APR.';

COMMENT ON COLUMN ANAG_USR.CONF_TITOLI_STUDIO.DESCRIZIONE IS 'Descrizione del titolo di studio.';



CREATE UNIQUE INDEX ANAG_USR.TITOLO_STUDIO_PK ON ANAG_USR.CONF_TITOLI_STUDIO
(ID_TITOLO_STUDIO_ANPR)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CONF_TITOLI_STUDIO FOR ANAG_USR.CONF_TITOLI_STUDIO;


ALTER TABLE ANAG_USR.CONF_TITOLI_STUDIO ADD (
  CONSTRAINT CONF_TITOLI_STUDIO_PK
  PRIMARY KEY
  (ID_TITOLO_STUDIO_ANPR)
  USING INDEX ANAG_USR.TITOLO_STUDIO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TITOLO_POSSESSO
(
  ID           NUMBER                           NOT NULL,
  DESCRIZIONE  VARCHAR2(50 CHAR)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_TITOLO_POSSESSO IS 'Tabella tipologica contenente l''elenco dei titoli di possesso di un immobile gestiti dal sistema';

COMMENT ON COLUMN ANAG_USR.CONF_TITOLO_POSSESSO.ID IS 'Identificativo del titolo di possesso';

COMMENT ON COLUMN ANAG_USR.CONF_TITOLO_POSSESSO.DESCRIZIONE IS 'Descrizione del titolo di possesso';



CREATE UNIQUE INDEX ANAG_USR.CONF_TITOLO_POSSESSO_PK ON ANAG_USR.CONF_TITOLO_POSSESSO
(ID)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TITOLO_POSSESSO ADD (
  CONSTRAINT CONF_TITOLO_POSSESSO_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_TITOLO_POSSESSO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TRASFERIMENTO_DIMORA
(
  ID           NUMBER                           NOT NULL,
  DESCRIZIONE  VARCHAR2(200 CHAR)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_TRASFERIMENTO_DIMORA IS 'Tabella tipologica contenente l''elenco delle motivazioni relative al trasferimento della dimora abituale.';

COMMENT ON COLUMN ANAG_USR.CONF_TRASFERIMENTO_DIMORA.ID IS 'Identificativo trasferimento dimora';

COMMENT ON COLUMN ANAG_USR.CONF_TRASFERIMENTO_DIMORA.DESCRIZIONE IS 'Descrizione trasferimento dimora';



CREATE UNIQUE INDEX ANAG_USR.CONF_TRASFERIMENTO_DIMORA_PK ON ANAG_USR.CONF_TRASFERIMENTO_DIMORA
(ID)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TRASFERIMENTO_DIMORA ADD (
  CONSTRAINT CONF_TRASFERIMENTO_DIMORA_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_TRASFERIMENTO_DIMORA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONSOLATO
(
  ID_CONSOLATO          NUMBER                  NOT NULL,
  DESCRIZIONE           VARCHAR2(200 BYTE),
  ID_LOCALITA           NUMBER,
  EMAIL                 VARCHAR2(80 BYTE),
  DESCRIZIONE_LOCALITA  VARCHAR2(120 BYTE),
  FLAG_ATTIVO           VARCHAR2(1 BYTE),
  INDIRIZZO             VARCHAR2(1000 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONSOLATO IS 'Tabella contenente l''anagrafica dei consolati nel mondo.';

COMMENT ON COLUMN ANAG_USR.CONSOLATO.ID_CONSOLATO IS 'identificativo del consolato estero';

COMMENT ON COLUMN ANAG_USR.CONSOLATO.DESCRIZIONE IS 'denominazione del consolato estero';

COMMENT ON COLUMN ANAG_USR.CONSOLATO.ID_LOCALITA IS 'località estera in cui ha sede il consolato';

COMMENT ON COLUMN ANAG_USR.CONSOLATO.EMAIL IS 'Email del consolato';

COMMENT ON COLUMN ANAG_USR.CONSOLATO.DESCRIZIONE_LOCALITA IS 'descrizione località estera in cui ha sede il consolato';

COMMENT ON COLUMN ANAG_USR.CONSOLATO.FLAG_ATTIVO IS 'S -> Attivo, N -> Disattivo';

COMMENT ON COLUMN ANAG_USR.CONSOLATO.INDIRIZZO IS 'Indirizzo in cui si trova il consolato';



CREATE UNIQUE INDEX ANAG_USR.CONSOLATO_PK ON ANAG_USR.CONSOLATO
(ID_CONSOLATO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CONSOLATO FOR ANAG_USR.CONSOLATO;


ALTER TABLE ANAG_USR.CONSOLATO ADD (
  CONSTRAINT CONSOLATO_PK
  PRIMARY KEY
  (ID_CONSOLATO)
  USING INDEX ANAG_USR.CONSOLATO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.DICHIARAZIONE
(
  ID_DICHIARAZIONE          NUMBER              NOT NULL,
  CODICE_TIPO_PROTOCOLLO    VARCHAR2(10 CHAR),
  ANNO_PROTOCOLLO           NUMBER,
  NUMERO_PROTOCOLLO         NUMBER,
  DATA_DICHIARAZIONE        DATE,
  ID_SOGGETTO_PRIMO         NUMBER              NOT NULL,
  ID_SOGGETTO_SECONDO       NUMBER              NOT NULL,
  C_COD_TIPO_PROTOCOLLO     VARCHAR2(10 CHAR),
  C_ANNO_PROTOCOLLO         NUMBER,
  C_NUMERO_PROTOCOLLO       NUMBER,
  C_DATA_DICHIARAZIONE      DATE,
  ID_STATO                  NUMBER              NOT NULL,
  ID_ESITO_ACCERTAMENTO     NUMBER,
  ID_MOTIV_CHIUSURA         NUMBER,
  E_COD_TIPO_PROTOCOLLO     VARCHAR2(10 CHAR),
  E_ANNO_PROTOCOLLO         NUMBER,
  E_NUMERO_PROTOCOLLO       NUMBER,
  E_DATA_DICHIARAZIONE      DATE,
  MOTIVAZIONE_ELIMINAZIONE  VARCHAR2(200 CHAR),
  NUMERO_DICHIARAZIONE      NUMBER              NOT NULL,
  DATA_PROTOCOLLO           DATE,
  C_DATA_PROTOCOLLO         DATE,
  E_DATA_PROTOCOLLO         DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.DICHIARAZIONE IS 'Tabella contenente le informazioni sulle dichiarazioni di convivenza.';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.ID_DICHIARAZIONE IS 'Identificativo della dichiarazione di convivenza';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.CODICE_TIPO_PROTOCOLLO IS 'Codice del protocollo della dichiarazione di convivenza';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.ANNO_PROTOCOLLO IS 'Anno del protocollo della dichiarazione di convivenza';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.NUMERO_PROTOCOLLO IS 'Numero del protocollo della dichiarazione di convivenza';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.DATA_DICHIARAZIONE IS 'Data della dichiarazione di convivenza.';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.ID_SOGGETTO_PRIMO IS 'Id del primo soggetto facente parte della convivenza';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.ID_SOGGETTO_SECONDO IS 'Id del secondo soggetto facente parte della convivenza.';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.C_COD_TIPO_PROTOCOLLO IS 'Codice del protocollo per la chiusura della dichiarazione di convivenza';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.C_ANNO_PROTOCOLLO IS 'Anno del protocollo per la chiusura della dichiarazione di convivenza';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.C_NUMERO_PROTOCOLLO IS 'Numero del protocollo per la chiusura della dichiarazione di convivenza';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.C_DATA_DICHIARAZIONE IS 'Data di chiusura della dichiarazione di convivenza';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.ID_STATO IS 'Identificativo dello stato del procedimento di dichiarazione di convivenza.';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.ID_ESITO_ACCERTAMENTO IS 'Identificativo rappresentante l''esito dell''accertamento';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.ID_MOTIV_CHIUSURA IS 'FK verso la tabella tipologica di motivazione della chiusura della dichiarazione di convivenza.';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.E_COD_TIPO_PROTOCOLLO IS 'Codice del protocollo per l''eliminazione della dichiarazione di convivenza';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.E_ANNO_PROTOCOLLO IS 'Anno del protocollo per l''eliminazione della dichiarazione di convivenza';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.E_NUMERO_PROTOCOLLO IS 'Numero del protocollo per l''eliminazione della dichiarazione di convivenza';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.E_DATA_DICHIARAZIONE IS 'Data dell''eliminazione della dichiarazione di convivenza';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.MOTIVAZIONE_ELIMINAZIONE IS 'Motivazione dell''eliminazione della dichiarazione di convivenza.';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.NUMERO_DICHIARAZIONE IS 'Numero della dichiarazione';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.DATA_PROTOCOLLO IS 'Data del protocollo di dichiarazione';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.C_DATA_PROTOCOLLO IS 'Data del protocollo della pratica di chiusura';

COMMENT ON COLUMN ANAG_USR.DICHIARAZIONE.E_DATA_PROTOCOLLO IS 'Data del protocollo della pratica di eliminazione';



CREATE UNIQUE INDEX ANAG_USR.DICHIARAZIONE_PK ON ANAG_USR.DICHIARAZIONE
(ID_DICHIARAZIONE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.DICHIARAZIONE ADD (
  CONSTRAINT DICHIARAZIONE_PK
  PRIMARY KEY
  (ID_DICHIARAZIONE)
  USING INDEX ANAG_USR.DICHIARAZIONE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.DICHIARAZIONE ADD (
  CONSTRAINT CONF_ESITO_DIC_CONVIVENZA_FK 
  FOREIGN KEY (ID_ESITO_ACCERTAMENTO) 
  REFERENCES ANAG_USR.CONF_ESITO_DIC_CONVIVENZA (ID)
  ENABLE VALIDATE,
  CONSTRAINT CONF_MOTIVAZIONE_CHIUSURA_FK 
  FOREIGN KEY (ID_MOTIV_CHIUSURA) 
  REFERENCES ANAG_USR.CONF_MOTIVAZIONE_CHIUSURA (ID)
  ENABLE VALIDATE,
  CONSTRAINT CONF_STATO_PRATICA_FKV3 
  FOREIGN KEY (ID_STATO) 
  REFERENCES ANAG_USR.CONF_STATO_PRATICA (ID_STATO_PRATICA)
  ENABLE VALIDATE,
  CONSTRAINT CONF_TIPO_PROTOCOLLO_FK1 
  FOREIGN KEY (CODICE_TIPO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE,
  CONSTRAINT C_CONF_TIPO_PROTOCOLLO_FK2 
  FOREIGN KEY (C_COD_TIPO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE,
  CONSTRAINT E_CONF_TIPO_PROTOCOLLO_FK2 
  FOREIGN KEY (E_COD_TIPO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_PRIMO_FK 
  FOREIGN KEY (ID_SOGGETTO_PRIMO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_SECONDO_FK 
  FOREIGN KEY (ID_SOGGETTO_SECONDO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.ESITO_ISCRIZIONE
(
  ID_ESITO                 NUMBER               NOT NULL,
  ID_ACCERTAMENTO          NUMBER,
  DATA_SOPRALLUOGO         DATE,
  CONFERMA_INDIRIZZO       CHAR(1 CHAR),
  INDIRIZZO_ESATTO         VARCHAR2(50 CHAR),
  ID_TIPO_ALLOGGIO         NUMBER,
  ALTRO_ALLOGGIO           VARCHAR2(50 CHAR),
  ID_TITOLO_POSSESSO       NUMBER,
  ALTRO_TITOLO_POSSESSO    VARCHAR2(50 CHAR),
  ESITO                    CHAR(1 CHAR),
  NOTE                     VARCHAR2(200 CHAR),
  ID_SOGGETTO              NUMBER,
  ID_TRASFERIMENTO_DIMORA  NUMBER,
  ID_PREAVVISO_RIGETTO     NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.ESITO_ISCRIZIONE IS 'Tabella contenente le informazioni inserite a sistema dai Gruppi di Polizia Locale relative all''ESITO di un accertamento per iscrizione.';

COMMENT ON COLUMN ANAG_USR.ESITO_ISCRIZIONE.ID_ESITO IS 'Identificativo dell''esito di un accertamento per Iscrizione';

COMMENT ON COLUMN ANAG_USR.ESITO_ISCRIZIONE.ID_ACCERTAMENTO IS 'FK rappresentante la richiesta di accertamento per la quale si sta impostando l''esito da parte del gruppo di polizia locale';

COMMENT ON COLUMN ANAG_USR.ESITO_ISCRIZIONE.DATA_SOPRALLUOGO IS 'Data del sopralluogo';

COMMENT ON COLUMN ANAG_USR.ESITO_ISCRIZIONE.CONFERMA_INDIRIZZO IS 'N -> NO
S -> SI';

COMMENT ON COLUMN ANAG_USR.ESITO_ISCRIZIONE.INDIRIZZO_ESATTO IS 'Descrizione dell''indirizzo esatto';

COMMENT ON COLUMN ANAG_USR.ESITO_ISCRIZIONE.ID_TIPO_ALLOGGIO IS 'FK verso la tabella tipologica che rappresenta la tipologia dell''alloggio';

COMMENT ON COLUMN ANAG_USR.ESITO_ISCRIZIONE.ALTRO_ALLOGGIO IS 'Ulteriore descrizione dell''alloggio';

COMMENT ON COLUMN ANAG_USR.ESITO_ISCRIZIONE.ID_TITOLO_POSSESSO IS 'FK verso la tabella tipologica del titolo di possesso';

COMMENT ON COLUMN ANAG_USR.ESITO_ISCRIZIONE.ALTRO_TITOLO_POSSESSO IS 'Ulteriore descrizione del titolo di possesso';

COMMENT ON COLUMN ANAG_USR.ESITO_ISCRIZIONE.ESITO IS '1-> POSITIVO 0->NEGATIVO';

COMMENT ON COLUMN ANAG_USR.ESITO_ISCRIZIONE.NOTE IS 'Note inseribili all''atto del caricamento dell''esito';



CREATE UNIQUE INDEX ANAG_USR.ESITO_ISCRIZIONE_PK ON ANAG_USR.ESITO_ISCRIZIONE
(ID_ESITO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.ESITO_ISCRIZIONE ADD (
  CONSTRAINT ESITO_ISCRIZIONE_PK
  PRIMARY KEY
  (ID_ESITO)
  USING INDEX ANAG_USR.ESITO_ISCRIZIONE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.ESITO_ISCRIZIONE ADD (
  CONSTRAINT ACCERTAMENTO_FKV2 
  FOREIGN KEY (ID_ACCERTAMENTO) 
  REFERENCES ANAG_USR.ACCERTAMENTO_ISCRIZIONE (ID_ACCERTAMENTO_ISCRIZIONE)
  ENABLE VALIDATE,
  CONSTRAINT CONF_TIPO_ALLOGGIO_FK 
  FOREIGN KEY (ID_TIPO_ALLOGGIO) 
  REFERENCES ANAG_USR.CONF_TIPO_ALLOGGIO (ID)
  ENABLE VALIDATE,
  CONSTRAINT CONF_TITOLO_POSSESSO_FK 
  FOREIGN KEY (ID_TITOLO_POSSESSO) 
  REFERENCES ANAG_USR.CONF_TITOLO_POSSESSO (ID)
  ENABLE VALIDATE,
  CONSTRAINT ESITO_ISCRIZIONE_FK1 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT ESITO_ISCRIZIONE_FK2 
  FOREIGN KEY (ID_TRASFERIMENTO_DIMORA) 
  REFERENCES ANAG_USR.CONF_TRASFERIMENTO_DIMORA (ID)
  ENABLE VALIDATE,
  CONSTRAINT ESITO_ISCRIZIONE_FK3 
  FOREIGN KEY (ID_PREAVVISO_RIGETTO) 
  REFERENCES ANAG_USR.PREAVVISO_RIGETTO (ID_PREAVVISO_RIGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.FAMIGLIA_CONVIVENZA
(
  ID_FAMIGLIA_CONV               NUMBER CONSTRAINT NNC_ID_FAMIGLIA_CONVIVENZA NOT NULL,
  ID_FAMIGLIA_CONV_ANPR          VARCHAR2(20 BYTE),
  AIRE                           CHAR(1 BYTE),
  DATA_ORIGINE_FAMIGLIA          DATE,
  MOTIVO_COSTITUZIONE            NUMBER(2),
  DENOMINAZIONE_CONVIVENZA       VARCHAR2(100 BYTE),
  SPECIE_CONVIVENZA              NUMBER(2),
  DATA_INTESTATARIO_CONVIVENZA   DATE,
  ID_FAMIGLIA_COABITANTE         NUMBER,
  ID_TIPO_MOVIMENTAZIONE         NUMBER(2),
  ID_TIPO_LEGAME                 NUMBER(2),
  CODICE_ISTAT_COMUNE            VARCHAR2(20 BYTE) DEFAULT '058091',
  FLAG_ATTIVO                    CHAR(1 BYTE)   DEFAULT 'S',
  DATA_CANCELLAZIONE             DATE,
  FLAG_INTERA_FAMIGLIA           VARCHAR2(1 BYTE),
  ID_TIPO_MUTAZIONE_FAMIGLIA     VARCHAR2(1 BYTE),
  ID_SOGGETTO_RESPONSABILE_COLL  NUMBER,
  CODICE_FAMIGLIA                VARCHAR2(20 CHAR),
  ID_RESIDENZA                   NUMBER,
  ID_OPERAZIONE_ANPR             NUMBER,
  ID_TUTORE_FAMIGLIA             NUMBER,
  SAI                            VARCHAR2(2 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.FAMIGLIA_CONVIVENZA IS 'Tabella contenente le informazioni su Famiglia o Convivenza che si genera tra più soggetti.';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.ID_FAMIGLIA_CONV IS 'identificativo della famiglia o convivenza in APR';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.ID_FAMIGLIA_CONV_ANPR IS 'identificativo della famiglia o convivenza in ANPR';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.AIRE IS 'flag S/N che indica se una famiglia è di tipo AIRE.';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.DATA_ORIGINE_FAMIGLIA IS 'data in cui la famigia si è creata	';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.MOTIVO_COSTITUZIONE IS '
conf_motivo_costituzione';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.DENOMINAZIONE_CONVIVENZA IS 'nome che identifica la convivenza (collettività)';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.SPECIE_CONVIVENZA IS 'codice che identifica il motivo della costituzione di una convivenza

conf_specie_convivenza';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.DATA_INTESTATARIO_CONVIVENZA IS 'data in cui l''intestatario scheda attuale è diventato intestatario scheda';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.ID_FAMIGLIA_COABITANTE IS 'Identificativo della famiglia coabitante';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.ID_TIPO_LEGAME IS 'tipo di famiglia/convivenza';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.CODICE_ISTAT_COMUNE IS 'codice istat che identifica il comune in cui la famiglia è iscritta. default ROMA';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.FLAG_ATTIVO IS 'flag che indica se una famiglia convivenza è attiva(S) o disattiva(N) ';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.DATA_CANCELLAZIONE IS 'data in cui una famiglia/convivenza è stata cancellata/disattivata';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.FLAG_INTERA_FAMIGLIA IS 'S se la migrazione comprende l''intera famiglia N altrimenti';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.ID_SOGGETTO_RESPONSABILE_COLL IS 'Id del soggetto responsabile della collettività';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.CODICE_FAMIGLIA IS 'Codice identificativo della famiglia';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.ID_RESIDENZA IS 'Identifica la residenza attuale della famiglia/collettività';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.ID_OPERAZIONE_ANPR IS 'Identificativo operazione Anpr';

COMMENT ON COLUMN ANAG_USR.FAMIGLIA_CONVIVENZA.ID_TUTORE_FAMIGLIA IS 'identificativo del soggetto tutore';



CREATE UNIQUE INDEX ANAG_USR.FAMIGLIA_CONVIVENZA_PK ON ANAG_USR.FAMIGLIA_CONVIVENZA
(ID_FAMIGLIA_CONV)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.FAMIGLIA_CONVIVENZA_UN ON ANAG_USR.FAMIGLIA_CONVIVENZA
(ID_FAMIGLIA_CONV_ANPR, ID_FAMIGLIA_CONV)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.FAMIGLIA_CONVIVENZA FOR ANAG_USR.FAMIGLIA_CONVIVENZA;


ALTER TABLE ANAG_USR.FAMIGLIA_CONVIVENZA ADD (
  CONSTRAINT FAMIGLIA_CONVIVENZA_PK
  PRIMARY KEY
  (ID_FAMIGLIA_CONV)
  USING INDEX ANAG_USR.FAMIGLIA_CONVIVENZA_PK
  ENABLE VALIDATE,
  CONSTRAINT FAMIGLIA_CONVIVENZA_UN
  UNIQUE (ID_FAMIGLIA_CONV_ANPR, ID_FAMIGLIA_CONV)
  USING INDEX ANAG_USR.FAMIGLIA_CONVIVENZA_UN
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.FAMIGLIA_CONVIVENZA ADD (
  CONSTRAINT CONF_TIPO_MOVIMENTAZIONE_FK 
  FOREIGN KEY (ID_TIPO_MOVIMENTAZIONE) 
  REFERENCES ANAG_USR.CONF_TIPO_MOVIMENTAZIONE (ID_TIPO_MOVIMENTAZIONE)
  ENABLE VALIDATE,
  CONSTRAINT FAMIGLIA_COABITANTE_FK 
  FOREIGN KEY (ID_FAMIGLIA_COABITANTE) 
  REFERENCES ANAG_USR.FAMIGLIA_CONVIVENZA (ID_FAMIGLIA_CONV)
  ENABLE VALIDATE,
  CONSTRAINT FAMIGLIA_CONVIVENZA_FK1 
  FOREIGN KEY (ID_TIPO_LEGAME) 
  REFERENCES ANAG_USR.CONF_TIPO_LEGAME (ID_TIPO_LEGAME)
  ENABLE VALIDATE,
  CONSTRAINT FAMIGLIA_CONVIVENZA_FK2 
  FOREIGN KEY (MOTIVO_COSTITUZIONE) 
  REFERENCES ANAG_USR.CONF_MOTIVO_COSTITUZIONE (ID_MOTIVO_COSTITUZIONE)
  ENABLE VALIDATE,
  CONSTRAINT FAMIGLIA_CONVIVENZA_FK3 
  FOREIGN KEY (SPECIE_CONVIVENZA) 
  REFERENCES ANAG_USR.CONF_SPECIE_CONVIVENZA (ID_SPECIE_CONVIVENZA)
  ENABLE VALIDATE,
  CONSTRAINT FAMIGLIA_CONVIVENZA_FK4 
  FOREIGN KEY (ID_TIPO_MUTAZIONE_FAMIGLIA) 
  REFERENCES ANAG_USR.CONF_TIPO_MUTAZIONE_FAMIGLIA (ID_TIPO_MUTAZIONE_FAMIGLIA)
  ENABLE VALIDATE,
  CONSTRAINT FAMIGLIA_CONVIVENZA_FK5 
  FOREIGN KEY (ID_RESIDENZA) 
  REFERENCES ANAG_USR.RESIDENZA (ID_RESIDENZA)
  ENABLE VALIDATE,
  CONSTRAINT FAMIGLIA_CONVIVENZA_FK6 
  FOREIGN KEY (ID_SOGGETTO_RESPONSABILE_COLL) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT TUTORE_FAMIGLIA_FK 
  FOREIGN KEY (ID_TUTORE_FAMIGLIA) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);

GRANT REFERENCES, SELECT ON ANAG_USR.FAMIGLIA_CONVIVENZA TO MATR_USR;
CREATE TABLE ANAG_USR.FAQ
(
  ID_FAQ             NUMBER                     NOT NULL,
  QUESITO            VARCHAR2(100 BYTE),
  RISPOSTA           VARCHAR2(900 BYTE),
  ID_AREE_TEMATICHE  NUMBER
)
TABLESPACE SYSTEM
RESULT_CACHE (MODE DEFAULT)
PCTUSED    40
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.FAQ_PK ON ANAG_USR.FAQ
(ID_FAQ)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.FAQ ADD (
  CONSTRAINT FAQ_PK
  PRIMARY KEY
  (ID_FAQ)
  USING INDEX ANAG_USR.FAQ_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.FAQ ADD (
  CONSTRAINT FAQ_FK1 
  FOREIGN KEY (ID_AREE_TEMATICHE) 
  REFERENCES ANAG_USR.CONF_AREE_TEMATICHE (ID_AREE_TEMATICHE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.FOGLIO_VIA
(
  ID_FOGLIO_VIA                   NUMBER        NOT NULL,
  TIPO_FOGLIO_VIA                 CHAR(1 BYTE)  NOT NULL,
  DATA_INIZIO_OSTATIVA            DATE          NOT NULL,
  ID_SOGGETTO                     NUMBER        NOT NULL,
  ID_COMUNE_OSTATIVA_EMIGRAZIONE  NUMBER,
  ANNI_DURATA_OSTATIVA            NUMBER(2),
  MESI_DURATA_OSTATIVA            NUMBER(3),
  CODICE_TIPO_PROTOCOLLO          VARCHAR2(10 BYTE),
  NUMERO_PROTOCOLLO               NUMBER,
  ANNO_PROTOCOLLO                 NUMBER(4),
  NUMERO_PRATICA                  NUMBER,
  ANNO_PRATICA                    NUMBER(4),
  ID_STATO_PRATICA                NUMBER        NOT NULL,
  DATA_AGGIORNAMENTO              DATE,
  DATA_FINE_OSTATIVA              DATE,
  ID_COMUNE_RESIDENZA             NUMBER,
  INDIRIZZO_RESIDENZA             VARCHAR2(20 BYTE),
  DOC_QUESTURA                    BLOB,
  NOME_DOC_QUESTURA               VARCHAR2(100 BYTE),
  ID_QUESTURA                     NUMBER,
  DATA_INSERIMENTO                DATE
)
LOB (DOC_QUESTURA) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.FOGLIO_VIA IS 'Tabella contenente le informazioni registrate a sistema sui Fogli di Via emessi dalla questura per determinati soggetti.';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.ID_FOGLIO_VIA IS 'Identificativo del foglio via.';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.TIPO_FOGLIO_VIA IS 'Flag che indica la tipologia di foglio via.

Valorizzato con:
- I se il foglio via è di interdizione di immigrazione
- E se il foglio via è di interdizione di emigrazione';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.DATA_INIZIO_OSTATIVA IS 'Data di inizio validità dell''ostativa.';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.ID_SOGGETTO IS 'Soggetto a cui è intetato il foglio via.
';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.ID_COMUNE_OSTATIVA_EMIGRAZIONE IS 'Identificativo del comune nel quale il soggetto non potrà emigrare per la durata dell''ostativa. 
Da valorizzare solo se TIPO_FOGLIO_VIA è emigrazione.';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.ANNI_DURATA_OSTATIVA IS 'Numero di anni di durata dell''ostativa emessa nel foglio via.';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.MESI_DURATA_OSTATIVA IS 'Numero di mesi  di durata dell''ostativa emessa nel foglio via.';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.CODICE_TIPO_PROTOCOLLO IS 'Codice identificativo dell''ente protocollante del foglio via.';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.NUMERO_PROTOCOLLO IS 'Campo che indica il numero del protocollo.';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.ANNO_PROTOCOLLO IS 'Campo che indica l''anno del protocollo.';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.NUMERO_PRATICA IS 'Campo che indica il numero della pratica.';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.ANNO_PRATICA IS 'Campo che indica il l''anno della pratica.';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.ID_STATO_PRATICA IS 'Campo che indica lo stato della pratica.';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.DATA_FINE_OSTATIVA IS 'Campo che indica la scadenza del foglioVia';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.ID_COMUNE_RESIDENZA IS 'il campo indica il comune di residenza del soggetto. interessa soltanto il foglio via di immigrazione
';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.INDIRIZZO_RESIDENZA IS 'il campo indica l''indirizzo di residenza del soggetto. interessa soltanto il foglio via di immigrazione';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.DOC_QUESTURA IS 'Documento inviato dalla questura';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.NOME_DOC_QUESTURA IS 'Nome documento inviato dalla Questura';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.ID_QUESTURA IS 'Id della questura di riferimento';

COMMENT ON COLUMN ANAG_USR.FOGLIO_VIA.DATA_INSERIMENTO IS 'Data di inserimento del foglio di via';



CREATE UNIQUE INDEX ANAG_USR.FOGLIO_VIA_PK ON ANAG_USR.FOGLIO_VIA
(ID_FOGLIO_VIA)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.FOGLIO_VIA ADD (
  CONSTRAINT FOGLIO_VIA_PK
  PRIMARY KEY
  (ID_FOGLIO_VIA)
  USING INDEX ANAG_USR.FOGLIO_VIA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.FOGLIO_VIA ADD (
  CONSTRAINT COMUNE_FKV2 
  FOREIGN KEY (ID_COMUNE_OSTATIVA_EMIGRAZIONE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT CONF_QUESTURE_FK 
  FOREIGN KEY (ID_QUESTURA) 
  REFERENCES ANAG_USR.CONF_QUESTURE (ID_QUESTURA)
  ENABLE VALIDATE,
  CONSTRAINT CONF_STATO_PRATICA_FKV4 
  FOREIGN KEY (ID_STATO_PRATICA) 
  REFERENCES ANAG_USR.CONF_STATO_PRATICA (ID_STATO_PRATICA)
  ENABLE VALIDATE,
  CONSTRAINT CONF_TIPO_PROTOCOLLO_FKV3 
  FOREIGN KEY (CODICE_TIPO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE,
  CONSTRAINT FOGLIO_VIA_FK1 
  FOREIGN KEY (ID_COMUNE_RESIDENZA) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_FK 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.LIBRETTO_LAVORO
(
  NUMERO_LIBRETTO    VARCHAR2(40 CHAR)          NOT NULL,
  DATA_RILASCIO      DATE,
  COMUNE_RILASCIO    NUMBER,
  MODALITA_RILASCIO  VARCHAR2(30 CHAR),
  ID_SOGGETTO        NUMBER                     NOT NULL
)
TABLESPACE SYSTEM
RESULT_CACHE (MODE DEFAULT)
PCTUSED    40
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.LIBRETTO_LAVORO.NUMERO_LIBRETTO IS 'Codice identificativo del libretto di lavoro';

COMMENT ON COLUMN ANAG_USR.LIBRETTO_LAVORO.DATA_RILASCIO IS 'data in cui il libretto di lavoro è stato rilascito';

COMMENT ON COLUMN ANAG_USR.LIBRETTO_LAVORO.COMUNE_RILASCIO IS 'comune di rilascio del libretto di lavoro';

COMMENT ON COLUMN ANAG_USR.LIBRETTO_LAVORO.MODALITA_RILASCIO IS 'modalità di rilascio del libretto di lavoro';

COMMENT ON COLUMN ANAG_USR.LIBRETTO_LAVORO.ID_SOGGETTO IS 'Id del soggetto possessore del libretto di lavoro';



CREATE UNIQUE INDEX ANAG_USR.LIBRETTO_LAVORO_PK ON ANAG_USR.LIBRETTO_LAVORO
(NUMERO_LIBRETTO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.LIBRETTO_LAVORO FOR ANAG_USR.LIBRETTO_LAVORO;


ALTER TABLE ANAG_USR.LIBRETTO_LAVORO ADD (
  CONSTRAINT LIBRETTO_LAVORO_PK
  PRIMARY KEY
  (NUMERO_LIBRETTO)
  USING INDEX ANAG_USR.LIBRETTO_LAVORO_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.LIBRETTO_LAVORO ADD (
  CONSTRAINT COMUNE_RILASCIO_FK 
  FOREIGN KEY (COMUNE_RILASCIO) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ON DELETE CASCADE
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_LIB_FK 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.LOCALITA
(
  ID_LOCALITA           NUMBER                  NOT NULL,
  ID_STATO_ESTERO       NUMBER                  NOT NULL,
  PROVINCIA_CONTEA      VARCHAR2(30 BYTE),
  DESCRIZIONE_LOCALITA  VARCHAR2(120 BYTE),
  ID_CONSOLATO          NUMBER,
  CODICE_AGGIOR         VARCHAR2(5 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.LOCALITA IS 'Tabella contenente l''elenco delle località gestite a sistema.';

COMMENT ON COLUMN ANAG_USR.LOCALITA.ID_LOCALITA IS 'Codice identificativo della Località estera.';

COMMENT ON COLUMN ANAG_USR.LOCALITA.ID_STATO_ESTERO IS 'Campo che indica il codice ISTAT dello stato a cui la localita appartiene.';

COMMENT ON COLUMN ANAG_USR.LOCALITA.PROVINCIA_CONTEA IS 'Campo che indica la descrizione della provincia contea.';

COMMENT ON COLUMN ANAG_USR.LOCALITA.DESCRIZIONE_LOCALITA IS 'Campo che indica la descrizione della localita.';

COMMENT ON COLUMN ANAG_USR.LOCALITA.ID_CONSOLATO IS 'Campo che indica il consolato di riferimento per la località';

COMMENT ON COLUMN ANAG_USR.LOCALITA.CODICE_AGGIOR IS 'Identificativo AGGIOR';



CREATE UNIQUE INDEX ANAG_USR.LOCALITA_PK ON ANAG_USR.LOCALITA
(ID_LOCALITA)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.LOCALITA__UN ON ANAG_USR.LOCALITA
(ID_STATO_ESTERO, PROVINCIA_CONTEA, DESCRIZIONE_LOCALITA)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.LOCALITA__UN1 ON ANAG_USR.LOCALITA
(ID_STATO_ESTERO, PROVINCIA_CONTEA, DESCRIZIONE_LOCALITA, CODICE_AGGIOR)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.LOCALITA FOR ANAG_USR.LOCALITA;


ALTER TABLE ANAG_USR.LOCALITA ADD (
  CONSTRAINT LOCALITA_PK
  PRIMARY KEY
  (ID_LOCALITA)
  USING INDEX ANAG_USR.LOCALITA_PK
  ENABLE VALIDATE,
  CONSTRAINT LOCALITA__UN
  UNIQUE (ID_STATO_ESTERO, PROVINCIA_CONTEA, DESCRIZIONE_LOCALITA, CODICE_AGGIOR)
  USING INDEX ANAG_USR.LOCALITA__UN1
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.LOCALITA ADD (
  CONSTRAINT LOCALITA_CONSOLATO 
  FOREIGN KEY (ID_CONSOLATO) 
  REFERENCES ANAG_USR.CONSOLATO (ID_CONSOLATO)
  ON DELETE CASCADE
  ENABLE VALIDATE,
  CONSTRAINT LOCALITA_STATO_ESTERO_FK1 
  FOREIGN KEY (ID_STATO_ESTERO) 
  REFERENCES ANAG_USR.CONF_STATO_ESTERO (ID_STATO_ESTERO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.MATRIMONIO
(
  ID_MATRIMONIO             NUMBER              NOT NULL,
  ORDINE_MATRIMONIO         NUMBER(2),
  DATA_EVENTO               DATE,
  LUOGO_ECCEZIONALE         VARCHAR2(120 BYTE),
  ID_LOCALITA               NUMBER,
  ID_SCELTA_PATRIMONIALE    NUMBER,
  ID_SOGGETTO_MARITO        NUMBER,
  ID_SOGGETTO_MOGLIE        NUMBER,
  ID_COMUNE                 NUMBER,
  ID_ATTO                   NUMBER,
  ID_MATRIMONIO_ANPR        VARCHAR2(20 BYTE),
  FLG_SENZA_GIORNO          VARCHAR2(1 BYTE),
  FLG_SENZA_MESE            VARCHAR2(1 BYTE),
  COD_COMUNE_AGGIOR         VARCHAR2(20 BYTE),
  ID_OPERAZIONE_ANPR        NUMBER,
  ID_SENTENZA_PATRIMONIALE  NUMBER,
  FLAG_ANPR                 VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.MATRIMONIO IS 'Tabella contenente le informazioni sull''atto di  matrimonio di due soggetti.';

COMMENT ON COLUMN ANAG_USR.MATRIMONIO.ID_MATRIMONIO IS 'Identificativo del matrimonio';

COMMENT ON COLUMN ANAG_USR.MATRIMONIO.ORDINE_MATRIMONIO IS 'Ordine del matrimonio';

COMMENT ON COLUMN ANAG_USR.MATRIMONIO.DATA_EVENTO IS 'Data della celebrazione del matrimonio';

COMMENT ON COLUMN ANAG_USR.MATRIMONIO.LUOGO_ECCEZIONALE IS 'Descrizione del luogo eccezionale (luogo diverso da comune o località) in cui si è svolto il matrmonio. ';

COMMENT ON COLUMN ANAG_USR.MATRIMONIO.ID_LOCALITA IS 'Identificativo della località di celebrazione dell''evento';

COMMENT ON COLUMN ANAG_USR.MATRIMONIO.ID_SCELTA_PATRIMONIALE IS 'Identificativo della scelta patrimoniale effettuata dai coniugi';

COMMENT ON COLUMN ANAG_USR.MATRIMONIO.ID_SOGGETTO_MARITO IS 'Id soggetto del marito';

COMMENT ON COLUMN ANAG_USR.MATRIMONIO.ID_SOGGETTO_MOGLIE IS 'Id soggetto della moglie';

COMMENT ON COLUMN ANAG_USR.MATRIMONIO.ID_COMUNE IS 'Identificativo del comune di celebrazione';

COMMENT ON COLUMN ANAG_USR.MATRIMONIO.ID_ATTO IS 'FK alle informazioni specifiche e relative all''atto di matrimonio.';

COMMENT ON COLUMN ANAG_USR.MATRIMONIO.ID_MATRIMONIO_ANPR IS 'Identificativo matrimonio associato da Anpr';

COMMENT ON COLUMN ANAG_USR.MATRIMONIO.FLG_SENZA_GIORNO IS 'se 1 allora data evento non ha giorno ma data fittizia';

COMMENT ON COLUMN ANAG_USR.MATRIMONIO.FLG_SENZA_MESE IS 'se 1 allora data evento non ha giorno e mese ma data fittizia';

COMMENT ON COLUMN ANAG_USR.MATRIMONIO.COD_COMUNE_AGGIOR IS 'identificativo aggior del comune salvato in LUOGO_ECCEZIONALE';

COMMENT ON COLUMN ANAG_USR.MATRIMONIO.ID_OPERAZIONE_ANPR IS 'Identificativo dell''operazione ANPR, da valorizzare solo nel momento della creazione';

COMMENT ON COLUMN ANAG_USR.MATRIMONIO.ID_SENTENZA_PATRIMONIALE IS 'Identificativo della sentenza patrimoniale';

COMMENT ON COLUMN ANAG_USR.MATRIMONIO.FLAG_ANPR IS 'N -> il matrimonio NON è stato inviato ad ANPR (doppione in fase di subentro)';



CREATE INDEX ANAG_USR.IDX_MATRIMONIO_CONIUGI ON ANAG_USR.MATRIMONIO
(NVL("FLAG_ANPR",'NULL'), ID_SOGGETTO_MARITO, ID_SOGGETTO_MOGLIE, DATA_EVENTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE INDEX ANAG_USR.IDX_MATRIMONIO_DATAEVENTO ON ANAG_USR.MATRIMONIO
(DATA_EVENTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.MATRIMONIO_PK ON ANAG_USR.MATRIMONIO
(ID_MATRIMONIO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE INDEX ANAG_STORICO.SID_ID_ATTO_IDX ON ANAG_USR.MATRIMONIO
(ID_ATTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE INDEX ANAG_STORICO.SID_SOG_MARITO_IDX ON ANAG_USR.MATRIMONIO
(ID_SOGGETTO_MARITO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE INDEX ANAG_STORICO.SID_SOG_MOGLIE_IDX ON ANAG_USR.MATRIMONIO
(ID_SOGGETTO_MOGLIE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.MATRIMONIO ADD (
  CONSTRAINT MATRIMONIO_PK
  PRIMARY KEY
  (ID_MATRIMONIO)
  USING INDEX ANAG_USR.MATRIMONIO_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.MATRIMONIO ADD (
  CONSTRAINT ATTO_FK 
  FOREIGN KEY (ID_ATTO) 
  REFERENCES ANAG_USR.ATTO (ID_ATTO)
  ENABLE VALIDATE,
  CONSTRAINT COMUNE_FKV3 
  FOREIGN KEY (ID_COMUNE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT CONF_SCELTA_PATRIMONIALE_FK 
  FOREIGN KEY (ID_SCELTA_PATRIMONIALE) 
  REFERENCES ANAG_USR.CONF_SCELTA_PATRIMONIALE (ID)
  ENABLE VALIDATE,
  CONSTRAINT LOCALITA_FK 
  FOREIGN KEY (ID_LOCALITA) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE,
  CONSTRAINT SENTENZA_PAT_FK 
  FOREIGN KEY (ID_SENTENZA_PATRIMONIALE) 
  REFERENCES ANAG_USR.SENTENZA (ID_SENTENZA)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_MARITO_FK 
  FOREIGN KEY (ID_SOGGETTO_MARITO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_MOGLIE_FK 
  FOREIGN KEY (ID_SOGGETTO_MOGLIE) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.MORTE
(
  ID_MORTE                      NUMBER          NOT NULL,
  ORDINE_MATRIMONIO_PRECEDENTE  NUMBER,
  DATA_EVENTO                   DATE,
  FLG_SENZA_GIORNO              CHAR(1 CHAR),
  FLG_SENZA_MESE                CHAR(1 CHAR),
  LUOGO_ECCEZIONALE             VARCHAR2(120 CHAR),
  ID_LOCALITA                   NUMBER,
  ID_COMUNE                     NUMBER,
  ID_ATTO                       NUMBER,
  CAUSA_DECESSO                 VARCHAR2(500 BYTE),
  COD_COMUNE_AGGIOR             VARCHAR2(20 BYTE),
  ID_SENTENZA                   NUMBER,
  ID_TIPO_MORTE                 NUMBER,
  MOTIVAZIONE_ANNULLAMENTO      VARCHAR2(500 BYTE),
  DATA_ANNULLAMENTO             DATE,
  ID_COMUNE_RESIDENZA           NUMBER,
  ID_LOCALITA_RESIDENZA         NUMBER,
  LUOGO_ECCEZIONALE_RESIDENZA   VARCHAR2(200 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.MORTE IS 'Tabella contenente le informazioni sull''atto di morte di un soggetto';

COMMENT ON COLUMN ANAG_USR.MORTE.ID_MORTE IS 'Identificativo del decesso';

COMMENT ON COLUMN ANAG_USR.MORTE.ORDINE_MATRIMONIO_PRECEDENTE IS 'Ordine del precedente matrimonio';

COMMENT ON COLUMN ANAG_USR.MORTE.DATA_EVENTO IS 'Data del decesso';

COMMENT ON COLUMN ANAG_USR.MORTE.FLG_SENZA_GIORNO IS 'S -> Non è presente il giorno del decesso
N -> E'' presente il giorno del decesso';

COMMENT ON COLUMN ANAG_USR.MORTE.FLG_SENZA_MESE IS 'S -> non è presente il mese del decesso
N -> è presente il mese del decesso';

COMMENT ON COLUMN ANAG_USR.MORTE.LUOGO_ECCEZIONALE IS 'Luogo eccezionale';

COMMENT ON COLUMN ANAG_USR.MORTE.ID_LOCALITA IS 'Identificativo della località relativa al decesso';

COMMENT ON COLUMN ANAG_USR.MORTE.ID_COMUNE IS 'Identificativo del comune relativo al decesso';

COMMENT ON COLUMN ANAG_USR.MORTE.ID_ATTO IS 'FK relativa all''atto di decesso';

COMMENT ON COLUMN ANAG_USR.MORTE.COD_COMUNE_AGGIOR IS 'identificativo aggior del comune salvato in LUOGO_ECCEZIONALE';

COMMENT ON COLUMN ANAG_USR.MORTE.MOTIVAZIONE_ANNULLAMENTO IS 'Motivo per cui è stata annullata la morte.';

COMMENT ON COLUMN ANAG_USR.MORTE.DATA_ANNULLAMENTO IS 'Data in cui è stata annullata la morte.';

COMMENT ON COLUMN ANAG_USR.MORTE.ID_COMUNE_RESIDENZA IS 'Identificato del comune di residenza al decesso. Valorizzato per i soggetti che non sono vivi residenti o vivi AIRE';



CREATE INDEX ANAG_USR.IDX_MORTE_IDATTO ON ANAG_USR.MORTE
(ID_ATTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.MORTE_PK ON ANAG_USR.MORTE
(ID_MORTE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.MORTE ADD (
  CONSTRAINT MORTE_PK
  PRIMARY KEY
  (ID_MORTE)
  USING INDEX ANAG_USR.MORTE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.MORTE ADD (
  CONSTRAINT COMUNE_RESIDENZA_FK 
  FOREIGN KEY (ID_COMUNE_RESIDENZA) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT CONF_TIPO_MORTE_FK 
  FOREIGN KEY (ID_TIPO_MORTE) 
  REFERENCES ANAG_USR.CONF_TIPO_MORTE (ID_TIPO_MORTE)
  ENABLE VALIDATE,
  CONSTRAINT LOCALITA_RESIDENZA_FK 
  FOREIGN KEY (ID_LOCALITA_RESIDENZA) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE,
  CONSTRAINT SENTENZA_FK 
  FOREIGN KEY (ID_SENTENZA) 
  REFERENCES ANAG_USR.SENTENZA (ID_SENTENZA)
  ENABLE VALIDATE,
  CONSTRAINT VEDOVANZA_ATTO_FK 
  FOREIGN KEY (ID_ATTO) 
  REFERENCES ANAG_USR.ATTO (ID_ATTO)
  ENABLE VALIDATE,
  CONSTRAINT VEDOVANZA_COMUNE_FK 
  FOREIGN KEY (ID_COMUNE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT VEDOVANZA_LOCALITA_FK 
  FOREIGN KEY (ID_LOCALITA) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.NASCITA
(
  ID_NASCITA                 NUMBER             NOT NULL,
  DATA_EVENTO                DATE,
  FLG_SENZA_GIORNO           CHAR(1 CHAR),
  FLG_SENZA_MESE             CHAR(1 CHAR),
  LUOGO_ECCEZIONALE          VARCHAR2(120 CHAR),
  ID_LOCALITA                NUMBER,
  ID_COMUNE                  NUMBER,
  ID_ATTO                    NUMBER,
  NOMINATIVO_PATERNITA       VARCHAR2(200 CHAR),
  NOMINATIVO_MATERNITA       VARCHAR2(200 CHAR),
  COD_COMUNE_AGGIOR          VARCHAR2(20 BYTE),
  NOMINATIVO_PADRE_ADOTTIVO  VARCHAR2(200 BYTE),
  NOMINATIVO_MADRE_ADOTTIVA  VARCHAR2(200 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.NASCITA IS 'Tabella contenente le informazioni sulla nascita di un soggetto.';

COMMENT ON COLUMN ANAG_USR.NASCITA.ID_NASCITA IS 'Identificato della nascita';

COMMENT ON COLUMN ANAG_USR.NASCITA.DATA_EVENTO IS 'Data di nascita';

COMMENT ON COLUMN ANAG_USR.NASCITA.FLG_SENZA_GIORNO IS 'S -> non è presente il giorno di nascita
N -> è presente il giorno di nascita';

COMMENT ON COLUMN ANAG_USR.NASCITA.FLG_SENZA_MESE IS 'S -> non è presente il mese di nascita
N -> è presente il mese di nascita';

COMMENT ON COLUMN ANAG_USR.NASCITA.LUOGO_ECCEZIONALE IS 'Luogo eccezionale di nascita';

COMMENT ON COLUMN ANAG_USR.NASCITA.ID_LOCALITA IS 'Identificativo della località di nascita';

COMMENT ON COLUMN ANAG_USR.NASCITA.ID_COMUNE IS 'Identificativo del comune di nascita';

COMMENT ON COLUMN ANAG_USR.NASCITA.ID_ATTO IS 'FK all''atto di nascita';

COMMENT ON COLUMN ANAG_USR.NASCITA.NOMINATIVO_PATERNITA IS 'Nominativo del padre qualora non sia un soggetto presente in banca dati all''interno della tabella soggetto';

COMMENT ON COLUMN ANAG_USR.NASCITA.NOMINATIVO_MATERNITA IS 'Nominativo della madre qualora non sia un soggetto presente in banca dati all''interno della tabella soggetto';

COMMENT ON COLUMN ANAG_USR.NASCITA.COD_COMUNE_AGGIOR IS 'identificativo aggior del comune salvato in LUOGO_ECCEZIONALE';

COMMENT ON COLUMN ANAG_USR.NASCITA.NOMINATIVO_PADRE_ADOTTIVO IS 'Nominativo padre adottivo';

COMMENT ON COLUMN ANAG_USR.NASCITA.NOMINATIVO_MADRE_ADOTTIVA IS 'Nominativo madre adottivo';



CREATE INDEX ANAG_USR.NASCITA_IDATTO ON ANAG_USR.NASCITA
(ID_ATTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.NASCITA_PK ON ANAG_USR.NASCITA
(ID_NASCITA)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.NASCITA FOR ANAG_USR.NASCITA;


ALTER TABLE ANAG_USR.NASCITA ADD (
  CONSTRAINT NASCITA_PK
  PRIMARY KEY
  (ID_NASCITA)
  USING INDEX ANAG_USR.NASCITA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.NASCITA ADD (
  CONSTRAINT NASCITA_ATTO_FK 
  FOREIGN KEY (ID_ATTO) 
  REFERENCES ANAG_USR.ATTO (ID_ATTO)
  DISABLE NOVALIDATE,
  CONSTRAINT NASCITA_COMUNE_FK 
  FOREIGN KEY (ID_COMUNE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT NASCITA_LOCALITA_FK 
  FOREIGN KEY (ID_LOCALITA) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.PATENTE
(
  NUMERO_PATENTE            VARCHAR2(40 CHAR)   NOT NULL,
  ID_STATO_VALIDITA         NUMBER(1),
  DATA_RILASCIO             DATE,
  ID_COMUNE                 NUMBER,
  ID_ENTE_RILASCIO_PATENTE  NUMBER(2)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.PATENTE IS 'Tabella contenente le informazioni sulle patenti possedute da un soggetto';

COMMENT ON COLUMN ANAG_USR.PATENTE.NUMERO_PATENTE IS 'Numero identificativo di una patente di guida.';

COMMENT ON COLUMN ANAG_USR.PATENTE.ID_STATO_VALIDITA IS 'Stato di validità della patemte di guida.';

COMMENT ON COLUMN ANAG_USR.PATENTE.DATA_RILASCIO IS 'Data in cui è stata rilasciata la partente di guida.';

COMMENT ON COLUMN ANAG_USR.PATENTE.ID_COMUNE IS 'Comune dell''ente di rilascio della patente di guida.';

COMMENT ON COLUMN ANAG_USR.PATENTE.ID_ENTE_RILASCIO_PATENTE IS 'identificativo dell''ente di rilascio della patente di guida';



CREATE UNIQUE INDEX ANAG_USR.PATENTE_PK ON ANAG_USR.PATENTE
(NUMERO_PATENTE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.PATENTE ADD (
  CONSTRAINT PATENTE_PK
  PRIMARY KEY
  (NUMERO_PATENTE)
  USING INDEX ANAG_USR.PATENTE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.PATENTE ADD (
  CONSTRAINT CONF_ENTE_RILASCIO_PATENTE_FK 
  FOREIGN KEY (ID_ENTE_RILASCIO_PATENTE) 
  REFERENCES ANAG_USR.CONF_ENTE_RILASCIO_PATENTE (ID_ENTE_RILASCIO_PATENTE)
  ENABLE VALIDATE,
  CONSTRAINT CONF_STATO_VALIDITA_PATENT_FK 
  FOREIGN KEY (ID_STATO_VALIDITA) 
  REFERENCES ANAG_USR.CONF_STATO_VALIDITA_PATENTE (ID_STATO_VALIDITA_PATENTE)
  ENABLE VALIDATE,
  CONSTRAINT PATENTE_COMUNE_FK 
  FOREIGN KEY (ID_COMUNE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.PENSIONE
(
  NUMERO_LIBRETTO   VARCHAR2(4000 BYTE)         NOT NULL,
  ID_CATEGORIA      VARCHAR2(20 BYTE),
  ID_ENTE_RILASCIO  NUMBER(2),
  SEDE              VARCHAR2(4000 BYTE),
  DATA_INSERIMENTO  DATE,
  ID_SOGGETTO       NUMBER,
  DATA_STAMPA       DATE,
  ID_PENSIONE       NUMBER                      NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.PENSIONE IS 'Tabella contente le informazioni sul libretto di pensione associato ad un soggetto.';

COMMENT ON COLUMN ANAG_USR.PENSIONE.NUMERO_LIBRETTO IS 'Numero del libretto pensionistico';

COMMENT ON COLUMN ANAG_USR.PENSIONE.ID_CATEGORIA IS 'categoria del libretto pensionistico';

COMMENT ON COLUMN ANAG_USR.PENSIONE.ID_ENTE_RILASCIO IS 'ente che ha rilasciato ill libretto pensionistico';

COMMENT ON COLUMN ANAG_USR.PENSIONE.SEDE IS 'Sede dell''INPS che gestisce la pratica pensionistica';

COMMENT ON COLUMN ANAG_USR.PENSIONE.DATA_INSERIMENTO IS 'data in cui il libertto pensionistico è stato associato al soggetto';

COMMENT ON COLUMN ANAG_USR.PENSIONE.ID_SOGGETTO IS 'identificativo del soggetto a cui è associato il libretto pensionistico';

COMMENT ON COLUMN ANAG_USR.PENSIONE.DATA_STAMPA IS 'data di stampa del libretto pensionistico';

COMMENT ON COLUMN ANAG_USR.PENSIONE.ID_PENSIONE IS 'identificativo del libretto pensionistico';



CREATE UNIQUE INDEX ANAG_USR.PENSIONE_PK ON ANAG_USR.PENSIONE
(ID_PENSIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.PENSIONE ADD (
  CONSTRAINT PENSIONE_PK
  PRIMARY KEY
  (ID_PENSIONE)
  USING INDEX ANAG_USR.PENSIONE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.PENSIONE ADD (
  CONSTRAINT CONF_CATEGORIA_PENSIONE_FF 
  FOREIGN KEY (ID_CATEGORIA) 
  REFERENCES ANAG_USR.CONF_CATEGORIA_PENSIONE (ID_CATEGORIA)
  ENABLE VALIDATE,
  CONSTRAINT CONF_ENTE_RILASCIO_PENSION_FK 
  FOREIGN KEY (ID_ENTE_RILASCIO) 
  REFERENCES ANAG_USR.CONF_ENTE_RILASCIO_PENSIONE (ID_ENTE_RILASCIO_PENSIONE)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_PENS_FK 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.PRATICA_AIRE
(
  ID_PRATICA_AIRE               NUMBER          NOT NULL,
  ID_STATO_PRATICA              NUMBER          NOT NULL,
  DATA_INVIO_MODELLO            DATE            NOT NULL,
  ID_CONSOLATO                  NUMBER          NOT NULL,
  CODICE_TIPO_PROTOCOLLO        VARCHAR2(10 CHAR),
  ANNO_PROTOCOLLO               NUMBER,
  NUMERO_PROTOCOLLO             NUMBER,
  NUMERO_PRATICA                VARCHAR2(200 BYTE),
  ANNO_PRATICA                  NUMBER,
  ID_RESIDENZA                  NUMBER,
  ID_OGGETTO_PRATICA_AIRE       NUMBER,
  ID_MOTIVO_CAMBIO_PRATICAAIRE  NUMBER,
  ID_SOGGETTO_RESIDENTE         NUMBER,
  DATA_DECORRENZA               DATE,
  UTENTE_PROTOCOLLAZIONE        VARCHAR2(100 BYTE),
  UTENTE_LAVORAZIONE            VARCHAR2(100 BYTE),
  DATA_LAVORAZIONE              DATE,
  FLAG_SELEZIONE_FAMIGLIA       VARCHAR2(1 BYTE),
  DATA_CREAZIONE_PRATICA        DATE,
  ID_FAMIGLIA                   NUMBER,
  NUMERO_PRATICA_CRE            VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.PRATICA_AIRE IS 'Tabella contenente le informazioni sulle pratiche di iscrizione o cancellazione dalle liste dell''AIRE.';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.ID_PRATICA_AIRE IS 'Identificativo pratica aire';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.ID_STATO_PRATICA IS 'Stato della pratica AIRE';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.DATA_INVIO_MODELLO IS 'Data di invio del modello consolare';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.ID_CONSOLATO IS 'FK alla tabella dei consolati di riferimento per la pratica aire';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.CODICE_TIPO_PROTOCOLLO IS 'Codice del protocollo acquisito per la richiesta di Iscrizione o Cancellazione AIRE';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.ANNO_PROTOCOLLO IS 'Anno del protocollo acquisito per la richiesta di Iscrizione o Cancellazione AIRE';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.NUMERO_PROTOCOLLO IS 'Numero del protocollo acquisito per la richiesta di Iscrizione o Cancellazione AIRE';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.NUMERO_PRATICA IS 'Numero della pratica';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.ANNO_PRATICA IS 'Anno della pratica';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.ID_RESIDENZA IS 'Identificato della residenza associata alla pratica AIRE';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.ID_OGGETTO_PRATICA_AIRE IS 'Identificativo dell''oggetto della pratica AIRE';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.ID_MOTIVO_CAMBIO_PRATICAAIRE IS 'Identificativo del motivo del cambio di pratica AIRE';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.ID_SOGGETTO_RESIDENTE IS 'Identificativo del soggetto residente';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.DATA_DECORRENZA IS 'Data di decorrenza dalla pratica AIRE';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.UTENTE_PROTOCOLLAZIONE IS 'Nome dell''utente che protocolla la pratica';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.UTENTE_LAVORAZIONE IS 'Nome dell''utente che lavora la pratica';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.DATA_LAVORAZIONE IS 'Data dell''avvenuta lavorazione della pratica AIRE';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.FLAG_SELEZIONE_FAMIGLIA IS 'Flag che tiene conto se nella pratica AIRE è sta selezionata una nuova famiglia o una già esistente. In caso affermativo il campo è selezionato, altrimenti rimane vuoto';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.DATA_CREAZIONE_PRATICA IS 'Data di creazione della pratica';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.ID_FAMIGLIA IS 'Identificativo della famiglia AIRE';

COMMENT ON COLUMN ANAG_USR.PRATICA_AIRE.NUMERO_PRATICA_CRE IS 'Numero pratica emigrazione se almeno uno dei soggetti è iscritto per espatrio';



CREATE UNIQUE INDEX ANAG_USR.PRATICA_AIRE_PK ON ANAG_USR.PRATICA_AIRE
(ID_PRATICA_AIRE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.PRATICA_AIRE ADD (
  CONSTRAINT PRATICA_AIRE_PK
  PRIMARY KEY
  (ID_PRATICA_AIRE)
  USING INDEX ANAG_USR.PRATICA_AIRE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.PRATICA_AIRE ADD (
  CONSTRAINT CONF_MOTIVAZIONI_AIRE_FK 
  FOREIGN KEY (ID_MOTIVO_CAMBIO_PRATICAAIRE) 
  REFERENCES ANAG_USR.CONF_MOTIVO_CAMBIO_PRATICAAIRE (ID_MOTIVO_CAMBIO_PRATICAAIRE)
  ENABLE VALIDATE,
  CONSTRAINT CONF_STATO_PRATICA_FKV6 
  FOREIGN KEY (ID_STATO_PRATICA) 
  REFERENCES ANAG_USR.CONF_STATO_PRATICA (ID_STATO_PRATICA)
  ENABLE VALIDATE,
  CONSTRAINT CONSOLATO_FK 
  FOREIGN KEY (ID_CONSOLATO) 
  REFERENCES ANAG_USR.CONSOLATO (ID_CONSOLATO)
  ENABLE VALIDATE,
  CONSTRAINT FKIXGQ1M0B3DVUN55Q74RPWQNVI 
  FOREIGN KEY (ID_SOGGETTO_RESIDENTE) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT PRATICA_AIRE_FK1 
  FOREIGN KEY (ID_RESIDENZA) 
  REFERENCES ANAG_USR.RESIDENZA (ID_RESIDENZA)
  ENABLE VALIDATE,
  CONSTRAINT PRATICA_AIRE_FK2 
  FOREIGN KEY (ID_OGGETTO_PRATICA_AIRE) 
  REFERENCES ANAG_USR.OGGETTO_PRATICA_AIRE (ID_OGGETTO_PRATICA_AIRE)
  ENABLE VALIDATE,
  CONSTRAINT PRATICA_AIRE_FK3 
  FOREIGN KEY (CODICE_TIPO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE,
  CONSTRAINT PRATICA_AIRE_FK4 
  FOREIGN KEY (ID_FAMIGLIA) 
  REFERENCES ANAG_USR.FAMIGLIA_CONVIVENZA (ID_FAMIGLIA_CONV)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_CERTIFICATO_IMPORTO
(
  ID_CERTIFICATO   NUMBER                       NOT NULL,
  ID_POSIZIONE     NUMBER                       NOT NULL,
  IUV              VARCHAR2(200 CHAR),
  DATA_RICHIESTA   DATE,
  DATA_PAGAMENTO   DATE,
  ID               NUMBER                       NOT NULL,
  OPE_RIC_IUV      VARCHAR2(200 BYTE),
  DATA_BOLLETTINO  DATE,
  OPE_BOLLETTINO   VARCHAR2(200 BYTE),
  OPE_PAGAMENTO    VARCHAR2(200 BYTE),
  XML_POSIZIONE    CLOB,
  ID_PRATICA_CERT  NUMBER
)
LOB (XML_POSIZIONE) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.R_CERTIFICATO_IMPORTO IS 'Tabella di relazione che associa ad un certificato eventuali importi da pagare per la sua emissione. Ad ogni importo è associato lo IUV rilasciato dal sistema SIR.';

COMMENT ON COLUMN ANAG_USR.R_CERTIFICATO_IMPORTO.ID_CERTIFICATO IS 'Identificato del certificato richiesto';

COMMENT ON COLUMN ANAG_USR.R_CERTIFICATO_IMPORTO.ID_POSIZIONE IS 'Identificativo dell''importo dovuto per il certificato';

COMMENT ON COLUMN ANAG_USR.R_CERTIFICATO_IMPORTO.IUV IS 'Identificativo univo del versamento rilasciato dal sistema SIR';



CREATE UNIQUE INDEX ANAG_USR.R_CERTIFICATO_IMPORTO_PK ON ANAG_USR.R_CERTIFICATO_IMPORTO
(ID_CERTIFICATO, ID_POSIZIONE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.R_CERTIFICATO_IMPORTO_PK1 ON ANAG_USR.R_CERTIFICATO_IMPORTO
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.UK_94WD07NYHP99MLUAKK46SHOQC ON ANAG_USR.R_CERTIFICATO_IMPORTO
(ID_CERTIFICATO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_CERTIFICATO_IMPORTO ADD (
  CONSTRAINT R_CERTIFICATO_IMPORTO_PK1
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.R_CERTIFICATO_IMPORTO_PK1
  ENABLE VALIDATE,
  CONSTRAINT UK_94WD07NYHP99MLUAKK46SHOQC
  UNIQUE (ID_CERTIFICATO)
  USING INDEX ANAG_USR.UK_94WD07NYHP99MLUAKK46SHOQC
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_CERTIFICATO_IMPORTO ADD (
  CONSTRAINT R_CERTIFICATO_IMPORTO_FK 
  FOREIGN KEY (ID_CERTIFICATO) 
  REFERENCES ANAG_USR.CERTIFICATI (ID_CERTIFICATO)
  ENABLE VALIDATE,
  CONSTRAINT R_CERTIFICATO_IMPORTO_FK1 
  FOREIGN KEY (ID_POSIZIONE) 
  REFERENCES ANAG_USR.CONF_POSIZIONI (ID)
  ENABLE VALIDATE,
  CONSTRAINT R_CERTIFICATO_IMPORTO_FK2 
  FOREIGN KEY (ID_PRATICA_CERT) 
  REFERENCES ANAG_USR.PRATICA_CERTIFICATI (ID_PRATICA_CERTIFICATI)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.RESIDENZA
(
  ID_RESIDENZA               NUMBER             NOT NULL,
  TIPO_INDIRIZZO             NUMBER(2),
  NOTE_INDIRIZZO             VARCHAR2(250 BYTE),
  CAP                        VARCHAR2(20 CHAR),
  FRAZIONE                   VARCHAR2(80 BYTE),
  ID_LOCALITA                NUMBER,
  ID_COMUNE                  NUMBER,
  ID_TOPONIMO                NUMBER,
  ID_CIVICO                  NUMBER,
  LUOGO_ECCEZIONALE          VARCHAR2(250 BYTE),
  ID_MUNICIPIO               NUMBER             DEFAULT 1,
  DATA_DECORRENZA_RESIDENZA  DATE,
  ID_ESTREMI_CATASTALI       NUMBER,
  ID_CIVICO_INTERNO          NUMBER,
  COD_COMUNE_AGGIOR          VARCHAR2(20 BYTE),
  ID_CONSOLATO               NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.RESIDENZA IS 'Tabella contenente gli estremi della residenza di un soggetto.';

COMMENT ON COLUMN ANAG_USR.RESIDENZA.ID_RESIDENZA IS 'Campo che indica l''id della residenza.';

COMMENT ON COLUMN ANAG_USR.RESIDENZA.TIPO_INDIRIZZO IS 'Tipologia dell''indirizzo';

COMMENT ON COLUMN ANAG_USR.RESIDENZA.NOTE_INDIRIZZO IS 'Campo che indica le note sull''idirizzo.';

COMMENT ON COLUMN ANAG_USR.RESIDENZA.CAP IS 'Campo che indica il cap dell''idirizzo.';

COMMENT ON COLUMN ANAG_USR.RESIDENZA.FRAZIONE IS 'Campo che indica la frazione del comune.';

COMMENT ON COLUMN ANAG_USR.RESIDENZA.ID_LOCALITA IS 'Codice identificativo della licalità estera in cui è collocata la residenza.

Da inserire in alternativa al comune di residenza.';

COMMENT ON COLUMN ANAG_USR.RESIDENZA.ID_COMUNE IS 'Campo che indica il codice identificatvo del comune.

Da inserire in alternativa alla località estera di residenza.';

COMMENT ON COLUMN ANAG_USR.RESIDENZA.ID_TOPONIMO IS 'Campo che indica il codice identificatIvo del toponimo.';

COMMENT ON COLUMN ANAG_USR.RESIDENZA.ID_CIVICO IS 'Campo che indica il codice identificatvo del civico.';

COMMENT ON COLUMN ANAG_USR.RESIDENZA.LUOGO_ECCEZIONALE IS 'Campo che indica il luogo eccezionale dell''idirizzo.';

COMMENT ON COLUMN ANAG_USR.RESIDENZA.ID_MUNICIPIO IS 'Identificativo del municipio della residenza';

COMMENT ON COLUMN ANAG_USR.RESIDENZA.DATA_DECORRENZA_RESIDENZA IS 'Data in cui la residenza è stata creata e associata al soggetto e/o al cambioResidenzaDomicilio';

COMMENT ON COLUMN ANAG_USR.RESIDENZA.ID_ESTREMI_CATASTALI IS 'Campo che indica gli estremi catastali dell''abitazione';

COMMENT ON COLUMN ANAG_USR.RESIDENZA.ID_CIVICO_INTERNO IS 'FK verso la tabella che contiene i civici interni';

COMMENT ON COLUMN ANAG_USR.RESIDENZA.COD_COMUNE_AGGIOR IS 'identificativo aggior del comune salvato in LUOGO_ECCEZIONALE';

COMMENT ON COLUMN ANAG_USR.RESIDENZA.ID_CONSOLATO IS 'Identificativo relativo al consolato di appartenenza AIRE';



CREATE UNIQUE INDEX ANAG_USR.RESIDENZA_PK ON ANAG_USR.RESIDENZA
(ID_RESIDENZA)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.RESIDENZA FOR ANAG_USR.RESIDENZA;


ALTER TABLE ANAG_USR.RESIDENZA ADD (
  CONSTRAINT RESIDENZA_PK
  PRIMARY KEY
  (ID_RESIDENZA)
  USING INDEX ANAG_USR.RESIDENZA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.RESIDENZA ADD (
  CONSTRAINT ESTREMI_CATASTALI_FK3 
  FOREIGN KEY (ID_ESTREMI_CATASTALI) 
  REFERENCES ANAG_USR.ESTREMI_CATASTALI (ID_ESTREMI_CATASTALI)
  ENABLE VALIDATE,
  CONSTRAINT RESIDENZA_CIVICO_FK 
  FOREIGN KEY (ID_CIVICO) 
  REFERENCES ANAG_USR.CIVICO (ID_CIVICO)
  ENABLE VALIDATE,
  CONSTRAINT RESIDENZA_COMUNE_FK 
  FOREIGN KEY (ID_COMUNE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT RESIDENZA_FK1 
  FOREIGN KEY (ID_MUNICIPIO) 
  REFERENCES ANAG_USR.CONF_MUNICIPIO (ID_MUNICIPIO)
  ENABLE VALIDATE,
  CONSTRAINT RESIDENZA_FK2 
  FOREIGN KEY (TIPO_INDIRIZZO) 
  REFERENCES ANAG_USR.CONF_TIPO_INDIRIZZO (ID_TIPO_INDIRIZZO)
  ENABLE VALIDATE,
  CONSTRAINT RESIDENZA_FK3 
  FOREIGN KEY (ID_CIVICO_INTERNO) 
  REFERENCES ANAG_USR.CIVICO_INTERNO (ID_CIVICO_INTERNO)
  ENABLE VALIDATE,
  CONSTRAINT RESIDENZA_LOCALITA_FK 
  FOREIGN KEY (ID_LOCALITA) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE,
  CONSTRAINT RESIDENZA_TOPONIMO_FK 
  FOREIGN KEY (ID_TOPONIMO) 
  REFERENCES ANAG_USR.TOPONIMO (ID_TOPONIMO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_SOGGETTI_AIRE
(
  ID_SOGGETTO                   NUMBER          NOT NULL,
  ID_PRATICA_AIRE               NUMBER          NOT NULL,
  FLG_LAVORATO                  CHAR(1 CHAR),
  ID_TIPO_PRATICA_AIRE          NUMBER,
  ID_MOTIVO_PERDITA_CITTADIN    NUMBER,
  ID_MOTIVO_ACQUISIZ_CITTADIN   NUMBER,
  NOTE                          VARCHAR2(1000 BYTE),
  ID_COMUNE_DUP_ISCR            NUMBER,
  DATA_DUPLICE_ISCRIZIONE       DATE,
  ID_COMUNE_IRREPERIBILITA      NUMBER,
  DATA_IRREPERIBILITA           DATE,
  ID_COMUNE_TRASFERIMENTO_AIRE  NUMBER,
  DATA_TRASFERIMENTO_AIRE       DATE,
  ID_NUOVA_CITTADINANZA         NUMBER,
  ID_INDIVIDUAZIONE_COMUNE      NUMBER,
  ID_INIZIATIVA_ISCRIZIONE      NUMBER,
  DATA_EMIGRAZIONE              DATE,
  CRITERIO_VALIDAZIONE_CF_ANPR  NUMBER,
  FLG_LAVORATO_ANPR             CHAR(1 BYTE),
  ID_VECCHIO_CODICE_LEGAME      NUMBER,
  ID_FAMIGLIA_PROVENIENZA       NUMBER,
  ID_RESIDENZA_PROVENIENZA      NUMBER,
  FLAG_SOGGETTO_NUOVO           VARCHAR2(1 BYTE),
  FLAG_PREC_AIRE                VARCHAR2(1 BYTE),
  ID_NUOVO_CODICE_LEGAME        NUMBER,
  ID_IRREPERIBILITA_CHIUSA      NUMBER,
  FLAG_DUPC_ISCR_DIFFERENTE     VARCHAR2(1 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.R_SOGGETTI_AIRE IS 'Tabella di relazione che contiene l''indicazione dei soggetti afferenti ad una determinata pratica AIRE';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.ID_SOGGETTO IS 'Id dell''individuo che ha avviato una pratica AIRE';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.ID_PRATICA_AIRE IS 'Identificativo della pratica dell''AIRE';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.FLG_LAVORATO IS 'S -> Soggetto Lavorato
N -> Soggetto da lavorare';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.ID_TIPO_PRATICA_AIRE IS 'Identificativo alla tipologia di pratica AIRE';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.ID_MOTIVO_PERDITA_CITTADIN IS 'Identificativo delmotivo di perdità della cittadinanza';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.ID_MOTIVO_ACQUISIZ_CITTADIN IS 'Identificativo delmotivo di acquisizione della cittadinanza';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.NOTE IS 'Note sul motivo di perdita o acquisizione della cittadinanza';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.ID_COMUNE_DUP_ISCR IS 'Identificativo del comune di duplice iscrizione';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.DATA_DUPLICE_ISCRIZIONE IS 'Data di decorrenza per duplice iscrizione';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.ID_COMUNE_IRREPERIBILITA IS 'Identificativo del comunedi irreperibilità';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.DATA_IRREPERIBILITA IS 'Data di irreperibilità';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.ID_COMUNE_TRASFERIMENTO_AIRE IS 'Identificativo del comune di precedente iscrizione per trasferimento da altra AIRE';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.DATA_TRASFERIMENTO_AIRE IS 'Data di decorrenza per trasferimento da altra AIRE';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.ID_NUOVA_CITTADINANZA IS 'Identificativo della nuova cittadinanza';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.ID_INDIVIDUAZIONE_COMUNE IS 'Identificativo dell''individuazione del comune di iscrizione AIRE';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.ID_INIZIATIVA_ISCRIZIONE IS 'Identificativo dell''iniziativa di iscrizione AIRE';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.DATA_EMIGRAZIONE IS 'Data dell''effettiva emigrazione del soggetto AIRE';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.CRITERIO_VALIDAZIONE_CF_ANPR IS 'Campo che identifica il criterio di validazione del cf per anpr.';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.FLG_LAVORATO_ANPR IS 'Campo che identifica se il soggetto è stato già lavorato su ANPR o meno';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.ID_VECCHIO_CODICE_LEGAME IS 'Identificativo del vecchio legame di parentela del soggetto';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.ID_FAMIGLIA_PROVENIENZA IS 'Identificativo della famiglia di provenienza';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.ID_RESIDENZA_PROVENIENZA IS 'Identificativo della residenza di provenienza';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.FLAG_SOGGETTO_NUOVO IS 'S -> Soggetto nuovo, R -> Soggetto esistente residente, A -> Soggetto AIRE, N -> Soggetto esistente non residente';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.FLAG_PREC_AIRE IS 'S -> Soggetto già stato AIRE in precedenza, N -> Soggetto mai stato AIRE';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.ID_NUOVO_CODICE_LEGAME IS 'Identificativo del nuovo legame di parentela del soggetto';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.ID_IRREPERIBILITA_CHIUSA IS 'Identificativo dell''irrepribilità chiusa con l''iscrizione AIRE';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTI_AIRE.FLAG_DUPC_ISCR_DIFFERENTE IS 'N -> Anagrafiche duplici congruenti, S _> Anagrafici duplici non congruenti';



CREATE UNIQUE INDEX ANAG_USR.R_SOGGETTI_AIRE_PK ON ANAG_USR.R_SOGGETTI_AIRE
(ID_SOGGETTO, ID_PRATICA_AIRE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_SOGGETTI_AIRE ADD (
  CONSTRAINT R_SOGGETTI_AIRE_PK
  PRIMARY KEY
  (ID_SOGGETTO, ID_PRATICA_AIRE)
  USING INDEX ANAG_USR.R_SOGGETTI_AIRE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_SOGGETTI_AIRE ADD (
  CONSTRAINT ID_COMUNE_DUP_ISCR_FK 
  FOREIGN KEY (ID_COMUNE_DUP_ISCR) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT ID_COMUNE_IRREPERIBILITA_FK 
  FOREIGN KEY (ID_COMUNE_IRREPERIBILITA) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT ID_COMUNE_TRASFERIMENTO_FK 
  FOREIGN KEY (ID_COMUNE_TRASFERIMENTO_AIRE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT ID_INDIVIDUAZIONE_COMUNE_FK 
  FOREIGN KEY (ID_INDIVIDUAZIONE_COMUNE) 
  REFERENCES ANAG_USR.CONF_INDIVIDUAZIONE_COM_AIRE (ID_INDIVIDUAZIONE)
  ENABLE VALIDATE,
  CONSTRAINT ID_INIZIATIVA_ISCRIZIONE_FK 
  FOREIGN KEY (ID_INIZIATIVA_ISCRIZIONE) 
  REFERENCES ANAG_USR.CONF_INIZIATIVA_ISCR_AIRE (ID_INIZIATIVA)
  ENABLE VALIDATE,
  CONSTRAINT ID_NUOVA_CITTADINANZA_FK 
  FOREIGN KEY (ID_NUOVA_CITTADINANZA) 
  REFERENCES ANAG_USR.CITTADINANZA (ID_CITTADINANZA)
  ENABLE VALIDATE,
  CONSTRAINT ID_TIPO_PRATICA_AIRE_FK 
  FOREIGN KEY (ID_TIPO_PRATICA_AIRE) 
  REFERENCES ANAG_USR.CONF_TIPO_PRATICA_AIRE (ID_TIPO_PRATICA_AIRE)
  ENABLE VALIDATE,
  CONSTRAINT R_SOGGETTI_AIRE_FK1 
  FOREIGN KEY (ID_MOTIVO_ACQUISIZ_CITTADIN) 
  REFERENCES ANAG_USR.CONF_MOTIVO_ACQUISIZ_CITTADIN (ID_MOTIVO_ACQUISIZ_CITTADIN)
  ENABLE VALIDATE,
  CONSTRAINT R_SOGGETTI_AIRE_FK2 
  FOREIGN KEY (ID_MOTIVO_PERDITA_CITTADIN) 
  REFERENCES ANAG_USR.CONF_MOTIVO_PERDITA_CITTADIN (ID_MOTIVO_PERDITA_CITTADIN)
  ENABLE VALIDATE,
  CONSTRAINT R_SOGGETTI_AIRE_SOGGETTO_FK 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT TABLE_62_PRATICA_AIRE_FK 
  FOREIGN KEY (ID_PRATICA_AIRE) 
  REFERENCES ANAG_USR.PRATICA_AIRE (ID_PRATICA_AIRE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_SOGGETTI_PATENTI
(
  NUMERO_PATENTE       VARCHAR2(40 CHAR)        NOT NULL,
  ID_SOGGETTO          NUMBER                   NOT NULL,
  CATEGORIA            VARCHAR2(20 BYTE),
  DATA_RILASCIO        TIMESTAMP(6),
  DATA_SCADENZA        TIMESTAMP(6),
  ID_CAMBIO_RESIDENZA  NUMBER
)
TABLESPACE SYSTEM
RESULT_CACHE (MODE DEFAULT)
PCTUSED    40
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.R_SOGETTI_PATENTI_PK ON ANAG_USR.R_SOGGETTI_PATENTI
(NUMERO_PATENTE, ID_SOGGETTO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_SOGGETTI_PATENTI ADD (
  CONSTRAINT R_SOGGETTI_PATENTI_PK
  PRIMARY KEY
  (NUMERO_PATENTE, ID_SOGGETTO)
  USING INDEX ANAG_USR.R_SOGETTI_PATENTI_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_SOGGETTI_PATENTI ADD (
  CONSTRAINT FKMY09HKERL9OLEU8BUHIIACUMR 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT PATENTE_FK 
  FOREIGN KEY (NUMERO_PATENTE) 
  REFERENCES ANAG_USR.PATENTE (NUMERO_PATENTE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZA
(
  ID_SOGGETTO                    NUMBER         NOT NULL,
  ID_CAMBIO_RESIDENZA_DOMICILIO  NUMBER,
  FLG_DICHIARANTE                CHAR(1 BYTE),
  ID_FAMIGLIA_PROVENIENZA        NUMBER,
  CRITERIO_VALIDAZIONE_CF_ANPR   NUMBER,
  SOG_MODIFICATO                 CHAR(1 BYTE)   DEFAULT 'N',
  ID_CODICE_LEGAME               NUMBER(2),
  ID_IRREPERIBILITA_CHIUSA       NUMBER,
  ID_PROVENIENZA_AIRE            NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZA IS 'Tabella di relazione che contiene l''indicazione dei soggetti associati ad una pratica di cambio di residenza/domicilio.';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZA.ID_SOGGETTO IS 'Id del soggetto che ha richiesto il cambio di residenza/domicilio';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZA.ID_CAMBIO_RESIDENZA_DOMICILIO IS 'Identificativo della pratica di cambio di residenza/domicilio';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZA.FLG_DICHIARANTE IS 'Campo che indica se il soggetto è il dichirante. "D"  se dichiarante , "N" altrimenti.';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZA.ID_FAMIGLIA_PROVENIENZA IS 'identificativo di una famigliaConvivenza di provenienza dei soggetti legati alla pratica di crica. non necessariamente quella del soggetto';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZA.CRITERIO_VALIDAZIONE_CF_ANPR IS 'Campo che identifica il criterio di validazione del cf per anpr.';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZA.SOG_MODIFICATO IS 'Campo che indifica se è stata effettuata una modifica e quindi necessario allineamento con ANPR, FLAG S e N ';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZA.ID_CODICE_LEGAME IS 'Identificativo del legame del soggetto nella famiglia al momento del cambio';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZA.ID_IRREPERIBILITA_CHIUSA IS 'Identifica la pratica di irreperibilità in corso chiusa dal CA';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZA.ID_PROVENIENZA_AIRE IS 'Identificativo località AIRE se la pratica è un Rientro da AIRE (ID_TIPO_RICHIESTA_CAMBIO = 5)';



CREATE UNIQUE INDEX ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZ_PK ON ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZA
(ID_SOGGETTO, ID_CAMBIO_RESIDENZA_DOMICILIO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.R_SOGGETTO_CAMBIO_RESIDENZA FOR ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZA;


ALTER TABLE ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZA ADD (
  CONSTRAINT R_SOGGETTO_CAMBIO_RESIDENZ_PK
  PRIMARY KEY
  (ID_SOGGETTO, ID_CAMBIO_RESIDENZA_DOMICILIO)
  USING INDEX ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZ_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZA ADD (
  CONSTRAINT FK7RCN7MUCGN7SIEBPNXF55Y1YN 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT R_CAMBIO_RESID_DOMICILIO_FK 
  FOREIGN KEY (ID_CAMBIO_RESIDENZA_DOMICILIO) 
  REFERENCES ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO (ID_CAMBIO_RESIDENZA_DOMICILIO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_UTENTE_COMUNICAZIONE
(
  ID_COMUNICAZIONE  NUMBER                      NOT NULL,
  ID_DESTINATARIO   NUMBER                      NOT NULL,
  FLG_DA_LEGGERE    CHAR(1 CHAR),
  DATA_LETTURA      DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.R_UTENTE_COMUNICAZIONE IS 'Tabella di relazione che associa una comunicazione a uno o più utenti destinatari.';

COMMENT ON COLUMN ANAG_USR.R_UTENTE_COMUNICAZIONE.ID_COMUNICAZIONE IS 'Identifica la comunicazione inviata ad uno o più utenti.';

COMMENT ON COLUMN ANAG_USR.R_UTENTE_COMUNICAZIONE.ID_DESTINATARIO IS 'Identifica l''utente destinatario della comunicazione.';

COMMENT ON COLUMN ANAG_USR.R_UTENTE_COMUNICAZIONE.FLG_DA_LEGGERE IS 'S -> Se l''utente deve ancora leggere la comunicazione.
N -> Se l''utente ha letto la comunicazione.';

COMMENT ON COLUMN ANAG_USR.R_UTENTE_COMUNICAZIONE.DATA_LETTURA IS 'Data in cui l''utente destinatario ha letto la comunicazione.';



CREATE UNIQUE INDEX ANAG_USR.R_UTENTE_COMUNICAZIONE_PK ON ANAG_USR.R_UTENTE_COMUNICAZIONE
(ID_COMUNICAZIONE, ID_DESTINATARIO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.UK_MSF2D9IRJ2YOUDFTGCXQT8LPP ON ANAG_USR.R_UTENTE_COMUNICAZIONE
(ID_DESTINATARIO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_UTENTE_COMUNICAZIONE ADD (
  CONSTRAINT R_UTENTE_COMUNICAZIONE_PK
  PRIMARY KEY
  (ID_COMUNICAZIONE, ID_DESTINATARIO)
  USING INDEX ANAG_USR.R_UTENTE_COMUNICAZIONE_PK
  ENABLE VALIDATE,
  CONSTRAINT UK_MSF2D9IRJ2YOUDFTGCXQT8LPP
  UNIQUE (ID_DESTINATARIO)
  USING INDEX ANAG_USR.UK_MSF2D9IRJ2YOUDFTGCXQT8LPP
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_UTENTE_COMUNICAZIONE ADD (
  CONSTRAINT R_COMUNICAZIONI_FK 
  FOREIGN KEY (ID_COMUNICAZIONE) 
  REFERENCES ANAG_USR.COMUNICAZIONI (ID)
  ENABLE VALIDATE,
  CONSTRAINT R_UTENTE_COMUNICAZIONE_FK 
  FOREIGN KEY (ID_DESTINATARIO) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_UTENTI_RUOLI
(
  ID                NUMBER                      NOT NULL,
  ID_UTENTE         NUMBER                      NOT NULL,
  ID_RUOLO          NUMBER                      NOT NULL,
  ID_AREA_TEMATICA  NUMBER                      NOT NULL,
  ID_FUNZIONALITA   NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.R_UTENTI_RUOLI IS 'Tabella di relazione che consente di attribuire ad un utente uno o più ruoli a sistema associando per ciascun ruolo Area Tematica su cui può operare e Funzionalità abilitate';

COMMENT ON COLUMN ANAG_USR.R_UTENTI_RUOLI.ID IS 'Id';

COMMENT ON COLUMN ANAG_USR.R_UTENTI_RUOLI.ID_UTENTE IS 'Identificativo dell''utente';

COMMENT ON COLUMN ANAG_USR.R_UTENTI_RUOLI.ID_RUOLO IS 'Identificativo del ruolo associato all''utente.';

COMMENT ON COLUMN ANAG_USR.R_UTENTI_RUOLI.ID_AREA_TEMATICA IS 'Identificativo dell''area tematica su cui l''utente con un determinato ruolo può operare.';

COMMENT ON COLUMN ANAG_USR.R_UTENTI_RUOLI.ID_FUNZIONALITA IS 'Identificativo della funzionalità a cui l''utente è abilitato';



CREATE UNIQUE INDEX ANAG_USR.R_UTENTI_RUOLI_PK ON ANAG_USR.R_UTENTI_RUOLI
(ID)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.R_UTENTI_RUOLI FOR ANAG_USR.R_UTENTI_RUOLI;


ALTER TABLE ANAG_USR.R_UTENTI_RUOLI ADD (
  CONSTRAINT R_UTENTI_RUOLI_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.R_UTENTI_RUOLI_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_UTENTI_RUOLI ADD (
  CONSTRAINT R_UTENTI_AREE_TEMATICHE_FK 
  FOREIGN KEY (ID_AREA_TEMATICA) 
  REFERENCES ANAG_USR.CONF_AREE_TEMATICHE (ID_AREE_TEMATICHE)
  ENABLE VALIDATE,
  CONSTRAINT R_UTENTI_FUNZIONALITA_FK 
  FOREIGN KEY (ID_FUNZIONALITA) 
  REFERENCES ANAG_USR.CONF_FUNZIONALITA (ID)
  ENABLE VALIDATE,
  CONSTRAINT R_UTENTI_RUOLI_CONF_RUOLI_FK 
  FOREIGN KEY (ID_RUOLO) 
  REFERENCES ANAG_USR.CONF_RUOLI (ID)
  ENABLE VALIDATE,
  CONSTRAINT R_UTENTI_RUOLI_UTENTI_FK 
  FOREIGN KEY (ID_UTENTE) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.SCIOGLIMENTOUNIONE
(
  ID_SCIOGLIMENTO       NUMBER                  NOT NULL,
  MOTIVO_SCIOGLIMENTO   VARCHAR2(200 CHAR),
  DATA_EVENTO           DATE,
  FLG_SENZA_GIORNO      CHAR(1 CHAR),
  FLG_SENZA_MESE        CHAR(1 CHAR),
  LUOGO_ECCEZIONALE     VARCHAR2(50 CHAR),
  ID_SENTENZA           NUMBER,
  ID_SOGGETTO           NUMBER,
  ID_ATTO               NUMBER,
  ID_COMUNE             NUMBER,
  ID_LOCALITA           NUMBER,
  COD_COMUNE_AGGIOR     VARCHAR2(20 BYTE),
  ID_TIPO_SCIOGLIMENTO  NUMBER,
  ID_UNIONE             NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.SCIOGLIMENTOUNIONE IS 'Tabella contenente le informazioni sull''atto di scioglimento di una unione civile.';

COMMENT ON COLUMN ANAG_USR.SCIOGLIMENTOUNIONE.ID_SCIOGLIMENTO IS 'Identificativo dello scioglimento dell''unione civile';

COMMENT ON COLUMN ANAG_USR.SCIOGLIMENTOUNIONE.MOTIVO_SCIOGLIMENTO IS 'Motivazione dello scioglimento - TABELLA 43 ANPR';

COMMENT ON COLUMN ANAG_USR.SCIOGLIMENTOUNIONE.DATA_EVENTO IS 'Data dello scioglimento';

COMMENT ON COLUMN ANAG_USR.SCIOGLIMENTOUNIONE.FLG_SENZA_GIORNO IS 'S -> non è presente il giorno dello scioglimento dell''unione civile
N -> è presente il giorno dello scioglimento dell''unione civile';

COMMENT ON COLUMN ANAG_USR.SCIOGLIMENTOUNIONE.FLG_SENZA_MESE IS 'S -> non è presente il mese dello scioglimento dell''unione civile
N -> è presente il mese dello scioglimento dell''unione civile';

COMMENT ON COLUMN ANAG_USR.SCIOGLIMENTOUNIONE.LUOGO_ECCEZIONALE IS 'Luogo eccezionale dello scioglimento';

COMMENT ON COLUMN ANAG_USR.SCIOGLIMENTOUNIONE.ID_SENTENZA IS 'Identificativo della senteza di unione civile';

COMMENT ON COLUMN ANAG_USR.SCIOGLIMENTOUNIONE.ID_SOGGETTO IS 'Id del soggetto per cui viene apposto lo scioglimento';

COMMENT ON COLUMN ANAG_USR.SCIOGLIMENTOUNIONE.ID_ATTO IS 'FK all''atto di scioglimento di unione civile';

COMMENT ON COLUMN ANAG_USR.SCIOGLIMENTOUNIONE.ID_COMUNE IS 'identificativo del comue in cui si è svolto l''evento';

COMMENT ON COLUMN ANAG_USR.SCIOGLIMENTOUNIONE.ID_LOCALITA IS 'identificativo della località in cui si è svolto l''evento';

COMMENT ON COLUMN ANAG_USR.SCIOGLIMENTOUNIONE.COD_COMUNE_AGGIOR IS 'identificativo aggior del comune salvato in LUOGO_ECCEZIONALE';

COMMENT ON COLUMN ANAG_USR.SCIOGLIMENTOUNIONE.ID_TIPO_SCIOGLIMENTO IS 'identificativo del tipo di scoglimento effettuato';

COMMENT ON COLUMN ANAG_USR.SCIOGLIMENTOUNIONE.ID_UNIONE IS 'identificativo dell''unione_civilie a cui è legato lo scioglimento';



CREATE UNIQUE INDEX ANAG_USR.SCIOGLIMENTOUNIONE_PK ON ANAG_USR.SCIOGLIMENTOUNIONE
(ID_SCIOGLIMENTO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.SCIOGLIMENTOUNIONE ADD (
  CONSTRAINT SCIOGLIMENTOUNIONE_PK
  PRIMARY KEY
  (ID_SCIOGLIMENTO)
  USING INDEX ANAG_USR.SCIOGLIMENTOUNIONE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.SCIOGLIMENTOUNIONE ADD (
  CONSTRAINT SCIOGLIMENTOUNIONE_ATTO_FK 
  FOREIGN KEY (ID_ATTO) 
  REFERENCES ANAG_USR.ATTO (ID_ATTO)
  DISABLE NOVALIDATE,
  CONSTRAINT SCIOGLIMENTOUNIONE_FK1 
  FOREIGN KEY (ID_COMUNE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT SCIOGLIMENTOUNIONE_FK2 
  FOREIGN KEY (ID_LOCALITA) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE,
  CONSTRAINT SCIOGLIMENTOUNIONE_FK3 
  FOREIGN KEY (ID_TIPO_SCIOGLIMENTO) 
  REFERENCES ANAG_USR.CONF_TIPO_SCIOGLIMENTO_UNIONE (ID_TIPO_SCIOGLIMENTO_UNIONE)
  ENABLE VALIDATE,
  CONSTRAINT SCIOGLIMENTOUNIONE_SENTENZA_FK 
  FOREIGN KEY (ID_SENTENZA) 
  REFERENCES ANAG_USR.SENTENZA (ID_SENTENZA)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_SCI_UNI_FK 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.SENTENZA
(
  ID_SENTENZA                 NUMBER            NOT NULL,
  DATA_SENTENZA               DATE,
  TIPO_TRIBUNALE              NUMBER,
  AUTORITA                    VARCHAR2(50 CHAR),
  DATA_VALIDITA               DATE,
  COD_TIPO_PROTOCOLLO         CHAR(10 CHAR),
  ANNO_PROTOCOLLO             NUMBER,
  NUMERO_PROTOCOLLO           NUMBER,
  ID_TIPO_SENTENZA            NUMBER,
  ID_COMUNE                   NUMBER,
  RICHIEDENTE                 NUMBER,
  VALIDANTE                   NUMBER,
  DATA_CONVENZIONE            DATE,
  DATA_ANNOTAZIONE            DATE,
  NOME_VALIDANTE              VARCHAR2(50 BYTE),
  COGNOME_VALIDANTE           VARCHAR2(50 BYTE),
  PARTE_REGISTRO              VARCHAR2(50 BYTE),
  SERIE_REGISTRO              VARCHAR2(50 BYTE),
  ANNO_REGISTRO               NUMBER,
  ID_ATTO                     NUMBER,
  ID_TIPO_CONVENZIONE         NUMBER,
  NOTE_SENTENZA               VARCHAR2(200 BYTE),
  NUMERO_REGISTRO             VARCHAR2(10 BYTE),
  NUMERO                      VARCHAR2(10 BYTE),
  ID_LOCALITA                 NUMBER,
  ID_TITOLO_NOTAIO            NUMBER,
  DISTRETTO                   VARCHAR2(200 BYTE),
  ID_DESCRIZIONE_CONVENZIONE  NUMBER,
  ID_TIPO_FONDO               NUMBER,
  LEGGE                       VARCHAR2(200 BYTE),
  TESTO_AGGIUNTIVO            VARCHAR2(2000 BYTE),
  ID_ARTICOLO_NOTAIO          NUMBER,
  AMBASCIATA_CONSOLATO        VARCHAR2(200 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.SENTENZA IS 'Tabella che contiene le informazioni su una sentenza emessa da un tribunale.';

COMMENT ON COLUMN ANAG_USR.SENTENZA.ID_SENTENZA IS 'Identificativo della sentenza';

COMMENT ON COLUMN ANAG_USR.SENTENZA.DATA_SENTENZA IS 'Data di emissione della sentenza';

COMMENT ON COLUMN ANAG_USR.SENTENZA.TIPO_TRIBUNALE IS 'Tipologia del tribunale che ha emesso la sentenza FK CONF_TIPO_TRIBUNALE';

COMMENT ON COLUMN ANAG_USR.SENTENZA.AUTORITA IS 'Autorità di emissione della sentenza - Indica il tribunale / professionista che ha emesso la sentenza / accordo scioglimento';

COMMENT ON COLUMN ANAG_USR.SENTENZA.DATA_VALIDITA IS 'Data validità della sentenza';

COMMENT ON COLUMN ANAG_USR.SENTENZA.COD_TIPO_PROTOCOLLO IS 'Codice del protocollo della sentenza';

COMMENT ON COLUMN ANAG_USR.SENTENZA.ANNO_PROTOCOLLO IS 'Anno del protocollo della sentenza';

COMMENT ON COLUMN ANAG_USR.SENTENZA.NUMERO_PROTOCOLLO IS 'Numero protocollo della sentenza';

COMMENT ON COLUMN ANAG_USR.SENTENZA.ID_TIPO_SENTENZA IS 'Indica il tipo di sentenza';

COMMENT ON COLUMN ANAG_USR.SENTENZA.ID_COMUNE IS 'indica il comune della sentenza';

COMMENT ON COLUMN ANAG_USR.SENTENZA.RICHIEDENTE IS '1-> SPOSO , 2->SPOSA , 3 ->SPOSI';

COMMENT ON COLUMN ANAG_USR.SENTENZA.VALIDANTE IS '1->NOTAIO, 2-> CONSOLE';

COMMENT ON COLUMN ANAG_USR.SENTENZA.DATA_CONVENZIONE IS 'data di convenzione della sentenza';

COMMENT ON COLUMN ANAG_USR.SENTENZA.DATA_ANNOTAZIONE IS 'data di annotazione della sentenza';

COMMENT ON COLUMN ANAG_USR.SENTENZA.NOME_VALIDANTE IS 'nome del validante';

COMMENT ON COLUMN ANAG_USR.SENTENZA.COGNOME_VALIDANTE IS 'cognome del validante ';

COMMENT ON COLUMN ANAG_USR.SENTENZA.PARTE_REGISTRO IS 'parte registro della sentenza';

COMMENT ON COLUMN ANAG_USR.SENTENZA.SERIE_REGISTRO IS 'serie registro della sentenza';

COMMENT ON COLUMN ANAG_USR.SENTENZA.ANNO_REGISTRO IS 'anno registro della sentenza';

COMMENT ON COLUMN ANAG_USR.SENTENZA.ID_ATTO IS 'indica l''atto di riferimento per la sentenza';

COMMENT ON COLUMN ANAG_USR.SENTENZA.ID_TIPO_CONVENZIONE IS 'Identificativo del tipo di convenzione patrimoniale';

COMMENT ON COLUMN ANAG_USR.SENTENZA.ID_LOCALITA IS 'Identificativo della località';



CREATE UNIQUE INDEX ANAG_USR.SENTENZA_PK ON ANAG_USR.SENTENZA
(ID_SENTENZA)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.SENTENZA ADD (
  CONSTRAINT SENTENZA_PK
  PRIMARY KEY
  (ID_SENTENZA)
  USING INDEX ANAG_USR.SENTENZA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.SENTENZA ADD (
  CONSTRAINT FKPM9TET7XVHOMY8E0MSU931XD1 
  FOREIGN KEY (ID_ATTO) 
  REFERENCES ANAG_USR.ATTO (ID_ATTO)
  ENABLE VALIDATE,
  CONSTRAINT ID_COMUNE 
  FOREIGN KEY (ID_COMUNE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT ID_LOCALITA 
  FOREIGN KEY (ID_LOCALITA) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE,
  CONSTRAINT ID_TIPO_CONVENZIONE 
  FOREIGN KEY (ID_TIPO_CONVENZIONE) 
  REFERENCES ANAG_USR.CONF_TIPO_CONVENZIONI (ID_TIPO_CONVENZIONI)
  ENABLE VALIDATE,
  CONSTRAINT ID_TIPO_SENTENZA 
  FOREIGN KEY (ID_TIPO_SENTENZA) 
  REFERENCES ANAG_USR.CONF_TIPO_SENTENZA (ID_TIPO_SENTENZA)
  ENABLE VALIDATE,
  CONSTRAINT SENTENZA_FK1 
  FOREIGN KEY (TIPO_TRIBUNALE) 
  REFERENCES ANAG_USR.CONF_TIPO_TRIBUNALE (ID_TIPO_TRIBUNALE)
  ENABLE VALIDATE,
  CONSTRAINT SENTENZA_FK2 
  FOREIGN KEY (ID_TITOLO_NOTAIO) 
  REFERENCES ANAG_USR.CONF_TITOLO_NOTAIO (ID_TITOLO_NOTAIO)
  ENABLE VALIDATE,
  CONSTRAINT SENTENZA_FK3 
  FOREIGN KEY (ID_DESCRIZIONE_CONVENZIONE) 
  REFERENCES ANAG_USR.CONF_DESCRIZIONE_CONVENZIONE (ID_DESCRIZIONE)
  ENABLE VALIDATE,
  CONSTRAINT SENTENZA_FK4 
  FOREIGN KEY (ID_TIPO_FONDO) 
  REFERENCES ANAG_USR.CONF_TIPO_FONDO_PATRIMONIALE (ID_TIPO_FONDO)
  ENABLE VALIDATE,
  CONSTRAINT SENTENZA_FK5 
  FOREIGN KEY (ID_ARTICOLO_NOTAIO) 
  REFERENCES ANAG_USR.CONF_ARTICOLO_NOTAIO (ID_ARTICOLO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.SENZA_FISSA_DIMORA
(
  ID_SENZA_FISSA_DIMORA   NUMBER CONSTRAINT NNC_SENZA_FISSA_DIMORA_ID NOT NULL,
  ANNO_NULLA_OSTA         NUMBER(4),
  NUMERO_NULLA_OSTA       VARCHAR2(4000 BYTE),
  DATA_EMISSIONE          DATE,
  CODICE_TIPO_PROTOCOLLO  VARCHAR2(10 BYTE),
  NUMERO_PROTOCOLLO       INTEGER,
  ANNO_PROTOCOLLO         INTEGER,
  ID_RESIDENZA            NUMBER,
  ID_ASSOCIAZIONE         NUMBER(4)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.SENZA_FISSA_DIMORA IS 'Tabella contenente gli estremi di un procedimento che identifica un soggetto come un Senza Fissa Dimora.';

COMMENT ON COLUMN ANAG_USR.SENZA_FISSA_DIMORA.ID_SENZA_FISSA_DIMORA IS 'Codice identificativo dello stato di senza fissa dimora associato ad un soggetto.';

COMMENT ON COLUMN ANAG_USR.SENZA_FISSA_DIMORA.ANNO_NULLA_OSTA IS 'Anno di emissione del nulla osta.';

COMMENT ON COLUMN ANAG_USR.SENZA_FISSA_DIMORA.NUMERO_NULLA_OSTA IS 'Numero associato al nulla osta.';

COMMENT ON COLUMN ANAG_USR.SENZA_FISSA_DIMORA.DATA_EMISSIONE IS 'Data in cui è stato emesso il nulla osta';

COMMENT ON COLUMN ANAG_USR.SENZA_FISSA_DIMORA.CODICE_TIPO_PROTOCOLLO IS 'Codice che identifica univocamente l''ente protocollante associato all''iscrizione del senza fissa dimora';

COMMENT ON COLUMN ANAG_USR.SENZA_FISSA_DIMORA.NUMERO_PROTOCOLLO IS 'Numero che identifica il protocollo associato alla pratica del senza fissa dimora';

COMMENT ON COLUMN ANAG_USR.SENZA_FISSA_DIMORA.ANNO_PROTOCOLLO IS 'Anno di riferimento del protocollo assoiato al senza fissa dimora.';

COMMENT ON COLUMN ANAG_USR.SENZA_FISSA_DIMORA.ID_RESIDENZA IS 'Residenza fisica dichiarata dal soggetto senza fissa dimora';

COMMENT ON COLUMN ANAG_USR.SENZA_FISSA_DIMORA.ID_ASSOCIAZIONE IS 'identificativo dell''associazione in cui è iscritto il soggeto senza fissa dimora';



CREATE UNIQUE INDEX ANAG_USR.SENZA_FISSA_DIMORA_PK ON ANAG_USR.SENZA_FISSA_DIMORA
(ID_SENZA_FISSA_DIMORA)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.SENZA_FISSA_DIMORA ADD (
  CONSTRAINT SENZA_FISSA_DIMORA_PK
  PRIMARY KEY
  (ID_SENZA_FISSA_DIMORA)
  USING INDEX ANAG_USR.SENZA_FISSA_DIMORA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.SENZA_FISSA_DIMORA ADD (
  CONSTRAINT ASSOCIAZ_SENZA_FISSA_DIMORA_FK 
  FOREIGN KEY (ID_ASSOCIAZIONE) 
  REFERENCES ANAG_USR.ASSOCIAZ_SENZA_FISSA_DIMORA (ID_ASSOCIAZIONE)
  ENABLE VALIDATE,
  CONSTRAINT CONF_TIPO_PROTOCOLLO_FKV4 
  FOREIGN KEY (CODICE_TIPO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE,
  CONSTRAINT RESIDENZA_FK 
  FOREIGN KEY (ID_RESIDENZA) 
  REFERENCES ANAG_USR.RESIDENZA (ID_RESIDENZA)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.SOGGIORNO
(
  ID_SOGGIORNO                    NUMBER        NOT NULL,
  NUMERO_PERMESSO_SOGG            VARCHAR2(20 BYTE),
  NOTE                            VARCHAR2(250 BYTE),
  DATA_RILASCIO                   DATE,
  QUESTURE_RILASCIO               NUMBER,
  NUMERO_DOCUMENTO                VARCHAR2(30 BYTE),
  ID_COMUNE_RILASCIO              NUMBER,
  ID_TIPO_SOGGIORNO               NUMBER(2),
  FLG_TIPO_SOGGIORNO              CHAR(1 CHAR),
  FLG_RUOLO_SOGGIORNO             VARCHAR2(1 BYTE),
  DATA_SCADENZA                   DATE,
  DATA_RINNOVO                    DATE,
  DATA_RICHIESTA_RINNOVO          DATE,
  TIPO_ATTESTATO                  CHAR(1 BYTE),
  FLG_CANCELLATO                  CHAR(1 BYTE),
  DATA_CANCELLAZIONE              DATE,
  BLOB                            BLOB,
  ID_MOTIVO_ANNULLAMENTO          NUMBER,
  FILENAME_DOC                    VARCHAR2(250 BYTE),
  NUMERO_ATTESTATO_SOGG           VARCHAR2(20 BYTE),
  ID_DOCUMENTO                    VARCHAR2(1 BYTE),
  ALTRE_MOTIVAZIONI_ANNULLAMENTO  VARCHAR2(200 BYTE),
  DATA_ULTIMO_AGGIORNAMENTO       DATE,
  ID_UTENTE                       NUMBER,
  ID_STRUTTURA                    NUMBER
)
LOB (BLOB) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.SOGGIORNO IS 'Tabella che contiene le informazioni sul rilascio di un Permesso di Soggiorno per i cittadini Extra UE o di un Attestato di Soggiorno per i cittadini UE.';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.ID_SOGGIORNO IS 'Identificativo del permesso o attestato di soggiorno.';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.NUMERO_PERMESSO_SOGG IS 'Numero del permesso di soggiorno.';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.DATA_RILASCIO IS 'Data in cui è stato rilasciato il permesso di soggiorno.';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.QUESTURE_RILASCIO IS 'Questura che ha rilasciato il permesso di soggiorno';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.NUMERO_DOCUMENTO IS 'Numero del documento
 del soggetto possessore del permesso di soggiorno.';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.ID_COMUNE_RILASCIO IS 'Identificativo del comune di rilascio del permesso di soggiorno.';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.ID_TIPO_SOGGIORNO IS 'Codice identificativo della tipologia del permesso di soggiorno.';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.FLG_TIPO_SOGGIORNO IS 'P -> Permesso di soggiorno
A -> Attestato di soggiorno';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.FLG_RUOLO_SOGGIORNO IS 'flag che identifica il ruolo del soggetto sul permesso o attestato di soggiorno T->TITOLARE; F->FAMILIARE; A->ALTRO COMUNE';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.DATA_SCADENZA IS 'Data di scadenza';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.DATA_RINNOVO IS 'Date di rinnovo';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.DATA_RICHIESTA_RINNOVO IS 'Data di richiesta del rinnovo';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.TIPO_ATTESTATO IS 'P--> PERMANENTE - T --> TEMPORANEO';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.FLG_CANCELLATO IS 'S --> SI - N --> NO';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.DATA_CANCELLAZIONE IS 'Data di cancellazione del permesso o attestato di soggiorno';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.BLOB IS 'Documento del permesso/attestato di soggiorno';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.ID_MOTIVO_ANNULLAMENTO IS 'Identificativo del motivo di annullamento dell''attestato';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.FILENAME_DOC IS 'Nome del file blob salvato';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.NUMERO_ATTESTATO_SOGG IS 'Numero dell''attestato di soggiorno';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.ID_DOCUMENTO IS 'Identificativo del documento posseduto 0->carta_identita, 1->patente, 2->passaporto
';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.ALTRE_MOTIVAZIONI_ANNULLAMENTO IS 'Motivazione dell''annullamento di un attestato di soggiorno nel caso venga selezionata la voce ''altro'' tra le motivazioni disponibili';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.DATA_ULTIMO_AGGIORNAMENTO IS 'Data ultimo aggiornamento';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.ID_UTENTE IS 'Identificativo dell''utente che ha effettuato l''ultima operazione';

COMMENT ON COLUMN ANAG_USR.SOGGIORNO.ID_STRUTTURA IS 'Identificativo del municipio in cui viene effettuata l''operazione';



CREATE UNIQUE INDEX ANAG_USR.PERMESSOSOGGIORNO_PK ON ANAG_USR.SOGGIORNO
(ID_SOGGIORNO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.PERMESSOSOGGIORNO__UN ON ANAG_USR.SOGGIORNO
(NUMERO_PERMESSO_SOGG)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.SOGGIORNO FOR ANAG_USR.SOGGIORNO;


ALTER TABLE ANAG_USR.SOGGIORNO ADD (
  CONSTRAINT PERMESSOSOGGIORNO_PK
  PRIMARY KEY
  (ID_SOGGIORNO)
  USING INDEX ANAG_USR.PERMESSOSOGGIORNO_PK
  ENABLE VALIDATE,
  CONSTRAINT PERMESSOSOGGIORNO__UN
  UNIQUE (NUMERO_PERMESSO_SOGG)
  USING INDEX ANAG_USR.PERMESSOSOGGIORNO__UN
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.SOGGIORNO ADD (
  CONSTRAINT CONF_MOTIV_ANNUL_ATT_FK 
  FOREIGN KEY (ID_MOTIVO_ANNULLAMENTO) 
  REFERENCES ANAG_USR.CONF_MOTIVO_ANNULLA_ATT_SOGG (ID)
  ENABLE VALIDATE,
  CONSTRAINT CONF_QUESTURE_FK2 
  FOREIGN KEY (QUESTURE_RILASCIO) 
  REFERENCES ANAG_USR.CONF_QUESTURE (ID_QUESTURA)
  ENABLE VALIDATE,
  CONSTRAINT CONF_TIPO_SOGGIORNO_FK 
  FOREIGN KEY (ID_TIPO_SOGGIORNO) 
  REFERENCES ANAG_USR.CONF_TIPO_SOGGIORNO (ID_TIPO_SOGGIORNO)
  ENABLE VALIDATE,
  CONSTRAINT PERMESSOSOGGIORNO_COMUNE_FK 
  FOREIGN KEY (ID_COMUNE_RILASCIO) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT STRUTTURA_FK 
  FOREIGN KEY (ID_STRUTTURA) 
  REFERENCES ANAG_USR.CONF_STRUTTURE_INTERNE_RC (ID)
  ENABLE VALIDATE,
  CONSTRAINT UTENTE_FK 
  FOREIGN KEY (ID_UTENTE) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.TOPONIMO
(
  ID_TOPONIMO              NUMBER               NOT NULL,
  COD_SPECIE               NUMBER(4),
  SPECIE                   VARCHAR2(30 BYTE),
  SPECIE_FONTE             NUMBER(1),
  COD_TOPONIMO             VARCHAR2(6 BYTE),
  DENOMINAZIONE_TOPONIMO   VARCHAR2(100 BYTE),
  TOPONIMO_FONTE           NUMBER(1),
  ID_TIPO_SPECIE_TOPONIMO  NUMBER,
  DENOMINAZIONE_BREVE      VARCHAR2(40 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.TOPONIMO IS 'Tabella contenente l''elenco dei toponimi di Roma Capitale.';

COMMENT ON COLUMN ANAG_USR.TOPONIMO.ID_TOPONIMO IS 'Campo che indica il codice identificativo del toponimo.';

COMMENT ON COLUMN ANAG_USR.TOPONIMO.COD_SPECIE IS 'Campo che indica il codice per la DUG (denominazione urbana generica) dell''indirizzo.';

COMMENT ON COLUMN ANAG_USR.TOPONIMO.SPECIE IS 'campo che indica la specie del toponimo.';

COMMENT ON COLUMN ANAG_USR.TOPONIMO.SPECIE_FONTE IS 'Campo che indica la fonte della specie.
Valorizzato:
1 se COD_SPECIE è ricavato dalla tabella ANPR
2 se COD_SPECIE è ricavato dalla tabella del comune.';

COMMENT ON COLUMN ANAG_USR.TOPONIMO.COD_TOPONIMO IS 'Campo che indica il codice assegnato dal comune al toponimo.';

COMMENT ON COLUMN ANAG_USR.TOPONIMO.DENOMINAZIONE_TOPONIMO IS 'Campo che indica la denominazione del toponimo.';

COMMENT ON COLUMN ANAG_USR.TOPONIMO.TOPONIMO_FONTE IS 'Campo che indica la fonte del toponimo. 
Valorizzato con:
- 1 se COD_TOPONIMO è ricavato dalla tabella ISTAT
-  2 se COD_TOPONIMO è ricavato dalla tabella del comune.';

COMMENT ON COLUMN ANAG_USR.TOPONIMO.ID_TIPO_SPECIE_TOPONIMO IS 'Identificativo della specie';

COMMENT ON COLUMN ANAG_USR.TOPONIMO.DENOMINAZIONE_BREVE IS 'Campo che identifica la denominazione breve del toponimo';



CREATE UNIQUE INDEX ANAG_USR.TOPONIMO_PK ON ANAG_USR.TOPONIMO
(ID_TOPONIMO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.TOPONIMOSIN FOR ANAG_USR.TOPONIMO;


ALTER TABLE ANAG_USR.TOPONIMO ADD (
  CONSTRAINT TOPONIMO_PK
  PRIMARY KEY
  (ID_TOPONIMO)
  USING INDEX ANAG_USR.TOPONIMO_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.TOPONIMO ADD (
  CONSTRAINT ID_SPECIE 
  FOREIGN KEY (ID_TIPO_SPECIE_TOPONIMO) 
  REFERENCES ANAG_USR.CONF_TIPO_SPECIE_TOPONIMO (ID_TIPO_SPECIE_TOPONIMO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.UNIONECIVILE
(
  ID_UNIONE               NUMBER                NOT NULL,
  DATA_EVENTO             DATE,
  FLG_SENZA_GIORNO        CHAR(1 CHAR),
  FLG_SENZA_MESE          CHAR(1 CHAR),
  ORDINE_UNIONE           NUMBER,
  LUOGO_ECCEZIONALE       VARCHAR2(120 CHAR),
  ID_LOCALITA             NUMBER,
  ID_SOGGETTO_PRIMO       NUMBER,
  ID_SOGGETTO_SECONDO     NUMBER,
  ID_COMUNE               NUMBER,
  ID_ATTO                 NUMBER,
  ID_SCELTA_PATRIMONIALE  NUMBER,
  COD_COMUNE_AGGIOR       VARCHAR2(20 BYTE),
  ID_OPERAZIONE_ANPR      NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.UNIONECIVILE IS 'Tabella contenente le informazioni di un atto di unione civile.';

COMMENT ON COLUMN ANAG_USR.UNIONECIVILE.ID_UNIONE IS 'Identificativo dell''unione civile';

COMMENT ON COLUMN ANAG_USR.UNIONECIVILE.DATA_EVENTO IS 'Data dell''unione civile';

COMMENT ON COLUMN ANAG_USR.UNIONECIVILE.FLG_SENZA_GIORNO IS 'S -> non è presente il giorno dell''unione civile
N -> è presente il giorno dell''unione civile';

COMMENT ON COLUMN ANAG_USR.UNIONECIVILE.FLG_SENZA_MESE IS 'S -> non è presente il mese dell''unione civile
N -> è presente il mese dell''unione civile';

COMMENT ON COLUMN ANAG_USR.UNIONECIVILE.ORDINE_UNIONE IS 'Ordine dell''unione civile';

COMMENT ON COLUMN ANAG_USR.UNIONECIVILE.LUOGO_ECCEZIONALE IS 'Luogo eccezionale dell''unione civile';

COMMENT ON COLUMN ANAG_USR.UNIONECIVILE.ID_LOCALITA IS 'Identificativo località dell''unione civile';

COMMENT ON COLUMN ANAG_USR.UNIONECIVILE.ID_SOGGETTO_PRIMO IS 'Id del primo soggetto unito civilmente con il secondo soggetto';

COMMENT ON COLUMN ANAG_USR.UNIONECIVILE.ID_SOGGETTO_SECONDO IS 'Id del secondo soggetto unito civilmente con il primo soggetto';

COMMENT ON COLUMN ANAG_USR.UNIONECIVILE.ID_COMUNE IS 'Comune dell''unione civile';

COMMENT ON COLUMN ANAG_USR.UNIONECIVILE.ID_ATTO IS 'FK All''atto di unione civile';

COMMENT ON COLUMN ANAG_USR.UNIONECIVILE.ID_SCELTA_PATRIMONIALE IS 'Scelta patrimoniale effettuata dai soggetti uniti civilmente.';

COMMENT ON COLUMN ANAG_USR.UNIONECIVILE.COD_COMUNE_AGGIOR IS 'identificativo aggior del comune salvato in LUOGO_ECCEZIONALE';

COMMENT ON COLUMN ANAG_USR.UNIONECIVILE.ID_OPERAZIONE_ANPR IS 'Identificativo dell''operazione ANPR, da valorizzare solo nel momento della creazione';



CREATE INDEX ANAG_USR.IDX_UNIONECIVILE_CONIUGI ON ANAG_USR.UNIONECIVILE
(ID_SOGGETTO_PRIMO, ID_SOGGETTO_SECONDO, DATA_EVENTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE INDEX ANAG_USR.IDX_UNIONECIVILE_DATAEVENTO ON ANAG_USR.UNIONECIVILE
(DATA_EVENTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE INDEX ANAG_USR.IDX_UNIONECIVILE_IDATTO ON ANAG_USR.UNIONECIVILE
(ID_ATTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.UNIONECIVILE_PK ON ANAG_USR.UNIONECIVILE
(ID_UNIONE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.UNIONECIVILE ADD (
  CONSTRAINT UNIONECIVILE_PK
  PRIMARY KEY
  (ID_UNIONE)
  USING INDEX ANAG_USR.UNIONECIVILE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.UNIONECIVILE ADD (
  CONSTRAINT CONF_SCELTA_PATRIMONIALE_FKV2 
  FOREIGN KEY (ID_SCELTA_PATRIMONIALE) 
  REFERENCES ANAG_USR.CONF_SCELTA_PATRIMONIALE (ID)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_PRIMO_UN_FK 
  FOREIGN KEY (ID_SOGGETTO_PRIMO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_SECONDO_UN_FK 
  FOREIGN KEY (ID_SOGGETTO_SECONDO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT UNIONECIVILE_ATTO_FK 
  FOREIGN KEY (ID_ATTO) 
  REFERENCES ANAG_USR.ATTO (ID_ATTO)
  ENABLE VALIDATE,
  CONSTRAINT UNIONECIVILE_COMUNE_FK 
  FOREIGN KEY (ID_COMUNE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT UNIONECIVILE_LOCALITA_FK 
  FOREIGN KEY (ID_LOCALITA) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.UTENTI
(
  ID                     NUMBER                 NOT NULL,
  NOME_UTENTE            VARCHAR2(200 CHAR)     NOT NULL,
  NOME                   VARCHAR2(200 CHAR)     NOT NULL,
  COGNOME                VARCHAR2(200 CHAR)     NOT NULL,
  FLG_ATTIVO             CHAR(1 CHAR)           NOT NULL,
  FLG_CANCELLATO         CHAR(1 CHAR)           NOT NULL,
  DATA_CREAZIONE_UTENZA  DATE                   NOT NULL,
  DATA_CANCELLAZIONE     DATE,
  ID_ORGANIZZAZIONE      NUMBER,
  ID_STRUTTURA_CONV      NUMBER,
  CODICE_FISCALE         VARCHAR2(50 BYTE),
  NOME_UTENTE_AGGIOR     VARCHAR2(11 BYTE),
  ID_SEDE_MUNICIPIO      NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.UTENTI IS 'La tabella contiene gli utenti che potranno accedere al sistema SIPO.';

COMMENT ON COLUMN ANAG_USR.UTENTI.ID IS 'Identificativo dell''utente';

COMMENT ON COLUMN ANAG_USR.UTENTI.NOME_UTENTE IS 'Nome utente utilizzato per l''accesso al sistema. Potrà essere o <nome.cognome> o <codice fiscale> per identificare univocamente o un dipendente id Roma Capitale o un Cittadino.';

COMMENT ON COLUMN ANAG_USR.UTENTI.NOME IS 'E'' il nome dell''utente profilato a sistema.';

COMMENT ON COLUMN ANAG_USR.UTENTI.COGNOME IS 'E'' il Cognome dell''utente profilato a sistema.';

COMMENT ON COLUMN ANAG_USR.UTENTI.FLG_ATTIVO IS 'S -> Se l''utente è attivo a sistema
N -> Se l''utente è disattivato';

COMMENT ON COLUMN ANAG_USR.UTENTI.FLG_CANCELLATO IS 'S-> Se l''utente è stato cancellato dal sistema (Cancellazione Logica)
N-> Altrimenti';

COMMENT ON COLUMN ANAG_USR.UTENTI.DATA_CREAZIONE_UTENZA IS 'Rappresenta la data in cui l''utenza è stata creata';

COMMENT ON COLUMN ANAG_USR.UTENTI.DATA_CANCELLAZIONE IS 'Rappresenta la data in cui l''utenza è stata cancellata logicamente dal sistema.';

COMMENT ON COLUMN ANAG_USR.UTENTI.ID_ORGANIZZAZIONE IS 'Rappresenta l''unità organizzativa di cui l''utente fa parte se dipendente di Roma Capitale.';

COMMENT ON COLUMN ANAG_USR.UTENTI.ID_STRUTTURA_CONV IS 'Nel caso di cittadini laddove si possa accedere come struttura convenzionata con Roma Capitale, il campo rappresenta la struttura di riferimento per l''utente.';

COMMENT ON COLUMN ANAG_USR.UTENTI.CODICE_FISCALE IS 'Codice fiscale del dipendente';

COMMENT ON COLUMN ANAG_USR.UTENTI.NOME_UTENTE_AGGIOR IS 'Nome utente su AGGIOR';

COMMENT ON COLUMN ANAG_USR.UTENTI.ID_SEDE_MUNICIPIO IS 'Indica la sede del municipio di appartenenza';



CREATE UNIQUE INDEX ANAG_USR.UTENTI_PK ON ANAG_USR.UTENTI
(ID)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.UTENTI__UN ON ANAG_USR.UTENTI
(NOME_UTENTE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.UTENTI FOR ANAG_USR.UTENTI;


ALTER TABLE ANAG_USR.UTENTI ADD (
  CONSTRAINT UTENTI_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.UTENTI_PK
  ENABLE VALIDATE,
  CONSTRAINT UTENTI__UN
  UNIQUE (NOME_UTENTE)
  USING INDEX ANAG_USR.UTENTI__UN
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.UTENTI ADD (
  CONSTRAINT CONF_STRUTTURE_INTERNE_RC_FKV2 
  FOREIGN KEY (ID_ORGANIZZAZIONE) 
  REFERENCES ANAG_USR.CONF_STRUTTURE_INTERNE_RC (ID)
  ENABLE VALIDATE,
  FOREIGN KEY (ID_SEDE_MUNICIPIO) 
  REFERENCES ANAG_USR.CONF_SEDE_MUNICIPIO (ID_SEDE_MUNICIPIO)
  ENABLE VALIDATE,
  CONSTRAINT UTENTI_CONF_STRUTTURE_CONV_FK 
  FOREIGN KEY (ID_STRUTTURA_CONV) 
  REFERENCES ANAG_USR.CONF_STRUTTURE_CONV (ID)
  ENABLE VALIDATE);

GRANT REFERENCES ON ANAG_USR.UTENTI TO ELET_USR;
CREATE TABLE ANAG_USR.VEICOLI
(
  TARGA                VARCHAR2(200 CHAR)       NOT NULL,
  ID_TIPO_VEICOLO      NUMBER(2),
  ID_SOGGETTO          NUMBER                   NOT NULL,
  ID_CAMBIO_RESIDENZA  NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.VEICOLI IS 'Tabella contenente l''elenco dei veicoli di proprietà di un determinato soggetto.';

COMMENT ON COLUMN ANAG_USR.VEICOLI.TARGA IS 'Targa del veicolo';

COMMENT ON COLUMN ANAG_USR.VEICOLI.ID_TIPO_VEICOLO IS 'Tipologia veicolo';

COMMENT ON COLUMN ANAG_USR.VEICOLI.ID_SOGGETTO IS 'Id del soggetto proprietario del veicolo';

COMMENT ON COLUMN ANAG_USR.VEICOLI.ID_CAMBIO_RESIDENZA IS 'Id del cambio di residenza dove è stato inserito il veicolo';



CREATE UNIQUE INDEX ANAG_USR.VEICOLI_PK ON ANAG_USR.VEICOLI
(TARGA)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.VEICOLI ADD (
  CONSTRAINT VEICOLI_PK
  PRIMARY KEY
  (TARGA)
  USING INDEX ANAG_USR.VEICOLI_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.VEICOLI ADD (
  CONSTRAINT CONF_TIPO_VEICOLO_FK 
  FOREIGN KEY (ID_TIPO_VEICOLO) 
  REFERENCES ANAG_USR.CONF_TIPO_VEICOLO (ID_TIPO_VEICOLO)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_VEICOLO_FK 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_MOTIVO_CAMBIO_PRATICAAIRE
(
  ID_MOTIVO_CAMBIO_PRATICAAIRE  NUMBER          NOT NULL,
  DESCRIZIONE                   VARCHAR2(200 CHAR),
  ID_TIPO_PRATICA_AIRE          NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_MOTIVO_CAMBIO_PRATICAAIRE IS 'Tabella tipologica che contiene l''elenco delle motivazioni ammesse per il cambio di stato di una pratica AIRE';

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_CAMBIO_PRATICAAIRE.ID_MOTIVO_CAMBIO_PRATICAAIRE IS 'Identificativo della motivazione di cambio stato per una pratica AIRE';

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_CAMBIO_PRATICAAIRE.DESCRIZIONE IS 'Descrizione della motivazione di cambio stato pratica AIRE';

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_CAMBIO_PRATICAAIRE.ID_TIPO_PRATICA_AIRE IS 'Identificativo del tipo di pratica AIRE';



CREATE UNIQUE INDEX ANAG_USR.CONF_MOTIVAZIONI_AIRE_PK ON ANAG_USR.CONF_MOTIVO_CAMBIO_PRATICAAIRE
(ID_MOTIVO_CAMBIO_PRATICAAIRE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_MOTIVO_CAMBIO_PRATICAAIRE ADD (
  CONSTRAINT CONF_MOTIVAZIONI_AIRE_PK
  PRIMARY KEY
  (ID_MOTIVO_CAMBIO_PRATICAAIRE)
  USING INDEX ANAG_USR.CONF_MOTIVAZIONI_AIRE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONF_MOTIVO_CAMBIO_PRATICAAIRE ADD (
  CONSTRAINT CONF_MOTIVO_CAMBIO_PRATIC_FK1 
  FOREIGN KEY (ID_TIPO_PRATICA_AIRE) 
  REFERENCES ANAG_USR.CONF_TIPO_PRATICA_AIRE (ID_TIPO_PRATICA_AIRE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_MOTIVO_PERDITA_CITTADIN
(
  ID_MOTIVO_PERDITA_CITTADIN  NUMBER            NOT NULL,
  DESCRIZIONE                 VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_MOTIVO_PERDITA_CITTAD_PK ON ANAG_USR.CONF_MOTIVO_PERDITA_CITTADIN
(ID_MOTIVO_PERDITA_CITTADIN)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_MOTIVO_PERDITA_CITTADIN ADD (
  CONSTRAINT CONF_MOTIVO_PERDITA_CITTAD_PK
  PRIMARY KEY
  (ID_MOTIVO_PERDITA_CITTADIN)
  USING INDEX ANAG_USR.CONF_MOTIVO_PERDITA_CITTAD_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_MOTIVO_ACQUISIZ_CITTADIN
(
  ID_MOTIVO_ACQUISIZ_CITTADIN  NUMBER           NOT NULL,
  DESCRIZIONE                  VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_MOTIVO_ACQUISIZ_CITTA_PK ON ANAG_USR.CONF_MOTIVO_ACQUISIZ_CITTADIN
(ID_MOTIVO_ACQUISIZ_CITTADIN)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_MOTIVO_ACQUISIZ_CITTADIN ADD (
  CONSTRAINT CONF_MOTIVO_ACQUISIZ_CITTA_PK
  PRIMARY KEY
  (ID_MOTIVO_ACQUISIZ_CITTADIN)
  USING INDEX ANAG_USR.CONF_MOTIVO_ACQUISIZ_CITTA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_MOTIVO_ANNULLA_ATT_SOGG
(
  ID           INTEGER                          NOT NULL,
  DESCRIZIONE  VARCHAR2(250 BYTE)               NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_ANNULLA_ATT_SOGG.ID IS 'Identificativo del motivo di annullamento di un attestato';

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_ANNULLA_ATT_SOGG.DESCRIZIONE IS 'Descrizione del motivo di annullamento di un attestato di soggiorno';



CREATE UNIQUE INDEX ANAG_USR.CONF_MOTIVO_ANNULLA_ATT_SO_PK ON ANAG_USR.CONF_MOTIVO_ANNULLA_ATT_SOGG
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_MOTIVO_ANNULLA_ATT_SOGG ADD (
  CONSTRAINT CONF_MOTIVO_ANNULLA_ATT_SO_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_MOTIVO_ANNULLA_ATT_SO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.PREAVVISO_RIGETTO
(
  ID_PREAVVISO_RIGETTO           NUMBER         NOT NULL,
  DATA_PREAVVISO_RIGETTO         DATE,
  NUMERO_PROTOCOLLO              NUMBER,
  ANNO_PROTOCOLLO                NUMBER,
  CAUSA_RIGETTO                  VARCHAR2(20 BYTE),
  ID_CAMBIO_RESIDENZA_DOMICILIO  NUMBER,
  ID_SOGGETTO                    NUMBER,
  TIPO_PROTOCOLLO                VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.PREAVVISO_RIGETTO.ID_PREAVVISO_RIGETTO IS 'identificativo del preavviso di rigetto';

COMMENT ON COLUMN ANAG_USR.PREAVVISO_RIGETTO.DATA_PREAVVISO_RIGETTO IS 'data in cui è stato richiesto il preavviso di rigetto per l'''' esitoIscrizione negativo';

COMMENT ON COLUMN ANAG_USR.PREAVVISO_RIGETTO.NUMERO_PROTOCOLLO IS 'numero di protocollo del documento di preavviso di rigetto';

COMMENT ON COLUMN ANAG_USR.PREAVVISO_RIGETTO.ANNO_PROTOCOLLO IS 'anno di protocollo del documento di preavviso di rigetto ';

COMMENT ON COLUMN ANAG_USR.PREAVVISO_RIGETTO.CAUSA_RIGETTO IS 'indica la tipologia di rigetto richiesta (vedi descrizione id_template 47,48,49,50)';

COMMENT ON COLUMN ANAG_USR.PREAVVISO_RIGETTO.ID_CAMBIO_RESIDENZA_DOMICILIO IS 'fk a R_soggetto_cambio_residenza';

COMMENT ON COLUMN ANAG_USR.PREAVVISO_RIGETTO.ID_SOGGETTO IS 'fk a R_soggetto_cambio_residenza';

COMMENT ON COLUMN ANAG_USR.PREAVVISO_RIGETTO.TIPO_PROTOCOLLO IS 'fk a conf_tipo_protocollo';



CREATE UNIQUE INDEX ANAG_USR.PREAVVISO_RIGETTO_PK ON ANAG_USR.PREAVVISO_RIGETTO
(ID_PREAVVISO_RIGETTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.PREAVVISO_RIGETTO ADD (
  CONSTRAINT PREAVVISO_RIGETTO_PK
  PRIMARY KEY
  (ID_PREAVVISO_RIGETTO)
  USING INDEX ANAG_USR.PREAVVISO_RIGETTO_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.PREAVVISO_RIGETTO ADD (
  CONSTRAINT PREAVVISO_RIGETTO_FK1 
  FOREIGN KEY (ID_SOGGETTO, ID_CAMBIO_RESIDENZA_DOMICILIO) 
  REFERENCES ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZA (ID_SOGGETTO,ID_CAMBIO_RESIDENZA_DOMICILIO)
  DEFERRABLE INITIALLY DEFERRED
  ENABLE VALIDATE,
  CONSTRAINT PREAVVISO_RIGETTO_FK2 
  FOREIGN KEY (TIPO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_APP_ROLE
(
  ID             NUMBER                         NOT NULL,
  ID_CONF_RUOLI  NUMBER                         NOT NULL,
  PROFILO_BE     VARCHAR2(50 CHAR)              NOT NULL,
  ID_APP_USER    NUMBER                         NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_APP_ROLE IS 'Tabella di relazione tra ruolo utente e credenziali necessarie per le chiamate di backend.';

COMMENT ON COLUMN ANAG_USR.CONF_APP_ROLE.ID IS 'Identificativo univoco';

COMMENT ON COLUMN ANAG_USR.CONF_APP_ROLE.ID_CONF_RUOLI IS 'Identificativo del ruolo associato';

COMMENT ON COLUMN ANAG_USR.CONF_APP_ROLE.PROFILO_BE IS 'Profilo associato al microservizio di backend da chiamare';

COMMENT ON COLUMN ANAG_USR.CONF_APP_ROLE.ID_APP_USER IS 'Identificativo relativo alle credenziali necessarie per le chiamate di backend.';



CREATE UNIQUE INDEX ANAG_USR.CONF_APP_ROLE_PK ON ANAG_USR.CONF_APP_ROLE
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CONF_APP_ROLE FOR ANAG_USR.CONF_APP_ROLE;


ALTER TABLE ANAG_USR.CONF_APP_ROLE ADD (
  CONSTRAINT CONF_APP_ROLE_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_APP_ROLE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONF_APP_ROLE ADD (
  CONSTRAINT CONF_APP_ROLE_APP_USER_FK 
  FOREIGN KEY (ID_APP_USER) 
  REFERENCES ANAG_USR.CONF_APP_USER (ID)
  ENABLE VALIDATE,
  CONSTRAINT CONF_APP_ROLE_RUOLI_FK 
  FOREIGN KEY (ID_CONF_RUOLI) 
  REFERENCES ANAG_USR.CONF_RUOLI (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_APP_USER
(
  ID        NUMBER                              NOT NULL,
  USERNAME  VARCHAR2(50 CHAR)                   NOT NULL,
  PASSWORD  VARCHAR2(100 CHAR)                  NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_APP_USER IS 'Tabella contenente le credenziali necessarie per le chiamate di backend associate ad uno specifico ruolo e profilo.';

COMMENT ON COLUMN ANAG_USR.CONF_APP_USER.ID IS 'Identificativo univoco';

COMMENT ON COLUMN ANAG_USR.CONF_APP_USER.USERNAME IS 'Username';

COMMENT ON COLUMN ANAG_USR.CONF_APP_USER.PASSWORD IS 'Password';



CREATE UNIQUE INDEX ANAG_USR.CONF_APP_USER_PK ON ANAG_USR.CONF_APP_USER
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CONF_APP_USER FOR ANAG_USR.CONF_APP_USER;


ALTER TABLE ANAG_USR.CONF_APP_USER ADD (
  CONSTRAINT CONF_APP_USER_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_APP_USER_PK
  ENABLE VALIDATE);

GRANT SELECT ON ANAG_USR.CONF_APP_USER TO STAT_USR;
CREATE TABLE ANAG_USR.CONF_PARAMETRI
(
  ID_CONF_PARAMETRI  NUMBER,
  NOME_UFF_ANAG      VARCHAR2(100 BYTE),
  COGNOME_UFF_ANAG   VARCHAR2(100 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_PARAMETRI.ID_CONF_PARAMETRI IS 'Identificativo della conf_parametri';

COMMENT ON COLUMN ANAG_USR.CONF_PARAMETRI.NOME_UFF_ANAG IS 'Nome dell''ufficiale dell anagrafe';

COMMENT ON COLUMN ANAG_USR.CONF_PARAMETRI.COGNOME_UFF_ANAG IS 'Cognome dell''ufficiale dell''anagrafe';



CREATE UNIQUE INDEX ANAG_USR.CONF_PARAMETRI_PK ON ANAG_USR.CONF_PARAMETRI
(ID_CONF_PARAMETRI)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_PARAMETRI ADD (
  CONSTRAINT CONF_PARAMETRI_PK
  PRIMARY KEY
  (ID_CONF_PARAMETRI)
  USING INDEX ANAG_USR.CONF_PARAMETRI_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.SOGGETTO
(
  ID_SOGGETTO                     NUMBER        NOT NULL,
  CODICE_INDIVIDUALE              VARCHAR2(20 BYTE),
  ID_SCHEDA_ANPR                  NUMBER(15),
  CODICE_FISCALE                  VARCHAR2(16 BYTE),
  VALIDITA_CF                     NUMBER(2),
  DATA_ATTRIBUZIONE_VALIDITA_CF   DATE,
  NOME                            VARCHAR2(250 BYTE),
  COGNOME                         VARCHAR2(250 BYTE),
  SESSO                           CHAR(1 BYTE),
  AIRE                            VARCHAR2(30 BYTE),
  ANNO_ESPATRIO                   NUMBER(4),
  DATA_ULTIMO_AGGIORNAMENTO       DATE,
  ID_STATO_CIVILE                 NUMBER(2),
  NOTE_STATO_CIVILE               VARCHAR2(250 BYTE),
  DATA_PRIMA_ISCRIZIONE_COMUNE    DATE,
  NUMERO_CARTA_IDENTITA           VARCHAR2(20 BYTE),
  ID_SOGGIORNO                    NUMBER,
  ID_FAMIGLIA_CONVIVENZA          NUMBER,
  ID_CENSIMENTO                   NUMBER,
  ID_CITTADINANZA                 NUMBER,
  DATA_VALIDITA_CITTADINANZA      DATE,
  ID_CITTADINANZA2                NUMBER,
  DATA_VALIDITA_CITTADINANZA2     DATE,
  ID_SENZA_FISSA_DIMORA           NUMBER,
  ID_SOGGETTO_MADRE               NUMBER,
  ID_SOGGETTO_PADRE               NUMBER,
  ID_CODICE_LEGAME_APR            NUMBER(5),
  ID_COMUNE_LEVA                  NUMBER,
  ID_COMUNE_ELETTORE              NUMBER,
  ID_MOTIVO_ISCRIZIONE_APR        NUMBER(2),
  ID_CERTIFICABILITA              NUMBER,
  ID_COND_NON_PROFESSIONALE_ANPR  NUMBER(2),
  PROGR_COMPONENTE_FAMCONV        NUMBER(4),
  DATA_DECORRENZA_FAMCONV         DATE,
  DATA_DECORRENZA_LEGAME_FAMCONV  DATE,
  ID_CODICE_LEGAME_FAMCONV        NUMBER(2),
  ID_NASCITA                      NUMBER,
  ID_MORTE                        NUMBER,
  ID_SOGGETTO_PREC                NUMBER,
  FLAG_SOGGETTO_ATTIVO            CHAR(1 BYTE),
  ID_RESPONSABILE                 NUMBER,
  ID_CERTIFICAZIONE_SOSPESA       NUMBER,
  ID_MOTIVO_MEMORIZZAZIONE        NUMBER,
  FLAG_CF_ATTIVO                  VARCHAR2(1 BYTE),
  MOTIVO_ELIMINAZIONE_CF          VARCHAR2(50 BYTE),
  POSSESSO_AUTOVEICOLI            VARCHAR2(1 BYTE),
  RECAPITO_TELEFONICO             VARCHAR2(100 BYTE),
  EMAIL                           VARCHAR2(100 BYTE),
  ID_TIPO_ISCRIZIONE              NUMBER,
  ID_STATUS_SOGGETTO              NUMBER,
  ID_DISATTIVAZIONE_SOGGETTO      NUMBER,
  ID_OPERAZIONE_ANPR              NUMBER,
  ID_ELENCO_PREP_LEVA             NUMBER,
  ID_LISTA_LEVA                   NUMBER,
  RUOLO_MATRICOLARE               NUMBER,
  FLG_VARIAZIONE_ANAG             VARCHAR2(1 BYTE),
  DATA_INSERIMENTO_LISTA_LEVA     DATE,
  DATA_VARIAZIONE_ANAGRAFICA      DATE,
  DATA_ACQUISIZIONE_CITTADINANZA  DATE,
  COMUNE_GIURAMENTO_CITT          NUMBER,
  ID_FAMIGLIA_PROVENIENZA_ANPR    VARCHAR2(20 BYTE),
  ID_SOGGETTO_REFERENTE           NUMBER,
  DATA_DECORRENZA_REFERENTE       DATE,
  DATA_DECORRENZA_RESIDENZA       DATE,
  CODICE_ANAGAIRE                 VARCHAR2(30 BYTE),
  ID_POS_PROFESSIONALE_ANPR       VARCHAR2(5 BYTE),
  ID_TITOLO_STUDIO_ANPR           VARCHAR2(5 BYTE),
  ID_ALTRO_DOC_RIC                NUMBER,
  FLG_COMUNICAZIONE_LEVA          CHAR(1 BYTE),
  FLAG_MODIFICA_LEVA              VARCHAR2(1 BYTE),
  DATA_CANCELLAZIONE_SPT          DATE,
  ID_UNICO_NAZIONALE              VARCHAR2(20 BYTE),
  DATA_FINE_ISCRIZIONE_COMUNE     DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.SOGGETTO IS 'Tabella contenente l''anagrafica di un soggetto';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_SOGGETTO IS 'Identificativo del soggetto';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.CODICE_INDIVIDUALE IS 'Codice  utilizzato in APR per identificare univocamente il soggetto.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_SCHEDA_ANPR IS 'Codice  utilizzato in ANPR per identificare univocamente il soggetto.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.CODICE_FISCALE IS 'Codice fiscale del soggetto.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.VALIDITA_CF IS 'Indica l''esito della validazione dei dati anagrafici con il servizio di AE';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.DATA_ATTRIBUZIONE_VALIDITA_CF IS 'Data in cui è stato validato il codice fiscale.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.NOME IS 'Nome del soggetto.
';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.COGNOME IS 'Cognome del soggetto.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.SESSO IS 'Sesso del soggetto';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.AIRE IS 'Flag che indica se il soggetto è iscritto all'' AIRE. 
Valorizzato con:
- S per indicare AIRE
- N per indicare non AIRE';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ANNO_ESPATRIO IS 'Anno in cui il soggetto è entrato in AIRE.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.DATA_ULTIMO_AGGIORNAMENTO IS 'data in cui la scheda del soggetto ha subito l''ultimo aggiornamento';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_STATO_CIVILE IS 'Codice identificativo dello stato civile attuale del soggetto.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.NOTE_STATO_CIVILE IS 'Campo che contiene eventuali note relative allo stato civile del soggetto.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.DATA_PRIMA_ISCRIZIONE_COMUNE IS 'Data in cui il soggetto è stato iscritto per la prima volta in APR.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.NUMERO_CARTA_IDENTITA IS 'Codice identificativo della carta d''identità associata al soggetto';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_SOGGIORNO IS 'Identificativo del permesso o attestato di soggiorno.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_FAMIGLIA_CONVIVENZA IS 'Identificativo della famiglia o convivenza in APR';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_CENSIMENTO IS 'Identificativo del censimento associato al soggetto.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_CITTADINANZA IS 'Identifica lo stato della prima cittadinanza del soggetto';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.DATA_VALIDITA_CITTADINANZA IS 'La data a partire dalla quale il soggetto ha assunto la cittadinanza indicata con ID_CITTADINANZA';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_CITTADINANZA2 IS 'Identifica lo stato della seconda cittadinanza del soggetto';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.DATA_VALIDITA_CITTADINANZA2 IS 'La data a partire dalla quale il soggetto ha assunto la cittadinanza indicata con ID_CITTADINANZA2';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_SENZA_FISSA_DIMORA IS 'Identificativo dei dati relativi ad un eventuale stato di senza fissa dimora del soggetto';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_SOGGETTO_MADRE IS 'Identificativo della madre del soggetto';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_SOGGETTO_PADRE IS 'Identificativo del padre del soggetto';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_CODICE_LEGAME_APR IS 'Codice del legame del soggetto con la famiglia o con la convivenza a cui è associato.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_COMUNE_LEVA IS 'Identificativo del comune appartenenza della lista di leva.
';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_COMUNE_ELETTORE IS 'Identificativo del comune appartenenza della lista elettorale.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_MOTIVO_ISCRIZIONE_APR IS 'Codice identificativo della motivazione per cui il soggetto è iscritto all''apr.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_CERTIFICABILITA IS 'Codice identificativo della tipologia di certificabilità che è possibile emettere ad un soggetto.
';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_COND_NON_PROFESSIONALE_ANPR IS 'Identificativo della condizione non professionale del soggetto. (in alternativa con ID_POS_PROFESSIONALE_ANPR)';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.PROGR_COMPONENTE_FAMCONV IS 'Indica il progressivo con cui il soggetto è attribuito alla famiglia.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.DATA_DECORRENZA_FAMCONV IS 'La data a partire dalla quale il soggetto appartiene alla famiglia/convivenza.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.DATA_DECORRENZA_LEGAME_FAMCONV IS 'La data a partire dalla quale il soggetto ha assunto un determinato rapporto di parentela/legame rispetto all''intestatario della scheda famiglia/convivenza';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_CODICE_LEGAME_FAMCONV IS 'Codice del legame che lega il soggetto all''intestatario della famiglia/convivenza ad esso associata.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_NASCITA IS 'Identificativo della nascita del soggetto';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_MORTE IS 'Identificativo della morte del soggetto';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.FLAG_SOGGETTO_ATTIVO IS 'Flag che identifica il soggetto attivo da quelli deprecati: S -> Attivo, N -> Deprecato';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_CERTIFICAZIONE_SOSPESA IS 'indica la lo sblocco blocco delle certificazioni del soggetto';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_MOTIVO_MEMORIZZAZIONE IS 'identificatore del motivo di memorizzazione';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.FLAG_CF_ATTIVO IS 'Flag per la validazione del codice fiscale per Variazioni Anagrafiche. S -> Attivo, N -> Cancellato';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.MOTIVO_ELIMINAZIONE_CF IS 'Motivo dell''eliminazione del codice fiscale in Variazioni Anagrafiche';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.POSSESSO_AUTOVEICOLI IS 'S se il soggetto possiede autoveicoli, N viceversa';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.RECAPITO_TELEFONICO IS 'Indica il recapito telefonico fornito dal soggetto';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.EMAIL IS 'Indica la email del soggetto';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_OPERAZIONE_ANPR IS 'Identificativo dell''operazione ANPR';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_ELENCO_PREP_LEVA IS 'Identificativo elenco preparatorio leva di appartenenza';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_LISTA_LEVA IS 'Identificativo lista di leva di appartenenza';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.FLG_VARIAZIONE_ANAG IS 'G->GENERALITA ; A-> ALTRE VARIAZIONI ANAGRAFICHE';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.DATA_INSERIMENTO_LISTA_LEVA IS 'Data in cui il soggetto è stato inserito nella lista di leva';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.DATA_VARIAZIONE_ANAGRAFICA IS 'Data dell''ultima variazione anagrafica';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.DATA_ACQUISIZIONE_CITTADINANZA IS 'Data in cui è stata acquisita la cittadinanza';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.COMUNE_GIURAMENTO_CITT IS 'Comune in cui è stato effettuato il giuramento relativo all acquisizione della cittadinanza';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_FAMIGLIA_PROVENIENZA_ANPR IS 'Identificativo famiglia provenienza associato da Anpr';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_SOGGETTO_REFERENTE IS 'IDENTIFICATIVO REFERENTE . indica il tutore della famiglia di cui il soggetto id_soggetto risulta intestatario ';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.DATA_DECORRENZA_REFERENTE IS 'data in cui è stato nominato come referente/tutore il soggetto_referente.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.DATA_DECORRENZA_RESIDENZA IS 'data in cui il soggetto ha acquisito la residenza ad esso associata.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.CODICE_ANAGAIRE IS 'Codicei identificativo AIRE';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_POS_PROFESSIONALE_ANPR IS 'Identificativo della posizione professionale del soggetto. (in alternativa con ID_COND_NON_PROFESSIONALE_ANPR)';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_TITOLO_STUDIO_ANPR IS 'Identificativo del titolo di studio del soggetto.';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_ALTRO_DOC_RIC IS 'Codice identificativo del documento di riconoscimento, diverso dalla carta d''identità italiana, associato al soggetto';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.FLG_COMUNICAZIONE_LEVA IS 'FLag che indica se è stata inviata una comunicazione massiva per la leva';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.ID_UNICO_NAZIONALE IS 'Id unico nazionale';

COMMENT ON COLUMN ANAG_USR.SOGGETTO.DATA_FINE_ISCRIZIONE_COMUNE IS 'Data fine residenza del soggetto';



CREATE UNIQUE INDEX ANAG_MIGR.COD_IND_IDX ON ANAG_USR.SOGGETTO
(CODICE_INDIVIDUALE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE INDEX ANAG_USR.IDX_SOGGETTO_MADRE ON ANAG_USR.SOGGETTO
(ID_SOGGETTO_MADRE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE INDEX ANAG_USR.IDX_SOGGETTO_NOMINATIVO ON ANAG_USR.SOGGETTO
(UPPER("COGNOME"), UPPER("NOME"), SESSO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE INDEX ANAG_USR.IDX_SOGGETTO_PADRE ON ANAG_USR.SOGGETTO
(ID_SOGGETTO_PADRE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.SOGGETTO_PK ON ANAG_USR.SOGGETTO
(ID_SOGGETTO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.SOGGETTO__UN ON ANAG_USR.SOGGETTO
(CODICE_FISCALE, ID_SCHEDA_ANPR, CODICE_INDIVIDUALE, ID_SOGGETTO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE TRIGGER ANAG_USR.INSERT_TFISCOD 
AFTER INSERT OR UPDATE OF CODICE_FISCALE ON ANAG_USR.SOGGETTO 
    FOR EACH ROW
DECLARE
    V_COUNT NUMBER;
    V_COUNT_X_COD_IND NUMBER;

BEGIN
    
    IF :NEW.CODICE_INDIVIDUALE IS NOT NULL AND LENGTH(:NEW.CODICE_INDIVIDUALE) = 7 THEN
    
        -- SE IL CF E' PRESENTE PROCEDO CON I CONTROLLI PER L'EVENTUALE INSERIMENTO
        IF :NEW.CODICE_FISCALE IS NOT NULL AND LENGTH(:NEW.CODICE_FISCALE) = 16 THEN
    
            SELECT COUNT(*) INTO V_COUNT
            FROM ANAG_USR.TFISCOD
            WHERE CODICE_INDIVIDUALE = :NEW.CODICE_INDIVIDUALE
            AND CODICE_FISCALE = :NEW.CODICE_FISCALE;
            
            -- SE NON SONO PRESENTI RECORD PER CODICE FISCALE E INDIVIDUALE
            -- PROCEDO ALL'INSERIMENTO
            IF V_COUNT = 0 THEN
            
                SELECT COUNT(*) INTO V_COUNT_X_COD_IND
                FROM ANAG_USR.TFISCOD
                WHERE CODICE_INDIVIDUALE = :NEW.CODICE_INDIVIDUALE;
                
                -- NEL CASO SIA PRESENTE UN RECORD PER CODICE INDIVIDUALE
                -- STORICIZZO E MODIFICO
                IF V_COUNT_X_COD_IND > 0 THEN
                
                    INSERT INTO ANAG_STORICO.TFISCOD(
                        SELECT * 
                        FROM ANAG_USR.TFISCOD 
                        WHERE CODICE_INDIVIDUALE = :NEW.CODICE_INDIVIDUALE
                    );
                    
                    UPDATE ANAG_USR.TFISCOD
                    SET CODICE_FISCALE = :NEW.CODICE_FISCALE, DATA_OPERAZIONE = SYSDATE
                    WHERE CODICE_INDIVIDUALE = :NEW.CODICE_INDIVIDUALE;
                
                -- ALTRIMENTI PROCEDO AL SOLO INSERIMENTO DELL'ATTUALE
                ELSE
                
                    INSERT INTO ANAG_USR.TFISCOD
                    VALUES(:NEW.CODICE_INDIVIDUALE, :NEW.CODICE_FISCALE, SYSDATE);
                
                END IF;
            
            END IF;
            
        -- SE IL CF E' STATO SBIANCATO STORICIZZO E ELIMINO IL RECORD
        ELSIF :NEW.CODICE_FISCALE IS NULL THEN
        
            INSERT INTO ANAG_STORICO.TFISCOD(
                SELECT * 
                FROM ANAG_USR.TFISCOD 
                WHERE CODICE_INDIVIDUALE = :NEW.CODICE_INDIVIDUALE
            );
            
            DELETE ANAG_USR.TFISCOD WHERE CODICE_INDIVIDUALE = :NEW.CODICE_INDIVIDUALE;
        
        END IF;
        
    END IF;
  
END;
/


CREATE OR REPLACE SYNONYM ELET_USR.SOGGETTO FOR ANAG_USR.SOGGETTO;


ALTER TABLE ANAG_USR.SOGGETTO ADD (
  CONSTRAINT SOGGETTO_PK
  PRIMARY KEY
  (ID_SOGGETTO)
  USING INDEX ANAG_USR.SOGGETTO_PK
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO__UN
  UNIQUE (CODICE_FISCALE, ID_SCHEDA_ANPR, CODICE_INDIVIDUALE, ID_SOGGETTO)
  USING INDEX ANAG_USR.SOGGETTO__UN
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.SOGGETTO ADD (
  CONSTRAINT COMUNE_GIURAMENTO_FK 
  FOREIGN KEY (COMUNE_GIURAMENTO_CITT) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT COND_NON_PROFESSIONALE_FK 
  FOREIGN KEY (ID_COND_NON_PROFESSIONALE_ANPR) 
  REFERENCES ANAG_USR.CONF_COND_NON_PROFESSIONALE (ID_COND_NON_PROFESSIONALE_ANPR)
  ENABLE VALIDATE,
  CONSTRAINT CONF_CERTIFICABILITA_FK 
  FOREIGN KEY (ID_CERTIFICABILITA) 
  REFERENCES ANAG_USR.CONF_CERTIFICABILITA (ID_CERTIFICABILITA)
  ENABLE VALIDATE,
  CONSTRAINT CONF_MOTIVO_ISCRIZIONE_APR_FK 
  FOREIGN KEY (ID_MOTIVO_ISCRIZIONE_APR) 
  REFERENCES ANAG_USR.CONF_MOTIVO_ISCRIZIONE_APR (ID_MOTIVO_ISCRIZIONE_APR)
  ENABLE VALIDATE,
  CONSTRAINT ELENCO_PREPARATORIO_FK 
  FOREIGN KEY (ID_ELENCO_PREP_LEVA) 
  REFERENCES ANAG_USR.ELENCO_PREPARATORIO_LEVA (ID_ELENCO_PREPARATORIO)
  ENABLE VALIDATE,
  CONSTRAINT FK38I18EV8NW2SKYJLE00USPBIN 
  FOREIGN KEY (ID_SOGGETTO_MADRE) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT FKLETFKDQ15D7VR763D829XG3AR 
  FOREIGN KEY (ID_SOGGETTO_PADRE) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT IDSOGGETTO_FK5 
  FOREIGN KEY (ID_SOGGETTO_REFERENTE) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT ID_ALTRO_DOC_RIC_FK 
  FOREIGN KEY (ID_ALTRO_DOC_RIC) 
  REFERENCES ANAG_USR.ALTRO_DOC_RICONOSCIMENTO (ID_DOCUMENTO)
  ENABLE VALIDATE,
  CONSTRAINT ID_CAMBIO_RESID_DOMIC_FK 
  FOREIGN KEY (ID_CENSIMENTO) 
  REFERENCES ANAG_USR.CENSIMENTO (ID_CENSIMENTO)
  ENABLE VALIDATE,
  CONSTRAINT ID_CERTIFICAZIONE_SOSPESA 
  FOREIGN KEY (ID_CERTIFICAZIONE_SOSPESA) 
  REFERENCES ANAG_USR.CERTIFICAZIONE_SOSPESA (ID_CERTIFICAZIONE_SOSPESA)
  ENABLE VALIDATE,
  CONSTRAINT ID_CITTADINANZA2_FK 
  FOREIGN KEY (ID_CITTADINANZA) 
  REFERENCES ANAG_USR.CITTADINANZA (ID_CITTADINANZA)
  ENABLE VALIDATE,
  CONSTRAINT ID_CITTADINANZA_FK 
  FOREIGN KEY (ID_CITTADINANZA2) 
  REFERENCES ANAG_USR.CITTADINANZA (ID_CITTADINANZA)
  ENABLE VALIDATE,
  CONSTRAINT ID_COMUNE_ELETTORE_FK 
  FOREIGN KEY (ID_COMUNE_ELETTORE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT ID_COMUNE_LEVA_FK 
  FOREIGN KEY (ID_COMUNE_LEVA) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT ID_MORTE_FK 
  FOREIGN KEY (ID_MORTE) 
  REFERENCES ANAG_USR.MORTE (ID_MORTE)
  ENABLE VALIDATE,
  CONSTRAINT ID_MOTIVO_MEMORIZZAZIONE_FK 
  FOREIGN KEY (ID_MOTIVO_MEMORIZZAZIONE) 
  REFERENCES ANAG_USR.CONF_MOTIVO_MEMORIZZAZIONE (ID_MOTIVO_MEMORIZZAZIONE)
  ENABLE VALIDATE,
  CONSTRAINT ID_NASCITA_FK 
  FOREIGN KEY (ID_NASCITA) 
  REFERENCES ANAG_USR.NASCITA (ID_NASCITA)
  ENABLE VALIDATE,
  CONSTRAINT ID_RESPONSABILE_FK 
  FOREIGN KEY (ID_RESPONSABILE) 
  REFERENCES ANAG_USR.RESPONSABILE_MINORE (ID_RESPONSABILE)
  ENABLE VALIDATE,
  CONSTRAINT ID_SENZA_FISSA_DIMORA_FK 
  FOREIGN KEY (ID_SENZA_FISSA_DIMORA) 
  REFERENCES ANAG_USR.SENZA_FISSA_DIMORA (ID_SENZA_FISSA_DIMORA)
  ENABLE VALIDATE,
  CONSTRAINT ID_SOGGETTO_MADRE_FK 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT ID_SOGGETTO_PADRE_FK 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT ID_SOGGIORNO_FK 
  FOREIGN KEY (ID_SOGGIORNO) 
  REFERENCES ANAG_USR.SOGGIORNO (ID_SOGGIORNO)
  ENABLE VALIDATE,
  CONSTRAINT LISTA_LEVA_FK 
  FOREIGN KEY (ID_LISTA_LEVA) 
  REFERENCES ANAG_USR.LISTE_LEVA (ID_LISTA_LEVA)
  ENABLE VALIDATE,
  CONSTRAINT NUMERO_CARTA_IDENTITA_FK 
  FOREIGN KEY (NUMERO_CARTA_IDENTITA) 
  REFERENCES ANAG_USR.CARTA_IDENTITA (NUMERO_CARTA_IDENTITA)
  ENABLE VALIDATE,
  CONSTRAINT POSIZIONE_PROFESSIONALE_FK 
  FOREIGN KEY (ID_POS_PROFESSIONALE_ANPR) 
  REFERENCES ANAG_USR.CONF_POSIZIONE_PROFESSIONALE (ID_POS_PROFESSIONALE_ANPR)
  ENABLE VALIDATE,
  CONSTRAINT RUOLO_MATRICOLARE_FK 
  FOREIGN KEY (RUOLO_MATRICOLARE) 
  REFERENCES ANAG_USR.RUOLO_MATRICOLARE (ID_RUOLO_MATRICOLARE)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_CODICE_LEGAME_FK 
  FOREIGN KEY (ID_CODICE_LEGAME_FAMCONV) 
  REFERENCES ANAG_USR.CONF_CODICE_LEGAME (ID_CODICE_LEGAME)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_CODICE_LEGAME_FK1 
  FOREIGN KEY (ID_CODICE_LEGAME_APR) 
  REFERENCES ANAG_USR.CONF_CODICE_LEGAME (ID_CODICE_LEGAME)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_CONF_STATO_CIVILE_FK 
  FOREIGN KEY (ID_STATO_CIVILE) 
  REFERENCES ANAG_USR.CONF_STATO_CIVILE (ID_STATO_CIVILE)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_FAM_CONV_FK1 
  FOREIGN KEY (ID_FAMIGLIA_CONVIVENZA) 
  REFERENCES ANAG_USR.FAMIGLIA_CONVIVENZA (ID_FAMIGLIA_CONV)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_FK1 
  FOREIGN KEY (ID_TIPO_ISCRIZIONE) 
  REFERENCES ANAG_USR.CONF_TIPO_ISCRIZIONE (ID_TIPO_ISCRIZIONE)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_FK2 
  FOREIGN KEY (ID_STATUS_SOGGETTO) 
  REFERENCES ANAG_USR.CONF_STATUS_SOGGETTO (ID_STATUS_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_FK3 
  FOREIGN KEY (ID_DISATTIVAZIONE_SOGGETTO) 
  REFERENCES ANAG_USR.CONF_DISATTIVAZIONE_SOGGETTO (ID_DISATTIVAZIONE_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_FK4 
  FOREIGN KEY (ID_OPERAZIONE_ANPR) 
  REFERENCES ANAG_USR.OPERAZIONE_ANPR (ID_OPERAZIONE_ANPR)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_TITOLO_STUDIO_FK 
  FOREIGN KEY (ID_TITOLO_STUDIO_ANPR) 
  REFERENCES ANAG_USR.CONF_TITOLI_STUDIO (ID_TITOLO_STUDIO_ANPR)
  ENABLE VALIDATE);

GRANT REFERENCES ON ANAG_USR.SOGGETTO TO ELET_USR;
CREATE TABLE ANAG_USR.CONF_TIPO_ALLEGATO_CRI
(
  ID_TIPO_ALLEGATO_CRI      NUMBER              NOT NULL,
  NOME_ALLEGATO             VARCHAR2(80 BYTE),
  FLAG_OBBLIGATORIO         VARCHAR2(1 BYTE),
  FLAG_ATTIVO               VARCHAR2(1 BYTE),
  FLAG_CONTRATTO_ABITATIVO  NUMBER,
  COMUNITARIO               CHAR(1 BYTE),
  FLAG_ENTRATA_FAMIGLIA     NUMBER,
  TIPO_ESTENSIONE_ALLEGATO  NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_ALLEGATO_CRI.FLAG_OBBLIGATORIO IS 'S -> OBBLIGATORIO; N-> NON OBBLIGATORIO ';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_ALLEGATO_CRI.FLAG_ATTIVO IS 'S->ATTIVO; N-> NON ATTIVO';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_ALLEGATO_CRI.FLAG_CONTRATTO_ABITATIVO IS 'IDENTIFICA LA TIPOLOGIA  DI ALLEGATI NECESSARI RELATIVI AL CONTRATTO ABITATIVO';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_ALLEGATO_CRI.TIPO_ESTENSIONE_ALLEGATO IS 'FK logica a conf_estensione_allegati. indica la tipologia di estensioni ammesse per l'' allegato CRI';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_ALLEGATO_CRI_PK ON ANAG_USR.CONF_TIPO_ALLEGATO_CRI
(ID_TIPO_ALLEGATO_CRI)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_ALLEGATO_CRI ADD (
  CONSTRAINT CONF_TIPO_ALLEGATO_CRI_PK
  PRIMARY KEY
  (ID_TIPO_ALLEGATO_CRI)
  USING INDEX ANAG_USR.CONF_TIPO_ALLEGATO_CRI_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.ALLEGATO_CRI
(
  ID_ALLEGATO_CRI                NUMBER         NOT NULL,
  ID_TIPO_ALLEGATO_CRI           NUMBER         NOT NULL,
  NOME_FILE                      VARCHAR2(80 BYTE) NOT NULL,
  DOCUMENTO                      BLOB           NOT NULL,
  DATA_CARICAMENTO               TIMESTAMP(6)   NOT NULL,
  ID_CAMBIO_RESIDENZA_DOMICILIO  NUMBER         NOT NULL,
  ID_CAMBIO_RESIDENZA_ONLINE     NUMBER,
  ID_SOGGETTO_ONLINE             NUMBER
)
LOB (DOCUMENTO) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.ALLEGATO_CRI_PK ON ANAG_USR.ALLEGATO_CRI
(ID_ALLEGATO_CRI)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.ALLEGATO_CRI ADD (
  CONSTRAINT ALLEGATO_CRI_PK
  PRIMARY KEY
  (ID_ALLEGATO_CRI)
  USING INDEX ANAG_USR.ALLEGATO_CRI_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.ALLEGATO_CRI ADD (
  CONSTRAINT ALLEGATO_CAMBIO_RES_FK 
  FOREIGN KEY (ID_CAMBIO_RESIDENZA_DOMICILIO) 
  REFERENCES ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO (ID_CAMBIO_RESIDENZA_DOMICILIO)
  ENABLE VALIDATE,
  CONSTRAINT CONF_TIPO_ALLEGATO_CRI_FK1 
  FOREIGN KEY (ID_TIPO_ALLEGATO_CRI) 
  REFERENCES ANAG_USR.CONF_TIPO_ALLEGATO_CRI (ID_TIPO_ALLEGATO_CRI)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_ONLINE_FK 
  FOREIGN KEY (ID_SOGGETTO_ONLINE) 
  REFERENCES ANAG_USR.SOGGETTO_CRI_ONLINE (ID_SOGGETTO_ONLINE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONTRATTO_ABITATIVO
(
  ID_CONTRATTO_ABITATIVO  NUMBER                NOT NULL,
  TIPO_CONTRATTO          NUMBER                NOT NULL,
  NOME_OSPITANTE          VARCHAR2(250 BYTE),
  COGNOME_OSPITANTE       VARCHAR2(250 BYTE),
  ID_COMUNE               NUMBER,
  NUMERO_REGISTRAZIONE    VARCHAR2(50 BYTE),
  DATA_REGISTRAZIONE      DATE,
  NOTE                    VARCHAR2(4000 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.TABLE1_PK ON ANAG_USR.CONTRATTO_ABITATIVO
(ID_CONTRATTO_ABITATIVO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONTRATTO_ABITATIVO ADD (
  CONSTRAINT TABLE1_PK
  PRIMARY KEY
  (ID_CONTRATTO_ABITATIVO)
  USING INDEX ANAG_USR.TABLE1_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONTRATTO_ABITATIVO ADD (
  CONSTRAINT ID_COMUNE_FK1 
  FOREIGN KEY (ID_COMUNE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_MOTIVO_COSTITUZIONE
(
  ID_MOTIVO_COSTITUZIONE  NUMBER                NOT NULL,
  DESCRIZIONE             VARCHAR2(50 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_MOTIVO_COSTITUZIONE_PK ON ANAG_USR.CONF_MOTIVO_COSTITUZIONE
(ID_MOTIVO_COSTITUZIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_MOTIVO_COSTITUZIONE ADD (
  CONSTRAINT CONF_MOTIVO_COSTITUZIONE_PK
  PRIMARY KEY
  (ID_MOTIVO_COSTITUZIONE)
  USING INDEX ANAG_USR.CONF_MOTIVO_COSTITUZIONE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_SPECIE_CONVIVENZA
(
  ID_SPECIE_CONVIVENZA  NUMBER                  NOT NULL,
  DESCRIZIONE           VARCHAR2(50 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_SPECIE_CONVIVENZA_PK ON ANAG_USR.CONF_SPECIE_CONVIVENZA
(ID_SPECIE_CONVIVENZA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_SPECIE_CONVIVENZA ADD (
  CONSTRAINT CONF_SPECIE_CONVIVENZA_PK
  PRIMARY KEY
  (ID_SPECIE_CONVIVENZA)
  USING INDEX ANAG_USR.CONF_SPECIE_CONVIVENZA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_CERTIFICATO
(
  ID_CONF_CERTIFICATO        NUMBER             NOT NULL,
  ID_TIPO_CERTIFICATO        NUMBER,
  DESCRIZIONE                VARCHAR2(1000 BYTE),
  FLG_ANAG_SC                CHAR(1 BYTE),
  FLG_ONEROSO                CHAR(1 BYTE),
  FLG_ONLINE                 CHAR(1 BYTE),
  FLG_IN_BOLLO               CHAR(1 BYTE),
  ID_R_CONF_CERT_CUMULATIVO  NUMBER,
  FLG_RITIRO_SUCC            CHAR(1 BYTE),
  FLG_NOTE_CERTIFICATO       CHAR(1 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_CERTIFICATO.ID_CONF_CERTIFICATO IS 'identificativo del certificato';

COMMENT ON COLUMN ANAG_USR.CONF_CERTIFICATO.ID_TIPO_CERTIFICATO IS 'identificativo del tipo certificato';

COMMENT ON COLUMN ANAG_USR.CONF_CERTIFICATO.DESCRIZIONE IS 'descrizione del certificato';

COMMENT ON COLUMN ANAG_USR.CONF_CERTIFICATO.FLG_ANAG_SC IS 'A -> Identifica un certificato Anagrafico
S -> Identifica un certificato di Stato Civile';

COMMENT ON COLUMN ANAG_USR.CONF_CERTIFICATO.FLG_ONEROSO IS 'S -> Identifica un certificato che prevede un corrispettivo economico per l''emissione
N -> Identifica un certificato a titolo gratuito.';

COMMENT ON COLUMN ANAG_USR.CONF_CERTIFICATO.FLG_ONLINE IS 'S -> Identifica un certificato emettibile online
N -> Identifica un certificato da emettere a sportello';

COMMENT ON COLUMN ANAG_USR.CONF_CERTIFICATO.FLG_IN_BOLLO IS 'S-> può essere in bollo, N-> non puo essere in bollo';

COMMENT ON COLUMN ANAG_USR.CONF_CERTIFICATO.ID_R_CONF_CERT_CUMULATIVO IS 'Identificattivo della r_conf_cert_cumulativo, se diverso da null significa che la conf certificato è cumulativo';

COMMENT ON COLUMN ANAG_USR.CONF_CERTIFICATO.FLG_RITIRO_SUCC IS 'Indica se questo tipo di certificato è a ritiro successivo oppure no.
S-> ritiro successivo , N-> ritiro immediato';

COMMENT ON COLUMN ANAG_USR.CONF_CERTIFICATO.FLG_NOTE_CERTIFICATO IS 'Indica se al certificato associato è possibile inserire una nota per il rilascio. S -> si, N/null -> no';



CREATE UNIQUE INDEX ANAG_USR.CONF_CERTIFICATO_PK ON ANAG_USR.CONF_CERTIFICATO
(ID_CONF_CERTIFICATO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_CERTIFICATO ADD (
  CONSTRAINT CONF_CERTIFICATO_PK
  PRIMARY KEY
  (ID_CONF_CERTIFICATO)
  USING INDEX ANAG_USR.CONF_CERTIFICATO_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONF_CERTIFICATO ADD (
  CONSTRAINT ID_TIPO_CERTIFICATO_FK 
  FOREIGN KEY (ID_TIPO_CERTIFICATO) 
  REFERENCES ANAG_USR.CONF_TIPO_CERTIFICATO (ID_CONF_TIPO_CERTIFICATO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_ESENZIONE_CERT_ANPR
(
  ID_ESEN_CERT  NUMBER,
  ID_ESEN_ANPR  NUMBER                          NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.R_ESENZIONE_CERT_ANPR.ID_ESEN_CERT IS 'Identificati dell id_esenzione gestito dal comune di ROMA
';

COMMENT ON COLUMN ANAG_USR.R_ESENZIONE_CERT_ANPR.ID_ESEN_ANPR IS 'Identificato dell''id_esenzione gestito da ANPR';



CREATE UNIQUE INDEX ANAG_USR.R_ESENZIONE_CERT_ANPR_PK ON ANAG_USR.R_ESENZIONE_CERT_ANPR
(ID_ESEN_CERT)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_ESENZIONE_CERT_ANPR ADD (
  CONSTRAINT R_ESENZIONE_CERT_ANPR_PK
  PRIMARY KEY
  (ID_ESEN_CERT)
  USING INDEX ANAG_USR.R_ESENZIONE_CERT_ANPR_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.RUOLO_MATRICOLARE
(
  ID_RUOLO_MATRICOLARE     NUMBER               NOT NULL,
  ANNO_ISCR_LEVA           NUMBER,
  PROG_ISCR_LEVA           VARCHAR2(20 BYTE),
  ANNO_SUCC_ISCR           NUMBER,
  PROG_SUCC_ISCR           VARCHAR2(20 BYTE),
  COMUNE_ISCR              NUMBER,
  DISTRETTO                NUMBER,
  DATA_VISITA_LEVA         DATE,
  ESITO_VISITA_LEVA        NUMBER,
  DATA_ARRUOLAMENTO        DATE,
  DATA_CONGEDO             DATE,
  ARMA                     NUMBER,
  MATRICOLA                VARCHAR2(20 BYTE),
  CORPO                    VARCHAR2(400 BYTE),
  GRADO                    NUMBER,
  COND_PARTICOLARI         NUMBER,
  MOTIVO                   VARCHAR2(20 BYTE),
  DATA_MOTIVO              DATE,
  NUMERO_ORDINE            VARCHAR2(20 BYTE),
  COMUNE_INVIO_COM         NUMBER,
  FLAG_ATTIVO              VARCHAR2(1 BYTE),
  FLAG_RINUNCIA_OBIETTORE  VARCHAR2(1 BYTE),
  DATA_RINUNCIA            DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.RUOLO_MATRICOLARE.ID_RUOLO_MATRICOLARE IS 'identificativo del ruolo matricolare';

COMMENT ON COLUMN ANAG_USR.RUOLO_MATRICOLARE.COMUNE_ISCR IS 'comune di iscrizione alla lista di leva';

COMMENT ON COLUMN ANAG_USR.RUOLO_MATRICOLARE.DISTRETTO IS 'distretto di leva';

COMMENT ON COLUMN ANAG_USR.RUOLO_MATRICOLARE.DATA_VISITA_LEVA IS 'data in cui è avvenuta la visita di leva';

COMMENT ON COLUMN ANAG_USR.RUOLO_MATRICOLARE.ESITO_VISITA_LEVA IS 'esito leva militare';

COMMENT ON COLUMN ANAG_USR.RUOLO_MATRICOLARE.DATA_ARRUOLAMENTO IS 'data di arruolamento';

COMMENT ON COLUMN ANAG_USR.RUOLO_MATRICOLARE.DATA_CONGEDO IS 'data di congedo';

COMMENT ON COLUMN ANAG_USR.RUOLO_MATRICOLARE.COMUNE_INVIO_COM IS 'comune al quale viene inviato l''estratto del ruolo matricolare';

COMMENT ON COLUMN ANAG_USR.RUOLO_MATRICOLARE.FLAG_ATTIVO IS 'N rende il ruolo non attivo';



CREATE UNIQUE INDEX ANAG_USR.RUOLO_MATRICOLARE_PK ON ANAG_USR.RUOLO_MATRICOLARE
(ID_RUOLO_MATRICOLARE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.RUOLO_MATRICOLARE ADD (
  CONSTRAINT RUOLO_MATRICOLARE_PK
  PRIMARY KEY
  (ID_RUOLO_MATRICOLARE)
  USING INDEX ANAG_USR.RUOLO_MATRICOLARE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.RUOLO_MATRICOLARE ADD (
  CONSTRAINT ARMA_FK 
  FOREIGN KEY (ARMA) 
  REFERENCES ANAG_USR.CONF_ARMA_MILITARE (ID_ARMA_MILITARE)
  ENABLE VALIDATE,
  CONSTRAINT COMUNE_INVIO_COM_FK 
  FOREIGN KEY (COMUNE_INVIO_COM) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT COMUNE_ISCR_FK 
  FOREIGN KEY (COMUNE_ISCR) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT COND_PART_FK 
  FOREIGN KEY (COND_PARTICOLARI) 
  REFERENCES ANAG_USR.CONF_COND_PART_LEVA (ID_COND_PART_LEVA)
  ENABLE VALIDATE,
  CONSTRAINT DISTRETTO_FK 
  FOREIGN KEY (DISTRETTO) 
  REFERENCES ANAG_USR.CONF_DISTRETTI_MILITARI (ID_DISTRETTO)
  ENABLE VALIDATE,
  CONSTRAINT ESITO_VISITA_LEVA_FK1 
  FOREIGN KEY (ESITO_VISITA_LEVA) 
  REFERENCES ANAG_USR.CONF_ESITO_LEVA (ID_ESITO)
  ENABLE VALIDATE,
  CONSTRAINT GRADO_FK 
  FOREIGN KEY (GRADO) 
  REFERENCES ANAG_USR.CONF_GRADO_MILITARE (ID_GRADO_MILITARE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_SPECIE_TOPONIMO
(
  ID_TIPO_SPECIE_TOPONIMO  NUMBER               NOT NULL,
  DESCRIZIONE              VARCHAR2(40 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_SPECIE_TOPONIMO.ID_TIPO_SPECIE_TOPONIMO IS 'Identificativo della specie del toponimo';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_SPECIE_TOPONIMO.DESCRIZIONE IS 'Nome del toponimo';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_SPECIE_PK ON ANAG_USR.CONF_TIPO_SPECIE_TOPONIMO
(ID_TIPO_SPECIE_TOPONIMO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_SPECIE_TOPONIMO ADD (
  CONSTRAINT CONF_TIPO_SPECIE_PK
  PRIMARY KEY
  (ID_TIPO_SPECIE_TOPONIMO)
  USING INDEX ANAG_USR.CONF_TIPO_SPECIE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.PRATICA_CERTIFICATI
(
  ID_PRATICA_CERTIFICATI  NUMBER                NOT NULL,
  DATA_APERTURA           DATE,
  NUMERO_PRATICA          VARCHAR2(200 BYTE),
  DATI_PRATICA            CLOB,
  DATA_CHIUSURA           DATE,
  FLG_TIPO_RICHIESTA      CHAR(1 BYTE),
  ID_STATO_PRATICA        NUMBER,
  ANNO_PROTOCOLLO         NUMBER,
  NUMERO_PROTOCOLLO       NUMBER,
  TIPO_PROTOCOLLO         VARCHAR2(20 BYTE),
  ID_USER_RICH            NUMBER,
  ID_USER_GESTORE         NUMBER
)
LOB (DATI_PRATICA) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.PRATICA_CERTIFICATI.ID_PRATICA_CERTIFICATI IS 'Identificativo di una pratica per la richiesta di certificati';

COMMENT ON COLUMN ANAG_USR.PRATICA_CERTIFICATI.DATA_APERTURA IS 'Data di apertura della richiesta';

COMMENT ON COLUMN ANAG_USR.PRATICA_CERTIFICATI.NUMERO_PRATICA IS 'Numero che identifica la pratica';

COMMENT ON COLUMN ANAG_USR.PRATICA_CERTIFICATI.DATI_PRATICA IS 'Contiene dati specifici per le varie tipologie di richieste:

- uno o più idCertificatoRichiesto (uno o più certificati richiesti nella pratica)

- idConfAllegatiCertificato (per la gestione degli allegati associati a una pratica)

- idRichiedente (per cittadini)

- idOperatore (per sportellisti)

- inQualitaDi (stringa)';

COMMENT ON COLUMN ANAG_USR.PRATICA_CERTIFICATI.DATA_CHIUSURA IS 'Data di chiusura della richiesta';

COMMENT ON COLUMN ANAG_USR.PRATICA_CERTIFICATI.FLG_TIPO_RICHIESTA IS '1-> ONLINE , 2-> PER POSTA (CORRISPONDENZA), 3 -> SPORTELLO, 4 -> PRATICA ENTI ESTERNI';

COMMENT ON COLUMN ANAG_USR.PRATICA_CERTIFICATI.ID_STATO_PRATICA IS 'Identificativo dello stato della pratica corrente relativa alla tabella CONF_STATO_PRATICA';

COMMENT ON COLUMN ANAG_USR.PRATICA_CERTIFICATI.ANNO_PROTOCOLLO IS 'anno protocollo richiesta certificati per posta';

COMMENT ON COLUMN ANAG_USR.PRATICA_CERTIFICATI.NUMERO_PROTOCOLLO IS 'numero protocollo richiesta certificati per posta';

COMMENT ON COLUMN ANAG_USR.PRATICA_CERTIFICATI.TIPO_PROTOCOLLO IS 'tipo protocollo richiesta certificati per posta';

COMMENT ON COLUMN ANAG_USR.PRATICA_CERTIFICATI.ID_USER_RICH IS 'id utente creazione richiesta';

COMMENT ON COLUMN ANAG_USR.PRATICA_CERTIFICATI.ID_USER_GESTORE IS 'id utente che gestisce la richiesta';



CREATE UNIQUE INDEX ANAG_USR.RICHIESTA_CERTIFICATI_PK ON ANAG_USR.PRATICA_CERTIFICATI
(ID_PRATICA_CERTIFICATI)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.PRATICA_CERTIFICATI ADD (
  CONSTRAINT RICHIESTA_CERTIFICATI_PK
  PRIMARY KEY
  (ID_PRATICA_CERTIFICATI)
  USING INDEX ANAG_USR.RICHIESTA_CERTIFICATI_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.PRATICA_CERTIFICATI ADD (
  CONSTRAINT ID_STATO_PRATICA_FK 
  FOREIGN KEY (ID_STATO_PRATICA) 
  REFERENCES ANAG_USR.CONF_STATO_PRATICA (ID_STATO_PRATICA)
  ENABLE VALIDATE,
  CONSTRAINT ID_TIPO_PROTOCOLLO_FK 
  FOREIGN KEY (TIPO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE,
  CONSTRAINT PRATICA_USER_GEST_FK 
  FOREIGN KEY (ID_USER_GESTORE) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE,
  CONSTRAINT PRATICA_USER_RICH_FK 
  FOREIGN KEY (ID_USER_RICH) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.ALLEGATO_CERTIFICATO
(
  ID_ALLEGATO_CERTIFICATO       NUMBER          NOT NULL,
  DOCUMENTO                     BLOB,
  NOME_FILE                     VARCHAR2(150 BYTE),
  DATA_CARICAMENTO              DATE,
  ID_TIPO_ALLEGATO_CERTIFICATO  NUMBER
)
LOB (DOCUMENTO) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.ALLEGATO_CERTIFICATO.ID_ALLEGATO_CERTIFICATO IS 'Id dell''allegato';

COMMENT ON COLUMN ANAG_USR.ALLEGATO_CERTIFICATO.DOCUMENTO IS 'Documento allegato';

COMMENT ON COLUMN ANAG_USR.ALLEGATO_CERTIFICATO.NOME_FILE IS 'Indica il nome del documento';

COMMENT ON COLUMN ANAG_USR.ALLEGATO_CERTIFICATO.DATA_CARICAMENTO IS 'Indica la data del caricamento del file';

COMMENT ON COLUMN ANAG_USR.ALLEGATO_CERTIFICATO.ID_TIPO_ALLEGATO_CERTIFICATO IS 'indica la tipologia di allegato certificato';



CREATE UNIQUE INDEX ANAG_USR.ALLEGATO_CERTIFICATO_PK ON ANAG_USR.ALLEGATO_CERTIFICATO
(ID_ALLEGATO_CERTIFICATO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.ALLEGATO_CERTIFICATO ADD (
  CONSTRAINT ALLEGATO_CERTIFICATO_PK
  PRIMARY KEY
  (ID_ALLEGATO_CERTIFICATO)
  USING INDEX ANAG_USR.ALLEGATO_CERTIFICATO_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.ALLEGATO_CERTIFICATO ADD (
  CONSTRAINT ALLEGATO_CERTIFICATO_FK1 
  FOREIGN KEY (ID_TIPO_ALLEGATO_CERTIFICATO) 
  REFERENCES ANAG_USR.CONF_TIPO_ALLEGATO_CERTIFICATO (ID_TIPO_ALLEGATO_CERTIFICATO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.ACCERTAMENTO_ISCRIZIONE
(
  ID_ACCERTAMENTO_ISCRIZIONE  NUMBER            NOT NULL,
  ID_CAMBIO_DOMICILIO         NUMBER,
  CODICE_TIPO_PROTOCOLLO      VARCHAR2(10 CHAR),
  ANNO_PROTOCOLLO             NUMBER,
  NUMERO_PROTOCOLLO           NUMBER,
  NUMERO_ACCERTAMENTO         NUMBER,
  ANNO_PRATICA                NUMBER,
  NUMERO_PRATICA              NUMBER,
  ID_GRUPPO_PL                NUMBER            NOT NULL,
  DATA_PREVISTA               DATE,
  DATA_EFFETTIVA              DATE,
  ID_STATO_PRATICA            NUMBER,
  DATA_RICHIESTA              DATE,
  ID_POP_TEMP                 NUMBER,
  ANNO_PROTOCOLLO_VIGILE      NUMBER,
  NUMERO_PROTOCOLLO_VIGILE    NUMBER,
  TIPO_PROTOCOLLO_VIGILE      VARCHAR2(20 BYTE),
  VERBALE_ACCERTAMENTO        BLOB,
  NOME_VERBALE_ACCERTAMENTO   VARCHAR2(250 BYTE),
  NOTE                        VARCHAR2(4000 BYTE),
  ID_SOGGETTO                 NUMBER
)
LOB (VERBALE_ACCERTAMENTO) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.ACCERTAMENTO_ISCRIZIONE IS 'La tabella contiene le richieste di accertamento inviate ai Gruppi di Polizia Locale relative ad un procedimento di cambio di residenza/domicilio o ad un procedimento di irreperibilità.';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_ISCRIZIONE.ID_ACCERTAMENTO_ISCRIZIONE IS 'Identificativo dell''accertamento';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_ISCRIZIONE.ID_CAMBIO_DOMICILIO IS 'FK che relazione l''accertamento ad un cambio di domicilio';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_ISCRIZIONE.CODICE_TIPO_PROTOCOLLO IS 'Codice identificativo del protocollo di richiesta di accertamento';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_ISCRIZIONE.ANNO_PROTOCOLLO IS 'Anno del protocollo di richiesta di accertamento';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_ISCRIZIONE.NUMERO_PROTOCOLLO IS 'Numero del protocollo di richiesta di accertamento';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_ISCRIZIONE.NUMERO_ACCERTAMENTO IS 'Numero di accertamento';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_ISCRIZIONE.ANNO_PRATICA IS 'Anno della pratica';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_ISCRIZIONE.NUMERO_PRATICA IS 'Numero Pratica';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_ISCRIZIONE.ID_GRUPPO_PL IS 'Identificativo del gruppo di polizia locale a cui è stata inoltrata la richiesta di accertamento';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_ISCRIZIONE.DATA_PREVISTA IS 'Data prevista per l''accertamento';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_ISCRIZIONE.DATA_EFFETTIVA IS 'Data effettiva dell''accertamento';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_ISCRIZIONE.ID_STATO_PRATICA IS 'Id che identifica lo stato della pratica';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_ISCRIZIONE.DATA_RICHIESTA IS 'Data in cui è stata effettuata la richiesta di accertamento';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_ISCRIZIONE.ID_POP_TEMP IS 'Identificativo della pratica per la popolazione temporanea come chiave esterna';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_ISCRIZIONE.ANNO_PROTOCOLLO_VIGILE IS 'anno protocollo relativo all'' esitodell'' accertamento da parte del vigile';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_ISCRIZIONE.NUMERO_PROTOCOLLO_VIGILE IS 'numero protocollo relativo all'' esitodell'' accertamento da parte del vigile';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_ISCRIZIONE.TIPO_PROTOCOLLO_VIGILE IS 'tipo protocollo relativo all'' esitodell'' accertamento da parte del vigile';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_ISCRIZIONE.ID_SOGGETTO IS 'Campo che identifica il soggetto per il quale è stato inserito l''accertamento';



CREATE UNIQUE INDEX ANAG_USR.ACCERTAMENTO_PK ON ANAG_USR.ACCERTAMENTO_ISCRIZIONE
(ID_ACCERTAMENTO_ISCRIZIONE)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.PRATICA ON ANAG_USR.ACCERTAMENTO_ISCRIZIONE
(ANNO_PRATICA, NUMERO_PRATICA)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.PROTOCOLLO ON ANAG_USR.ACCERTAMENTO_ISCRIZIONE
(CODICE_TIPO_PROTOCOLLO, NUMERO_PROTOCOLLO, ANNO_PROTOCOLLO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.ACCERTAMENTO_ISCRIZIONE ADD (
  CONSTRAINT ACCERTAMENTO_PK
  PRIMARY KEY
  (ID_ACCERTAMENTO_ISCRIZIONE)
  USING INDEX ANAG_USR.ACCERTAMENTO_PK
  ENABLE VALIDATE,
  CONSTRAINT PRATICA
  UNIQUE (ANNO_PRATICA, NUMERO_PRATICA)
  USING INDEX ANAG_USR.PRATICA
  ENABLE VALIDATE,
  CONSTRAINT PROTOCOLLO
  UNIQUE (CODICE_TIPO_PROTOCOLLO, NUMERO_PROTOCOLLO, ANNO_PROTOCOLLO)
  USING INDEX ANAG_USR.PROTOCOLLO
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.ACCERTAMENTO_ISCRIZIONE ADD (
  CONSTRAINT ACCERTAMENTO_FK1 
  FOREIGN KEY (CODICE_TIPO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE,
  CONSTRAINT ACCERTAMENTO_ISCRIZIONE_FK1 
  FOREIGN KEY (TIPO_PROTOCOLLO_VIGILE) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE,
  CONSTRAINT ACC_CONF_STATO_PRATICA_FK 
  FOREIGN KEY (ID_STATO_PRATICA) 
  REFERENCES ANAG_USR.CONF_STATO_PRATICA (ID_STATO_PRATICA)
  ENABLE VALIDATE,
  CONSTRAINT CAMBI_RESIDENZA_DOMICILIO_FK 
  FOREIGN KEY (ID_CAMBIO_DOMICILIO) 
  REFERENCES ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO (ID_CAMBIO_RESIDENZA_DOMICILIO)
  ENABLE VALIDATE,
  CONSTRAINT CONF_STRUTTURE_INTERNE_RC_FK 
  FOREIGN KEY (ID_GRUPPO_PL) 
  REFERENCES ANAG_USR.CONF_STRUTTURE_INTERNE_RC (ID)
  ENABLE VALIDATE,
  CONSTRAINT ID_SOGGETTO_FK2 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT POP_TEMP_FK 
  FOREIGN KEY (ID_POP_TEMP) 
  REFERENCES ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA (ID_PRATICA)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.ACCERTAMENTO_CANCELLAZIONE
(
  ID_ACCERTAMENTO_CANC       NUMBER             NOT NULL,
  ID_IRREPERIBILITA          NUMBER,
  CODICE_TIPO_PROTOCOLLO     VARCHAR2(20 BYTE),
  ANNO_PROTOCOLLO            NUMBER,
  NUMERO_PROTOCOLLO          NUMBER,
  NUMERO_ACCERTAMENTO        NUMBER,
  ANNO_PRATICA               NUMBER,
  NUMERO_PRATICA             NUMBER,
  ID_GRUPPO_PL               NUMBER,
  DATA_PREVISTA              DATE,
  ID_STATO_PRATICA           NUMBER,
  DATA_RICHIESTA             DATE,
  DATA_SOPRALLUOGO           DATE,
  ESITO                      VARCHAR2(20 BYTE),
  ID_STATO_ESTERO            NUMBER,
  ID_COMUNE                  NUMBER,
  NOTE                       VARCHAR2(20 BYTE),
  ID_LOCALITA                NUMBER,
  NUMERO_PROTOCOLLO_VIGILE   NUMBER,
  ANNO_PROTOCOLLO_VIGILE     NUMBER,
  TIPO_PROTOCOLLO_VIGILE     VARCHAR2(20 BYTE),
  VERBALE_ACCERTAMENTO       BLOB,
  NOME_VERBALE_ACCERTAMENTO  VARCHAR2(250 BYTE)
)
LOB (VERBALE_ACCERTAMENTO) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_CANCELLAZIONE.ID_ACCERTAMENTO_CANC IS 'Identificativo dell''accertamento';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_CANCELLAZIONE.ESITO IS '1-> POSITIVO 0->NEGATIVO';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_CANCELLAZIONE.ID_STATO_ESTERO IS 'Stato In cui il soggetto si è trasferito';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_CANCELLAZIONE.ID_COMUNE IS 'Comune Italiano  in cui il soggetto si è trasferito';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_CANCELLAZIONE.ID_LOCALITA IS 'Comune Estero in cui il soggetto si è trasferito';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_CANCELLAZIONE.NUMERO_PROTOCOLLO_VIGILE IS 'numero protocollo esito accertamento vigile';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_CANCELLAZIONE.ANNO_PROTOCOLLO_VIGILE IS 'anno protocollo esito accertamento vigile';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_CANCELLAZIONE.TIPO_PROTOCOLLO_VIGILE IS 'tipo protocollo esito accertamento vigile';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_CANCELLAZIONE.VERBALE_ACCERTAMENTO IS 'verbale di accertamento';

COMMENT ON COLUMN ANAG_USR.ACCERTAMENTO_CANCELLAZIONE.NOME_VERBALE_ACCERTAMENTO IS 'nome pdf verbale accertamento';



CREATE UNIQUE INDEX ANAG_USR.ACCERTAMENTO_CANCELLAZIONE_PK ON ANAG_USR.ACCERTAMENTO_CANCELLAZIONE
(ID_ACCERTAMENTO_CANC)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.ACCERTAMENTO_CANCELLAZIONE ADD (
  CONSTRAINT ACCERTAMENTO_CANCELLAZIONE_PK
  PRIMARY KEY
  (ID_ACCERTAMENTO_CANC)
  USING INDEX ANAG_USR.ACCERTAMENTO_CANCELLAZIONE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.ACCERTAMENTO_CANCELLAZIONE ADD (
  CONSTRAINT ACCERTAMENTO_CANCELLAZION_FK1 
  FOREIGN KEY (ID_IRREPERIBILITA) 
  REFERENCES ANAG_USR.IRREPERIBILITA (ID_IRREPERIBILITA)
  ENABLE VALIDATE,
  CONSTRAINT ACCERTAMENTO_CANCELLAZION_FK2 
  FOREIGN KEY (CODICE_TIPO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE,
  CONSTRAINT ACCERTAMENTO_CANCELLAZION_FK3 
  FOREIGN KEY (ID_GRUPPO_PL) 
  REFERENCES ANAG_USR.CONF_STRUTTURE_INTERNE_RC (ID)
  ENABLE VALIDATE,
  CONSTRAINT ACCERTAMENTO_CANCELLAZION_FK4 
  FOREIGN KEY (ID_STATO_PRATICA) 
  REFERENCES ANAG_USR.CONF_STATO_PRATICA (ID_STATO_PRATICA)
  ENABLE VALIDATE,
  CONSTRAINT ACCERTAMENTO_CANCELLAZION_FK5 
  FOREIGN KEY (ID_LOCALITA) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE,
  CONSTRAINT ACCERTAMENTO_CANCELLAZION_FK6 
  FOREIGN KEY (ID_STATO_ESTERO) 
  REFERENCES ANAG_USR.CONF_STATO_ESTERO (ID_STATO_ESTERO)
  ENABLE VALIDATE,
  CONSTRAINT ACCERTAMENTO_CANCELLAZION_FK7 
  FOREIGN KEY (ID_COMUNE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT ACCERTAMENTO_CANCELLAZION_FK8 
  FOREIGN KEY (TIPO_PROTOCOLLO_VIGILE) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_INDIVIDUAZIONE_COM_AIRE
(
  ID_INDIVIDUAZIONE  NUMBER                     NOT NULL,
  DESCRIZIONE        VARCHAR2(150 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_INDIVIDUAZIONE_COM_AIRE.ID_INDIVIDUAZIONE IS 'Identificativo dell''individuazione del comune AIRE';

COMMENT ON COLUMN ANAG_USR.CONF_INDIVIDUAZIONE_COM_AIRE.DESCRIZIONE IS 'Descrizione dell''individuazione del comune AIRE';



CREATE UNIQUE INDEX ANAG_USR.CONF_INDIVIDUAZIONE_COM_AI_PK ON ANAG_USR.CONF_INDIVIDUAZIONE_COM_AIRE
(ID_INDIVIDUAZIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_INDIVIDUAZIONE_COM_AIRE ADD (
  CONSTRAINT CONF_INDIVIDUAZIONE_COM_AI_PK
  PRIMARY KEY
  (ID_INDIVIDUAZIONE)
  USING INDEX ANAG_USR.CONF_INDIVIDUAZIONE_COM_AI_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.VARIAZIONE
(
  ID_VARIAZIONE            NUMBER               NOT NULL,
  ID_CONF_TIPO_VARIAZIONE  NUMBER,
  DATA_VARIAZIONE          DATE,
  ID_SOGGETTO_STORICO      NUMBER,
  MOTIVAZIONE              VARCHAR2(4000 BYTE),
  ID_UTENTE                NUMBER,
  ID_ORGANIZZAZIONE        NUMBER,
  ID_SEDE_MUNICIPIO        NUMBER,
  DATA_DEC_VARIAZIONE      DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.VARIAZIONE.ID_VARIAZIONE IS 'Campo che identifica in modo univoco la variazione';

COMMENT ON COLUMN ANAG_USR.VARIAZIONE.ID_CONF_TIPO_VARIAZIONE IS 'Campo che identifica il tipo di variazione.';

COMMENT ON COLUMN ANAG_USR.VARIAZIONE.DATA_VARIAZIONE IS 'Data della variazione.';

COMMENT ON COLUMN ANAG_USR.VARIAZIONE.ID_SOGGETTO_STORICO IS 'Campo che identifica l''id del soggetto nello storico';

COMMENT ON COLUMN ANAG_USR.VARIAZIONE.MOTIVAZIONE IS 'Campo che indica la motivazione della variazione';

COMMENT ON COLUMN ANAG_USR.VARIAZIONE.ID_UTENTE IS 'Identificativo dell''utente';

COMMENT ON COLUMN ANAG_USR.VARIAZIONE.ID_ORGANIZZAZIONE IS 'Rappresenta l''unità organizzativa di cui l''utente fa parte';

COMMENT ON COLUMN ANAG_USR.VARIAZIONE.ID_SEDE_MUNICIPIO IS 'Rappresenta l''unità organizzativa di cui l''utente fa parte';

COMMENT ON COLUMN ANAG_USR.VARIAZIONE.DATA_DEC_VARIAZIONE IS 'Data decorrenza della variazione';



CREATE UNIQUE INDEX ANAG_USR.VARIAZINE_PK ON ANAG_USR.VARIAZIONE
(ID_VARIAZIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.VARIAZIONE ADD (
  CONSTRAINT VARIAZINE_PK
  PRIMARY KEY
  (ID_VARIAZIONE)
  USING INDEX ANAG_USR.VARIAZINE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.VARIAZIONE ADD (
  CONSTRAINT CONF_SEDE_MUNICIPIO_FK 
  FOREIGN KEY (ID_SEDE_MUNICIPIO) 
  REFERENCES ANAG_USR.CONF_SEDE_MUNICIPIO (ID_SEDE_MUNICIPIO)
  ENABLE VALIDATE,
  CONSTRAINT CONF_TIPO_VARIAZIONE_FK1 
  FOREIGN KEY (ID_CONF_TIPO_VARIAZIONE) 
  REFERENCES ANAG_USR.CONF_TIPO_VARIAZIONE (ID_TIPO_VARIAZIONE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_QUESTURE
(
  ID_QUESTURA      NUMBER                       NOT NULL,
  DESCRIZIONE      VARCHAR2(100 BYTE)           NOT NULL,
  CODICE_QUESTURA  VARCHAR2(5 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_QUESTURE.ID_QUESTURA IS 'Identificativo della questura';

COMMENT ON COLUMN ANAG_USR.CONF_QUESTURE.DESCRIZIONE IS 'Descrizione della questura';

COMMENT ON COLUMN ANAG_USR.CONF_QUESTURE.CODICE_QUESTURA IS 'Codice della Questura';



CREATE UNIQUE INDEX ANAG_USR.CONF_QUESTURE_PK ON ANAG_USR.CONF_QUESTURE
(ID_QUESTURA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_QUESTURE ADD (
  CONSTRAINT CONF_QUESTURE_PK
  PRIMARY KEY
  (ID_QUESTURA)
  USING INDEX ANAG_USR.CONF_QUESTURE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.ELENCO_PREPARATORIO_LEVA
(
  ID_ELENCO_PREPARATORIO  NUMBER                NOT NULL,
  DATA_CREAZIONE          DATE,
  STATO_ELENCO            CHAR(1 BYTE),
  ANNO_PRATICA            INTEGER,
  NUMERO_PRATICA          NUMBER,
  CLASSE_LEVA             NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.ELENCO_PREPARATORIO_LEVA.ID_ELENCO_PREPARATORIO IS 'identificativo dell'' elenco preparatorio di leva';

COMMENT ON COLUMN ANAG_USR.ELENCO_PREPARATORIO_LEVA.DATA_CREAZIONE IS 'data di creazione dell''elenco';

COMMENT ON COLUMN ANAG_USR.ELENCO_PREPARATORIO_LEVA.STATO_ELENCO IS 'G -> GENERATO L -> LAVORATO';

COMMENT ON COLUMN ANAG_USR.ELENCO_PREPARATORIO_LEVA.ANNO_PRATICA IS 'anno pratica relativo all'''' elenco preparatorio';

COMMENT ON COLUMN ANAG_USR.ELENCO_PREPARATORIO_LEVA.NUMERO_PRATICA IS 'numero pratica relativo all''elenco preparatorio';

COMMENT ON COLUMN ANAG_USR.ELENCO_PREPARATORIO_LEVA.CLASSE_LEVA IS 'anno classe di leva di riferimento';



CREATE UNIQUE INDEX ANAG_USR.ELENCO_PREPARATORIO_LEVA_PK ON ANAG_USR.ELENCO_PREPARATORIO_LEVA
(ID_ELENCO_PREPARATORIO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.ELENCO_PREPARATORIO_LEVA ADD (
  CONSTRAINT ELENCO_PREPARATORIO_LEVA_PK
  PRIMARY KEY
  (ID_ELENCO_PREPARATORIO)
  USING INDEX ANAG_USR.ELENCO_PREPARATORIO_LEVA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.LISTE_LEVA
(
  ID_LISTA_LEVA      NUMBER                     NOT NULL,
  DATA_GENERAZIONE   DATE,
  DATA_CHIUSURA      DATE,
  NUMERO_PRATICA     NUMBER,
  ANNO_PRATICA       NUMBER,
  NUMERO_PROTOCOLLO  NUMBER,
  ANNO_PROTOCOLLO    NUMBER,
  STATO_ELENCO       CHAR(1 BYTE),
  CLASSE_LEVA        NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.LISTE_LEVA.DATA_GENERAZIONE IS 'data generazione lista di leva';

COMMENT ON COLUMN ANAG_USR.LISTE_LEVA.STATO_ELENCO IS 'G->Generato L->Lavorato';

COMMENT ON COLUMN ANAG_USR.LISTE_LEVA.CLASSE_LEVA IS 'anno classe di leva di riferimento';



CREATE UNIQUE INDEX ANAG_USR.LISTE_LEVA_PK ON ANAG_USR.LISTE_LEVA
(ID_LISTA_LEVA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.LISTE_LEVA ADD (
  CONSTRAINT LISTE_LEVA_PK
  PRIMARY KEY
  (ID_LISTA_LEVA)
  USING INDEX ANAG_USR.LISTE_LEVA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_CODICE_COMUNE
(
  PARTE_PRIMA    VARCHAR2(1 BYTE),
  PARTE_SECONDA  VARCHAR2(1 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;
CREATE TABLE ANAG_USR.CONF_MUNICIPIO
(
  ID_MUNICIPIO  NUMBER                          NOT NULL,
  DESCRIZIONE   VARCHAR2(20 BYTE)               NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_MUNICIPIO.ID_MUNICIPIO IS 'codice identificativo municipio';

COMMENT ON COLUMN ANAG_USR.CONF_MUNICIPIO.DESCRIZIONE IS 'descrizione del municipio
';



CREATE UNIQUE INDEX ANAG_USR.CONF_MUNICIPIO_PK ON ANAG_USR.CONF_MUNICIPIO
(ID_MUNICIPIO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CONF_MUNICIPIO FOR ANAG_USR.CONF_MUNICIPIO;


ALTER TABLE ANAG_USR.CONF_MUNICIPIO ADD (
  CONSTRAINT CONF_MUNICIPIO_PK
  PRIMARY KEY
  (ID_MUNICIPIO)
  USING INDEX ANAG_USR.CONF_MUNICIPIO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_VARIAZIONE
(
  ID_TIPO_VARIAZIONE  NUMBER                    NOT NULL,
  DESCRIZIONE         VARCHAR2(250 BYTE),
  FLAG_RICERCA        CHAR(1 BYTE),
  PAGINA_HTML         VARCHAR2(250 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_VARIAZIONE.ID_TIPO_VARIAZIONE IS 'identificativo del tipo di variazione';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_VARIAZIONE.DESCRIZIONE IS 'descrizione del tipo dio variazione';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_VARIAZIONE.FLAG_RICERCA IS 'S-> indica che la variazione passa da una ricerca, N-> indica che la variazione non ha bisogno di passare da una ricerca';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_VARIAZIONE.PAGINA_HTML IS 'indica la pagina html della variazione in cui si vuole andare ';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_VARIAZIONE_PK ON ANAG_USR.CONF_TIPO_VARIAZIONE
(ID_TIPO_VARIAZIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CONF_TIPO_VARIAZIONE_SIN FOR ANAG_USR.CONF_TIPO_VARIAZIONE;


ALTER TABLE ANAG_USR.CONF_TIPO_VARIAZIONE ADD (
  CONSTRAINT CONF_TIPO_VARIAZIONE_PK
  PRIMARY KEY
  (ID_TIPO_VARIAZIONE)
  USING INDEX ANAG_USR.CONF_TIPO_VARIAZIONE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_OSTATIVA
(
  ID_TIPO_OSTATIVA  NUMBER                      NOT NULL,
  DESCRIZIONE       VARCHAR2(250 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_OSTATIVA.ID_TIPO_OSTATIVA IS 'Identificativo del tipo di ostativa.';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_OSTATIVA.DESCRIZIONE IS 'Descrizione del tipo di ostativa';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_OSTATIVA_PK ON ANAG_USR.CONF_TIPO_OSTATIVA
(ID_TIPO_OSTATIVA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_OSTATIVA ADD (
  CONSTRAINT CONF_TIPO_OSTATIVA_PK
  PRIMARY KEY
  (ID_TIPO_OSTATIVA)
  USING INDEX ANAG_USR.CONF_TIPO_OSTATIVA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.OPERAZIONE_ANPR
(
  ID_OPERAZIONE_ANPR      NUMBER,
  TIPO_OPERAZIONE_ANPR    VARCHAR2(20 BYTE),
  DATA_OPERAZIONE_ANPR    DATE,
  MOTIVO_OPERAZIONE_ANPR  VARCHAR2(250 BYTE),
  ID_OPERAZIONE_COMUNE    VARCHAR2(200 BYTE),
  NOTE                    VARCHAR2(100 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.OPERAZIONE_ANPR.ID_OPERAZIONE_ANPR IS 'Identificativo operazione ANPR';

COMMENT ON COLUMN ANAG_USR.OPERAZIONE_ANPR.TIPO_OPERAZIONE_ANPR IS 'Servizio utilizzato ';

COMMENT ON COLUMN ANAG_USR.OPERAZIONE_ANPR.DATA_OPERAZIONE_ANPR IS 'Data in cui il servizio è stato richiamato';

COMMENT ON COLUMN ANAG_USR.OPERAZIONE_ANPR.MOTIVO_OPERAZIONE_ANPR IS 'Descrizione servizio utilizzato';

COMMENT ON COLUMN ANAG_USR.OPERAZIONE_ANPR.ID_OPERAZIONE_COMUNE IS 'Identificativo operazione comune';

COMMENT ON COLUMN ANAG_USR.OPERAZIONE_ANPR.NOTE IS 'Campo per eventuali note sulle operazioni Anpr';



CREATE UNIQUE INDEX ANAG_USR.OPERAZIONI_ANPR_PK ON ANAG_USR.OPERAZIONE_ANPR
(ID_OPERAZIONE_ANPR)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.OPERAZIONE_ANPR ADD (
  CONSTRAINT OPERAZIONI_ANPR_PK
  PRIMARY KEY
  (ID_OPERAZIONE_ANPR)
  USING INDEX ANAG_USR.OPERAZIONI_ANPR_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_MUTAZIONE_FAMIGLIA
(
  ID_TIPO_MUTAZIONE_FAMIGLIA  VARCHAR2(1 BYTE)  NOT NULL,
  DESCRIZIONE                 VARCHAR2(90 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_MUTAZIONE_FAMIGL_PK ON ANAG_USR.CONF_TIPO_MUTAZIONE_FAMIGLIA
(ID_TIPO_MUTAZIONE_FAMIGLIA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_MUTAZIONE_FAMIGLIA ADD (
  CONSTRAINT CONF_TIPO_MUTAZIONE_FAMIGL_PK
  PRIMARY KEY
  (ID_TIPO_MUTAZIONE_FAMIGLIA)
  USING INDEX ANAG_USR.CONF_TIPO_MUTAZIONE_FAMIGL_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_ISCRIZIONE
(
  ID_TIPO_ISCRIZIONE  NUMBER                    NOT NULL,
  DESCRIZIONE         VARCHAR2(120 CHAR)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_ISCRIZIONE_PK ON ANAG_USR.CONF_TIPO_ISCRIZIONE
(ID_TIPO_ISCRIZIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_ISCRIZIONE ADD (
  CONSTRAINT CONF_TIPO_ISCRIZIONE_PK
  PRIMARY KEY
  (ID_TIPO_ISCRIZIONE)
  USING INDEX ANAG_USR.CONF_TIPO_ISCRIZIONE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CERTIFICAZIONE_SOSPESA
(
  ID_CERTIFICAZIONE_SOSPESA       NUMBER        NOT NULL,
  FLAG_CERTIFICAZIONE_NASCITA     CHAR(1 BYTE),
  FLAG_ESTRATTO_NASCITA           CHAR(1 BYTE),
  FLAG_CERTIFICAZIONE_MATRIMONIO  CHAR(1 BYTE),
  FLAG_ESTRATTO_MATRIMONIO        CHAR(1 BYTE),
  FLAG_CERTIFICAZIONE_MORTE       CHAR(1 BYTE),
  FLAG_ESTRATTO_MORTE             CHAR(1 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CERTIFICAZIONE_SOSPESA.ID_CERTIFICAZIONE_SOSPESA IS 'identificazione delle certificazioni sospese';

COMMENT ON COLUMN ANAG_USR.CERTIFICAZIONE_SOSPESA.FLAG_CERTIFICAZIONE_NASCITA IS 'Flag che identifica il blocco sblocco della certificazione : S -> sblocco, N -> blocco';

COMMENT ON COLUMN ANAG_USR.CERTIFICAZIONE_SOSPESA.FLAG_ESTRATTO_NASCITA IS 'Flag che identifica il blocco sblocco dell estratto : S -> sblocco, N -> blocco';

COMMENT ON COLUMN ANAG_USR.CERTIFICAZIONE_SOSPESA.FLAG_CERTIFICAZIONE_MATRIMONIO IS 'Flag che identifica il blocco sblocco della certificazione : S -> sblocco, N -> blocco';

COMMENT ON COLUMN ANAG_USR.CERTIFICAZIONE_SOSPESA.FLAG_ESTRATTO_MATRIMONIO IS 'Flag che identifica il blocco sblocco dell estratto : S -> sblocco, N -> blocco';

COMMENT ON COLUMN ANAG_USR.CERTIFICAZIONE_SOSPESA.FLAG_CERTIFICAZIONE_MORTE IS 'Flag che identifica il blocco sblocco della certificazione : S -> sblocco, N -> blocco';

COMMENT ON COLUMN ANAG_USR.CERTIFICAZIONE_SOSPESA.FLAG_ESTRATTO_MORTE IS 'Flag che identifica il blocco sblocco dell estratto : S -> sblocco, N -> blocco';



CREATE UNIQUE INDEX ANAG_USR.CERTIFICAZIONE_SOSPESA_PK ON ANAG_USR.CERTIFICAZIONE_SOSPESA
(ID_CERTIFICAZIONE_SOSPESA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CERTIFICAZIONE_SOSPESA ADD (
  CONSTRAINT CERTIFICAZIONE_SOSPESA_PK
  PRIMARY KEY
  (ID_CERTIFICAZIONE_SOSPESA)
  USING INDEX ANAG_USR.CERTIFICAZIONE_SOSPESA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_TIPO_ALLEGATI_PRATICA_CERT
(
  ID_R_TIPO_ALLEGATI_PRATICA    NUMBER          NOT NULL,
  ID_TIPO_ALLEGATO_CERTIFICATO  NUMBER          NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.R_TIPO_ALLEGATI_PRATICA_CERT.ID_R_TIPO_ALLEGATI_PRATICA IS 'identificativo della relazione tra una pratica di certificati e i tipo di allegati necessari per quella pratica';

COMMENT ON COLUMN ANAG_USR.R_TIPO_ALLEGATI_PRATICA_CERT.ID_TIPO_ALLEGATO_CERTIFICATO IS 'id del tipo allegato associato';



CREATE UNIQUE INDEX ANAG_USR.R_TIPO_ALLEGATO_PRATICA_PK ON ANAG_USR.R_TIPO_ALLEGATI_PRATICA_CERT
(ID_R_TIPO_ALLEGATI_PRATICA, ID_TIPO_ALLEGATO_CERTIFICATO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_TIPO_ALLEGATI_PRATICA_CERT ADD (
  CONSTRAINT R_TIPO_ALLEGATO_PRATICA_PK
  PRIMARY KEY
  (ID_R_TIPO_ALLEGATI_PRATICA, ID_TIPO_ALLEGATO_CERTIFICATO)
  USING INDEX ANAG_USR.R_TIPO_ALLEGATO_PRATICA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_TIPO_ALLEGATI_PRATICA_CERT ADD (
  CONSTRAINT R_TIPO_ALLEGATI_PRATICA_FK1 
  FOREIGN KEY (ID_TIPO_ALLEGATO_CERTIFICATO) 
  REFERENCES ANAG_USR.CONF_TIPO_ALLEGATO_CERTIFICATO (ID_TIPO_ALLEGATO_CERTIFICATO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.MV_MIGRA_COLL_SVIL
(
  ID_SOGGETTO  NUMBER                           NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;
CREATE TABLE ANAG_USR.PROVINCIA
(
  ID_PROVINCIA             NUMBER               NOT NULL,
  SIGLA_PROVINCIA          VARCHAR2(3 BYTE)     NOT NULL,
  DENOMINAZIONE_PROVINCIA  VARCHAR2(400 BYTE),
  REGIONE                  VARCHAR2(200 BYTE),
  FLG_ATTIVO               VARCHAR2(1 BYTE),
  ANNO_ISTITUZIONE         VARCHAR2(4 BYTE),
  ANNO_CESSAZIONE          VARCHAR2(4 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.PROVINCIA.ID_PROVINCIA IS 'Identificativo della provincia';

COMMENT ON COLUMN ANAG_USR.PROVINCIA.SIGLA_PROVINCIA IS 'Sigla della provincia';

COMMENT ON COLUMN ANAG_USR.PROVINCIA.DENOMINAZIONE_PROVINCIA IS 'Denominazione della provincia per esteso';

COMMENT ON COLUMN ANAG_USR.PROVINCIA.REGIONE IS 'Nome della regione di appartenenza';

COMMENT ON COLUMN ANAG_USR.PROVINCIA.FLG_ATTIVO IS 'S -> Attivo, N -> Non attivo';

COMMENT ON COLUMN ANAG_USR.PROVINCIA.ANNO_ISTITUZIONE IS 'Anno di istituzione';

COMMENT ON COLUMN ANAG_USR.PROVINCIA.ANNO_CESSAZIONE IS 'Anno di cessazione';



CREATE UNIQUE INDEX ANAG_USR.PROVINCIA_PK ON ANAG_USR.PROVINCIA
(ID_PROVINCIA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.PROVINCIA FOR ANAG_USR.PROVINCIA;


ALTER TABLE ANAG_USR.PROVINCIA ADD (
  CONSTRAINT PROVINCIA_PK
  PRIMARY KEY
  (ID_PROVINCIA)
  USING INDEX ANAG_USR.PROVINCIA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.RESPONSABILE_MINORE
(
  ID_RESPONSABILE       NUMBER                  NOT NULL,
  COGNOME_RESPONSABILE  VARCHAR2(80 BYTE),
  NOME_RESPONSABILE     VARCHAR2(80 BYTE),
  TIPO_RESPONSABILE     VARCHAR2(40 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.RESPONSABILE_MINORE_PK ON ANAG_USR.RESPONSABILE_MINORE
(ID_RESPONSABILE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.RESPONSABILE_MINORE ADD (
  CONSTRAINT RESPONSABILE_MINORE_PK
  PRIMARY KEY
  (ID_RESPONSABILE)
  USING INDEX ANAG_USR.RESPONSABILE_MINORE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_STATO_VALIDITA_CARTA
(
  ID_STATO_VALIDITA_CARTA        NUMBER         NOT NULL,
  DESCRIZIONE_STATO_VALIDITA_CA  VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_STATO_VALIDITA_CARTA.ID_STATO_VALIDITA_CARTA IS 'Identificativo dello stato della carta d''identità';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_VALIDITA_CARTA.DESCRIZIONE_STATO_VALIDITA_CA IS 'Descrizione dello stato di validità della carta d''identità';



CREATE UNIQUE INDEX ANAG_USR.CONF_STATO__PK ON ANAG_USR.CONF_STATO_VALIDITA_CARTA
(ID_STATO_VALIDITA_CARTA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_STATO_VALIDITA_CARTA ADD (
  CONSTRAINT CONF_STATO__PK
  PRIMARY KEY
  (ID_STATO_VALIDITA_CARTA)
  USING INDEX ANAG_USR.CONF_STATO__PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.RECAPITI
(
  ID_RECAPITO    NUMBER                         NOT NULL,
  VIA_PIAZZA     VARCHAR2(200 BYTE),
  NUMERO_CIVICO  VARCHAR2(20 BYTE),
  ID_COMUNE      NUMBER,
  TELEFONO       VARCHAR2(50 BYTE),
  EMAIL          VARCHAR2(100 BYTE),
  FAX            VARCHAR2(50 BYTE),
  CELLULARE      VARCHAR2(50 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.RECAPITI_PK ON ANAG_USR.RECAPITI
(ID_RECAPITO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.RECAPITI ADD (
  CONSTRAINT RECAPITI_PK
  PRIMARY KEY
  (ID_RECAPITO)
  USING INDEX ANAG_USR.RECAPITI_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.RECAPITI ADD (
  CONSTRAINT ID_COMUNE_FK 
  FOREIGN KEY (ID_COMUNE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.ESTREMI_CATASTALI
(
  ID_ESTREMI_CATASTALI  NUMBER                  NOT NULL,
  SEZIONE               VARCHAR2(10 BYTE),
  FOGLIO                VARCHAR2(10 BYTE),
  PARTICELLA_MAPPALE    VARCHAR2(10 BYTE),
  SUBALTERNO            VARCHAR2(10 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.ESTREMI_CATASTALI.ID_ESTREMI_CATASTALI IS 'Campo che identifica univocamente gli estremi catastali di un''abitazione';



CREATE UNIQUE INDEX ANAG_USR.ESTREMI_CATASTALI_PK ON ANAG_USR.ESTREMI_CATASTALI
(ID_ESTREMI_CATASTALI)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.ESTREMI_CATASTALI ADD (
  CONSTRAINT ESTREMI_CATASTALI_PK
  PRIMARY KEY
  (ID_ESTREMI_CATASTALI)
  USING INDEX ANAG_USR.ESTREMI_CATASTALI_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_POSIZIONI
(
  ID                NUMBER                      NOT NULL,
  COD_TIPO_OGGETTO  VARCHAR2(10 CHAR),
  COD_DESCRIZIONE   VARCHAR2(10 CHAR),
  TIPOLOGIA         VARCHAR2(200 CHAR),
  CAUSALE           VARCHAR2(200 CHAR),
  TIPO_POSIZIONE    CHAR(1 CHAR),
  AREA              NUMBER,
  CNC_RIEPILOGO     VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_POSIZIONI.ID IS 'Primary Key';

COMMENT ON COLUMN ANAG_USR.CONF_POSIZIONI.COD_TIPO_OGGETTO IS 'Codice rappresentante la macro tipologia della posizione. Utilizzato nel primo blocco <dettaglio> del XML crediti.xsd.';

COMMENT ON COLUMN ANAG_USR.CONF_POSIZIONI.COD_DESCRIZIONE IS 'Codice rappresentante la descrizione della posizione. Utilizzato nel secondo blocco <dettaglio> in posizione 1 del tag <descrizioneOggetto>.';

COMMENT ON COLUMN ANAG_USR.CONF_POSIZIONI.TIPOLOGIA IS 'Tipologia della posizione.';

COMMENT ON COLUMN ANAG_USR.CONF_POSIZIONI.CAUSALE IS 'Causale della posizione';

COMMENT ON COLUMN ANAG_USR.CONF_POSIZIONI.TIPO_POSIZIONE IS 'O - Ordinaria';



CREATE UNIQUE INDEX ANAG_USR.CONF_POSIZIONI_PK ON ANAG_USR.CONF_POSIZIONI
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_POSIZIONI ADD (
  CONSTRAINT CONF_POSIZIONI_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_POSIZIONI_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_CERTIFICATI_IMPORTI
(
  ID_CONF_CERTIFICATO  NUMBER                   NOT NULL,
  ID_POSIZIONE         NUMBER                   NOT NULL,
  ID                   NUMBER                   NOT NULL,
  FLG_BOLLATA          CHAR(1 BYTE),
  FLG_TIPO_RICHIESTA   NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_CERTIFICATI_IMPORTI.FLG_BOLLATA IS 'S->Carta Semplice B->Marca da Bollo V->Marca da bollo da applicare';

COMMENT ON COLUMN ANAG_USR.CONF_CERTIFICATI_IMPORTI.FLG_TIPO_RICHIESTA IS '1-> ONLINE , 2-> PER POSTA (CORRISPONDENZA), 3 -> SPORTELLO, 4 -> PRATICA ENTI ESTERNI';



CREATE UNIQUE INDEX ANAG_USR.CONF_CERTIFICATI_IMPORTI_PK ON ANAG_USR.CONF_CERTIFICATI_IMPORTI
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_CERTIFICATI_IMPORTI ADD (
  CONSTRAINT CONF_CERTIFICATI_IMPORTI_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_CERTIFICATI_IMPORTI_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONF_CERTIFICATI_IMPORTI ADD (
  CONSTRAINT CONF_CERTIFICATI_IMPORTI_FK1 
  FOREIGN KEY (ID_CONF_CERTIFICATO) 
  REFERENCES ANAG_USR.CONF_CERTIFICATO (ID_CONF_CERTIFICATO)
  ENABLE VALIDATE,
  CONSTRAINT CONF_CERTIFICATI_IMPORTI_FK2 
  FOREIGN KEY (ID_POSIZIONE) 
  REFERENCES ANAG_USR.CONF_POSIZIONI (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_CARTA_IDENTITA_IMPORTO
(
  ID               NUMBER                       NOT NULL,
  ID_POSIZIONE     NUMBER,
  NUMERO_CARTA     VARCHAR2(20 BYTE),
  IUV              VARCHAR2(200 BYTE),
  DATA_RICHIESTA   DATE,
  DATA_PAGAMENTO   DATE,
  OPE_RIC_IUV      VARCHAR2(200 BYTE),
  DATA_BOLLETTINO  DATE,
  OPE_BOLLETTINO   VARCHAR2(200 BYTE),
  OPE_PAGAMENTO    VARCHAR2(200 BYTE),
  XML_POSIZIONE    CLOB
)
LOB (XML_POSIZIONE) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.R_CARTA_IDENTITA_IMPORTO_PK ON ANAG_USR.R_CARTA_IDENTITA_IMPORTO
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_CARTA_IDENTITA_IMPORTO ADD (
  CONSTRAINT R_CARTA_IDENTITA_IMPORTO_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.R_CARTA_IDENTITA_IMPORTO_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_CARTA_IDENTITA_IMPORTO ADD (
  CONSTRAINT R_CARTA_IDENTITA_IMPORTO_FK1 
  FOREIGN KEY (ID_POSIZIONE) 
  REFERENCES ANAG_USR.CONF_POSIZIONI (ID)
  ENABLE VALIDATE,
  CONSTRAINT R_CARTA_IDENTITA_IMPORTO_FK2 
  FOREIGN KEY (NUMERO_CARTA) 
  REFERENCES ANAG_USR.CARTA_IDENTITA (NUMERO_CARTA_IDENTITA)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_CARTA_IDENTITA_IMPORTI
(
  ID                    NUMBER                  NOT NULL,
  TIPOLOGIA             CHAR(1 BYTE),
  ID_MODALITA_RILASCIO  NUMBER,
  ID_POSIZIONE          NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_CARTA_IDENTITA_IMPORTI.TIPOLOGIA IS '0-cartacea, 1-elettronica';



CREATE UNIQUE INDEX ANAG_USR.CONF_CARTA_IDENTITA_IMPORT_PK ON ANAG_USR.CONF_CARTA_IDENTITA_IMPORTI
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_CARTA_IDENTITA_IMPORTI ADD (
  CONSTRAINT CONF_CARTA_IDENTITA_IMPORT_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_CARTA_IDENTITA_IMPORT_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONF_CARTA_IDENTITA_IMPORTI ADD (
  CONSTRAINT CONF_CARTA_IDENTITA_IMPOR_FK1 
  FOREIGN KEY (ID_POSIZIONE) 
  REFERENCES ANAG_USR.CONF_POSIZIONI (ID)
  ENABLE VALIDATE,
  CONSTRAINT CONF_CARTA_IDENTITA_IMPOR_FK2 
  FOREIGN KEY (ID_MODALITA_RILASCIO) 
  REFERENCES ANAG_USR.CONF_MODALITA_RILASCIO_CI (ID_CONF_MODALITA_RILASCIO_CI)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_DISATTIVAZIONE_SOGGETTO
(
  ID_DISATTIVAZIONE_SOGGETTO  NUMBER            NOT NULL,
  DESCRIZIONE                 VARCHAR2(80 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_DISATTIVAZIONE_SOGGET_PK ON ANAG_USR.CONF_DISATTIVAZIONE_SOGGETTO
(ID_DISATTIVAZIONE_SOGGETTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_DISATTIVAZIONE_SOGGETTO ADD (
  CONSTRAINT CONF_DISATTIVAZIONE_SOGGET_PK
  PRIMARY KEY
  (ID_DISATTIVAZIONE_SOGGETTO)
  USING INDEX ANAG_USR.CONF_DISATTIVAZIONE_SOGGET_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_STATUS_SOGGETTO
(
  ID_STATUS_SOGGETTO  NUMBER                    NOT NULL,
  DESCRIZIONE         VARCHAR2(50 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_STATUS_SOGGETTO_PK ON ANAG_USR.CONF_STATUS_SOGGETTO
(ID_STATUS_SOGGETTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CONF_STATUS_SOGGETTO FOR ANAG_USR.CONF_STATUS_SOGGETTO;


ALTER TABLE ANAG_USR.CONF_STATUS_SOGGETTO ADD (
  CONSTRAINT CONF_STATUS_SOGGETTO_PK
  PRIMARY KEY
  (ID_STATUS_SOGGETTO)
  USING INDEX ANAG_USR.CONF_STATUS_SOGGETTO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.RECAPITO_RETTIFICA_ANPR
(
  ID_RECAPITO_ONLINE  NUMBER                    NOT NULL,
  EMAIL               VARCHAR2(100 BYTE),
  PEC                 VARCHAR2(100 BYTE),
  TELEFONO            VARCHAR2(50 BYTE),
  CELLULARE           VARCHAR2(50 BYTE),
  DOMICILIO_DIGITALE  VARCHAR2(100 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.RECAPITO_RETTIFICA_ANPR_PK ON ANAG_USR.RECAPITO_RETTIFICA_ANPR
(ID_RECAPITO_ONLINE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.RECAPITO_RETTIFICA_ANPR ADD (
  CONSTRAINT RECAPITO_RETTIFICA_ANPR_PK
  PRIMARY KEY
  (ID_RECAPITO_ONLINE)
  USING INDEX ANAG_USR.RECAPITO_RETTIFICA_ANPR_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_ALLEGATO_ANPR
(
  ID_TIPO_ALLEGATO_ANPR  NUMBER                 NOT NULL,
  DESCRIZIONE            VARCHAR2(50 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_ALLEGATO_ANPR_PK ON ANAG_USR.CONF_TIPO_ALLEGATO_ANPR
(ID_TIPO_ALLEGATO_ANPR)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_ALLEGATO_ANPR ADD (
  CONSTRAINT CONF_TIPO_ALLEGATO_ANPR_PK
  PRIMARY KEY
  (ID_TIPO_ALLEGATO_ANPR)
  USING INDEX ANAG_USR.CONF_TIPO_ALLEGATO_ANPR_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_FORMATO_ALLEGATO_ANPR
(
  ID_FORMATO_ALLEGATO  NUMBER                   NOT NULL,
  DESCRIZIONE          VARCHAR2(50 BYTE),
  ESTENSIONE           VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_FORMATO_ALLEGATO_ANPR_PK ON ANAG_USR.CONF_FORMATO_ALLEGATO_ANPR
(ID_FORMATO_ALLEGATO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_FORMATO_ALLEGATO_ANPR ADD (
  CONSTRAINT CONF_FORMATO_ALLEGATO_ANPR_PK
  PRIMARY KEY
  (ID_FORMATO_ALLEGATO)
  USING INDEX ANAG_USR.CONF_FORMATO_ALLEGATO_ANPR_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.ALLEGATO_CRI_ANPR
(
  ID_ALLEGATO          NUMBER                   NOT NULL,
  ID_CRI_ONLINE        NUMBER,
  NOME_FILE            VARCHAR2(100 BYTE),
  DOCUMENTO            BLOB,
  ID_FORMATO_ALLEGATO  NUMBER,
  ID_TIPO_ALLEGATO     NUMBER,
  FLG_INTEGRATA        VARCHAR2(1 BYTE)
)
LOB (DOCUMENTO) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.ALLEGATO_CRI_ANPR.FLG_INTEGRATA IS '0 -> No, 1 -> Sì';



CREATE UNIQUE INDEX ANAG_USR.ALLEGATO_CRI_ANPR_PK ON ANAG_USR.ALLEGATO_CRI_ANPR
(ID_ALLEGATO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.ALLEGATO_CRI_ANPR ADD (
  CONSTRAINT ALLEGATO_CRI_ANPR_PK
  PRIMARY KEY
  (ID_ALLEGATO)
  USING INDEX ANAG_USR.ALLEGATO_CRI_ANPR_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.ALLEGATO_CRI_ANPR ADD (
  CONSTRAINT ID_CRI_ONLINE_FK1 
  FOREIGN KEY (ID_CRI_ONLINE) 
  REFERENCES ANAG_USR.CAMBIO_RESIDENZA_ONLINE (ID_CAMBIO_RESIDENZA_ONLINE)
  ENABLE VALIDATE,
  CONSTRAINT ID_FORMATO_ALLEGATO_FK1 
  FOREIGN KEY (ID_FORMATO_ALLEGATO) 
  REFERENCES ANAG_USR.CONF_FORMATO_ALLEGATO_ANPR (ID_FORMATO_ALLEGATO)
  ENABLE VALIDATE,
  CONSTRAINT ID_TIPO_ALLEGATO_FK1 
  FOREIGN KEY (ID_TIPO_ALLEGATO) 
  REFERENCES ANAG_USR.CONF_TIPO_ALLEGATO_ANPR (ID_TIPO_ALLEGATO_ANPR)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.ALLEGATO_RETTIFICA_ANPR
(
  ID_ALLEGATO          NUMBER                   NOT NULL,
  ID_RETTIFICA         NUMBER,
  NOME_FILE            VARCHAR2(100 BYTE),
  DOCUMENTO            BLOB,
  ID_FORMATO_ALLEGATO  NUMBER,
  ID_TIPO_ALLEGATO     NUMBER,
  FLG_INTEGRATA        VARCHAR2(1 BYTE)
)
LOB (DOCUMENTO) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.ALLEGATO_RETTIFICA_ANPR_PK ON ANAG_USR.ALLEGATO_RETTIFICA_ANPR
(ID_ALLEGATO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.ALLEGATO_RETTIFICA_ANPR ADD (
  CONSTRAINT ALLEGATO_RETTIFICA_ANPR_PK
  PRIMARY KEY
  (ID_ALLEGATO)
  USING INDEX ANAG_USR.ALLEGATO_RETTIFICA_ANPR_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.ALLEGATO_RETTIFICA_ANPR ADD (
  CONSTRAINT ALLEGATO_RETTIFICA_ANPR_FK1 
  FOREIGN KEY (ID_TIPO_ALLEGATO) 
  REFERENCES ANAG_USR.CONF_TIPO_ALLEGATO_ANPR (ID_TIPO_ALLEGATO_ANPR)
  ENABLE VALIDATE,
  CONSTRAINT ALLEGATO_RETTIFICA_ANPR_FK2 
  FOREIGN KEY (ID_FORMATO_ALLEGATO) 
  REFERENCES ANAG_USR.CONF_FORMATO_ALLEGATO_ANPR (ID_FORMATO_ALLEGATO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.GESTIONE_SEGNALAZIONE
(
  ID                NUMBER                      NOT NULL,
  DESCRIZIONE       VARCHAR2(500 BYTE),
  ID_AREA_TEMATICA  NUMBER,
  FLAG_ATTIVO       VARCHAR2(1 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.GESTIONE_SEGNALAZIONE.ID IS 'Identificativo primario di tabella';

COMMENT ON COLUMN ANAG_USR.GESTIONE_SEGNALAZIONE.DESCRIZIONE IS 'Descrizione segnalazione';

COMMENT ON COLUMN ANAG_USR.GESTIONE_SEGNALAZIONE.ID_AREA_TEMATICA IS 'Identificativo dell''area tematica';

COMMENT ON COLUMN ANAG_USR.GESTIONE_SEGNALAZIONE.FLAG_ATTIVO IS 'S -> Attivo, N -> Non attivo';



CREATE UNIQUE INDEX ANAG_USR.AREA_SEGNALAZIONE_PK ON ANAG_USR.GESTIONE_SEGNALAZIONE
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.GESTIONE_SEGNALAZIONE ADD (
  CONSTRAINT AREA_SEGNALAZIONE_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.AREA_SEGNALAZIONE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.AREA_TEMATICA_SEGNALAZIONE
(
  ID             NUMBER                         NOT NULL,
  DESCRIZIONE    VARCHAR2(200 BYTE),
  ID_MACRO_AREA  NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.AREA_TEMATICA_SEGNALAZIONE.ID IS 'Identificativo di tabella';

COMMENT ON COLUMN ANAG_USR.AREA_TEMATICA_SEGNALAZIONE.DESCRIZIONE IS 'Descrizione area tematica';

COMMENT ON COLUMN ANAG_USR.AREA_TEMATICA_SEGNALAZIONE.ID_MACRO_AREA IS '0 -> Anagrafe, 1 -> Stato Civile,
2 -> Elettorale';



CREATE UNIQUE INDEX ANAG_USR.AREA_SEGNALAZIONE_PK1 ON ANAG_USR.AREA_TEMATICA_SEGNALAZIONE
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.AREA_TEMATICA_SEGNALAZIONE ADD (
  CONSTRAINT AREA_TEM_SEGNALAZIONE_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.AREA_SEGNALAZIONE_PK1
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_INDIRIZZO
(
  ID_TIPO_INDIRIZZO  NUMBER                     NOT NULL,
  DESCRIZIONE        VARCHAR2(50 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_INDIRIZZO_PK ON ANAG_USR.CONF_TIPO_INDIRIZZO
(ID_TIPO_INDIRIZZO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_INDIRIZZO ADD (
  CONSTRAINT CONF_TIPO_INDIRIZZO_PK
  PRIMARY KEY
  (ID_TIPO_INDIRIZZO)
  USING INDEX ANAG_USR.CONF_TIPO_INDIRIZZO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_SOGGETTO_OSTATIVA
(
  ID_SOGGETTO  NUMBER                           NOT NULL,
  ID_OSTATIVA  NUMBER                           NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_OSTATIVA.ID_SOGGETTO IS 'Campo che identifica il soggetto';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_OSTATIVA.ID_OSTATIVA IS 'Campo che identifica l''ostativa';



CREATE UNIQUE INDEX ANAG_USR.R_SOGGETTO_OSTATIVA_PK ON ANAG_USR.R_SOGGETTO_OSTATIVA
(ID_SOGGETTO, ID_OSTATIVA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.UK_G4Y39IU4W9D0DG4F5HSMTGUDE ON ANAG_USR.R_SOGGETTO_OSTATIVA
(ID_OSTATIVA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.R_SOGGETTO_OSTATIVA FOR ANAG_USR.R_SOGGETTO_OSTATIVA;


ALTER TABLE ANAG_USR.R_SOGGETTO_OSTATIVA ADD (
  CONSTRAINT R_SOGGETTO_OSTATIVA_PK
  PRIMARY KEY
  (ID_SOGGETTO, ID_OSTATIVA)
  USING INDEX ANAG_USR.R_SOGGETTO_OSTATIVA_PK
  ENABLE VALIDATE,
  CONSTRAINT UK_G4Y39IU4W9D0DG4F5HSMTGUDE
  UNIQUE (ID_OSTATIVA)
  USING INDEX ANAG_USR.UK_G4Y39IU4W9D0DG4F5HSMTGUDE
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_SOGGETTO_OSTATIVA ADD (
  CONSTRAINT ID_OSTATIVA_FK1 
  FOREIGN KEY (ID_OSTATIVA) 
  REFERENCES ANAG_USR.OSTATIVA (ID_OSTATIVA)
  ENABLE VALIDATE,
  CONSTRAINT ID_SOGGETTO_FK1 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_ALLEGATO_CERTIFICATO
(
  ID_TIPO_ALLEGATO_CERTIFICATO  NUMBER          NOT NULL,
  DESCRIZIONE                   VARCHAR2(70 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_ALLEGATO_CERTIFICATO.ID_TIPO_ALLEGATO_CERTIFICATO IS 'identificativo del tipo allegato certificato';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_ALLEGATO_CERTIFICATO.DESCRIZIONE IS 'descrizione del tipo allegato certificato';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_ALLEGATO_PK ON ANAG_USR.CONF_TIPO_ALLEGATO_CERTIFICATO
(ID_TIPO_ALLEGATO_CERTIFICATO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_ALLEGATO_CERTIFICATO ADD (
  CONSTRAINT CONF_TIPO_ALLEGATO_PK
  PRIMARY KEY
  (ID_TIPO_ALLEGATO_CERTIFICATO)
  USING INDEX ANAG_USR.CONF_TIPO_ALLEGATO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_ESITO_LEVA
(
  ID_ESITO              NUMBER                  NOT NULL,
  DESCRIZIONE           VARCHAR2(20 BYTE),
  DESCRIZIONE_COMPLETA  VARCHAR2(400 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_ESITO_LEVA.DESCRIZIONE IS 'esito di leva';



CREATE UNIQUE INDEX ANAG_USR.CONF_ESITO_LEVA_PK ON ANAG_USR.CONF_ESITO_LEVA
(ID_ESITO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_ESITO_LEVA ADD (
  CONSTRAINT CONF_ESITO_LEVA_PK
  PRIMARY KEY
  (ID_ESITO)
  USING INDEX ANAG_USR.CONF_ESITO_LEVA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_DISTRETTI_MILITARI
(
  ID_DISTRETTO  NUMBER                          NOT NULL,
  DESCRIZIONE   VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_DISTRETTI_MILITARI_PK ON ANAG_USR.CONF_DISTRETTI_MILITARI
(ID_DISTRETTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_DISTRETTI_MILITARI ADD (
  CONSTRAINT CONF_DISTRETTI_MILITARI_PK
  PRIMARY KEY
  (ID_DISTRETTO)
  USING INDEX ANAG_USR.CONF_DISTRETTI_MILITARI_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_ATTESTATO_IMPORTO
(
  ID               NUMBER                       NOT NULL,
  ID_POSIZIONE     NUMBER,
  ID_SOGGETTO      NUMBER,
  IUV              VARCHAR2(200 BYTE),
  DATA_RICHIESTA   DATE,
  DATA_PAGAMENTO   DATE,
  OPE_RIC_IUV      VARCHAR2(200 BYTE),
  DATA_BOLLETTINO  DATE,
  OPE_BOLLETTINO   VARCHAR2(200 BYTE),
  OPE_PAGAMENTO    VARCHAR2(200 BYTE),
  XML_POSIZIONE    CLOB,
  STORICO          NUMBER
)
LOB (XML_POSIZIONE) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.R_ATTESTATO_IMPORTO_PK ON ANAG_USR.R_ATTESTATO_IMPORTO
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_ATTESTATO_IMPORTO ADD (
  CONSTRAINT R_ATTESTATO_IMPORTO_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.R_ATTESTATO_IMPORTO_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_ATTESTATO_IMPORTO ADD (
  CONSTRAINT R_ATTESTATO_IMPORTO_FK1 
  FOREIGN KEY (ID_POSIZIONE) 
  REFERENCES ANAG_USR.CONF_POSIZIONI (ID)
  ENABLE VALIDATE,
  CONSTRAINT R_ATTESTATO_IMPORTO_FK2 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.LISTE_AIRE
(
  ID_LISTE_AIRE               NUMBER            NOT NULL,
  ID_SOGGETTO                 NUMBER,
  EMAIL                       CHAR(1 BYTE),
  TIPO_LISTA                  CHAR(1 BYTE),
  DATA_SCARTO_CENTENARIO      DATE,
  DATA_ENTRATA_CANCELLANDI    DATE,
  DATA_CANCELLAZIONE          DATE,
  DATA_RIPRISTINO_CENTENARIO  DATE,
  NUMERO_LISTA_CANCELLATI     NUMBER,
  DATA_INVIO_EMAIL            DATE,
  NUMERO_PROTOCOLLO           NUMBER,
  ANNO_PROTOCOLLO             NUMBER,
  TIPO_PROTOCOLLO             VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.LISTE_AIRE.ID_LISTE_AIRE IS 'Identificativo delle liste aire';

COMMENT ON COLUMN ANAG_USR.LISTE_AIRE.ID_SOGGETTO IS 'Identificativo del soggetto';

COMMENT ON COLUMN ANAG_USR.LISTE_AIRE.EMAIL IS '1- Inviata, 2- Risposta Positiva, 3- Risposta Negativa';

COMMENT ON COLUMN ANAG_USR.LISTE_AIRE.TIPO_LISTA IS '1- Centenario, 2- Cancellando, 3- Cancellato, 4- Scartato';

COMMENT ON COLUMN ANAG_USR.LISTE_AIRE.DATA_SCARTO_CENTENARIO IS 'Data di scarto del centenario';

COMMENT ON COLUMN ANAG_USR.LISTE_AIRE.DATA_ENTRATA_CANCELLANDI IS 'Data di entrata nei cancellandi';

COMMENT ON COLUMN ANAG_USR.LISTE_AIRE.DATA_CANCELLAZIONE IS 'Data di cancellazione';

COMMENT ON COLUMN ANAG_USR.LISTE_AIRE.DATA_RIPRISTINO_CENTENARIO IS 'Data di ripristino del centenario';

COMMENT ON COLUMN ANAG_USR.LISTE_AIRE.NUMERO_LISTA_CANCELLATI IS 'Numero identificativo della lista di cancellati';

COMMENT ON COLUMN ANAG_USR.LISTE_AIRE.DATA_INVIO_EMAIL IS 'Data di invio email';

COMMENT ON COLUMN ANAG_USR.LISTE_AIRE.TIPO_PROTOCOLLO IS 'ID CONF_TIPO_PROTOCOLLO';



CREATE UNIQUE INDEX ANAG_USR.LISTE_AIRE_PK ON ANAG_USR.LISTE_AIRE
(ID_LISTE_AIRE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.LISTE_AIRE ADD (
  CONSTRAINT LISTE_AIRE_PK
  PRIMARY KEY
  (ID_LISTE_AIRE)
  USING INDEX ANAG_USR.LISTE_AIRE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.LISTE_AIRE ADD (
  CONSTRAINT ID_SOGGETTO_CENT_FK 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT TIPO_PROTOCOLLO_FK 
  FOREIGN KEY (TIPO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.ELENCO_IRREPERIBILITA
(
  ID_ELENCO_IRREPERIBILITA  NUMBER              NOT NULL,
  TIPO_ELENCO               CHAR(1 BYTE),
  DATA_GENERAZIONE          DATE,
  DATA_PUBBLICAZIONE        DATE,
  STATO_ELENCO              CHAR(1 BYTE),
  NUMERO_PERSONE            NUMBER,
  DATA_CANCELLAZIONE        DATE,
  ANNO_PROTOCOLLO           NUMBER,
  NUMERO_PROTOCOLLO         NUMBER,
  CODICE_TIPO_PROTOCOLLO    VARCHAR2(10 BYTE),
  ID_MUNICIPIO              NUMBER,
  PDF_DOCUMENTO             BLOB,
  NOME_DOCUMENTO            VARCHAR2(50 BYTE),
  NUMERO_ALLEGATO           NUMBER
)
LOB (PDF_DOCUMENTO) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.ELENCO_IRREPERIBILITA.ID_ELENCO_IRREPERIBILITA IS 'Identificativo dell''elenco.';

COMMENT ON COLUMN ANAG_USR.ELENCO_IRREPERIBILITA.TIPO_ELENCO IS 'A-> Elenco avvio procedimento, C -> elenco cancellati.';

COMMENT ON COLUMN ANAG_USR.ELENCO_IRREPERIBILITA.DATA_GENERAZIONE IS 'Campo che identifica la data di generazione di un elenco.';

COMMENT ON COLUMN ANAG_USR.ELENCO_IRREPERIBILITA.DATA_PUBBLICAZIONE IS 'Campo che identifica la data di pubblicazione di un elenco.';

COMMENT ON COLUMN ANAG_USR.ELENCO_IRREPERIBILITA.STATO_ELENCO IS 'P -> pubblicato, C-> Lavorato,   I-> Generato';

COMMENT ON COLUMN ANAG_USR.ELENCO_IRREPERIBILITA.NUMERO_PERSONE IS 'Campo che identifica il numero delle persone presenti nell''elenco';

COMMENT ON COLUMN ANAG_USR.ELENCO_IRREPERIBILITA.DATA_CANCELLAZIONE IS 'Campo che identifica la data di cancellazione di un elenco.';

COMMENT ON COLUMN ANAG_USR.ELENCO_IRREPERIBILITA.ID_MUNICIPIO IS 'Campo che identifica il municipio che ha creato l''elenco';

COMMENT ON COLUMN ANAG_USR.ELENCO_IRREPERIBILITA.PDF_DOCUMENTO IS 'Blob del documento generato';



CREATE UNIQUE INDEX ANAG_USR.ELENCO_IRREPERIBILITA_PK ON ANAG_USR.ELENCO_IRREPERIBILITA
(ID_ELENCO_IRREPERIBILITA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.ELENCO_IRREPERIBILITA ADD (
  CONSTRAINT ELENCO_IRREPERIBILITA_PK
  PRIMARY KEY
  (ID_ELENCO_IRREPERIBILITA)
  USING INDEX ANAG_USR.ELENCO_IRREPERIBILITA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.ELENCO_IRREPERIBILITA ADD (
  CONSTRAINT FK92BRJHAPERDWB4QRLT0GYARXD 
  FOREIGN KEY (CODICE_TIPO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE,
  CONSTRAINT ID_MUNICIPIO_FK 
  FOREIGN KEY (ID_MUNICIPIO) 
  REFERENCES ANAG_USR.CONF_STRUTTURE_INTERNE_RC (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CAMBIO_RESIDENZA_EMIGRAZIONE
(
  ID_CAMBIO_RESIDENZA_EMIGR     NUMBER          NOT NULL,
  CONTEGGIO                     VARCHAR2(1 BYTE),
  TIPO_ISTANZA                  VARCHAR2(1 BYTE),
  DATA_EMIGRAZIONE              DATE,
  DATA_AGGIORNAMENTO            DATE,
  ID_FAMIGLIA_CONVIVENZA        NUMBER,
  NOTE                          VARCHAR2(4000 BYTE),
  ID_STATO_PRATICA              NUMBER,
  ID_RESIDENZA_ATTUALE          NUMBER,
  ID_RESIDENZA_EMIGRAZIONE      NUMBER,
  NUMERO_PRATICA                NUMBER,
  DATA_PRATICA                  DATE,
  NUMERO_PROTOCOLLO             NUMBER,
  ANNO_PROTOCOLLO               NUMBER,
  CODICE_TIPO_PROTOCOLLO        VARCHAR2(10 BYTE),
  MODELLO_APR4                  BLOB,
  ID_STATO_EMIGRAZIONE          NUMBER,
  FLAG_CANCELLAZIONE_ABBANDONO  CHAR(1 BYTE),
  NOME_ALLEGATO_APR4            VARCHAR2(80 BYTE),
  MODELLO_APR4_NEG              BLOB,
  NOME_ALLEGATO_APR4_NEG        VARCHAR2(80 BYTE),
  ID_MOTIVO_COMUNICAZIONE       NUMBER,
  NUMERO_PRATICA_INTERNO        NUMBER,
  ANNO_PRATICA_INTERNO          NUMBER(4),
  NUMERO_PRATICA_CRE            NUMBER,
  DATA_CREAZIONE_PRATICA_CRE    DATE,
  FLAG_AIRE                     VARCHAR2(1 BYTE)
)
LOB (MODELLO_APR4) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
LOB (MODELLO_APR4_NEG) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_EMIGRAZIONE.ID_RESIDENZA_ATTUALE IS 'residenza prima dell''emigrazione';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_EMIGRAZIONE.ID_RESIDENZA_EMIGRAZIONE IS 'residenza di emigrazione';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_EMIGRAZIONE.NOME_ALLEGATO_APR4 IS 'Campo che indica il nome del modello apr4 caricato.';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_EMIGRAZIONE.MODELLO_APR4_NEG IS 'campo che contiene il modello Apr4 nel caso in cui la pratica è stata lavorata negativamente';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_EMIGRAZIONE.NOME_ALLEGATO_APR4_NEG IS 'campo che contiene il nome del file nel caso in cui la pratica è stata lavorata negativamente';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_EMIGRAZIONE.NUMERO_PRATICA_INTERNO IS 'Numero pratica per integrazione Aggior. Aggiornato con la seq NUM_PRATICA_INT_CRE_SEQ';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_EMIGRAZIONE.ANNO_PRATICA_INTERNO IS 'Anno pratica per integrazione Aggior. Anno in cui viene aperta la pratica';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_EMIGRAZIONE.FLAG_AIRE IS 'Campo che identifica se è un''emigrazione o una cancellazione per trasferimento in altra AIRE';



CREATE UNIQUE INDEX ANAG_USR.CAMBIO_RESIDENZA_EMIGRAZIO_PK ON ANAG_USR.CAMBIO_RESIDENZA_EMIGRAZIONE
(ID_CAMBIO_RESIDENZA_EMIGR)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CAMBIO_RESIDENZA_EMIGRAZIONE FOR ANAG_USR.CAMBIO_RESIDENZA_EMIGRAZIONE;


ALTER TABLE ANAG_USR.CAMBIO_RESIDENZA_EMIGRAZIONE ADD (
  CONSTRAINT CAMBIO_RESIDENZA_EMIGRAZIO_PK
  PRIMARY KEY
  (ID_CAMBIO_RESIDENZA_EMIGR)
  USING INDEX ANAG_USR.CAMBIO_RESIDENZA_EMIGRAZIO_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CAMBIO_RESIDENZA_EMIGRAZIONE ADD (
  CONSTRAINT CAMBIO_RESIDENZA_EMIGRAZI_FK1 
  FOREIGN KEY (ID_FAMIGLIA_CONVIVENZA) 
  REFERENCES ANAG_USR.FAMIGLIA_CONVIVENZA (ID_FAMIGLIA_CONV)
  ENABLE VALIDATE,
  CONSTRAINT CAMBIO_RESIDENZA_EMIGRAZI_FK2 
  FOREIGN KEY (ID_STATO_PRATICA) 
  REFERENCES ANAG_USR.CONF_STATO_PRATICA (ID_STATO_PRATICA)
  ENABLE VALIDATE,
  CONSTRAINT CAMBIO_RESIDENZA_EMIGRAZI_FK3 
  FOREIGN KEY (ID_RESIDENZA_ATTUALE) 
  REFERENCES ANAG_USR.RESIDENZA (ID_RESIDENZA)
  ENABLE VALIDATE,
  CONSTRAINT CAMBIO_RESIDENZA_EMIGRAZI_FK4 
  FOREIGN KEY (ID_RESIDENZA_EMIGRAZIONE) 
  REFERENCES ANAG_USR.RESIDENZA (ID_RESIDENZA)
  ENABLE VALIDATE,
  CONSTRAINT CAMBIO_RESIDENZA_EMIGRAZI_FK5 
  FOREIGN KEY (ID_MOTIVO_COMUNICAZIONE) 
  REFERENCES ANAG_USR.CONF_MOTIVO_COMUNICAZIONE (ID_MOTIVO_COMUNICAZIONE)
  ENABLE VALIDATE,
  CONSTRAINT CAMBIO_RESIDENZA_EMIGRAZI_FK7 
  FOREIGN KEY (CODICE_TIPO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE,
  CONSTRAINT CAMBIO_RESIDENZA_EMIGRAZI_FK8 
  FOREIGN KEY (ID_STATO_EMIGRAZIONE) 
  REFERENCES ANAG_USR.CONF_STATO_ESTERO (ID_STATO_ESTERO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_SOGGETTO_CRE
(
  ID_SOGGETTO                NUMBER             NOT NULL,
  ID_CAMBIO_RESIDENZA_EMIGR  NUMBER             NOT NULL,
  NOME_ALLEGATO_APR4         VARCHAR2(80 BYTE),
  MODELLO_APR4               BLOB,
  NOME_ALLEGATO_DETTAGLIO    VARCHAR2(80 BYTE),
  DETTAGLIO_PERSONA          BLOB,
  ID_IRREPERIBILITA_CHIUSA   NUMBER
)
LOB (MODELLO_APR4) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
LOB (DETTAGLIO_PERSONA) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CRE.NOME_ALLEGATO_APR4 IS 'Indica il nome del file';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CRE.MODELLO_APR4 IS 'Contiene il file APR4';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CRE.ID_IRREPERIBILITA_CHIUSA IS 'Identificativo dell''ierreperibilità chiusa con l''emigrazione';



CREATE UNIQUE INDEX ANAG_USR.R_CAMBIO_RESIDENZA_EMIGR_PK ON ANAG_USR.R_SOGGETTO_CRE
(ID_SOGGETTO, ID_CAMBIO_RESIDENZA_EMIGR)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.R_SOGGETTO_CRE FOR ANAG_USR.R_SOGGETTO_CRE;


ALTER TABLE ANAG_USR.R_SOGGETTO_CRE ADD (
  CONSTRAINT R_CAMBIO_RESIDENZA_EMIGR_PK
  PRIMARY KEY
  (ID_SOGGETTO, ID_CAMBIO_RESIDENZA_EMIGR)
  USING INDEX ANAG_USR.R_CAMBIO_RESIDENZA_EMIGR_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_SOGGETTO_CRE ADD (
  CONSTRAINT R_CAMBIO_RESIDENZA_EMIGR_FK1 
  FOREIGN KEY (ID_CAMBIO_RESIDENZA_EMIGR) 
  REFERENCES ANAG_USR.CAMBIO_RESIDENZA_EMIGRAZIONE (ID_CAMBIO_RESIDENZA_EMIGR)
  ENABLE VALIDATE,
  CONSTRAINT R_CAMBIO_RESIDENZA_EMIGR_FK2 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_MODALITA_RILASCIO_CI
(
  ID_CONF_MODALITA_RILASCIO_CI  NUMBER          NOT NULL,
  DESCRIZIONE                   VARCHAR2(50 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_MODALITA_RILASCIO_CI.ID_CONF_MODALITA_RILASCIO_CI IS 'Il campo che identifica la modalita di rilascio';

COMMENT ON COLUMN ANAG_USR.CONF_MODALITA_RILASCIO_CI.DESCRIZIONE IS 'Descrizione della modalita di rilascio';



CREATE UNIQUE INDEX ANAG_USR.CONF_MODALITA_RILASCIO_CI_PK ON ANAG_USR.CONF_MODALITA_RILASCIO_CI
(ID_CONF_MODALITA_RILASCIO_CI)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_MODALITA_RILASCIO_CI ADD (
  CONSTRAINT CONF_MODALITA_RILASCIO_CI_PK
  PRIMARY KEY
  (ID_CONF_MODALITA_RILASCIO_CI)
  USING INDEX ANAG_USR.CONF_MODALITA_RILASCIO_CI_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONSENSO_RILASCIO_CI
(
  ID_CONSENSO_RILASCIO_CI  NUMBER               NOT NULL,
  TIPO_CONSENSO            CHAR(1 BYTE),
  COGNOME_PADRE            VARCHAR2(250 BYTE),
  NOME_PADRE               VARCHAR2(250 BYTE),
  COGNOME_MADRE            VARCHAR2(250 BYTE),
  NOME_MADRE               VARCHAR2(250 BYTE),
  COGNOME_TUTORE           VARCHAR2(250 BYTE),
  NOME_TUTORE              VARCHAR2(250 BYTE),
  COGNOME_TESTIMONE        VARCHAR2(250 BYTE),
  NOME_TESTIMONE           VARCHAR2(250 BYTE),
  DELEGA_PADRE             CHAR(1 BYTE),
  DELEGA_MADRE             CHAR(1 BYTE),
  DEFUNTO_PADRE            CHAR(1 BYTE),
  DEFUNTO_MADRE            CHAR(1 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONSENSO_RILASCIO_CI.ID_CONSENSO_RILASCIO_CI IS 'Campo che identifica il consenso.';

COMMENT ON COLUMN ANAG_USR.CONSENSO_RILASCIO_CI.TIPO_CONSENSO IS 'G -> genitore, T-> tutore';

COMMENT ON COLUMN ANAG_USR.CONSENSO_RILASCIO_CI.COGNOME_PADRE IS 'Campo che identifica il cognome del padre.';

COMMENT ON COLUMN ANAG_USR.CONSENSO_RILASCIO_CI.NOME_PADRE IS 'Campo che identifica il nome del padre.';

COMMENT ON COLUMN ANAG_USR.CONSENSO_RILASCIO_CI.COGNOME_MADRE IS 'Campo che identifica il cognome della madre.';

COMMENT ON COLUMN ANAG_USR.CONSENSO_RILASCIO_CI.NOME_MADRE IS 'Campo che identifica il nome della madre.';

COMMENT ON COLUMN ANAG_USR.CONSENSO_RILASCIO_CI.COGNOME_TUTORE IS 'Campo che identifica il cognome del tutore.';

COMMENT ON COLUMN ANAG_USR.CONSENSO_RILASCIO_CI.NOME_TUTORE IS 'Campo che identifica il nome del tutore.';



CREATE UNIQUE INDEX ANAG_USR.CONSENSO_RILASCIO_CI_PK ON ANAG_USR.CONSENSO_RILASCIO_CI
(ID_CONSENSO_RILASCIO_CI)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONSENSO_RILASCIO_CI ADD (
  CONSTRAINT CONSENSO_RILASCIO_CI_PK
  PRIMARY KEY
  (ID_CONSENSO_RILASCIO_CI)
  USING INDEX ANAG_USR.CONSENSO_RILASCIO_CI_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.OSTATIVA
(
  ID_OSTATIVA         NUMBER                    NOT NULL,
  TIPO_OSTATIVA       NUMBER,
  DATA_INSERIMENTO    DATE,
  DATA_ANNULLAMENTO   DATE,
  TIPO_COMUNICAZIONE  VARCHAR2(80 BYTE),
  NOTE                VARCHAR2(80 BYTE),
  ID_COMUNE_OSTATIVA  NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.OSTATIVA.ID_OSTATIVA IS 'Campo che identifica l''id dell''ostativa.';

COMMENT ON COLUMN ANAG_USR.OSTATIVA.TIPO_OSTATIVA IS 'Campo che identifica il tipo di ostativa';

COMMENT ON COLUMN ANAG_USR.OSTATIVA.DATA_INSERIMENTO IS 'Campo che identifica la data di inserimento dell''ostativa';

COMMENT ON COLUMN ANAG_USR.OSTATIVA.DATA_ANNULLAMENTO IS 'Campo che identifica la data di annullamento dell''ostativa';

COMMENT ON COLUMN ANAG_USR.OSTATIVA.NOTE IS 'Campo che identifica le note inserite in fase di annullamento.';

COMMENT ON COLUMN ANAG_USR.OSTATIVA.ID_COMUNE_OSTATIVA IS 'Indica il comune che ha inserito / comunicato l''ostativa';



CREATE UNIQUE INDEX ANAG_USR.OSTATIVA_PK ON ANAG_USR.OSTATIVA
(ID_OSTATIVA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.OSTATIVA FOR ANAG_USR.OSTATIVA;


ALTER TABLE ANAG_USR.OSTATIVA ADD (
  CONSTRAINT OSTATIVA_PK
  PRIMARY KEY
  (ID_OSTATIVA)
  USING INDEX ANAG_USR.OSTATIVA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.OSTATIVA ADD (
  CONSTRAINT TIPO_OSTATIVA_FK1 
  FOREIGN KEY (TIPO_OSTATIVA) 
  REFERENCES ANAG_USR.CONF_TIPO_OSTATIVA (ID_TIPO_OSTATIVA)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.IRREPERIBILITA
(
  ID_IRREPERIBILITA           NUMBER            NOT NULL,
  ID_PROCEDIMENTO_ANPR        NUMBER,
  ID_SOGGETTO                 NUMBER            NOT NULL,
  CODICE_TIPO_PROTOCOLLO      VARCHAR2(10 CHAR),
  ANNO_PROTOCOLLO             NUMBER,
  NUMERO_PROTOCOLLO           NUMBER,
  ANNO_PRATICA                NUMBER,
  NUMERO_PRATICA              NUMBER,
  ID_STATO_PRATICA            NUMBER,
  DATA_INIZIO                 DATE,
  DATA_FINE                   DATE,
  DATA_PUBBLICAZIONE_PRIMA    DATE,
  DATA_PUBBLICAZIONE_SECONDA  DATE,
  MOTIVAZIONE                 VARCHAR2(500 CHAR),
  FLG_COMUNE                  CHAR(1 CHAR),
  DATA_AGGIORNAMENTO          DATE,
  ID_MUNICIPIO                NUMBER,
  TIPO_ISTANZA                CHAR(1 BYTE),
  NOME_PARTE                  VARCHAR2(30 BYTE),
  COGNOME_PARTE               VARCHAR2(30 BYTE),
  SESSO_PARTE                 CHAR(1 BYTE),
  DATA_NASCITA_PARTE          DATE,
  NOTE_PARTE                  VARCHAR2(500 BYTE),
  ID_ELENCO_CANCELLATI        NUMBER,
  ID_ELENCO_AVVIO             NUMBER,
  NOTE                        VARCHAR2(500 BYTE),
  ID_GRUPPO_PL                NUMBER,
  FLG_SOSPESA                 VARCHAR2(1 BYTE),
  ID_UTENTE                   NUMBER,
  ID_UTENTE_DEF               NUMBER,
  ID_SOGGETTO_DICH            NUMBER,
  ID_RESIDENZA                NUMBER,
  ID_TOPONIMO                 NUMBER,
  ID_CIVICO                   NUMBER,
  CIVICO_INTERNO              VARCHAR2(500 BYTE),
  ALTRO_INDIRIZZO             VARCHAR2(1000 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.IRREPERIBILITA IS 'Tabella contenente le informazioni sul procedimento di Irreperibilità avviato a sistema.';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.ID_IRREPERIBILITA IS 'Identificativo della pratica di irreperibilità';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.ID_PROCEDIMENTO_ANPR IS 'Identificativo rilasciato da ANPR all''atto dell''apertura di un procedimento';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.ID_SOGGETTO IS 'Identificativo del soggetto per il quale è stata aperta una pratica di irreperibilità';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.CODICE_TIPO_PROTOCOLLO IS 'Codice di protocollo rappresentante la richiesta di irreperibilità';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.ANNO_PROTOCOLLO IS 'Anno di protocollo rappresentante la richiesta di irreperibilità';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.NUMERO_PROTOCOLLO IS 'Numero di protocollo rappresentante la richiesta di irreperibilità';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.ANNO_PRATICA IS 'Anno pratica';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.NUMERO_PRATICA IS 'Numero Pratica';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.ID_STATO_PRATICA IS 'FK verso la tabella tipologica contenente i vari stati attribuibili ad una pratica';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.DATA_INIZIO IS 'Data di inizio del procedimento di irreperibilità';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.DATA_FINE IS 'Data di conclusione del procedimento di irreperibilità';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.DATA_PUBBLICAZIONE_PRIMA IS 'Prima data di pubblicazione sull''albo pretorio.';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.DATA_PUBBLICAZIONE_SECONDA IS 'Seconda  data di pubblicazione sull''albo pretorio.';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.MOTIVAZIONE IS 'Motivazione di apertura del procedimento di irreperibilità';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.FLG_COMUNE IS 'S - > SI 
N -> NO';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.DATA_AGGIORNAMENTO IS 'Data ultima modifica';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.ID_MUNICIPIO IS 'Municipio di riferimento della pratica';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.TIPO_ISTANZA IS 'P - > ISTANZA DI PARTE  U - > ISTANZA D''UFFICIO';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.NOME_PARTE IS 'Nome soggetto che denuncia l''irreperibilità';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.COGNOME_PARTE IS 'Cognome soggetto che denuncia l''irreperibilità';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.SESSO_PARTE IS 'M -> UOMO  F -> DONNA sesso soggetto che denuncia l''irreperibilità';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.DATA_NASCITA_PARTE IS 'data di nascita soggetto che denuncia l''irreperibilità';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.NOTE_PARTE IS 'Note soggetto che denuncia l''irreperibilità';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.ID_ELENCO_CANCELLATI IS 'Campo che identifica l''elenco di cancellati che identifica la pratica';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.ID_ELENCO_AVVIO IS 'Campo che identifica l''elenco di avvio procedimento che identifica la pratica';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.NOTE IS 'Note procedimento';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.ID_GRUPPO_PL IS 'identificativo gruppo vigili';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.FLG_SOSPESA IS 'B->BLOCCATA S->SOSPESA';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.ID_UTENTE IS 'Identificativo dell''utente';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.ID_RESIDENZA IS 'Identificativo della residenza';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.ID_TOPONIMO IS 'Identificativo del toponimo';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.ID_CIVICO IS 'Identificativo del civico';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.CIVICO_INTERNO IS 'Civico intento';

COMMENT ON COLUMN ANAG_USR.IRREPERIBILITA.ALTRO_INDIRIZZO IS 'Descrizione indirizzo ignorasi o AIRE per irreperibilità precedenti a SIPO';



CREATE UNIQUE INDEX ANAG_USR.IRREPERIBILITA ON ANAG_USR.IRREPERIBILITA
(CODICE_TIPO_PROTOCOLLO, NUMERO_PROTOCOLLO, ANNO_PROTOCOLLO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.IRREPERIBILITA_PK ON ANAG_USR.IRREPERIBILITA
(ID_IRREPERIBILITA)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.IRREPERIBILITA ADD (
  CONSTRAINT IRREPERIBILITA_PK
  PRIMARY KEY
  (ID_IRREPERIBILITA)
  USING INDEX ANAG_USR.IRREPERIBILITA_PK
  ENABLE VALIDATE,
  CONSTRAINT IRREPERIBILITA
  UNIQUE (CODICE_TIPO_PROTOCOLLO, NUMERO_PROTOCOLLO, ANNO_PROTOCOLLO)
  USING INDEX ANAG_USR.IRREPERIBILITA
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.IRREPERIBILITA ADD (
  CONSTRAINT CONF_STATO_PRATICA_FKV5 
  FOREIGN KEY (ID_STATO_PRATICA) 
  REFERENCES ANAG_USR.CONF_STATO_PRATICA (ID_STATO_PRATICA)
  ENABLE VALIDATE,
  CONSTRAINT ELENCO_FK1 
  FOREIGN KEY (ID_ELENCO_CANCELLATI) 
  REFERENCES ANAG_USR.ELENCO_IRREPERIBILITA (ID_ELENCO_IRREPERIBILITA)
  ENABLE VALIDATE,
  CONSTRAINT ELENCO_FK2 
  FOREIGN KEY (ID_ELENCO_AVVIO) 
  REFERENCES ANAG_USR.ELENCO_IRREPERIBILITA (ID_ELENCO_IRREPERIBILITA)
  ENABLE VALIDATE,
  CONSTRAINT ID_GRUPPO_PL_FK 
  FOREIGN KEY (ID_GRUPPO_PL) 
  REFERENCES ANAG_USR.CONF_STRUTTURE_INTERNE_RC (ID)
  ENABLE VALIDATE,
  CONSTRAINT ID_MUNICIPIO_CSI_FK 
  FOREIGN KEY (ID_MUNICIPIO) 
  REFERENCES ANAG_USR.CONF_STRUTTURE_INTERNE_RC (ID)
  ENABLE VALIDATE,
  CONSTRAINT IRREPERIBILITA_FK1 
  FOREIGN KEY (CODICE_TIPO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE,
  CONSTRAINT IRREPERIBILITA_FK2 
  FOREIGN KEY (ID_TOPONIMO) 
  REFERENCES ANAG_USR.TOPONIMO (ID_TOPONIMO)
  ENABLE VALIDATE,
  CONSTRAINT IRREPERIBILITA_FK3 
  FOREIGN KEY (ID_CIVICO) 
  REFERENCES ANAG_USR.CIVICO (ID_CIVICO)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_IRR_FK 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.RETTIFICHE_LISTE_LEVA
(
  ID_RETTIFICHE     NUMBER                      NOT NULL,
  ID_SOGGETTO_LEVA  NUMBER,
  ID_LISTA_LEVA     NUMBER,
  ANNO              NUMBER(4)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.RETTIFICHE_LISTE_LEVA_PK ON ANAG_USR.RETTIFICHE_LISTE_LEVA
(ID_RETTIFICHE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.RETTIFICHE_LISTE_LEVA ADD (
  CONSTRAINT RETTIFICHE_LISTE_LEVA_PK
  PRIMARY KEY
  (ID_RETTIFICHE)
  USING INDEX ANAG_USR.RETTIFICHE_LISTE_LEVA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.RETTIFICHE_LISTE_LEVA ADD (
  CONSTRAINT ID_LISTA_LEVA_FK1 
  FOREIGN KEY (ID_LISTA_LEVA) 
  REFERENCES ANAG_USR.LISTE_LEVA (ID_LISTA_LEVA)
  ENABLE VALIDATE,
  CONSTRAINT ID_SOGGETTO_LEVA_FK1 
  FOREIGN KEY (ID_SOGGETTO_LEVA) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_ALLEGATI_PRATICA_CERTIFCATI
(
  ID_R_ALLEGATI_PRATICA    NUMBER               NOT NULL,
  ID_ALLEGATO_CERTIFICATO  NUMBER               NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.R_ALLEGATI_PRATICA_CERTIFCATI.ID_R_ALLEGATI_PRATICA IS 'identificativo della relazione tra una pratica di certificati e gli allegati ad essa connessa';

COMMENT ON COLUMN ANAG_USR.R_ALLEGATI_PRATICA_CERTIFCATI.ID_ALLEGATO_CERTIFICATO IS 'Id allegato associato';



CREATE UNIQUE INDEX ANAG_USR.CONF_ALLEGATI_CERTIFCATO_UK1 ON ANAG_USR.R_ALLEGATI_PRATICA_CERTIFCATI
(ID_R_ALLEGATI_PRATICA, ID_ALLEGATO_CERTIFICATO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_ALLEGATI_PRATICA_CERTIFCATI ADD (
  CONSTRAINT CONF_ALLEGATI_CERTIFCATO_UK1
  UNIQUE (ID_R_ALLEGATI_PRATICA, ID_ALLEGATO_CERTIFICATO)
  USING INDEX ANAG_USR.CONF_ALLEGATI_CERTIFCATO_UK1
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_ALLEGATI_PRATICA_CERTIFCATI ADD (
  CONSTRAINT ID_ALLEGATO_CERTIFICATO_FK 
  FOREIGN KEY (ID_ALLEGATO_CERTIFICATO) 
  REFERENCES ANAG_USR.ALLEGATO_CERTIFICATO (ID_ALLEGATO_CERTIFICATO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.POP
(
  ID                          NUMBER            NOT NULL,
  ID_SOGGETTO                 NUMBER,
  CODICE_INDIVIDUALE          VARCHAR2(20 BYTE),
  ID_FAMIGLIA                 NUMBER,
  CODICE_FAMIGLIA             VARCHAR2(20 BYTE),
  DATA_APPARTENENZA_FAMIGLIA  DATE,
  DATA_INIZIO_RESIDENZA       DATE,
  DATA_FINE_RESIDENZA         DATE,
  ID_COMUNE_PROVENIENZA       NUMBER,
  ID_LOCALITA_PROVENIENZA     NUMBER,
  ID_COMUNE_EMIGRAZIONE       NUMBER,
  ID_LOCALITA_EMIGRAZIONE     NUMBER,
  PRATICA_IMMIGRAZIONE        VARCHAR2(20 BYTE),
  ANNO_PRATICA_IMMIGRAZIONE   VARCHAR2(4 BYTE),
  PRATICA_EMIGRAZIONE         VARCHAR2(20 BYTE),
  ANNO_PRATICA_EMIGRAZIONE    VARCHAR2(4 BYTE),
  ID_STATUS_SOGGETTO          NUMBER,
  DATA_INIZIO_REGISTRAZIONE   DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.POP.ID IS 'Identificativo incrementale di tabella';

COMMENT ON COLUMN ANAG_USR.POP.ID_SOGGETTO IS 'Identificativo del soggetto';

COMMENT ON COLUMN ANAG_USR.POP.CODICE_INDIVIDUALE IS 'Codice individuale del soggetto';

COMMENT ON COLUMN ANAG_USR.POP.ID_FAMIGLIA IS 'Identificativo della famiglia';

COMMENT ON COLUMN ANAG_USR.POP.CODICE_FAMIGLIA IS 'Codice famiglia del soggetto';

COMMENT ON COLUMN ANAG_USR.POP.DATA_APPARTENENZA_FAMIGLIA IS 'Data di inizio appartenenza alla famiglia';

COMMENT ON COLUMN ANAG_USR.POP.DATA_INIZIO_RESIDENZA IS 'Data di inizio residenza';

COMMENT ON COLUMN ANAG_USR.POP.DATA_FINE_RESIDENZA IS 'Data fine residenza / Data iscrizione AIRE';

COMMENT ON COLUMN ANAG_USR.POP.ID_COMUNE_PROVENIENZA IS 'Identificativo del comune di provenienza';

COMMENT ON COLUMN ANAG_USR.POP.ID_LOCALITA_PROVENIENZA IS 'Identificativo della località di provenienza';

COMMENT ON COLUMN ANAG_USR.POP.ID_COMUNE_EMIGRAZIONE IS 'Identificativo del comune di emigrazione';

COMMENT ON COLUMN ANAG_USR.POP.ID_LOCALITA_EMIGRAZIONE IS 'Identificativo della località di emigrazione / iscrizione AIRE';

COMMENT ON COLUMN ANAG_USR.POP.PRATICA_IMMIGRAZIONE IS 'Numero pratica di immigrazione a Roma';

COMMENT ON COLUMN ANAG_USR.POP.ANNO_PRATICA_IMMIGRAZIONE IS 'Anno pratica di immigrazione a Roma';

COMMENT ON COLUMN ANAG_USR.POP.PRATICA_EMIGRAZIONE IS 'Numero pratica emigrazione da Roma';

COMMENT ON COLUMN ANAG_USR.POP.ANNO_PRATICA_EMIGRAZIONE IS 'Anno pratica emigrazione da Roma';

COMMENT ON COLUMN ANAG_USR.POP.ID_STATUS_SOGGETTO IS 'Status Soggetto';

COMMENT ON COLUMN ANAG_USR.POP.DATA_INIZIO_REGISTRAZIONE IS 'Data inizio registrazione pop';



CREATE UNIQUE INDEX ANAG_USR.POP_ID_SOGGETTO_UK ON ANAG_USR.POP
(ID_SOGGETTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.POP_P_PK ON ANAG_USR.POP
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.POP ADD (
  CONSTRAINT POP_P_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.POP_P_PK
  ENABLE VALIDATE,
  CONSTRAINT POP_ID_SOGGETTO_UK
  UNIQUE (ID_SOGGETTO)
  USING INDEX ANAG_USR.POP_ID_SOGGETTO_UK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.POP ADD (
  CONSTRAINT POP_COMUNE_EMI_FK 
  FOREIGN KEY (ID_COMUNE_EMIGRAZIONE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT POP_COMUNE_PROV_FK 
  FOREIGN KEY (ID_COMUNE_PROVENIENZA) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT POP_ID_FAMIGLIA_FK 
  FOREIGN KEY (ID_FAMIGLIA) 
  REFERENCES ANAG_USR.FAMIGLIA_CONVIVENZA (ID_FAMIGLIA_CONV)
  ENABLE VALIDATE,
  CONSTRAINT POP_ID_SOGGETTO_FK 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT POP_LOCALITA_EMI_FK 
  FOREIGN KEY (ID_LOCALITA_EMIGRAZIONE) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE,
  CONSTRAINT POP_LOCALITA_PROV_FK 
  FOREIGN KEY (ID_LOCALITA_PROVENIENZA) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE,
  CONSTRAINT POP_STATUS_SOGGETTO_FK 
  FOREIGN KEY (ID_STATUS_SOGGETTO) 
  REFERENCES ANAG_USR.CONF_STATUS_SOGGETTO (ID_STATUS_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.FAMIGL
(
  ID                        NUMBER              NOT NULL,
  ID_FAMIGLIA               NUMBER,
  CODICE_FAMIGLIA           VARCHAR2(20 BYTE),
  ID_TOPONIMO               NUMBER,
  ID_CIVICO                 NUMBER,
  LOTTO                     VARCHAR2(20 BYTE),
  PALAZZINA                 VARCHAR2(20 BYTE),
  SCALA                     VARCHAR2(20 BYTE),
  PIANO                     VARCHAR2(20 BYTE),
  INTERNO                   VARCHAR2(20 BYTE),
  FLAG_ATTIVO               VARCHAR2(1 BYTE),
  DATA_INIZIO_VALIDITA      DATE,
  DATA_CAMBIO_DOMICILIO     DATE,
  PRATICA_CAMBIO_DOMICILIO  VARCHAR2(20 BYTE),
  ID_LOCALITA_AIRE          NUMBER,
  INDIRIZZO_AIRE            VARCHAR2(500 BYTE),
  CAP_AIRE                  VARCHAR2(20 BYTE),
  ID_CONSOLATO              NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.FAMIGL.ID IS 'Identificativo incrementale di tabella';

COMMENT ON COLUMN ANAG_USR.FAMIGL.ID_FAMIGLIA IS 'Identificativo della famiglia';

COMMENT ON COLUMN ANAG_USR.FAMIGL.CODICE_FAMIGLIA IS 'Codice famiglia';

COMMENT ON COLUMN ANAG_USR.FAMIGL.ID_TOPONIMO IS 'Identificativo del toponimo';

COMMENT ON COLUMN ANAG_USR.FAMIGL.ID_CIVICO IS 'Identificativo del civico';

COMMENT ON COLUMN ANAG_USR.FAMIGL.LOTTO IS 'Numero del lotto';

COMMENT ON COLUMN ANAG_USR.FAMIGL.FLAG_ATTIVO IS 'S -> Attivo, N -> Non attivo';

COMMENT ON COLUMN ANAG_USR.FAMIGL.DATA_CAMBIO_DOMICILIO IS 'Data cambio di domicilio';

COMMENT ON COLUMN ANAG_USR.FAMIGL.PRATICA_CAMBIO_DOMICILIO IS 'Numero pratica del cambio di domicilio';

COMMENT ON COLUMN ANAG_USR.FAMIGL.ID_LOCALITA_AIRE IS 'Identificativo della località AIRE di residenza';

COMMENT ON COLUMN ANAG_USR.FAMIGL.INDIRIZZO_AIRE IS 'Indirizzo AIRE';

COMMENT ON COLUMN ANAG_USR.FAMIGL.CAP_AIRE IS 'CAP AIRE';

COMMENT ON COLUMN ANAG_USR.FAMIGL.ID_CONSOLATO IS 'Identificativo del consolato di appartenenza';



CREATE UNIQUE INDEX ANAG_USR.FAMIGL_ID_FAMIGLIA_UN ON ANAG_USR.FAMIGL
(ID_FAMIGLIA, CODICE_FAMIGLIA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.FAMIGL_PK ON ANAG_USR.FAMIGL
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.FAMIGL ADD (
  CONSTRAINT FAMIGL_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.FAMIGL_PK
  ENABLE VALIDATE,
  CONSTRAINT FAMIGL_ID_FAMIGLIA_UN
  UNIQUE (ID_FAMIGLIA, CODICE_FAMIGLIA)
  USING INDEX ANAG_USR.FAMIGL_ID_FAMIGLIA_UN
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.FAMIGL ADD (
  CONSTRAINT FAMIGL_ID_CIVICO_FK 
  FOREIGN KEY (ID_CIVICO) 
  REFERENCES ANAG_USR.CIVICO (ID_CIVICO)
  ENABLE VALIDATE,
  CONSTRAINT FAMIGL_ID_CONSOLATO_FK 
  FOREIGN KEY (ID_CONSOLATO) 
  REFERENCES ANAG_USR.CONSOLATO (ID_CONSOLATO)
  ENABLE VALIDATE,
  CONSTRAINT FAMIGL_ID_FAMIGLIA_FK 
  FOREIGN KEY (ID_FAMIGLIA) 
  REFERENCES ANAG_USR.FAMIGLIA_CONVIVENZA (ID_FAMIGLIA_CONV)
  ENABLE VALIDATE,
  CONSTRAINT FAMIGL_ID_LOCALITA_FK 
  FOREIGN KEY (ID_LOCALITA_AIRE) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE,
  CONSTRAINT FAMIGL_ID_TOPONIMO_FK 
  FOREIGN KEY (ID_TOPONIMO) 
  REFERENCES ANAG_USR.TOPONIMO (ID_TOPONIMO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.FAMIG2
(
  ID                    NUMBER                  NOT NULL,
  ID_SOGGETTO           NUMBER,
  CODICE_INDIVIDUALE    VARCHAR2(20 BYTE),
  ID_FAMIGLIA           NUMBER,
  CODICE_FAMIGLIA       VARCHAR2(20 BYTE),
  ID_CODICE_LEGAME      NUMBER,
  DATA_INIZIO_VALIDITA  DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.FAMIG2.ID IS 'Identificativo incrementale di tabella';

COMMENT ON COLUMN ANAG_USR.FAMIG2.ID_SOGGETTO IS 'Identificativo del soggetto';

COMMENT ON COLUMN ANAG_USR.FAMIG2.CODICE_INDIVIDUALE IS 'Codice individuale';

COMMENT ON COLUMN ANAG_USR.FAMIG2.ID_FAMIGLIA IS 'Identificativo della famiglia del soggetto';

COMMENT ON COLUMN ANAG_USR.FAMIG2.CODICE_FAMIGLIA IS 'Codice famiglia del soggetto';

COMMENT ON COLUMN ANAG_USR.FAMIG2.ID_CODICE_LEGAME IS 'Identificativo del rapporto di parentela';

COMMENT ON COLUMN ANAG_USR.FAMIG2.DATA_INIZIO_VALIDITA IS 'Data inizio validità famiglia';



CREATE UNIQUE INDEX ANAG_USR.FAMIG2_ID_SOGGETTO_UK ON ANAG_USR.FAMIG2
(ID_SOGGETTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.FAMIG2_PK ON ANAG_USR.FAMIG2
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.FAMIG2 ADD (
  CONSTRAINT FAMIG2_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.FAMIG2_PK
  ENABLE VALIDATE,
  CONSTRAINT FAMIG2_ID_SOGGETTO_UK
  UNIQUE (ID_SOGGETTO)
  USING INDEX ANAG_USR.FAMIG2_ID_SOGGETTO_UK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.FAMIG2 ADD (
  CONSTRAINT ID_FAMIGLIA_FK 
  FOREIGN KEY (ID_FAMIGLIA) 
  REFERENCES ANAG_USR.FAMIGLIA_CONVIVENZA (ID_FAMIGLIA_CONV)
  ENABLE VALIDATE,
  CONSTRAINT ID_SOGGETTO_FK 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_MOTIVO_MEMORIZZAZIONE
(
  ID_MOTIVO_MEMORIZZAZIONE  NUMBER              NOT NULL,
  DESCRIZIONE               VARCHAR2(250 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_MEMORIZZAZIONE.ID_MOTIVO_MEMORIZZAZIONE IS 'Identificativo del motivo di memorizzazione';

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_MEMORIZZAZIONE.DESCRIZIONE IS 'Descrizione del motivo di memorizzazione';



CREATE UNIQUE INDEX ANAG_USR.CONF_MOTIVO_MEMORIZZAZIONE_PK ON ANAG_USR.CONF_MOTIVO_MEMORIZZAZIONE
(ID_MOTIVO_MEMORIZZAZIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_MOTIVO_MEMORIZZAZIONE ADD (
  CONSTRAINT CONF_MOTIVO_MEMORIZZAZIONE_PK
  PRIMARY KEY
  (ID_MOTIVO_MEMORIZZAZIONE)
  USING INDEX ANAG_USR.CONF_MOTIVO_MEMORIZZAZIONE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_INIZIATIVA_ISCR_AIRE
(
  ID_INIZIATIVA  NUMBER                         NOT NULL,
  DESCRIZIONE    VARCHAR2(100 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_INIZIATIVA_ISCR_AIRE.ID_INIZIATIVA IS 'Identificativo dell''iniziativa di iscrizione AIRE';

COMMENT ON COLUMN ANAG_USR.CONF_INIZIATIVA_ISCR_AIRE.DESCRIZIONE IS 'Descrizione dell''iniziativa di iscrizione AIRE';



CREATE UNIQUE INDEX ANAG_USR.CONF_INIZIATIVA_ISCR_AIRE_PK ON ANAG_USR.CONF_INIZIATIVA_ISCR_AIRE
(ID_INIZIATIVA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_INIZIATIVA_ISCR_AIRE ADD (
  CONSTRAINT CONF_INIZIATIVA_ISCR_AIRE_PK
  PRIMARY KEY
  (ID_INIZIATIVA)
  USING INDEX ANAG_USR.CONF_INIZIATIVA_ISCR_AIRE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_ESTENSIONE_ALLEGATI
(
  ID_ESTENSIONE_ALLEGATO    NUMBER              NOT NULL,
  NOME_ESTENSIONE           VARCHAR2(20 BYTE),
  TIPO_ESTENSIONE_ALLEGATO  NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_ESTENSIONE_ALLEGATI_PK ON ANAG_USR.CONF_ESTENSIONE_ALLEGATI
(ID_ESTENSIONE_ALLEGATO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_ESTENSIONE_ALLEGATI ADD (
  CONSTRAINT CONF_ESTENSIONE_ALLEGATI_PK
  PRIMARY KEY
  (ID_ESTENSIONE_ALLEGATO)
  USING INDEX ANAG_USR.CONF_ESTENSIONE_ALLEGATI_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_ESENZIONE_CERTIFICATO
(
  ID_ESENZIONE  NUMBER                          NOT NULL,
  DESCRIZIONE   VARCHAR2(500 BYTE),
  FLG_ONLINE    CHAR(1 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_ESENZIONE_CERTIFICATO.ID_ESENZIONE IS 'Identificativo della conf esenzione certificato';

COMMENT ON COLUMN ANAG_USR.CONF_ESENZIONE_CERTIFICATO.DESCRIZIONE IS 'Descrizione dell esenzione dell imposta di bollo del certificato richiesto
';

COMMENT ON COLUMN ANAG_USR.CONF_ESENZIONE_CERTIFICATO.FLG_ONLINE IS 'S-> indica che l''esenzione è valida solo per le richieste di certificati online, N-> indica che l esenzione è valida per tutte le richieste';



CREATE UNIQUE INDEX ANAG_USR.CONF_ESENZIONE_CERTIFICATO_PK ON ANAG_USR.CONF_ESENZIONE_CERTIFICATO
(ID_ESENZIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_ESENZIONE_CERTIFICATO ADD (
  CONSTRAINT CONF_ESENZIONE_CERTIFICATO_PK
  PRIMARY KEY
  (ID_ESENZIONE)
  USING INDEX ANAG_USR.CONF_ESENZIONE_CERTIFICATO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.TEMPLATE
(
  ID_TEMPLATE  NUMBER                           NOT NULL,
  DESCRIZIONE  VARCHAR2(150 BYTE),
  TEMPLATE     BLOB
)
LOB (TEMPLATE) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.TEMPLATE_PK ON ANAG_USR.TEMPLATE
(ID_TEMPLATE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.TEMPLATE ADD (
  CONSTRAINT TEMPLATE_PK
  PRIMARY KEY
  (ID_TEMPLATE)
  USING INDEX ANAG_USR.TEMPLATE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CIC_BIANCHE
(
  ID_CIC_BIANCHE   NUMBER                       NOT NULL,
  DA_NUMERO        VARCHAR2(20 BYTE),
  A_NUMERO         VARCHAR2(20 BYTE),
  TIPO_OPERAZIONE  CHAR(1 BYTE),
  ID_STRUTTURA     NUMBER,
  DATA_OPERAZIONE  DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CIC_BIANCHE.ID_CIC_BIANCHE IS 'Identificativo dell''operazione sui blocchi di carte bianche';

COMMENT ON COLUMN ANAG_USR.CIC_BIANCHE.DA_NUMERO IS 'Numero di partenza delle carte';

COMMENT ON COLUMN ANAG_USR.CIC_BIANCHE.TIPO_OPERAZIONE IS 'Campo che identifica il tipo di operazione R -> REGISTRAZIONE, A-> ASSEGNAZIONE, C-> CANCELLAZIONE.';



CREATE UNIQUE INDEX ANAG_USR.CIC_BIANCHE_PK ON ANAG_USR.CIC_BIANCHE
(ID_CIC_BIANCHE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CIC_BIANCHE ADD (
  CONSTRAINT CIC_BIANCHE_PK
  PRIMARY KEY
  (ID_CIC_BIANCHE)
  USING INDEX ANAG_USR.CIC_BIANCHE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CIC_BIANCHE ADD (
  CONSTRAINT ID_STRUTTURA 
  FOREIGN KEY (ID_STRUTTURA) 
  REFERENCES ANAG_USR.CONF_STRUTTURE_INTERNE_RC (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_CONVENZIONI
(
  ID_TIPO_CONVENZIONI       NUMBER              NOT NULL,
  DESCRIZIONE               VARCHAR2(250 BYTE),
  TIPO_SCELTA_PATRIMONIALE  VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_CONVENZIONI.ID_TIPO_CONVENZIONI IS 'Identificativo del tipo di convenzione ';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_CONVENZIONI.DESCRIZIONE IS 'Descrizione del tipo di convenzione';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_CONVENZIONI.TIPO_SCELTA_PATRIMONIALE IS 'S - Separazione, C- Comunione';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_CONVENZIONI_PK ON ANAG_USR.CONF_TIPO_CONVENZIONI
(ID_TIPO_CONVENZIONI)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_CONVENZIONI ADD (
  CONSTRAINT CONF_TIPO_CONVENZIONI_PK
  PRIMARY KEY
  (ID_TIPO_CONVENZIONI)
  USING INDEX ANAG_USR.CONF_TIPO_CONVENZIONI_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA
(
  ID_PRATICA            NUMBER                  NOT NULL,
  NUMERO_PROTOCOLLO     VARCHAR2(200 BYTE),
  NUMERO_PRATICA        NUMBER,
  ID_STATO_PRATICA      NUMBER,
  ID_SOGGETTO_INT       NUMBER,
  DATA_CREAZIONE        DATE,
  DATA_MODIFICA         DATE,
  DATA_VALIDITA         DATE,
  ANNO_PROTOCOLLO       NUMBER,
  ID_RESIDENZA          NUMBER,
  ANNO_PRATICA          NUMBER,
  ID_OPERAZIONE_ANPR    VARCHAR2(50 BYTE),
  ID_OPERAZIONE_COMUNE  VARCHAR2(50 BYTE),
  OPERAZIONE_RICHIESTA  VARCHAR2(50 BYTE),
  NOTE_CANCELLAZIONE    VARCHAR2(400 BYTE),
  FLG_ACCERTAMENTO      NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA.ID_PRATICA IS 'Identificativo univoco della pratica';

COMMENT ON COLUMN ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA.NUMERO_PROTOCOLLO IS 'Indica il numero di protocollo della pratica';

COMMENT ON COLUMN ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA.NUMERO_PRATICA IS 'Indica il numero della pratica';

COMMENT ON COLUMN ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA.ID_STATO_PRATICA IS 'Indica lo stato della pratica';

COMMENT ON COLUMN ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA.ID_SOGGETTO_INT IS 'Indica il soggetto intestatario della pratica';

COMMENT ON COLUMN ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA.DATA_CREAZIONE IS 'Indica la data di creazione della pratica';

COMMENT ON COLUMN ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA.DATA_MODIFICA IS 'Indica la data in cui la pratica è stata modificata';

COMMENT ON COLUMN ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA.DATA_VALIDITA IS 'Indica la data in cui la pratica è stata validata ';

COMMENT ON COLUMN ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA.ANNO_PROTOCOLLO IS 'Indica l''anno di protocollazione della pratica
';

COMMENT ON COLUMN ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA.ID_RESIDENZA IS 'Indica il domicilio in cui il soggetto vuole trasferirsi in maniera temporanea
';

COMMENT ON COLUMN ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA.ANNO_PRATICA IS 'Indica l''anno della pratica';

COMMENT ON COLUMN ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA.ID_OPERAZIONE_ANPR IS 'Id operazione comune di anpr';

COMMENT ON COLUMN ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA.ID_OPERAZIONE_COMUNE IS 'id operazione comune di ANPR';

COMMENT ON COLUMN ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA.OPERAZIONE_RICHIESTA IS 'Indica l''operazione richiesta su anpr per questa pratica';

COMMENT ON COLUMN ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA.NOTE_CANCELLAZIONE IS 'Sono le note che descrivono il motivo della cancellazione';

COMMENT ON COLUMN ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA.FLG_ACCERTAMENTO IS 'Campo che indica se l''accertamento per la pratica è in corso. 1->In corso';



CREATE UNIQUE INDEX ANAG_USR.PRATICA_POPOLAZIONE_TEMPOR_PK ON ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA
(ID_PRATICA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA ADD (
  CONSTRAINT PRATICA_POPOLAZIONE_TEMPOR_PK
  PRIMARY KEY
  (ID_PRATICA)
  USING INDEX ANAG_USR.PRATICA_POPOLAZIONE_TEMPOR_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.PRATICA_POPOLAZIONE_TEMPORANEA ADD (
  CONSTRAINT ID_DOMICILIO_FK 
  FOREIGN KEY (ID_RESIDENZA) 
  REFERENCES ANAG_USR.RESIDENZA (ID_RESIDENZA)
  ENABLE VALIDATE,
  CONSTRAINT ID_SOGG_PT_FK 
  FOREIGN KEY (ID_SOGGETTO_INT) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT ID_STATO_PRATICA_PT_FK 
  FOREIGN KEY (ID_STATO_PRATICA) 
  REFERENCES ANAG_USR.CONF_STATO_PRATICA (ID_STATO_PRATICA)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_SENTENZA
(
  ID_TIPO_SENTENZA  NUMBER                      NOT NULL,
  DESCRIZIONE       VARCHAR2(200 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_SENTENZA.ID_TIPO_SENTENZA IS 'identificativo del tipo di sentenza';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_SENTENZA.DESCRIZIONE IS 'Descrizione del tipo di sentenza';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_SENTENZA_PK ON ANAG_USR.CONF_TIPO_SENTENZA
(ID_TIPO_SENTENZA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_SENTENZA ADD (
  CONSTRAINT CONF_TIPO_SENTENZA_PK
  PRIMARY KEY
  (ID_TIPO_SENTENZA)
  USING INDEX ANAG_USR.CONF_TIPO_SENTENZA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.OGGETTO_PRATICA_AIRE
(
  ID_OGGETTO_PRATICA_AIRE  NUMBER               NOT NULL,
  DESCRIZIONE              VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.OGGETTO_PRATICA_AIRE.ID_OGGETTO_PRATICA_AIRE IS 'Identificativo dell''oggetto pratica AIRE';

COMMENT ON COLUMN ANAG_USR.OGGETTO_PRATICA_AIRE.DESCRIZIONE IS 'Descrizione dell''oggetto pratica AIRE';



CREATE UNIQUE INDEX ANAG_USR.OGGETTO_PRATICA_AIRE_PK ON ANAG_USR.OGGETTO_PRATICA_AIRE
(ID_OGGETTO_PRATICA_AIRE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.OGGETTO_PRATICA_AIRE ADD (
  CONSTRAINT OGGETTO_PRATICA_AIRE_PK
  PRIMARY KEY
  (ID_OGGETTO_PRATICA_AIRE)
  USING INDEX ANAG_USR.OGGETTO_PRATICA_AIRE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.VACCINAZIONE
(
  ID_VACCINAZIONE       NUMBER                  NOT NULL,
  ID_SOGGETTO           NUMBER,
  ID_CONF_VACCINAZIONE  NUMBER,
  ESITO_VACCINAZIONE    NUMBER(1),
  DATA_VACC             DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.VACCINAZIONE.ID_VACCINAZIONE IS 'Identificativo univoco della vaccinazione';

COMMENT ON COLUMN ANAG_USR.VACCINAZIONE.ID_SOGGETTO IS 'Identificativo della persona che ha fatto il vaccino';

COMMENT ON COLUMN ANAG_USR.VACCINAZIONE.ID_CONF_VACCINAZIONE IS 'Identificativo del tipo di vaccino fatto';

COMMENT ON COLUMN ANAG_USR.VACCINAZIONE.ESITO_VACCINAZIONE IS 'Esito della vaccinazione, ''1''-> POSITIVA, ''0''->NEGATIVA';

COMMENT ON COLUMN ANAG_USR.VACCINAZIONE.DATA_VACC IS 'Data nella quale la vaccinazione è stata eseguita';



CREATE UNIQUE INDEX ANAG_USR.VACCINAZIONE_PK ON ANAG_USR.VACCINAZIONE
(ID_VACCINAZIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.VACCINAZIONE ADD (
  CONSTRAINT VACCINAZIONE_PK
  PRIMARY KEY
  (ID_VACCINAZIONE)
  USING INDEX ANAG_USR.VACCINAZIONE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.VACCINAZIONE ADD (
  CONSTRAINT FK_CONF_VACC 
  FOREIGN KEY (ID_CONF_VACCINAZIONE) 
  REFERENCES ANAG_USR.CONF_VACCINAZIONE (ID_CONF_VACCINAZIONE)
  ENABLE VALIDATE,
  CONSTRAINT FK_SOGGETTO 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.REG_USER_ANPR
(
  ID                   NUMBER                   NOT NULL,
  ID_UTENTE            NUMBER,
  ID_SEDE              VARCHAR2(20 BYTE),
  ID_POSTAZIONE        VARCHAR2(100 BYTE),
  KEYSTORE_POSTAZIONE  BLOB                     NOT NULL,
  PWD_KEYSTORE         VARCHAR2(100 BYTE),
  ALIAS_KEYSTORE       VARCHAR2(100 BYTE),
  HOSTNAME             VARCHAR2(200 BYTE),
  SN_KEYSTORE          VARCHAR2(20 BYTE)
)
LOB (KEYSTORE_POSTAZIONE) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.RENG_USER_ANPR_PK ON ANAG_USR.REG_USER_ANPR
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.REG_USER_ANPR ADD (
  CONSTRAINT RENG_USER_ANPR_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.RENG_USER_ANPR_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.REG_USER_ANPR ADD (
  CONSTRAINT REG_USER_ANPR_FK1 
  FOREIGN KEY (ID_UTENTE) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_MOTIVO_COMUNICAZIONE
(
  ID_MOTIVO_COMUNICAZIONE  NUMBER               NOT NULL,
  DESCRIZIONE              VARCHAR2(40 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_COMUNICAZIONE.DESCRIZIONE IS 'DESCRIZIONE MOTIVAZIONE';



CREATE UNIQUE INDEX ANAG_USR.CONF_MOTIVAZIONE_COMUNICAZ_PK ON ANAG_USR.CONF_MOTIVO_COMUNICAZIONE
(ID_MOTIVO_COMUNICAZIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_MOTIVO_COMUNICAZIONE ADD (
  CONSTRAINT CONF_MOTIVAZIONE_COMUNICAZ_PK
  PRIMARY KEY
  (ID_MOTIVO_COMUNICAZIONE)
  USING INDEX ANAG_USR.CONF_MOTIVAZIONE_COMUNICAZ_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONTRATTO
(
  ID_CONTRATTO                NUMBER            NOT NULL,
  DATA_INIZIO                 DATE,
  DATA_NOTIFICA               DATE,
  DATA_DOCUMENTO              DATE,
  DOCUMENTO                   CLOB,
  CHECK_DOCUMENTO             CHAR(1 CHAR),
  FLG_NOTAIO_AVVOCATO         CHAR(1 CHAR),
  COGNOME_PROF                VARCHAR2(50 CHAR),
  NOME_PROF                   VARCHAR2(50 CHAR),
  EMAIL_PROF                  VARCHAR2(50 CHAR),
  TELEFONO_PROF               VARCHAR2(50 CHAR),
  STUDIO_PROF                 VARCHAR2(50 CHAR),
  COMUNE_STUDIO_PROF          VARCHAR2(50 CHAR),
  LUOGO_ECCEZIONALE           VARCHAR2(120 BYTE),
  LOCALITA_ID                 NUMBER,
  ID_COMUNE_REGISTRAZIONE     NUMBER,
  ID_COMUNE_EVENTO            NUMBER,
  CODICE_TIPO_PROTOCOLLO      VARCHAR2(10 BYTE),
  NUMERO_PROTOCOLLO           NUMBER,
  ANNO_PROTOCOLLO             NUMBER(4),
  NUMERO_PRATICA              NUMBER,
  ANNO_PRATICA                NUMBER(4),
  ID_STATO_PRATICA            NUMBER            NOT NULL,
  MOTIVO_ELIMINAZIONE         VARCHAR2(50 CHAR),
  ID_DICHIARAZIONE            NUMBER            NOT NULL,
  ID_CONTRATTO_ANNULLATO      NUMBER,
  DATA_PROTOCOLLO             DATE,
  ID_MOTIV_CHIUSURA           NUMBER,
  FLAG_TIPO_CONTRATTO         VARCHAR2(1 BYTE),
  NUMERO_REPERTORIO_NOTARILE  NUMBER,
  COD_COMUNE_AGGIOR           VARCHAR2(20 BYTE)
)
LOB (DOCUMENTO) STORE AS (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  RETENTION
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          64K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONTRATTO IS 'Tabella contenente le informazioni sui contratti stipulati presso un notaio o avvocato.';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.ID_CONTRATTO IS 'identificativo del contratto';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.DATA_INIZIO IS 'Indica la data di costituzione della convivenza; oppure indica la data di cessazione. 
';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.DATA_NOTIFICA IS 'indica la data di notifica del contratto o della risoluzione al comune
';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.DATA_DOCUMENTO IS 'Indica la data di sottoscrizione del contratto se si tratta di una stipula; oppure indica la data di risoluzione del contratto se si tratta di una risoluzione
';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.DOCUMENTO IS 'documento del contratto.';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.CHECK_DOCUMENTO IS ' indica se è stato processato tramite verifica antivirus il documento inviato
';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.FLG_NOTAIO_AVVOCATO IS 'N - NOTAIO
A - AVVOCATO';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.COGNOME_PROF IS 'Cognome del professionista che ha redatto il contratto';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.NOME_PROF IS 'Nome del professionista che ha redatto il contratto';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.EMAIL_PROF IS 'Email del professionista che ha redatto il contratto';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.TELEFONO_PROF IS 'Telefono del professionista che ha redatto il contratto';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.STUDIO_PROF IS 'Studio del professionista che ha redatto il contratto';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.COMUNE_STUDIO_PROF IS 'Comune di residenza dello studio  del professionista che ha redatto il contratto';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.LUOGO_ECCEZIONALE IS 'Descrizione del luogo eccezionale (luogo diverso da comune o località) in cui si è svolto l''evento. ';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.LOCALITA_ID IS 'località estera  in cui si è svolto l''evento. ';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.ID_COMUNE_REGISTRAZIONE IS 'indica il comune che protocolla il contratto o la sua risoluzione.
';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.ID_COMUNE_EVENTO IS 'identificativo del comune in cui si è svolto l''evento.';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.CODICE_TIPO_PROTOCOLLO IS 'identificativo dell''ente protocollante';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.NUMERO_PROTOCOLLO IS 'Campo che indica il numero del protocollo.';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.ANNO_PROTOCOLLO IS 'Campo che indica l''anno del protocollo.';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.NUMERO_PRATICA IS 'Campo che indica il numero della pratica.';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.ANNO_PRATICA IS 'Campo che indica il l''anno della pratica.';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.ID_STATO_PRATICA IS 'identificativo dello stato della pratica';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.DATA_PROTOCOLLO IS 'Data del protocollo del contratto';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.FLAG_TIPO_CONTRATTO IS 'A -> APERTURA, C -> CHIUSURA; identifica la tipologia di contratto';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.NUMERO_REPERTORIO_NOTARILE IS 'Numero del repertorio notarile';

COMMENT ON COLUMN ANAG_USR.CONTRATTO.COD_COMUNE_AGGIOR IS 'identificativo aggior del comune salvato in LUOGO_ECCEZIONALE';



CREATE UNIQUE INDEX ANAG_USR.CONTRATTO_PK ON ANAG_USR.CONTRATTO
(ID_CONTRATTO)
LOGGING
TABLESPACE SYSTEM
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            FREELISTS        1
            FREELIST GROUPS  1
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONTRATTO ADD (
  CONSTRAINT CONTRATTO_PK
  PRIMARY KEY
  (ID_CONTRATTO)
  USING INDEX ANAG_USR.CONTRATTO_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONTRATTO ADD (
  CONSTRAINT COMUNE_EVENTO_FK 
  FOREIGN KEY (ID_COMUNE_REGISTRAZIONE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT CONF_MOTIVAZIONE_CHIUSURA_FK2 
  FOREIGN KEY (ID_MOTIV_CHIUSURA) 
  REFERENCES ANAG_USR.CONF_MOTIVAZIONE_CHIUSURA (ID)
  ENABLE VALIDATE,
  CONSTRAINT CONF_STATO_PRATICA_FKV2 
  FOREIGN KEY (ID_STATO_PRATICA) 
  REFERENCES ANAG_USR.CONF_STATO_PRATICA (ID_STATO_PRATICA)
  ENABLE VALIDATE,
  CONSTRAINT CONF_TIPO_PROTOCOLLO_FKV2 
  FOREIGN KEY (CODICE_TIPO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_TIPO_PROTOCOLLO (CODICE_TIPO_PROTOCOLLO)
  ENABLE VALIDATE,
  CONSTRAINT CONTRATTO_FK 
  FOREIGN KEY (ID_CONTRATTO_ANNULLATO) 
  REFERENCES ANAG_USR.CONTRATTO (ID_CONTRATTO)
  ENABLE VALIDATE,
  CONSTRAINT DICHIARAZIONE_FK 
  FOREIGN KEY (ID_DICHIARAZIONE) 
  REFERENCES ANAG_USR.DICHIARAZIONE (ID_DICHIARAZIONE)
  ENABLE VALIDATE,
  CONSTRAINT LOCALITA_EVENTO_FK 
  FOREIGN KEY (LOCALITA_ID) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE,
  CONSTRAINT LUOGO_REGISTRAZIONE_FK 
  FOREIGN KEY (ID_COMUNE_EVENTO) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_MOTIVO_PROVENIENZA
(
  ID_MOTIVO           NUMBER                    NOT NULL,
  DESCRIZIONE_MOTIVO  VARCHAR2(250 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_PROVENIENZA.ID_MOTIVO IS 'Identificativo del motivo';

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_PROVENIENZA.DESCRIZIONE_MOTIVO IS 'Descrizione della motivazione.';



CREATE UNIQUE INDEX ANAG_USR.CONF_MOTIVO_PROVENIENZA_PK ON ANAG_USR.CONF_MOTIVO_PROVENIENZA
(ID_MOTIVO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_MOTIVO_PROVENIENZA ADD (
  CONSTRAINT CONF_MOTIVO_PROVENIENZA_PK
  PRIMARY KEY
  (ID_MOTIVO)
  USING INDEX ANAG_USR.CONF_MOTIVO_PROVENIENZA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.V_COMUNE_PROVINCIA
(
  ID_COMUNE        NUMBER                       NOT NULL,
  NOME_COMUNE      VARCHAR2(80 BYTE),
  ISTAT_COMUNE     VARCHAR2(6 BYTE),
  SIGLA_PROVINCIA  VARCHAR2(3 BYTE)             NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;
CREATE TABLE ANAG_USR.CONF_TIPO_USO_CERTIFICATO
(
  ID_TIPO_USO  NUMBER                           NOT NULL,
  CODICE_ANPR  NUMBER,
  DESCRIZIONE  VARCHAR2(300 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_USO_CERTIFICATO.ID_TIPO_USO IS 'Identificativo della conf tipo uso certificato';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_USO_CERTIFICATO.CODICE_ANPR IS 'Codice anpr relativo al tipo di uso del certificato';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_USO_CERTIFICATO.DESCRIZIONE IS 'Descrizione del tipo di uso del certificato';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_USO_CERTIFICATO_PK ON ANAG_USR.CONF_TIPO_USO_CERTIFICATO
(ID_TIPO_USO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_USO_CERTIFICATO ADD (
  CONSTRAINT CONF_TIPO_USO_CERTIFICATO_PK
  PRIMARY KEY
  (ID_TIPO_USO)
  USING INDEX ANAG_USR.CONF_TIPO_USO_CERTIFICATO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_CONF_CERT_ANPR
(
  ID_CONF_CERTIFICATO  NUMBER                   NOT NULL,
  ID_TIPO_CERT_ANPR    NUMBER                   NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.R_CONF_CERT_ANPR.ID_CONF_CERTIFICATO IS 'Identificativo dell id_conf_certificato';

COMMENT ON COLUMN ANAG_USR.R_CONF_CERT_ANPR.ID_TIPO_CERT_ANPR IS 'Identificativo dell id dei tipo certificato di ANPR';



CREATE UNIQUE INDEX ANAG_USR.R_CONF_CERT_ANPR_PK ON ANAG_USR.R_CONF_CERT_ANPR
(ID_CONF_CERTIFICATO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_CONF_CERT_ANPR ADD (
  CONSTRAINT R_CONF_CERT_ANPR_PK
  PRIMARY KEY
  (ID_CONF_CERTIFICATO)
  USING INDEX ANAG_USR.R_CONF_CERT_ANPR_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_CONF_CERT_ANPR ADD (
  CONSTRAINT R_CONF_CERT_ANPR_FK1 
  FOREIGN KEY (ID_CONF_CERTIFICATO) 
  REFERENCES ANAG_USR.CONF_CERTIFICATO (ID_CONF_CERTIFICATO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_CONF_CERT_CUMULATIVO
(
  ID_R_CONF_CERT_CUMULATIVO  NUMBER             NOT NULL,
  ID_CONF_CERTIFICATO        NUMBER             NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.R_CONF_CERT_CUMULATIVO IS 'Tabella che permette di ricostruire i singoli certificati all interno di un cumulativo';

COMMENT ON COLUMN ANAG_USR.R_CONF_CERT_CUMULATIVO.ID_R_CONF_CERT_CUMULATIVO IS 'identificativo della r_conf cert cumulativo';

COMMENT ON COLUMN ANAG_USR.R_CONF_CERT_CUMULATIVO.ID_CONF_CERTIFICATO IS 'identificativo della conf_ertificato';



CREATE UNIQUE INDEX ANAG_USR.CONF_CERT_CUMULATIVO_PK ON ANAG_USR.R_CONF_CERT_CUMULATIVO
(ID_R_CONF_CERT_CUMULATIVO, ID_CONF_CERTIFICATO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_CONF_CERT_CUMULATIVO ADD (
  CONSTRAINT CONF_CERT_CUMULATIVO_PK
  PRIMARY KEY
  (ID_R_CONF_CERT_CUMULATIVO, ID_CONF_CERTIFICATO)
  USING INDEX ANAG_USR.CONF_CERT_CUMULATIVO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_MOTIVO_ANNULLAMENTO_CARTA
(
  ID_MOTIVO_ANNULLAMENTO_CARTA  NUMBER          NOT NULL,
  DESCRIZIONE                   VARCHAR2(250 BYTE),
  ID_STATO_VALIDITA_CARTA       NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_ANNULLAMENTO_CARTA.ID_MOTIVO_ANNULLAMENTO_CARTA IS 'Il campo identifica l''id del tipo di annullamento della carta.';

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_ANNULLAMENTO_CARTA.DESCRIZIONE IS 'Descrizione del tipo di annullamento della carta d''identita.';

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_ANNULLAMENTO_CARTA.ID_STATO_VALIDITA_CARTA IS 'Identificativo dello stato della carta d''dentita.';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_ANNULLAMENTO_CAR_PK ON ANAG_USR.CONF_MOTIVO_ANNULLAMENTO_CARTA
(ID_MOTIVO_ANNULLAMENTO_CARTA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_MOTIVO_ANNULLAMENTO_CARTA ADD (
  CONSTRAINT CONF_TIPO_ANNULLAMENTO_CAR_PK
  PRIMARY KEY
  (ID_MOTIVO_ANNULLAMENTO_CARTA)
  USING INDEX ANAG_USR.CONF_TIPO_ANNULLAMENTO_CAR_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONF_MOTIVO_ANNULLAMENTO_CARTA ADD (
  CONSTRAINT ID_STATO_VALIDITA_CARTA_FK1 
  FOREIGN KEY (ID_STATO_VALIDITA_CARTA) 
  REFERENCES ANAG_USR.CONF_STATO_VALIDITA_CARTA (ID_STATO_VALIDITA_CARTA)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_CAPELLI_CI
(
  ID             NUMBER                         NOT NULL,
  DESCRIZIONE    VARCHAR2(10 BYTE),
  SESSO          CHAR(1 BYTE),
  CODICE_AGGIOR  NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_CAPELLI_CI.ID IS 'Identificativo della entry della conf.';

COMMENT ON COLUMN ANAG_USR.CONF_CAPELLI_CI.DESCRIZIONE IS 'Descrizione del colore dei capelli in base al valore del campo sesso.';

COMMENT ON COLUMN ANAG_USR.CONF_CAPELLI_CI.SESSO IS 'M maschio, F femmina. Se null valido per tutti i generi.';

COMMENT ON COLUMN ANAG_USR.CONF_CAPELLI_CI.CODICE_AGGIOR IS 'Codice aggior della entry.';



CREATE UNIQUE INDEX ANAG_USR.CONF_CAPELLI_CI_PK ON ANAG_USR.CONF_CAPELLI_CI
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_CAPELLI_CI ADD (
  CONSTRAINT CONF_CAPELLI_CI_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_CAPELLI_CI_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_OCCHI_CI
(
  ID             NUMBER                         NOT NULL,
  DESCRIZIONE    VARCHAR2(10 BYTE),
  CODICE_AGGIOR  NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_OCCHI_CI.ID IS 'Identificativo della entry della conf.';

COMMENT ON COLUMN ANAG_USR.CONF_OCCHI_CI.DESCRIZIONE IS 'Descrizione del colore degli occhi.';

COMMENT ON COLUMN ANAG_USR.CONF_OCCHI_CI.CODICE_AGGIOR IS 'Codice aggior della entry.';



CREATE UNIQUE INDEX ANAG_USR.CONF_OCCHI_CI_PK ON ANAG_USR.CONF_OCCHI_CI
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_OCCHI_CI ADD (
  CONSTRAINT CONF_OCCHI_CI_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_OCCHI_CI_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_CESS_MATRIMONIO
(
  ID_TIPO_CESS_MATRIMONIO  NUMBER               NOT NULL,
  DESCRIZIONE              VARCHAR2(50 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_TIPO_CESS_MATRIMONIO IS 'LA TABELLA DESCRIVE LE TIPOLOGIE DI CESSIONE DI UN MATRIMONIO. 
IDENTIFICATIVI PRESI DA ANPR';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_CESS_MATRIMONIO_PK ON ANAG_USR.CONF_TIPO_CESS_MATRIMONIO
(ID_TIPO_CESS_MATRIMONIO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_CESS_MATRIMONIO ADD (
  CONSTRAINT CONF_TIPO_CESS_MATRIMONIO_PK
  PRIMARY KEY
  (ID_TIPO_CESS_MATRIMONIO)
  USING INDEX ANAG_USR.CONF_TIPO_CESS_MATRIMONIO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_TRIBUNALE
(
  ID_TIPO_TRIBUNALE  NUMBER                     NOT NULL,
  DESCRIZIONE        VARCHAR2(80 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_TIPO_TRIBUNALE IS 'LA TABELLA CONTIENE LE TIPOLOGIE DI ENTI CHE EMETTONO SENTENZA DI ANNULLAMENTO ATTO
ID PRESI DA ANPR';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_TRIBUNALE_PK ON ANAG_USR.CONF_TIPO_TRIBUNALE
(ID_TIPO_TRIBUNALE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_TRIBUNALE ADD (
  CONSTRAINT CONF_TIPO_TRIBUNALE_PK
  PRIMARY KEY
  (ID_TIPO_TRIBUNALE)
  USING INDEX ANAG_USR.CONF_TIPO_TRIBUNALE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_INFO_PROTOCOLLO
(
  ID_INFO_PROTOCOLLO          NUMBER            NOT NULL,
  FUNZIONALITA                VARCHAR2(250 BYTE),
  CODICE_PROCEDURA_CHIAMANTE  VARCHAR2(50 BYTE),
  CODICE_DOCUMENTO            NUMBER,
  CODICE_MITTENTE             VARCHAR2(50 BYTE),
  CODICE_DESTINATARIO         VARCHAR2(20 BYTE),
  DOC_FISICO                  NUMBER,
  DOC_LOGICO                  NUMBER,
  DOC_SOTTOLOGICO             NUMBER,
  FLAG_RICEZIONE              NUMBER,
  COD_FUNZIONALITA            NUMBER,
  STRUT_PROTOCOLLO            VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_INFO_PROTOCOLLO_PK ON ANAG_USR.CONF_INFO_PROTOCOLLO
(ID_INFO_PROTOCOLLO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_INFO_PROTOCOLLO ADD (
  CONSTRAINT CONF_INFO_PROTOCOLLO_PK
  PRIMARY KEY
  (ID_INFO_PROTOCOLLO)
  USING INDEX ANAG_USR.CONF_INFO_PROTOCOLLO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_STRUTTURE_INFO_PROTOCOLLO
(
  ID_STRUTTURE_INTERNE_RC  NUMBER               NOT NULL,
  ID_INFO_PROTOCOLLO       NUMBER               NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.R_STRUTTURE_INFO_PROTOCOLL_PK ON ANAG_USR.R_STRUTTURE_INFO_PROTOCOLLO
(ID_STRUTTURE_INTERNE_RC, ID_INFO_PROTOCOLLO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_STRUTTURE_INFO_PROTOCOLLO ADD (
  CONSTRAINT R_STRUTTURE_INFO_PROTOCOLL_PK
  PRIMARY KEY
  (ID_STRUTTURE_INTERNE_RC, ID_INFO_PROTOCOLLO)
  USING INDEX ANAG_USR.R_STRUTTURE_INFO_PROTOCOLL_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_STRUTTURE_INFO_PROTOCOLLO ADD (
  CONSTRAINT R_STRUTTURE_INFO_PROT_INFO 
  FOREIGN KEY (ID_INFO_PROTOCOLLO) 
  REFERENCES ANAG_USR.CONF_INFO_PROTOCOLLO (ID_INFO_PROTOCOLLO)
  ENABLE VALIDATE,
  CONSTRAINT R_STRUTTURE_INFO_PROT_STRUT 
  FOREIGN KEY (ID_STRUTTURE_INTERNE_RC) 
  REFERENCES ANAG_USR.CONF_STRUTTURE_INTERNE_RC (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_ST_INT_POLIZIA
(
  ID_CONF_ST_INT_MUNICIPIO  NUMBER              NOT NULL,
  ID_CONF_ST_INT_POLIZIA    NUMBER              NOT NULL,
  ID_GRUPPO_PL              NUMBER              NOT NULL,
  ID_CONF_MUNICIPIO         NUMBER              NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_ST_INT_POLIZIA.ID_CONF_ST_INT_MUNICIPIO IS 'ID DEL MUNICIPIO DA ASSOCIARE AL GRUPPO DI POLIZIA';

COMMENT ON COLUMN ANAG_USR.CONF_ST_INT_POLIZIA.ID_CONF_ST_INT_POLIZIA IS 'CHIAVE PRIMARIA DELLA TABELLA DI RELAZIONE';

COMMENT ON COLUMN ANAG_USR.CONF_ST_INT_POLIZIA.ID_GRUPPO_PL IS 'ID GRUPPO POLIZIA DA ASSOCIRARE AL MUNICIPIO';

COMMENT ON COLUMN ANAG_USR.CONF_ST_INT_POLIZIA.ID_CONF_MUNICIPIO IS 'ID CONF_MUNICIPIO';



CREATE UNIQUE INDEX ANAG_USR.CONF_ST_INT_POLIZIA_PK ON ANAG_USR.CONF_ST_INT_POLIZIA
(ID_CONF_ST_INT_POLIZIA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_ST_INT_POLIZIA ADD (
  CONSTRAINT CONF_ST_INT_POLIZIA_PK
  PRIMARY KEY
  (ID_CONF_ST_INT_POLIZIA)
  USING INDEX ANAG_USR.CONF_ST_INT_POLIZIA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONF_ST_INT_POLIZIA ADD (
  CONSTRAINT CONF_ST_INT_POLIZIA_FK1 
  FOREIGN KEY (ID_CONF_MUNICIPIO) 
  REFERENCES ANAG_USR.CONF_MUNICIPIO (ID_MUNICIPIO)
  ENABLE VALIDATE,
  CONSTRAINT ID_GRUPPO_POL_FK 
  FOREIGN KEY (ID_GRUPPO_PL) 
  REFERENCES ANAG_USR.CONF_STRUTTURE_INTERNE_RC (ID)
  ENABLE VALIDATE,
  CONSTRAINT ID_MUNICIPIO_PL_FK 
  FOREIGN KEY (ID_CONF_ST_INT_MUNICIPIO) 
  REFERENCES ANAG_USR.CONF_STRUTTURE_INTERNE_RC (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_MODALITA_RILASCIO_CIE
(
  ID_CONF_MODALITA_RILASCIO_CIE  NUMBER         NOT NULL,
  DESCRIZIONE                    VARCHAR2(50 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_MODALITA_RILASCIO_CIE.ID_CONF_MODALITA_RILASCIO_CIE IS 'Il campo che identifica la modalita di rilascio CIE';

COMMENT ON COLUMN ANAG_USR.CONF_MODALITA_RILASCIO_CIE.DESCRIZIONE IS 'Descrizione della modalita di rilascio CIE';



CREATE UNIQUE INDEX ANAG_USR.CONF_MODALITA_RILASCIO_CIE_PK ON ANAG_USR.CONF_MODALITA_RILASCIO_CIE
(ID_CONF_MODALITA_RILASCIO_CIE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_MODALITA_RILASCIO_CIE ADD (
  CONSTRAINT CONF_MODALITA_RILASCIO_CIE_PK
  PRIMARY KEY
  (ID_CONF_MODALITA_RILASCIO_CIE)
  USING INDEX ANAG_USR.CONF_MODALITA_RILASCIO_CIE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_VACCINAZIONE
(
  ID_CONF_VACCINAZIONE  NUMBER                  NOT NULL,
  CODICE_VACC           VARCHAR2(50 BYTE),
  DESCRIZIONE           VARCHAR2(200 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_VACCINAZIONE.ID_CONF_VACCINAZIONE IS 'Identificativo della conf_vaccinazione';

COMMENT ON COLUMN ANAG_USR.CONF_VACCINAZIONE.CODICE_VACC IS 'Codice del vaccino ';

COMMENT ON COLUMN ANAG_USR.CONF_VACCINAZIONE.DESCRIZIONE IS 'Descrizione del vaccino';



CREATE UNIQUE INDEX ANAG_USR.CONF_VACCINAZIONE_PK ON ANAG_USR.CONF_VACCINAZIONE
(ID_CONF_VACCINAZIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_VACCINAZIONE ADD (
  CONSTRAINT CONF_VACCINAZIONE_PK
  PRIMARY KEY
  (ID_CONF_VACCINAZIONE)
  USING INDEX ANAG_USR.CONF_VACCINAZIONE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_MOTIVO_ANNULL_REVOCA_CIE
(
  ID_MOTIVO_ANN_REV_CIE    NUMBER               NOT NULL,
  DESCRIZIONE              VARCHAR2(250 BYTE),
  ID_STATO_VALIDITA_CARTA  NUMBER,
  CHK_REVOCA               VARCHAR2(1 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_ANNULL_REVOCA_CIE.ID_MOTIVO_ANN_REV_CIE IS 'Il campo che identifica la modalita di revoca CIE';

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_ANNULL_REVOCA_CIE.DESCRIZIONE IS 'Descrizione della modalita di revoca CIE';

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_ANNULL_REVOCA_CIE.ID_STATO_VALIDITA_CARTA IS 'Identificativo dello stato della carta identita CIE';

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_ANNULL_REVOCA_CIE.CHK_REVOCA IS 'Se settato ad S allora è revoca altrimenti annullamento emissione';



CREATE UNIQUE INDEX ANAG_USR.CONF_MOTIVO_ANN_REV_CIE_PK ON ANAG_USR.CONF_MOTIVO_ANNULL_REVOCA_CIE
(ID_MOTIVO_ANN_REV_CIE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_MOTIVO_ANNULL_REVOCA_CIE ADD (
  CONSTRAINT CONF_MOTIVO_ANN_REV_CIE_PK
  PRIMARY KEY
  (ID_MOTIVO_ANN_REV_CIE)
  USING INDEX ANAG_USR.CONF_MOTIVO_ANN_REV_CIE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONF_MOTIVO_ANNULL_REVOCA_CIE ADD (
  CONSTRAINT ID_STATO_VALIDITA_CARTA_FK 
  FOREIGN KEY (ID_STATO_VALIDITA_CARTA) 
  REFERENCES ANAG_USR.CONF_STATO_VALIDITA_CARTA (ID_STATO_VALIDITA_CARTA)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_RICHIESTA_RUOLI
(
  ID_TIPO_RICHIESTA  NUMBER                     NOT NULL,
  ID_RUOLO           NUMBER                     NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_RICHIESTA_RUOLI.ID_TIPO_RICHIESTA IS 'Identifica il tipo richiesta di un certificato';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_RICHIESTA_RUOLI.ID_RUOLO IS 'Identifica il tipo di ruolo abilitato pe quella richiesta';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_RICHIESTA_RUOLI_PK ON ANAG_USR.CONF_TIPO_RICHIESTA_RUOLI
(ID_TIPO_RICHIESTA, ID_RUOLO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_RICHIESTA_RUOLI ADD (
  CONSTRAINT CONF_TIPO_RICHIESTA_RUOLI_PK
  PRIMARY KEY
  (ID_TIPO_RICHIESTA, ID_RUOLO)
  USING INDEX ANAG_USR.CONF_TIPO_RICHIESTA_RUOLI_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.DOCUMENTO_SOGGETTO_CRI
(
  ID_DOCUMENTO                   NUMBER         NOT NULL,
  NOME_DOCUMENTO                 VARCHAR2(100 BYTE),
  PDF_DOCUMENTO                  BLOB,
  ID_CAMBIO_RESIDENZA_DOMICILIO  NUMBER,
  ID_SOGGETTO                    NUMBER,
  ID_TEMPLATE                    NUMBER,
  NUMERO_ALLEGATO                NUMBER
)
LOB (PDF_DOCUMENTO) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.DOCUMENTO_SOGGETTO_CRI.NOME_DOCUMENTO IS 'nome del file salvato';

COMMENT ON COLUMN ANAG_USR.DOCUMENTO_SOGGETTO_CRI.PDF_DOCUMENTO IS 'blob del file salvato';

COMMENT ON COLUMN ANAG_USR.DOCUMENTO_SOGGETTO_CRI.ID_CAMBIO_RESIDENZA_DOMICILIO IS 'identificativo della pratica di cambio residenza relativa al documento';

COMMENT ON COLUMN ANAG_USR.DOCUMENTO_SOGGETTO_CRI.ID_SOGGETTO IS 'identificativo del soggetto relativo al documento';

COMMENT ON COLUMN ANAG_USR.DOCUMENTO_SOGGETTO_CRI.ID_TEMPLATE IS 'identificativo del template relativo al documento';



CREATE UNIQUE INDEX ANAG_USR.DOCUMENTO_SOGGETTO_CRI_PK ON ANAG_USR.DOCUMENTO_SOGGETTO_CRI
(ID_DOCUMENTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.DOCUMENTO_SOGGETTO_CRI ADD (
  CONSTRAINT DOCUMENTO_SOGGETTO_CRI_PK
  PRIMARY KEY
  (ID_DOCUMENTO)
  USING INDEX ANAG_USR.DOCUMENTO_SOGGETTO_CRI_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.DOCUMENTO_SOGGETTO_CRI ADD (
  CONSTRAINT DOCUMENTO_SOGGETTO_CRI_FK1 
  FOREIGN KEY (ID_SOGGETTO, ID_CAMBIO_RESIDENZA_DOMICILIO) 
  REFERENCES ANAG_USR.R_SOGGETTO_CAMBIO_RESIDENZA (ID_SOGGETTO,ID_CAMBIO_RESIDENZA_DOMICILIO)
  DEFERRABLE INITIALLY DEFERRED
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.OPERATORI_ANPR
(
  CODICE_FISCALE       VARCHAR2(20 BYTE),
  ID_POSTAZIONE        VARCHAR2(20 BYTE),
  ABILITATO_NOTIFICHE  VARCHAR2(1 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.OPERATORI_ANPR.CODICE_FISCALE IS 'Codice fiscale dell''utente loggato in sessione ';

COMMENT ON COLUMN ANAG_USR.OPERATORI_ANPR.ID_POSTAZIONE IS 'Postazione associata all''operatore';

COMMENT ON COLUMN ANAG_USR.OPERATORI_ANPR.ABILITATO_NOTIFICHE IS 'Campo che indica operatore responsabile delle operazioni di notifica';
CREATE TABLE ANAG_USR.ANPR_DATI_FORNITURA
(
  VERSIONE_FORNITURA             VARCHAR2(20 BYTE) NOT NULL,
  TOTALE_INVII                   VARCHAR2(20 BYTE),
  NUMERO_TOTALE_SCHEDE_SOGGETTO  VARCHAR2(20 BYTE),
  N_TOT_CITTADINI_ITALIANI       VARCHAR2(20 BYTE),
  N_TOT_ISCRITTI_NON_ITALIANI    VARCHAR2(20 BYTE),
  N_TOT_PERSONE_SESSO_FEMMINILE  VARCHAR2(20 BYTE),
  N_TOT_PERSONE_SESSO_MASCHILE   VARCHAR2(20 BYTE),
  NUMERO_TOTALE_SCHEDE_FAMIGLIA  VARCHAR2(20 BYTE),
  N_TOT_SCHEDE_CONVIVENZA        VARCHAR2(20 BYTE),
  DATA_FORNITURA                 DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.ANPR_DATI_FORNITURA_PK ON ANAG_USR.ANPR_DATI_FORNITURA
(VERSIONE_FORNITURA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.ANPR_DATI_FORNITURA ADD (
  CONSTRAINT ANPR_DATI_FORNITURA_PK
  PRIMARY KEY
  (VERSIONE_FORNITURA)
  USING INDEX ANAG_USR.ANPR_DATI_FORNITURA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.V_LOCALITA_STATO_ESTERO
(
  ID_LOCALITA           NUMBER                  NOT NULL,
  DESCRIZIONE_LOCALITA  VARCHAR2(120 BYTE),
  DESCRIZIONE           VARCHAR2(20 BYTE),
  ID_STATO_ESTERO       VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;
CREATE TABLE ANAG_USR.ANPR_DATI_INVIO
(
  PROGRESSIVO_INVIO              VARCHAR2(250 BYTE),
  DATA_ESTRAZIONE                VARCHAR2(250 BYTE),
  NUMERO_SCHEDE_SOGGETTO_INVIO   VARCHAR2(250 BYTE),
  N_CITTADINI_ITALIANI_INVIO     VARCHAR2(250 BYTE),
  N_ISCRITTI_NON_ITALIANI_INVIO  VARCHAR2(250 BYTE),
  N_PERS_SESSO_F_INVIO           VARCHAR2(250 BYTE),
  N_PERS_SESSO_M_INVIO           VARCHAR2(250 BYTE),
  N_TOT_SCHEDE_FAMIGLIA_INVIO    VARCHAR2(250 BYTE),
  N_TOT_SCHEDE_CONVIVENZA_INVIO  VARCHAR2(250 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;
CREATE TABLE ANAG_USR.MV_ANPR_SOGGETTI
(
  ID_SOGGETTO                     NUMBER        NOT NULL,
  CODFISCALE                      VARCHAR2(16 BYTE),
  VALIDITACF                      NUMBER(2),
  DATAATTRIBUZIONEVALIDITA        DATE,
  COGNOME                         VARCHAR2(250 BYTE),
  NOME                            VARCHAR2(250 BYTE),
  SESSO                           CHAR(1 BYTE),
  DATANASCITA                     DATE,
  SENZAGIORNO                     CHAR(1 CHAR),
  SENZAGIORNOMESE                 CHAR(1 CHAR),
  LUOGOECCEZIONALE                VARCHAR2(50 CHAR),
  NOMECOMUNE                      VARCHAR2(80 BYTE),
  CODICEISTAT                     VARCHAR2(6 BYTE),
  SIGLAPROVISTAT                  VARCHAR2(3 BYTE),
  COMUNE_DESCRIZIONELOC           VARCHAR2(10 BYTE),
  LOCALITA_DESCRIZIONELOC         VARCHAR2(120 BYTE),
  DESCRIZIONESTATO_NASCITA        VARCHAR2(20 BYTE),
  CODICESTATO_NASCITA             NUMBER,
  PROVINCIACONTEA                 VARCHAR2(10 BYTE),
  SOGGETTOAIRE                    VARCHAR2(1 BYTE),
  IDSCHEDASOGGETTOCOMUNEISTAT     VARCHAR2(10 BYTE),
  IDSCHEDASOGGETTO                VARCHAR2(20 BYTE),
  IDSCHEDASOGGETTOANPR            VARCHAR2(10 BYTE),
  DATAPRIMAISCRIZIONECOMUNE       DATE,
  STATOCIVILE                     NUMBER(2),
  NOTESTATOCIVILE                 VARCHAR2(250 BYTE),
  STATOCIVILEND                   VARCHAR2(10 BYTE),
  SENZAFISSADIMORA                VARCHAR2(1 BYTE),
  SOGGETTOCERTIFICABILE           NUMBER,
  DATAULTIMOAGGIORNAMENTO         DATE,
  MOTIVOISCRIZIONEAPR             NUMBER(2),
  COMUNEREG_NOMECOMUNE            VARCHAR2(80 BYTE),
  COMUNEREG_CODICEISTAT           VARCHAR2(6 BYTE),
  COMUNEREG_SIGLAPROVINCIAISTAT   VARCHAR2(3 BYTE),
  COMUNEREG_DESCRIZIONELOCALITA   VARCHAR2(10 BYTE),
  UFFICIOMUNICIPIO                VARCHAR2(50 BYTE),
  ANNO                            NUMBER(4),
  PARTE                           VARCHAR2(5 BYTE),
  SERIE                           VARCHAR2(10 BYTE),
  NUMEROATTO                      VARCHAR2(20 BYTE),
  VOLUME                          VARCHAR2(5 BYTE),
  DATAFORMAZIONEATTO              DATE,
  TRASCRITTO                      NUMBER,
  DESCRIZIONESTATO_ATTONASC       VARCHAR2(250 BYTE),
  CODICESTATO_ATTONASC            NUMBER(3),
  NOTESTATO                       VARCHAR2(250 BYTE),
  DATAVALIDITA                    DATE,
  PATERNITA_CODFISCALE            VARCHAR2(16 BYTE),
  PATERNITA_VALIDITACF            NUMBER(2),
  PATERNITA_DATAATTRVALIDITA      DATE,
  PATERNITA_COGNOME               VARCHAR2(250 BYTE),
  PATERNITA_NOME                  VARCHAR2(250 BYTE),
  PATERNITA_SESSO                 CHAR(1 BYTE),
  PATERNITA_DATANASCITA           DATE,
  PATERNITA_SENZAGIORNO           CHAR(1 CHAR),
  PATERNITA_SENZAGIORNOMESE       CHAR(1 CHAR),
  PATERNITA_LUOGOECCEZIONALE      VARCHAR2(50 CHAR),
  PATERNITA_NOMECOMUNE            VARCHAR2(80 BYTE),
  PATERNITA_CODICEISTAT           VARCHAR2(6 BYTE),
  PATERNITA_SIGLAPROVINCIAISTAT   VARCHAR2(3 BYTE),
  PATERNITA_COMUNEDESLOCALITA     VARCHAR2(10 BYTE),
  PATERNITA_LOCALITADESLOCALITA   VARCHAR2(120 BYTE),
  PATERNITA_DESSTATO_NASCITA      VARCHAR2(20 BYTE),
  PATERNITA_CODICESTATO_NASCITA   NUMBER,
  PATERNITA_PROVINCIACONTEA       VARCHAR2(10 BYTE),
  PATERNITA_SOGGETTOAIRE          VARCHAR2(1 BYTE),
  PATERNITA_ANNOESPATRIO          NUMBER(4),
  PATERNITA_IDSCSOGGCOMUNEISTAT   VARCHAR2(10 BYTE),
  PATERNITA_IDSCHEDASOGGETTO      VARCHAR2(20 BYTE),
  PATERNITA_IDSCSOGGETTOANPR      NUMBER(15),
  PATERNITA_NOTE                  VARCHAR2(10 BYTE),
  PATERNITA_STATOCIVILE           NUMBER(2),
  PATERNITA_NOTESTATOCIVILE       VARCHAR2(250 BYTE),
  PATERNITA_STATOCIVILEND         VARCHAR2(10 BYTE),
  PATERNITA_DESCRIZIONESTATO      VARCHAR2(250 BYTE),
  PATERNITA_CODICESTATO           NUMBER(3),
  PATERNITA_NOTESTATO             VARCHAR2(250 BYTE),
  PATERNITA_DATAVALIDITA          DATE,
  PATERNITA_POSIZIONEPROF         NUMBER(2),
  PATERNITA_CONDIZIONENONPROF     NUMBER(2),
  PATERNITA_TITOLOSTUDIO          NUMBER(2),
  MATERNITA_CODFISCALE            VARCHAR2(16 BYTE),
  MATERNITA_VALIDITACF            NUMBER(2),
  MATERNITA_DATAATTRVALIDITA      DATE,
  MATERNITA_COGNOME               VARCHAR2(250 BYTE),
  MATERNITA_NOME                  VARCHAR2(250 BYTE),
  MATERNITA_SESSO                 CHAR(1 BYTE),
  MATERNITA_DATANASCITA           DATE,
  MATERNITA_SENZAGIORNO           CHAR(1 CHAR),
  MATERNITA_SENZAGIORNOMESE       CHAR(1 CHAR),
  MATERNITA_LUOGOECCEZIONALE      VARCHAR2(50 CHAR),
  MATERNITA_NOMECOMUNE            VARCHAR2(80 BYTE),
  MATERNITA_CODICEISTAT           VARCHAR2(6 BYTE),
  MATERNITA_SIGLAPROVINCIAISTAT   VARCHAR2(3 BYTE),
  MATERNITA_COMUNEDESLOCALITA     VARCHAR2(10 BYTE),
  MATERNITA_LOCALITADESLOCALITA   VARCHAR2(120 BYTE),
  MATERNITA_DESSTATO_NASCITA      VARCHAR2(20 BYTE),
  MATERNITA_CODICESTATO_NASCITA   NUMBER,
  MATERNITA_PROVINCIACONTEA       VARCHAR2(10 BYTE),
  MATERNITA_SOGGETTOAIRE          CHAR(1 BYTE),
  MATERNITA_ANNOESPATRIO          NUMBER(4),
  MATERNITA_IDSCSOGGCOMUNEISTAT   VARCHAR2(10 BYTE),
  MATERNITA_IDSCHEDASOGGETTO      VARCHAR2(20 BYTE),
  MATERNITA_IDSCSOGGETTOANPR      NUMBER(15),
  MATERNITA_NOTE                  VARCHAR2(10 BYTE),
  MATERNITA_STATOCIVILE           NUMBER(2),
  MATERNITA_NOTESTATOCIVILE       VARCHAR2(250 BYTE),
  MATERNITA_STATOCIVILEND         VARCHAR2(10 BYTE),
  MATERNITA_DESCRIZIONESTATO      VARCHAR2(250 BYTE),
  MATERNITA_CODICESTATO           NUMBER(3),
  MATERNITA_NOTESTATO             VARCHAR2(250 BYTE),
  MATERNITA_DATAVALIDITA          DATE,
  MATERNITA_POSIZIONEPROF         NUMBER(2),
  MATERNITA_CONDIZIONENONPROF     NUMBER(2),
  MATERNITA_TITOLOSTUDIO          NUMBER(2),
  TIPOINDIRIZZO                   NUMBER(2),
  NOTEINDIRIZZO                   VARCHAR2(250 BYTE),
  INDIRIZZO_CAP                   VARCHAR2(20 CHAR),
  INDIRIZZO_NOMECOMUNE            VARCHAR2(10 BYTE),
  INDIRIZZO_CODICEISTAT           VARCHAR2(10 BYTE),
  INDIRIZZO_SIGLAPROVINCIAISTAT   VARCHAR2(10 BYTE),
  DESCRIZIONELOCALITA             VARCHAR2(10 BYTE),
  FRAZIONE                        VARCHAR2(10 BYTE),
  TOPONIMO_CODSPECIE              NUMBER(4),
  TOPONIMO_SPECIE                 VARCHAR2(30 BYTE),
  TOPONIMO_SPECIEFONTE            NUMBER(1),
  TOPONIMO_CODTOPONIMO            VARCHAR2(6 BYTE),
  TOPONIMO_DENOMINAZIONETOP       VARCHAR2(50 BYTE),
  TOPONIMO_TOPONIMOFONTE          NUMBER(1),
  CODICECIVICO                    VARCHAR2(10 BYTE),
  CIVICOFONTE                     NUMBER(1),
  NUMERO                          NUMBER(20),
  PROGSNC                         NUMBER(5),
  LETTERA                         VARCHAR2(10 BYTE),
  ESPONENTE1                      VARCHAR2(20 BYTE),
  COLORE                          NUMBER(1),
  CORTE                           VARCHAR2(4 BYTE),
  SCALA                           VARCHAR2(4 BYTE),
  INTERNO                         VARCHAR2(4 BYTE),
  ESPINTERNO1                     VARCHAR2(20 BYTE),
  INTERNO2                        VARCHAR2(4 BYTE),
  ESPINTERNO2                     VARCHAR2(20 BYTE),
  SCALAESTERNA                    VARCHAR2(10 BYTE),
  SECONDARIO                      CHAR(1 BYTE),
  PIANO                           VARCHAR2(5 BYTE),
  NUI                             VARCHAR2(3 BYTE),
  ISOLATO                         VARCHAR2(10 BYTE),
  PRESSO                          VARCHAR2(10 BYTE),
  DATADECORRENZARESIDENZA         DATE,
  FAMIGLIA_IDFAMCONVCOMUNE        VARCHAR2(20 CHAR),
  FAMIGLIA_TIPOLEGAME             NUMBER,
  FAMIGLIA_DATADECORRENZA         DATE,
  FAMIGLIA_CODICELEGAME           NUMBER,
  FAMIGLIA_PROGRCOMPONENTE        NUMBER,
  FAMIGLIA_DATADECORRENZALEGAME   DATE,
  CONVIVENZA_IDFAMCONVCOMUNE      VARCHAR2(20 CHAR),
  CONVIVENZA_TIPOLEGAME           NUMBER,
  CONVIVENZA_DATADECORRENZA       DATE,
  CONVIVENZA_CODICELEGAME         NUMBER,
  CONVIVENZA_PROGRCOMPONENTE      NUMBER,
  CONVIVENZA_DATADECOLEGAME       DATE,
  CI_NUMERO                       VARCHAR2(20 BYTE),
  CI_DATARILASCIO                 DATE,
  CI_CARTACEAELETTRONICA          VARCHAR2(1 BYTE),
  CI_INTERDIZIONEESPATRIO         CHAR(1 BYTE),
  CI_NOMECOMUNE                   VARCHAR2(80 BYTE),
  CI_CODICEISTAT                  VARCHAR2(6 BYTE),
  CI_SIGLAPROVINCIAISTAT          VARCHAR2(3 BYTE),
  CI_DESCRIZIONELOCALITA          VARCHAR2(10 BYTE),
  CI_DATASCADENZA                 DATE,
  PS_NUMEROSOGGIORNO              VARCHAR2(20 BYTE),
  PS_TIPOSOGGIORNO                VARCHAR2(2 BYTE),
  PS_NOTESOGGIORNO                VARCHAR2(250 BYTE),
  PS_DATARILASCIO                 DATE,
  PS_DATASCADENZA                 DATE,
  PS_QUESTURARILASCIOSOGGIORNO    VARCHAR2(100 BYTE),
  PS_NOMECOMUNE                   VARCHAR2(80 BYTE),
  PS_CODICEISTAT                  VARCHAR2(6 BYTE),
  PERMSOGG_SIGLAPROVINCIAISTAT    VARCHAR2(3 BYTE),
  PERMSOGG_COMUNEDESLOCALITA      VARCHAR2(10 BYTE),
  PS_NUMEROPASSAPORTO             VARCHAR2(30 BYTE),
  ELETT_ELETTORE                  VARCHAR2(1 BYTE),
  ELETT_NOMECOMUNE                VARCHAR2(80 BYTE),
  ELETT_CODICEISTAT               VARCHAR2(6 BYTE),
  ELETT_SIGLAPROVINCIAISTAT       VARCHAR2(3 BYTE),
  ELETT_COMUNEDESCLOCALITA        VARCHAR2(10 BYTE),
  LEVA_ISCRITTO                   VARCHAR2(1 BYTE),
  LEVA_NOMECOMUNE                 VARCHAR2(80 BYTE),
  LEVA_CODICEISTAT                VARCHAR2(6 BYTE),
  LEVA_SIGLAPROVISTAT             VARCHAR2(3 BYTE),
  LEVA_COMUNEDESLOCALITA          VARCHAR2(10 BYTE),
  ANNOCENSIMENTO                  NUMBER(4),
  SEZIONECENSIMENTO               VARCHAR2(30 BYTE),
  FOGLIOCENSIMENTO                VARCHAR2(30 BYTE),
  DATAREGOLARIZZAZIONE            DATE,
  MOTIVOCOMPILAZIONE              VARCHAR2(240 BYTE),
  POSSESSOAUTOVEICOLI             VARCHAR2(1 BYTE),
  POSSESSOPATENTE                 VARCHAR2(1 BYTE),
  SOGGETTO_POSIZIONEPROF          NUMBER(2),
  SOGGETTO_CONDIZIONENONPROF      NUMBER(2),
  SOGGETTO_TITOLOSTUDIO           NUMBER(2),
  ALTRACITT_DESCRIZIONESTATO      VARCHAR2(250 BYTE),
  ALTRACITT_CODICESTATO           NUMBER(3),
  ALTRACITTADINANZA_NOTESTATO     VARCHAR2(250 BYTE),
  ALTRACITT_DATAVALIDITA          DATE,
  FAMIGLIA_IDFAMCONVCOMUNEISTAT   VARCHAR2(10 BYTE),
  FAMIGLIA_IDFAMCONV              VARCHAR2(20 CHAR),
  FAMIGLIA_IDFAMCONVANPR          VARCHAR2(10 BYTE),
  FAMIGLIA_FAMIGLIAAIRE           VARCHAR2(10 BYTE),
  FAMIGLIA_DATAORIGINEFAMCONV     DATE,
  FAMIGLIA_MOTIVOCOSTITUZIONE     NUMBER,
  FAMIGLIA_DENOMINAZIONECONV      VARCHAR2(10 BYTE),
  FAMIGLIA_SPECIECONVIVENZA       VARCHAR2(10 BYTE),
  FAMIGLIA_TIPOMOVIMENTAZIONE     NUMBER,
  FAMIGLIA_PRESENZAFAMCOABIT      VARCHAR2(10 BYTE),
  FAMIGLIA_TIPOSCHEDA             NUMBER,
  TUTOREINTESTF_CODFISCALE        VARCHAR2(16 BYTE),
  TUTOREINTESTF_VALIDITACF        NUMBER(2),
  TUTINTESTF_DATAATTRVALIDITA     DATE,
  TUTOREINTESTATARIOF_COGNOME     VARCHAR2(250 BYTE),
  TUTOREINTESTATARIOF_NOME        VARCHAR2(250 BYTE),
  TUTOREINTESTATARIOF_SESSO       CHAR(1 BYTE),
  TUTOREINTESTF_DATANASCITA       DATE,
  TUTOREINTESTF_SENZAGIORNO       CHAR(1 CHAR),
  TUTOREINTESTF_SENZAGIORNOMESE   CHAR(1 CHAR),
  TUTOREINTESTF_LUOGOECCEZIONALE  VARCHAR2(50 CHAR),
  TUTOREINTESTF_NOMECOMUNE        VARCHAR2(80 BYTE),
  TUTOREINTESTF_CODICEISTAT       VARCHAR2(6 BYTE),
  TUTOREINTESTF_SIGLAPROVISTAT    VARCHAR2(3 BYTE),
  TUTOREINTESTF_COMUNEDESLOCAL    VARCHAR2(10 BYTE),
  TUTOREINTESTF_LOCALITADESLOCAL  VARCHAR2(120 BYTE),
  TUTOREINTESTF_DESSTATO_NASCITA  VARCHAR2(20 BYTE),
  TUTOREINTESTF_CODSTATO_NASCITA  NUMBER,
  TUTOREINTESTF_PROVCONTEA        VARCHAR2(10 BYTE),
  TUTOREINTESTF_SOGGETTOAIRE      VARCHAR2(1 BYTE),
  TUTOREINTESTF_ANNOESPATRIO      NUMBER(4),
  TUTINTESTF_IDSCSOGGCOMUNEISTAT  CHAR(6 BYTE),
  TUTOREINTESTF_IDSCSOGGETTO      VARCHAR2(20 BYTE),
  TUTOREINTESTF_IDSCSOGGANPR      VARCHAR2(10 BYTE),
  TUTOREINTESTATARIOF_NOTE        VARCHAR2(10 BYTE),
  TUTINTESTF_NOMECOMUNERESIDENZA  VARCHAR2(80 BYTE),
  TUTINTESTF_CODISTATRESIDENZA    VARCHAR2(6 BYTE),
  TUTINTESTF_SIGLAPROVISTATRESID  VARCHAR2(3 BYTE),
  TUTINTF_COMUNEDESLOCALITARESID  VARCHAR2(10 BYTE),
  DATAINTESTARIOCONVIVENZAFAM     DATE,
  CONVIVENZAIDFAMCONVCOMUNEISTAT  VARCHAR2(10 BYTE),
  CONVIVENZA_IIDFAMCONV           VARCHAR2(20 CHAR),
  CONVIVENZA_IDFAMCONVIANPR       VARCHAR2(10 BYTE),
  CONVIVENZA_FAMIGLIAAIRE         VARCHAR2(10 BYTE),
  CONVIVENZA_DATAORIGINEFAMCONV   DATE,
  CONVIVENZA_MOTIVOCOSTITUZIONE   NUMBER,
  CONVIVENZA_DENOMINAZIONECONV    VARCHAR2(100 BYTE),
  CONVIVENZA_SPECIECONVIVENZA     NUMBER,
  CONVIVENZA_TIPOMOVIMENTAZIONE   NUMBER,
  CONVIVENZA_PRESENZAFAMCOAB      VARCHAR2(10 BYTE),
  CONVIVENZA_TIPOSCHEDA           NUMBER,
  TUTOREINTESTC_CODFISCALE        VARCHAR2(16 BYTE),
  TUTOREINTESTC_VALIDITACF        NUMBER(2),
  TUTOREINTESTC_DATAATTRVALIDITA  DATE,
  TUTOREINTESTATARIOC_COGNOME     VARCHAR2(250 BYTE),
  TUTOREINTESTATARIOC_NOME        VARCHAR2(250 BYTE),
  TUTOREINTESTATARIOC_SESSO       CHAR(1 BYTE),
  TUTOREINTESTC_DATANASCITA       DATE,
  TUTOREINTESTC_SENZAGIORNO       CHAR(1 CHAR),
  TUTOREINTESTC_SENZAGIORNOMESE   CHAR(1 CHAR),
  TUTOREINTESTC_LUOGOECCEZ        VARCHAR2(50 CHAR),
  TUTOREINTESTC_NOMECOMUNE        VARCHAR2(80 BYTE),
  TUTOREINTESTC_CODICEISTAT       VARCHAR2(6 BYTE),
  TUTOREINTESTC_SIGLAPROVISTAT    VARCHAR2(3 BYTE),
  TUTOREINTESTC_COMUNEDESLOCAL    VARCHAR2(10 BYTE),
  TUTOREINTESTC_LOCALITADESLOCAL  VARCHAR2(120 BYTE),
  TUTOREINTESTC_DESCSTATONASCITA  VARCHAR2(20 BYTE),
  TUTOREINTESTC_CODSTATONASCITA   NUMBER,
  TUTOREINTESTC_PROVINCIACONTEA   VARCHAR2(10 BYTE),
  TUTOREINTESTC_SOGGETTOAIRE      VARCHAR2(1 BYTE),
  TUTOREINTESTC_ANNOESPATRIO      NUMBER(4),
  TUTINTESTC_IDSCSOGGCOMUNEISTAT  CHAR(6 BYTE),
  TUTOREINTESTC_IDSCHEDASOGGETTO  VARCHAR2(20 BYTE),
  TUTOREINTESTC_IDSCSOGGANPR      VARCHAR2(10 BYTE),
  TUTOREINTESTATARIOC_NOTE        VARCHAR2(10 BYTE),
  TUTINTESTC_NOMECOMUNERESIDENZA  VARCHAR2(80 BYTE),
  TUTINTESTC_CODICEISTATRESID     VARCHAR2(6 BYTE),
  TUTINTESTC_SIGLAPROVISTATRESID  VARCHAR2(3 BYTE),
  TUTINTESTC_COMUNEDESLOCALRESID  VARCHAR2(10 BYTE),
  DATAINTESTARIOCONVIVENZACONV    DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;
CREATE TABLE ANAG_USR.CONF_TIPO_SCIOGLIMENTO_UNIONE
(
  ID_TIPO_SCIOGLIMENTO_UNIONE  NUMBER           NOT NULL,
  DESCRIZIONE                  VARCHAR2(50 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_SCIOGLIMENTO_UNI_PK ON ANAG_USR.CONF_TIPO_SCIOGLIMENTO_UNIONE
(ID_TIPO_SCIOGLIMENTO_UNIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_SCIOGLIMENTO_UNIONE ADD (
  CONSTRAINT CONF_TIPO_SCIOGLIMENTO_UNI_PK
  PRIMARY KEY
  (ID_TIPO_SCIOGLIMENTO_UNIONE)
  USING INDEX ANAG_USR.CONF_TIPO_SCIOGLIMENTO_UNI_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.RIPRISTINO
(
  ID_RIPRISTINO       NUMBER                    NOT NULL,
  ID_SOGGETTO         NUMBER,
  ID_TIPO_RIPRISTINO  NUMBER,
  ID_PRATICA          NUMBER,
  DATA_RIPRISTINO     VARCHAR2(20 BYTE),
  ID_UTENTE           NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.RIPRISTINO.ID_RIPRISTINO IS 'Identificativo del ripristino';

COMMENT ON COLUMN ANAG_USR.RIPRISTINO.ID_SOGGETTO IS 'Identificativo del soggetto ripristinato';

COMMENT ON COLUMN ANAG_USR.RIPRISTINO.ID_TIPO_RIPRISTINO IS 'Tipologia di ripristino';

COMMENT ON COLUMN ANAG_USR.RIPRISTINO.ID_PRATICA IS 'Identificativo della pratica in base al tipo di ripristino';

COMMENT ON COLUMN ANAG_USR.RIPRISTINO.DATA_RIPRISTINO IS 'Data in cui è stato effettuato il ripristino';

COMMENT ON COLUMN ANAG_USR.RIPRISTINO.ID_UTENTE IS 'Utente che ha effettuato il ripristino';



CREATE UNIQUE INDEX ANAG_USR.RIPRISTINO_PK ON ANAG_USR.RIPRISTINO
(ID_RIPRISTINO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.RIPRISTINO ADD (
  CONSTRAINT RIPRISTINO_PK
  PRIMARY KEY
  (ID_RIPRISTINO)
  USING INDEX ANAG_USR.RIPRISTINO_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.RIPRISTINO ADD (
  CONSTRAINT RIPRISTINO_FK1 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT RIPRISTINO_FK2 
  FOREIGN KEY (ID_TIPO_RIPRISTINO) 
  REFERENCES ANAG_USR.CONF_TIPO_RIPRISTINO (ID_TIPO_RIPRISTINO)
  ENABLE VALIDATE,
  CONSTRAINT RIPRISTINO_FK3 
  FOREIGN KEY (ID_UTENTE) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_RIPRISTINO
(
  ID_TIPO_RIPRISTINO  NUMBER                    NOT NULL,
  DESCRIZIONE         VARCHAR2(200 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_RIPRISTINO.ID_TIPO_RIPRISTINO IS 'Identificativo del tipo ripristino';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_RIPRISTINO.DESCRIZIONE IS 'Descrizione del tipo di ripristino';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_RIPRISTINO_PK ON ANAG_USR.CONF_TIPO_RIPRISTINO
(ID_TIPO_RIPRISTINO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_RIPRISTINO ADD (
  CONSTRAINT CONF_TIPO_RIPRISTINO_PK
  PRIMARY KEY
  (ID_TIPO_RIPRISTINO)
  USING INDEX ANAG_USR.CONF_TIPO_RIPRISTINO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.MV_COMUNE_PROVINCIA
(
  ID_COMUNE         NUMBER                      NOT NULL,
  NOME_COMUNE       VARCHAR2(80 BYTE),
  ISTAT_COMUNE      VARCHAR2(6 BYTE),
  CODICE_AGGIOR     VARCHAR2(5 BYTE),
  DATA_CESSAZIONE   DATE,
  DATA_ISTITUZIONE  DATE,
  ID_PROVINCIA      NUMBER                      NOT NULL,
  SIGLA_PROVINCIA   VARCHAR2(3 BYTE)            NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;
CREATE TABLE ANAG_USR.LOG_EVENTI_STATO_CIVILE
(
  TIPO_EVENTO         VARCHAR2(50 BYTE),
  TIPO_ERRORE         VARCHAR2(1 BYTE),
  DESCRIZIONE_ERRORE  VARCHAR2(2000 BYTE),
  CODICE_INDIVIDUALE  VARCHAR2(20 BYTE),
  ID_OPERAZIONE_ANPR  NUMBER,
  DATA_ERRORE         DATE,
  ID_LOG_EVENTI       NUMBER                    NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.LOG_EVENTI_STATO_CIVILE.TIPO_EVENTO IS 'Indica il tipo evento ';

COMMENT ON COLUMN ANAG_USR.LOG_EVENTI_STATO_CIVILE.TIPO_ERRORE IS 'A-> indica un errore di ANPR, S-> indica un errore SIPO';

COMMENT ON COLUMN ANAG_USR.LOG_EVENTI_STATO_CIVILE.DESCRIZIONE_ERRORE IS 'Viene indicata la tipologia di errore relativa all exception';

COMMENT ON COLUMN ANAG_USR.LOG_EVENTI_STATO_CIVILE.CODICE_INDIVIDUALE IS 'Indica il codice individuale della persona per cui è andata in errore la procedura di batch';

COMMENT ON COLUMN ANAG_USR.LOG_EVENTI_STATO_CIVILE.ID_OPERAZIONE_ANPR IS 'Indica l operazione anpr per cui è andata in errore la procedura di batch';

COMMENT ON COLUMN ANAG_USR.LOG_EVENTI_STATO_CIVILE.DATA_ERRORE IS 'Indica la data in cui è andata in errore il batch';

COMMENT ON COLUMN ANAG_USR.LOG_EVENTI_STATO_CIVILE.ID_LOG_EVENTI IS 'Identificativo della tabella';



CREATE UNIQUE INDEX ANAG_USR.LOG_EVENTI_STATO_CIVILE_PK ON ANAG_USR.LOG_EVENTI_STATO_CIVILE
(ID_LOG_EVENTI)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.LOG_EVENTI_STATO_CIVILE ADD (
  CONSTRAINT LOG_EVENTI_STATO_CIVILE_PK
  PRIMARY KEY
  (ID_LOG_EVENTI)
  USING INDEX ANAG_USR.LOG_EVENTI_STATO_CIVILE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_CODICE_INDIVIDUALE
(
  ID                NUMBER                      NOT NULL,
  FLAG_OCCASIONALE  CHAR(1 BYTE),
  PARTE_INIZIALE    NUMBER(1),
  ESADECIMALE       CHAR(1 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_CODICE_INDIVIDUALE.ID IS 'Identificativo incrementale di tabella';

COMMENT ON COLUMN ANAG_USR.CONF_CODICE_INDIVIDUALE.FLAG_OCCASIONALE IS 'N -> Residente/AIRE, S -> Occasionale';

COMMENT ON COLUMN ANAG_USR.CONF_CODICE_INDIVIDUALE.PARTE_INIZIALE IS 'Prima cifra numerica del codice individuale';

COMMENT ON COLUMN ANAG_USR.CONF_CODICE_INDIVIDUALE.ESADECIMALE IS 'Seconda cifra alfanumerica del codice';



CREATE UNIQUE INDEX ANAG_USR.CONF_CODICE_INDIVIDUALE_PK ON ANAG_USR.CONF_CODICE_INDIVIDUALE
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_CODICE_INDIVIDUALE ADD (
  CONSTRAINT CONF_CODICE_INDIVIDUALE_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_CODICE_INDIVIDUALE_PK
  ENABLE VALIDATE);

GRANT SELECT, UPDATE ON ANAG_USR.CONF_CODICE_INDIVIDUALE TO MATR_USR;
CREATE TABLE ANAG_USR.LOG_GENERA_CODICI
(
  ID                  NUMBER                    NOT NULL,
  ID_SOGGETTO         NUMBER,
  ID_FAMIGLIA         NUMBER,
  CODICE              VARCHAR2(20 BYTE),
  DESCRIZIONE_ERRORE  VARCHAR2(1000 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.LOG_GENERA_CODICI.ID IS 'Identificativo incrementale di tabella';

COMMENT ON COLUMN ANAG_USR.LOG_GENERA_CODICI.ID_SOGGETTO IS 'Identificativo del soggetto';

COMMENT ON COLUMN ANAG_USR.LOG_GENERA_CODICI.ID_FAMIGLIA IS 'Identificativo della famiglia';

COMMENT ON COLUMN ANAG_USR.LOG_GENERA_CODICI.CODICE IS 'Codice Individuale/Famiglia';



CREATE UNIQUE INDEX ANAG_USR.LOG_GENERA_CODICI_PK ON ANAG_USR.LOG_GENERA_CODICI
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.LOG_GENERA_CODICI ADD (
  CONSTRAINT LOG_GENERA_CODICI_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.LOG_GENERA_CODICI_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.PROCEDURA_URGENZA
(
  ID              NUMBER(10)                    DEFAULT "ANAG_USR"."ISEQ$$_144218".nextval NOT NULL,
  DESCRIZIONE     VARCHAR2(200 BYTE),
  ID_UTENTE       NUMBER(10),
  DATA            DATE,
  NOTE            VARCHAR2(400 BYTE),
  DODUMENTO       BLOB,
  NOME_DOCUMENTO  VARCHAR2(200 BYTE)
)
LOB (DODUMENTO) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.PROCEDURA_URGENZA_PK ON ANAG_USR.PROCEDURA_URGENZA
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.PROCEDURA_URGENZA ADD (
  CONSTRAINT PROCEDURA_URGENZA_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.PROCEDURA_URGENZA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_ATTIVITA_URGENZA
(
  ID                 NUMBER(10)                 DEFAULT "ANAG_USR"."ISEQ$$_144223".nextval NOT NULL,
  ID_CONF_STRUTTURA  NUMBER(20),
  FLGATTIVO          VARCHAR2(50 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


--  There is no statement for index ANAG_USR.SYS_C0014230.
--  The object is created when the parent object is created.

ALTER TABLE ANAG_USR.R_ATTIVITA_URGENZA ADD (
  PRIMARY KEY
  (ID)
  USING INDEX
    TABLESPACE ANAG_USR
    PCTFREE    10
    INITRANS   2
    MAXTRANS   255
    STORAGE    (
                INITIAL          64K
                NEXT             1M
                MINEXTENTS       1
                MAXEXTENTS       UNLIMITED
                PCTINCREASE      0
                BUFFER_POOL      DEFAULT
                FLASH_CACHE      DEFAULT
                CELL_FLASH_CACHE DEFAULT
               )
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_SEDE_MUNICIPIO
(
  ID_SEDE_MUNICIPIO     NUMBER                  NOT NULL,
  FLG_RIPARTIZIONE      NUMBER,
  DESCRIZIONE           VARCHAR2(40 BYTE),
  DESCRIZIONE_COMPLETA  VARCHAR2(100 BYTE),
  SEDE                  VARCHAR2(20 BYTE),
  ID_MUNICIPIO          NUMBER,
  ID_ST_INT_POLIZIA     NUMBER,
  ID_STRUTTURE_INTERNE  NUMBER,
  CAP                   VARCHAR2(20 BYTE),
  NUMERO_ROMANO         VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_SEDE_MUNICIPIO.FLG_RIPARTIZIONE IS '0 -> RIPARTIZIONE 20 MUNICIPI | 1-> RIPARTIZIONE 15 MUNICIPI';

COMMENT ON COLUMN ANAG_USR.CONF_SEDE_MUNICIPIO.ID_MUNICIPIO IS 'FK_CONF_MUNICIPIO';

COMMENT ON COLUMN ANAG_USR.CONF_SEDE_MUNICIPIO.ID_ST_INT_POLIZIA IS 'FK_CONF_ST_INT_POL';

COMMENT ON COLUMN ANAG_USR.CONF_SEDE_MUNICIPIO.ID_STRUTTURE_INTERNE IS 'FK_CONF_STRUTTURE_INTERNE_RC';



CREATE UNIQUE INDEX ANAG_USR.CONF_SEDE_MINICIPIO_PK ON ANAG_USR.CONF_SEDE_MUNICIPIO
(ID_SEDE_MUNICIPIO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE OR REPLACE SYNONYM ELET_USR.CONF_SEDE_MUNICIPIO FOR ANAG_USR.CONF_SEDE_MUNICIPIO;


ALTER TABLE ANAG_USR.CONF_SEDE_MUNICIPIO ADD (
  CONSTRAINT CONF_SEDE_MINICIPIO_PK
  PRIMARY KEY
  (ID_SEDE_MUNICIPIO)
  USING INDEX ANAG_USR.CONF_SEDE_MINICIPIO_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONF_SEDE_MUNICIPIO ADD (
  CONSTRAINT CONF_MUNICIPIO_FK1 
  FOREIGN KEY (ID_MUNICIPIO) 
  REFERENCES ANAG_USR.CONF_MUNICIPIO (ID_MUNICIPIO)
  ENABLE VALIDATE,
  CONSTRAINT CONF_STR_INTERNE_FK1 
  FOREIGN KEY (ID_STRUTTURE_INTERNE) 
  REFERENCES ANAG_USR.CONF_STRUTTURE_INTERNE_RC (ID)
  ENABLE VALIDATE,
  CONSTRAINT CONF_ST_INT_POL_FK1 
  FOREIGN KEY (ID_ST_INT_POLIZIA) 
  REFERENCES ANAG_USR.CONF_ST_INT_POLIZIA (ID_CONF_ST_INT_POLIZIA)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.BLOCCO_CARTA
(
  ID_BLOCCO_CARTA  NUMBER                       NOT NULL,
  ID_SOGGETTO      NUMBER,
  ID_UTENTE_INS    NUMBER,
  DATA_INS         DATE,
  MOTIVO_INS       VARCHAR2(400 CHAR),
  ID_UTENTE_CANC   NUMBER,
  DATA_CANC        DATE,
  MOTIVO_CANC      VARCHAR2(400 CHAR)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.BLOCCO_CARTA_PK ON ANAG_USR.BLOCCO_CARTA
(ID_BLOCCO_CARTA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.BLOCCO_CARTA ADD (
  CONSTRAINT BLOCCO_CARTA_PK
  PRIMARY KEY
  (ID_BLOCCO_CARTA)
  USING INDEX ANAG_USR.BLOCCO_CARTA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.BLOCCO_CARTA ADD (
  CONSTRAINT ID_SOGGETTO_BLOCCO_FK1 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT UTENTE_CAN_BLOCCO_FK_F 
  FOREIGN KEY (ID_UTENTE_CANC) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE,
  CONSTRAINT UTENTE_INS_BLOCCO_FK 
  FOREIGN KEY (ID_UTENTE_INS) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_DOCUMENTO
(
  ID_DOCUMENTO  NUMBER                          NOT NULL,
  DESCRIZIONE   VARCHAR2(30 BYTE)               NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_TIPO_DOCUMENTO IS 'Tabella tipologica che contiene l''elenco dei documenti di riconoscimento alternativi alla carta d''identità';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_DOCUMENTO.ID_DOCUMENTO IS 'Identificativo del documento';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_DOCUMENTO.DESCRIZIONE IS 'Descrizione del documento';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_DOCUMENTO_PK ON ANAG_USR.CONF_TIPO_DOCUMENTO
(ID_DOCUMENTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_DOCUMENTO ADD (
  CONSTRAINT CONF_TIPO_DOCUMENTO_PK
  PRIMARY KEY
  (ID_DOCUMENTO)
  USING INDEX ANAG_USR.CONF_TIPO_DOCUMENTO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.ALTRO_DOC_RICONOSCIMENTO
(
  ID_DOCUMENTO          NUMBER                  NOT NULL,
  TIPOLOGIA             NUMBER                  NOT NULL,
  DATA_RILASCIO         DATE,
  DATA_SCADENZA         DATE,
  ENTE_RILASCIO         VARCHAR2(30 BYTE),
  NUMERO_DOCUMENTO      VARCHAR2(20 BYTE)       NOT NULL,
  TIPO_DOCUMENTO_ALTRO  VARCHAR2(40 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.ALTRO_DOC_RICONOSCIMENTO IS 'La tabella contiene le informazioni relative al documento di riconoscimento di un soggetto diverso dalla carta d''identità italiana.';

COMMENT ON COLUMN ANAG_USR.ALTRO_DOC_RICONOSCIMENTO.ID_DOCUMENTO IS 'Codice identificativo del documento';

COMMENT ON COLUMN ANAG_USR.ALTRO_DOC_RICONOSCIMENTO.TIPOLOGIA IS 'Tipologia del documento';

COMMENT ON COLUMN ANAG_USR.ALTRO_DOC_RICONOSCIMENTO.DATA_RILASCIO IS 'Data in cui è stato rilasciato il documento';

COMMENT ON COLUMN ANAG_USR.ALTRO_DOC_RICONOSCIMENTO.DATA_SCADENZA IS 'Data in cui scade il documento';

COMMENT ON COLUMN ANAG_USR.ALTRO_DOC_RICONOSCIMENTO.ENTE_RILASCIO IS 'Ente che ha rilasciato il documento';

COMMENT ON COLUMN ANAG_USR.ALTRO_DOC_RICONOSCIMENTO.NUMERO_DOCUMENTO IS 'Numero identificativo del documento';



CREATE UNIQUE INDEX ANAG_USR.ALTRO_DOC_RICONOSCIMENTO_PK ON ANAG_USR.ALTRO_DOC_RICONOSCIMENTO
(ID_DOCUMENTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.ALTRO_DOC_RICONOSCIMENTO ADD (
  CONSTRAINT ID_DOCUMENTO_PK
  PRIMARY KEY
  (ID_DOCUMENTO)
  USING INDEX ANAG_USR.ALTRO_DOC_RICONOSCIMENTO_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.ALTRO_DOC_RICONOSCIMENTO ADD (
  CONSTRAINT ALTRO_DOC_RICONOSCIMENTO_FK1 
  FOREIGN KEY (TIPOLOGIA) 
  REFERENCES ANAG_USR.CONF_TIPO_DOCUMENTO (ID_DOCUMENTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_EMIGRAZIONE_LEVA
(
  ID_R_EMIGRAZIONE_LEVA  NUMBER                 NOT NULL,
  DATA_EMIGRAZIONE       DATE,
  ID_SOGGETTO            NUMBER                 NOT NULL,
  ID_COMUNE              NUMBER                 NOT NULL,
  ID_TOPONIMO            NUMBER,
  ID_LOCALITA            NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.R_EMIGRAZIONE_LEVA_PK ON ANAG_USR.R_EMIGRAZIONE_LEVA
(ID_R_EMIGRAZIONE_LEVA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_EMIGRAZIONE_LEVA ADD (
  CONSTRAINT R_EMIGRAZIONE_LEVA_PK
  PRIMARY KEY
  (ID_R_EMIGRAZIONE_LEVA)
  USING INDEX ANAG_USR.R_EMIGRAZIONE_LEVA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_EMIGRAZIONE_LEVA ADD (
  CONSTRAINT COMUNE_R_EMIGRAZIONE_LEVA_FK 
  FOREIGN KEY (ID_COMUNE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT LOCALITA_R_EMIGRAZIONE_LEVA_FK 
  FOREIGN KEY (ID_LOCALITA) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_R_EMIGRAZIONE_LEVA_FK 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT TOPONIMO_R_EMIGRAZIONE_LEVA_FK 
  FOREIGN KEY (ID_TOPONIMO) 
  REFERENCES ANAG_USR.TOPONIMO (ID_TOPONIMO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_COND_PART_LEVA
(
  ID_COND_PART_LEVA  NUMBER                     NOT NULL,
  DESCRIZIONE        VARCHAR2(200 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_COND_PART_LEVA_PK ON ANAG_USR.CONF_COND_PART_LEVA
(ID_COND_PART_LEVA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_COND_PART_LEVA ADD (
  CONSTRAINT CONF_COND_PART_LEVA_PK
  PRIMARY KEY
  (ID_COND_PART_LEVA)
  USING INDEX ANAG_USR.CONF_COND_PART_LEVA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_GRADO_MILITARE
(
  ID_GRADO_MILITARE  NUMBER                     NOT NULL,
  GRADO_AGGIOR       VARCHAR2(25 BYTE),
  DESCRIZIONE        VARCHAR2(100 BYTE),
  DESCRIZIONE_BREVE  VARCHAR2(50 BYTE),
  RUOLO_POLIZIA      VARCHAR2(50 BYTE),
  ID_ARMA_MILITARE   NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_GRADO_MILITARE_PK ON ANAG_USR.CONF_GRADO_MILITARE
(ID_GRADO_MILITARE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_GRADO_MILITARE ADD (
  CONSTRAINT CONF_GRADO_MILITARE_PK
  PRIMARY KEY
  (ID_GRADO_MILITARE)
  USING INDEX ANAG_USR.CONF_GRADO_MILITARE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONF_GRADO_MILITARE ADD (
  CONSTRAINT CONF_ARMA_MILITARE_FK1 
  FOREIGN KEY (ID_ARMA_MILITARE) 
  REFERENCES ANAG_USR.CONF_ARMA_MILITARE (ID_ARMA_MILITARE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_ARMA_MILITARE
(
  ID_ARMA_MILITARE  NUMBER                      NOT NULL,
  DESCRIZIONE       VARCHAR2(50 BYTE),
  CODICE_AGGIOR     VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_ARMA_LEVA_PK ON ANAG_USR.CONF_ARMA_MILITARE
(ID_ARMA_MILITARE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_ARMA_MILITARE ADD (
  CONSTRAINT CONF_ARMA_LEVA_PK
  PRIMARY KEY
  (ID_ARMA_MILITARE)
  USING INDEX ANAG_USR.CONF_ARMA_LEVA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CIE_PAGAMENTI_ANT
(
  ID                       NUMBER               NOT NULL,
  CF_RICHIEDENTE           VARCHAR2(16 CHAR)    NOT NULL,
  CF_BENEFICIARIO          VARCHAR2(16 CHAR)    NOT NULL,
  DATA_RICHIESTA           DATE,
  DATA_VERIFICA_PAG_FO     DATE,
  DATA_VERIFICA_PAG_BO     DATE,
  DATA_BOLLETTINO          DATE,
  IUV                      VARCHAR2(200 CHAR),
  XML_POSIZIONE_FO         CLOB,
  XML_POSIZIONE_BO         CLOB,
  ID_STRUTTURA_INTERNA_RC  NUMBER,
  ID_TIPO_EMISSIONE        NUMBER
)
LOB (XML_POSIZIONE_FO) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
LOB (XML_POSIZIONE_BO) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CIE_PAGAMENTI_ANT_PK ON ANAG_USR.CIE_PAGAMENTI_ANT
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.IDX_CF_BEN_CIE ON ANAG_USR.CIE_PAGAMENTI_ANT
(CF_BENEFICIARIO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CIE_PAGAMENTI_ANT ADD (
  CONSTRAINT CIE_PAGAMENTI_ANT_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CIE_PAGAMENTI_ANT_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CIE_PAGAMENTI_ANT ADD (
  CONSTRAINT CIE_PAGAMENTI_ANT_FK1 
  FOREIGN KEY (ID_STRUTTURA_INTERNA_RC) 
  REFERENCES ANAG_USR.CONF_STRUTTURE_INTERNE_RC (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_EMI_CIEONLINE
(
  ID            NUMBER                          NOT NULL,
  DESCRIZIONE   VARCHAR2(100 BYTE)              NOT NULL,
  ID_POSIZIONE  NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_EMI_CIEONLINE_PK ON ANAG_USR.CONF_TIPO_EMI_CIEONLINE
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_EMI_CIEONLINE ADD (
  CONSTRAINT CONF_TIPO_EMI_CIEONLINE_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_TIPO_EMI_CIEONLINE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONF_TIPO_EMI_CIEONLINE ADD (
  CONSTRAINT CONF_TIPO_EMI_CIEONLINE_FK2 
  FOREIGN KEY (ID_POSIZIONE) 
  REFERENCES ANAG_USR.CONF_POSIZIONI (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_CONTROLLO_TUTELA
(
  ID_CONTROLLO_TUTELA  NUMBER                   NOT NULL,
  DESCRIZIONE          VARCHAR2(400 BYTE),
  FLAG_ATTIVO          CHAR(1 BYTE)             NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_CONTROLLO_TUTELA.ID_CONTROLLO_TUTELA IS 'Identificativo del tipo di controllo per i meritevoli di tutela';

COMMENT ON COLUMN ANAG_USR.CONF_CONTROLLO_TUTELA.DESCRIZIONE IS 'Descrizione del tipo di controllo per i meritevoli di tutela';

COMMENT ON COLUMN ANAG_USR.CONF_CONTROLLO_TUTELA.FLAG_ATTIVO IS 'Indica se il tipo di controllo è attivo o meno';



CREATE UNIQUE INDEX ANAG_USR.CONF_CONTROLLO_TUTELA_PK ON ANAG_USR.CONF_CONTROLLO_TUTELA
(ID_CONTROLLO_TUTELA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_CONTROLLO_TUTELA ADD (
  CONSTRAINT CONF_CONTROLLO_TUTELA_PK
  PRIMARY KEY
  (ID_CONTROLLO_TUTELA)
  USING INDEX ANAG_USR.CONF_CONTROLLO_TUTELA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_CORPO_MILITARE
(
  ID_CORPO_MILITARE  NUMBER                     NOT NULL,
  DESCRIZIONE        VARCHAR2(200 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_CORPO_MILITARE_PK ON ANAG_USR.CONF_CORPO_MILITARE
(ID_CORPO_MILITARE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_CORPO_MILITARE ADD (
  CONSTRAINT CONF_CORPO_MILITARE_PK
  PRIMARY KEY
  (ID_CORPO_MILITARE)
  USING INDEX ANAG_USR.CONF_CORPO_MILITARE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_MOTIVO_IRRICEVIBILITA
(
  ID_MOTIVO    NUMBER                           NOT NULL,
  DESCRIZIONE  VARCHAR2(100 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_IRRICEVIBILITA.ID_MOTIVO IS 'Campo che identifica l''id della tabella';

COMMENT ON COLUMN ANAG_USR.CONF_MOTIVO_IRRICEVIBILITA.DESCRIZIONE IS 'Campo che identifica la descrizone del motivo';



CREATE UNIQUE INDEX ANAG_USR.CONF_MOTIVO_IRRICEVIBILITA_PK ON ANAG_USR.CONF_MOTIVO_IRRICEVIBILITA
(ID_MOTIVO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_MOTIVO_IRRICEVIBILITA ADD (
  CONSTRAINT CONF_MOTIVO_IRRICEVIBILITA_PK
  PRIMARY KEY
  (ID_MOTIVO)
  USING INDEX ANAG_USR.CONF_MOTIVO_IRRICEVIBILITA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_REPORT
(
  ID_TIPO_REPORT  NUMBER                        NOT NULL,
  DESCRIZIONE     VARCHAR2(200 BYTE),
  FLG_VISUALIZZA  VARCHAR2(1 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_REPORT.ID_TIPO_REPORT IS 'Campo che identifica in modo univoco il report';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_REPORT.DESCRIZIONE IS 'Campo che descrive la tipologia del report ';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_REPORT.FLG_VISUALIZZA IS 'S -> Visualizzazione in Maschera, N -> Nascosto';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_REPORT_PK ON ANAG_USR.CONF_TIPO_REPORT
(ID_TIPO_REPORT)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_REPORT ADD (
  CONSTRAINT CONF_TIPO_REPORT_PK
  PRIMARY KEY
  (ID_TIPO_REPORT)
  USING INDEX ANAG_USR.CONF_TIPO_REPORT_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.DOCUMENTI_PROFESSIONISTI
(
  CODICE_FISCALE    VARCHAR2(50 BYTE)           NOT NULL,
  NUMERO_DOCUMENTO  VARCHAR2(50 BYTE),
  DATA_RILASCIO     DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.DOCUMENTI_PROFESSIONISTI.CODICE_FISCALE IS 'Codice fiscale del cittadino professionista
';

COMMENT ON COLUMN ANAG_USR.DOCUMENTI_PROFESSIONISTI.NUMERO_DOCUMENTO IS 'Numero documento del cittadino professionista';

COMMENT ON COLUMN ANAG_USR.DOCUMENTI_PROFESSIONISTI.DATA_RILASCIO IS 'Data di rilascio del documento del cittadino professionista';



CREATE UNIQUE INDEX ANAG_USR.DOCUMENTI_PROFESSIONISTI_PK ON ANAG_USR.DOCUMENTI_PROFESSIONISTI
(CODICE_FISCALE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.DOCUMENTI_PROFESSIONISTI ADD (
  CONSTRAINT DOCUMENTI_PROFESSIONISTI_PK
  PRIMARY KEY
  (CODICE_FISCALE)
  USING INDEX ANAG_USR.DOCUMENTI_PROFESSIONISTI_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.PREINSERIMENTO_TUTELA
(
  ID_PREINSERIMENTO_TUTELA  NUMBER              NOT NULL,
  DATA_IMMIGRAZIONE         DATE,
  COGNOME                   VARCHAR2(200 BYTE),
  NOME                      VARCHAR2(200 BYTE),
  SESSO                     CHAR(1 BYTE),
  DATA_NASCITA              DATE,
  CODICE_FISCALE            VARCHAR2(16 BYTE),
  ID_COMUNE                 NUMBER,
  ID_LOCALITA               NUMBER,
  INDIRIZZO                 VARCHAR2(400 BYTE),
  NOTE                      VARCHAR2(2000 BYTE),
  TUTELA_A                  CHAR(1 BYTE),
  TUTELA_B                  CHAR(1 BYTE),
  ID_UTENTE                 NUMBER,
  DATA_INSERIMENTO          DATE,
  FLG_CANCELLATA            CHAR(1 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.PREINSERIMENTO_TUTELA.ID_PREINSERIMENTO_TUTELA IS 'Campo che identifica il preinserimento tutela';

COMMENT ON COLUMN ANAG_USR.PREINSERIMENTO_TUTELA.DATA_IMMIGRAZIONE IS 'Campo che identifica la data di residenza';

COMMENT ON COLUMN ANAG_USR.PREINSERIMENTO_TUTELA.ID_COMUNE IS 'Campo che identifica il comune di nascita';

COMMENT ON COLUMN ANAG_USR.PREINSERIMENTO_TUTELA.ID_LOCALITA IS 'Campo che identifica la località di nascita';

COMMENT ON COLUMN ANAG_USR.PREINSERIMENTO_TUTELA.INDIRIZZO IS 'Campo che identifica l''indirizzo della nuova residenza';

COMMENT ON COLUMN ANAG_USR.PREINSERIMENTO_TUTELA.TUTELA_A IS 'Campo che viene valorizzato con S se il soggetto fa parte della categoria A, N altrimenti';

COMMENT ON COLUMN ANAG_USR.PREINSERIMENTO_TUTELA.TUTELA_B IS 'Campo che viene valorizzato con S se il soggetto fa parte della categoria B, N altrimenti';

COMMENT ON COLUMN ANAG_USR.PREINSERIMENTO_TUTELA.FLG_CANCELLATA IS 'Flag che indica se la pratica è stata cancellata';



CREATE UNIQUE INDEX ANAG_USR.PREINSERIMENTO_TUTELA_PK ON ANAG_USR.PREINSERIMENTO_TUTELA
(ID_PREINSERIMENTO_TUTELA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.PREINSERIMENTO_TUTELA ADD (
  CONSTRAINT PREINSERIMENTO_TUTELA_PK
  PRIMARY KEY
  (ID_PREINSERIMENTO_TUTELA)
  USING INDEX ANAG_USR.PREINSERIMENTO_TUTELA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.PREINSERIMENTO_TUTELA ADD (
  CONSTRAINT ID_COMUNE_NASCITA_FK 
  FOREIGN KEY (ID_COMUNE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT ID_LOCALITA_NASCITA_FK 
  FOREIGN KEY (ID_LOCALITA) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE,
  CONSTRAINT ID_UTENTE_FK3 
  FOREIGN KEY (ID_UTENTE) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_CONTROLLO_CRI
(
  ID_CRI          NUMBER                        NOT NULL,
  ID_CONTROLLO    NUMBER                        NOT NULL,
  FLAG_CONTROLLO  CHAR(1 BYTE),
  DATA_CONTROLLO  DATE,
  OPERATORE       NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.R_CONTROLLO_CRI.ID_CRI IS 'Campo che identifica il cambio di residenza';

COMMENT ON COLUMN ANAG_USR.R_CONTROLLO_CRI.ID_CONTROLLO IS 'Campo che identifica il tipo di controllo eseguito';

COMMENT ON COLUMN ANAG_USR.R_CONTROLLO_CRI.FLAG_CONTROLLO IS 'Campo che identifica l''esito del controllo';

COMMENT ON COLUMN ANAG_USR.R_CONTROLLO_CRI.DATA_CONTROLLO IS 'Campo che identifica la data in cui è stato effettuato il controllo ';

COMMENT ON COLUMN ANAG_USR.R_CONTROLLO_CRI.OPERATORE IS 'Campo che identifica l''operatore che ha eseguito il controllo';



CREATE UNIQUE INDEX ANAG_USR.R_CONTROLLO_CRI_PK ON ANAG_USR.R_CONTROLLO_CRI
(ID_CRI, ID_CONTROLLO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_CONTROLLO_CRI ADD (
  CONSTRAINT R_CONTROLLO_CRI_PK
  PRIMARY KEY
  (ID_CRI, ID_CONTROLLO)
  USING INDEX ANAG_USR.R_CONTROLLO_CRI_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_CONTROLLO_CRI ADD (
  CONSTRAINT ID_CONTROLLO_FK1 
  FOREIGN KEY (ID_CONTROLLO) 
  REFERENCES ANAG_USR.CONF_CONTROLLO_TUTELA (ID_CONTROLLO_TUTELA)
  ENABLE VALIDATE,
  CONSTRAINT ID_CRI_FK1 
  FOREIGN KEY (ID_CRI) 
  REFERENCES ANAG_USR.CAMBIO_RESIDENZA_DOMICILIO (ID_CAMBIO_RESIDENZA_DOMICILIO)
  ENABLE VALIDATE,
  CONSTRAINT OPERATORE_FK1 
  FOREIGN KEY (OPERATORE) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.REPORT_TUTELA_CRI
(
  ID_REPORT_TUTELA  NUMBER                      NOT NULL,
  SEMESTRE          CHAR(1 BYTE),
  ANNO_REPORT       NUMBER(4),
  ID_TIPO_REPORT    NUMBER,
  DOCUMENTO         BLOB,
  DATA_GENERAZIONE  DATE,
  UTENTE            NUMBER,
  MUNICIPIO         NUMBER
)
LOB (DOCUMENTO) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.REPORT_TUTELA_CRI.ID_REPORT_TUTELA IS 'Campo che identifica il report';

COMMENT ON COLUMN ANAG_USR.REPORT_TUTELA_CRI.SEMESTRE IS 'Campo che identifica il semestre 1 -> gennaio-giugno 2 -> luglio-dicembre';

COMMENT ON COLUMN ANAG_USR.REPORT_TUTELA_CRI.ANNO_REPORT IS 'Campo che identifica l''anno di riferimento del report';

COMMENT ON COLUMN ANAG_USR.REPORT_TUTELA_CRI.ID_TIPO_REPORT IS 'Campo che identifica il tipo del report';

COMMENT ON COLUMN ANAG_USR.REPORT_TUTELA_CRI.DOCUMENTO IS 'Campo che contiene il documento ';

COMMENT ON COLUMN ANAG_USR.REPORT_TUTELA_CRI.DATA_GENERAZIONE IS 'Campo che contiene la data di generazione del report';

COMMENT ON COLUMN ANAG_USR.REPORT_TUTELA_CRI.UTENTE IS 'Campo che identifica l''utente che ha generato il report';

COMMENT ON COLUMN ANAG_USR.REPORT_TUTELA_CRI.MUNICIPIO IS 'Campo che identifica il municipio di appartenenza';



CREATE UNIQUE INDEX ANAG_USR.REPORT_TUTELA_CRI_PK ON ANAG_USR.REPORT_TUTELA_CRI
(ID_REPORT_TUTELA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.REPORT_TUTELA_CRI ADD (
  CONSTRAINT REPORT_TUTELA_CRI_PK
  PRIMARY KEY
  (ID_REPORT_TUTELA)
  USING INDEX ANAG_USR.REPORT_TUTELA_CRI_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.REPORT_TUTELA_CRI ADD (
  CONSTRAINT REPORT_TUTELA_CRI_FK1 
  FOREIGN KEY (ID_TIPO_REPORT) 
  REFERENCES ANAG_USR.CONF_TIPO_REPORT (ID_TIPO_REPORT)
  ENABLE VALIDATE,
  CONSTRAINT REPORT_TUTELA_CRI_FK2 
  FOREIGN KEY (UTENTE) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE,
  CONSTRAINT REPORT_TUTELA_CRI_FK3 
  FOREIGN KEY (MUNICIPIO) 
  REFERENCES ANAG_USR.CONF_MUNICIPIO (ID_MUNICIPIO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.REG_USER_ANPR_SIGN
(
  ID                   NUMBER                   NOT NULL,
  ALIAS_KEYSTORE       VARCHAR2(200 BYTE),
  ID_POSTAZIONE        VARCHAR2(200 BYTE),
  SN_KEYSTORE          VARCHAR2(200 BYTE),
  FIRMA_ID_POSTAZIONE  VARCHAR2(4000 BYTE),
  HOSTNAME             VARCHAR2(200 BYTE),
  ID_SEDE              VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.REG_USER_ANPR_NEW_PK ON ANAG_USR.REG_USER_ANPR_SIGN
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.REG_USER_ANPR_SIGN ADD (
  CONSTRAINT REG_USER_ANPR_NEW_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.REG_USER_ANPR_NEW_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CANCELL_DUPLICE_ISCR
(
  ID_CANCELL_DUPLICE_ISCR  NUMBER               NOT NULL,
  NUMERO_PRATICA_INTERNO   VARCHAR2(20 CHAR),
  ANNO_PRATICA_INTERNO     VARCHAR2(20 CHAR),
  NUMERO_PROT_COMUNE       VARCHAR2(20 CHAR),
  ANNO_PROT_COMUNE         VARCHAR2(20 CHAR),
  DATA_PRATICA             DATE,
  DATA_RICHIESTA           DATE,
  DATA_RISPOSTA            DATE,
  DATA_DECORRENZA_CANCELL  DATE,
  ID_STATO_PRATICA         NUMBER,
  TIPO_ISTANZA             VARCHAR2(1 CHAR),
  ID_COMUNE_RICHIESTA      NUMBER,
  NUMERO_COMPONENTI        NUMBER,
  NOTE                     VARCHAR2(400 CHAR),
  ID_UTENTE                NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CANCELL_DUPLICE_ISCR.ID_CANCELL_DUPLICE_ISCR IS 'identificativo univoco della pratica';

COMMENT ON COLUMN ANAG_USR.CANCELL_DUPLICE_ISCR.NUMERO_PRATICA_INTERNO IS 'numero pratica del comune di Roma';

COMMENT ON COLUMN ANAG_USR.CANCELL_DUPLICE_ISCR.ANNO_PRATICA_INTERNO IS 'anno pratica del comune di Roma';

COMMENT ON COLUMN ANAG_USR.CANCELL_DUPLICE_ISCR.NUMERO_PROT_COMUNE IS 'numero protocollo del comune altra iscrizione';

COMMENT ON COLUMN ANAG_USR.CANCELL_DUPLICE_ISCR.ANNO_PROT_COMUNE IS 'anno protocollo del comune altra iscrizione';

COMMENT ON COLUMN ANAG_USR.CANCELL_DUPLICE_ISCR.DATA_PRATICA IS 'data in cui è stata definita la pratica';

COMMENT ON COLUMN ANAG_USR.CANCELL_DUPLICE_ISCR.DATA_RICHIESTA IS 'data in cui è pervenuta la richiesta del comune altra iscrizione';

COMMENT ON COLUMN ANAG_USR.CANCELL_DUPLICE_ISCR.DATA_RISPOSTA IS 'data in cui è stata inviata risposta al comune atra iscrizione';

COMMENT ON COLUMN ANAG_USR.CANCELL_DUPLICE_ISCR.DATA_DECORRENZA_CANCELL IS 'data effettiva di cancellazione del/ dei soggetti relativi alla pratica';

COMMENT ON COLUMN ANAG_USR.CANCELL_DUPLICE_ISCR.ID_STATO_PRATICA IS 'identificativo dello stato in cui si trova la pratica';

COMMENT ON COLUMN ANAG_USR.CANCELL_DUPLICE_ISCR.TIPO_ISTANZA IS 'tipo di istanza (P - DI PARTE, U - DI UFFICIO)';

COMMENT ON COLUMN ANAG_USR.CANCELL_DUPLICE_ISCR.ID_COMUNE_RICHIESTA IS 'identificativo del comune altra iscrizione';

COMMENT ON COLUMN ANAG_USR.CANCELL_DUPLICE_ISCR.NUMERO_COMPONENTI IS 'numero dei soggetti relativi alla pratica';

COMMENT ON COLUMN ANAG_USR.CANCELL_DUPLICE_ISCR.NOTE IS 'note pratica';

COMMENT ON COLUMN ANAG_USR.CANCELL_DUPLICE_ISCR.ID_UTENTE IS 'identificativo dell''utente che ha definito la pratica';



CREATE UNIQUE INDEX ANAG_USR.CANCELL_DUPLICE_ISCR_PK ON ANAG_USR.CANCELL_DUPLICE_ISCR
(ID_CANCELL_DUPLICE_ISCR)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CANCELL_DUPLICE_ISCR ADD (
  CONSTRAINT CANCELL_DUPLICE_ISCR_PK
  PRIMARY KEY
  (ID_CANCELL_DUPLICE_ISCR)
  USING INDEX ANAG_USR.CANCELL_DUPLICE_ISCR_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CANCELL_DUPLICE_ISCR ADD (
  CONSTRAINT COMUNE_CDI_FK 
  FOREIGN KEY (ID_COMUNE_RICHIESTA) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT CONF_STATO_PRATICA_CDI_FK 
  FOREIGN KEY (ID_STATO_PRATICA) 
  REFERENCES ANAG_USR.CONF_STATO_PRATICA (ID_STATO_PRATICA)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_SOGGETTO_CANC_DUPLICE_ISCR
(
  ID_SOGGETTO                NUMBER             NOT NULL,
  ID_CANCELL_DUPLICE_ISCR    NUMBER             NOT NULL,
  PROGRESSIVO_COMPONENTE     NUMBER,
  ID_ESITO_ACCERTAMENTO_CDI  NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.R_SOGGETTO_CANC_DUPLICE_IS_PK ON ANAG_USR.R_SOGGETTO_CANC_DUPLICE_ISCR
(ID_SOGGETTO, ID_CANCELL_DUPLICE_ISCR)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_SOGGETTO_CANC_DUPLICE_ISCR ADD (
  CONSTRAINT R_SOGGETTO_CANC_DUPLICE_IS_PK
  PRIMARY KEY
  (ID_SOGGETTO, ID_CANCELL_DUPLICE_ISCR)
  USING INDEX ANAG_USR.R_SOGGETTO_CANC_DUPLICE_IS_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_SOGGETTO_CANC_DUPLICE_ISCR ADD (
  CONSTRAINT CANCELL_DUPLICE_ISCR_FK 
  FOREIGN KEY (ID_CANCELL_DUPLICE_ISCR) 
  REFERENCES ANAG_USR.CANCELL_DUPLICE_ISCR (ID_CANCELL_DUPLICE_ISCR)
  ENABLE VALIDATE,
  CONSTRAINT ESITO_ACCERTAMENTO_CDI_FK 
  FOREIGN KEY (ID_ESITO_ACCERTAMENTO_CDI) 
  REFERENCES ANAG_USR.CONF_ESITO_ACCERTAMENTO_CDI (ID_ESITO_ACCERTAMENTO_CDI)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_CDI_FK 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_ESITO_ACCERTAMENTO_CDI
(
  ID_ESITO_ACCERTAMENTO_CDI  NUMBER             NOT NULL,
  DESCRIZIONE                VARCHAR2(100 CHAR)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_ESITO_ACCERTAMENTO_CD_PK ON ANAG_USR.CONF_ESITO_ACCERTAMENTO_CDI
(ID_ESITO_ACCERTAMENTO_CDI)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_ESITO_ACCERTAMENTO_CDI ADD (
  CONSTRAINT CONF_ESITO_ACCERTAMENTO_CD_PK
  PRIMARY KEY
  (ID_ESITO_ACCERTAMENTO_CDI)
  USING INDEX ANAG_USR.CONF_ESITO_ACCERTAMENTO_CD_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.ERROR_ACC_PROT
(
  ID_ACCERTAMENTO_CANC  NUMBER                  NOT NULL,
  ERRORE                VARCHAR2(4000 BYTE)     NOT NULL,
  DATA_PROCESSAMENTO    DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;
CREATE TABLE ANAG_USR.RETTIFICA_ANPR
(
  ID_RETTIFICA           NUMBER                 NOT NULL,
  CODICE_RICHIESTA_ANPR  VARCHAR2(200 BYTE),
  DATA_RICHIESTA         DATE,
  DATA_SCADENZA          DATE,
  DATA_RISOLUZIONE       DATE,
  ID_UTENTE              NUMBER,
  ID_ORGANIZZAZIONE      NUMBER,
  ID_STATO_RICHIESTA     NUMBER,
  NOTE_SOSPENSIONE       VARCHAR2(239 BYTE),
  NOTE_RIFIUTO           VARCHAR2(239 BYTE),
  RIEPILOGO_RICHIESTA    BLOB,
  ID_RECAPITO            NUMBER
)
LOB (RIEPILOGO_RICHIESTA) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.RETTIFICA_ANPR.ID_RETTIFICA IS 'Identificativo della rettifica';

COMMENT ON COLUMN ANAG_USR.RETTIFICA_ANPR.CODICE_RICHIESTA_ANPR IS 'Codice richiesta ANPR della richiesta di rettifica';

COMMENT ON COLUMN ANAG_USR.RETTIFICA_ANPR.DATA_RICHIESTA IS 'Data della richiesta delle rettifiche';

COMMENT ON COLUMN ANAG_USR.RETTIFICA_ANPR.DATA_SCADENZA IS 'Data di scadenza della rettifica';

COMMENT ON COLUMN ANAG_USR.RETTIFICA_ANPR.DATA_RISOLUZIONE IS 'Data della risoluzione negativa o positiva della richiesta';

COMMENT ON COLUMN ANAG_USR.RETTIFICA_ANPR.ID_UTENTE IS 'Identificativo dell''utente che ha lavorato la richiesta';

COMMENT ON COLUMN ANAG_USR.RETTIFICA_ANPR.ID_ORGANIZZAZIONE IS 'Identificativo dell''organizzazione che ha lavorato la richiesta';

COMMENT ON COLUMN ANAG_USR.RETTIFICA_ANPR.ID_STATO_RICHIESTA IS 'Identificativo dello stato della richiesta';

COMMENT ON COLUMN ANAG_USR.RETTIFICA_ANPR.NOTE_SOSPENSIONE IS 'Note di sospensione';

COMMENT ON COLUMN ANAG_USR.RETTIFICA_ANPR.NOTE_RIFIUTO IS 'Note di rifiuto';

COMMENT ON COLUMN ANAG_USR.RETTIFICA_ANPR.RIEPILOGO_RICHIESTA IS 'PDF di riepilogo della richiesta del cittadino';

COMMENT ON COLUMN ANAG_USR.RETTIFICA_ANPR.ID_RECAPITO IS 'Identificativo del recapito';



CREATE UNIQUE INDEX ANAG_USR.RETTIFICA_ANPR_PK ON ANAG_USR.RETTIFICA_ANPR
(ID_RETTIFICA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.RETTIFICA_ANPR ADD (
  CONSTRAINT RETTIFICA_ANPR_PK
  PRIMARY KEY
  (ID_RETTIFICA)
  USING INDEX ANAG_USR.RETTIFICA_ANPR_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.RETTIFICA_ANPR ADD (
  CONSTRAINT RETTIFICA_ANPR_FK1 
  FOREIGN KEY (ID_RECAPITO) 
  REFERENCES ANAG_USR.RECAPITO_RETTIFICA_ANPR (ID_RECAPITO_ONLINE)
  ENABLE VALIDATE,
  CONSTRAINT RETTIFICA_ANPR_FK2 
  FOREIGN KEY (ID_UTENTE) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE,
  CONSTRAINT RETTIFICA_ANPR_FK3 
  FOREIGN KEY (ID_ORGANIZZAZIONE) 
  REFERENCES ANAG_USR.CONF_STRUTTURE_INTERNE_RC (ID)
  ENABLE VALIDATE,
  CONSTRAINT RETTIFICA_ANPR_FK4 
  FOREIGN KEY (ID_STATO_RICHIESTA) 
  REFERENCES ANAG_USR.CONF_STATO_RICHIESTA_ANPR (ID_STATO_RICHIESTA)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_SEZIONE_RETTIFICA_ANPR
(
  ID_SEZIONE   NUMBER                           NOT NULL,
  DESCRIZIONE  VARCHAR2(200 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_SEZIONE_RETTIFICA_ANPR.ID_SEZIONE IS 'Identificativo della sezione';

COMMENT ON COLUMN ANAG_USR.CONF_SEZIONE_RETTIFICA_ANPR.DESCRIZIONE IS 'Descrizione della sezione';



CREATE UNIQUE INDEX ANAG_USR.CONF_SEZIONE_RETTIFICA_ANP_PK ON ANAG_USR.CONF_SEZIONE_RETTIFICA_ANPR
(ID_SEZIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_SEZIONE_RETTIFICA_ANPR ADD (
  CONSTRAINT CONF_SEZIONE_RETTIFICA_ANP_PK
  PRIMARY KEY
  (ID_SEZIONE)
  USING INDEX ANAG_USR.CONF_SEZIONE_RETTIFICA_ANP_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_RETTIFICA_ANPR
(
  ID           NUMBER                           NOT NULL,
  CODICE       VARCHAR2(100 BYTE),
  DESCRIZIONE  VARCHAR2(200 BYTE),
  ID_SEZIONE   NUMBER,
  FLG_ATTIVO   VARCHAR2(1 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_RETTIFICA_ANPR.ID IS 'Identificativo della tabella';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_RETTIFICA_ANPR.CODICE IS 'Codice ANPR della rettifica';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_RETTIFICA_ANPR.DESCRIZIONE IS 'Descrizione della rettifica';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_RETTIFICA_ANPR.ID_SEZIONE IS 'Identificativo della sezione di appartenenza';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_RETTIFICA_ANPR.FLG_ATTIVO IS 'S -> Attivo, N -> Non attivo';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_RETTIFICA_ANPR_PK ON ANAG_USR.CONF_TIPO_RETTIFICA_ANPR
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_RETTIFICA_ANPR ADD (
  CONSTRAINT CONF_TIPO_RETTIFICA_ANPR_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_TIPO_RETTIFICA_ANPR_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CONF_TIPO_RETTIFICA_ANPR ADD (
  CONSTRAINT CONF_TIPO_RETTIFICA_ANPR_FK1 
  FOREIGN KEY (ID_SEZIONE) 
  REFERENCES ANAG_USR.CONF_SEZIONE_RETTIFICA_ANPR (ID_SEZIONE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_STATO_RICHIESTA_ANPR
(
  ID_STATO_RICHIESTA  NUMBER                    NOT NULL,
  DESCRIZIONE         VARCHAR2(200 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_STATO_RICHIESTA_ANPR.ID_STATO_RICHIESTA IS 'Identificativo ANPR dello stato della richiesta';

COMMENT ON COLUMN ANAG_USR.CONF_STATO_RICHIESTA_ANPR.DESCRIZIONE IS 'Descrizione dello stato della richiesta';



CREATE UNIQUE INDEX ANAG_USR.CONF_STATO_RICHIESTA_ANPR_PK ON ANAG_USR.CONF_STATO_RICHIESTA_ANPR
(ID_STATO_RICHIESTA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_STATO_RICHIESTA_ANPR ADD (
  CONSTRAINT CONF_STATO_RICHIESTA_ANPR_PK
  PRIMARY KEY
  (ID_STATO_RICHIESTA)
  USING INDEX ANAG_USR.CONF_STATO_RICHIESTA_ANPR_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_SOGGETTO_RETTIFICA
(
  ID_SOGGETTO   NUMBER                          NOT NULL,
  ID_RETTIFICA  NUMBER                          NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_RETTIFICA.ID_SOGGETTO IS 'Identificativo del soggetto';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_RETTIFICA.ID_RETTIFICA IS 'Identificativo della rettifica ANPR';



CREATE UNIQUE INDEX ANAG_USR.R_SOGGETTO_RETTIFICA_PK ON ANAG_USR.R_SOGGETTO_RETTIFICA
(ID_SOGGETTO, ID_RETTIFICA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_SOGGETTO_RETTIFICA ADD (
  CONSTRAINT R_SOGGETTO_RETTIFICA_PK
  PRIMARY KEY
  (ID_SOGGETTO, ID_RETTIFICA)
  USING INDEX ANAG_USR.R_SOGGETTO_RETTIFICA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.MV_SOGGETTO_FAMIGLIA_STORICO
(
  NOME                     VARCHAR2(250 BYTE),
  COGNOME                  VARCHAR2(250 BYTE),
  SESSO                    CHAR(1 BYTE),
  CODICE_INDIVIDUALE       VARCHAR2(20 BYTE),
  CODICE_FISCALE           VARCHAR2(16 BYTE),
  DATA_DECORRENZA_FAMCONV  DATE,
  ID_SOGGETTO_USR          NUMBER,
  ID_SOGGETTO_ST           NUMBER               NOT NULL,
  ID_FAMIGLIA_CONV         NUMBER,
  ID_MORTE                 NUMBER,
  CODICE_FAMIGLIA          VARCHAR2(20 CHAR),
  CODICELEGAME             NUMBER(5),
  ID_STATUS_SOGGETTO       NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;
CREATE TABLE ANAG_USR.TMP_BONUS_SPESA_MV
(
  NOME                VARCHAR2(250 BYTE),
  COGNOME             VARCHAR2(250 BYTE),
  SESSO               CHAR(1 BYTE),
  CODICE_INDIVIDUALE  VARCHAR2(20 BYTE),
  CODICE_FISCALE      VARCHAR2(16 BYTE),
  ID_SOGGETTO         NUMBER                    NOT NULL,
  DATA_EVENTO         DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;
CREATE TABLE ANAG_USR.MV_TOPONIMI_CHIUSI
(
  ID_TOPONIMO  NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;
CREATE TABLE ANAG_USR.CONF_TIPO_AIRE
(
  ID           NUMBER                           NOT NULL,
  CODICE       VARCHAR2(10 BYTE),
  DESCRIZIONE  VARCHAR2(200 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_AIRE.ID IS 'Identificativo della tabella';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_AIRE.CODICE IS 'Codice della tipologia AIRE';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_AIRE.DESCRIZIONE IS 'Descrizione della tipologia AIRE';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_AIRE_PK ON ANAG_USR.CONF_TIPO_AIRE
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_AIRE ADD (
  CONSTRAINT CONF_TIPO_AIRE_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_TIPO_AIRE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.ANAGRAFICA_AIRE
(
  ID_ANAGRAFICA_AIRE  NUMBER                    NOT NULL,
  ID_SOGGETTO         NUMBER,
  CODICE_ANAGAIRE     VARCHAR2(30 BYTE),
  FLAG_CANCELLATO     VARCHAR2(1 BYTE),
  ID_TIPO_AIRE        NUMBER,
  DATA_ISCRIZIONE     DATE,
  ID_COMUNE_RIENTRO   NUMBER,
  DATA_RIENTRO        DATE,
  DATA_FINE_AIRE      DATE,
  NUMERO_PRATICA      VARCHAR2(20 BYTE),
  DATA_PRATICA        DATE,
  DATA_INVIO_MODELLO  DATE,
  ANNO_PROTOCOLLO     NUMBER(4),
  NUMERO_PROTOCOLLO   VARCHAR2(20 BYTE),
  ID_PRATICA_AIRE     NUMBER,
  FLAG_SUBENTRO       VARCHAR2(1 BYTE),
  FLAG_ATTIVO         VARCHAR2(1 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.ANAGRAFICA_AIRE.ID_ANAGRAFICA_AIRE IS 'Identificativo di tabella';

COMMENT ON COLUMN ANAG_USR.ANAGRAFICA_AIRE.ID_SOGGETTO IS 'Identificativo del soggetto';

COMMENT ON COLUMN ANAG_USR.ANAGRAFICA_AIRE.CODICE_ANAGAIRE IS 'Codice anagaire';

COMMENT ON COLUMN ANAG_USR.ANAGRAFICA_AIRE.FLAG_CANCELLATO IS 'N -> AIRE, -> Cancellato AIRE';

COMMENT ON COLUMN ANAG_USR.ANAGRAFICA_AIRE.ID_TIPO_AIRE IS 'Identificativo della tipologia di iscrizione o cancellazione AIRE';

COMMENT ON COLUMN ANAG_USR.ANAGRAFICA_AIRE.DATA_ISCRIZIONE IS 'Data di iscrizione AIRE';

COMMENT ON COLUMN ANAG_USR.ANAGRAFICA_AIRE.ID_COMUNE_RIENTRO IS 'Identificativo del comune di rientro in Italia';

COMMENT ON COLUMN ANAG_USR.ANAGRAFICA_AIRE.DATA_RIENTRO IS 'Data del rientro in Italia';

COMMENT ON COLUMN ANAG_USR.ANAGRAFICA_AIRE.DATA_FINE_AIRE IS 'Data di cancellazione AIRE';

COMMENT ON COLUMN ANAG_USR.ANAGRAFICA_AIRE.NUMERO_PRATICA IS 'Numero pratica';

COMMENT ON COLUMN ANAG_USR.ANAGRAFICA_AIRE.DATA_PRATICA IS 'Data definizione pratica';

COMMENT ON COLUMN ANAG_USR.ANAGRAFICA_AIRE.DATA_INVIO_MODELLO IS 'Data di invio modello consolare';

COMMENT ON COLUMN ANAG_USR.ANAGRAFICA_AIRE.ANNO_PROTOCOLLO IS 'Anno del protocollo';

COMMENT ON COLUMN ANAG_USR.ANAGRAFICA_AIRE.NUMERO_PROTOCOLLO IS 'Numero del protocollo';

COMMENT ON COLUMN ANAG_USR.ANAGRAFICA_AIRE.ID_PRATICA_AIRE IS 'Identificativo della pratica AIRE';

COMMENT ON COLUMN ANAG_USR.ANAGRAFICA_AIRE.FLAG_SUBENTRO IS 'N -> Aggior, S -> SIPO';

COMMENT ON COLUMN ANAG_USR.ANAGRAFICA_AIRE.FLAG_ATTIVO IS 'N -> No, S -> Sì';



CREATE UNIQUE INDEX ANAG_USR.ANAGRAFICA_AIRE_PK ON ANAG_USR.ANAGRAFICA_AIRE
(ID_ANAGRAFICA_AIRE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.ANAGRAFICA_AIRE ADD (
  CONSTRAINT ANAGRAFICA_AIRE_PK
  PRIMARY KEY
  (ID_ANAGRAFICA_AIRE)
  USING INDEX ANAG_USR.ANAGRAFICA_AIRE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.ANAGRAFICA_AIRE ADD (
  CONSTRAINT ANAGRAFICA_AIRE_FK1 
  FOREIGN KEY (ID_TIPO_AIRE) 
  REFERENCES ANAG_USR.CONF_TIPO_AIRE (ID)
  ENABLE VALIDATE,
  CONSTRAINT ANAGRAFICA_AIRE_FK2 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT ANAGRAFICA_AIRE_FK3 
  FOREIGN KEY (ID_PRATICA_AIRE) 
  REFERENCES ANAG_USR.PRATICA_AIRE (ID_PRATICA_AIRE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CANCELLAZIONE_ALTRI_MOTIVI
(
  ID                     NUMBER                 NOT NULL,
  ID_SOGGETTO            NUMBER,
  DATA_CANCELLAZIONE     DATE,
  ID_TIPO_CANCELLAZIONE  NUMBER,
  ID_COMUNE              NUMBER,
  NOTE                   VARCHAR2(4000 BYTE),
  FLG_ATTIVO             VARCHAR2(1 BYTE),
  DATA_OPERAZIONE        DATE,
  ID_UTENTE              NUMBER,
  ID_FAMIGLIA            NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CANCELLAZIONE_ALTRI_MOTIVI.ID IS 'Identificativo di tabella';

COMMENT ON COLUMN ANAG_USR.CANCELLAZIONE_ALTRI_MOTIVI.DATA_CANCELLAZIONE IS 'Data di decorrenza della cancellazione';

COMMENT ON COLUMN ANAG_USR.CANCELLAZIONE_ALTRI_MOTIVI.ID_TIPO_CANCELLAZIONE IS 'Tipo di cancellazione';

COMMENT ON COLUMN ANAG_USR.CANCELLAZIONE_ALTRI_MOTIVI.ID_COMUNE IS 'Comune di cancellazione';

COMMENT ON COLUMN ANAG_USR.CANCELLAZIONE_ALTRI_MOTIVI.NOTE IS 'Note relative alla cancellazione';

COMMENT ON COLUMN ANAG_USR.CANCELLAZIONE_ALTRI_MOTIVI.FLG_ATTIVO IS 'S -> Attivo, N -> Non attivo';

COMMENT ON COLUMN ANAG_USR.CANCELLAZIONE_ALTRI_MOTIVI.DATA_OPERAZIONE IS 'Datd dell''operazione';

COMMENT ON COLUMN ANAG_USR.CANCELLAZIONE_ALTRI_MOTIVI.ID_UTENTE IS 'Identificato dell''utente che ha effettuato l''operazione';

COMMENT ON COLUMN ANAG_USR.CANCELLAZIONE_ALTRI_MOTIVI.ID_FAMIGLIA IS 'Identificativo della famiglia';



CREATE UNIQUE INDEX ANAG_USR.CANCELLAZIONE_ALTRI_MOTIVI_PK ON ANAG_USR.CANCELLAZIONE_ALTRI_MOTIVI
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CANCELLAZIONE_ALTRI_MOTIVI ADD (
  CONSTRAINT CANCELLAZIONE_ALTRI_MOTIVI_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CANCELLAZIONE_ALTRI_MOTIVI_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CANCELLAZIONE_ALTRI_MOTIVI ADD (
  CONSTRAINT CANCELLAZIONE_ALTRI_MOTIV_FK1 
  FOREIGN KEY (ID_TIPO_CANCELLAZIONE) 
  REFERENCES ANAG_USR.CONF_CANCELLAZIONE_AM (ID)
  ENABLE VALIDATE,
  CONSTRAINT CANCELLAZIONE_ALTRI_MOTIV_FK2 
  FOREIGN KEY (ID_FAMIGLIA) 
  REFERENCES ANAG_USR.FAMIGLIA_CONVIVENZA (ID_FAMIGLIA_CONV)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_CANCELLAZIONE_AM
(
  ID           NUMBER                           NOT NULL,
  CODICE_ANPR  VARCHAR2(20 BYTE),
  DESCRIZIONE  VARCHAR2(200 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_CANCELLAZIONE_AM.ID IS 'Identificativo di tabella';

COMMENT ON COLUMN ANAG_USR.CONF_CANCELLAZIONE_AM.CODICE_ANPR IS 'Codice ANPR di cancellazione';



CREATE UNIQUE INDEX ANAG_USR.CONF_CANCELLAZIONE_AM_PK ON ANAG_USR.CONF_CANCELLAZIONE_AM
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_CANCELLAZIONE_AM ADD (
  CONSTRAINT CONF_CANCELLAZIONE_AM_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_CANCELLAZIONE_AM_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.BS_HEADER
(
  DTA_CREAZIONE        DATE,
  NUM_ANAGRAFICHE      NUMBER,
  MITTENTE             VARCHAR2(20 BYTE),
  NUM_CONTO            VARCHAR2(50 BYTE),
  DTA_INSERIMENTO      TIMESTAMP(6),
  NOME_SUPPORTO        VARCHAR2(20 BYTE),
  CAMPO_DISP           VARCHAR2(20 BYTE),
  COD_PRODOTTO         VARCHAR2(20 BYTE),
  REL_PRODOTTO         VARCHAR2(20 BYTE),
  CODICE_BANCA         VARCHAR2(30 BYTE),
  DTA_RENDICONTAZIONE  DATE,
  ID_HEADER            NUMBER                   NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.BS_HEADER_PK ON ANAG_USR.BS_HEADER
(ID_HEADER)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.BS_HEADER ADD (
  CONSTRAINT BS_HEADER_PK
  PRIMARY KEY
  (ID_HEADER)
  USING INDEX ANAG_USR.BS_HEADER_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.BS_RICHIESTE
(
  NUM_PROGRESSIVO         NUMBER                NOT NULL,
  NOME                    VARCHAR2(45 BYTE),
  COGNOME                 VARCHAR2(45 BYTE),
  COD_FISCALE             VARCHAR2(45 BYTE),
  NUMERO_CARTA            VARCHAR2(50 BYTE),
  DTA_EMISSIONE           DATE,
  DTA_INSERIMENTO         TIMESTAMP(6),
  ELEGIBILE               VARCHAR2(2 BYTE),
  NUM_COMP_NUCLEO         NUMBER,
  MOTIVO_NON_ELIGIBILITA  VARCHAR2(200 BYTE),
  COD_FAMIGLIA            VARCHAR2(20 BYTE),
  IMPORTO_RICARICA        NUMBER,
  ID_HEADER               NUMBER                NOT NULL,
  DATA_RIFERIMENTO        DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.BS_RICHIESTE_PK ON ANAG_USR.BS_RICHIESTE
(NUM_PROGRESSIVO, ID_HEADER)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.BS_RICHIESTE ADD (
  CONSTRAINT BS_RICHIESTE_PK
  PRIMARY KEY
  (NUM_PROGRESSIVO, ID_HEADER)
  USING INDEX ANAG_USR.BS_RICHIESTE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.BS_FOOTER
(
  DTA_CREAZIONE    DATE,
  NUM_RECORD       NUMBER,
  DTA_INSERIMENTO  TIMESTAMP(6),
  ID_HEADER        NUMBER                       NOT NULL
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.BS_FOOTER_PK ON ANAG_USR.BS_FOOTER
(ID_HEADER)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.BS_FOOTER ADD (
  CONSTRAINT BS_FOOTER_PK
  PRIMARY KEY
  (ID_HEADER)
  USING INDEX ANAG_USR.BS_FOOTER_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.RECAPITI_CRI_ONLINE
(
  ID_RECAPITO_ONLINE  NUMBER                    NOT NULL,
  VIA_PIAZZA          VARCHAR2(200 BYTE),
  NUMERO_CIVICO       VARCHAR2(20 BYTE),
  ID_COMUNE           NUMBER,
  TELEFONO            VARCHAR2(50 BYTE),
  EMAIL               VARCHAR2(100 BYTE),
  FAX                 VARCHAR2(50 BYTE),
  CELLULARE           VARCHAR2(50 BYTE),
  PEC                 VARCHAR2(100 BYTE),
  DOMICILIO_DIGITALE  VARCHAR2(100 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.RECAPITI_CRI_ONLINE_PK ON ANAG_USR.RECAPITI_CRI_ONLINE
(ID_RECAPITO_ONLINE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.RECAPITI_CRI_ONLINE ADD (
  CONSTRAINT RECAPITI_CRI_ONLINE_PK
  PRIMARY KEY
  (ID_RECAPITO_ONLINE)
  USING INDEX ANAG_USR.RECAPITI_CRI_ONLINE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CAMBIO_RESIDENZA_ONLINE
(
  ID_CAMBIO_RESIDENZA_ONLINE  NUMBER            NOT NULL,
  DATA_IMMIGRAZIONE           DATE,
  ID_RESIDENZA_ONLINE         NUMBER,
  ID_SOGGETTO_RESIDENTE       NUMBER,
  ID_TIPO_RICHIESTA_CAMBIO    NUMBER,
  ID_COMUNE_PROVENIENZA       NUMBER,
  ID_STATO_PRATICA            NUMBER,
  NUMERO_PRATICA_ONLINE       NUMBER,
  DATA_AGGIORNAMENTO          DATE,
  TIPOLOGIA_CAMBIO            CHAR(1 BYTE),
  ID_RECAPITO_ONLINE          NUMBER,
  ID_CONTRATTO_ABITATIVO      NUMBER,
  ID_LOCALITA_PROVENIENZA     NUMBER,
  CHECK_PROVENIENZA           CHAR(1 BYTE),
  CHECK_DICHIARANTE           CHAR(1 BYTE),
  CHECK_INDIRIZZO             CHAR(1 BYTE),
  CHECK_FAMIGLIA_RES          CHAR(1 BYTE),
  CHECK_FAMIGLIARI            CHAR(1 BYTE),
  CHECK_CONTRATTO_AB          CHAR(1 BYTE),
  CHECK_RECAPITI              CHAR(1 BYTE),
  CHECK_ALLEGATI              CHAR(1 BYTE),
  FLG_ENTRATA_FAMIGLIA        CHAR(1 BYTE),
  FLG_FAMIGLIA_COABITANTE     CHAR(1 BYTE),
  ID_STATO_ESTERO             NUMBER,
  DICHIARAZIONE               BLOB,
  NOME_DICHIARAZIONE          VARCHAR2(80 BYTE),
  CHECK_DOCUMENTAZIONE        VARCHAR2(1 BYTE),
  NOTE_RIGETTO                VARCHAR2(200 BYTE),
  CODICE_TIPO_PROTOCOLLO      VARCHAR2(10 BYTE),
  ANNO_PROTOCOLLO             NUMBER,
  NUMERO_PROTOCOLLO           NUMBER,
  ANNO_PRATICA                NUMBER,
  ID_UTENTE                   NUMBER,
  CODICE_RICHIESTA_ANPR       VARCHAR2(20 BYTE),
  ID_MOTIVO_IRRICEVIBILITA    NUMBER,
  FLG_SOSPESA                 CHAR(1 BYTE),
  FLG_INTEGRATA               CHAR(1 BYTE)
)
LOB (DICHIARAZIONE) STORE AS SECUREFILE (
  TABLESPACE  ANAG_USR
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          104K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_ONLINE.CODICE_TIPO_PROTOCOLLO IS 'Codice identificativo del protocollo di richiesta pratica';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_ONLINE.ANNO_PROTOCOLLO IS 'Anno del protocollo di richiesta pratica';

COMMENT ON COLUMN ANAG_USR.CAMBIO_RESIDENZA_ONLINE.NUMERO_PROTOCOLLO IS 'Numero del protocollo di richiesta pratica';



CREATE UNIQUE INDEX ANAG_USR.CAMBIO_RESIDENZA_ONLINE_PK ON ANAG_USR.CAMBIO_RESIDENZA_ONLINE
(ID_CAMBIO_RESIDENZA_ONLINE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CAMBIO_RESIDENZA_ONLINE ADD (
  CONSTRAINT CAMBIO_RESIDENZA_ONLINE_PK
  PRIMARY KEY
  (ID_CAMBIO_RESIDENZA_ONLINE)
  USING INDEX ANAG_USR.CAMBIO_RESIDENZA_ONLINE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.CAMBIO_RESIDENZA_ONLINE ADD (
  CONSTRAINT COMUNE_PROVENIENZA_FK1 
  FOREIGN KEY (ID_COMUNE_PROVENIENZA) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT CONTRATTO_ABITATIVO_FK1 
  FOREIGN KEY (ID_CONTRATTO_ABITATIVO) 
  REFERENCES ANAG_USR.CONTRATTO_ABITATIVO (ID_CONTRATTO_ABITATIVO)
  ENABLE VALIDATE,
  CONSTRAINT LOCALITA_FK2 
  FOREIGN KEY (ID_LOCALITA_PROVENIENZA) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE,
  CONSTRAINT RECAPITO_FK2 
  FOREIGN KEY (ID_RECAPITO_ONLINE) 
  REFERENCES ANAG_USR.RECAPITI_CRI_ONLINE (ID_RECAPITO_ONLINE)
  ENABLE VALIDATE,
  CONSTRAINT RESIDENZA_ONLINE_FK1 
  FOREIGN KEY (ID_RESIDENZA_ONLINE) 
  REFERENCES ANAG_USR.RESIDENZA_ONLINE (ID_RESIDENZA)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_RESIDENTE_FK1 
  FOREIGN KEY (ID_SOGGETTO_RESIDENTE) 
  REFERENCES ANAG_USR.SOGGETTO_CRI_ONLINE (ID_SOGGETTO_ONLINE)
  ENABLE VALIDATE,
  CONSTRAINT STATO_ESTERO_FK1 
  FOREIGN KEY (ID_STATO_ESTERO) 
  REFERENCES ANAG_USR.CONF_STATO_ESTERO (ID_STATO_ESTERO)
  ENABLE VALIDATE,
  CONSTRAINT STATO_PRATICA_FK2 
  FOREIGN KEY (ID_STATO_PRATICA) 
  REFERENCES ANAG_USR.CONF_STATO_PRATICA (ID_STATO_PRATICA)
  ENABLE VALIDATE,
  CONSTRAINT TIPO_RICHIESTA_CAMBIO_FK2 
  FOREIGN KEY (ID_TIPO_RICHIESTA_CAMBIO) 
  REFERENCES ANAG_USR.CONF_TIPO_RICHIESTA_CAMBIO (ID_TIPO_RICHIESTA_CAMBIO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.SOGGETTO_CRI_ONLINE
(
  ID_SOGGETTO_ONLINE      NUMBER                NOT NULL,
  NOME                    VARCHAR2(250 BYTE),
  COGNOME                 VARCHAR2(250 BYTE),
  CODICE_FISCALE          VARCHAR2(16 BYTE),
  ID_COMUNE_NASCITA       NUMBER,
  ID_LOCALITA_NASCITA     NUMBER,
  ID_STATO_CIVILE         NUMBER,
  ID_CITTADINANZA         NUMBER,
  SESSO                   CHAR(1 BYTE),
  DATA_NASCITA            DATE,
  ID_CONDIZIONE_PROF      VARCHAR2(5 BYTE),
  ID_CONDIZIONE_NON_PROF  NUMBER,
  ID_TITOLO_STUDIO        VARCHAR2(5 BYTE),
  NOME_RESPONSABILE       VARCHAR2(250 BYTE),
  COGNOME_RESPONSABILE    VARCHAR2(250 BYTE),
  TIPO_RESPONSABILE       VARCHAR2(250 BYTE),
  ID_TIPO_LEGAME_APR      NUMBER,
  POSSESSO_AUTOVEICOLI    CHAR(1 BYTE),
  ID_DOCUMENTO_ONLINE     NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.SOGGETTO_CRI_ONLINE_PK ON ANAG_USR.SOGGETTO_CRI_ONLINE
(ID_SOGGETTO_ONLINE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.SOGGETTO_CRI_ONLINE ADD (
  CONSTRAINT SOGGETTO_CRI_ONLINE_PK
  PRIMARY KEY
  (ID_SOGGETTO_ONLINE)
  USING INDEX ANAG_USR.SOGGETTO_CRI_ONLINE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.SOGGETTO_CRI_ONLINE ADD (
  CONSTRAINT CITTADINANZA_FK2 
  FOREIGN KEY (ID_CITTADINANZA) 
  REFERENCES ANAG_USR.CITTADINANZA (ID_CITTADINANZA)
  ENABLE VALIDATE,
  CONSTRAINT COMUNE_NASCITA_FK1 
  FOREIGN KEY (ID_COMUNE_NASCITA) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT COND_NON_PROF_FK1 
  FOREIGN KEY (ID_CONDIZIONE_NON_PROF) 
  REFERENCES ANAG_USR.CONF_COND_NON_PROFESSIONALE (ID_COND_NON_PROFESSIONALE_ANPR)
  ENABLE VALIDATE,
  CONSTRAINT LOCALITA_NASCITA_FK1 
  FOREIGN KEY (ID_LOCALITA_NASCITA) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_CRI_ONLINE_FK1 
  FOREIGN KEY (ID_TITOLO_STUDIO) 
  REFERENCES ANAG_USR.CONF_TITOLI_STUDIO (ID_TITOLO_STUDIO_ANPR)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_CRI_ONLINE_FK2 
  FOREIGN KEY (ID_DOCUMENTO_ONLINE) 
  REFERENCES ANAG_USR.DOCUMENTO_CRI_ONLINE (ID_DOCUMENTO_ONLINE)
  ENABLE VALIDATE,
  CONSTRAINT STATO_CIVILE_FK2 
  FOREIGN KEY (ID_STATO_CIVILE) 
  REFERENCES ANAG_USR.CONF_STATO_CIVILE (ID_STATO_CIVILE)
  ENABLE VALIDATE,
  FOREIGN KEY (ID_CONDIZIONE_PROF) 
  REFERENCES ANAG_USR.CONF_POSIZIONE_PROFESSIONALE (ID_POS_PROFESSIONALE_ANPR)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.VEICOLI_CRI_ONLINE
(
  ID_VEICOLO                  NUMBER            NOT NULL,
  TARGA                       VARCHAR2(200 BYTE),
  ID_TIPO_VEICOLO             NUMBER,
  ID_SOGGETTO_CRI_ONLINE      NUMBER,
  ID_CAMBIO_RESIDENZA_ONLINE  NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.VEICOLI_CRI_ONLINE_PK ON ANAG_USR.VEICOLI_CRI_ONLINE
(ID_VEICOLO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.VEICOLI_CRI_ONLINE ADD (
  CONSTRAINT VEICOLI_CRI_ONLINE_PK
  PRIMARY KEY
  (ID_VEICOLO)
  USING INDEX ANAG_USR.VEICOLI_CRI_ONLINE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.VEICOLI_CRI_ONLINE ADD (
  CONSTRAINT VEICOLI_CRI_ONLINE_FK1 
  FOREIGN KEY (ID_TIPO_VEICOLO) 
  REFERENCES ANAG_USR.CONF_TIPO_VEICOLO (ID_TIPO_VEICOLO)
  ENABLE VALIDATE,
  CONSTRAINT VEICOLI_CRI_ONLINE_FK2 
  FOREIGN KEY (ID_SOGGETTO_CRI_ONLINE) 
  REFERENCES ANAG_USR.SOGGETTO_CRI_ONLINE (ID_SOGGETTO_ONLINE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.RESIDENZA_ONLINE
(
  ID_RESIDENZA         NUMBER                   NOT NULL,
  ID_TOPONIMO          NUMBER,
  NUMERO_CIVICO        NUMBER,
  LETTERA              VARCHAR2(10 BYTE),
  ESPONENTE            VARCHAR2(20 BYTE),
  CAP                  VARCHAR2(6 BYTE),
  METRICO              NUMBER(6),
  LOTTO                VARCHAR2(20 BYTE),
  PALAZZINA            VARCHAR2(20 BYTE),
  FLG_PALAZZINA_UNICA  CHAR(1 BYTE),
  SCALA                VARCHAR2(4 BYTE),
  PIANO                VARCHAR2(5 BYTE),
  INTERNO              VARCHAR2(4 BYTE),
  SEZIONE              VARCHAR2(26 BYTE),
  FOGLIO               VARCHAR2(26 BYTE),
  PARTICELLA           VARCHAR2(26 BYTE),
  SUBALTERNO           VARCHAR2(26 BYTE),
  ID_MUNICIPIO         NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.RESIDENZA_ONLINE_PK ON ANAG_USR.RESIDENZA_ONLINE
(ID_RESIDENZA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.RESIDENZA_ONLINE ADD (
  CONSTRAINT RESIDENZA_ONLINE_PK
  PRIMARY KEY
  (ID_RESIDENZA)
  USING INDEX ANAG_USR.RESIDENZA_ONLINE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.RESIDENZA_ONLINE ADD (
  CONSTRAINT MUNICIPIO_FK1 
  FOREIGN KEY (ID_MUNICIPIO) 
  REFERENCES ANAG_USR.CONF_MUNICIPIO (ID_MUNICIPIO)
  ENABLE VALIDATE,
  CONSTRAINT TOPONIMO_FK1 
  FOREIGN KEY (ID_TOPONIMO) 
  REFERENCES ANAG_USR.TOPONIMO (ID_TOPONIMO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_SOGGETTO_CRI_ONLINE
(
  ID_SOGGETTO_ONLINE          NUMBER            NOT NULL,
  ID_CAMBIO_RESIDENZA_ONLINE  NUMBER            NOT NULL,
  FLAG_DICHIARANTE            CHAR(1 BYTE),
  FLAG_LAVORATO               NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.R_SOGGETTTO_CRI_ONLINE_PK ON ANAG_USR.R_SOGGETTO_CRI_ONLINE
(ID_SOGGETTO_ONLINE, ID_CAMBIO_RESIDENZA_ONLINE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_SOGGETTO_CRI_ONLINE ADD (
  CONSTRAINT R_SOGGETTTO_CRI_ONLINE_PK
  PRIMARY KEY
  (ID_SOGGETTO_ONLINE, ID_CAMBIO_RESIDENZA_ONLINE)
  USING INDEX ANAG_USR.R_SOGGETTTO_CRI_ONLINE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_SOGGETTO_CRI_ONLINE ADD (
  CONSTRAINT CAMBIO_RESIDENZA_ONLINE_FK1 
  FOREIGN KEY (ID_CAMBIO_RESIDENZA_ONLINE) 
  REFERENCES ANAG_USR.CAMBIO_RESIDENZA_ONLINE (ID_CAMBIO_RESIDENZA_ONLINE)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTTO_CRI_ONLINE_FK1 
  FOREIGN KEY (ID_SOGGETTO_ONLINE) 
  REFERENCES ANAG_USR.SOGGETTO_CRI_ONLINE (ID_SOGGETTO_ONLINE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_SOGGETTI_PATENTI_ONLINE
(
  ID_PATENTE_ONLINE           NUMBER,
  ID_SOGGETTO_ONLINE          NUMBER,
  CATEGORIA                   VARCHAR2(20 BYTE),
  DATA_RILASCIO               DATE,
  DATA_SCADENZA               DATE,
  ID_CAMBIO_RESIDENZA_ONLINE  NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


ALTER TABLE ANAG_USR.R_SOGGETTI_PATENTI_ONLINE ADD (
  CONSTRAINT R_SOGGETTI_PATENTI_ONLINE_FK1 
  FOREIGN KEY (ID_PATENTE_ONLINE) 
  REFERENCES ANAG_USR.PATENTE_CRI_ONLINE (ID_PATENTE)
  ENABLE VALIDATE,
  CONSTRAINT R_SOGGETTI_PATENTI_ONLINE_FK2 
  FOREIGN KEY (ID_SOGGETTO_ONLINE) 
  REFERENCES ANAG_USR.SOGGETTO_CRI_ONLINE (ID_SOGGETTO_ONLINE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.DOCUMENTO_CRI_ONLINE
(
  ID_DOCUMENTO_ONLINE       NUMBER              NOT NULL,
  ID_TIPO_DOCUMENTO_ONLINE  NUMBER,
  NUMERO_DOCUMENTO          VARCHAR2(26 BYTE),
  DATA_RILASCIO             DATE,
  DATA_SCADENZA             DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.DOCUMENTO_CRI_ONLINE_PK ON ANAG_USR.DOCUMENTO_CRI_ONLINE
(ID_DOCUMENTO_ONLINE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.DOCUMENTO_CRI_ONLINE ADD (
  CONSTRAINT DOCUMENTO_CRI_ONLINE_PK
  PRIMARY KEY
  (ID_DOCUMENTO_ONLINE)
  USING INDEX ANAG_USR.DOCUMENTO_CRI_ONLINE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.DOCUMENTO_CRI_ONLINE ADD (
  CONSTRAINT DOCUMENTO_CRI_ONLINE_FK1 
  FOREIGN KEY (ID_TIPO_DOCUMENTO_ONLINE) 
  REFERENCES ANAG_USR.CONF_TIPO_DOCUMENTO_ONLINE (ID_TIPO_DOCUMENTO_ONLINE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_DOCUMENTO_ONLINE
(
  ID_TIPO_DOCUMENTO_ONLINE  NUMBER              NOT NULL,
  DESCRIZIONE               VARCHAR2(26 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_DOCUMENTO_ONLINE_PK ON ANAG_USR.CONF_TIPO_DOCUMENTO_ONLINE
(ID_TIPO_DOCUMENTO_ONLINE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_DOCUMENTO_ONLINE ADD (
  CONSTRAINT CONF_TIPO_DOCUMENTO_ONLINE_PK
  PRIMARY KEY
  (ID_TIPO_DOCUMENTO_ONLINE)
  USING INDEX ANAG_USR.CONF_TIPO_DOCUMENTO_ONLINE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.PATENTE_CRI_ONLINE
(
  ID_PATENTE                NUMBER              NOT NULL,
  NUMERO_PATENTE            VARCHAR2(40 BYTE),
  ID_STATO_VALIDITA         NUMBER,
  DATA_RILASCIO             DATE,
  ID_COMUNE                 NUMBER,
  ID_ENTE_RILASCIO_PATENTE  NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.PATENTE_CRI_ONLINE_PK ON ANAG_USR.PATENTE_CRI_ONLINE
(ID_PATENTE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.PATENTE_CRI_ONLINE ADD (
  CONSTRAINT PATENTE_CRI_ONLINE_PK
  PRIMARY KEY
  (ID_PATENTE)
  USING INDEX ANAG_USR.PATENTE_CRI_ONLINE_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.PATENTE_CRI_ONLINE ADD (
  CONSTRAINT PATENTE_CRI_ONLINE_FK1 
  FOREIGN KEY (ID_STATO_VALIDITA) 
  REFERENCES ANAG_USR.CONF_STATO_VALIDITA_PATENTE (ID_STATO_VALIDITA_PATENTE)
  ENABLE VALIDATE,
  CONSTRAINT PATENTE_CRI_ONLINE_FK2 
  FOREIGN KEY (ID_ENTE_RILASCIO_PATENTE) 
  REFERENCES ANAG_USR.CONF_ENTE_RILASCIO_PATENTE (ID_ENTE_RILASCIO_PATENTE)
  ENABLE VALIDATE,
  CONSTRAINT PATENTE_CRI_ONLINE_FK3 
  FOREIGN KEY (ID_COMUNE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_MORTE
(
  ID_TIPO_MORTE  NUMBER                         NOT NULL,
  DESCRIZIONE    VARCHAR2(50 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE ANAG_USR.CONF_TIPO_MORTE IS 'Tipologica che contiene le informazioni di tipologia morte.';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_MORTE.ID_TIPO_MORTE IS 'Codice identificativo della tipologia di morte che è possibile dichiarare per un soggetto.';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_MORTE.DESCRIZIONE IS 'Descrizione della tipologia di morte che è possibile dichiarare per un soggetto.';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_MORTE_PK ON ANAG_USR.CONF_TIPO_MORTE
(ID_TIPO_MORTE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_MORTE ADD (
  CONSTRAINT CONF_TIPO_MORTE_PK
  PRIMARY KEY
  (ID_TIPO_MORTE)
  USING INDEX ANAG_USR.CONF_TIPO_MORTE_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.GESTIONE_SPT
(
  ID_GESTIONE_SPT          NUMBER               NOT NULL,
  ID_SOGGETTO              NUMBER               NOT NULL,
  ID_PROVINCIA_ISCRIZIONE  NUMBER,
  ID_COMUNE_ISCRIZIONE     NUMBER               NOT NULL,
  INDIRIZZO_ISCRIZIONE     VARCHAR2(200 BYTE),
  DATA_ISCRIZIONE          DATE,
  NOTE                     VARCHAR2(4000 BYTE),
  FLG_ATTIVO               VARCHAR2(1 BYTE),
  DATA_CANC_SPT            DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.GESTIONE_SPT.ID_GESTIONE_SPT IS 'Identificativo SPT';

COMMENT ON COLUMN ANAG_USR.GESTIONE_SPT.ID_SOGGETTO IS 'Soggetto SPT';

COMMENT ON COLUMN ANAG_USR.GESTIONE_SPT.ID_PROVINCIA_ISCRIZIONE IS 'Provincia di iscrizione SPT';

COMMENT ON COLUMN ANAG_USR.GESTIONE_SPT.ID_COMUNE_ISCRIZIONE IS 'Comune di iscrizione SPT';

COMMENT ON COLUMN ANAG_USR.GESTIONE_SPT.INDIRIZZO_ISCRIZIONE IS 'Indirizzo di iscrizione SPT';

COMMENT ON COLUMN ANAG_USR.GESTIONE_SPT.DATA_ISCRIZIONE IS 'Data di iscrizione SPT';

COMMENT ON COLUMN ANAG_USR.GESTIONE_SPT.FLG_ATTIVO IS 'S -> ATTIVA N -> NON ATTIVA';



CREATE UNIQUE INDEX ANAG_USR.GESTIONE_SPT_PK ON ANAG_USR.GESTIONE_SPT
(ID_GESTIONE_SPT)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.GESTIONE_SPT ADD (
  CONSTRAINT GESTIONE_SPT_PK
  PRIMARY KEY
  (ID_GESTIONE_SPT)
  USING INDEX ANAG_USR.GESTIONE_SPT_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.GESTIONE_SPT ADD (
  CONSTRAINT ID_COMUNE_GESTIONE_SPT_FK 
  FOREIGN KEY (ID_COMUNE_ISCRIZIONE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT ID_PROVINCIA_GESTIONE_SPT_FK 
  FOREIGN KEY (ID_PROVINCIA_ISCRIZIONE) 
  REFERENCES ANAG_USR.PROVINCIA (ID_PROVINCIA)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_GESTIONE_SPT_FK 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.TMP_PDZ2
(
  INDIRIZZO  VARCHAR2(40 BYTE),
  CIVICO     VARCHAR2(30 BYTE),
  NUMERO     VARCHAR2(30 BYTE),
  LETTERA    VARCHAR2(30 BYTE),
  DEN_PDZ    VARCHAR2(40 BYTE),
  COD_PDZ    VARCHAR2(40 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;
CREATE TABLE ANAG_USR.TRASFORMA_COD_IND
(
  ID_SOGGETTO_USR  NUMBER,
  COD_IND_VECCHIO  VARCHAR2(7 BYTE),
  COD_IND_NUOVO    VARCHAR2(7 BYTE),
  ESITO            VARCHAR2(2 BYTE),
  DATA_OPERAZIONE  DATE,
  NUMERO_RECORD    NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.TRASFORMA_COD_IND.ID_SOGGETTO_USR IS 'id_soggetto di anag_usr a cui è stato trasormato il codice_indivuale';

COMMENT ON COLUMN ANAG_USR.TRASFORMA_COD_IND.COD_IND_VECCHIO IS 'codice individuale prima della trasformazione';

COMMENT ON COLUMN ANAG_USR.TRASFORMA_COD_IND.COD_IND_NUOVO IS 'codice individuale dopo la trasformazione';

COMMENT ON COLUMN ANAG_USR.TRASFORMA_COD_IND.ESITO IS 'indica se la trasformazione dello storico è andata a buon fine';

COMMENT ON COLUMN ANAG_USR.TRASFORMA_COD_IND.DATA_OPERAZIONE IS 'data in cui è stata effettuata la trasformazione';

COMMENT ON COLUMN ANAG_USR.TRASFORMA_COD_IND.NUMERO_RECORD IS 'indica quanti record storici sono stati trasformati al momento della richiesta';
CREATE TABLE ANAG_USR.TESTO_CONVENZIONE_PATRIMONIALE
(
  ID_TESTO_CONVENZIONE  NUMBER                  NOT NULL,
  ID_TIPO_CONVENZIONE   NUMBER,
  ID_VALIDANTE          NUMBER,
  TESTO_CONVENZIONE     VARCHAR2(500 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.TESTO_CONVENZIONE_PATRIMONIALE.ID_TESTO_CONVENZIONE IS 'Identificativo';

COMMENT ON COLUMN ANAG_USR.TESTO_CONVENZIONE_PATRIMONIALE.ID_TIPO_CONVENZIONE IS 'Identificativo del tipo di convenzione';

COMMENT ON COLUMN ANAG_USR.TESTO_CONVENZIONE_PATRIMONIALE.ID_VALIDANTE IS 'Identificativo del validante della convenzione';

COMMENT ON COLUMN ANAG_USR.TESTO_CONVENZIONE_PATRIMONIALE.TESTO_CONVENZIONE IS 'Testo dell''anotazione marginal sulla convenzione';



CREATE UNIQUE INDEX ANAG_USR.TESTO_CONVENZIONE_PATRIMON_PK ON ANAG_USR.TESTO_CONVENZIONE_PATRIMONIALE
(ID_TESTO_CONVENZIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.TESTO_CONVENZIONE_PATRIMONIALE ADD (
  CONSTRAINT TESTO_CONVENZIONE_PATRIMON_PK
  PRIMARY KEY
  (ID_TESTO_CONVENZIONE)
  USING INDEX ANAG_USR.TESTO_CONVENZIONE_PATRIMON_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CAPPARIO_STRADA_RC
(
  COD_TOPONIMO             VARCHAR2(6 BYTE),
  COD_SPECIE               NUMBER(4),
  SPECIE                   VARCHAR2(30 BYTE),
  SPECIE_FONTE             NUMBER(1),
  DENOMINAZIONE_TOPONIMO   VARCHAR2(200 CHAR),
  TOPONIMO_FONTE           NUMBER(1),
  ID_TIPO_SPECIE_TOPONIMO  NUMBER,
  ID_STRADA                VARCHAR2(20 BYTE),
  CAP                      VARCHAR2(5 BYTE),
  MULTI_CAP                VARCHAR2(1 BYTE),
  TIPO_NUM                 CHAR(1 BYTE),
  NUM_DAL                  NUMBER,
  NUM_AL                   NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE INDEX ANAG_USR.CAPPARIO_STRADA_CODTOP_IDX ON ANAG_USR.CAPPARIO_STRADA_RC
(COD_TOPONIMO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;
CREATE TABLE ANAG_USR.CAPPARIO_COMUNI
(
  ID                       NUMBER,
  ID_PROVINCIA             NUMBER,
  DENOMINAZIONE_STD        VARCHAR2(400 CHAR),
  DENOMINAZIONE_APICI_STD  VARCHAR2(400 CHAR),
  DENOM_ABBREV_STD         VARCHAR2(400 CHAR),
  COD_ISTAT                VARCHAR2(6 CHAR),
  ID_PRINCIPALE            NUMBER,
  MULTI_CAP                VARCHAR2(1 CHAR),
  CAP                      VARCHAR2(5 CHAR),
  CODICE_BELFIORE          VARCHAR2(4 CHAR),
  CODICE_CAB               VARCHAR2(5 CHAR)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE INDEX ANAG_USR.CAPPARIO_COMUNI_ISTAT_IDX ON ANAG_USR.CAPPARIO_COMUNI
(COD_ISTAT)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


CREATE UNIQUE INDEX ANAG_USR.CAPPARIO_COMUNI_PK ON ANAG_USR.CAPPARIO_COMUNI
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CAPPARIO_COMUNI ADD (
  CONSTRAINT CAPPARIO_COMUNI_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CAPPARIO_COMUNI_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.TFISCOD
(
  CODICE_INDIVIDUALE  VARCHAR2(20 BYTE),
  CODICE_FISCALE      VARCHAR2(20 BYTE),
  DATA_OPERAZIONE     DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;
CREATE TABLE ANAG_USR.R_SOGGETTO_CITTADINANZA
(
  ID_SOGGETTO        NUMBER,
  ID_ATTO            NUMBER,
  DATA_CITTADINANZA  DATE,
  DATA_OPERAZIONE    DATE,
  ID_UTENTE          NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


ALTER TABLE ANAG_USR.R_SOGGETTO_CITTADINANZA ADD (
  CONSTRAINT R_SOGGETTO_CITTADINANZA_FK1 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT R_SOGGETTO_CITTADINANZA_FK2 
  FOREIGN KEY (ID_ATTO) 
  REFERENCES ANAG_USR.ATTO (ID_ATTO)
  ENABLE VALIDATE,
  CONSTRAINT R_SOGGETTO_CITTADINANZA_FK3 
  FOREIGN KEY (ID_UTENTE) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.SEPA30
(
  ID               NUMBER                       NOT NULL,
  ID_MATRIMONIO    NUMBER,
  ID_UNIONE        NUMBER,
  LEGGE            VARCHAR2(500 BYTE),
  DATA_OPERAZIONE  DATE,
  ID_UTENTE        NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.SEPA30_PK ON ANAG_USR.SEPA30
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.SEPA30 ADD (
  CONSTRAINT SEPA30_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.SEPA30_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.SEPA30 ADD (
  CONSTRAINT SEPA30_FK1 
  FOREIGN KEY (ID_MATRIMONIO) 
  REFERENCES ANAG_USR.MATRIMONIO (ID_MATRIMONIO)
  ENABLE VALIDATE,
  CONSTRAINT SEPA30_FK2 
  FOREIGN KEY (ID_UNIONE) 
  REFERENCES ANAG_USR.UNIONECIVILE (ID_UNIONE)
  ENABLE VALIDATE,
  CONSTRAINT SEPA30_FK3 
  FOREIGN KEY (ID_UTENTE) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_CONVENZIONE_MATRIMONIO
(
  ID_MATRIMONIO      NUMBER                     NOT NULL,
  ID_SENTENZA        NUMBER,
  ID_UTENTE          NUMBER,
  ID_ORGANIZZAZIONE  NUMBER,
  DATA_INSERIMENTO   DATE,
  FLAG_MIGRAZIONE    VARCHAR2(1 BYTE),
  TESTO_MIGRAZIONE   VARCHAR2(3999 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.R_CONVENZIONE_MATRIMONIO.ID_MATRIMONIO IS 'Identificativo del matrimonio';

COMMENT ON COLUMN ANAG_USR.R_CONVENZIONE_MATRIMONIO.ID_SENTENZA IS 'Identificativo della convenzione patrimoniale';

COMMENT ON COLUMN ANAG_USR.R_CONVENZIONE_MATRIMONIO.ID_UTENTE IS 'Utente che ha inserito la convenzione';

COMMENT ON COLUMN ANAG_USR.R_CONVENZIONE_MATRIMONIO.ID_ORGANIZZAZIONE IS 'Organizazzione dell''utente che ha inserito la convenzione';

COMMENT ON COLUMN ANAG_USR.R_CONVENZIONE_MATRIMONIO.DATA_INSERIMENTO IS 'Data di inserimento a sistema della convenzione';

COMMENT ON COLUMN ANAG_USR.R_CONVENZIONE_MATRIMONIO.FLAG_MIGRAZIONE IS 'S -> Migrazione Stato Civile, N -> No';

COMMENT ON COLUMN ANAG_USR.R_CONVENZIONE_MATRIMONIO.TESTO_MIGRAZIONE IS 'Testo convenzione per record migrati stato civile';



ALTER TABLE ANAG_USR.R_CONVENZIONE_MATRIMONIO ADD (
  CONSTRAINT ID_MATRIMONIO_FK 
  FOREIGN KEY (ID_MATRIMONIO) 
  REFERENCES ANAG_USR.MATRIMONIO (ID_MATRIMONIO)
  ENABLE VALIDATE,
  CONSTRAINT ID_SENTENZA_FK 
  FOREIGN KEY (ID_SENTENZA) 
  REFERENCES ANAG_USR.SENTENZA (ID_SENTENZA)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.ESTRAZIONE_ELETTORI_FUORI_ROMA
(
  ID_ESTRAZIONE    NUMBER                       NOT NULL,
  PROGRESSIVO      VARCHAR2(20 BYTE),
  ANNO             NUMBER,
  SEMESTRE         NUMBER,
  TOTALE_SOGGETTI  VARCHAR2(20 BYTE),
  ID_UTENTE        NUMBER,
  DATA_OPERAZIONE  VARCHAR2(20 BYTE),
  FLG_INVIO_MAIL   CHAR(1 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.ESTRAZIONE_ELETTORI_FUORI_ROMA.ID_ESTRAZIONE IS 'Identificativo estrazione';

COMMENT ON COLUMN ANAG_USR.ESTRAZIONE_ELETTORI_FUORI_ROMA.PROGRESSIVO IS 'Codice progressivo dell''estrazione';

COMMENT ON COLUMN ANAG_USR.ESTRAZIONE_ELETTORI_FUORI_ROMA.ANNO IS 'Anno del''estrazione';

COMMENT ON COLUMN ANAG_USR.ESTRAZIONE_ELETTORI_FUORI_ROMA.SEMESTRE IS 'Primo o secondo semestre';

COMMENT ON COLUMN ANAG_USR.ESTRAZIONE_ELETTORI_FUORI_ROMA.TOTALE_SOGGETTI IS 'Totale dei soggetti estratti per estrazione';

COMMENT ON COLUMN ANAG_USR.ESTRAZIONE_ELETTORI_FUORI_ROMA.ID_UTENTE IS 'Identificativo dell''utente';

COMMENT ON COLUMN ANAG_USR.ESTRAZIONE_ELETTORI_FUORI_ROMA.DATA_OPERAZIONE IS 'Data in cui è stata creata l''estrazione';

COMMENT ON COLUMN ANAG_USR.ESTRAZIONE_ELETTORI_FUORI_ROMA.FLG_INVIO_MAIL IS 'Flag per mostrare il pulsante di invio mail';



CREATE UNIQUE INDEX ANAG_USR.ESTRAZIONE_ELETTORI_PK ON ANAG_USR.ESTRAZIONE_ELETTORI_FUORI_ROMA
(ID_ESTRAZIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.ESTRAZIONE_ELETTORI_FUORI_ROMA ADD (
  CONSTRAINT ESTRAZIONE_ELETTORI_PK
  PRIMARY KEY
  (ID_ESTRAZIONE)
  USING INDEX ANAG_USR.ESTRAZIONE_ELETTORI_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.ESTRAZIONE_ELETTORI_FUORI_ROMA ADD (
  CONSTRAINT ESTRAZIONE_ELETTORI_FUORI_FK1 
  FOREIGN KEY (ID_UTENTE) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA
(
  ID_R_COMUNICAZIONE     NUMBER                 NOT NULL,
  ID_SOGGETTO            NUMBER,
  CODICE_INDIVIDUALE     VARCHAR2(20 BYTE),
  PROGRESSIVO            NUMBER,
  COGNOME                VARCHAR2(200 BYTE),
  NOME                   VARCHAR2(200 BYTE),
  DATA_NASCITA           DATE,
  SESSO                  VARCHAR2(1 BYTE),
  ID_COMUNE_NASCITA      NUMBER,
  ID_LOCALITA_NASCITA    NUMBER,
  NUMERO_ATTO            VARCHAR2(20 BYTE),
  PARTE                  VARCHAR2(20 BYTE),
  SERIE                  VARCHAR2(20 BYTE),
  ANNO_ATTO              NUMBER,
  ESITO_MAIL             VARCHAR2(2 BYTE),
  ID_ESTRAZIONE          NUMBER,
  ID_COMUNE_EMIGRAZIONE  NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA.ID_R_COMUNICAZIONE IS 'Identificativo di tabella';

COMMENT ON COLUMN ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA.ID_SOGGETTO IS 'Identificativo del soggetto';

COMMENT ON COLUMN ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA.CODICE_INDIVIDUALE IS 'Codice Individuale del soggetto';

COMMENT ON COLUMN ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA.PROGRESSIVO IS 'Progressivo del record';

COMMENT ON COLUMN ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA.COGNOME IS 'Fotografia del cognome al momento dell''estrazione';

COMMENT ON COLUMN ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA.NOME IS 'Fotografia del nome al momento dell''estrazione';

COMMENT ON COLUMN ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA.DATA_NASCITA IS 'Fotografia della data di nascita al momento dell''estrazione';

COMMENT ON COLUMN ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA.SESSO IS 'Fotografia del sesso al momento dell''estrazione';

COMMENT ON COLUMN ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA.ID_COMUNE_NASCITA IS 'Fotografia del comune di nascita al momento dell''estrazione';

COMMENT ON COLUMN ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA.ID_LOCALITA_NASCITA IS 'Fotografia della località di nascita al momento dell''estrazione';

COMMENT ON COLUMN ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA.NUMERO_ATTO IS 'Fotografia del numero dell''atto al momento dell''estrazione';

COMMENT ON COLUMN ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA.PARTE IS 'Fotografia della parte dell''atto al momento dell''estrazione';

COMMENT ON COLUMN ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA.SERIE IS 'Fotografia della serie dell''atto al momento dell''estrazione';

COMMENT ON COLUMN ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA.ANNO_ATTO IS 'Fotografia dell''anno dell''atto al momento dell''estrazione';

COMMENT ON COLUMN ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA.ESITO_MAIL IS 'Esito invio mail CrabMail';

COMMENT ON COLUMN ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA.ID_ESTRAZIONE IS 'Identificativo dell''estrazione associata alla posizione';

COMMENT ON COLUMN ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA.ID_COMUNE_EMIGRAZIONE IS 'Identificativo del comune di emigrazione';



CREATE UNIQUE INDEX ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA_PK ON ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA
(ID_R_COMUNICAZIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA ADD (
  CONSTRAINT R_COMUNICAZIONE_FUORI_ROMA_PK
  PRIMARY KEY
  (ID_R_COMUNICAZIONE)
  USING INDEX ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_COMUNICAZIONE_FUORI_ROMA ADD (
  CONSTRAINT R_COMUNICAZIONE_FUORI_ROM_FK1 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE,
  CONSTRAINT R_COMUNICAZIONE_FUORI_ROM_FK2 
  FOREIGN KEY (ID_COMUNE_NASCITA) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT R_COMUNICAZIONE_FUORI_ROM_FK3 
  FOREIGN KEY (ID_LOCALITA_NASCITA) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE,
  CONSTRAINT R_COMUNICAZIONE_FUORI_ROM_FK4 
  FOREIGN KEY (ID_ESTRAZIONE) 
  REFERENCES ANAG_USR.ESTRAZIONE_ELETTORI_FUORI_ROMA (ID_ESTRAZIONE)
  ENABLE VALIDATE,
  CONSTRAINT R_COMUNICAZIONE_FUORI_ROM_FK5 
  FOREIGN KEY (ID_COMUNE_EMIGRAZIONE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.FUSIONE_ANAGRAFICA
(
  ID_FUSIONE                    NUMBER          NOT NULL,
  ID_SOGGETTO_ELIMINATO         NUMBER,
  ID_SOGGETTO_TENUTO            NUMBER,
  CODICE_INDIVIDUALE_ELIMINATO  VARCHAR2(7 BYTE),
  CODICE_INDIVIDUALE_TENUTO     VARCHAR2(7 BYTE),
  DATA_OPERAZIONE               DATE,
  ID_UTENTE                     NUMBER
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.FUSIONE_ANAGRAFICA.ID_FUSIONE IS 'Identificativo della fusione';

COMMENT ON COLUMN ANAG_USR.FUSIONE_ANAGRAFICA.ID_SOGGETTO_TENUTO IS 'Identificativo del soggetto tenuto';

COMMENT ON COLUMN ANAG_USR.FUSIONE_ANAGRAFICA.CODICE_INDIVIDUALE_ELIMINATO IS 'Codice individuale eliminato';

COMMENT ON COLUMN ANAG_USR.FUSIONE_ANAGRAFICA.DATA_OPERAZIONE IS 'Data dell''operazione';

COMMENT ON COLUMN ANAG_USR.FUSIONE_ANAGRAFICA.ID_UTENTE IS 'Identificativo dell''operatore';



CREATE UNIQUE INDEX ANAG_USR.FUSIONE_ANAGRAFICA_PK ON ANAG_USR.FUSIONE_ANAGRAFICA
(ID_FUSIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.FUSIONE_ANAGRAFICA ADD (
  CONSTRAINT FUSIONE_ANAGRAFICA_PK
  PRIMARY KEY
  (ID_FUSIONE)
  USING INDEX ANAG_USR.FUSIONE_ANAGRAFICA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.MEFA_MUFA
(
  ID_GESTIONE_MEFA_MUFA  NUMBER                 NOT NULL,
  ID_SOGGETTO            NUMBER                 NOT NULL,
  NUMERO_PRATICA_CRI     NUMBER,
  ANNO_PRATICA_CRI       NUMBER,
  ID_FAMIGLIA_CONV       NUMBER                 NOT NULL,
  DATA_DEC               DATE,
  ID_SOGGETTO_STORICO    NUMBER,
  INDIRIZZO_ENTRATA      VARCHAR2(200 CHAR)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.MEFA_MUFA.ID_GESTIONE_MEFA_MUFA IS 'Identificativo SPT';

COMMENT ON COLUMN ANAG_USR.MEFA_MUFA.ID_SOGGETTO IS 'Soggetto MEFA_MUFA';

COMMENT ON COLUMN ANAG_USR.MEFA_MUFA.NUMERO_PRATICA_CRI IS 'NUMERO PRATICA CRI PRECEDENTE';

COMMENT ON COLUMN ANAG_USR.MEFA_MUFA.ANNO_PRATICA_CRI IS 'ANNO PRATICA CRI PRECEDENTE';

COMMENT ON COLUMN ANAG_USR.MEFA_MUFA.ID_FAMIGLIA_CONV IS 'FAMIGLIA POST_MEFA_MUFA';

COMMENT ON COLUMN ANAG_USR.MEFA_MUFA.DATA_DEC IS 'DATA DECORRENZA LEGAME FAM CONV';

COMMENT ON COLUMN ANAG_USR.MEFA_MUFA.ID_SOGGETTO_STORICO IS 'ID SOGGETTO STORICIZZATO';

COMMENT ON COLUMN ANAG_USR.MEFA_MUFA.INDIRIZZO_ENTRATA IS 'INDIRIZZO DELLA FAMIGLIA IN CUI IL SOGGETTO ENTRA CON IL MEFA MUFA';



CREATE UNIQUE INDEX ANAG_USR.MEFA_MUFA_PK ON ANAG_USR.MEFA_MUFA
(ID_GESTIONE_MEFA_MUFA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.MEFA_MUFA ADD (
  CONSTRAINT MEFA_MUFA_PK
  PRIMARY KEY
  (ID_GESTIONE_MEFA_MUFA)
  USING INDEX ANAG_USR.MEFA_MUFA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.MEFA_MUFA ADD (
  CONSTRAINT ID_FAMIGLIA_CONV_MEFA_MUFA_FK 
  FOREIGN KEY (ID_FAMIGLIA_CONV) 
  REFERENCES ANAG_USR.FAMIGLIA_CONVIVENZA (ID_FAMIGLIA_CONV)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_MEFA_MUFA_FK 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CREAZIONE_INDIVIDUO
(
  ID                         NUMBER             NOT NULL,
  ID_SOGGETTO                NUMBER,
  ID_TIPO_CREAZIONE          NUMBER,
  DATA_OPERAZIONE            DATE,
  ID_UTENTE                  NUMBER,
  DATA_DECORRENZA_RESIDENZA  DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CREAZIONE_INDIVIDUO.ID IS 'Identificativo';

COMMENT ON COLUMN ANAG_USR.CREAZIONE_INDIVIDUO.ID_SOGGETTO IS 'Identificativo del soggetto';

COMMENT ON COLUMN ANAG_USR.CREAZIONE_INDIVIDUO.ID_TIPO_CREAZIONE IS 'Identificativo del tipo di creazione dell''individuo';

COMMENT ON COLUMN ANAG_USR.CREAZIONE_INDIVIDUO.DATA_OPERAZIONE IS 'Data dell''operazione';

COMMENT ON COLUMN ANAG_USR.CREAZIONE_INDIVIDUO.ID_UTENTE IS 'Identificativo dell''operatore';

COMMENT ON COLUMN ANAG_USR.CREAZIONE_INDIVIDUO.DATA_DECORRENZA_RESIDENZA IS 'Data decorrenza della residenza se si creano soggetti residenti o AIRE';



CREATE UNIQUE INDEX ANAG_USR.CREAZIONE_INDIVIDUO_PK ON ANAG_USR.CREAZIONE_INDIVIDUO
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CREAZIONE_INDIVIDUO ADD (
  CONSTRAINT CREAZIONE_INDIVIDUO_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CREAZIONE_INDIVIDUO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_CREAZIONE_INDIVIDUO
(
  ID_TIPO_CREAZIONE  NUMBER                     NOT NULL,
  DESCRIZIONE        VARCHAR2(500 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_CREAZIONE_INDIVIDUO.ID_TIPO_CREAZIONE IS 'Identificativo';

COMMENT ON COLUMN ANAG_USR.CONF_CREAZIONE_INDIVIDUO.DESCRIZIONE IS 'Descrizione';



CREATE UNIQUE INDEX ANAG_USR.CONF_CREAZIONE_INDIVIDUO_PK ON ANAG_USR.CONF_CREAZIONE_INDIVIDUO
(ID_TIPO_CREAZIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_CREAZIONE_INDIVIDUO ADD (
  CONSTRAINT CONF_CREAZIONE_INDIVIDUO_PK
  PRIMARY KEY
  (ID_TIPO_CREAZIONE)
  USING INDEX ANAG_USR.CONF_CREAZIONE_INDIVIDUO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_OPERAZIONE_LEVA
(
  ID_OPERAZIONE_LEVA  NUMBER                    NOT NULL,
  DESCRIZIONE         VARCHAR2(100 CHAR)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_OPERAZIONE_LEVA.ID_OPERAZIONE_LEVA IS 'Identificativo univoco';

COMMENT ON COLUMN ANAG_USR.CONF_OPERAZIONE_LEVA.DESCRIZIONE IS 'Tipo operazione';



CREATE UNIQUE INDEX ANAG_USR.CONF_OPERAZIONE_LEVA_PK ON ANAG_USR.CONF_OPERAZIONE_LEVA
(ID_OPERAZIONE_LEVA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_OPERAZIONE_LEVA ADD (
  CONSTRAINT CONF_OPERAZIONE_LEVA_PK
  PRIMARY KEY
  (ID_OPERAZIONE_LEVA)
  USING INDEX ANAG_USR.CONF_OPERAZIONE_LEVA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_SOGGETTO_AZIONI_LEVA
(
  ID_R_SOGGETTO_AZIONI_LEVA  NUMBER             NOT NULL,
  ID_SOGGETTO                NUMBER             NOT NULL,
  ID_OPERAZIONE              NUMBER             NOT NULL,
  DATA                       DATE,
  ID_COMUNE                  NUMBER,
  ID_LOCALITA                NUMBER,
  DATA_DECESSO               DATE,
  FLG_MODIFICA_COMUNE        VARCHAR2(1 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_AZIONI_LEVA.ID_R_SOGGETTO_AZIONI_LEVA IS 'Identificativo univoco';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_AZIONI_LEVA.ID_SOGGETTO IS 'Identificativo del soggetto';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_AZIONI_LEVA.ID_OPERAZIONE IS 'Identificativo di operazione leva';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_AZIONI_LEVA.DATA IS 'Data operazione';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_AZIONI_LEVA.ID_COMUNE IS 'Identificativo del comune decesso';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_AZIONI_LEVA.ID_LOCALITA IS 'Identificativo della localita decesso';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_AZIONI_LEVA.DATA_DECESSO IS 'Data decesso';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_AZIONI_LEVA.FLG_MODIFICA_COMUNE IS 'Flag utilizzata per verificare se dopo l''emigrazione di un soggetto viene modificato il comune emigrazione';



CREATE UNIQUE INDEX ANAG_USR.R_SOGGETTO_AZIONI_LEVA_PK ON ANAG_USR.R_SOGGETTO_AZIONI_LEVA
(ID_R_SOGGETTO_AZIONI_LEVA)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_SOGGETTO_AZIONI_LEVA ADD (
  CONSTRAINT R_SOGGETTO_AZIONI_LEVA_PK
  PRIMARY KEY
  (ID_R_SOGGETTO_AZIONI_LEVA)
  USING INDEX ANAG_USR.R_SOGGETTO_AZIONI_LEVA_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_SOGGETTO_AZIONI_LEVA ADD (
  CONSTRAINT COMUNE_AZIONI_LEVA_FK 
  FOREIGN KEY (ID_COMUNE) 
  REFERENCES ANAG_USR.COMUNE (ID_COMUNE)
  ENABLE VALIDATE,
  CONSTRAINT LOCALITA_AZIONI_LEVA_FK 
  FOREIGN KEY (ID_LOCALITA) 
  REFERENCES ANAG_USR.LOCALITA (ID_LOCALITA)
  ENABLE VALIDATE,
  CONSTRAINT OPERAZIONE_AZIONI_LEVA_FK 
  FOREIGN KEY (ID_OPERAZIONE) 
  REFERENCES ANAG_USR.CONF_OPERAZIONE_LEVA (ID_OPERAZIONE_LEVA)
  ENABLE VALIDATE,
  CONSTRAINT SOGGETTO_AZIONI_LEVA_FK 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.LOG_EVENTI_CRI_ANPR
(
  ID                  NUMBER                    NOT NULL,
  CODICE_RICHIESTA    VARCHAR2(200 BYTE),
  DATA_OPERAZIONE     DATE,
  TIPO_ERRORE         VARCHAR2(1 BYTE),
  DESCRIZIONE_ERRORE  VARCHAR2(2000 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.LOG_EVENTI_CRI_ANPR.ID IS 'Identificativo primario della tabella';

COMMENT ON COLUMN ANAG_USR.LOG_EVENTI_CRI_ANPR.CODICE_RICHIESTA IS 'Codice della richiesta ANPR';

COMMENT ON COLUMN ANAG_USR.LOG_EVENTI_CRI_ANPR.DATA_OPERAZIONE IS 'Data dell''operazione';

COMMENT ON COLUMN ANAG_USR.LOG_EVENTI_CRI_ANPR.TIPO_ERRORE IS 'T -> Toponomastica, A -> ANPR';

COMMENT ON COLUMN ANAG_USR.LOG_EVENTI_CRI_ANPR.DESCRIZIONE_ERRORE IS 'Descrizione dell''errore';



CREATE UNIQUE INDEX ANAG_USR.LOG_EVENTI_CRI_ANPR_PK ON ANAG_USR.LOG_EVENTI_CRI_ANPR
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.LOG_EVENTI_CRI_ANPR ADD (
  CONSTRAINT LOG_EVENTI_CRI_ANPR_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.LOG_EVENTI_CRI_ANPR_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_ATTO_ANNULLAMENTO
(
  ID_TIPO_ATTO_ANNULLAMENTO  NUMBER             NOT NULL,
  DESCRIZIONE_ANNULLAMENTO   VARCHAR2(200 BYTE),
  CATEGORIA                  VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_ATTO_ANNULLAMENTO.ID_TIPO_ATTO_ANNULLAMENTO IS 'Identificativo di tabella';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_ATTO_ANNULLAMENTO.DESCRIZIONE_ANNULLAMENTO IS 'Descrizione della tipologia di atto';

COMMENT ON COLUMN ANAG_USR.CONF_TIPO_ATTO_ANNULLAMENTO.CATEGORIA IS 'D -> Divorzio, S -> Separazione, M -> Modifica Condizione';



CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_ATTO_ANNULLAMENTO_PK ON ANAG_USR.CONF_TIPO_ATTO_ANNULLAMENTO
(ID_TIPO_ATTO_ANNULLAMENTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_ATTO_ANNULLAMENTO ADD (
  CONSTRAINT CONF_TIPO_ATTO_ANNULLAMENTO_PK
  PRIMARY KEY
  (ID_TIPO_ATTO_ANNULLAMENTO)
  USING INDEX ANAG_USR.CONF_TIPO_ATTO_ANNULLAMENTO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_ATTO_MATRIMONIO
(
  ID_MATRIMONIO              NUMBER             NOT NULL,
  ID_ATTO                    NUMBER             NOT NULL,
  ID_TIPO_ATTO_ANNULLAMENTO  NUMBER,
  ID_UTENTE                  NUMBER,
  ID_ORGANIZZAZIONE          NUMBER,
  DATA_OPERAZIONE            DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.R_ATTO_MATRIMONIO.ID_UTENTE IS 'Identificativo dell''utente che ha effettuato l''operazione';

COMMENT ON COLUMN ANAG_USR.R_ATTO_MATRIMONIO.ID_ORGANIZZAZIONE IS 'Identificativo dell''organizzazione che ha effettuato l''operazione';

COMMENT ON COLUMN ANAG_USR.R_ATTO_MATRIMONIO.DATA_OPERAZIONE IS 'Data in cui è stata effettuata l''operazione';



CREATE UNIQUE INDEX ANAG_USR.R_ATTO_MATRIMONIO_U1 ON ANAG_USR.R_ATTO_MATRIMONIO
(ID_ATTO, ID_MATRIMONIO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_ATTO_MATRIMONIO ADD (
  CONSTRAINT R_ATTO_MATRIMONIO_FK1 
  FOREIGN KEY (ID_MATRIMONIO) 
  REFERENCES ANAG_USR.MATRIMONIO (ID_MATRIMONIO)
  ENABLE VALIDATE,
  CONSTRAINT R_ATTO_MATRIMONIO_FK2 
  FOREIGN KEY (ID_ATTO) 
  REFERENCES ANAG_USR.ATTO (ID_ATTO)
  ENABLE VALIDATE,
  CONSTRAINT R_ATTO_MATRIMONIO_FK3 
  FOREIGN KEY (ID_TIPO_ATTO_ANNULLAMENTO) 
  REFERENCES ANAG_USR.CONF_TIPO_ATTO_ANNULLAMENTO (ID_TIPO_ATTO_ANNULLAMENTO)
  ENABLE VALIDATE,
  CONSTRAINT R_ATTO_MATRIMONIO_FK4 
  FOREIGN KEY (ID_UTENTE) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE,
  CONSTRAINT R_ATTO_MATRIMONIO_FK5 
  FOREIGN KEY (ID_ORGANIZZAZIONE) 
  REFERENCES ANAG_USR.CONF_STRUTTURE_INTERNE_RC (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.ESTRAZIONE_CITTADINANZA_18
(
  ID_ESTRAZIONE         NUMBER                  NOT NULL,
  PROGRESSIVO           VARCHAR2(20 BYTE),
  ANNO                  NUMBER,
  MESE                  NUMBER,
  TOTALE_SOGGETTI       NUMBER,
  ID_STATUS_ESTRAZIONE  NUMBER,
  ID_UTENTE             NUMBER,
  ID_ORGANIZZAZIONE     NUMBER,
  DATA_OPERAZIONE       DATE
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.ESTRAZIONE_CITTADINANZA_18.ID_ESTRAZIONE IS 'Identificativo estrazione';

COMMENT ON COLUMN ANAG_USR.ESTRAZIONE_CITTADINANZA_18.PROGRESSIVO IS 'Codice progressivo dell''estrazione da mostrare all''utente';

COMMENT ON COLUMN ANAG_USR.ESTRAZIONE_CITTADINANZA_18.ANNO IS 'Anno di nascita dei soggetti estratti';

COMMENT ON COLUMN ANAG_USR.ESTRAZIONE_CITTADINANZA_18.MESE IS 'Mese di nascita dei soggetti estratti';

COMMENT ON COLUMN ANAG_USR.ESTRAZIONE_CITTADINANZA_18.TOTALE_SOGGETTI IS 'Totale dei soggetti estratti per anno e mese';

COMMENT ON COLUMN ANAG_USR.ESTRAZIONE_CITTADINANZA_18.ID_STATUS_ESTRAZIONE IS 'Status dell''estrazione';

COMMENT ON COLUMN ANAG_USR.ESTRAZIONE_CITTADINANZA_18.ID_UTENTE IS 'Identificativo dell''utente';

COMMENT ON COLUMN ANAG_USR.ESTRAZIONE_CITTADINANZA_18.ID_ORGANIZZAZIONE IS 'Identificativo dell''organizzazione dell''utente';

COMMENT ON COLUMN ANAG_USR.ESTRAZIONE_CITTADINANZA_18.DATA_OPERAZIONE IS 'Data in cui è stata effettuata l''ultima operazione';



CREATE UNIQUE INDEX ANAG_USR.ESTRAZIONE_CITTADINANZA_18_PK ON ANAG_USR.ESTRAZIONE_CITTADINANZA_18
(ID_ESTRAZIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.ESTRAZIONE_CITTADINANZA_18 ADD (
  CONSTRAINT ESTRAZIONE_CITTADINANZA_18_PK
  PRIMARY KEY
  (ID_ESTRAZIONE)
  USING INDEX ANAG_USR.ESTRAZIONE_CITTADINANZA_18_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.ESTRAZIONE_CITTADINANZA_18 ADD (
  CONSTRAINT ESTRAZIONE_CITTADINANZA_1_FK1 
  FOREIGN KEY (ID_STATUS_ESTRAZIONE) 
  REFERENCES ANAG_USR.CONF_STATUS_ESTRAZIONE_18 (ID)
  ENABLE VALIDATE,
  CONSTRAINT ESTRAZIONE_CITTADINANZA_1_FK2 
  FOREIGN KEY (ID_ORGANIZZAZIONE) 
  REFERENCES ANAG_USR.CONF_STRUTTURE_INTERNE_RC (ID)
  ENABLE VALIDATE,
  CONSTRAINT ESTRAZIONE_CITTADINANZA_1_FK3 
  FOREIGN KEY (ID_UTENTE) 
  REFERENCES ANAG_USR.UTENTI (ID)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_STATUS_ESTRAZIONE_18
(
  ID           NUMBER                           NOT NULL,
  DESCRIZIONE  VARCHAR2(50 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_STATUS_ESTRAZIONE_18_PK ON ANAG_USR.CONF_STATUS_ESTRAZIONE_18
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_STATUS_ESTRAZIONE_18 ADD (
  CONSTRAINT CONF_STATUS_ESTRAZIONE_18_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_STATUS_ESTRAZIONE_18_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.R_SOGGETTO_CITTADINANZA_18
(
  ID_SOGGETTO         NUMBER,
  ID_ESTRAZIONE       NUMBER,
  PROGRESSIVO         NUMBER,
  COGNOME             VARCHAR2(200 BYTE),
  NOME                VARCHAR2(200 BYTE),
  DATA_NASCITA        DATE,
  SESSO               VARCHAR2(1 BYTE),
  ANNO_PROTOCOLLO     NUMBER,
  NUMERO_PROTOCOLLO   NUMBER,
  TIPO_PROTOCOLLO     VARCHAR2(2 BYTE),
  INDIRIZZO           VARCHAR2(500 BYTE),
  CAP                 VARCHAR2(5 BYTE),
  ID_R_SOGGETTO       NUMBER                    NOT NULL,
  CODICE_INDIVIDUALE  VARCHAR2(20 BYTE),
  CODICE_TOPONIMO     VARCHAR2(20 BYTE),
  TOPONIMO            VARCHAR2(200 BYTE),
  NUMERO_CIVICO       VARCHAR2(20 BYTE),
  ESPONENTE           VARCHAR2(20 BYTE),
  INTERNO             VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CITTADINANZA_18.ID_SOGGETTO IS 'Identificativo del soggetto';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CITTADINANZA_18.ID_ESTRAZIONE IS 'Identificativo dell''estrazione';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CITTADINANZA_18.PROGRESSIVO IS 'Progressivo da mostrare in pagina all''utente';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CITTADINANZA_18.COGNOME IS 'Fotografia del cognome al momento dell''estrazione';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CITTADINANZA_18.NOME IS 'Fotografia del nome al momento dell''estrazione';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CITTADINANZA_18.DATA_NASCITA IS 'Fotografia della data di nascita al momento dell''estrazione';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CITTADINANZA_18.SESSO IS 'Fotografia del sesso al momento dell''estrazione';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CITTADINANZA_18.ANNO_PROTOCOLLO IS 'Anno protocollo';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CITTADINANZA_18.NUMERO_PROTOCOLLO IS 'Numero protocollo';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CITTADINANZA_18.TIPO_PROTOCOLLO IS 'Tipologia del protocollo';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CITTADINANZA_18.INDIRIZZO IS 'Fotografia dell''indirizzo al momento dell''estrazione';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CITTADINANZA_18.CAP IS 'Fotografia del CAP al momento dell''''estrazione';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CITTADINANZA_18.ID_R_SOGGETTO IS 'Identificativo della relazione';

COMMENT ON COLUMN ANAG_USR.R_SOGGETTO_CITTADINANZA_18.CODICE_INDIVIDUALE IS 'Codice Individuale del soggetto';



CREATE UNIQUE INDEX ANAG_USR.R_SOGGETTO_CITTADINANZA_18_PK ON ANAG_USR.R_SOGGETTO_CITTADINANZA_18
(ID_R_SOGGETTO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.R_SOGGETTO_CITTADINANZA_18 ADD (
  CONSTRAINT R_SOGGETTO_CITTADINANZA_18_PK
  PRIMARY KEY
  (ID_R_SOGGETTO)
  USING INDEX ANAG_USR.R_SOGGETTO_CITTADINANZA_18_PK
  ENABLE VALIDATE);

ALTER TABLE ANAG_USR.R_SOGGETTO_CITTADINANZA_18 ADD (
  CONSTRAINT R_SOGGETTO_CITTADINANZA_1_FK1 
  FOREIGN KEY (ID_ESTRAZIONE) 
  REFERENCES ANAG_USR.ESTRAZIONE_CITTADINANZA_18 (ID_ESTRAZIONE)
  ENABLE VALIDATE,
  CONSTRAINT R_SOGGETTO_CITTADINANZA_1_FK2 
  FOREIGN KEY (ID_SOGGETTO) 
  REFERENCES ANAG_USR.SOGGETTO (ID_SOGGETTO)
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_RICHIESTA_ANNULLAMENTO
(
  ID           NUMBER                           NOT NULL,
  TIPO         VARCHAR2(2 BYTE),
  DESCRIZIONE  VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_RICHIESTA_ANNULLAMENT_PK ON ANAG_USR.CONF_RICHIESTA_ANNULLAMENTO
(ID)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_RICHIESTA_ANNULLAMENTO ADD (
  CONSTRAINT CONF_RICHIESTA_ANNULLAMENT_PK
  PRIMARY KEY
  (ID)
  USING INDEX ANAG_USR.CONF_RICHIESTA_ANNULLAMENT_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TITOLO_NOTAIO
(
  ID_TITOLO_NOTAIO  NUMBER                      NOT NULL,
  DESCRIZIONE       VARCHAR2(200 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_TITOLO_NOTAIO_PK ON ANAG_USR.CONF_TITOLO_NOTAIO
(ID_TITOLO_NOTAIO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TITOLO_NOTAIO ADD (
  CONSTRAINT CONF_TITOLO_NOTAIO_PK
  PRIMARY KEY
  (ID_TITOLO_NOTAIO)
  USING INDEX ANAG_USR.CONF_TITOLO_NOTAIO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_DESCRIZIONE_CONVENZIONE
(
  ID_DESCRIZIONE  NUMBER                        NOT NULL,
  DESCRIZIONE     VARCHAR2(200 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_DESCRIZIONE_CONVENZIO_PK ON ANAG_USR.CONF_DESCRIZIONE_CONVENZIONE
(ID_DESCRIZIONE)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_DESCRIZIONE_CONVENZIONE ADD (
  CONSTRAINT CONF_DESCRIZIONE_CONVENZIO_PK
  PRIMARY KEY
  (ID_DESCRIZIONE)
  USING INDEX ANAG_USR.CONF_DESCRIZIONE_CONVENZIO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_TIPO_FONDO_PATRIMONIALE
(
  ID_TIPO_FONDO  NUMBER                         NOT NULL,
  DESCRIZIONE    VARCHAR2(200 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_TIPO_FONDO_PATRIMONIA_PK ON ANAG_USR.CONF_TIPO_FONDO_PATRIMONIALE
(ID_TIPO_FONDO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_TIPO_FONDO_PATRIMONIALE ADD (
  CONSTRAINT CONF_TIPO_FONDO_PATRIMONIA_PK
  PRIMARY KEY
  (ID_TIPO_FONDO)
  USING INDEX ANAG_USR.CONF_TIPO_FONDO_PATRIMONIA_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.CONF_ARTICOLO_NOTAIO
(
  ID_ARTICOLO  NUMBER                           NOT NULL,
  DESCRIZIONE  VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;


CREATE UNIQUE INDEX ANAG_USR.CONF_ARTICOLO_NOTAIO_PK ON ANAG_USR.CONF_ARTICOLO_NOTAIO
(ID_ARTICOLO)
LOGGING
TABLESPACE ANAG_USR
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE ANAG_USR.CONF_ARTICOLO_NOTAIO ADD (
  CONSTRAINT CONF_ARTICOLO_NOTAIO_PK
  PRIMARY KEY
  (ID_ARTICOLO)
  USING INDEX ANAG_USR.CONF_ARTICOLO_NOTAIO_PK
  ENABLE VALIDATE);
CREATE TABLE ANAG_USR.TMP_TEST_AMA
(
  COLUMN1  VARCHAR2(20 BYTE)
)
TABLESPACE ANAG_USR
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;
