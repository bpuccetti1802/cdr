# -*- coding: utf-8 -*-
"""Analisi delle nascite gemellari, v1.0 (22/11/2026), dal FILE REALE della v0.9.

Richiesta dell'utente: il capitolo «La modalità di integrazione» diventa un MANUALE PER LO
SVILUPPATORE — le pagine da costruire, il loro funzionamento, le tabelle collegate a ogni azione,
le transizioni fra le pagine e i cambi di stato — sulla proposta accettata
PROPOSTA_Pagina-Gemelli_SIPO-ANSC_v0.4.pptx (immagini e flusso dei due casi da lì).
Decisioni recepite: una sola pagina «Gemelli del parto» dopo la divisione; documenti e firmatari
nel Riepilogo; numeri e prenotazione automatici alla divisione in ENTRAMBI i casi (caso 2 con
11999999, verificato dal Comune); passi della card come pulsanti che aprono modali, «Salvato in
SIPO» chip; conformità solo con firme su carta; caso 1 salvataggio automatico alla firma USC;
caso 2 RECUPERA DA ANSC → AGGIORNA SIPO DA ANSC; testo in ANSC_SOGGETTO_ATTO.TXT_TESTO_ATTO;
CANCELLA PRATICA. Elementi dell'incontro del 21/11 [M3]: trascrizioni da ospedale nel
perimetro, UC 1399 solo senza copertura migliore.
Figure: diagrammi_gemellari_v1_0_pptx.py (gem10_*).

    /Library/Developer/CommandLineTools/usr/bin/python3 gemellari_v1_0.py
"""
import os
import re
import sys

import docx
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.text.paragraph import Paragraph

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import docx_comune as D                                             # noqa: E402
from genera_testo_libero import par, voce, tabella                 # noqa: E402
from gemellari_v0_2 import in_coda, sposta_prima, para_che_inizia, figura, codice  # noqa: E402
from gemellari_v0_4 import rifai_voce, riga_di                     # noqa: E402

