# Riprendere il lavoro da un'altra postazione

`RICOSTRUIRE.md` spiega come rimettere in piedi il **workspace**. Questo spiega dove sono
arrivati **i lavori** e come si continuano.

---

## 1. Prendere il repository

Il repository è su GitHub, privato, e si clona così (serve essere autenticati: `gh auth
login`, oppure un token personale al posto della password):

```bash
git clone https://github.com/bpuccetti1802/cdr.git "Comune di Roma"
cd "Comune di Roma"
```

### Senza GitHub

Se la postazione non raggiunge GitHub, git sa produrre un **pacchetto autoportante**, un
singolo file che contiene l'intera storia.

Sulla postazione di partenza:

```bash
git bundle create workspace-comune-di-roma.bundle --all
```

Si copia quel file con qualunque mezzo — chiavetta, disco, cartella condivisa — e
sull'altra postazione:

```bash
git clone workspace-comune-di-roma.bundle "Comune di Roma"
cd "Comune di Roma"
```

Si ottiene un repository completo, con la storia e il ramo `main`. Quando GitHub sarà
disponibile basta aggiungere il remote e spingere: le due strade non si escludono.

⚠️ Il pacchetto contiene gli stessi 718 file del commit, quindi **niente chiavi, niente
credenziali**. Resta però il lavoro dell'ufficio: si tratta come si tratterebbe una
chiavetta con i documenti di progetto.

---

## 2. Prerequisiti dell'ambiente

```bash
/Library/Developer/CommandLineTools/usr/bin/python3 -c "import docx, openpyxl, yaml, PIL; print('ok')"
```

⚠️ **Usare quell'interprete, non `/usr/bin/python3`**: il secondo non parte finché non è
accettata la licenza Xcode (`sudo xcodebuild -license accept`). È lo stesso motivo per cui
`brew install` fallisce.

Pillow dev'essere arm64. Se dà `incompatible architecture`:

```bash
/Library/Developer/CommandLineTools/usr/bin/python3 -m pip install --user \
    --force-reinstall --no-cache-dir pillow
```

⚠️ **Per eseguire `verifica-conteggi.py` serve il repository di ANSC**, perché 31 delle 40
regole confrontano i numeri scritti nei documenti con le sorgenti vere — decodifiche,
mapping dei casi d'uso, contratti OpenAPI. È pubblico:

```bash
git clone https://github.com/italia/ansc.git ansc
```

Senza, il controllo non gira. Gli altri generatori non ne hanno bisogno, con l'unica
eccezione di `workbook_nascite_morte.py`.

---

## 3. Dove sono arrivati i documenti

| Documento | Versione | Commenti di Word | Punti aperti |
|---|---|---:|---|
| `ANALISI_Integrazione-ANSC` | **v3.31** | 22 | 67 (OP-01…OP-67) |
| `DISEGNO_Back-Office_ANSC` | **v0.6** | 6 | 22 (BO-1…BO-22) |
| `ANALISI_Front-End-Angular` | **v0.6** | — | 16 (OP-FE-1…OP-FE-16) |
| `ANALISI_Identita-Profilazione-IAM` | **v0.3** | — | 19 (PI-01…PI-19) |
| `ASIS_Autenticazione-Profilazione_SIPO` | **v0.2** | — | 12 (PA-1…PA-12) + 21 rilievi |
| `PROCEDURA_Formazione-Atto_SIPO-ANSC` | v0.1 | — | — |
| `SPEC_API_Integrazione-ANSC` | v0.1 | — | PS-1…PS-7 |

⚠️ **Due documenti si rimandano a vicenda e vanno letti insieme**: il disegno del
back-office descrive le pagine (campi, bottoni, tabelle sottese), l'analisi del front-end
le mappa sui componenti della libreria condivisa. Il primo cita il secondo come `[R2]`,
il secondo cita il primo come `[F8]`.

⚠️ I `~$…docx` che compaiono nella cartella indicano solo documenti **aperti in Word**:
vanno chiusi prima di rigenerare, altrimenti il salvataggio fallisce. Non sono versionati.

---

## 4. Il metodo, in cinque regole

1. **Si modifica il file reale, non si rigenera.** I documenti portano modifiche fatte a
   mano e commenti di Word: rigenerarli da script li perderebbe. Ogni versione ha il suo
   script in `Documenti finali/strumenti/v…py`, che parte da una copia della precedente.
2. **I commenti di Word si preservano.** Gli script contano i commenti all'inizio e alla
   fine e si interrompono se il numero cambia. Non togliere quel controllo.
3. **Gli script stanno in `Documenti finali/strumenti/`**, mai nello scratchpad: una
   ripulitura ne ha già fatti perdere tutti, il 3 settembre.
4. **Prima di consegnare, il controllo dei conteggi:**
   ```bash
   cd "Documenti finali"
   /Library/Developer/CommandLineTools/usr/bin/python3 verifica-conteggi.py "<file>.docx"
   ```
   Esce 1 se trova discordanze. I numeri scritti in prosa non si aggiornano da soli quando
   si aggiunge una riga a una tabella: è la classe di errore più frequente su questi
   documenti.
