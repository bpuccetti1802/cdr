# Ricostruire il workspace su una seconda postazione

Questo repository contiene **il lavoro prodotto** — documenti, generatori, sorgenti
documentali — e non i sorgenti applicativi. Quelli hanno già un'origine ufficiale e si
riprendono da lì: sono più aggiornati, e così chiavi private, password in chiaro e dati
personali non lasciano il perimetro dell'ente.

## 1. Prendere questo repository

```bash
git clone https://github.com/bpuccetti1802/cdr.git "Comune di Roma"
cd "Comune di Roma"
```

## 2. Rimettere i sorgenti applicativi

Dal GitLab interno del Comune (serve la VPN):

```bash
# esempio: ciascun modulo è un repository a sé
git clone https://gitlab.ecaas.datacenter.comune.roma/sipo/cross/Signps.git  cross/Signps
git clone https://gitlab.ecaas.datacenter.comune.roma/sipo/sql.git           sipo-root/sql
# … e così per gli altri moduli di common/, cross/, back-end/, front-end/, sipo-root/
```

Il repository di ANSC è pubblico:

```bash
git clone https://github.com/italia/ansc.git ansc
```

La documentazione ANPR (`anpr-9.2.9/`) proviene dal pacchetto Sogei già in uso.

⚠️ **Non copiare le cartelle dei sorgenti da una postazione all'altra con una chiavetta o
con un servizio di sincronizzazione.** Contengono sette PKCS#12 di produzione, le password
dei keystore in chiaro e codici fiscali reali di operatori: ogni copia è una copia di
quelli. Il clone dal GitLab li porta comunque, ma resta dentro il perimetro dell'ente.

## 3. Che cosa manca e non si ricostruisce

Due registrazioni schermo (1,8 GB e 1,6 GB) superano il limite di 100 MB per file di
GitHub e restano solo sulla postazione originale. Non è una perdita: quanto se ne è
ricavato è già nei documenti — la composizione del codice UC cifra per cifra, le sezioni
che la web app chiede e quelle che ricava dal contesto, la finestra dell'OTP.

Restano fuori anche le **credenziali personali di accesso** (`accessi comune di Roma/`).
Sono personali per definizione e si riottengono dal Dipartimento, non da un repository.

## 4. Verificare che l'ambiente funzioni

```bash
/Library/Developer/CommandLineTools/usr/bin/python3 -c "import docx, openpyxl, yaml, PIL; print('ok')"
```

Se Pillow dà `incompatible architecture`, reinstallare la ruota per arm64:

```bash
/Library/Developer/CommandLineTools/usr/bin/python3 -m pip install --user \
    --force-reinstall --no-cache-dir pillow
```

I generatori stanno in `Documenti finali/strumenti/` e si lanciano dalla cartella
`Documenti finali/`. Le immagini in `strumenti/img/` sono versionate perché sono già
incorporate nei documenti: rigenerarle serve solo quando cambia il modello dati.

## 5. Regola di igiene per i commit futuri

Il `.gitignore` esclude per posizione, non per contenuto. Prima di aggiungere una cartella
nuova conviene un controllo:

```bash
git add -A && git diff --cached --name-only | \
  grep -iE '\.(p12|jks|pfx|key|pem)$|accessi|credenzial|token'
```

Se stampa qualcosa, non è pronto per il commit.