BASE = os.path.dirname(QUI)
IN = os.path.join(BASE, 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.9.docx')
OUT = os.path.join(BASE, 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v1.0.docx')
NOME = 'ANALISI_Nascite-Gemellari_SIPO-ANSC'
DATA = '22/11/2026'
IMG = os.path.join(QUI, 'img', 'gemellari')
LARGO = 6.3
MODALE = 5.6


def png(nome):
    return os.path.join(IMG, nome)


def h(d, livello, t):
    return d.add_paragraph(t, style='Heading %d' % livello)


def tab(d, righe, larghezze):
    return tabella(d, righe, larghezze)


def cella(t, primo, col, testo):
    D.riscrivi_cella(riga_di(t, primo).cells[col], testo)


def cambia_cella(c, vecchio, nuovo):
    assert vecchio in c.text, (vecchio, c.text[:80])
    D.riscrivi_cella(c, c.text.replace(vecchio, nuovo))


def tabella_con(d, *voci):
    t = [x for x in d.tables if all(v in [c.text for c in x.rows[0].cells] for v in voci)]
    assert len(t) == 1, (voci, len(t))
    return t[0]


# ════════════════════════════════════════════════════════════ il capitolo 7
def capitolo(d, conserva):
    """Scrive in coda il nuovo capitolo; `conserva` = elementi della v0.9 da reinserire."""
    par(d, 'Questo capitolo è il manuale per chi sviluppa l’integrazione dei parti plurimi. '
        'Descrive le pagine da costruire, che cosa fa ogni pulsante, quali servizi chiama, quali '
        'tabelle legge e scrive e come cambiano gli stati dell’atto in SIPO e in ANSC. Le pagine '
        'sono quelle della proposta accettata [P1]; il dimostratore che la accompagna è un file '
        'HTML funzionante su dati fittizi, con il registro delle chiamate simulate, e va letto '
        'insieme a questo capitolo.')
    par(d, 'I casi restano due e non li sceglie l’operatore: li decide l’UC dei nati. Se tutti i '
        'gemelli hanno lo stesso UC si segue il caso 1, tutto con i servizi cooperativi; se gli UC '
        'differiscono il caso 2, in cui gli atti si completano sulla web app. In entrambi i casi '
        'SIPO divide la pratica, stacca i numeri comunali e prenota gli atti in ANSC; poi apre la '
        'stessa pagina, «Gemelli del parto». Cambiano i passi delle card e la direzione in cui '
        'viaggiano i dati alla fine: da SIPO ad ANSC nel caso 1, da ANSC a SIPO nel caso 2.')

    # ── le pagine da costruire
    h(d, 2, 'Le pagine da costruire')
    par(d, 'Una pagina si modifica, una è nuova; tutte le altre interfacce sono modali che si '
        'aprono dalla pagina nuova. La colonna «Sezione» rimanda al punto del capitolo che le '
        'descrive.')
    tab(d, [
        ['#', 'Pagina o modale', 'Tipo', 'Caso', 'Si apre da', 'Sezione'],
        ['P1', 'Riepilogo, con documenti e firmatari per atto', 'pagina esistente, modificata',
         '1 e 2', 'maschera dei gemelli', 'Il Riepilogo'],
        ['P2', 'Gemelli del parto', 'pagina nuova', '1 e 2', 'conferma del Riepilogo; dettaglio '
         'o ricerca di un gemello', 'La pagina «Gemelli del parto»'],
        ['M1', 'Riepilogo numeri', 'modale', '1 e 2', 'testata di P2', 'La testata'],
        ['M2', 'Cancella pratica', 'modale', '1 e 2', 'testata di P2', 'La testata'],
        ['M3', 'Recupera numeri e prenotazione', 'modale', '1 e 2', 'testata di P2, solo se la '
         'divisione non ha completato numeri o prenotazione', 'La divisione'],
        ['M4', 'Validazione', 'modale', '1', 'pulsante Valida della card', 'Caso 1'],
        ['M5', 'Firma dei dichiaranti', 'modale', '1', 'pulsante Firma dichiaranti', 'Caso 1'],
        ['M6', 'Attestazione di conformità', 'modale', '1', 'pulsante Conformità, solo con '
         'firme su carta', 'Caso 1'],
        ['M7', 'Firma dell’USC', 'modale', '1', 'pulsante Firma USC', 'Caso 1'],
        ['M8', 'Verifica in ANSC', 'modale', '1', 'collegamento della card dopo un esito incerto',
         'Caso 1'],
        ['M9', 'Riprova il salvataggio', 'modale', '1', 'collegamento della card con il chip '
         'rosso', 'Caso 1'],
        ['M10', 'Dati per la web app', 'modale', '2', 'pulsante Dati per la web app o '
         'collegamento DETTAGLIO', 'Caso 2'],
        ['M11', 'Recupera da ANSC', 'modale', '2', 'pulsante Recupera da ANSC', 'Caso 2'],
        ['M12', 'Aggiorna SIPO da ANSC', 'modale', '2', 'pulsante Aggiorna SIPO o M11',
         'Caso 2'],
        ['M13', 'Anteprima ANSC', 'modale', '1', 'pannello del testo, atto validato',
         'Il testo dell’atto'],
    ], [0.4, 1.7, 1.0, 0.45, 1.6, 1.15])
    figura(d, png('gem10_navigazione.pptx.png'), LARGO,
           'Le pagine, le modali e i comandi, dal Riepilogo alla pagina «Gemelli del parto»')
    par(d, 'Il percorso di una card, pulsante per pulsante, nei due casi; è la slide della '
        'proposta che riassume il flusso [P1].')
    figura(d, png('gem10_s_percorso.png'), LARGO, 'Il percorso sulla card nei due casi')

    # ── il percorso e le fasi
    h(d, 2, 'Il percorso in sintesi')
    tab(d, [
        ['Fase', 'Pagina', 'Servizi', 'Tabelle scritte', 'Stato SIPO · ANSC'],
        ['Compilazione', 'maschera dei gemelli (come oggi)', 'nascita-be; R005 sui genitori',
         'ATTO_NASCITA, ATTO_NASCITA_SOGGETTO; riga dello store del gemello 1', '1 IN '
         'LAVORAZIONE · —'],
        ['Riepilogo', 'P1', '—', 'MATR_USR.ALLEGATO, ANSC_USR.firmatari (GE-27)', '1 · —'],
        ['Divisione', 'conferma di P1, poi P2', '/performAttiPlurigemellari; POST /richiesta; '
         'R009 /prenota/evento', 'ATTO (N atti); numerazione; ANSC_STATO_ATTO; '
         'ANSC_SOGGETTO_ATTO; ANSC_LOG_AUDIT', '1 · 1 BOZZA per ciascun gemello'],
        ['Lavoro sulle card, caso 1', 'P2 e modali M4…M9', 'R001, R009, R010, R012, R006, R007, '
         '/finalizzaAtto', 'store, ALLEGATO, firmatari, forzatura_validazione, '
         'ANSC_SOGGETTO_ATTO, ATTO_SCANSIONATO', 'per gemello: 1 → 2 DEFINITO · 1 → 5 FIRMATO '
         'DA USC'],
        ['Lavoro sulle card, caso 2', 'P2, M10…M12 e web app', 'R005, /finalizzaAtto',
         'store, tabelle dell’atto in MATR_USR, ANSC_SOGGETTO_ATTO, ATTO_SCANSIONATO',
         'per gemello: 1 → 2 DEFINITO · 1 → 5 sulla web app'],
        ['Parto concluso', 'P2, tutte le card verdi', '—', '—', 'tutti 2 DEFINITO · 5 FIRMATO '
         'DA USC'],
    ], [1.05, 1.05, 1.45, 1.75, 1.0])

    # ── P1 riepilogo
    h(d, 2, 'Il Riepilogo: documenti e firmatari per atto')
    par(d, 'La pagina di riepilogo di oggi, che precede la divisione, si arricchisce di una '
        'scheda per ciascun nato. Lì si raccolgono, atto per atto, i documenti e i firmatari: la '
        'pagina «Gemelli del parto» non ha più un pulsante dei documenti, e sulla card resta solo '
        'il loro numero.')
    voce(d, 'Documenti.', 'L’elenco richiesto dall’UC del nato, letto da ALLEGATI_USECASE con la '
         'presenza (obbligatorio, facoltativo, condizionato): per il nato morto e per il nato vivo '
         'poi deceduto compare il certificato medico. Ogni documento si carica in SIPO (stato 0, '
         'locale) e va in ANSC solo alla validazione (caso 1) o si carica sulla web app (caso 2, '
         'GE-30).')
    voce(d, 'Firmatari.', 'Dichiarante e altri soggetti che firmano l’atto, proposti da '
         'SOGGETTI_USECASE (fg_firmatario) e dai dati della pratica: uno, due o nessun '
         'dichiarante. Il modo di firma (elettronico o su carta) non si sceglie qui ma nella '
         'modale di firma.')
    voce(d, 'Mancanze.', 'Un documento obbligatorio mancante si segnala e non blocca la conferma: '
         'nel caso 1 la Validazione non parte finché manca.')
    voce(d, 'Conferma.', 'La conferma di oggi («la pratica verrà divisa in N atti») avvia la '
         'divisione e, se riesce, numeri e prenotazione; al termine si apre la pagina «Gemelli '
         'del parto».')
    tab(d, [
        ['Azione', 'Servizi', 'Tabelle lette', 'Tabelle scritte', 'Effetto'],
        ['Scelta del nato (scheda)', '—', 'ATTO_NASCITA_SOGGETTO; ANSC_CFG_UC; '
         'ALLEGATI_USECASE; SOGGETTI_USECASE', '—', 'documenti e firmatari del nato'],
        ['CARICA un documento', 'caricamento in SIPO', '—', 'MATR_USR.ALLEGATO (cd_stato 0)',
         'documento del nato'],
        ['ELIMINA un documento', '—', '—', 'MATR_USR.ALLEGATO, solo in stato 0',
         'documento tolto'],
        ['Conferma dei firmatari', '—', 'SOGGETTO, SOGGETTI_USECASE', 'ANSC_USR.firmatari '
         '(ty_soggetto, cd_stato_firma da firmare)', 'elenco per la modale di firma'],
        ['CONFERMA', '/performAttiPlurigemellari, poi la divisione automatica', 'pratica',
         'vedi «La divisione»', 'apre la pagina «Gemelli del parto»'],
    ], [1.2, 1.15, 1.45, 1.55, 0.95])
    par(d, 'Prima della divisione gli atti 2…N non esistono, mentre ALLEGATO e firmatari sono '
        'chiavi sull’atto: come registrare i documenti e i firmatari di ciascun nato fino alla '
        'divisione è GE-27.')

    # ── divisione
    h(d, 2, 'La divisione: numeri comunali e prenotazione')
    par(d, 'Alla conferma SIPO esegue in sequenza quattro passi. Dal secondo in poi sono un’azione '
        'del concentratore, che registra numeri, righe e identificativi insieme; la prenotazione è '
        'una sola chiamata per il parto.')
    tab(d, [
        ['#', 'Passo', 'Servizio', 'Tabelle scritte', 'Stati dopo il passo'],
        ['1', 'Divisione della pratica in N atti', '/performAttiPlurigemellari → '
         'PKG_PRATICA.CREA_ATTI_NASCITA_FIGLI', 'MATR_USR.ATTO (N atti, ID_LAVORAZIONE_PADRE '
         'verso il gemello 1)', 'N atti 1 IN LAVORAZIONE'],
        ['2', 'UC di ciascun nato e scelta del caso', 'all-ansc-sipo (configurazione)',
         'ANSC_STATO_ATTO: gemello 1 UPDATE, gemelli 2…N INSERT con le colonne comuni; '
         'ID_UC_ANSC (caso 1 l’UC comune, caso 2 11999999)', 'COD_FASE UC_DETERMINATO'],
        ['3', 'Stacco di N numeri consecutivi', 'be-numeratore-comunale POST /richiesta',
         'NUMERATORE_COMUNALE, PRENOTAZIONE_ATTI, DATI_ATTO_ESTERNO (1 Disponibile); '
         'ANSC_STATO_ATTO.NUMERO_ATTO', 'numeri assegnati, in ordine di POS_GEMELLO'],
        ['4', 'Prenotazione degli atti', 'all-ansc-sipo → R009 /prenota/evento '
         '(numeroGemelliNatiVivi = N, nati morti compresi; listaNumeriComunali; idUsecase)',
         'ANSC_STATO_ATTO: ID_ANSC, ID_STATO 1, STATO BOZZA, COD_FASE PRENOTATO, TXT_EVENTO; '
         'ANSC_SOGGETTO_ATTO: N righe (COD_ORIGINE PRENOTAZIONE); ANSC_LOG_AUDIT (PRENOTAZIONE); '
         'numeri PUT /utilizza', 'N atti 1 BOZZA in ANSC'],
        ['5', 'Composizione dei testi', 'formulario di SIPO (PKG_FORMULARI) per ciascun atto',
         'ANSC_SOGGETTO_ATTO.TXT_TESTO_ATTO', '—'],
    ], [0.3, 1.25, 1.6, 2.15, 1.0])
    voce(d, 'Abbinamento per numero.', 'Gli identificativi restituiti non si assegnano '
         'confidando nell’ordine delle due liste: ciascun idAnsc contiene il numero comunale '
         '(anno, progressivo nazionale, numero comunale, comune [S5]) e va al gemello che porta '
         'quel numero. Un identificativo che non contiene alcun numero del parto è un errore.')
    voce(d, 'Il caso 2.', 'La prenotazione usa il caso d’uso di servizio 11999999: il Comune ha '
         'verificato che tramite servizi cooperativi si può (GE-31). Gli idAnsc sono quindi noti '
         'dall’inizio anche nel caso 2: il testo cita i fratelli e il recupero cerca per '
         'identificativo, non per numero.')
    voce(d, 'Se un passo non riesce.', 'Se fallisce il passo 1 si resta sul Riepilogo, come oggi. '
         'Se falliscono i passi 3 o 4 la divisione resta: la pagina «Gemelli del parto» si apre '
         'con un avviso e il solo comando RECUPERA NUMERI E PRENOTAZIONE (M3), che prima legge in '
         'ANSC con R005, per numero comunale, che cosa esiste già e poi completa solo ciò che '
         'manca, con gli stessi numeri. Un esito incerto della prenotazione non si ripete mai '
         'alla cieca (GE-13).')
    voce(d, 'La divisione non si annulla più.', 'Dopo la prenotazione gli atti esistono in ANSC: '
         'il pulsante «indietro» dell’anteprima che oggi annulla la divisione non va offerto; la '
         'via d’uscita è CANCELLA PRATICA (GE-09).')

    # ── P2
    h(d, 2, 'La pagina «Gemelli del parto»')
    par(d, 'La pagina ha tre zone: una testata bassa con i dati del parto e i comandi del parto, '
        'una card per ciascun gemello a sinistra e, a destra, il testo dell’atto del gemello '
        'selezionato. È la stessa nei due casi; cambiano i passi delle card.')
    figura(d, png('gem10_s_caso1.png'), LARGO, 'Caso 1: la pagina con il gemello 1 concluso, il '
           'gemello 2 alla firma dei dichiaranti e il gemello 3 in bozza (ipotesi)')
    figura(d, png('gem10_s_caso2.png'), LARGO, 'Caso 2: la pagina con il gemello 1 recuperato da '
           'ANSC, il gemello 2 selezionato e il gemello 3 da completare sulla web app (ipotesi)')
    h(d, 3, 'Quando si apre')
    voce(d, 'Dopo la conferma del Riepilogo.', 'Al termine della divisione automatica.')
    voce(d, 'Dal dettaglio o dalla ricerca di un gemello.', 'Qualunque atto con '
         'ID_LAVORAZIONE_PADRE, o che lo è per altri, porta alla pagina del suo parto. Aprire la '
         'pagina è già riprendere: non c’è una pagina di ripresa separata.')
    voce(d, 'Che cosa legge all’apertura.', 'Le righe del parto (l’interrogazione è in «Le '
         'tabelle») e, per ciascuna riga con identificativo, lo stato in ANSC con R005: se lo '
         'store è rimasto indietro, per esempio dopo una chiusura del browser, vale lo stato letto '
         'in ANSC, che si riscrive nello store. Un atto a 3 ANNULLATO, 9 CANCELLATO o 10 '
         'INEFFICACE, o con un identificativo diverso da quello registrato, blocca la card e '
         'compare nella supervisione [R1].')
    h(d, 3, 'La testata')
    par(d, 'Riporta genitori e dichiarante (codici fiscali mascherati), data e luogo, tipo atto e '
        'caso, lo stato della sessione OTP verso ANSC e tre comandi.')
    tab(d, [
        ['Comando', 'Abilitato', 'Che cosa fa', 'Servizi', 'Tabelle scritte'],
        ['RIEPILOGO NUMERI (M1)', 'sempre, dopo lo stacco', 'per ciascun gemello numero '
         'comunale, idAnsc e stato; STAMPA come promemoria', '—', '—'],
        ['CANCELLA PRATICA (M2)', 'solo se nessun gemello è FIRMATO DA USC', 'cancella le bozze '
         'in ANSC, scarta i numeri, cancella la pratica in SIPO; non si annulla', 'R011 '
         '/evento/elimina per gemello; PUT /scarta; /cancellaAnnullaAtto (ANNULLAMENTOPRATICA)',
         'ANSC_STATO_ATTO (ID_STATO 9, COD_FASE ANNULLATO); DATI_ATTO_ESTERNO (3 Scartato); '
         'ATTO; ANSC_LOG_AUDIT (ANNULLAMENTO)'],
        ['RECUPERA NUMERI E PRENOTAZIONE (M3)', 'solo se numeri o prenotazione non sono '
         'completi', 'R005 per numero comunale, poi completa numeri e prenotazione', 'R005; POST '
         '/richiesta; R009 /prenota/evento', 'come i passi 3 e 4 della divisione'],
        ['Stato OTP', 'sempre', 'tempo residuo della sessione; RICHIEDI o RINNOVA OTP', 'PUT '
         '/ansc/v1/sessione [R1]', '—'],
    ], [1.3, 1.1, 1.55, 1.25, 1.1])
    voce(d, 'CANCELLA PRATICA e un esito incerto.', 'Se R011 non risponde per un gemello, la '
         'modale non ripete la chiamata: legge lo stato con R005 e cancella solo ciò che è '
         'ancora in bozza.')
    h(d, 3, 'Le card')
    par(d, 'Una card per gemello, nell’ordine di nascita. I passi sono pulsanti che aprono una '
        'modale; il solo «Salvato in SIPO» è un chip, che non si clicca e si accende quando '
        'l’atto di SIPO è definito.')
    figura(d, png('gem10_s_card.png'), 4.6, 'La card: passi come pulsanti e chip finale; con una '
           'firma su carta si abilita la conformità, senza la conformità «non serve» (ipotesi)')
    tab(d, [
        ['Elemento della card', 'Fonte'],
        ['Gemello k · sesso · nome', 'ANSC_SOGGETTO_ATTO.NUM_PROGRESSIVO_GEMELLO; '
         'ATTO_NASCITA_SOGGETTO'],
        ['Tipologia di nascita', 'ANSC_SOGGETTO_ATTO.ID_TIPO_NASCITA (ANSC_107), dai due flag di '
         'SIPO'],
        ['UC', 'ANSC_STATO_ATTO.ID_UC_ANSC; nel caso 2 11999999, con accanto l’UC specifico del '
         'nato calcolato dai flag'],
        ['Numero comunale, in grande', 'ANSC_STATO_ATTO.NUMERO_ATTO'],
        ['idAnsc, con il numero comunale evidenziato', 'ANSC_STATO_ATTO.ID_ANSC'],
        ['Stato, senza codice (FIRMATO DA USC in verde)', 'ANSC_STATO_ATTO.ID_STATO e STATO, '
         'COD_FASE (corrispondenza in «Le transizioni e i cambi di stato»)'],
        ['Documenti e firmatari (numero)', 'MATR_USR.ALLEGATO; ANSC_USR.firmatari'],
        ['Conformità abilitata', 'almeno una riga di firmatari con ty_firma CARTA'],
        ['Chip «Salvato in SIPO»', 'MATR_USR.ATTO.ID_STATO_PRATICA = 2; rosso se l’atto è a 5 in '
         'ANSC e non definito in SIPO'],
        ['Caso 2: nascita, ora, luogo, posizione, dichiarante', 'ATTO_NASCITA_SOGGETTO '
         '(DATAORARIO_NASCITA, POS_GEMELLO), ATTO_NASCITA, dati del dichiarante'],
    ], [2.4, 3.9])
    voce(d, 'Quale card si lavora.', 'Qualunque card non ancora FIRMATO DA USC, in qualsiasi '
         'ordine. Il clic su una card la seleziona e porta il suo testo nel pannello di destra; '
         'il clic su un pulsante la seleziona e apre la modale.')
    voce(d, 'Un’azione alla volta.', 'Mentre una modale chiama un servizio i suoi pulsanti si '
         'disabilitano e la modale non si chiude: nessuna chiamata parte due volte.')
    voce(d, 'Sessione OTP.', 'Se la sessione verso ANSC manca o è sotto la soglia di guardia, la '
         'modale chiede il codice prima di cominciare (GE-12).')
    voce(d, 'Collegamenti secondari.', 'STAMPA, APRI IL PDF (atto definito), TORNA AI DATI '
         '(dalla modale di firma), VERIFICA IN ANSC (esito incerto), RIPROVA IL SALVATAGGIO '
         '(chip rosso), DETTAGLIO e COPIA TESTO (caso 2).')
    h(d, 3, 'Il testo dell’atto')
    par(d, 'Il pannello di destra mostra il testo dell’atto del gemello selezionato. Lo compone '
        'SIPO con il formulario dopo la prenotazione, quando sono noti il numero comunale del '
        'gemello e gli identificativi nazionali dei fratelli, e lo conserva in '
        'ANSC_SOGGETTO_ATTO.TXT_TESTO_ATTO. È lo stesso nei due casi; cambia la via verso ANSC: '
        'nel caso 1 viaggia con la validazione in evento.composizioneCompleta, come chiede ANSC '
        'per le bozze prenotate da gestionale [A12]; nel caso 2 l’ufficiale lo copia nella '
        'composizione libera della bozza sulla web app.')
    conserva['attne']()
    tab(d, [
        ['Comando', 'Caso', 'Abilitato', 'Che cosa fa', 'Tabelle'],
        ['SALVA TESTO', '1 e 2', 'testo modificato e ancora modificabile', 'registra il testo',
         'ANSC_SOGGETTO_ATTO.TXT_TESTO_ATTO, TS_TESTO_ATTO'],
        ['STAMPA', '1 e 2', 'sempre', 'stampa il testo del gemello', '—'],
        ['COPIA TESTO', '2', 'finché l’atto non è recuperato', 'copia il testo negli appunti '
         'per la composizione libera', '—'],
        ['ANTEPRIMA ANSC (M13)', '1', 'atto validato', 'R010 /anteprima/evento con presaVisione: '
         'il PDF di ANSC con il testo ricevuto', 'ANSC_LOG_AUDIT (ANTEPRIMA)'],
    ], [1.15, 0.5, 1.4, 1.75, 1.5])
    voce(d, 'Fino a quando è modificabile.', 'Nel caso 1 fino a Valida, che lo invia; dopo, si '
         'modifica solo tornando ai dati dalla modale di firma, e la nuova validazione lo invia '
         'di nuovo. Nel caso 2 finché l’atto non è recuperato da ANSC.')
    voce(d, 'Che cosa resta in SIPO.', 'Nel caso 1 la definizione genera il PDF da '
         'TXT_TESTO_ATTO, cioè dal testo inviato ad ANSC. Nel caso 2 AGGIORNA SIPO DA ANSC '
         'sostituisce TXT_TESTO_ATTO con la composizione letta da ANSC e il PDF nasce da quella '
         '(GE-25).')

    # ── caso 1
    h(d, 2, 'Caso 1: i passi della card e le loro modali')
    par(d, 'I quattro passi si eseguono in ordine su ciascun gemello. Il pulsante del passo di '
        'turno è il primario; i passi fatti sono verdi con la spunta e non si cliccano più. La '
        'conformità si salta se nessun dichiarante ha firmato su carta: il pulsante mostra '
        '«Conformità · non serve» e la Firma USC si abilita subito.')
    tab(d, [
        ['Pulsante', 'Si abilita quando', 'Apre'],
        ['Valida', 'BOZZA (prenotato), anche dopo TORNA AI DATI', 'M4 Validazione'],
        ['Firma dichiaranti', 'CONFERMATO', 'M5 Firma dei dichiaranti'],
        ['Conformità', 'FIRMATO DAL DICHIARANTE e almeno una firma su carta',
         'M6 Attestazione di conformità'],
        ['Firma USC', 'FIRMATO PER CONFORMITÀ, oppure FIRMATO DAL DICHIARANTE senza firme su '
         'carta', 'M7 Firma dell’USC'],
        ['chip Salvato in SIPO', 'non è un pulsante: si accende a /finalizzaAtto riuscita', '—'],
    ], [1.4, 3.3, 1.6])

    h(d, 3, 'M4 · Validazione')
    figura(d, png('gem10_s_validazione.png'), MODALE, 'La modale «Validazione», con un esito di '
           'anomalie superabili (ipotesi)')
    par(d, 'Riepiloga che cosa si invia ad ANSC (dati dell’atto, testo, documenti, firmatari) e '
        'mostra l’esito della validazione nella forma della risposta di ANSC.')
    tab(d, [
        ['Azione', 'Servizi', 'Tabelle lette', 'Tabelle scritte', 'Stato dopo'],
        ['VALIDA', 'R001 per ogni documento in stato 0 (attesa di ANSC_08 = 3 Inserito); '
         'R009 /validazione/evento sulla bozza prenotata', 'ALLEGATO; ANSC_CFG_CAMPO; '
         'ANSC_SOGGETTO_ATTO (testo, fratelli); tabelle dell’atto', 'ALLEGATO (cd_stato, '
         'id_ansc_allegato); ANSC_STATO_ATTO (TXT_EVENTO, NUM_REVISIONE); ANSC_LOG_AUDIT '
         '(ALLEGATI, DEPOSITO)', 'esito positivo: CONFERMATO (ID_STATO 2, TS_VALIDAZIONE, '
         'COD_FASE VALIDATO)'],
        ['esito con errori', '—', '—', 'ANSC_STATO_ATTO.ULTIMO_ERRORE', 'resta BOZZA; si '
         'correggono i dati e si valida di nuovo'],
        ['FORZA LA VALIDAZIONE (solo USC)', 'seconda R009 con il forcingCode', 'risposta '
         'precedente', 'forzatura_validazione; store come per l’esito positivo', 'CONFERMATO'],
        ['ANNULLA', '—', '—', '—', 'invariato'],
    ], [1.05, 1.5, 1.2, 1.6, 0.95])
    voce(d, 'Il modello evento.', 'Il concentratore valorizza i campi che nessun mapping '
         'dichiara: partoGemellare, numeroGemelli, progressivoGemello, gli elenchi dei fratelli e '
         'lo stato del nato (natoMorto, natoVivoMaDeceduto) dai flag di SIPO; '
         'composizioneCompleta è TXT_TESTO_ATTO. La combinazione dei due flag entrambi a S si '
         'respinge prima della chiamata.')
    voce(d, 'L’identificativo.', 'La validazione deve riconoscere la bozza prenotata (GE-02): se '
         'restituisce un idAnsc diverso, si riallineano lo store, la riga del gemello e i '
         'riferimenti dei due fratelli adiacenti.')
    voce(d, 'Esito incerto.', 'La modale non ripete R009: chiude con VERIFICA IN ANSC (M8).')

    h(d, 3, 'M5 · Firma dei dichiaranti')
    figura(d, png('gem10_s_firma_dich.png'), MODALE, 'La modale «Firma dei dichiaranti» con due '
           'dichiaranti: il padre con la firma elettronica, la madre su carta (ipotesi)')
    par(d, 'Elenca i dichiaranti raccolti nel Riepilogo: uno, due o nessuno. Per ciascuno si '
        'sceglie il modo di firma; la firma si chiede nella modale. Senza dichiaranti la modale '
        'lo dice e PROSEGUI porta alla firma dell’USC (GE-28).')
    tab(d, [
        ['Azione', 'Servizi', 'Tabelle scritte', 'Effetto'],
        ['Scelta del modo, per dichiarante', '—', '—', 'elettronica o su carta; non si cambia '
         'dopo l’invio del link o il caricamento'],
        ['INVIA LINK (elettronica)', 'R012 /firmadichiarante/invio-email', 'firmatari '
         '(ty_firma ELETTRONICA, ds_email_notifica_firma, id_presa_visione, cd_stato_firma LINK '
         'INVIATO); ANSC_LOG_AUDIT (FIRMA_DICH)', 'il dichiarante riceve il link all’anteprima'],
        ['AGGIORNA STATO', 'R012 /firmadichiarante/pooling-statoatto', 'firmatari.cd_stato_firma '
         '(1 visionato → FIRMATO, 2 annullato)', 'stato della presa visione'],
        ['ANNULLA LINK', 'R012 /firmadichiarante/annulla-link', 'firmatari.cd_stato_firma',
         'si può scegliere di nuovo il modo'],
        ['STAMPA MODULO (carta)', 'R010 /anteprima/evento con presaVisione', '—', 'il PDF di '
         'ANSC da far firmare in sala'],
        ['CARICA FILE FIRMATO (carta)', 'R006 /firmadichiarante/upload, un file con '
         'listaFirmatari di tutti i dichiaranti su carta', 'ALLEGATO (processo verbale, ANSC_09 '
         '999); firmatari (ty_firma CARTA, cd_stato_firma FIRMATO); ANSC_LOG_AUDIT (FIRMA_DICH)',
         'firma acquisita'],
        ['CONFERMA LE FIRME', '—', 'ANSC_STATO_ATTO (ID_STATO 4 come restituito da ANSC)',
         'FIRMATO DAL DICHIARANTE; con una firma su carta si abilita Conformità'],
        ['TORNA AI DATI', 'R012 annulla-link per i link aperti', 'ANSC_STATO_ATTO (stato 0, '
         'COD_FASE IN_LAVORAZIONE); firmatari azzerati', 'si torna a BOZZA: nuova validazione '
         'dello stesso atto'],
    ], [1.35, 1.6, 2.15, 1.2])
    voce(d, 'Il ritorno ai dati dopo una firma.', 'Ammesso solo se tutti i firmatari possono '
         'firmare di nuovo: la modale lo chiede prima di procedere.')
    voce(d, 'La firma elettronica nei parti gemellari.', 'La guida ANSC la esclude per i parti '
         'gemellari sulla web app [A3]; nel caso 1 la pagina la prevede tramite R012, e va '
         'provata sulle bozze prenotate (GE-28). Nel caso 2 vale solo la firma su carta.')

    h(d, 3, 'M6 · Attestazione di conformità')
    figura(d, png('gem10_s_conformita.png'), MODALE, 'La modale «Attestazione di conformità» '
           '(ipotesi)')
    par(d, 'Si apre solo se almeno un dichiarante ha firmato su carta. L’ufficiale attesta che le '
        'copie per immagine dei documenti cartacei sono conformi agli originali: il modulo '
        'firmato su carta è sempre incluso, gli altri documenti sono preselezionati e '
        'l’ufficiale può escluderli (i P7M sono già firmati digitalmente).')
    tab(d, [
        ['Azione', 'Servizi', 'Tabelle scritte', 'Stato dopo'],
        ['Selezione dei documenti', '—', 'ALLEGATO.fg_incluso_att_conformita', '—'],
        ['ANTEPRIMA ATTESTAZIONE', 'R010 /anteprima/attestazione', 'ANSC_LOG_AUDIT (ANTEPRIMA)',
         '—'],
        ['FIRMA PER CONFORMITÀ', 'R007 /attestazione/firma con gli allegati e il loro '
         'flagAttConformita; parametri di firma in base64', 'ANSC_STATO_ATTO (ID_STATO 11); '
         'ANSC_LOG_AUDIT (FIRMA_CONFORMITA)', 'FIRMATO PER CONFORMITÀ; si abilita Firma USC'],
        ['errore di firma (406001, 406002, 406004)', '—', 'ANSC_STATO_ATTO.ULTIMO_ERRORE',
         'invariato; si riprova, anche con un nuovo OTP di firma'],
    ], [1.5, 1.9, 1.9, 1.0])
    voce(d, 'Le credenziali.', 'Utente, PIN e OTP sono quelli del servizio di firma remota, non '
         'l’OTP della sessione ANSC della testata; la modalità «in chiaro» non è accettata in '
         'produzione.')

    h(d, 3, 'M7 · Firma dell’USC')
    figura(d, png('gem10_s_firma_usc.png'), MODALE, 'La modale «Firma dell’USC», con i due passi '
           'dell’avanzamento: firma in ANSC e salvataggio in SIPO (ipotesi)')
    par(d, 'Riepiloga l’atto (numero, idAnsc, intestatario, firme raccolte), offre l’anteprima '
        'di ANSC e chiede la conferma di lettura e le credenziali di firma remota. FIRMA L’ATTO '
        'esegue due passi, mostrati in sequenza: la firma in ANSC e il salvataggio in SIPO. Non '
        'c’è un pulsante di salvataggio: alla firma riuscita SIPO definisce l’atto da sé.')
    tab(d, [
        ['Passo', 'Servizi', 'Tabelle scritte', 'Stato dopo'],
        ['ANTEPRIMA ATTO', 'R010 /anteprima/evento con presaVisione', 'ANSC_LOG_AUDIT '
         '(ANTEPRIMA)', '—'],
        ['1 · Firma in ANSC', 'R007 /firma_usc', 'ANSC_STATO_ATTO (ID_STATO 5, COD_FASE '
         'FIRMATO); ANSC_LOG_AUDIT (FIRMA_USC)', 'FIRMATO DA USC: non si torna più ai dati'],
        ['2 · Salvataggio in SIPO', '/finalizzaAtto per il solo gemello', 'ATTO (ID_STATO_PRATICA '
         '2, DATA_DEFINIZIONE_ATTO); ATTO_SCANSIONATO (PDF da TXT_TESTO_ATTO); dopo '
         'l’iscrizione anagrafica ANSC_SOGGETTO_ATTO.ID_SOGGETTO', '2 DEFINITO; chip verde'],
        ['errore di firma con codice', '—', 'ANSC_STATO_ATTO.ULTIMO_ERRORE', 'invariato; si '
         'riprova'],
        ['firma senza risposta', '—', '—', 'card con VERIFICA IN ANSC (M8)'],
        ['salvataggio non riuscito', '—', '—', 'FIRMATO DA USC con chip rosso e RIPROVA IL '
         'SALVATAGGIO (M9)'],
    ], [1.35, 1.55, 2.3, 1.1])

    h(d, 3, 'M8 · Verifica in ANSC e M9 · Riprova il salvataggio')
    voce(d, 'Verifica in ANSC.', 'Dopo un esito incerto della firma (o della validazione) legge '
         'lo stato dell’atto con R005 per idAnsc, lo scrive nello store (ID_STATO, STATO; '
         'ANSC_LOG_AUDIT RICONCILIAZIONE) e decide: se è 5 FIRMATO DA USC prosegue con il '
         'salvataggio in SIPO; se è ancora 11 o 4 la firma si può ripetere.')
    voce(d, 'Riprova il salvataggio.', 'L’atto è già formato in ANSC: si ripete la sola '
         '/finalizzaAtto, senza altre chiamate ad ANSC (GE-21).')

    # ── caso 2
    h(d, 2, 'Caso 2: i passi della card e le loro modali')
    par(d, 'Gli atti sono prenotati con il caso d’uso di servizio e si completano e si firmano '
        'sulla web app. La card porta più informazioni sul nato, per trovare ciò che serve alla '
        'compilazione a mano, e quattro passi: Dati per la web app, Web app, Recupera da ANSC, '
        'Aggiorna SIPO.')
    tab(d, [
        ['Pulsante', 'Si abilita quando', 'Apre', 'Tabelle scritte'],
        ['Dati per la web app', 'sempre (anche dal collegamento DETTAGLIO)', 'M10',
         'ANSC_STATO_ATTO.COD_PAGINA_RIPRESA (DATI_WEBAPP)'],
        ['Web app', 'sempre; primario dopo i dati', 'la web app ANSC, fuori da SIPO',
         'ANSC_STATO_ATTO.COD_PAGINA_RIPRESA (WEBAPP)'],
        ['Recupera da ANSC', 'sempre; primario dopo la web app', 'M11', 'vedi M11'],
        ['Aggiorna SIPO', 'recupero con l’atto FIRMATO DA USC', 'M12', 'vedi M12'],
        ['chip Salvato in SIPO', 'non è un pulsante: si accende a /finalizzaAtto riuscita', '—',
         '—'],
    ], [1.3, 1.9, 1.3, 1.8])

    h(d, 3, 'M10 · Dati per la web app')
    figura(d, png('gem10_s_dati_webapp.png'), MODALE, 'La modale «Dati per la web app»: le '
           'sezioni del caso d’uso di servizio, con la copia per campo (ipotesi)')
    par(d, 'Riporta, sezione per sezione e nell’ordine della web app, i valori che l’ufficiale '
        'deve inserire nella bozza prenotata: è la scheda di dettaglio del gemello. Non scrive '
        'nulla; ogni valore si copia con un clic.')
    tab(d, [
        ['Linguetta', 'Campi (mapping Dic_Nasc_999)', 'Fonte in SIPO'],
        ['Formazione atto', 'numero comunale; data, ora e minuti di formazione',
         'ANSC_STATO_ATTO.NUMERO_ATTO; data di formazione'],
        ['Dati generali', 'tipologia di nascita (ANSC_107); data e ora di decorrenza; motivo del '
         'recupero (ANSC_96, GE-29); atto secretato', 'ANSC_SOGGETTO_ATTO.ID_TIPO_NASCITA; '
         'ATTO_NASCITA_SOGGETTO'],
        ['Soggetto', 'cognome, nome, sesso, data, ora e minuto, stato e comune di nascita, luogo, '
         'assegnazione del cognome', 'ATTO_NASCITA_SOGGETTO, ATTO_NASCITA'],
        ['Madre, Padre', 'anagrafica, nascita, nazionalità, residenza, flag dichiarante, '
         'comparente, firmatario', 'SOGGETTO dei genitori; firmatari'],
        ['Dichiarante', 'chi dichiara; firma su carta', 'dati della pratica; firmatari'],
        ['Nel parto', 'posizione, numero dei gemelli, UC specifico, idAnsc del gemello precedente '
         'e del successivo', 'ANSC_SOGGETTO_ATTO'],
        ['Composizione libera', 'il testo dell’atto (formula 999.1.1)',
         'ANSC_SOGGETTO_ATTO.TXT_TESTO_ATTO'],
        ['Allegati', 'i documenti del Riepilogo, con SCARICA', 'MATR_USR.ALLEGATO'],
    ], [1.25, 2.85, 2.2])
    voce(d, 'Come si ricavano i valori.', 'Dalle righe di ANSC_CFG_CAMPO dell’UC 11999999, con la '
         'colonna SIPO (ALIAS_CAMPO_SIPO), già nella forma della web app: descrizioni delle '
         'decodifiche, date e ore separate.')
    voce(d, 'Comandi.', 'COPIA idAnsc, STAMPA LA SCHEDA, APRI WEB APP, CHIUDI.')

    h(d, 3, 'La web app')
    par(d, 'Fuori da SIPO l’ufficiale ritrova la bozza prenotata (per identificativo o da '
        '«Recupero evento in bozza»), la completa con i dati della scheda, incolla il testo nella '
        'composizione libera, carica i documenti se non sono già in ANSC (GE-30), acquisisce la '
        'firma su carta del dichiarante e firma come ufficiale. SIPO non vede la web app: '
        'l’esito lo accerta Recupera da ANSC.')

    h(d, 3, 'M11 · Recupera da ANSC e M12 · Aggiorna SIPO da ANSC')
    figura(d, png('gem10_s_recupera.png'), LARGO, 'Le modali «Recupera da ANSC» e «Aggiorna SIPO '
           'da ANSC»: prima si vede, poi si scrive (ipotesi)')
    par(d, 'Sono due passi distinti: il primo legge e confronta, il secondo scrive su SIPO. ANSC '
        'è la fonte: si riportano tutti i campi obbligatori in ANSC, non solo le differenze.')
    tab(d, [
        ['Azione', 'Servizi', 'Tabelle scritte', 'Esito'],
        ['Recupera da ANSC (all’apertura di M11)', 'R005 /consultazione/ansc/evento per idAnsc',
         'ANSC_STATO_ATTO (ID_STATO, STATO, TXT_EVENTO letto; COD_FASE RECUPERATO se 5); '
         'ANSC_SOGGETTO_ATTO.ID_ANSC_SOGGETTO; ANSC_LOG_AUDIT (RICONCILIAZIONE)', 'FIRMATO DA USC '
         '· DA AGGIORNARE, con le differenze; NON FIRMATO; INCOERENTE'],
        ['Controlli', '—', '—', 'stato 5; intestatario (nome, sesso) e tipologia di nascita '
         'uguali al nato in SIPO; numero comunale contenuto nell’idAnsc'],
        ['CONFERMA L’AGGIORNAMENTO (M12), passo 1', '—', 'tabelle dell’atto in MATR_USR (ATTO, '
         'ATTO_NASCITA, ATTO_NASCITA_SOGGETTO) per i campi obbligatori in ANSC, tramite '
         'ALIAS_CAMPO_SIPO; ANSC_SOGGETTO_ATTO.TXT_TESTO_ATTO = composizione di ANSC',
         'dati di SIPO allineati ad ANSC'],
        ['passo 2', '/finalizzaAtto', 'ATTO (2 DEFINITO); ATTO_SCANSIONATO; '
         'ANSC_STATO_ATTO.COD_FASE FIRMATO', 'chip verde'],
    ], [1.45, 1.45, 2.3, 1.1])
    voce(d, 'NON FIRMATO.', 'In ANSC l’atto non è ancora a 5: nessuna scrittura su SIPO, si '
         'torna alla web app e si recupera di nuovo.')
    voce(d, 'INCOERENTE.', 'Intestatario o tipologia di nascita diversi dal nato in SIPO: nessuna '
         'scrittura; l’ufficiale verifica l’atto sulla web app.')
    voce(d, 'Aggiornamento non riuscito.', 'I dati si scrivono in una transazione; se fallisce '
         'la /finalizzaAtto il chip diventa rosso e la card offre RIPROVA IL SALVATAGGIO, come '
         'nel caso 1.')
    voce(d, 'Anagrafe.', 'Per l’atto completato sulla web app la comunicazione anagrafica la '
         'genera ANSC: se la /finalizzaAtto debba ancora chiamare l’iscrizione ANPR è GE-16.')

    # ── transizioni
    h(d, 2, 'Le transizioni e i cambi di stato')
    par(d, 'Lo stato di un gemello vive in tre posti: lo stato in ANSC (ANSC_11, in '
        'ANSC_STATO_ATTO.ID_STATO e STATO), la fase dell’integrazione (COD_FASE) e lo stato della '
        'pratica in SIPO (ATTO.ID_STATO_PRATICA). La card ne mostra la sintesi.')
    figura(d, png('gem10_stati_1.pptx.png'), LARGO, 'Caso 1: gli stati della card e i pulsanti '
           'che li fanno avanzare')
    tab(d, [
        ['Da (card)', 'Evento', 'A (card)', 'ANSC_11', 'COD_FASE', 'SIPO'],
        ['—', 'divisione riuscita', 'BOZZA (prenotato)', '1 BOZZA', 'PRENOTATO',
         '1 IN LAVORAZIONE'],
        ['BOZZA (prenotato)', 'VALIDA, esito positivo o forzato', 'CONFERMATO', '2 CONFERMATO',
         'VALIDATO', '1'],
        ['CONFERMATO', 'firme acquisite (R012, R006)', 'FIRMATO DAL DICHIARANTE',
         '4 FIRMATO DAL DICHIARANTE', 'VALIDATO', '1'],
        ['CONFERMATO o FIRMATO DAL DICHIARANTE', 'TORNA AI DATI', 'BOZZA (prenotato)', '1 BOZZA '
         '(stato 0 per SIPO)', 'IN_LAVORAZIONE', '1'],
        ['FIRMATO DAL DICHIARANTE', 'FIRMA PER CONFORMITÀ (con firme su carta)',
         'FIRMATO PER CONFORMITÀ', '11 FIRMATO PER CONFORMITÀ', 'VALIDATO', '1'],
        ['FIRMATO PER CONFORMITÀ, o FIRMATO DAL DICHIARANTE senza carta', 'FIRMA L’ATTO, firma '
         'e salvataggio riusciti', 'FIRMATO DA USC · chip verde', '5 FIRMATO DA USC', 'FIRMATO',
         '2 DEFINITO'],
        ['come sopra', 'firma riuscita, salvataggio no', 'FIRMATO DA USC · chip rosso',
         '5 FIRMATO DA USC', 'FIRMATO', '1'],
        ['FIRMATO DA USC · chip rosso', 'RIPROVA IL SALVATAGGIO', 'FIRMATO DA USC · chip verde',
         '5', 'FIRMATO', '2 DEFINITO'],
        ['qualunque, prima di 5', 'CANCELLA PRATICA', 'cancellato', '9 CANCELLATO', 'ANNULLATO',
         'pratica cancellata'],
    ], [1.35, 1.35, 1.2, 0.95, 0.75, 0.7])
    figura(d, png('gem10_stati_2.pptx.png'), LARGO, 'Caso 2: gli stati della card; l’atto si '
           'forma sulla web app e torna in SIPO')
    tab(d, [
        ['Da (card)', 'Evento', 'A (card)', 'ANSC_11', 'COD_FASE', 'SIPO'],
        ['—', 'divisione riuscita', 'BOZZA · ATTESA WEBAPP', '1 BOZZA (11999999)', 'PRENOTATO',
         '1 IN LAVORAZIONE'],
        ['BOZZA · ATTESA WEBAPP', 'Recupera da ANSC, atto a 5', 'FIRMATO DA USC · DA AGGIORNARE',
         '5 FIRMATO DA USC', 'RECUPERATO', '1'],
        ['BOZZA · ATTESA WEBAPP', 'Recupera da ANSC, atto non a 5', 'NON FIRMATO', 'letto da '
         'ANSC', 'PRENOTATO', '1'],
        ['BOZZA · ATTESA WEBAPP', 'Recupera da ANSC, intestatario diverso', 'INCOERENTE',
         'letto da ANSC', 'PRENOTATO', '1'],
        ['FIRMATO DA USC · DA AGGIORNARE', 'CONFERMA L’AGGIORNAMENTO', 'FIRMATO DA USC · chip '
         'verde', '5', 'FIRMATO', '2 DEFINITO'],
        ['qualunque, prima di 5', 'CANCELLA PRATICA', 'cancellato', '9 CANCELLATO', 'ANNULLATO',
         'pratica cancellata'],
    ], [1.35, 1.35, 1.2, 0.95, 0.75, 0.7])
    par(d, 'Le transizioni fra le pagine sono poche, perché quasi tutto avviene nelle modali '
        'della stessa pagina:')
    tab(d, [
        ['Da', 'Comando o evento', 'A', 'Condizione'],
        ['Maschera dei gemelli', 'salvataggio', 'Riepilogo (P1)', 'come oggi'],
        ['Riepilogo (P1)', 'CONFERMA', 'Gemelli del parto (P2)', 'divisione riuscita; numeri e '
         'prenotazione riusciti o da recuperare (M3)'],
        ['Dettaglio o ricerca di un gemello', 'apertura dell’atto', 'Gemelli del parto (P2)',
         'atto di un parto diviso'],
        ['Gemelli del parto (P2)', 'pulsante di una card', 'modale M4…M12', 'card non FIRMATO '
         'DA USC (salvo M9)'],
        ['Modale', 'chiusura (o fine dell’azione)', 'Gemelli del parto (P2), card aggiornata',
         'nessuna chiamata in corso'],
        ['Gemelli del parto (P2)', 'CANCELLA PRATICA riuscita', 'ricerca degli atti',
         'pratica cancellata'],
        ['Gemelli del parto (P2)', 'Web app', 'web app ANSC (nuova scheda del browser)',
         'caso 2'],
    ], [1.6, 1.4, 1.75, 1.55])
    par(d, 'COD_FASE riceve due valori nuovi, PRENOTATO e RECUPERATO, e COD_PAGINA_RIPRESA i '
        'valori DATI_WEBAPP e WEBAPP; ANSC_LOG_AUDIT la fase PRENOTAZIONE (GE-14).')

    # ── errori
    h(d, 2, 'Quando qualcosa non va a buon fine')
    par(d, 'Vale la regola dell’analisi di integrazione [R1]: un esito certo si tratta, un esito '
        'incerto prima si verifica con R005 e poi si decide, mai un secondo tentativo alla '
        'cieca. Ogni errore resta sulla card del suo gemello: gli altri gemelli si lavorano.')
    tab(d, [
        ['Dove si ferma', 'Che cosa resta', 'Che cosa offre la pagina'],
        ['Divisione', 'la pratica, come oggi', 'si resta sul Riepilogo'],
        ['Stacco dei numeri', 'N atti in SIPO, nessun numero', 'avviso e RECUPERA NUMERI E '
         'PRENOTAZIONE'],
        ['Prenotazione rifiutata (codice)', 'numeri staccati, nessun atto in ANSC (righe a '
         'UC_DETERMINATO, ULTIMO_ERRORE sul gemello 1)', 'RECUPERA NUMERI E PRENOTAZIONE, con gli '
         'stessi numeri'],
        ['Prenotazione dall’esito incerto', 'non si sa se gli atti esistano', 'R005 per numero '
         'comunale; si prenota di nuovo solo se non c’è nulla (GE-13)'],
        ['Meno identificativi dei gemelli', 'alcuni gemelli senza atto', 'quelli abbinati '
         'proseguono; gli altri in errore e in supervisione'],
        ['Validazione con errori', 'atto in BOZZA', 'si correggono i dati e si valida di nuovo; se '
         'la correzione cambia l’UC, GE-20'],
        ['Firma (dichiarante, conformità, USC) con codice', 'lo stato raggiunto', 'si riprova '
         'dalla stessa modale, con un nuovo OTP se scaduto'],
        ['Firma dall’esito incerto', 'non si sa se l’atto sia avanzato', 'VERIFICA IN ANSC (M8)'],
        ['Salvataggio in SIPO', 'atto 5 in ANSC, 1 in SIPO', 'chip rosso e RIPROVA IL '
         'SALVATAGGIO (M9)'],
        ['Sessione OTP scaduta a metà', 'lo stato del passo in corso', 'nuovo codice e si ripete '
         'lo stesso passo (GE-12)'],
        ['Recupero NON FIRMATO o INCOERENTE (caso 2)', 'atto in ANSC non concluso o diverso',
         'nessuna scrittura; si torna alla web app'],
        ['Stato inatteso all’apertura (3, 9, 10 o idAnsc diverso)', 'atto toccato fuori dalla '
         'pagina', 'card bloccata; il parto compare nella supervisione [R1]'],
    ], [1.9, 2.0, 2.4])
    voce(d, 'Chi riprende.', 'Anche un ufficiale diverso, con la propria sessione OTP; la firma '
         'del dichiarante, se manca, richiede di nuovo la sua presenza (GE-22).')

    # ── trascrizioni
    h(d, 2, 'Le trascrizioni da ospedale')
    par(d, 'L’incontro del 21/11/2026 ha incluso nel perimetro le trascrizioni da ospedale di '
        'gemelli (serie 2B) [M3], che sono una parte rilevante dei parti plurimi (tipi atto 1608, '
        '1601, 1602, 1619, 1611). Per queste SIPO forza a N i due flag dello stato del nato, '
        'quindi i gemelli hanno tutti lo stesso UC e seguono il caso 1, con la stessa pagina e le '
        'stesse modali.')
    voce(d, 'Quale UC.', 'Quello specifico della trascrizione (per esempio 1314 Trascr_022 o '
         '1318 Trascr_037), che non ha varianti per il nato morto. Il caso d’uso di servizio delle '
         'trascrizioni di nascita, 1399, ancora disponibile tramite servizi cooperativi per la '
         'fase ibrida [A7], si usa solo quando non c’è una copertura più adatta [M3].')
    voce(d, 'Che cosa va verificato.', 'Che /prenota/evento accetti questi UC, e quali passi di '
         'firma richieda una trascrizione, dove non c’è un dichiarante in sala (GE-11).')

    # ── nato morto
    h(d, 2, 'Nato morto e nato vivo poi deceduto nel parto plurimo')
    voce(d, 'UC.', 'Ogni gemello ha l’UC della propria variante. Se la variante è la stessa per '
         'tutti l’UC è comune e vale il caso 1; altrimenti il caso 2.')
    voce(d, 'Allegati.', 'Il certificato medico che attesta lo stato è obbligatorio per il nato '
         'morto e per il nato vivo poi deceduto: si carica nel Riepilogo, nella scheda del '
         'nato.')
    voce(d, 'Prenotazione.', 'Il numero dei gemelli comprende i nati morti: è l’indicazione di '
         'ANSC sul campo numeroGemelliNatiVivi [A9]. Ogni nato, vivo o morto, ha il suo atto e '
         'compare negli elenchi dei fratelli.')
    voce(d, 'Morte e anagrafe.', 'Per il nato vivo e poi deceduto il documento non propone '
         'automatismi verso l’area decessi né verso ANPR finché GE-05 e GE-06 non sono chiusi.')

    # ── tabelle
    h(d, 2, 'Le tabelle')
    par(d, 'Le azioni scrivono in tabelle già descritte nell’analisi di integrazione [R1] — '
        'ANSC_STATO_ATTO, ANSC_LOG_AUDIT, firmatari, forzatura_validazione, MATR_USR.ALLEGATO, '
        'NUMERATORE_COMUNALE, PRENOTAZIONE_ATTI, DATI_ATTO_ESTERNO — e in una tabella nuova, '
        'ANSC_SOGGETTO_ATTO, che lega il nato al suo atto ANSC, raggruppa il parto e conserva il '
        'testo dell’atto.')
    h(d, 3, 'ANSC_SOGGETTO_ATTO')
    tab(d, [
        ['Colonna', 'Tipo', 'Note'],
        ['ID_SOGGETTO_ATTO', 'NUMBER (PK)', 'Chiave tecnica (IDENTITY).'],
        ['ID_ATTO_SIPO', 'NUMBER (FK)', 'L’atto di SIPO: chiave esterna verso '
         'ANSC_STATO_ATTO.ID_ATTO_SIPO.'],
        ['ID_ANSC', 'VARCHAR2(50)', 'Copia di ANSC_STATO_ATTO.ID_ANSC, scritta nella stessa '
         'transazione. Valorizzata dalla prenotazione in entrambi i casi.'],
        ['ID_UC_ANSC', 'VARCHAR2(20)', 'Copia di ANSC_STATO_ATTO.ID_UC_ANSC: l’UC comune nel caso '
         '1, 11999999 nel caso 2.'],
        ['ID_NASCITA_SOGGETTO', 'NUMBER', 'Il nato come riga di ATTO_NASCITA_SOGGETTO.ID, per '
         'valore.'],
        ['ID_SOGGETTO', 'NUMBER', 'MATR_USR.SOGGETTO.ID_SOGGETTO, per valore: per il nato si '
         'scrive dopo l’iscrizione anagrafica della definizione.'],
        ['COD_RUOLO', 'VARCHAR2(20)', 'Ruolo nell’atto ANSC: INTESTATARIO per i nati (GE-17).'],
        ['ID_ANSC_SOGGETTO', 'VARCHAR2(50)', 'Identificativo del soggetto in ANSC, quando R005 lo '
         'restituisce.'],
        ['ID_LAVORAZIONE_PADRE', 'NUMBER (FK)', 'Il parto: l’ID_ATTO del gemello 1, chiave '
         'esterna verso la sua riga dello store.'],
        ['NUM_PROGRESSIVO_GEMELLO', 'NUMBER(2)', 'Posizione = POS_GEMELLO = progressivoGemello.'],
        ['ID_TIPO_NASCITA', 'VARCHAR2(10)', 'ANSC_107 = tipoNascitaSoggetto, dai due flag di '
         'SIPO.'],
        ['ID_ANSC_GEMELLO_PREC', 'VARCHAR2(50)', 'idAnsc del gemello immediatamente precedente.'],
        ['ID_ANSC_GEMELLO_SUCC', 'VARCHAR2(50)', 'idAnsc del gemello immediatamente successivo.'],
        ['TXT_TESTO_ATTO', 'CLOB', 'Il testo dell’atto composto da SIPO; dopo l’aggiornamento '
         'del caso 2 la composizione letta da ANSC. La definizione genera il PDF da qui.'],
        ['TS_TESTO_ATTO', 'TIMESTAMP', 'Ultimo salvataggio del testo.'],
        ['COD_ORIGINE', 'VARCHAR2(20)', 'PRENOTAZIONE (parto, entrambi i casi), RECUPERO (atto '
         'formato sulla web app e recuperato fuori dal parto), VALIDAZIONE (atto ordinario).'],
        ['TS_ABBINAMENTO', 'TIMESTAMP', 'Quando nasce l’abbinamento.'],
        ['TS_INS, TS_UPD, UTENTE_INS, UTENTE_UPD', '', 'Campi tecnici [R1].'],
    ], [1.9, 1.15, 3.25])
    codice(d, [
        'CREATE TABLE ANSC_USR.ANSC_SOGGETTO_ATTO (',
        '  ID_SOGGETTO_ATTO         NUMBER GENERATED ALWAYS AS IDENTITY,',
        '  ID_ATTO_SIPO             NUMBER            NOT NULL,',
        '  ID_ANSC                  VARCHAR2(50 CHAR),',
        '  ID_UC_ANSC               VARCHAR2(20 CHAR),',
        '  ID_NASCITA_SOGGETTO      NUMBER,',
        '  ID_SOGGETTO              NUMBER,',
        '  COD_RUOLO                VARCHAR2(20 CHAR) NOT NULL,',
        '  ID_ANSC_SOGGETTO         VARCHAR2(50 CHAR),',
        '  ID_LAVORAZIONE_PADRE     NUMBER,',
        '  NUM_PROGRESSIVO_GEMELLO  NUMBER(2),',
        '  ID_TIPO_NASCITA          VARCHAR2(10 CHAR),',
        '  ID_ANSC_GEMELLO_PREC     VARCHAR2(50 CHAR),',
        '  ID_ANSC_GEMELLO_SUCC     VARCHAR2(50 CHAR),',
        '  TXT_TESTO_ATTO           CLOB,',
        '  TS_TESTO_ATTO            TIMESTAMP,',
        '  COD_ORIGINE              VARCHAR2(20 CHAR) NOT NULL,',
        '  TS_ABBINAMENTO           TIMESTAMP         NOT NULL,',
        '  TS_INS                   TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,',
        '  TS_UPD                   TIMESTAMP,',
        '  UTENTE_INS               VARCHAR2(40 CHAR) NOT NULL,',
        '  UTENTE_UPD               VARCHAR2(40 CHAR),',
        '  CONSTRAINT PK_ANSC_SOGGETTO_ATTO PRIMARY KEY (ID_SOGGETTO_ATTO),',
        '  CONSTRAINT UK_ANSC_SOGG_ATTO_RUOLO UNIQUE (ID_ATTO_SIPO, COD_RUOLO),',
        '  CONSTRAINT UK_ANSC_SOGG_ATTO_PARTO',
        '    UNIQUE (ID_LAVORAZIONE_PADRE, NUM_PROGRESSIVO_GEMELLO),',
        '  CONSTRAINT FK_ANSC_SOGG_ATTO_STATO FOREIGN KEY (ID_ATTO_SIPO)',
        '    REFERENCES ANSC_USR.ANSC_STATO_ATTO (ID_ATTO_SIPO),',
        '  CONSTRAINT FK_ANSC_SOGG_ATTO_PARTO FOREIGN KEY (ID_LAVORAZIONE_PADRE)',
        '    REFERENCES ANSC_USR.ANSC_STATO_ATTO (ID_ATTO_SIPO),',
        '  CONSTRAINT CK_ANSC_SOGG_ATTO_RIF',
        '    CHECK (ID_NASCITA_SOGGETTO IS NOT NULL OR ID_SOGGETTO IS NOT NULL),',
        '  CONSTRAINT CK_ANSC_SOGG_ATTO_ORIG',
        '    CHECK (COD_ORIGINE IN (\'PRENOTAZIONE\',\'RECUPERO\',\'VALIDAZIONE\')),',
        '  CONSTRAINT CK_ANSC_SOGG_ATTO_PROG',
        '    CHECK (NUM_PROGRESSIVO_GEMELLO BETWEEN 1 AND 10),',
        '  CONSTRAINT CK_ANSC_SOGG_ATTO_GEM',
        '    CHECK ((ID_LAVORAZIONE_PADRE IS NULL AND NUM_PROGRESSIVO_GEMELLO IS NULL',
        '            AND ID_ANSC_GEMELLO_PREC IS NULL AND ID_ANSC_GEMELLO_SUCC IS NULL)',
        '        OR (ID_LAVORAZIONE_PADRE IS NOT NULL AND NUM_PROGRESSIVO_GEMELLO IS NOT NULL))',
        ');',
        'CREATE INDEX IX_ANSC_SOGG_ATTO_NASC ON ANSC_USR.ANSC_SOGGETTO_ATTO (ID_NASCITA_SOGGETTO);',
        'CREATE INDEX IX_ANSC_SOGG_ATTO_SOGG ON ANSC_USR.ANSC_SOGGETTO_ATTO (ID_SOGGETTO);',
        'CREATE INDEX IX_ANSC_SOGG_ATTO_ANSC ON ANSC_USR.ANSC_SOGGETTO_ATTO (ID_ANSC);',
    ])
    voce(d, 'Quando nascono le righe.', 'Alla prenotazione, una per gemello, in entrambi i casi: '
         'con l’ID_NASCITA_SOGGETTO del nato che la divisione ha messo in quell’atto (GE-07).')
    voce(d, 'Le copie dallo store.', 'ID_ANSC e ID_UC_ANSC ripetono i valori di '
         'ANSC_STATO_ATTO, così che il nato, il suo atto e i suoi fratelli si leggano da una sola '
         'tabella. Le scrive solo il concentratore, nella stessa transazione in cui aggiorna lo '
         'store; l’apertura della pagina le confronta con lo store e con ANSC.')
    voce(d, 'Una sola riga per ruolo.', 'Il vincolo di unicità su atto e ruolo impedisce di '
         'abbinare due nati allo stesso atto.')
    h(d, 3, 'Le scelte di Side')
    par(d, 'Side [M1] tiene insieme i gemelli con una tabella propria, atti_gemellari, che a Roma '
        'non si crea. Dove vanno le sue colonne:')
    conserva['side']()
    h(d, 3, 'Le righe, azione per azione')
    tab(d, [
        ['Momento', 'ANSC_STATO_ATTO', 'ANSC_SOGGETTO_ATTO', 'Altre tabelle'],
        ['Dati della pratica (R005 sui genitori)', 'gemello 1: INSERT (IN_LAVORAZIONE, '
         'DETTAGLIO)', '—', '—'],
        ['Riepilogo', '—', '—', 'ALLEGATO, firmatari (GE-27)'],
        ['Divisione', '—', '—', 'MATR_USR.ATTO (N atti)'],
        ['UC e numeri', 'gemello 1 UPDATE, 2…N INSERT; ID_UC_ANSC, NUMERO_ATTO, UC_DETERMINATO',
         '—', 'NUMERATORE_COMUNALE, PRENOTAZIONE_ATTI, DATI_ATTO_ESTERNO'],
        ['Prenotazione', 'tutte: ID_ANSC, 1 BOZZA, PRENOTATO, TXT_EVENTO', 'INSERT di N righe, '
         'con parto, posizione, tipologia e gemelli adiacenti', 'ANSC_LOG_AUDIT (PRENOTAZIONE); '
         'DATI_ATTO_ESTERNO (2 Utilizzato)'],
        ['Composizione del testo; SALVA TESTO', '—', 'TXT_TESTO_ATTO, TS_TESTO_ATTO', '—'],
        ['Validazione (caso 1)', 'riga k: 2 CONFERMATO, VALIDATO, TS_VALIDAZIONE, TXT_EVENTO',
         'riallineamento se cambia l’idAnsc', 'ALLEGATO; forzatura_validazione; audit'],
        ['Firme del dichiarante, conformità (caso 1)', 'riga k: 4, poi 11', '—', 'firmatari; '
         'ALLEGATO; audit'],
        ['Firma USC e salvataggio (caso 1)', 'riga k: 5, FIRMATO', 'ID_SOGGETTO', 'ATTO, '
         'ATTO_SCANSIONATO; audit'],
        ['Recupero (caso 2)', 'riga k: stato letto, RECUPERATO, TXT_EVENTO letto',
         'ID_ANSC_SOGGETTO', 'audit (RICONCILIAZIONE)'],
        ['Aggiornamento (caso 2)', 'riga k: FIRMATO', 'TXT_TESTO_ATTO = composizione ANSC; '
         'ID_SOGGETTO', 'tabelle dell’atto in MATR_USR; ATTO_SCANSIONATO'],
        ['Apertura della pagina', 'stato letto con R005', 'confronto di ID_ANSC e ID_UC_ANSC',
         'audit (RICONCILIAZIONE)'],
        ['CANCELLA PRATICA', 'tutte: 9 CANCELLATO, ANNULLATO', 'invariate, come storico',
         'DATI_ATTO_ESTERNO (3 Scartato); ATTO'],
    ], [1.5, 1.75, 1.5, 1.55])
    h(d, 3, 'I legami')
    figura(d, png('gem10_erd.pptx.png'), LARGO, 'Le righe di ANSC_STATO_ATTO nel parto plurimo e '
           'i loro legami, con ANSC_SOGGETTO_ATTO')
    conserva['legami']()
    par(d, 'Tutti i gemelli di un parto si ritrovano con una sola interrogazione, partendo da '
        'qualunque di essi; è quella che la pagina esegue all’apertura:')
    conserva['query']()
    h(d, 3, 'Gli elenchi dei fratelli')
    par(d, 'attiGemelliPrec e attiGemelliSucc del gemello k si ricavano da ANSC_SOGGETTO_ATTO '
        'seguendo la catena: i primi risalendo con ID_ANSC_GEMELLO_PREC fino al gemello 1, i '
        'secondi scendendo con ID_ANSC_GEMELLO_SUCC fino all’ultimo; l’interrogazione del parto '
        'dà lo stesso risultato e serve da controllo. numeroGemelli è il numero delle righe del '
        'parto, progressivoGemello è NUM_PROGRESSIVO_GEMELLO, tipoNascitaSoggetto è '
        'ID_TIPO_NASCITA, partoGemellare vale SI. Gli stessi dati entrano nel testo dell’atto in '
        'entrambi i casi e, nel caso 1, nel modello evento a ogni validazione.')

    # ── interventi
    h(d, 2, 'Gli interventi da realizzare')
    tab(d, [
        ['Componente', 'Intervento'],
        ['Riepilogo della pratica (front-end e back-end delle nascite)', 'Scheda per nato con '
         'documenti e firmatari; conferma che avvia divisione, numeri e prenotazione.'],
        ['Pagina «Gemelli del parto» (statocivile-web) e modali M1…M13', 'Nuova; raggiungibile '
         'anche dal dettaglio e dalla ricerca di un gemello.'],
        ['/performAttiPlurigemellari (statocivile-be)', 'Dopo la divisione chiama il '
         'concentratore per numeri e prenotazione; dopo la prenotazione l’annullamento della '
         'divisione non si offre più.'],
        ['all-ansc-sipo', 'Operazioni nuove da aggiungere al contratto ansc-v1.yaml: prenotazione '
         'del parto (numeri, R009 /prenota/evento, store e ANSC_SOGGETTO_ATTO in una sola '
         'azione), lettura del parto, salvataggio del testo, firme R012/R006/R007 per atto, '
         'recupero e aggiornamento da ANSC (caso 2), cancellazione del parto.'],
        ['be-numeratore-comunale', 'Uso di POST /richiesta per N numeri, PUT /utilizza e PUT '
         '/scarta [R3]; l’idAnsc sul numero è un punto aperto dell’analisi di integrazione.'],
        ['PKG_FORMULARI', 'Il testo dei gemelli deve leggere numero comunale e idAnsc dei '
         'fratelli dalle tabelle dell’integrazione (GE-26).'],
        ['/finalizzaAtto', 'Per un solo gemello alla volta; PDF da TXT_TESTO_ATTO invece che dal '
         'formulario; nel caso 2 dopo l’aggiornamento da ANSC (GE-16).'],
        ['/cancellaAnnullaAtto', 'Per un parto diviso e prenotato: R011 sulle bozze e scarto dei '
         'numeri prima della procedura di SIPO (GE-09).'],
        ['ANSC_USR', 'Tabella ANSC_SOGGETTO_ATTO; valori PRENOTATO e RECUPERATO di COD_FASE, '
         'DATI_WEBAPP e WEBAPP di COD_PAGINA_RIPRESA; fase PRENOTAZIONE di ANSC_LOG_AUDIT '
         '(GE-14).'],
    ], [2.2, 4.1])


def main():
    d = docx.Document(IN)
    fatti = []
    body = d.element.body

    # ── 1. elementi del vecchio capitolo da conservare
    def paragrafo_con_box(testo):
        for p in d.paragraphs:
            if any(testo in ''.join(t.text or '' for t in tb.iter(qn('w:t')))
                   for tb in p._p.iter(qn('w:txbxContent'))):
                return p._p
        raise SystemExit('box non trovato: ' + testo)
    attne = paragrafo_con_box('E’ necessario modificare il package')
    side = tabella_con(d, 'Scelta di Side', 'Per Roma')
    legami = tabella_con(d, 'Legame', 'Da', 'A', 'Come', 'Cardinalità')
    q0 = para_che_inizia(d, 'SELECT g.NUM_PROGRESSIVO_GEMELLO')
    query, e = [], q0._p
    while True:
        query.append(e)
        if Paragraph(e, d).text.strip().startswith('ORDER BY'):
            break
        e = e.getnext()
    cambia_cella(riga_di(side, '—').cells[2], ' Raggruppa i gemelli anche quando la '
                 'prenotazione non passa da SIPO (caso 2).', '')
    cambia_cella(riga_di(legami, 'Fratelli in ANSC').cells[3], 'scritti alla prenotazione '
                 '(caso 1) o al recupero (caso 2).', 'scritti alla prenotazione, in entrambi i '
                 'casi.')
    conservati = [attne, side._tbl, legami._tbl] + query

    # ── 2. via il vecchio corpo del capitolo
    cap = D.h(d, 1, 'La modalità di integrazione', esatto=True)._p
    fine = D.h(d, 1, 'Punti aperti', esatto=True)._p
    via, e = [], cap.getnext()
    while e is not fine:
        via.append(e)
        e = e.getnext()
    for x in conservati:
        assert any(x is v for v in via), 'elemento conservato fuori dal capitolo'
    for x in via:
        if any(x is c for c in conservati):
            x.getparent().remove(x)
            continue
        assert not D.ha_commenti(x)
        x.getparent().remove(x)
    fatti.append('capitolo 7: tolti %d elementi, conservati %d' % (len(via) - len(conservati),
                                                                    len(conservati)))

    # ── 3. il capitolo nuovo
    def inserisci(*elementi):
        def f():
            for x in elementi:                      # in coda al corpo, prima di sectPr
                body.find(qn('w:sectPr')).addprevious(x)
        return f

    def side_f():
        inserisci(side._tbl)()
        d.add_paragraph()

    def legami_f():
        inserisci(legami._tbl)()
        d.add_paragraph()
    conserva = {'attne': inserisci(attne), 'side': side_f, 'legami': legami_f,
                'query': lambda: (inserisci(*query)(), d.add_paragraph())}
    racc = in_coda(d)
    capitolo(d, conserva)
    nuovi = racc()
    sposta_prima(nuovi, fine)
    fatti.append('capitolo 7: %d elementi nuovi' % len(nuovi))

    # ── 4. Scopo e perimetro
    D.sostituisci(d, 'Il perimetro sono le dichiarazioni di nascita con più nati. Il nato '
                  'singolo vi compare solo come termine di confronto. Le trascrizioni da ospedale '
                  'sono richiamate dove i dati lo richiedono, ma la loro corrispondenza con gli '
                  'UC di ANSC resta un punto aperto (GE-11).',
                  'Il perimetro sono le dichiarazioni di nascita con più nati e le trascrizioni '
                  'da ospedale di gemelli, incluse dall’incontro del 21/11/2026 [M3]. Il nato '
                  'singolo vi compare solo come termine di confronto. Il capitolo «La modalità di '
                  'integrazione» è scritto come manuale per lo sviluppo: le pagine da costruire, '
                  'le tabelle che ogni azione legge e scrive, le transizioni fra le pagine e i '
                  'cambi di stato.', attese=1, fatti=fatti)

    # ── 5. Riferimenti
    rif = D.trova_tabella(d, 'riferimento', 'natura')
    m2 = riga_di(rif, '[M2]')._tr
    for valori in (
            ('[P1]', 'PROPOSTA_Pagina-Gemelli_SIPO-ANSC_v0.4.pptx e '
             'DIMOSTRATORE_Pagina-Gemelli_SIPO-ANSC_v0.1.html — la pagina «Gemelli del parto», '
             'le card e le modali: mockup accettati e dimostratore funzionante su dati fittizi.',
             'Documento di progetto'),
            ('[M3]', 'Appunti dell’incontro del 21/11/2026 (mail di C. Sacco): trascrizioni da '
             'ospedale nel perimetro, conteggi dei tipi atto gemellari, uso del caso d’uso di '
             'servizio 1399 solo senza copertura migliore.', 'Comunicazione del Comune')):
        r = D.clona_riga(rif, valori)
        m2.addnext(r._tr)
        m2 = r._tr

    # ── 6. In sintesi
    nuove = [
        ('Due casi, decisi dallo stato dei nati.', 'Due casi, decisi dallo stato dei nati.',
         'La prenotazione accetta un solo caso d’uso e le bozze si completano con quello. Se '
         'tutti i gemelli hanno lo stesso UC si prenota con l’UC specifico e ciascuna bozza si '
         'completa da SIPO con i servizi cooperativi: è il caso 1 [A9]. Se gli UC sono diversi si '
         'prenota con il caso d’uso di servizio 11999999, con la tipologia di nascita nei dati '
         'generali [A10]: la prenotazione tramite servizi cooperativi l’ha verificata il Comune, '
         'il completamento avviene solo sulla web app [A7]. È il caso 2.'),
        ('Il caso 1 in SIPO.', 'Una sola pagina dopo la divisione.', 'Nel Riepilogo si '
         'raccolgono documenti e firmatari di ciascun atto; la conferma divide la pratica, '
         'stacca i numeri comunali e prenota gli atti. Si apre poi la pagina «Gemelli del '
         'parto»: una testata, una card per gemello con i passi come pulsanti che aprono una '
         'modale, il testo dell’atto del gemello selezionato. I gemelli si lavorano in qualsiasi '
         'ordine; aprire la pagina è già riprendere un parto interrotto.'),
        ('Il caso 2 svolto completamente in WebApp', 'Due conclusioni opposte.', 'Nel caso 1 la '
         'firma dell’ufficiale conclude il gemello e SIPO lo definisce da sé: i dati vanno da '
         'SIPO ad ANSC. Nel caso 2 l’atto si completa e si firma sulla web app con i dati e il '
         'testo preparati da SIPO; poi RECUPERA DA ANSC e AGGIORNA SIPO DA ANSC riportano in '
         'SIPO i campi obbligatori in ANSC: i dati vanno da ANSC a SIPO.'),
        ('Il raccordo dei numeri.', 'Il testo dell’atto.', 'Lo compone SIPO con gli '
         'identificativi nazionali dei fratelli, noti in entrambi i casi dalla prenotazione, e lo '
         'conserva in ANSC_SOGGETTO_ATTO: nel caso 1 viaggia con la validazione, nel caso 2 si '
         'copia nella composizione libera della bozza.'),
        ('Il soggetto e il suo atto ANSC.', 'Il soggetto e il suo atto ANSC.', 'Una tabella '
         'nuova, ANSC_SOGGETTO_ATTO, registra per ciascun nato l’atto ANSC che lo ha per '
         'intestatario, con l’identificativo nazionale, l’UC, il testo dell’atto e, per i '
         'gemelli, posizione, tipo di nascita e identificativi dei gemelli adiacenti. Le righe '
         'nascono alla prenotazione, in entrambi i casi. Vale anche fuori dal parto plurimo.'),
    ]
    for inizio, testa, corpo in nuove:
        rifai_voce(d, para_che_inizia(d, inizio), testa, corpo)
    D.sostituisci(d, 'le altre si inseriscono alla prenotazione nel caso 1, allo stacco dei '
                  'numeri nel caso 2.', 'le altre si inseriscono alla divisione, con i numeri '
                  'e la prenotazione, in entrambi i casi.', attese=1, fatti=fatti)
    D.sostituisci(d, 'una riga per per ogni atto', 'una riga per ogni atto', attese=1,
                  fatti=fatti)

    # ── 7. SIPO oggi: i conteggi dell'incontro
    t = tabella_con(d, 'Tipo atto', 'Modello', 'Descrizione', 'Atti nella ricognizione')
    col = t.add_column(Inches(1.0))
    valori = {'Tipo atto': 'Incontro del 21/11 [M3]', '1429': '302', '1608': '179',
              '1601': '166', '1449': '125', '1437': '52', '1438': '60', '1602': '36',
              'Altri 138': '1619: 16 · 1611: 14', 'Totale': '950 sui nove tipi più usati'}
    for r in t.rows:
        k = r.cells[0].text.strip()
        c = r.cells[-1]
        c.text = ''
        run = c.paragraphs[0].add_run(valori[k])
        run.font.size = Pt(9)
        run.bold = k == 'Tipo atto'
    racc = in_coda(d)
    par(d, 'Gli appunti dell’incontro del 21/11/2026 [M3] riportano per gli stessi tipi '
        'conteggi più alti: 950 atti sui nove tipi più usati, contro i 774 dell’intera '
        'ricognizione [M2]. Le due fonti non coincidono, probabilmente per il periodo '
        'considerato [DA VERIFICARE]; entrambe mostrano il peso delle trascrizioni da ospedale '
        '(1608, 1601, 1602, 1619, 1611), che il documento comprende nel perimetro.')
    sposta_prima(racc(), t._tbl.getnext().getnext())

    # ── 8. ANSC: la prenotazione con 11999999
    t = tabella_con(d, 'Elemento', 'Contenuto', 'Osservazioni')
    c = riga_di(t, 'Richiesta: idUsecase').cells[2]
    D.riscrivi_cella(c, c.text + ' Il Comune ha verificato che tramite servizi cooperativi si '
                     'prenota anche con il caso d’uso di servizio 11999999: è la prenotazione '
                     'del caso 2 (GE-31).')
    t = tabella_con(d, 'Caso', 'Quando', 'Che cosa dice ANSC', 'Canale')
    D.riscrivi_cella(t.rows[2].cells[3], 'Prenotazione tramite servizi cooperativi con 11999999, '
                     'verificata dal Comune (GE-31); completamento, firme e validazione solo '
                     'sulla web app, perché il caso d’uso di servizio non si completa tramite '
                     'servizi cooperativi dal 9 settembre 2024 [A7].')
    t = tabella_con(d, '#', 'Passo del percorso ANSC')
    D.riscrivi_cella(riga_di(t, '1').cells[3], 'R009 /prenota/evento tramite servizi '
                     'cooperativi, con il caso d’uso di servizio 11999999 (verificato dal '
                     'Comune).')

    # ── 9. SIPO e ANSC a confronto
    t = tabella_con(d, 'Aspetto', 'SIPO oggi', 'ANSC', 'Conseguenza per l’integrazione')
    for primo, testo in (
            ('Numerazione', 'Stacco in blocco da be-numeratore-comunale alla divisione, prima '
             'della prenotazione, in entrambi i casi.'),
            ('Stato del singolo nato', 'Se gli UC dei nati coincidono si prenota con quell’UC e '
             'si completa da SIPO (caso 1); se differiscono si prenota con 11999999 e si completa '
             'sulla web app (caso 2).'),
            ('Testo dell’atto', 'Il testo si compone dopo la prenotazione, con gli idAnsc dei '
             'fratelli, e si conserva in ANSC_SOGGETTO_ATTO.'),
            ('Firma del dichiarante', 'Caso 1: su carta (R006) o elettronica (R012), da '
             'verificare (GE-28); caso 2: su carta, sulla web app.'),
            ('Definizione', 'Ciascun gemello si conclude da solo: nel caso 1 alla firma '
             'dell’ufficiale, nel caso 2 all’aggiornamento da ANSC.')):
        D.riscrivi_cella(riga_di(t, primo).cells[3], testo)

    # ── 10. Punti aperti
    op = D.trova_tabella(d, 'tema', 'questione')
    agg = {
        'GE-04': ('I gemelli con UC diversi si prenotano tramite servizi cooperativi con il caso '
                  'd’uso di servizio 11999999 e si completano sulla web app, con la tipologia di '
                  'nascita nei dati generali [A10]: è il caso 2. Resta aperta la richiesta di una '
                  'procedura interamente cooperativa [A11].', 'Risolto in parte'),
        'GE-09': ('Dopo la prenotazione gli atti esistono in ANSC: il pulsante «indietro» non '
                  'annulla più la divisione. CANCELLA PRATICA, ammessa solo se nessun gemello è '
                  'FIRMATO DA USC, cancella le bozze (R011), scarta i numeri e cancella la '
                  'pratica. Va verificato che /cancellaAnnullaAtto (ANNULLAMENTOPRATICA) tratti '
                  'gli N atti di una pratica divisa.', 'Risolto in parte'),
        'GE-11': ('Le trascrizioni da ospedale di gemelli sono nel perimetro [M3] e seguono il '
                  'caso 1. Si usa l’UC specifico (1314 Trascr_022, 1318 Trascr_037), senza '
                  'varianti per il nato morto; il caso d’uso di servizio 1399 solo senza '
                  'copertura migliore. Da verificare: che /prenota/evento accetti questi UC e '
                  'quali firme richieda una trascrizione.', 'Aperto'),
        'GE-15': ('Superato: anche nel caso 2 prenota SIPO con i propri numeri; sulla web app '
                  'l’ufficiale completa bozze già numerate.', 'Chiuso'),
        'GE-16': ('Per un atto completato sulla web app la comunicazione anagrafica la genera '
                  'ANSC. Va deciso se la /finalizzaAtto lanciata da AGGIORNA SIPO DA ANSC chiami '
                  'ancora l’iscrizione ANPR di SIPO.', 'Aperto'),
        'GE-18': ('Va verificato in preproduzione che R005 per idAnsc restituisca, per le bozze '
                  'prenotate con 11999999 e completate sulla web app, stato, intestatario, '
                  'tipologia di nascita, composizione e campi obbligatori da riportare in SIPO.',
                  'Aperto'),
        'GE-19': ('Superato: non c’è più un riepilogo con i numeri previsti; i numeri si '
                  'staccano alla divisione.', 'Chiuso'),
        'GE-20': ('Se dopo la prenotazione la correzione di un errore di validazione cambia lo '
                  'stato di un nato, la sua bozza ha un UC che non è più il suo: va stabilito se '
                  'cancellarla (R011) e passare il parto al caso 2.', 'Aperto'),
        'GE-22': ('La ripresa, cioè l’apertura della pagina, può farla un ufficiale diverso con '
                  'la propria sessione OTP; la firma del dichiarante, se manca, richiede di nuovo '
                  'la sua presenza. Va deciso se un parto possa restare aperto oltre la giornata.',
                  'Aperto'),
        'GE-25': ('Nel caso 2 il testo in ANSC può differire da quello copiato da SIPO. AGGIORNA '
                  'SIPO DA ANSC sostituisce TXT_TESTO_ATTO con la composizione letta da R005 e la '
                  'definizione genera il PDF da quella: va verificato che R005 la restituisca '
                  'completa.', 'Aperto'),
        'GE-26': ('Il testo del gemello contiene il numero comunale e gli identificativi '
                  'nazionali dei fratelli, che dopo la prenotazione stanno in ANSC_STATO_ATTO e '
                  'ANSC_SOGGETTO_ATTO: il formulario (PKG_FORMULARI) va esteso per leggerli.',
                  'Aperto'),
    }
    for k, (q, s) in agg.items():
        r = riga_di(op, k)
        D.riscrivi_cella(r.cells[2], q)
        D.riscrivi_cella(r.cells[3], s)
    c = riga_di(op, 'GE-14').cells[2]
    D.riscrivi_cella(c, c.text.rstrip('. ') + '; i valori RECUPERATO di COD_FASE e DATI_WEBAPP, '
                     'WEBAPP di COD_PAGINA_RIPRESA.')
    for riga in (
            ('GE-27', 'Documenti e firmatari prima della divisione', 'Il Riepilogo li raccoglie '
             'atto per atto prima che la divisione crei gli atti 2…N, mentre MATR_USR.ALLEGATO e '
             'firmatari sono chiavi sull’atto. Proposta: registrarli sull’atto della pratica con '
             'il riferimento al nato (ATTO_NASCITA_SOGGETTO.ID) e spostarli sull’atto del nato '
             'alla divisione; serve una colonna o una tabella di appoggio.', 'Aperto'),
            ('GE-28', 'Firma dei dichiaranti', 'La guida esclude la firma elettronica per i parti '
             'gemellari [A3], la pagina la prevede nel caso 1 (R012). Da verificare: se R012 è '
             'ammessa sulle bozze prenotate da gestionale; se lo stesso atto ammette una firma '
             'elettronica e una su carta; come ANSC porta a FIRMATO DAL DICHIARANTE un atto senza '
             'dichiaranti.', 'Aperto'),
            ('GE-29', 'Motivo di recupero nel caso 2', 'Il mapping di 11999999 rende obbligatorio '
             'motivoRecupero (ANSC_96): va chiesto ad ANSC quale valore indicare per i gemelli con '
             'UC diversi prenotati da gestionale.', 'Aperto'),
            ('GE-30', 'Documenti sulla bozza del caso 2', 'Va provato se R001 carica i documenti '
             'sulla bozza prenotata con 11999999; altrimenti l’ufficiale li scarica dalla modale '
             '«Dati per la web app» e li carica sulla web app.', 'Aperto'),
            ('GE-31', 'Prenotazione con 11999999', 'Il Comune ha verificato che /prenota/evento '
             'accetta il caso d’uso di servizio tramite servizi cooperativi. Vanno documentati '
             'ambiente, data e risposta della prova e verificato che la web app ritrovi le bozze '
             'e ne consenta il completamento.', 'Risolto in parte')):
        D.clona_riga(op, riga)

    # ── 11. figure rinumerate, frontespizio, storia
    n = 0
    for p in d.paragraphs:
        m = re.match(r'Figura \d+ – ', p.text)
        if m:
            n += 1
            D.testo_di(p, 'Figura %d – ' % n + p.text[m.end():])
    for fatto in D.frontespizio(d, '1.0', NOME, DATA):
        fatti.append(fatto)
    D.storia(d, DATA, '1.0', 'Scopo e perimetro · Riferimenti · In sintesi · SIPO oggi · ANSC · '
             'SIPO e ANSC a confronto · La modalità di integrazione · Punti aperti',
             'Il capitolo della modalità di integrazione riscritto come manuale per lo sviluppo, '
             'sulla proposta accettata della pagina «Gemelli del parto»: pagine e modali da '
             'costruire, azioni con servizi e tabelle, transizioni e cambi di stato nei due '
             'casi. Numeri e prenotazione alla divisione in entrambi i casi (caso 2 con '
             '11999999); testo dell’atto in ANSC_SOGGETTO_ATTO.TXT_TESTO_ATTO. Trascrizioni da '
             'ospedale nel perimetro. Nuovi riferimenti P1 e M3; GE-27…GE-31.')
    d.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE), '| figure numerate:', n)
    for f in fatti:
        print('  ' + f)
    print('capitoli %d | tabelle %d | figure %d' % D.riepilogo(OUT))


if __name__ == '__main__':
    main()
