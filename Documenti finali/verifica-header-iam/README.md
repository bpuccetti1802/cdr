# Pagina di verifica delle variabili di header IAM

Due file da innestare in un front-end Thymeleaf esistente per sapere **che cosa IAM manda
davvero a SIPO**. Non è un documento: è codice da consegnare agli sviluppatori.

Il manuale IAM (`RMCAP-IAM-MAN - Integrazione applicativa IAM`, Edizione 16 del
23/06/2025, §3.2) suggerisce lui stesso di prevedere una pagina di questo tipo in fase di
sviluppo, perché le variabili disponibili **dipendono dalla policy configurata per
ciascuna applicazione**: la Tabella 2 dice che cosa IAM *può* mandare, non che cosa manda.

## A che domande risponde

1. **`iv-codfis` arriva anche per i dipendenti?** Il manuale lo dichiara «garantito»
   (p. 15), ma oggi `CdRLoginFilter` lo legge **solo nel ramo cittadino**: per i
   dipendenti non è mai stato verificato sul campo.
2. **`iv-portal-groups` arriva a SIPO, e con quali nomi di gruppo?** Oggi non è letto in
   nessun punto del codice. Se arriva, i gruppi LDAP possono fare da cancello di accesso;
   se non arriva, è una richiesta di configurazione a IAM.
3. **I dati dell'header coincidono con quelli del database?** Per i dipendenti nome,
   cognome e codice fiscale in sessione vengono da `UTENTI`, non dall'header. Sapere se
   divergono decide quale fonte fa fede.

Mostra anche i **ruoli in sessione nell'ordine vero**, segnalando il primo — che è quello
che i front-end usano in 4.829 punti (`getRuoli().get(0).getRuoloBe()`) per scegliere
l'utenza tecnica verso i back-end.

## Come si innesta

1. `VerificaHeaderIamController.java` → nel package dei controller del front-end scelto
   (per esempio `front-end/decessi-web/.../controller/`). Cambia la dichiarazione
   `package` con quella del front-end che lo ospita.
2. `verificaHeaderIam.html` → in `src/main/resources/templates/`.
3. Nel `application.properties` del front-end, **solo sull'ambiente su cui si verifica**:

   ```properties
   verifica.header.iam.abilitata=true
   ```

4. Si raggiunge a `/<contesto>/verificaHeaderIam` (pagina) oppure
   `/<contesto>/verificaHeaderIam.txt` (testo semplice, comodo da incollare in una
   segnalazione).

Il controller dipende solo da ciò che il front-end ha già: Spring Web, Thymeleaf e
`it.romaCapitale.profilazioneUtente` (per `User` e `ConfRuoloVO`). **Nessuna libreria
nuova, nessuna modifica a file esistenti** a parte la riga di properties.

## Avvertenze, che non sono formali

- ⚠️ **Spenta per difetto.** Senza la property il bean non viene nemmeno creato
  (`@ConditionalOnProperty`), quindi l'URL non esiste: un rilascio distratto non la
  espone.
- ⚠️ **Va rispenta o rimossa appena fatta la verifica.** Stampa dati personali.
- ⚠️ **Valori mascherati per difetto** (prime e ultime due lettere più la lunghezza:
  basta a dire «c'è e ha la forma giusta»). Il chiaro si ottiene con `?completo=1` ed è
  da usare solo su collaudo.
- ⚠️ **`Authorization`, `Cookie` e `Set-Cookie` non vengono mai stampati**: trasportano
  credenziali e il gettone di sessione.
- ⚠️ **Ogni apertura è registrata** nel log applicativo a livello WARN con l'utente che
  l'ha chiesta.
- ⚠️ Va raggiunta **passando dal portale**, come una pagina qualunque: è il percorso di
  cui si vuole conoscere il risultato. Raggiungerla scavalcando il portale non dice nulla
  di utile — anzi, se ci si riesce, è di per sé il rilievo RI-04.

## La trappola nel formato dei gruppi

Il manuale dichiara questo formato per `iv-portal-groups`:

```
cn=gruppo1\,ou=Groups\,dc=cdr\,dc=it,cn=gruppo2\,ou=Groups\,dc=cdr\,dc=it
```

I **gruppi** sono separati da virgola; le **componenti del path LDAP** dalla sequenza
backslash-virgola. Uno `split(",")` ingenuo spezza ogni gruppo in quattro pezzi: la
virgola da usare è quella non preceduta da backslash — nel controller,
`split("(?<!\\\\),")`. È il genere di dettaglio che costa un pomeriggio se si scopre
in collaudo.

## Che cosa farne dopo

L'esito va riportato nei punti aperti dell'analisi su identità e profilazione:

| se risulta | conseguenza sul disegno |
|---|---|
| `iv-codfis` presente per i dipendenti | la chiave di ricerca su `UTENTI` diventa il codice fiscale, con `cf_src=IAM-header` |
| `iv-codfis` assente | si resta su `NOME_UTENTE` e il codice fiscale si legge dal database (`cf_src=DB`) |
| `iv-portal-groups` presente | i gruppi diventano il cancello di accesso, e serve la convenzione dei nomi |
| `iv-portal-groups` assente | va chiesto a IAM come variabile (modalità header) o come claim/scope (OIDC) |
| header e database divergono | va deciso quale fonte fa fede, e segnalata la divergenza in login |