5. **Modello dati e figure sono una coppia.** Se cambia una tabella, l'ERD va rigenerato
   (`strumenti/diagrammi_erd.py`) e sostituito nel documento con `sostituisci_immagine()`.
   È già successo due volte di lasciarlo indietro.

---

## 5. Che cosa è rimasto in sospeso

**Pronto da riportare nei documenti, e sarebbe perso se non stesse qui.**

- **La struttura dei dati di R901**, verificata il 04/10 sul contratto e sul corpus. Va
  portata nella pagina «Dizionari ANSC» del disegno e nel capitolo dei dizionari
  dell'analisi, dove oggi il tracciato è citato ma non riportato per intero. I numeri
  sono in `CLAUDE.md`, sezione «La struttura dei dati di R901»: non rifare la verifica.

**Da decidere, in ordine di peso.**

- **OP-67 / BO-17 — corrispondenze molti-a-uno nella riconciliazione.** La chiave adottata
  ammette un solo valore di SIPO per ciascun valore di ANSC e campo. Va accertato se in
  qualche decodifica due codici locali distinti debbano confluire nello stesso valore —
  il caso di un archivio stratificato, con un codice vecchio e uno nuovo. ⚠️ **La verifica
  si fa sulle tabelle `CONF_*` raccordate**, non sul contratto di ANSC: sono trenta
  decodifiche, per quattro la tabella di SIPO è già indicata nel foglio del Comune. Se il
  caso esiste, la chiave va allargata al valore di SIPO.
- **BO-18 — su quale tabella poggi il registro delle postazioni**, e dove risieda il
  contenitore PKCS#12. La funzione esiste già in SIPO come servizio, alimentata da un
  programma a riga di comando: il registro è suo, e va accertato prima di realizzare
  l'interfaccia disegnata nella pagina «Postazioni e certificati».
- **BO-19 — data di caricamento, operatore e scadenza nel registro dei certificati.**
  Le schermate fornite mostrano solo nome e sede. Senza la scadenza, un certificato
  scaduto si manifesta come un guasto allo sportello invece che come un avviso.
- **BO-22 — la collisione di nomi fra `mfe-operativa` e `mfOperation`.** Due remote
  diversi con nomi quasi identici: il primo sono le pagine sugli atti, il secondo le
  operazioni di postazione. Da rinominare prima che entrino nei manifesti.
- **BO-21 / OP-FE-13 — quando si rientra dal menu su ConfigMap** al registro su base
  dati. La deroga è dichiarata temporanea e vale per il primo rilascio: senza una data di
  riesame diventa l'impianto.
- **BO-20 — accessibilità e note legali nel piè di pagina istituzionale**, che il
  `Footer cdr.jpeg` non porta. Non è nel nostro perimetro, ma va posto a chi governa il
  design system.
- **BO-16 — ambiente e versione nella cornice.** Il committente non intende modificare
  l'interfaccia istituzionale; restano raccomandazioni nel testo.
- **BO-15 — l'area dedicata sotto la testata**, che la shell sta predisponendo: quando
  sarà pronta, il distintivo della sessione OTP vi si trasferisce.
- **BO-10 — se il registro delle pagine debba diventare un registro d'ente** e non solo
  del back-office ANSC.
- **PI-19 — se le applicazioni Angular debbano adottare un BFF**, e con quale
  granularità. Oggi conservano il gettone in `localStorage`.

**Da fare, se si decide di farlo.**

- Portare i rilievi dell'AS-IS sulla sicurezza dentro **OP-06** dell'analisi e
  **OP-FE-11** del front-end. Oggi OP-06 cita i segreti versionati nominando il solo
  client ANPR, mentre la ricognizione ha mostrato che il fenomeno è sistemico.
- Riformulare **OP-15 e OP-16** dell'analisi: danno il certificato server e il registro
  delle postazioni come cose da progettare, mentre un registro con certificati, firma e
  arruolamento **esiste già** in SIPO e alimenta il canale ANPR. Non li chiude, ma li
  cambia di natura — da «costruire» a «estendere». ⚠️ Si lega a BO-18.
- **La clausola di chiusura (`anyRequest()`)**: è l'unico rilievo dell'AS-IS realizzabile
  in giorni e non in mesi, e finché resta aperto il resto conta poco.

---

## 6. Il contesto in una pagina

Il filone principale è la **componente nuova che scrive gli atti di stato civile da SIPO
verso ANSC**. Tre cose da non rimettere in discussione, perché sono state decise e sono
costate tempo:

- **ANSC è presidiato, non asincrono.** La v1.0 lo disegnava come coda non presidiata:
  è sbagliato. R009 deposita davvero e restituisce l'identificativo nazionale; la firma
  richiede un OTP per singolo atto e non è automatizzabile.
- **Il sistema è SIPO-centrico.** L'operatore lavora nelle maschere di SIPO; ANSC è un
  passo di finalizzazione, non un sottosistema attorno a cui riorganizzare il lavoro.
- **Il payload non si costruisce per caso d'uso.** `model_evento.yaml` è un albero solo,
  un superset discriminato: si costruisce una volta e si riempie dalla configurazione.
  Ogni ramo condizionale per famiglia è configurazione mancata.

Il resto — impianto, numeri verificati, decisioni con la loro motivazione — sta in
`CLAUDE.md`, che è lungo ma è la memoria del progetto.
