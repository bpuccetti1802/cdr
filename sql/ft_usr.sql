CREATE TABLE FT_USR.FT_IRREPERIBILI
(
  ID_STATO_PRATICA    NUMBER,
  ID_SOGGETTO         NUMBER,
  ID_IRREPERIBILITA   NUMBER,
  DATA_FINE           DATE,
  CODICE_INDIVIDUALE  VARCHAR2(20 BYTE),
  SESSO               VARCHAR2(1 BYTE),
  ID_CITTADINANZA     NUMBER,
  ID                  NUMBER
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

COMMENT ON COLUMN FT_USR.FT_IRREPERIBILI.ID_STATO_PRATICA IS 'Identificativo dello stato di avanzamento della pratica collegata al cambio di residenza o domicilio. CONF_STATO_PRATICA';

COMMENT ON COLUMN FT_USR.FT_IRREPERIBILI.ID_SOGGETTO IS 'Identificativo del soggetto';

COMMENT ON COLUMN FT_USR.FT_IRREPERIBILI.ID_IRREPERIBILITA IS 'Campo che identifica univocamente un cambio di residenza o domicillio.';

COMMENT ON COLUMN FT_USR.FT_IRREPERIBILI.DATA_FINE IS 'Data di conclusione del procedimento di irreperibilità';

COMMENT ON COLUMN FT_USR.FT_IRREPERIBILI.CODICE_INDIVIDUALE IS 'Codice utilizzato in APR per identificare univocamente il soggetto';

COMMENT ON COLUMN FT_USR.FT_IRREPERIBILI.SESSO IS 'Sesso del soggetto';

COMMENT ON COLUMN FT_USR.FT_IRREPERIBILI.ID_CITTADINANZA IS 'Identifica lo stato della prima cittadinanza del soggetto';



CREATE UNIQUE INDEX FT_USR.FT_IRREPERIBILI_U1 ON FT_USR.FT_IRREPERIBILI
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


CREATE UNIQUE INDEX FT_USR.FT_IRREPERIBILI_U2 ON FT_USR.FT_IRREPERIBILI
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
CREATE TABLE FT_USR.ETL_CFG_FT
(
  ID           NUMBER(38)                       NOT NULL,
  FLUSSO       VARCHAR2(50 BYTE)                NOT NULL,
  DATA_INIZIO  DATE                             NOT NULL,
  DATA_FINE    DATE                             NOT NULL,
  FLG_ATTIVO   VARCHAR2(1 BYTE)                 NOT NULL
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
NOLOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN FT_USR.ETL_CFG_FT.ID IS 'Identificativo del record';

COMMENT ON COLUMN FT_USR.ETL_CFG_FT.FLUSSO IS 'Nome del FLUSSO ETL_';

COMMENT ON COLUMN FT_USR.ETL_CFG_FT.DATA_INIZIO IS 'Data inizio estrazione del delta';

COMMENT ON COLUMN FT_USR.ETL_CFG_FT.DATA_FINE IS 'Data fine estrazione del delta';

COMMENT ON COLUMN FT_USR.ETL_CFG_FT.FLG_ATTIVO IS 'Flag attivo Y or N';



CREATE UNIQUE INDEX FT_USR.ETL_CFG_FT_U1 ON FT_USR.ETL_CFG_FT
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


CREATE UNIQUE INDEX FT_USR.ETL_CFG_FT_U2 ON FT_USR.ETL_CFG_FT
(FLUSSO, FLG_ATTIVO)
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
CREATE TABLE FT_USR.FT_UNIONI
(
  N_ATTO                         VARCHAR2(20 BYTE),
  PARTE                          VARCHAR2(5 BYTE),
  SERIE                          VARCHAR2(10 BYTE),
  DATA_COSTITUZIONE              DATE,
  FLG_SEPARAZIONE_BENI           VARCHAR2(1 BYTE),
  NOME_U1                        VARCHAR2(250 BYTE),
  COGNOME_U1                     VARCHAR2(250 BYTE),
  SESSO_U1                       VARCHAR2(1 BYTE),
  ID_COMUNE_COMPARIZIONE         NUMBER,
  ID_COMUNE_RESIDENZA_U1         NUMBER,
  ID_STATO_RESIDENZA_U1          NUMBER,
  ID_COMUNE_NASCITA_U1           NUMBER,
  ID_STATO_NASCITA_U1            NUMBER,
  DATA_NASCITA_U1                DATE,
  ID_TITOLO_STUDIO_U1            VARCHAR2(5 BYTE),
  ID_POS_PROFESSIONALE_U1        NUMBER,
  ID_COND_NON_PROFESSIONALE_U1   NUMBER,
  ID_CITTADINANZA_U1             NUMBER,
  DATA_VALIDITA_CITTADINANZA_U1  DATE,
  CODICE_FISCALE_U1              VARCHAR2(16 BYTE),
  NOME_U2                        VARCHAR2(250 BYTE),
  COGNOME_U2                     VARCHAR2(250 BYTE),
  SESSO_U2                       VARCHAR2(1 BYTE),
  ID_COMUNE_RESIDENZA_U2         NUMBER,
  ID_STATO_RESIDENZA_U2          NUMBER,
  ID_COMUNE_NASCITA_U2           NUMBER,
  ID_STATO_NASCITA_U2            NUMBER,
  DATA_NASCITA_U2                DATE,
  ID_TITOLO_STUDIO_U2            VARCHAR2(5 BYTE),
  ID_POS_PROFESSIONALE_U2        NUMBER,
  ID_COND_NON_PROFESSIONALE_U2   NUMBER,
  ID_CITTADINANZA_U2             NUMBER,
  DATA_VALIDITA_CITTADINANZA_U2  DATE,
  CODICE_FISCALE_U2              VARCHAR2(16 BYTE),
  CODICE_INDIVIDUALE_U1          VARCHAR2(20 BYTE),
  CODICE_INDIVIDUALE_U2          VARCHAR2(20 BYTE),
  ID_ATTO_UNIONE                 NUMBER,
  ID_FLUSSO                      VARCHAR2(30 BYTE),
  ID_CAUSALE                     VARCHAR2(30 BYTE),
  FLG_STATO_ELEBORAZIONE         VARCHAR2(1 BYTE),
  FLG_STATO_RETTIFICA            VARCHAR2(1 BYTE),
  RETTIFICA_VAL_OLD              VARCHAR2(20 BYTE),
  RETTIFICA_VAL_NEW              VARCHAR2(20 BYTE),
  DATA_PRATICA                   DATE,
  ID_STATO_PRATICA               NUMBER,
  DATA_UPD_ATTO                  DATE,
  ID_STATO_CIVILE_PREC_U1        NUMBER,
  ID_STATO_CIVILE_PREC_U2        NUMBER,
  ID_TIPO_LUOGO_RESIDENZA_U1     NUMBER,
  ID_TIPO_LUOGO_RESIDENZA_U2     NUMBER,
  ID_TIPO_LUOGO_NASCITA_U1       NUMBER,
  ID_TIPO_LUOGO_NASCITA_U2       NUMBER,
  ID_TIPO_CITTADINANZA_U1        NUMBER,
  ID_TIPO_CITTADINANZA_U2        NUMBER
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

COMMENT ON COLUMN FT_USR.FT_UNIONI.N_ATTO IS 'Campo che indica il numero dell''atto. Mi aspetterei che corrisponda sempre all''ANNO (dell''esponente).. a meno che non registrato su anno diverso';

COMMENT ON COLUMN FT_USR.FT_UNIONI.PARTE IS 'Campo che indica il numero della parte dell''atto di unione';

COMMENT ON COLUMN FT_USR.FT_UNIONI.SERIE IS 'Campo che indica la serie dell''atto di unione';

COMMENT ON COLUMN FT_USR.FT_UNIONI.DATA_COSTITUZIONE IS 'Data costituzione unione';

COMMENT ON COLUMN FT_USR.FT_UNIONI.FLG_SEPARAZIONE_BENI IS 'Flag separazione beni [S]I o [N]O';

COMMENT ON COLUMN FT_USR.FT_UNIONI.NOME_U1 IS 'nome unendo 1';

COMMENT ON COLUMN FT_USR.FT_UNIONI.COGNOME_U1 IS 'cognome unendo 1';

COMMENT ON COLUMN FT_USR.FT_UNIONI.SESSO_U1 IS 'sesso unendo 1';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_COMUNE_COMPARIZIONE IS 'Identificativo del comune';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_COMUNE_RESIDENZA_U1 IS 'Identificativo del comune di residenza del unendo 1';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_STATO_RESIDENZA_U1 IS 'Identificativo dello stato di residenza del unendo 1';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_COMUNE_NASCITA_U1 IS 'Identificativo del comune di nascita del unendo 1';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_STATO_NASCITA_U1 IS 'Identificativo dello stato di nascita del unendo 1';

COMMENT ON COLUMN FT_USR.FT_UNIONI.DATA_NASCITA_U1 IS 'data nascita unendo 1';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_TITOLO_STUDIO_U1 IS 'Identificativo del titolo di studio del unendo 1';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_POS_PROFESSIONALE_U1 IS 'Identificativo della posizione professionale del unendo 1';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_COND_NON_PROFESSIONALE_U1 IS 'Identificativo della condizione non professionale del unendo 1';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_CITTADINANZA_U1 IS 'Identifica lo stato della prima cittadinanza del soggetto';

COMMENT ON COLUMN FT_USR.FT_UNIONI.DATA_VALIDITA_CITTADINANZA_U1 IS 'La data a partire dalla quale il soggetto ha assunto la cittadinanza indicata con ID_CITTADINANZA';

COMMENT ON COLUMN FT_USR.FT_UNIONI.CODICE_FISCALE_U1 IS 'Codice fiscale del unendo 1';

COMMENT ON COLUMN FT_USR.FT_UNIONI.NOME_U2 IS 'nome unendo 2';

COMMENT ON COLUMN FT_USR.FT_UNIONI.COGNOME_U2 IS 'cognome unendo 2';

COMMENT ON COLUMN FT_USR.FT_UNIONI.SESSO_U2 IS 'sesso unendo 2';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_COMUNE_RESIDENZA_U2 IS 'Identificativo del comune di residenza del unendo 2';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_STATO_RESIDENZA_U2 IS 'Identificativo dello stato di residenza del unendo 2';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_COMUNE_NASCITA_U2 IS 'Identificativo del comune di nascita del unendo 2';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_STATO_NASCITA_U2 IS 'Identificativo dello stato di nascita del unendo 2';

COMMENT ON COLUMN FT_USR.FT_UNIONI.DATA_NASCITA_U2 IS 'data nascita unendo 2';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_TITOLO_STUDIO_U2 IS 'Identificativo del titolo di studio del unendo 2';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_POS_PROFESSIONALE_U2 IS 'Identificativo della posizione professionale del unendo 2';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_COND_NON_PROFESSIONALE_U2 IS 'Identificativo della condizione non professionale del unendo 2';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_CITTADINANZA_U2 IS 'Identifica lo stato della prima cittadinanza del soggetto';

COMMENT ON COLUMN FT_USR.FT_UNIONI.DATA_VALIDITA_CITTADINANZA_U2 IS 'La data a partire dalla quale il soggetto ha assunto la cittadinanza indicata con ID_CITTADINANZA';

COMMENT ON COLUMN FT_USR.FT_UNIONI.CODICE_FISCALE_U2 IS 'Codice fiscale del unendo 2';

COMMENT ON COLUMN FT_USR.FT_UNIONI.CODICE_INDIVIDUALE_U1 IS 'Codice utilizzato in APR per identificare univocamente il soggetto unendo 1';

COMMENT ON COLUMN FT_USR.FT_UNIONI.CODICE_INDIVIDUALE_U2 IS 'Codice utilizzato in APR per identificare univocamente il soggetto unendo 2';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_ATTO_UNIONE IS 'Campo che indica l''id dell''atto unione.';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_FLUSSO IS 'Identificativo del Flusso di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_CAUSALE IS 'Identificativo della causale di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_UNIONI.FLG_STATO_ELEBORAZIONE IS 'Flg inserimento su OUT_';

COMMENT ON COLUMN FT_USR.FT_UNIONI.FLG_STATO_RETTIFICA IS 'Flg inserimento su RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_UNIONI.RETTIFICA_VAL_OLD IS 'In caso di rettifica contiene il vecchio valore del campo COMUNE o STATO';

COMMENT ON COLUMN FT_USR.FT_UNIONI.RETTIFICA_VAL_NEW IS 'In caso di rettifica contiene il nuovo valore del campo COMUNE o NAZIONE';

COMMENT ON COLUMN FT_USR.FT_UNIONI.DATA_PRATICA IS 'Data prima accoglimento della Pratica/Inizio lavorazioni - differisce dalla data dell''Atto';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_STATO_PRATICA IS 'Campo che indica lo stato della pratica.';

COMMENT ON COLUMN FT_USR.FT_UNIONI.DATA_UPD_ATTO IS 'Ultima data di aggiornamento del atto';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_STATO_CIVILE_PREC_U1 IS 'Identificativo stato civile precedente all unione del unendo 1';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_STATO_CIVILE_PREC_U2 IS 'Identificativo stato civile precedente all unione del unendo 2';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_TIPO_LUOGO_RESIDENZA_U1 IS 'Identificativo tipo luogo residenza - Valori ammessi: 1= Stesso Comune di costituzione dell’unione civile 2= Comune diverso da quello di costituzione dell’unione civile3 = Stato estero';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_TIPO_LUOGO_RESIDENZA_U2 IS 'Identificativo tipo luogo residenza - Valori ammessi: 1= Stesso Comune di costituzione dell’unione civile 2= Comune diverso da quello di costituzione dell’unione civile3 = Stato estero';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_TIPO_LUOGO_NASCITA_U1 IS 'Identificativo tipo luogo nascita -Valori ammessi: 
1= Stesso Comune di costituzione dell’unione civile 
2= Comune diverso da quello di costituzione dell’unione civile 
3 = Stato estero';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_TIPO_LUOGO_NASCITA_U2 IS 'Identificativo tipo luogo nascita -Valori ammessi: 
1= Stesso Comune di costituzione dell’unione civile 
2= Comune diverso da quello di costituzione dell’unione civile 
3 = Stato estero';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_TIPO_CITTADINANZA_U1 IS 'Identificativo del tipo cittadinanza -Valori ammessi 
1= Italiana dalla nascita 
2= Italiana acquisita 
3= Straniera';

COMMENT ON COLUMN FT_USR.FT_UNIONI.ID_TIPO_CITTADINANZA_U2 IS 'Identificativo del tipo cittadinanza -Valori ammessi 
1= Italiana dalla nascita 
2= Italiana acquisita 
3= Straniera';
CREATE TABLE FT_USR.CFG_FT_RETTIFICA
(
  ID_CAUSALE       VARCHAR2(30 BYTE),
  ID_FLUSSO        VARCHAR2(30 BYTE),
  TIP_MOV          VARCHAR2(30 BYTE),
  CAUSALE          VARCHAR2(30 BYTE),
  PGM              VARCHAR2(30 BYTE),
  VAL_OLD          VARCHAR2(30 BYTE),
  VAL_NEW          VARCHAR2(30 BYTE),
  DIREZIONE        VARCHAR2(30 BYTE),
  FLG_ERC          VARCHAR2(30 BYTE),
  ID_TIPO_CAUSALE  VARCHAR2(30 BYTE)
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
CREATE TABLE FT_USR.FT_NASCITE
(
  ID_FAMIGLIA_CONVIVENZA     NUMBER,
  ID_COMUNE_RESIDENZA        NUMBER,
  COGNOME_NATO               VARCHAR2(250 BYTE),
  NOME_NATO                  VARCHAR2(250 BYTE),
  ID_COMUNE_NASCITA          NUMBER,
  ID_STATO_NASCITA           NUMBER,
  DATA_NASCITA               DATE,
  SESSO_NATO                 VARCHAR2(1 BYTE),
  ID_CITTADINANZA            NUMBER,
  DATA_ISCRIZ_NASCITA        DATE,
  COGNOME_MADRE              VARCHAR2(250 BYTE),
  NOME_MADRE                 VARCHAR2(250 BYTE),
  DATA_NASCITA_MADRE         DATE,
  ID_STATO_CIVILE_MADRE      NUMBER,
  ID_CITTADINANZA_MADRE      NUMBER,
  COD_FISC_MADRE             VARCHAR2(16 BYTE),
  COGNOME_PADRE              VARCHAR2(250 BYTE),
  NOME_PADRE                 VARCHAR2(250 BYTE),
  DATA_NASCITA_PADRE         DATE,
  ID_STATO_CIVILE_PADRE      NUMBER,
  ID_CITTADINANZA_PADRE      NUMBER,
  COD_FISC_PADRE             VARCHAR2(16 BYTE),
  CODICE_FAMIGLIA            VARCHAR2(20 BYTE),
  CODICE_CONVIVENZA          VARCHAR2(20 BYTE),
  FLAG_NATO_MORTO            VARCHAR2(1 BYTE),
  COD_IND_MADRE              VARCHAR2(20 BYTE),
  COD_IND_PADRE              VARCHAR2(20 BYTE),
  ID_COMUNE_RESIDENZA_MADRE  NUMBER,
  ID_COMUNE_RESIDENZA_PADRE  NUMBER,
  SESSO_PADRE                VARCHAR2(1 BYTE),
  SESSO_MADRE                VARCHAR2(1 BYTE),
  CODICE_INDIVIDUALE         VARCHAR2(20 BYTE),
  ID_FLUSSO                  VARCHAR2(30 BYTE),
  ID_CAUSALE                 VARCHAR2(30 BYTE),
  FLG_STATO_ELEBORAZIONE     VARCHAR2(1 BYTE),
  FLG_STATO_RETTIFICA        VARCHAR2(1 BYTE),
  RETTIFICA_VAL_OLD          VARCHAR2(20 BYTE),
  RETTIFICA_VAL_NEW          VARCHAR2(20 BYTE),
  ID_ATTO_NASCITA            NUMBER,
  ID_STATO_PRATICA           NUMBER,
  DATA_PRATICA               DATE,
  DATA_UPD_ATTO              DATE,
  FLG_PARTO_PLURIMO          VARCHAR2(1 BYTE),
  FLG_NATO_OSP               VARCHAR2(1 BYTE),
  FLG_NATO_IN_MATRIMONIO     VARCHAR2(1 BYTE),
  ID_MUNICIPIO               NUMBER,
  ANNO_ATTO                  NUMBER,
  PARTE_ATTO                 VARCHAR2(5 BYTE),
  SERIE_ATTO                 VARCHAR2(10 BYTE),
  NUMERO_ATTO                VARCHAR2(20 BYTE),
  ID_ATTO                    NUMBER,
  ESPONENTE                  VARCHAR2(20 BYTE)
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

COMMENT ON COLUMN FT_USR.FT_NASCITE.ID_FAMIGLIA_CONVIVENZA IS 'identificativo della famiglia o convivenza in APR';

COMMENT ON COLUMN FT_USR.FT_NASCITE.ID_COMUNE_RESIDENZA IS 'Identifica la residenza attuale della famiglia/collettività';

COMMENT ON COLUMN FT_USR.FT_NASCITE.COGNOME_NATO IS 'Cognome Nato';

COMMENT ON COLUMN FT_USR.FT_NASCITE.NOME_NATO IS 'Nome Nato';

COMMENT ON COLUMN FT_USR.FT_NASCITE.ID_COMUNE_NASCITA IS 'Identificativo del comune di nascita';

COMMENT ON COLUMN FT_USR.FT_NASCITE.ID_STATO_NASCITA IS 'Identificativo dello stato di nascita';

COMMENT ON COLUMN FT_USR.FT_NASCITE.DATA_NASCITA IS 'Data nascita';

COMMENT ON COLUMN FT_USR.FT_NASCITE.SESSO_NATO IS 'Sesso nato';

COMMENT ON COLUMN FT_USR.FT_NASCITE.ID_CITTADINANZA IS 'Identifica lo stato della prima cittadinanza del soggetto nato';

COMMENT ON COLUMN FT_USR.FT_NASCITE.DATA_ISCRIZ_NASCITA IS 'Data di iscrizione in anagrafe per nascita del nato';

COMMENT ON COLUMN FT_USR.FT_NASCITE.COGNOME_MADRE IS 'Cognome madre';

COMMENT ON COLUMN FT_USR.FT_NASCITE.NOME_MADRE IS 'Nome madre';

COMMENT ON COLUMN FT_USR.FT_NASCITE.DATA_NASCITA_MADRE IS 'Data nascita madre';

COMMENT ON COLUMN FT_USR.FT_NASCITE.ID_STATO_CIVILE_MADRE IS 'Identificativo dello stato civile della madre';

COMMENT ON COLUMN FT_USR.FT_NASCITE.ID_CITTADINANZA_MADRE IS 'Identifica lo stato della prima cittadinanza della madre';

COMMENT ON COLUMN FT_USR.FT_NASCITE.COD_FISC_MADRE IS 'Codice fiscale della madre';

COMMENT ON COLUMN FT_USR.FT_NASCITE.COGNOME_PADRE IS 'Cognome padre';

COMMENT ON COLUMN FT_USR.FT_NASCITE.NOME_PADRE IS 'Nome padre';

COMMENT ON COLUMN FT_USR.FT_NASCITE.DATA_NASCITA_PADRE IS 'Data nascita padre';

COMMENT ON COLUMN FT_USR.FT_NASCITE.ID_STATO_CIVILE_PADRE IS 'Identificativo dello stato civile del padre';

COMMENT ON COLUMN FT_USR.FT_NASCITE.ID_CITTADINANZA_PADRE IS 'Identifica lo stato della prima cittadinanza del padre';

COMMENT ON COLUMN FT_USR.FT_NASCITE.COD_FISC_PADRE IS 'Codice fiscale del padre';

COMMENT ON COLUMN FT_USR.FT_NASCITE.CODICE_FAMIGLIA IS 'Codice identificativo della famiglia';

COMMENT ON COLUMN FT_USR.FT_NASCITE.CODICE_CONVIVENZA IS 'Codice identificativo della convivenza';

COMMENT ON COLUMN FT_USR.FT_NASCITE.FLAG_NATO_MORTO IS 'Nato Morto ([S]i o [N]o) - se iscrizione da Pubblico Ufficiale';

COMMENT ON COLUMN FT_USR.FT_NASCITE.COD_IND_MADRE IS 'Codice  utilizzato in APR per identificare univocamente il soggetto madre';

COMMENT ON COLUMN FT_USR.FT_NASCITE.COD_IND_PADRE IS 'Codice  utilizzato in APR per identificare univocamente il soggetto padre';

COMMENT ON COLUMN FT_USR.FT_NASCITE.ID_COMUNE_RESIDENZA_MADRE IS 'Identificativo del comune di residenza della madre';

COMMENT ON COLUMN FT_USR.FT_NASCITE.ID_COMUNE_RESIDENZA_PADRE IS 'Identificativo del comune di residenza del padre';

COMMENT ON COLUMN FT_USR.FT_NASCITE.SESSO_PADRE IS 'Sesso madre';

COMMENT ON COLUMN FT_USR.FT_NASCITE.SESSO_MADRE IS 'Sesso padre';

COMMENT ON COLUMN FT_USR.FT_NASCITE.CODICE_INDIVIDUALE IS 'Codice  utilizzato in APR per identificare univocamente il soggetto nato';

COMMENT ON COLUMN FT_USR.FT_NASCITE.ID_FLUSSO IS 'Identificativo del Flusso di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_NASCITE.ID_CAUSALE IS 'Identificativo della causale di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_NASCITE.FLG_STATO_ELEBORAZIONE IS 'Flg inserimento su OUT_';

COMMENT ON COLUMN FT_USR.FT_NASCITE.FLG_STATO_RETTIFICA IS 'Flg inserimento su RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_NASCITE.RETTIFICA_VAL_OLD IS 'In caso di rettifica contiene il vecchio valore del campo COMUNE o STATO';

COMMENT ON COLUMN FT_USR.FT_NASCITE.RETTIFICA_VAL_NEW IS 'In caso di rettifica contiene il nuovo valore del campo COMUNE o NAZIONE';

COMMENT ON COLUMN FT_USR.FT_NASCITE.ID_STATO_PRATICA IS 'Campo che indica lo stato della pratica.';

COMMENT ON COLUMN FT_USR.FT_NASCITE.FLG_PARTO_PLURIMO IS 'Flag che segnala se il PARTO è stato plurimo o meno. default a NULL fino allo splitting. se vi sono più figli viene impostato a ''S'' altrimenti a ''N''';

COMMENT ON COLUMN FT_USR.FT_NASCITE.FLG_NATO_OSP IS 'Flag che indica se dichiarati alla Direzione sanitaria di centro nascita';

COMMENT ON COLUMN FT_USR.FT_NASCITE.FLG_NATO_IN_MATRIMONIO IS 'Flag che indica seè nato all''interno del matrimonio';

COMMENT ON COLUMN FT_USR.FT_NASCITE.ID_MUNICIPIO IS 'Identificativo del municipio della residenza del nato';

COMMENT ON COLUMN FT_USR.FT_NASCITE.ANNO_ATTO IS 'Campo che indica l''anno in cui si registra l''atto.';

COMMENT ON COLUMN FT_USR.FT_NASCITE.PARTE_ATTO IS 'Campo che indica il numero della parte dell''atto.';

COMMENT ON COLUMN FT_USR.FT_NASCITE.SERIE_ATTO IS 'Campo che indica la serie dell''atto.';

COMMENT ON COLUMN FT_USR.FT_NASCITE.NUMERO_ATTO IS 'IL NUMERO ATTO VIENE CREATO COME PROGRESSIVO DA 1 A XXXXX PER SINGOLO ANNO E PARTE/SERIE';

COMMENT ON COLUMN FT_USR.FT_NASCITE.ID_ATTO IS 'Campo che indica l''id dell''atto.';

COMMENT ON COLUMN FT_USR.FT_NASCITE.ESPONENTE IS 'Campo che indica l''esponente dell''atto';



CREATE UNIQUE INDEX FT_USR.FT_NASCITE_U1 ON FT_USR.FT_NASCITE
(ID_ATTO_NASCITA)
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


CREATE UNIQUE INDEX FT_USR.FT_NASCITE_U2 ON FT_USR.FT_NASCITE
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
CREATE TABLE FT_USR.FT_DIVORZI
(
  ID_PROVV_TIPO                  NUMBER,
  DATA_STIPULA                   DATE,
  DATA_RILASCIO                  DATE,
  NUMERO_ATTO                    VARCHAR2(20 BYTE),
  PARTE                          VARCHAR2(5 BYTE),
  SERIE                          VARCHAR2(10 BYTE),
  ID_ACCORDO_DIVORZIO            NUMBER,
  DATA_CONFERMA_ACCORDO          DATE,
  ID_COMUNE_CELEB                NUMBER,
  ID_TIPO_RITO                   NUMBER,
  ID_TIPO_SEPARAZIONE_BENI       NUMBER,
  DATA_CELEBRAZIONE              DATE,
  NOME_MARITO                    VARCHAR2(250 BYTE),
  COGNOME_MARITO                 VARCHAR2(250 BYTE),
  DATA_NASC_MARITO               DATE,
  ID_COMUNE_NASCITA_MARITO       NUMBER,
  ID_STATO_NASCITA_MARITO        NUMBER,
  CODICE_FISCALE_MARITO          VARCHAR2(16 BYTE),
  ID_COMUNE_RESIDENZA_MARITO     NUMBER,
  ID_STATO_RESIDENZA_MARITO      NUMBER,
  ID_STATO_CITTADINANZA_MARITO   NUMBER,
  DATA_ACQ_CITTADINANZA_MARITO   VARCHAR2(50 BYTE),
  ID_TITOLO_STUDIO_MARITO        NUMBER,
  ID_POS_PROFESSIONALE_MARITO    NUMBER,
  ID_COND_NON_PROF_MARITO        NUMBER,
  NOME_MOGLIE                    VARCHAR2(250 BYTE),
  COGNOME_MOGLIE                 VARCHAR2(250 BYTE),
  DATA_NASC_MOGLIE               DATE,
  ID_COMUNE_NASCITA_MOGLIE       NUMBER,
  ID_STATO_NASCITA_MOGLIE        NUMBER,
  CODICE_FISCALE_MOGLIE          VARCHAR2(16 BYTE),
  ID_COMUNE_RESIDENZA_MOGLIE     NUMBER,
  ID_STATO_RESIDENZA_MOGLIE      NUMBER,
  ID_STATO_CITTADINANZA_MOGLIE   NUMBER,
  DATA_ACQ_CITTADINANZA_MOGLIE   VARCHAR2(50 BYTE),
  ID_TITOLO_STUDIO_MOGLIE        NUMBER,
  ID_POS_PROFESSIONALE_MOGLIE    NUMBER,
  ID_COND_NON_PROF_MOGLIE        NUMBER,
  NOME_AVV_MARITO                VARCHAR2(250 BYTE),
  COGNOME_AVV_MARITO             VARCHAR2(250 BYTE),
  NOME_AVV_MOGLIE                VARCHAR2(250 BYTE),
  COGNOME_AVV_MOGLIE             VARCHAR2(250 BYTE),
  CODICE_INDIV_MARITO            VARCHAR2(20 BYTE),
  CODICE_INDIV_MOGLIE            VARCHAR2(20 BYTE),
  ID_ATTO_DIVORZIO               NUMBER,
  ID_TIPO_CITTAD_MARITO          NUMBER,
  ID_STATO_CIV_PRE_MATRI_MARITO  NUMBER,
  AVV_CODICE_FISCALE_MARITO      VARCHAR2(20 BYTE),
  AVV_ALBOORDINE_DI_MARITO       VARCHAR2(50 BYTE),
  ID_TIPO_CITTAD_MOGLIE          NUMBER,
  ID_STATO_CIV_PRE_MATRI_MOGLIE  NUMBER,
  AVV_CODICE_FISCALE_MOGLIE      VARCHAR2(20 BYTE),
  AVV_ALBOORDINE_DI_MOGLIE       VARCHAR2(50 BYTE),
  DATA_PRATICA                   DATE,
  ID_STATO_PRATICA               NUMBER,
  DATA_UPD_ATTO                  DATE,
  ID_FLUSSO                      VARCHAR2(30 BYTE),
  ID_CAUSALE                     VARCHAR2(30 BYTE),
  FLG_STATO_ELEBORAZIONE         VARCHAR2(1 BYTE),
  FLG_STATO_RETTIFICA            VARCHAR2(1 BYTE),
  RETTIFICA_VAL_OLD              VARCHAR2(20 BYTE),
  RETTIFICA_VAL_NEW              VARCHAR2(20 BYTE),
  CONTRIBUTO_ECONOMICO           VARCHAR2(30 BYTE),
  IMPORTO_MENSILE                VARCHAR2(30 BYTE),
  IMPORTO_MENSILE_U              VARCHAR2(30 BYTE),
  CONIUGE_CONTRIBUISCE           VARCHAR2(30 BYTE),
  ASSEGNAZIONE_ABITAZIONE        VARCHAR2(30 BYTE),
  COPPIA_CON_FIGLI               VARCHAR2(30 BYTE),
  COPPIA_CON_FIGLI_MINORENNI     VARCHAR2(30 BYTE),
  COPPIA_CON_FIGLI_HANDICAP      VARCHAR2(30 BYTE),
  COPPIA_CON_FIGLI_NUMERO        VARCHAR2(30 BYTE),
  FIGLI_MINORENNI_NUMERO         VARCHAR2(30 BYTE),
  FIGLI_HANDICAP_NUMERO          VARCHAR2(30 BYTE),
  F1_SESSO                       VARCHAR2(30 BYTE),
  F1_DATA_NASCITA                VARCHAR2(30 BYTE),
  F1_ETA                         VARCHAR2(30 BYTE),
  F1_CODICE_FISCALE              VARCHAR2(30 BYTE),
  F1_TIPO_AFFIDAMENTO            VARCHAR2(30 BYTE),
  F1_PERNOTTAMENTI_PADRE         VARCHAR2(30 BYTE),
  F2_SESSO                       VARCHAR2(30 BYTE),
  F2_DATA_NASCITA                VARCHAR2(30 BYTE),
  F2_ETA                         VARCHAR2(30 BYTE),
  F2_CODICE_FISCALE              VARCHAR2(30 BYTE),
  F2_TIPO_AFFIDAMENTO            VARCHAR2(30 BYTE),
  F2_PERNOTTAMENTI_PADRE         VARCHAR2(30 BYTE),
  F3_SESSO                       VARCHAR2(30 BYTE),
  F3_DATA_NASCITA                VARCHAR2(30 BYTE),
  F3_ETA                         VARCHAR2(30 BYTE),
  F3_CODICE_FISCALE              VARCHAR2(30 BYTE),
  F3_TIPO_AFFIDAMENTO            VARCHAR2(30 BYTE),
  F3_PERNOTTAMENTI_PADRE         VARCHAR2(30 BYTE),
  F4_SESSO                       VARCHAR2(30 BYTE),
  F4_DATA_NASCITA                VARCHAR2(30 BYTE),
  F4_ETA                         VARCHAR2(30 BYTE),
  F4_CODICE_FISCALE              VARCHAR2(30 BYTE),
  F4_TIPO_AFFIDAMENTO            VARCHAR2(30 BYTE),
  F4_PERNOTTAMENTI_PADRE         VARCHAR2(30 BYTE),
  TESTO_SEZIONE7                 VARCHAR2(30 BYTE),
  TIPO_MANTENIMENTO_FIGLI        VARCHAR2(30 BYTE),
  TESTO2_SEZIONE7                VARCHAR2(30 BYTE),
  SPESA_ABITAZIONE               VARCHAR2(30 BYTE),
  SPESA_ABBIGLIAMENTO            VARCHAR2(30 BYTE),
  SPESA_SALUTE                   VARCHAR2(30 BYTE),
  SPESA_ISTRUZIONE               VARCHAR2(30 BYTE),
  SPESA_ATTIVITA                 VARCHAR2(30 BYTE),
  TESTO3_SEZIONE7                VARCHAR2(30 BYTE),
  IMPORTO_MENSILE_ASSEGNO_FIGLI  VARCHAR2(30 BYTE),
  CONIUGE_CORRISPONDE_ASSEGNO    VARCHAR2(30 BYTE),
  MANTENIMENTO_CORRISPOSTO_A     VARCHAR2(51 BYTE),
  ANNO_ATTO                      NUMBER(4),
  PARTE_ATTO                     VARCHAR2(5 BYTE),
  SERIE_ATTO                     VARCHAR2(10 BYTE),
  ID_SOTTOTIPO_ATTO              NUMBER
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

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_PROVV_TIPO IS 'Tipologia di Provvedimento dell''Autorità Giudiziaria. Art.6 e Art.12 (selettività sull''articolo)';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.DATA_STIPULA IS 'Data stipula convenzione';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.DATA_RILASCIO IS 'Data di rilascio/iscrizione dell''ATTO  Data Verbale (per verbali UNIONI CIVILI)';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.NUMERO_ATTO IS 'Campo che indica il numero dell''atto di divorzio';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.PARTE IS 'Campo che indica il numero della parte dell''atto di divorzio';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.SERIE IS 'Campo che indica la serie dell''atto di divorzio';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_ACCORDO_DIVORZIO IS 'Tipologia di Accordo di Divorzio Art.12';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.DATA_CONFERMA_ACCORDO IS 'Data conferma Accordo di divorzio e separazione consensuale';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_COMUNE_CELEB IS 'Comune celebrazione del matrimonio (può differire dal comune di iscrizione dell''atto';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_TIPO_RITO IS 'identificativo del rito di celebrazione del matrimonio ';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_TIPO_SEPARAZIONE_BENI IS 'Flag separazione beni [S]I o [N]O';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.DATA_CELEBRAZIONE IS 'Data celebrazione matrimonio';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.NOME_MARITO IS 'nome marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.COGNOME_MARITO IS 'cognome marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.DATA_NASC_MARITO IS 'data nascita marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_COMUNE_NASCITA_MARITO IS 'Identificativo del comune di nascita del marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_STATO_NASCITA_MARITO IS 'Identificativo dello stato di nascita del marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.CODICE_FISCALE_MARITO IS 'codice fiscale del marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_COMUNE_RESIDENZA_MARITO IS 'Identificativo del comune di residenza del marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_STATO_RESIDENZA_MARITO IS 'Identificativo dello stato di residenza del marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_STATO_CITTADINANZA_MARITO IS 'Identificativo dello stato di cittadinanza del marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.DATA_ACQ_CITTADINANZA_MARITO IS 'Data di acquisto cittadinanza marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_TITOLO_STUDIO_MARITO IS 'Identificativo del titolo di studio del marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_POS_PROFESSIONALE_MARITO IS 'Identificativo della posizione professionale del marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_COND_NON_PROF_MARITO IS 'Identificativo della condizione non professionale del marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.NOME_MOGLIE IS 'nome moglie';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.COGNOME_MOGLIE IS 'cognome moglie';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.DATA_NASC_MOGLIE IS 'data nascita della moglie';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_COMUNE_NASCITA_MOGLIE IS 'Identificativo del comune di nascita della moglie';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_STATO_NASCITA_MOGLIE IS 'Identificativo dello stato di nascita della moglie';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.CODICE_FISCALE_MOGLIE IS 'codice fiscale della moglie';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_COMUNE_RESIDENZA_MOGLIE IS 'Identificativo del comune di residenza della moglie';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_STATO_RESIDENZA_MOGLIE IS 'Identificativo dello stato di residenza della moglie';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_STATO_CITTADINANZA_MOGLIE IS 'Identificativo dello stato di cittadinanza della moglie';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.DATA_ACQ_CITTADINANZA_MOGLIE IS 'Data di acquisto cittadinanza della moglie';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_TITOLO_STUDIO_MOGLIE IS 'Identificativo del titolo di studio della moglie';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_POS_PROFESSIONALE_MOGLIE IS 'Identificativo della posizione professionale della moglie';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_COND_NON_PROF_MOGLIE IS 'Identificativo della condizione non professionale della moglie';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.NOME_AVV_MARITO IS 'nome avvocato marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.COGNOME_AVV_MARITO IS 'cognome avvocato marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.NOME_AVV_MOGLIE IS 'nome avvocato moglie';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.COGNOME_AVV_MOGLIE IS 'cognome avvocato moglie';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.CODICE_INDIV_MARITO IS 'Codice utilizzato in APR per identificare univocamente il soggetto marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.CODICE_INDIV_MOGLIE IS 'Codice utilizzato in APR per identificare univocamente il soggetto moglie';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_ATTO_DIVORZIO IS 'Campo che indica l''id dell''atto.';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_TIPO_CITTAD_MARITO IS 'Tipologia di cittadinanza (Italiana dalla nascita,acquisita, straniera) del marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_STATO_CIV_PRE_MATRI_MARITO IS 'Identificativo dello stato civile dello sposo precedente al matrimonio';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.AVV_CODICE_FISCALE_MARITO IS 'Codice fiscale avvocato del marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.AVV_ALBOORDINE_DI_MARITO IS 'Albo Ordine del avvocato del marito';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_TIPO_CITTAD_MOGLIE IS 'Tipologia di cittadinanza (Italiana dalla nascita,acquisita, straniera) della moglia';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_STATO_CIV_PRE_MATRI_MOGLIE IS 'Identificativo dello stato civile della sposa precedente al matrimonio';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.AVV_CODICE_FISCALE_MOGLIE IS 'Codice fiscale avvocato dela moglie';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.AVV_ALBOORDINE_DI_MOGLIE IS 'Albo Ordine del avvocato della moglie';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.DATA_PRATICA IS 'Data prima accoglimento della Pratica/Inizio lavorazioni - differisce dalla data dell''Atto';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_STATO_PRATICA IS 'Campo che indica lo stato della pratica.';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.DATA_UPD_ATTO IS 'Ultima data di aggiornamento del atto';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_FLUSSO IS 'Identificativo del Flusso di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_CAUSALE IS 'Identificativo della causale di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.FLG_STATO_ELEBORAZIONE IS 'Flg inserimento su OUT_';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.FLG_STATO_RETTIFICA IS 'Flg inserimento su RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.RETTIFICA_VAL_OLD IS 'In caso di rettifica contiene il vecchio valore del campo COMUNE o STATO';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.RETTIFICA_VAL_NEW IS 'In caso di rettifica contiene il nuovo valore del campo COMUNE o NAZIONE';

COMMENT ON COLUMN FT_USR.FT_DIVORZI.ID_SOTTOTIPO_ATTO IS 'Tipologia di Provvedimento dell''Autorità Giudiziaria. Art.6 e Art.12 (selettività sull''articolo)';



CREATE UNIQUE INDEX FT_USR.FT_DIVORZI_U1 ON FT_USR.FT_DIVORZI
(ID_ATTO_DIVORZIO)
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
CREATE TABLE FT_USR.FT_MATRIMONI
(
  NUMERO_ATTO                    VARCHAR2(20 BYTE),
  PARTE                          VARCHAR2(5 BYTE),
  SERIE                          VARCHAR2(10 BYTE),
  DATA_CELEBRAZIONE              DATE,
  ID_TIPO_RITO                   NUMBER,
  NOME_SPOSO                     VARCHAR2(250 BYTE),
  COGNOME_SPOSO                  VARCHAR2(250 BYTE),
  ID_COMUNE_NASCITA_SPOSO        NUMBER,
  ID_STATO_NASCITA_SPOSO         NUMBER,
  DATA_NASCITA_SPOSO             DATE,
  DATA_CESS_MATR_PREC_SPOSO      DATE,
  ID_TITOLO_STUDIO_SPOSO         NUMBER,
  ID_POS_PROF_ANPR_SPOSO         NUMBER,
  ID_COND_NON_PROF_ANPR_SPOSO    NUMBER,
  ID_CITTADINANZA_SPOSO          NUMBER,
  CODICE_FISCALE_SPOSO           VARCHAR2(16 BYTE),
  ID_COMUNE_RESIDENZA_SPOSO      NUMBER,
  NOME_SPOSA                     VARCHAR2(250 BYTE),
  COGNOME_SPOSA                  VARCHAR2(250 BYTE),
  ID_COMUNE_NASCITA_SPOSA        NUMBER,
  ID_STATO_NASCITA_SPOSA         NUMBER,
  DATA_NASCITA_SPOSA             DATE,
  DATA_CESS_MATR_PREC_SPOSA      DATE,
  ID_TITOLO_STUDIO_SPOSA         NUMBER,
  ID_POS_PROF_ANPR_SPOSA         NUMBER,
  ID_COND_NON_PROF_ANPR_SPOSA    NUMBER,
  ID_CITTADINANZA_SPOSA          NUMBER,
  CODICE_FISCALE_SPOSA           VARCHAR2(16 BYTE),
  ID_COMUNE_RESIDENZA_SPOSA      NUMBER,
  FLG_SEPARAZIONE_BENI           VARCHAR2(1 BYTE),
  ID_ATTO_MATRIMONIO             NUMBER,
  CODICE_INDIVINDUALE_SPOSO      VARCHAR2(20 BYTE),
  CODICE_INDIVINDUALE_SPOSA      VARCHAR2(20 BYTE),
  ID_FLUSSO                      VARCHAR2(30 BYTE),
  ID_CAUSALE                     VARCHAR2(30 BYTE),
  FLG_STATO_ELEBORAZIONE         VARCHAR2(1 BYTE),
  FLG_STATO_RETTIFICA            VARCHAR2(1 BYTE),
  RETTIFICA_VAL_OLD              VARCHAR2(20 BYTE),
  RETTIFICA_VAL_NEW              VARCHAR2(20 BYTE),
  ID_RAMO_ATTIVITA_ECON_SPOSO    NUMBER,
  ID_RAMO_ATTIVITA_ECON_SPOSA    NUMBER,
  ID_STATO_CIVILE_PRIMA_SPOSO    NUMBER,
  ID_STATO_CIVILE_PRIMA_SPOSA    NUMBER,
  ID_STATO_RES_CONIUGALE_SPOSO   NUMBER,
  ID_COMUNE_RES_CONIUGALE_SPOSO  NUMBER,
  ID_STATO_RES_CONIUGALE_SPOSA   NUMBER,
  ID_COMUNE_RES_CONIUGALE_SPOSA  NUMBER,
  ID_LUOGO_RESIDENZA_SPOSO       NUMBER,
  DATA_UPD_ATTO                  DATE,
  DATA_PRATICA                   DATE,
  ID_LUOGO_NASCITA_SPOSO         NUMBER,
  ID_LUOGO_NASCITA_SPOSA         NUMBER,
  ID_LUOGO_RESIDENZA_SPOSA       NUMBER,
  ID_STATO_RES_PRIMA_SPOSA       NUMBER,
  ID_STATO_RES_PRIMA_SPOSO       NUMBER
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

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.NUMERO_ATTO IS 'Campo che indica il numero dell''atto di matrimonio';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.PARTE IS 'Campo che indica il numero della parte dell''atto di matrimonio';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.SERIE IS 'Campo che indica la serie dell''atto di matrimonio';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.DATA_CELEBRAZIONE IS 'Data celebrazione matrimonio';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_TIPO_RITO IS 'identificativo del rito di celebrazione del matrimonio ';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.NOME_SPOSO IS 'nome sposo';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.COGNOME_SPOSO IS 'cognome sposo';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_COMUNE_NASCITA_SPOSO IS 'Identificativo del comune di nascita dello sposo';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_STATO_NASCITA_SPOSO IS 'Identificativo dello stato di nascita dello sposo';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.DATA_NASCITA_SPOSO IS 'data nascita dello sposo';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.DATA_CESS_MATR_PREC_SPOSO IS 'data cessazione matrimonio precedente dello sposo';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_TITOLO_STUDIO_SPOSO IS 'Identificativo del titolo di studio dello sposo';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_POS_PROF_ANPR_SPOSO IS 'Identificativo della posizione professionale dello sposo';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_COND_NON_PROF_ANPR_SPOSO IS 'Identificativo della condizione non professionale dello sposo';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_CITTADINANZA_SPOSO IS 'Identifica lo stato della prima cittadinanza del soggetto sposo';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.CODICE_FISCALE_SPOSO IS 'Codice fiscale dello sposo';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_COMUNE_RESIDENZA_SPOSO IS 'Identificativo del comune di residenza dello sposo';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.NOME_SPOSA IS 'nome sposa';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.COGNOME_SPOSA IS 'cognome sposa';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_COMUNE_NASCITA_SPOSA IS 'Identificativo del comune di nascita della sposa';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_STATO_NASCITA_SPOSA IS 'Identificativo dello stato di nascita della sposa';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.DATA_NASCITA_SPOSA IS 'data nascita della sposa';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.DATA_CESS_MATR_PREC_SPOSA IS 'data cessazione matrimonio precedente della sposa';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_TITOLO_STUDIO_SPOSA IS 'Identificativo del titolo di studio della sposa';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_POS_PROF_ANPR_SPOSA IS 'Identificativo della posizione professionale della sposa';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_COND_NON_PROF_ANPR_SPOSA IS 'Identificativo della condizione non professionale della sposa';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_CITTADINANZA_SPOSA IS 'Identifica lo stato della prima cittadinanza del soggetto sposa';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.CODICE_FISCALE_SPOSA IS 'Codice fiscale della sposa';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_COMUNE_RESIDENZA_SPOSA IS 'Identificativo del comune di residenza della sposa';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.FLG_SEPARAZIONE_BENI IS 'Flag separazione beni [S]I o [N]O';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_ATTO_MATRIMONIO IS 'Campo che indica l''id dell''atto.';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.CODICE_INDIVINDUALE_SPOSO IS 'Codice utilizzato in APR per identificare univocamente il soggetto sposo';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.CODICE_INDIVINDUALE_SPOSA IS 'Codice utilizzato in APR per identificare univocamente il soggetto sposa';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_FLUSSO IS 'Identificativo del Flusso di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_CAUSALE IS 'Identificativo della causale di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.FLG_STATO_ELEBORAZIONE IS 'Flg inserimento su OUT_';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.FLG_STATO_RETTIFICA IS 'Flg inserimento su RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.RETTIFICA_VAL_OLD IS 'In caso di rettifica contiene il vecchio valore del campo COMUNE o STATO';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.RETTIFICA_VAL_NEW IS 'In caso di rettifica contiene il nuovo valore del campo COMUNE o NAZIONE';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_RAMO_ATTIVITA_ECON_SPOSO IS 'Ramo attività economica dello sposo';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_RAMO_ATTIVITA_ECON_SPOSA IS 'Ramo attività economica della sposa';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_STATO_CIVILE_PRIMA_SPOSO IS 'Stato civile pre-matrimonio dello sposo';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_STATO_CIVILE_PRIMA_SPOSA IS 'Stato civile pre-matrimonio della sposa';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_STATO_RES_CONIUGALE_SPOSO IS 'POST-MATRIMONIO - Eventuale residenza in STATO ESTERO';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_COMUNE_RES_CONIUGALE_SPOSO IS 'POST-MATRIMONIO - Comune di residenza coniugale';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_STATO_RES_CONIUGALE_SPOSA IS 'POST-MATRIMONIO - Eventuale residenza in STATO ESTERO';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_COMUNE_RES_CONIUGALE_SPOSA IS 'POST-MATRIMONIO - Comune di residenza coniugale';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_LUOGO_RESIDENZA_SPOSO IS 'Luogo di residenza - SE MEDESIMO O MENO DEL COMUNE DI CELEBRAZIONE';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.DATA_UPD_ATTO IS 'Ultima data di aggiornamento dell''atto';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.DATA_PRATICA IS 'Data prima accoglimento della Pratica/Inizio lavorazioni - differisce dalla data dell''Atto';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_LUOGO_NASCITA_SPOSO IS 'Luogo di nascita - SE MEDESIMO O MENO DEL COMUNE DI CELEBRAZIONE';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_LUOGO_NASCITA_SPOSA IS 'Luogo di nascita - SE MEDESIMO O MENO DEL COMUNE DI CELEBRAZIONE';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_LUOGO_RESIDENZA_SPOSA IS 'POST-MATRIMONIO - Riporta se la residenza coniugale post-matrimonio coinciderà o meno con la residenza attuale';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_STATO_RES_PRIMA_SPOSA IS 'STATO DI RESIDENZA - ITALIA (DEFAULT) O ESTERO';

COMMENT ON COLUMN FT_USR.FT_MATRIMONI.ID_STATO_RES_PRIMA_SPOSO IS 'STATO DI RESIDENZA - ITALIA (DEFAULT) O ESTERO';



CREATE UNIQUE INDEX FT_USR.FT_MATRIMONI_U1 ON FT_USR.FT_MATRIMONI
(ID_ATTO_MATRIMONIO)
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
CREATE TABLE FT_USR.ETL_LOG_ERR
(
  ID              NUMBER(38)                    NOT NULL,
  PROCEDURE_NAME  VARCHAR2(50 BYTE)             NOT NULL,
  ERROR_MESSAGE   VARCHAR2(4000 BYTE),
  NOTE            VARCHAR2(4000 BYTE),
  FLUSSO          VARCHAR2(50 BYTE)             NOT NULL,
  STEP_PROC       NUMBER(10,2),
  DATA_INSERT     DATE,
  ID_SESSIONE     NUMBER(38)                    NOT NULL
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

COMMENT ON COLUMN FT_USR.ETL_LOG_ERR.ID IS 'Identificativo del record';

COMMENT ON COLUMN FT_USR.ETL_LOG_ERR.PROCEDURE_NAME IS 'Nome  della procedura';

COMMENT ON COLUMN FT_USR.ETL_LOG_ERR.ERROR_MESSAGE IS 'descrizione errore';

COMMENT ON COLUMN FT_USR.ETL_LOG_ERR.NOTE IS 'Note';

COMMENT ON COLUMN FT_USR.ETL_LOG_ERR.FLUSSO IS 'Identificativo flusso';

COMMENT ON COLUMN FT_USR.ETL_LOG_ERR.STEP_PROC IS 'step della procedura';

COMMENT ON COLUMN FT_USR.ETL_LOG_ERR.DATA_INSERT IS 'data inserimento record';

COMMENT ON COLUMN FT_USR.ETL_LOG_ERR.ID_SESSIONE IS 'identificativo della sessione';
CREATE TABLE FT_USR.FT_RETTIFICHE
(
  COD_IND        VARCHAR2(20 BYTE),
  COD_FAM        VARCHAR2(20 BYTE),
  TIPO_FAMIGLIA  VARCHAR2(1 BYTE),
  DTA_VAL        VARCHAR2(8 BYTE),
  DTA_OPE        VARCHAR2(8 BYTE),
  DTA_EVE        DATE,
  ID_FLUSSO      VARCHAR2(5 BYTE),
  ID_CAUSALE     VARCHAR2(5 BYTE),
  FLG_SCARTO     VARCHAR2(1 BYTE),
  DTA_SCARTO     DATE,
  SEX_OLD        VARCHAR2(1 BYTE),
  SEX_NEW        VARCHAR2(1 BYTE),
  NAZ_OLD        VARCHAR2(3 BYTE),
  NAZ_NEW        VARCHAR2(3 BYTE),
  COM_OLD        VARCHAR2(5 BYTE),
  COM_NEW        VARCHAR2(5 BYTE),
  MUN_OLD        VARCHAR2(2 BYTE),
  MUN_NEW        VARCHAR2(2 BYTE),
  VAL_OLD        VARCHAR2(10 BYTE),
  VAL_NEW        VARCHAR2(10 BYTE),
  FLG_1          VARCHAR2(2 BYTE),
  STORNO         VARCHAR2(1 BYTE),
  DTA_ORA_OPE    TIMESTAMP(6),
  ID             NUMBER
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

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.COD_IND IS 'Codice Individuale';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.COD_FAM IS 'Codice Famiglia';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.TIPO_FAMIGLIA IS 'Flag Famiglia/Convivenza';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.DTA_VAL IS 'Data Validità';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.DTA_OPE IS 'Data Operazione';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.DTA_EVE IS 'Data Evento';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.ID_FLUSSO IS 'Identificativo Flusso';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.ID_CAUSALE IS 'Identificativo Causale';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.FLG_SCARTO IS 'Flag Scarto';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.DTA_SCARTO IS 'Data Scarto';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.SEX_OLD IS 'Sesso OLD';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.SEX_NEW IS 'Sesso NEW';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.NAZ_OLD IS 'Nazione OLD';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.NAZ_NEW IS 'Nazione NEW';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.COM_OLD IS 'Comune OLD';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.COM_NEW IS 'Comune NEW';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.MUN_OLD IS 'Municipio OLD';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.FLG_1 IS 'FLAG 1';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.STORNO IS 'Storno';

COMMENT ON COLUMN FT_USR.FT_RETTIFICHE.DTA_ORA_OPE IS 'Data Ora Operazione';
CREATE TABLE FT_USR.FT_IMMIGRATI
(
  SOG_MODIFICATO                  VARCHAR2(1 BYTE),
  ID_SOGGETTO                     NUMBER,
  ID_CAMBIO_RESIDENZA_DOMICILIO   NUMBER,
  CONTEGGIO                       VARCHAR2(1 BYTE),
  TIPO_ISTANZA                    VARCHAR2(1 BYTE),
  DATA_IMMIGRAZIONE               DATE,
  ID_RESIDENZA                    NUMBER,
  ID_FAMIGLIA_CONVIVENZA          NUMBER,
  TIPOLOGIA_CAMBIO                VARCHAR2(1 BYTE),
  ID_STATO_ESTERO                 NUMBER,
  ID_LOCALITA                     NUMBER,
  ID_COMUNE_PROVENIENZA           NUMBER,
  ID_SOGGETTO_RESIDENTE           NUMBER,
  ID_STATO_PRATICA                NUMBER,
  ID_RESIDENZA_PROVENIENZA        NUMBER,
  ID_TIPO_RICHIESTA_CAMBIO        NUMBER,
  CODICE_INDIVIDUALE              VARCHAR2(20 BYTE),
  DATA_DEFINIZIONE_PRATICA        DATE,
  SESSO                           VARCHAR2(1 BYTE),
  DATA_PRATICA                    DATE,
  ID_FLUSSO                       VARCHAR2(30 BYTE),
  ID_CAUSALE                      VARCHAR2(30 BYTE),
  FLG_STATO_ELEBORAZIONE          VARCHAR2(1 BYTE),
  FLG_STATO_RETTIFICA             VARCHAR2(1 BYTE),
  RETTIFICA_VAL_OLD               VARCHAR2(20 BYTE),
  RETTIFICA_VAL_NEW               VARCHAR2(20 BYTE),
  DATA_AGGIORNAMENTO              DATE,
  DATA_INSERIMENTO                DATE,
  ID                              NUMBER,
  UTENTE_SIPO                     VARCHAR2(256 BYTE),
  FLG_REPORT                      VARCHAR2(1 BYTE),
  REP_STATO                       VARCHAR2(30 BYTE),
  ID_MUNICIPIO_IN                 NUMBER,
  ID_MUNICIPIO_OUT                NUMBER,
  ID_CITTADINANZA                 NUMBER,
  NUMERO_PRATICA                  NUMBER,
  ID_TIPO_LEGAME                  NUMBER,
  NUMERO_PERSONE                  NUMBER,
  CODICE_FISCALE                  VARCHAR2(16 BYTE),
  DATA_NASCITA                    DATE,
  ID_COMUNE_NASCITA               NUMBER,
  ID_STATO_NASCITA                NUMBER,
  ID_STATO_CIVILE                 NUMBER,
  ID_POS_PROFESSIONALE_ANPR       NUMBER,
  ID_COND_NON_PROFESSIONALE_ANPR  NUMBER,
  ID_TITOLO_STUDIO_ANPR           NUMBER,
  ID_CODICE_LEGAME_APR            NUMBER,
  ID_CODICE_LEGAME_FAMCONV        NUMBER
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

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_SOGGETTO IS 'Identificativo del soggetto';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_CAMBIO_RESIDENZA_DOMICILIO IS 'Campo che identifica univocamente un cambio di residenza o domicillio.';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.CONTEGGIO IS 'Flag che indica se il cambio di residenza ha valenza ai fini del conteggio.valorizzato con S se vale per il conteggio, N altrimenti';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.TIPO_ISTANZA IS 'Flag che descrive la tipologia di istanza del cambio di domicilio:- P istanza di parte;- U istanza d''ufficio.';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.DATA_IMMIGRAZIONE IS 'Data in cui è stato effettuato il cambio di residenza o domicilio';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_RESIDENZA IS 'Codice identificativo della residenza associata al cambio di residenza o domicilio. Identifica la residenza di immigrazione';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_FAMIGLIA_CONVIVENZA IS 'Codice identificativo della famiglia o convivenza in cui intende entrare il soggetto immigrante relativo al cambio di residenza o domicilio';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.TIPOLOGIA_CAMBIO IS 'Flag che indica se la pratica è un cambio di residenza o un cambio di abitazione. R se cambio di residenza, A se cambio di abitazione';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_STATO_ESTERO IS 'Identificativo stato CONF_STATO_ESTERO';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_LOCALITA IS 'Identificativo della Località estera di provenienza Da inserire in alternativa al comune di provenienza';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_COMUNE_PROVENIENZA IS 'Identificativo del comune di provenienza del soggetto immigrante del relativo cambio di residenza o domicilio';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_SOGGETTO_RESIDENTE IS 'Identificativo del soggetto residente alla residenza in cui il dichiarante vuole immigrare';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_STATO_PRATICA IS 'Identificativo dello stato di avanzamento della pratica collegata al cambio di residenza o domicilio. CONF_STATO_PRATICA';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_RESIDENZA_PROVENIENZA IS 'Indirizzo di provenienza del dichiarante della pratica';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_TIPO_RICHIESTA_CAMBIO IS 'Codice identificativo della tipologia di richiesta con il quale è pervenuto il relativo cambio di residenza o domicilio';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.CODICE_INDIVIDUALE IS 'Codice utilizzato in APR per identificare univocamente il soggetto';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.DATA_DEFINIZIONE_PRATICA IS 'Data di comunicazione pratica	dd/mm/yyyy';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.SESSO IS 'Sesso del soggetto';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.DATA_PRATICA IS 'Data definizione della pratica';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_FLUSSO IS 'Identificativo del Flusso di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_CAUSALE IS 'Identificativo della causale di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.FLG_STATO_ELEBORAZIONE IS 'Flg inserimento su OUT_';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.FLG_STATO_RETTIFICA IS 'Flg inserimento su RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.RETTIFICA_VAL_OLD IS 'In caso di rettifica contiene il vecchio valore del campo COMUNE o STATO';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.RETTIFICA_VAL_NEW IS 'In caso di rettifica contiene il nuovo valore del campo COMUNE o NAZIONE';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.DATA_AGGIORNAMENTO IS 'Data ultimo aggiornamento record';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.DATA_INSERIMENTO IS 'Data inserimento record';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID IS 'Identificativo univico OUT_DECESSI';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.UTENTE_SIPO IS 'Nome operatore';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_MUNICIPIO_IN IS 'Identificativo del municipio della residenza';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_MUNICIPIO_OUT IS 'Identificativo del municipio della residenza';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_CITTADINANZA IS 'Identifica lo stato della prima cittadinanza del soggetto';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.NUMERO_PRATICA IS 'Numero associato alla pratica relativa cambio di residenza o domicilio.';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_TIPO_LEGAME IS 'Identificativo tipo di famiglia/convivenza';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.NUMERO_PERSONE IS 'Numero di persone relative alla pratica di cambio residenza o domicilio';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.CODICE_FISCALE IS 'Codice fiscale del soggetto.';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.DATA_NASCITA IS 'Data di nascita';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_COMUNE_NASCITA IS 'Identificativo del comune di nascita';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_STATO_NASCITA IS 'Identificativo della località di nascita';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_STATO_CIVILE IS 'Codice identificativo dello stato civile attuale del soggetto.';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_POS_PROFESSIONALE_ANPR IS 'Identificativo della posizione professionale del soggetto. (in alternativa con ID_COND_NON_PROFESSIONALE_ANPR)';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_COND_NON_PROFESSIONALE_ANPR IS 'Identificativo della condizione non professionale del soggetto. (in alternativa con ID_POS_PROFESSIONALE_ANPR)';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_TITOLO_STUDIO_ANPR IS 'Identificativo del titolo di studio del soggetto.';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_CODICE_LEGAME_APR IS 'Codice del legame del soggetto con la famiglia o con la convivenza a cui è associato.';

COMMENT ON COLUMN FT_USR.FT_IMMIGRATI.ID_CODICE_LEGAME_FAMCONV IS 'Codice del legame che lega il soggetto all''intestatario della famiglia/convivenza ad esso associata.';



CREATE UNIQUE INDEX FT_USR.FT_IMMIGRATI_U1 ON FT_USR.FT_IMMIGRATI
(ID_CAMBIO_RESIDENZA_DOMICILIO, ID_SOGGETTO)
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


CREATE UNIQUE INDEX FT_USR.FT_IMMIGRATI_U2 ON FT_USR.FT_IMMIGRATI
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
CREATE TABLE FT_USR.FT_RESIDENTI
(
  ID_SOGGETTO                   NUMBER,
  CODICE_INDIVIDUALE            VARCHAR2(20 BYTE),
  NOME                          VARCHAR2(250 BYTE),
  COGNOME                       VARCHAR2(250 BYTE),
  CODICE_FISCALE                VARCHAR2(16 BYTE),
  SESSO                         VARCHAR2(1 BYTE),
  ID_FAMIGLIA_CONVIVENZA        NUMBER,
  DATA_NASCITA                  DATE,
  ID_COMUNE_RESIDENZA           NUMBER,
  ID_STATO_CIVICO               NUMBER,
  CODICE_FAMIGLIA               VARCHAR2(20 BYTE),
  ID_COMUNE_NASCITA             NUMBER,
  ID_STATO_NASCITA              NUMBER,
  ID_STATO_CITTADINANZA         NUMBER,
  ID_STATUS_SOGGETTO            NUMBER,
  AIRE                          VARCHAR2(1 BYTE),
  ID_FLUSSO                     VARCHAR2(30 BYTE),
  ID_CAUSALE                    VARCHAR2(30 BYTE),
  FLG_STATO_ELEBORAZIONE        VARCHAR2(1 BYTE),
  FLG_STATO_RETTIFICA           VARCHAR2(1 BYTE),
  RETTIFICA_VAL_OLD             VARCHAR2(20 BYTE),
  RETTIFICA_VAL_NEW             VARCHAR2(20 BYTE),
  DATA_AGGIORNAMENTO            DATE,
  DATA_INSERIMENTO              DATE,
  ID                            NUMBER,
  UTENTE_SIPO                   VARCHAR2(256 BYTE),
  FLG_REPORT                    VARCHAR2(1 BYTE),
  REP_STATO                     VARCHAR2(30 BYTE),
  DATA_DECORRENZA_RESIDENZA     DATE,
  ID_TOPONIMO                   NUMBER,
  ID_CIVICO                     NUMBER,
  ID_MUNICIPIO                  NUMBER,
  CAP                           VARCHAR2(20 BYTE),
  ID_ESTREMI_CATASTALI          NUMBER,
  ID_TIPO_LEGAME                NUMBER,
  DATA_PRIMA_ISCRIZIONE_COMUNE  DATE,
  DATA_DECESSO                  DATE,
  ID_CODICE_LEGAME_APR          NUMBER,
  ID_CODICE_LEGAME_FAMCONV      NUMBER,
  N_COMP_FAM                    NUMBER
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

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.ID_SOGGETTO IS 'Identificativo del soggetto';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.CODICE_INDIVIDUALE IS 'Codice utilizzato in APR per identificare univocamente il soggetto';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.NOME IS 'nome del soggetto';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.COGNOME IS 'cognome del soggetto';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.CODICE_FISCALE IS 'Codice fiscale del soggetto';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.SESSO IS 'sesso';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.ID_FAMIGLIA_CONVIVENZA IS 'identificativo della famiglia o convivenza in APR';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.DATA_NASCITA IS 'data nascita del soggetto';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.ID_COMUNE_RESIDENZA IS 'Identificativo del comune di residenza del soggetto';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.ID_STATO_CIVICO IS 'Identificativo dello stato civile del soggetto';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.CODICE_FAMIGLIA IS 'Codice identificativo della famiglia';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.ID_COMUNE_NASCITA IS 'Identificativo del comune di nascita del soggetto';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.ID_STATO_NASCITA IS 'Identificativo dello stato di nascita del soggetto';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.ID_STATO_CITTADINANZA IS 'Identificativo dello stato di cittadinanza del soggetto';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.ID_STATUS_SOGGETTO IS 'Identificativo dello status del soggetto';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.AIRE IS 'Flag che indica se il soggetto è iscritto all'' AIRE. 
Valorizzato con:- S per indicare AIRE- N per indicare non AIRE""';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.ID_FLUSSO IS 'Identificativo del Flusso di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.ID_CAUSALE IS 'Identificativo della causale di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.FLG_STATO_ELEBORAZIONE IS 'Flg inserimento su OUT_';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.FLG_STATO_RETTIFICA IS 'Flg inserimento su RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.RETTIFICA_VAL_OLD IS 'In caso di rettifica contiene il vecchio valore del campo COMUNE o STATO';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.RETTIFICA_VAL_NEW IS 'In caso di rettifica contiene il nuovo valore del campo COMUNE o NAZIONE';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.DATA_AGGIORNAMENTO IS 'Data ultimo aggiornamento record';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.DATA_INSERIMENTO IS 'Data inserimento record';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.ID IS 'Identificativo univico OUT_DECESSI';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.UTENTE_SIPO IS 'Nome operatore';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.DATA_DECORRENZA_RESIDENZA IS 'data in cui il soggetto ha acquisito la residenza ad esso associata.';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.ID_TOPONIMO IS 'Campo che indica il codice identificatIvo del toponimo.';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.ID_CIVICO IS 'Campo che indica il codice identificatvo del civico.';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.ID_MUNICIPIO IS 'Identificativo del municipio della residenza';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.CAP IS 'Campo che indica il cap dell''idirizzo.';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.ID_ESTREMI_CATASTALI IS 'Campo che indica gli estremi catastali dell''abitazione';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.ID_TIPO_LEGAME IS 'Codice identificavo della tipologia di legame.';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.DATA_PRIMA_ISCRIZIONE_COMUNE IS 'Data in cui il soggetto è stato iscritto per la prima volta in APR.';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.DATA_DECESSO IS 'data decesso del soggetto';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.ID_CODICE_LEGAME_APR IS 'Codice del legame del soggetto con la famiglia o con la convivenza a cui è associato.';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.ID_CODICE_LEGAME_FAMCONV IS 'Codice del legame che lega il soggetto all''intestatario della famiglia/convivenza ad esso associata.';

COMMENT ON COLUMN FT_USR.FT_RESIDENTI.N_COMP_FAM IS 'Numero componenti famiglia/convivenza';



CREATE UNIQUE INDEX FT_USR.FT_RESIDENTI_U1 ON FT_USR.FT_RESIDENTI
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


CREATE UNIQUE INDEX FT_USR.FT_RESIDENTI_U2 ON FT_USR.FT_RESIDENTI
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
CREATE TABLE FT_USR.FT_CITTADINANZE
(
  ID_CASISTICA_CITTADINANZA  NUMBER,
  NUMERO_PRATICA             VARCHAR2(20 BYTE),
  ATTO_TRASCR_NUMEROATTO     VARCHAR2(20 BYTE),
  CODICE_FISCALE             VARCHAR2(16 BYTE),
  DATA_NASCITA               DATE,
  ID_COMUNE_NASCITA          NUMBER,
  ID_STATO_NASCITA           NUMBER,
  SESSO                      VARCHAR2(1 BYTE),
  ID_STATO_CIVILE            NUMBER,
  ID_STATO_CITTADINANZA      NUMBER,
  ID_POS_PROFESSIONALE_ANPR  NUMBER,
  ID_TITOLO_STUDIO_ANPR      NUMBER,
  CODICE_INDIVIDUALE         VARCHAR2(20 BYTE),
  ANNO_ATTO                  NUMBER(4),
  PARTE_ATTO                 VARCHAR2(5 BYTE),
  SERIE_ATTO                 VARCHAR2(10 BYTE),
  NUMERO_ATTO                VARCHAR2(20 BYTE),
  ID_ATTO_CITTADINANZA       NUMBER,
  ID_STATO_PRATICA           NUMBER,
  DATA_PRATICA               DATE,
  ID_PRATICA_RICHIESTA       NUMBER,
  DATA_RESIDENZA_DAL         DATE,
  DATA_FINE_RESIDENZA        DATE,
  ID_COMUNE_RESIDENZA        NUMBER,
  ID_CAUSALE                 VARCHAR2(30 BYTE),
  FLG_STATO_ELEBORAZIONE     VARCHAR2(1 BYTE),
  FLG_STATO_RETTIFICA        VARCHAR2(1 BYTE),
  RETTIFICA_VAL_OLD          VARCHAR2(20 BYTE),
  RETTIFICA_VAL_NEW          VARCHAR2(20 BYTE),
  ID_FLUSSO                  VARCHAR2(30 BYTE),
  UTENTE_SIPO                VARCHAR2(256 BYTE),
  ID_MUNICIPIO               NUMBER,
  ID_TIPO_ATTO               NUMBER,
  ESPONENTE                  VARCHAR2(20 BYTE)
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

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.ID_CASISTICA_CITTADINANZA IS 'Casistica di cittadinanza senza atto';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.NUMERO_PRATICA IS 'Numero pratica di lavorazione - impostata come numero incrementale per ANNO_PRATICA';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.ATTO_TRASCR_NUMEROATTO IS 'ATTO TRASCRITTO: Campo che indica il numero dell''atto originario';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.CODICE_FISCALE IS 'codice fiscale del soggetto';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.DATA_NASCITA IS 'data di nascita del soggetto';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.ID_COMUNE_NASCITA IS 'Identificativo del comune di nascita del soggetto';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.ID_STATO_NASCITA IS 'Identificativo dello stato di nascita del soggetto';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.ID_STATO_CIVILE IS 'Identificativo dello stato civile del soggetto';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.ID_STATO_CITTADINANZA IS 'Identificativo dello stato di cittadinanza del soggetto';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.ID_POS_PROFESSIONALE_ANPR IS 'Identificativo della posizione professionale del soggetto';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.ID_TITOLO_STUDIO_ANPR IS 'Identificativo del titolo di studio del soggetto';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.CODICE_INDIVIDUALE IS 'Codice utilizzato in APR per identificare univocamente il soggetto';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.ANNO_ATTO IS 'Campo che indica l''anno in cui si registra l''atto.';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.PARTE_ATTO IS 'Campo che indica il numero della parte dell''atto.';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.SERIE_ATTO IS 'Campo che indica la serie dell''atto.';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.NUMERO_ATTO IS 'IL NUMERO ATTO VIENE CREATO COME PROGRESSIVO DA 1 A XXXXX PER SINGOLO ANNO E PARTE/SERIE';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.ID_ATTO_CITTADINANZA IS 'Campo che indica l''id dell''atto.';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.ID_STATO_PRATICA IS 'Campo che indica lo stato della pratica.';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.DATA_PRATICA IS 'Data prima accoglimento della Pratica/Inizio lavorazioni - differisce dalla data dell''Atto';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.ID_PRATICA_RICHIESTA IS 'Id Pratica che ha comportato la generazione di questo atto di ATTESTAZIONE (ex. Acquisto cittadinanza art. 2 comma 2 (1.2))';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.DATA_RESIDENZA_DAL IS 'Residenza dalla data';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.DATA_FINE_RESIDENZA IS 'Data fine Residenza';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.ID_COMUNE_RESIDENZA IS 'Identificativo del Comune di residenza';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.ID_CAUSALE IS 'Identificativo della causale di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.FLG_STATO_ELEBORAZIONE IS 'Flg inserimento su OUT_';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.FLG_STATO_RETTIFICA IS 'Flg inserimento su RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.RETTIFICA_VAL_OLD IS 'In caso di rettifica contiene il vecchio valore del campo COMUNE o STATO';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.RETTIFICA_VAL_NEW IS 'In caso di rettifica contiene il nuovo valore del campo COMUNE o NAZIONE';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.ID_FLUSSO IS 'Identificativo del Flusso di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.ID_MUNICIPIO IS 'codice identificativo municipio';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.ID_TIPO_ATTO IS 'Codice identificativo della tipologia di atto.';

COMMENT ON COLUMN FT_USR.FT_CITTADINANZE.ESPONENTE IS 'Campo che indica l''esponente dell''atto';



CREATE UNIQUE INDEX FT_USR.FT_CITTADINANZE_U1 ON FT_USR.FT_CITTADINANZE
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


CREATE UNIQUE INDEX FT_USR.FT_CITTADINANZE_U2 ON FT_USR.FT_CITTADINANZE
(ID_ATTO_CITTADINANZA)
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
CREATE TABLE FT_USR.ETL_LOG
(
  ID              NUMBER(38)                    NOT NULL,
  STATUS          VARCHAR2(50 BYTE)             NOT NULL,
  PROCEDURE_NAME  VARCHAR2(50 BYTE)             NOT NULL,
  ERROR_MESSAGE   VARCHAR2(4000 BYTE),
  NOTE            VARCHAR2(4000 BYTE),
  NOTE_C          CLOB,
  TYPE            VARCHAR2(30 BYTE)             NOT NULL,
  FLUSSO          VARCHAR2(50 BYTE)             NOT NULL,
  ESITO           VARCHAR2(50 BYTE)             NOT NULL,
  STEP_PROC       NUMBER(10,2),
  DATA_INSERT     DATE,
  ID_SESSIONE     NUMBER(38)                    NOT NULL
)
LOB (NOTE_C) STORE AS SECUREFILE (
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
NOLOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN FT_USR.ETL_LOG.ID IS 'Identificativo del record';

COMMENT ON COLUMN FT_USR.ETL_LOG.STATUS IS 'STATUS IN (''IP'', ''INI'',''END'')';

COMMENT ON COLUMN FT_USR.ETL_LOG.PROCEDURE_NAME IS 'Nome della procedura';

COMMENT ON COLUMN FT_USR.ETL_LOG.ERROR_MESSAGE IS 'descrizione Errore -Warning';

COMMENT ON COLUMN FT_USR.ETL_LOG.NOTE IS 'Note';

COMMENT ON COLUMN FT_USR.ETL_LOG.NOTE_C IS 'Note Clob';

COMMENT ON COLUMN FT_USR.ETL_LOG.TYPE IS 'TYPE IN (''ERROR GENERIC'',''ERROR'',''WARNING'',''INFO'')';

COMMENT ON COLUMN FT_USR.ETL_LOG.FLUSSO IS 'Nome identificativo del flusso';

COMMENT ON COLUMN FT_USR.ETL_LOG.ESITO IS 'ESITO IN (''OK'',''KO'')';

COMMENT ON COLUMN FT_USR.ETL_LOG.STEP_PROC IS 'step della procedura ';

COMMENT ON COLUMN FT_USR.ETL_LOG.DATA_INSERT IS 'Data inserimento record';

COMMENT ON COLUMN FT_USR.ETL_LOG.ID_SESSIONE IS 'Identificativo della sessione';



CREATE INDEX FT_USR.ETL_LOG_D1 ON FT_USR.ETL_LOG
(ID_SESSIONE)
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


CREATE UNIQUE INDEX FT_USR.ETL_LOG_U1 ON FT_USR.ETL_LOG
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


ALTER TABLE FT_USR.ETL_LOG ADD (
  CONSTRAINT ETL_LOG_C1
  CHECK (STATUS IN ('IP', 'INI','END'))
  ENABLE VALIDATE,
  CONSTRAINT ETL_LOG_C2
  CHECK (TYPE IN ('ERROR GENERIC','ERROR','WARNING','INFO'))
  ENABLE VALIDATE,
  CONSTRAINT ETL_LOG_C3
  CHECK (ESITO IN ('OK','KO'))
  ENABLE VALIDATE);
CREATE TABLE FT_USR.ETL_CFG_LOG
(
  FLUSSO       VARCHAR2(50 BYTE),
  N_LOG        NUMBER,
  DESCRIZIONE  VARCHAR2(200 BYTE),
  ATTIVO       VARCHAR2(1 BYTE)
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
NOLOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN FT_USR.ETL_CFG_LOG.FLUSSO IS 'Nome identificativo  del flusso';

COMMENT ON COLUMN FT_USR.ETL_CFG_LOG.N_LOG IS 'Livello Log da 0  a 4';

COMMENT ON COLUMN FT_USR.ETL_CFG_LOG.DESCRIZIONE IS 'descrizione livello log';

COMMENT ON COLUMN FT_USR.ETL_CFG_LOG.ATTIVO IS 'Flag attivo Y or N';



CREATE UNIQUE INDEX FT_USR.ETL_CFG_LOG_U1 ON FT_USR.ETL_CFG_LOG
(FLUSSO, N_LOG)
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
CREATE TABLE FT_USR.ETL_RUN_ESITO
(
  ID                   NUMBER                   DEFAULT FT_USR.ETL_LOG_SEQ.NEXTVAL NOT NULL,
  PROCEDURE_NAME       VARCHAR2(200 BYTE),
  FLUSSO               VARCHAR2(50 BYTE),
  ID_SESSIONE          NUMBER(38),
  ESITO                VARCHAR2(50 BYTE),
  ERROR_MESSAGE        VARCHAR2(4000 BYTE),
  NOTE                 VARCHAR2(4000 BYTE),
  INIZIO_ELABORAZIONE  TIMESTAMP(6),
  FINE_ELABORAZIONE    TIMESTAMP(6)
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
NOLOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON COLUMN FT_USR.ETL_RUN_ESITO.ID IS 'Identificativo del record';

COMMENT ON COLUMN FT_USR.ETL_RUN_ESITO.PROCEDURE_NAME IS 'nome della procedura';

COMMENT ON COLUMN FT_USR.ETL_RUN_ESITO.FLUSSO IS 'Nome identificativo del flusso';

COMMENT ON COLUMN FT_USR.ETL_RUN_ESITO.ID_SESSIONE IS 'Identificativo della sessione';

COMMENT ON COLUMN FT_USR.ETL_RUN_ESITO.ESITO IS 'Esito OK or KO';

COMMENT ON COLUMN FT_USR.ETL_RUN_ESITO.ERROR_MESSAGE IS 'Error';

COMMENT ON COLUMN FT_USR.ETL_RUN_ESITO.NOTE IS 'Note';

COMMENT ON COLUMN FT_USR.ETL_RUN_ESITO.INIZIO_ELABORAZIONE IS 'Data inizio flusso';

COMMENT ON COLUMN FT_USR.ETL_RUN_ESITO.FINE_ELABORAZIONE IS 'Data fine flusso';



CREATE INDEX FT_USR.ETL_RUN_ESITO_D1 ON FT_USR.ETL_RUN_ESITO
(PROCEDURE_NAME, FLUSSO, ID_SESSIONE)
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
CREATE TABLE FT_USR.FT_DECESSI
(
  COGNOME                    VARCHAR2(250 BYTE),
  NOME                       VARCHAR2(250 BYTE),
  SESSO                      VARCHAR2(1 BYTE),
  ID_ATTO_DECESSO            NUMBER,
  ID_COMUNE_DECESSO          NUMBER,
  DATA_DECESSO               DATE,
  ORA_DECESSO                VARCHAR2(5 BYTE),
  DATA_NASCITA               DATE,
  ID_COMUNE_NASCITA          NUMBER,
  ID_STATO_NASCITA           NUMBER,
  ID_STATO_CIVILE            NUMBER,
  ID_COMUNE_RESIDENZA        NUMBER,
  ID_STATO_RESIDENZA         NUMBER,
  PARTE                      VARCHAR2(5 BYTE),
  LUOGO_DECESSO              VARCHAR2(200 BYTE),
  ID_RESIDENZA               NUMBER,
  CODICE_INDIVIDUALE         VARCHAR2(20 BYTE),
  CODICE_FISCALE             VARCHAR2(16 BYTE),
  ID_SOGGETTO_GEN2           NUMBER,
  ID_SOGGETTO_GEN1           NUMBER,
  ID_FAMIGLIA_CONVIVENZA     NUMBER,
  ID_CITTADINANZA            NUMBER,
  ID_FLUSSO                  VARCHAR2(30 BYTE),
  ID_CAUSALE                 VARCHAR2(30 BYTE),
  FLG_STATO_ELEBORAZIONE     VARCHAR2(1 BYTE),
  FLG_STATO_RETTIFICA        VARCHAR2(1 BYTE),
  ID_STATO_DECESSO           NUMBER,
  RETTIFICA_VAL_OLD          VARCHAR2(20 BYTE),
  RETTIFICA_VAL_NEW          VARCHAR2(20 BYTE),
  DATA_PRATICA               DATE,
  DATA_UPD_ATTO              DATE,
  AIRE                       VARCHAR2(30 BYTE),
  ID_COMUNE_ISCRIZIONE       NUMBER,
  ANNO_ATTO                  NUMBER(4),
  PARTE_ATTO                 VARCHAR2(5 BYTE),
  SERIE_ATTO                 VARCHAR2(10 BYTE),
  NUMERO_ATTO                VARCHAR2(20 BYTE),
  ID_TITOLO_STUDIO_ANPR      NUMBER,
  UTENTE_SIPO                VARCHAR2(256 BYTE),
  ID_STATUS_SOGGETTO         NUMBER,
  ID_MUNICIPIO               NUMBER,
  CODICE_FAMIGLIA            VARCHAR2(20 BYTE),
  ID_TIPO_LEGAME             NUMBER,
  ID_TIPO_INDIRIZZO          NUMBER,
  ID_TIPO_ATTO               NUMBER,
  TIPO_ATTO_ESTERO_ITALIANO  VARCHAR2(20 BYTE),
  ID_CODICE_LEGAME_APR       NUMBER,
  ID_CODICE_LEGAME_FAMCONV   NUMBER
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

COMMENT ON COLUMN FT_USR.FT_DECESSI.COGNOME IS 'Cognome deceduto';

COMMENT ON COLUMN FT_USR.FT_DECESSI.NOME IS 'Nome deceduto';

COMMENT ON COLUMN FT_USR.FT_DECESSI.SESSO IS 'Sesso deceduto';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_ATTO_DECESSO IS 'Campo che indica l''id dell''atto decesso';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_COMUNE_DECESSO IS 'Comune decesso (prima di arrivo in ospedale)';

COMMENT ON COLUMN FT_USR.FT_DECESSI.DATA_DECESSO IS 'Data/orario Decesso/Rinvenimento corpo/parti non superiore alle 24h dalla data dell''atto decesso';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ORA_DECESSO IS 'Identificativo del tipo di informazione mancante';

COMMENT ON COLUMN FT_USR.FT_DECESSI.DATA_NASCITA IS 'Data di nascita deceduto';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_COMUNE_NASCITA IS 'Identificativo del comune di nascita del deceduto';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_STATO_NASCITA IS 'Identificativo dello stato di nascita del deceduto';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_STATO_CIVILE IS 'Identificativo dello stato civile del deceduto';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_COMUNE_RESIDENZA IS 'Identificativo del comune di residenza del deceduto';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_STATO_RESIDENZA IS 'Identificativo dello stato di residenza del deceduto';

COMMENT ON COLUMN FT_USR.FT_DECESSI.PARTE IS 'Campo che indica il numero della parte dell''atto';

COMMENT ON COLUMN FT_USR.FT_DECESSI.LUOGO_DECESSO IS 'Luogo del decesso (anche ospedale)';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_RESIDENZA IS 'Identifica la residenza attuale della famiglia/collettività';

COMMENT ON COLUMN FT_USR.FT_DECESSI.CODICE_INDIVIDUALE IS 'Codice  utilizzato in APR per identificare univocamente il soggetto deceduto';

COMMENT ON COLUMN FT_USR.FT_DECESSI.CODICE_FISCALE IS 'Codice fiscale del soggetto deceduto';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_SOGGETTO_GEN2 IS 'ID soggetto Genitore 2 - Madre';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_SOGGETTO_GEN1 IS 'ID soggetto Genitore 1 - Padre';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_FAMIGLIA_CONVIVENZA IS 'Identificativo della famiglia o convivenza in APR';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_CITTADINANZA IS 'Identifica lo stato della prima cittadinanza del soggetto';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_FLUSSO IS 'Identificativo del Flusso di  RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_CAUSALE IS 'Identificativo della causale di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_DECESSI.FLG_STATO_ELEBORAZIONE IS 'Flg inserimento su OUT_';

COMMENT ON COLUMN FT_USR.FT_DECESSI.FLG_STATO_RETTIFICA IS 'Flg inserimento su RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_STATO_DECESSO IS 'Comune estero di decesso, se non presente su anagrafiche si consente testo libero. Mutuamente esclusico con ID_COMUNE_DECESSO italiano';

COMMENT ON COLUMN FT_USR.FT_DECESSI.RETTIFICA_VAL_OLD IS 'In caso di rettifica contiene il vecchio valore del campo COMUNE o STATO';

COMMENT ON COLUMN FT_USR.FT_DECESSI.RETTIFICA_VAL_NEW IS 'In caso di rettifica contiene il nuovo valore del campo COMUNE o NAZIONE';

COMMENT ON COLUMN FT_USR.FT_DECESSI.DATA_PRATICA IS 'Data prima accoglimento della Pratica/Inizio lavorazioni - differisce dalla data dell''Atto';

COMMENT ON COLUMN FT_USR.FT_DECESSI.DATA_UPD_ATTO IS 'Ultima data di aggiornamento dell''atto';

COMMENT ON COLUMN FT_USR.FT_DECESSI.AIRE IS 'Flag che indica se il soggetto è iscritto all'' AIRE. Valorizzato con:- S per indicare AIRE- N per indicare non AIRE';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_COMUNE_ISCRIZIONE IS 'ATTO TRASCRITTO: Indica il comune in cui si è registrato/iscritto l''atto originario';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ANNO_ATTO IS 'Campo che indica l''anno in cui si registra l''atto.';

COMMENT ON COLUMN FT_USR.FT_DECESSI.PARTE_ATTO IS 'Campo che indica il numero della parte dell''atto.';

COMMENT ON COLUMN FT_USR.FT_DECESSI.SERIE_ATTO IS 'Campo che indica la serie dell''atto.';

COMMENT ON COLUMN FT_USR.FT_DECESSI.NUMERO_ATTO IS 'IL NUMERO ATTO VIENE CREATO COME PROGRESSIVO DA 1 A XXXXX PER SINGOLO ANNO E PARTE/SERIE';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_TITOLO_STUDIO_ANPR IS 'Identificativo del titolo di studio';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_MUNICIPIO IS 'Identificativo del municipio della residenza';

COMMENT ON COLUMN FT_USR.FT_DECESSI.CODICE_FAMIGLIA IS 'Codice identificativo della famiglia';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_TIPO_LEGAME IS 'tipo di famiglia/convivenza';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_TIPO_INDIRIZZO IS 'Tipologia dell''indirizzo';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_TIPO_ATTO IS 'Codice identificativo della tipologia di atto';

COMMENT ON COLUMN FT_USR.FT_DECESSI.TIPO_ATTO_ESTERO_ITALIANO IS 'Atto Italiano-Estero';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_CODICE_LEGAME_APR IS 'Codice del legame del soggetto con la famiglia o con la convivenza a cui è associato.';

COMMENT ON COLUMN FT_USR.FT_DECESSI.ID_CODICE_LEGAME_FAMCONV IS 'Codice del legame che lega il soggetto all''intestatario della famiglia/convivenza ad esso associata.';



CREATE UNIQUE INDEX FT_USR.FT_DECESSI_U1 ON FT_USR.FT_DECESSI
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


CREATE UNIQUE INDEX FT_USR.FT_DECESSI_U2 ON FT_USR.FT_DECESSI
(ID_ATTO_DECESSO)
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
CREATE TABLE FT_USR.FT_EMIGRATI
(
  ID_SOGGETTO                     NUMBER,
  ID_CAMBIO_RESIDENZA_EMIGR       NUMBER,
  CONTEGGIO                       CHAR(1 BYTE),
  TIPO_ISTANZA                    CHAR(1 BYTE),
  DATA_EMIGRAZIONE                DATE,
  ID_RESIDENZA_ATTUALE            NUMBER,
  ID_FAMIGLIA_CONVIVENZA          NUMBER,
  ID_STATO_PRATICA                NUMBER,
  ID_RESIDENZA_EMIGRAZIONE        NUMBER,
  ID_STATO_EMIGRAZIONE            NUMBER,
  CODICE_INDIVIDUALE              VARCHAR2(20 BYTE),
  DATA_PRATICA                    DATE,
  ID_FLUSSO                       VARCHAR2(30 BYTE),
  ID_CAUSALE                      VARCHAR2(30 BYTE),
  FLG_STATO_ELEBORAZIONE          VARCHAR2(1 BYTE),
  FLG_STATO_RETTIFICA             VARCHAR2(1 BYTE),
  RETTIFICA_VAL_OLD               VARCHAR2(20 BYTE),
  RETTIFICA_VAL_NEW               VARCHAR2(20 BYTE),
  DATA_AGGIORNAMENTO              DATE,
  DATA_INSERIMENTO                DATE,
  ID                              NUMBER,
  UTENTE_SIPO                     VARCHAR2(256 BYTE),
  FLG_REPORT                      VARCHAR2(1 BYTE),
  REP_STATO                       VARCHAR2(30 BYTE),
  SESSO                           VARCHAR2(1 BYTE),
  ID_MOTIVO_COMUNICAZIONE         NUMBER,
  ID_MUNICIPIO_IN                 NUMBER,
  ID_MUNICIPIO_OUT                NUMBER,
  ID_CITTADINANZA                 NUMBER,
  NUMERO_PRATICA                  NUMBER,
  ID_TIPO_LEGAME                  NUMBER,
  NUMERO_PERSONE                  NUMBER,
  CODICE_FISCALE                  VARCHAR2(16 BYTE),
  DATA_NASCITA                    DATE,
  ID_COMUNE_NASCITA               NUMBER,
  ID_STATO_NASCITA                NUMBER,
  ID_STATO_CIVILE                 NUMBER,
  ID_POS_PROFESSIONALE_ANPR       NUMBER,
  ID_COND_NON_PROFESSIONALE_ANPR  NUMBER,
  ID_TITOLO_STUDIO_ANPR           NUMBER,
  ID_CODICE_LEGAME_APR            NUMBER,
  ID_CODICE_LEGAME_FAMCONV        NUMBER
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

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_SOGGETTO IS 'Identificativo unicovo del soggetto';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_CAMBIO_RESIDENZA_EMIGR IS 'Identificativo del CAMBIO_RESIDENZA_EMIGRAZIONE';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.DATA_EMIGRAZIONE IS 'data EMIGRAZIONE';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_RESIDENZA_ATTUALE IS 'Identificativo residenza attuale';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_FAMIGLIA_CONVIVENZA IS 'identificativo della famiglia o convivenza in APR';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_STATO_PRATICA IS 'Identificativo stato pratica CONF_STATO_PRATICA';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_RESIDENZA_EMIGRAZIONE IS 'residenza di emigrazione';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_STATO_EMIGRAZIONE IS 'Identificativo stato emigrazione CONF_STATO_ESTERO';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.CODICE_INDIVIDUALE IS 'Codice utilizzato in APR per identificare univocamente il soggetto';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.DATA_PRATICA IS 'Data prima accoglimento della Pratica/Inizio lavorazioni';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_FLUSSO IS 'Identificativo del Flusso di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_CAUSALE IS 'Identificativo della causale di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.FLG_STATO_ELEBORAZIONE IS 'Flg inserimento su OUT_';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.FLG_STATO_RETTIFICA IS 'Flg inserimento su RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.RETTIFICA_VAL_OLD IS 'In caso di rettifica contiene il vecchio valore del campo COMUNE o STATO';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.RETTIFICA_VAL_NEW IS 'In caso di rettifica contiene il nuovo valore del campo COMUNE o NAZIONE';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.DATA_AGGIORNAMENTO IS 'Data ultimo aggiornamento record';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.DATA_INSERIMENTO IS 'Data inserimento record';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID IS 'Identificativo univico OUT_DECESSI';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.UTENTE_SIPO IS 'Nome operatore';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.SESSO IS 'Sesso del soggetto';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_MOTIVO_COMUNICAZIONE IS 'Identificativo del motivo di emigrazione';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_MUNICIPIO_IN IS 'Identificativo del municipio della residenza';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_MUNICIPIO_OUT IS 'Identificativo del municipio della residenza';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_CITTADINANZA IS 'Identifica lo stato della prima cittadinanza del soggetto';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.NUMERO_PRATICA IS 'Numero associato alla pratica relativa cambio di residenza emigrazione.';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_TIPO_LEGAME IS 'Identificativo tipo di famiglia/convivenza';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.NUMERO_PERSONE IS 'Numero di persone relative alla pratica di cambio residenza emigrazione';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.CODICE_FISCALE IS 'Codice fiscale del soggetto.';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.DATA_NASCITA IS 'Data di nascita';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_COMUNE_NASCITA IS 'Identificativo del comune di nascita';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_STATO_NASCITA IS 'Identificativo della località di nascita';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_STATO_CIVILE IS 'Codice identificativo dello stato civile attuale del soggetto.';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_POS_PROFESSIONALE_ANPR IS 'Identificativo della posizione professionale del soggetto. (in alternativa con ID_COND_NON_PROFESSIONALE_ANPR)';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_COND_NON_PROFESSIONALE_ANPR IS 'Identificativo della condizione non professionale del soggetto. (in alternativa con ID_POS_PROFESSIONALE_ANPR)';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_TITOLO_STUDIO_ANPR IS 'Identificativo del titolo di studio del soggetto.';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_CODICE_LEGAME_APR IS 'Codice del legame del soggetto con la famiglia o con la convivenza a cui è associato.';

COMMENT ON COLUMN FT_USR.FT_EMIGRATI.ID_CODICE_LEGAME_FAMCONV IS 'Codice del legame che lega il soggetto all''intestatario della famiglia/convivenza ad esso associata.';



CREATE UNIQUE INDEX FT_USR.FT_EMIGRATI_U1 ON FT_USR.FT_EMIGRATI
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


CREATE UNIQUE INDEX FT_USR.FT_EMIGRATI_U2 ON FT_USR.FT_EMIGRATI
(ID_CAMBIO_RESIDENZA_EMIGR, ID_SOGGETTO)
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
CREATE TABLE FT_USR.FT_SFD
(
  SESSO                   VARCHAR2(1 BYTE),
  ID_CITTADINANZA         NUMBER,
  ID_ASSOCIAZIONE         NUMBER,
  ID_SENZA_FISSA_DIMORA   NUMBER,
  ID_SOGGETTO             NUMBER,
  NOME                    VARCHAR2(250 BYTE),
  COGNOME                 VARCHAR2(250 BYTE),
  CODICE_FISCALE          VARCHAR2(16 BYTE),
  CODICE_INDIVIDUALE      VARCHAR2(20 BYTE),
  DATA_EMISSIONE          DATE,
  ID_RESIDENZA            NUMBER,
  ID_FLUSSO               VARCHAR2(30 BYTE),
  ID_CAUSALE              VARCHAR2(30 BYTE),
  FLG_STATO_ELEBORAZIONE  VARCHAR2(1 BYTE),
  FLG_STATO_RETTIFICA     VARCHAR2(1 BYTE),
  RETTIFICA_VAL_OLD       VARCHAR2(20 BYTE),
  RETTIFICA_VAL_NEW       VARCHAR2(20 BYTE),
  DATA_AGGIORNAMENTO      DATE,
  DATA_INSERIMENTO        DATE,
  ID                      NUMBER,
  UTENTE_SIPO             VARCHAR2(256 BYTE),
  FLG_REPORT              VARCHAR2(1 BYTE),
  REP_STATO               VARCHAR2(30 BYTE),
  NOME_ASSOCIAZIONE       VARCHAR2(250 BYTE)
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

COMMENT ON COLUMN FT_USR.FT_SFD.SESSO IS 'sesso';

COMMENT ON COLUMN FT_USR.FT_SFD.ID_CITTADINANZA IS 'Identifica lo stato della prima cittadinanza del soggetto';

COMMENT ON COLUMN FT_USR.FT_SFD.ID_ASSOCIAZIONE IS 'identificativo dell''associazione in cui è iscritto il soggeto senza fissa dimora';

COMMENT ON COLUMN FT_USR.FT_SFD.ID_SENZA_FISSA_DIMORA IS 'Identificativo dei dati relativi ad un eventuale stato di senza fissa dimora del soggetto';

COMMENT ON COLUMN FT_USR.FT_SFD.ID_SOGGETTO IS 'Identificativo del soggetto';

COMMENT ON COLUMN FT_USR.FT_SFD.NOME IS 'nome';

COMMENT ON COLUMN FT_USR.FT_SFD.COGNOME IS 'cognome';

COMMENT ON COLUMN FT_USR.FT_SFD.CODICE_FISCALE IS 'Codice fiscale del soggetto';

COMMENT ON COLUMN FT_USR.FT_SFD.CODICE_INDIVIDUALE IS 'Codice utilizzato in APR per identificare univocamente il soggetto';

COMMENT ON COLUMN FT_USR.FT_SFD.DATA_EMISSIONE IS 'Data in cui è stato emesso il nulla osta';

COMMENT ON COLUMN FT_USR.FT_SFD.ID_RESIDENZA IS 'Residenza fisica dichiarata dal soggetto senza fissa dimora';

COMMENT ON COLUMN FT_USR.FT_SFD.ID_FLUSSO IS 'Identificativo del Flusso di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_SFD.ID_CAUSALE IS 'Identificativo della causale di RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_SFD.FLG_STATO_ELEBORAZIONE IS 'Flg inserimento su OUT_';

COMMENT ON COLUMN FT_USR.FT_SFD.FLG_STATO_RETTIFICA IS 'Flg inserimento su RETTIFICA';

COMMENT ON COLUMN FT_USR.FT_SFD.RETTIFICA_VAL_OLD IS 'In caso di rettifica contiene il vecchio valore del campo COMUNE o STATO';

COMMENT ON COLUMN FT_USR.FT_SFD.RETTIFICA_VAL_NEW IS 'In caso di rettifica contiene il nuovo valore del campo COMUNE o NAZIONE';

COMMENT ON COLUMN FT_USR.FT_SFD.DATA_AGGIORNAMENTO IS 'Data ultimo aggiornamento record';

COMMENT ON COLUMN FT_USR.FT_SFD.DATA_INSERIMENTO IS 'Data inserimento record';

COMMENT ON COLUMN FT_USR.FT_SFD.ID IS 'Identificativo univico OUT_SFD';

COMMENT ON COLUMN FT_USR.FT_SFD.UTENTE_SIPO IS 'Nome operatore';

COMMENT ON COLUMN FT_USR.FT_SFD.NOME_ASSOCIAZIONE IS 'nome dell''associazione';
CREATE TABLE FT_USR.LOG_FT_ERROR
(
  ID_ATTO             NUMBER,
  TYPE                VARCHAR2(100 BYTE),
  ERROR_M             VARCHAR2(1000 BYTE),
  DATE_INSERT         DATE                      DEFAULT SYSDATE,
  CODICE_INDIVIDUALE  VARCHAR2(20 BYTE)
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
CREATE TABLE FT_USR.FT_CONVIVENZE
(
  ID_STATO_PRATICA       NUMBER,
  ID_SOGGETTO_C1         NUMBER,
  ID_SOGGETTO_C2         NUMBER,
  ID_CONTRATTO           NUMBER,
  DATA_DOCUMENTO         DATE,
  DATA_INIZIO            DATE,
  DATA_NOTIFICA          DATE,
  DATA_PROTOCOLLO        DATE,
  CODICE_INDIVIDUALE_C1  VARCHAR2(20 BYTE),
  SESSO_C1               VARCHAR2(1 BYTE),
  ID_CITTADINANZA_C1     NUMBER,
  CODICE_INDIVIDUALE_C2  VARCHAR2(20 BYTE),
  SESSO_C2               VARCHAR2(1 BYTE),
  ID_CITTADINANZA_C2     NUMBER,
  ID                     NUMBER
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


CREATE UNIQUE INDEX FT_USR.FT_CONVIVENZE_U1 ON FT_USR.FT_CONVIVENZE
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
