# -*- coding: utf-8 -*-
"""DISEGNO_Back-Office_ANSC v0.5 → v0.6 (02/10/2026).

Riporta nel documento giusto il lavoro svolto oggi, che era finito per errore nella sola
analisi del front-end. Quattro cose appartengono a questo documento e non a quella:

  1. ⚠️ **Le diciassette figure della v0.5 sono vecchie.** I wireframe sono stati
     rigenerati oggi con il piè di pagina di «Footer cdr.jpeg» — due colonne invece di
     tre, sette canali, niente colonna MENU — ma la sostituzione è avvenuta solo nella
     cartella delle immagini. Qui si riscrive il blob di ciascuna figura.
  2. Il capitolo «Che cosa deve contenere il piè di pagina» descrive ancora tre colonne.
  3. La pagina «Postazioni e certificati», che chiude BO-6: le schermate reali esistono
     («screen-app-certificati.docx»), la funzione è già realizzata in versione autonoma.
  4. La deroga del menu da ConfigMap, che appartiene al registro delle pagine.

⚠️ Il documento porta SEI commenti di Word: si contano prima e dopo e non si usa mai
`riscrivi_tabella`. ⚠️ La v0.5 risulta aperta in Word (file ~$): si scrive su un nome
nuovo, mai sulla v0.5.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/bo_v0_6.py
"""
import os
import shutil
import subprocess
import sys

import docx
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIN = os.path.join(BASE, 'Documenti finali')
SRC = os.path.join(FIN, 'DISEGNO_Back-Office_ANSC_v0.5.docx')
DST = os.path.join(FIN, 'DISEGNO_Back-Office_ANSC_v0.6.docx')
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')

# Figura → PNG rigenerato. ⚠️ La Figura 1 è già allineata; le altre diciassette no.
FIGURE = {
    1: 'bo_mfe.png', 2: 'bo_chrome.png', 3: 'bo_home.png', 4: 'bo_atti.png',
    5: 'bo_atto.png', 6: 'bo_allegati.png', 7: 'bo_notifiche.png',
    8: 'bo_uc_elenco.png', 9: 'bo_uc_dettaglio.png', 10: 'bo_catalogo_uc.png',
    11: 'bo_logiche.png', 12: 'bo_dizionari.png', 13: 'bo_riconciliazione.png',
    14: 'bo_riconciliazione_dettaglio.png', 15: 'bo_versioni.png',
    16: 'bo_comandi.png', 17: 'bo_numerazione.png', 18: 'bo_amministrazione.png',
}

PIEDE = [
    ['Elemento', 'Che cosa contiene', 'Perché serve'],
    ['Marchio e stemma', 'Il logotipo ROMA con lo stemma, in negativo sul fondo scuro.',
     'Chiude la pagina con la stessa identità con cui la testata l’apre.'],
    ['Colonna «Contatti»',
     'Piazza del Campidoglio 1 — 00186 (RM), partita IVA e codice fiscale dell’ente; '
     'Ufficio Responsabile Protezione Dati, Direzione Ufficio Stampa e Media, Chiama '
     'Roma 060606, «Tutti i contatti».',
     'Obbligo istituzionale e punto di contatto. ⚠️ Il recapito per il malfunzionamento '
     'di un applicativo interno non è fra questi: «Chiama Roma 060606» è il numero del '
     'cittadino, non il supporto applicativo dell’operatore.'],
    ['Colonna «Seguici su»',
     'Sette canali — Facebook, X, LinkedIn, Instagram, YouTube, WhatsApp, TikTok — e il '
     'rimando a INFORoMA.',
     'Fa parte dell’identità istituzionale. ⚠️ Per un applicativo interno non ha alcun '
     'uso: resta perché il piè di pagina è dell’ente e non dell’applicazione.'],
    ['Fascia inferiore', 'Privacy e Cookie Policy.',
     '⚠️ Mancano la dichiarazione di accessibilità e le note legali, che la versione '
     'precedente di questo documento dava per presenti. Non è un rilievo sul nostro '
     'disegno — il piè di pagina è della shell — ma va segnalato a chi governa il design '
     'system (BO-20).'],
    ['Versione e build (raccomandati)',
     'Non presenti.',
     '⚠️ Resta la raccomandazione già formulata: durante un aggiornamento progressivo '
     'due operatori possono vedere versioni diverse della stessa pagina, e senza '
     'l’indicazione della build una segnalazione non è riconducibile a un artefatto. '
     'Il committente non intende modificare l’interfaccia: resta BO-16.'],
]

CONFIGMAP = [
    ['Aspetto', 'Menu da ConfigMap (primo rilascio)', 'Menu dalle quattro tabelle (bersaglio)'],
    ['Chi lo cambia', 'Chi ha accesso al cluster: sistemisti o rilascio.',
     'Il funzionario abilitato, dalla pagina «Pagine e menu».'],
    ['Quando ha effetto',
     'Al riavvio dei pod, oppure al successivo ricaricamento se il file è montato e '
     'riletto.',
     'Al successivo caricamento del menu, senza toccare i pod.'],
    ['Tracciabilità della modifica',
     '⚠️ Nessuna dentro l’applicazione: resta nella storia del repository di '
     'configurazione, se c’è.',
     'Utente e momento su ogni riga, come per il resto della configurazione.'],
    ['Abilitazioni per voce',
     'Dichiarate nel file, senza vincolo di integrità verso il vocabolario reale.',
     'In tabella, con il vincolo verso l’elenco delle abilitazioni esistenti '
     '(ANSC_CFG_PAGINA_ABILITAZ).'],
    ['Differenze fra ambienti',
     '⚠️ Un file per ambiente: il menu di collaudo e quello di esercizio divergono senza '
     'che nulla lo segnali.',
     'Un solo modello, con i dati propri di ciascun ambiente.'],
    ['Reversibilità della granularità',
     'Conservata: anche il file disaccoppia il menu dall’impacchettamento.',
     'Conservata, con in più il governo da interfaccia.'],
    ['Costo di realizzazione', 'Pressoché nullo: è un file.',
     'Quattro tabelle, un servizio di lettura e la pagina «Pagine e menu».'],
]

CERT_TABELLE = [
    ['Tabella', 'Uso', 'Che cosa se ne mostra'],
    ['Registro delle postazioni di SIPO',
     'Lettura ed eliminazione dell’elenco; inserimento al caricamento.',
     '⚠️ Il nome della tabella non è dichiarato in questo documento: la funzione esiste '
     'già in SIPO come servizio, alimentato da un programma a riga di comando, e il '
     'registro è suo. Prima di realizzare va accertato quale tabella sia e se le colonne '
     'proposte qui sotto esistano (BO-18).'],
    ['Nome del certificato',
     'Chiave visibile della riga, nella forma «sede-PC-numero» (058091-PC-2611).',
     'Colonna «Certificato». ⚠️ Coincide con il nome comune del certificato, che la nota '
     'tecnica di ANSC usa come identificativo della postazione: non è un’etichetta '
     'libera e non va reso modificabile.'],
    ['Sede',
     'Il codice ISTAT del comune (058091 = Roma).',
     'Colonna «Sede». Alla scala di Roma il valore è costante: la colonna ha senso '
     'perché il registro è pensato per più sedi, non perché distingua.'],
    ['Contenitore PKCS#12',
     'Il file caricato, con la chiave privata della postazione.',
     'Non si mostra mai. ⚠️ Dove risieda — base dati, volume cifrato o gestore di '
     'segreti del cluster — è una decisione aperta: è materiale di chiave privata, non '
     'un allegato.'],
]

CERT_CAMPI = [
    ['Elemento', 'Genere', 'Comportamento'],
    ['Nome Certificato', 'Filtro',
     'Ricerca per nome, con i bottoni CERCA e ANNULLA accanto. ANNULLA azzera il filtro '
     'e ricarica l’elenco intero.'],
    ['CARICA CERTIFICATO', 'Azione di pagina',
     'Non apre una pagina né una finestra: **sostituisce la riga di ricerca** con quella '
     'di inserimento, lasciando l’elenco visibile sotto. È una scelta economica e '
     'coerente con l’uso, perché chi carica un certificato ha quasi sempre bisogno di '
     'vedere che cosa c’è già.'],
    ['Nome Certificato (inserimento)', 'Campo',
     'Il nome con cui il certificato entra nel registro. ⚠️ Nelle schermate è libero: '
     'converrebbe ricavarlo dal nome comune del certificato caricato, invece di '
     'chiederlo, perché una divergenza fra i due rende il registro inservibile.'],
    ['Password', 'Campo',
     '⚠️ La parola d’ordine del contenitore PKCS#12. Nelle schermate fornite **è '
     'mostrata in chiaro** mentre la si digita (il valore «E3704AD0» è leggibile nella '
     'schermata di flusso). Va mascherata come qualunque credenziale e non va conservata '
     'dopo il caricamento: serve soltanto ad aprire il file nel momento in cui lo si '
     'riceve.'],
    ['SELEZIONA CERTIFICATO', 'Azione',
     'Sceglie il file. Accanto compare il nome scelto («058091-PC-2611.p12») oppure '
     '«Nessun file selezionato». Il formato ammesso è il solo PKCS#12.'],
    ['SALVA / ANNULLA', 'Azioni',
     'SALVA carica il certificato e riporta la pagina in modo ricerca; l’esito è una '
     'notifica in alto a destra, non un cambio di pagina. ANNULLA abbandona e ripristina '
     'la riga di ricerca.'],
    ['Caricato il / Caricato da', 'Colonne proposte',
     '⚠️ **Non sono nelle schermate fornite.** Un registro di certificati senza la data '
     'di caricamento e senza chi lo ha fatto non consente di ricostruire nulla quando '
     'una postazione smette di funzionare.'],
    ['Stato', 'Colonna proposta',
     '⚠️ **Non è nelle schermate fornite.** La data di scadenza non va chiesta '
     'all’operatore: sta dentro il certificato e si legge all’atto del caricamento. '
     'Senza di essa nessuno si accorge di una scadenza finché le chiamate verso l’ente '
     'esterno non cominciano a fallire — ed è il modo peggiore di accorgersene, perché '
     'accade allo sportello.'],
    ['Occhio', 'Azione di riga',
     'Apre il dettaglio del certificato: nome comune, emittente, validità, impronta. '
     'Sola lettura.'],
    ['Cestino', 'Azione di riga',
     'Elimina il certificato. Chiede conferma in una finestra che **nomina il '
     'certificato** — «Sei sicuro di voler eliminare il certificato 058091-PC-2611?» — e '
     'non un generico «sei sicuro?». ⚠️ Eliminare il certificato di una postazione la '
     'rende incapace di dialogare con ANPR e con ANSC: l’azione va subordinata a '
     'un’abilitazione propria, distinta da quella di accesso alla pagina.'],
]

NUOVI_BO = [
    ('BO-18', 'Su quale tabella poggi il registro delle postazioni, e dove risieda il '
              'contenitore PKCS#12',
     'La funzione esiste già in SIPO come servizio, alimentata da un programma a riga di '
     'comando: il registro è suo e questo documento non lo ridisegna. Prima di realizzare '
     'l’interfaccia va accertato quale tabella sia, quali colonne abbia e dove stia il '
     'materiale di chiave privata, che non è un allegato.'),
    ('BO-19', 'Se il registro dei certificati debba esporre data di caricamento, '
              'operatore e scadenza',
     'Le schermate fornite mostrano solo nome e sede. ⚠️ Senza la scadenza nessuno si '
     'accorge che un certificato sta per scadere; senza data e operatore non si ricostruisce '
     'chi ha messo che cosa. La scadenza non va chiesta: si legge dal certificato.'),
    ('BO-20', 'Dichiarazione di accessibilità e note legali nel piè di pagina '
              'istituzionale',
     'Il piè di pagina aggiornato porta Privacy e Cookie Policy. La dichiarazione di '
     'accessibilità e le note legali non compaiono. Non è nel nostro perimetro — il piè di '
     'pagina è della shell — ma va posto a chi governa il design system.'),
    ('BO-21', 'Quando si rientra dal menu su ConfigMap al registro su base dati',
     '⚠️ La deroga è dichiarata temporanea e vale per il primo rilascio. Una deroga senza '
     'una data di riesame diventa l’impianto: va fissata l’occasione in cui si rientra, e '
     'il rientro va dimensionato prima, non dopo.'),
    ('BO-22', 'Il nome del remote delle operazioni di postazione',
     '⚠️ Collisione di nomi da sciogliere: questo documento chiama «mfe-operativa» l’unità '
     'di rilascio delle pagine sugli atti, mentre l’analisi del front-end chiama '
     '«mfOperation» il remote delle operazioni di postazione. Sono due cose diverse con '
     'nomi quasi identici, e vanno rinominate prima che entrino nei manifesti.'),
]


def main():
    if os.path.exists(DST):
        os.remove(DST)
    shutil.copy(SRC, DST)

    def commenti(p):
        return int(subprocess.run(
            ['bash', '-c', "unzip -p %s word/comments.xml 2>/dev/null | "
                           "grep -o '<w:comment ' | wc -l" % repr(p)],
            capture_output=True, text=True).stdout.strip() or 0)
    prima = commenti(DST)

    d = docx.Document(DST)
    fatti = []
    MOD = D.trova_tabella(d, 'Tabella', 'Che cosa dichiara')   # modello di bordi

    # ------------------------------------------------ 1. le figure, tutte da rifare
    from docx.text.paragraph import Paragraph
    seq = [Paragraph(ch, d) for ch in d.element.body.iterchildren()
           if ch.tag.endswith('}p')]
    posizioni = [k for k, p in enumerate(seq) if p._p.findall('.//' + qn('a:blip'))]
    rifatte = []
    for k in posizioni:
        # la didascalia «Figura N — …» è il primo paragrafo a valle entro cinque
        num = None
        for j in range(k + 1, min(k + 6, len(seq))):
            t = seq[j].text.strip()
            if t.startswith('Figura '):
                num = int(t.split()[1].rstrip('—').strip())
                break
        if num is None or num not in FIGURE:
            continue
        png = os.path.join(IMG, FIGURE[num])
        rid = seq[k]._p.findall('.//' + qn('a:blip'))[0].get(qn('r:embed'))
        d.part.related_parts[rid]._blob = open(png, 'rb').read()
        rifatte.append(num)
    if len(rifatte) != 18:
        raise SystemExit('attese 18 figure, rifatte %d: %s' % (len(rifatte), rifatte))
    fatti.append('18 figure riscritte con i wireframe del piè di pagina a due colonne')

    # ------------------------------------------------ 2. il piè di pagina
    D.sostituisci(
        d, 'Il piè di pagina raccoglie contatti, menu, canali e riferimenti legali su '
           'fondo scuro.',
        'Il piè di pagina raccoglie contatti, canali e riferimenti legali su fondo scuro. '
        '⚠️ Nella versione aggiornata del design system le colonne sono due e non più '
        'tre: la colonna «Menu» non c’è più.',
        attese=1, etichetta='piè di pagina a due colonne nella descrizione della cornice',
        fatti=fatti)

    # ⚠️ NON si usa trova_tabella('Elemento', 'Perché serve'): intercetterebbe la
    # tabella della TESTATA, che contiene entrambe le intestazioni fra le sue quattro.
    # Quella del piè di pagina è l'unica a due sole colonne con quella testata.
    tp = next(t for t in d.tables
              if len(t.columns) == 2
              and t.rows[0].cells[0].text.strip() == 'Elemento'
              and t.rows[0].cells[1].text.strip() == 'Perché serve')
    if any(D.ha_commenti(c._tc) for r in tp.rows for c in r.cells):
        raise SystemExit('la tabella del piè di pagina porta commenti: riscriverla a mano')
    ancora_t = tp._tbl
    D.tabella(d, ancora_t, PIEDE, modello=tp, larghezze=[1.5, 2.4, 2.4])
    ancora_t.getparent().remove(ancora_t)
    fatti.append('tabella del piè di pagina rifatta sul «Footer cdr.jpeg» (%d voci)'
                 % (len(PIEDE) - 1))

    # ------------------------------------------------ 3. la deroga del ConfigMap
    # ⚠️ ci si ancora al capitolo SUCCESSIVO: la deroga va letta dopo aver visto come il
    # menu dovrebbe costruirsi, altrimenti si legge la deroga di qualcosa non ancora detto.
    ancora = D.h(d, 1, 'La mappa dell’applicazione')

    def par(t, stile='Normal'):
        return D.para(d, ancora._p, t, stile=stile)

    par('Una deroga per il primo rilascio: il menu da ConfigMap', 'Heading 2')
    par('⚠️ **Per il primo rilascio il menu non viene dalle quattro tabelle: viene da un '
        'ConfigMap del cluster.** È una decisione presa per accorciare i tempi — le '
        'quattro tabelle, il servizio che le legge e la pagina che le governa sono lavoro '
        'che non entra nella prima consegna — ed è dichiarata qui invece di essere '
        'scoperta dopo, perché una deroga taciuta diventa l’impianto.')
    par('**Che cos’è, in concreto.** Un ConfigMap è un oggetto di Kubernetes che contiene '
        'dati di configurazione in forma di file, montato dentro il pod o letto come '
        'variabile. Il menu diventa quindi un file — tipicamente lo stesso config.json '
        'che la shell già legge a runtime per gli indirizzi dei remote — con l’elenco '
        'delle voci, il titolo, il sottotitolo, l’icona, l’ordine e l’abilitazione '
        'richiesta. La home continua a costruirsi leggendo un dato: cambia da dove il '
        'dato viene.')
    par('**Perché non è una buona pratica, detto senza attenuanti.** Il pregio del '
        'registro è che il menu sia governabile da chi usa l’applicazione e non da chi '
        'amministra il cluster. Con il ConfigMap quel pregio si perde per intero: la '
        'modifica di una voce torna a essere un’operazione di esercizio, con i tempi e le '
        'autorizzazioni di un rilascio. Il confronto, voce per voce:')
    cap = par('Le due vie a confronto. La colonna di destra è il bersaglio descritto in '
              'questo capitolo; quella di mezzo è ciò che si realizza ora.')
    for r in cap.runs:
        r.italic = True
        r.font.size = docx.shared.Pt(9)
    D.tabella(d, ancora._p, CONFIGMAP, modello=MOD, larghezze=[1.5, 2.4, 2.4])
    par('**Che cosa rende la deroga accettabile, e a quali condizioni.** Tre.')
    D.voce(d, ancora._p, 'La forma del dato non cambia.',
           'Le voci nel file hanno gli stessi attributi delle colonne di '
           'ANSC_CFG_PAGINA — codice, titolo, sottotitolo, icona, rotta, ordine, stato, '
           'abilitazione. ⚠️ È la condizione che rende il rientro una migrazione di dati '
           'e non una riscrittura: se il file nasce con una forma propria, il rientro '
           'costa quanto costruire tutto.')
    D.voce(d, ancora._p, 'Il servizio che la home interroga esiste comunque.',
           'La home non legge il file: chiede al servizio le pagine visibili per il '
           'profilo corrente, e il servizio le prende dal file invece che dalle tabelle. '
           'Così il rientro cambia una sorgente dentro un componente, e nessuna '
           'schermata se ne accorge.')
    D.voce(d, ancora._p, 'La deroga è datata.',
           'Vale per il primo rilascio e si riesamina subito dopo. Senza una data di '
           'riesame non è una soluzione tampone: è la soluzione (BO-21).')
    par('⚠️ **Una conseguenza da non sottovalutare: il filtro per abilitazione resta, ma '
        'senza vincolo di integrità.** Nelle tabelle l’abilitazione di una pagina è '
        'vincolata al vocabolario reale; in un file è una stringa. Un refuso non produce '
        'un errore: produce una voce che non compare a nessuno, oppure — ed è il caso '
        'peggiore — una voce che compare a chi non dovrebbe vederla. Finché dura la '
        'deroga, l’elenco delle abilitazioni usate nel file va confrontato con quello '
        'reale a ogni modifica, e il confronto è umano.')
    par('Resta fermo che il controllo di sicurezza non è mai nel menu: è sui servizi. '
        'Una voce mostrata per errore espone un titolo, non un dato.')
    fatti.append('nuovo capitolo «Una deroga per il primo rilascio: il menu da ConfigMap»')

    # ------------------------------------------------ 4. la pagina dei certificati
    ancora2 = D.h(d, 1, 'La copertura del modello dati')

    def par2(t, stile='Normal'):
        return D.para(d, ancora2._p, t, stile=stile)

    par2('Postazioni e certificati', 'Heading 2')
    D.immagine(d, ancora2._p, os.path.join(IMG, 'bo_certificati.png'), 6.3,
               'Figura 19 — Postazioni e certificati. La riga di inserimento sostituisce '
               'quella di ricerca; le colonne «Caricato il», «Caricato da» e «Stato» sono '
               'una proposta di questo documento e non compaiono nelle schermate fornite.')
    par2('**La pagina esiste già.** La gestione dei certificati di postazione è la prima '
         'porzione del sistema a essere stata realizzata, in versione autonoma, e le sue '
         'schermate sono fra le sorgenti [R7]. Non si sta disegnando una funzione nuova: '
         'si sta portando dentro la cornice comune una funzione che esiste, e se ne sta '
         'scrivendo il dettaglio applicativo che finora mancava.')
    par2('**Che cosa amministra.** Ogni postazione dispone di un certificato in formato '
         'PKCS#12, ed è con la chiave privata di quel contenitore che il concentratore '
         'firma le richieste verso ANPR e verso ANSC. Il registro di quei certificati è '
         'quindi il presupposto del dialogo con gli enti esterni: senza, la postazione non '
         'parla con nessuno. ⚠️ Per questo la pagina non è una pagina di configurazione '
         'dell’integrazione: amministra gli strumenti con cui una postazione si presenta, '
         'e la sua indisponibilità ferma il lavoro di uno sportello, non la revisione di '
         'un mapping.')
    par2('⚠️ **Appartiene a un’unità di rilascio diversa dalle quattro del back-office.** '
         'Il committente l’ha assegnata al remote delle operazioni di postazione, '
         '«mfOperation», che non è una delle quattro aree descritte nel capitolo sul '
         'contesto tecnico. La scelta è coerente con la natura della pagina — non '
         'configura l’integrazione e non forma atti — e con il fatto che quella porzione '
         'sia già stata costruita per conto proprio. È descritta qui perché il menu la '
         'espone accanto alle altre e perché l’operatore non percepisce il confine fra i '
         'remote: il registro delle pagine, del resto, serve esattamente a rendere quel '
         'confine invisibile. ⚠️ Resta da sciogliere una collisione di nomi fra '
         '«mfe-operativa» e «mfOperation» (BO-22).')
    par2('**Il flusso in quattro passi.** Si cerca per nome; si preme CARICA CERTIFICATO e '
         'la riga di ricerca lascia il posto a quella di inserimento, con nome, password e '
         'scelta del file; si salva e l’esito arriva come notifica in alto a destra; si '
         'elimina dal menu di riga, con una conferma che nomina il certificato. Tutto il '
         'repertorio grafico è già nella libreria condivisa: tabella, barra degli '
         'strumenti, campo riservato, scelta del file, finestra di conferma e notifica.')
    par2('Tabelle sottese', 'Heading 3')
    D.tabella(d, ancora2._p, CERT_TABELLE, modello=MOD, larghezze=[1.5, 2.0, 2.8])
    par2('Campi, colonne e azioni', 'Heading 3')
    D.tabella(d, ancora2._p, CERT_CAMPI, modello=MOD, larghezze=[1.5, 1.1, 3.7])
    par2('⚠️ **Due rilievi sulle schermate fornite, che vanno risolti prima di portare la '
         'pagina in esercizio.** Il primo è la password del contenitore mostrata in '
         'chiaro: è una credenziale che apre una chiave privata, e il componente di campo '
         'riservato esiste già nella libreria. Il secondo è l’assenza di «caricato il», '
         '«caricato da» e «scadenza»: senza la terza, in particolare, un certificato '
         'scaduto si manifesta come un guasto allo sportello invece che come un avviso. '
         'Sono registrati come BO-19.')
    fatti.append('nuova pagina «Postazioni e certificati» (figura, scopo, tabelle, campi)')

    # ------------------------------------------------ 5. mappa e copertura
    D.sostituisci(
        d, 'L’applicazione è stata pensata con quindici pagine distribuite su quattro '
           'aree funzionali.',
        'L’applicazione è stata pensata con quindici pagine distribuite su quattro aree '
        'funzionali, cui si aggiunge una sedicesima pagina — «Postazioni e certificati» — '
        'che il menu espone accanto alle altre ma che appartiene a un remote distinto, '
        'già realizzato per conto proprio.',
        attese=1, etichetta='la mappa dichiara la sedicesima pagina', fatti=fatti)

    tm = D.trova_tabella(d, 'Area', 'Pagine')
    D.clona_riga(tm, (
        'Operazioni di postazione',
        'Postazioni e certificati',
        'Chi amministra le postazioni, quando se ne aggiunge una o scade un certificato. '
        '⚠️ Non è un’area del back-office: sta nel remote «mfOperation» ed è qui perché '
        'il menu la espone e l’operatore non vede il confine.'))

    tc = D.trova_tabella(d, 'Tabella', 'Pagine che la governano')
    D.clona_riga(tc, (
        'Registro delle postazioni (di SIPO)',
        'Postazioni e certificati',
        '⚠️ Non appartiene al modello dell’integrazione: è una struttura preesistente di '
        'SIPO, di cui questo documento descrive l’interfaccia e non il disegno. Da '
        'accertare prima di realizzare (BO-18).'))
    fatti.append('mappa dell’applicazione e copertura del modello dati aggiornate')

    # ------------------------------------------------ 6. riferimenti
    tr = D.trova_tabella(d, '#', 'Riferimento')
    D.sostituisci(d, 'ANALISI_Front-End-Angular_v0.4.docx',
                  'ANALISI_Front-End-Angular_v0.6.docx', attese=1,
                  etichetta='[R2] portato alla versione corrente', fatti=fatti)
    D.clona_riga(tr, (
        '[R7]', 'screen-app-certificati.docx — le otto schermate della gestione dei '
                'certificati di postazione, nella versione autonoma già realizzata',
        'Evidenza fornita'))
    D.clona_riga(tr, (
        '[R8]', 'Footer cdr.jpeg — il piè di pagina aggiornato del design system di '
                'Roma Capitale: due colonne, sette canali, niente colonna «Menu»',
        'Evidenza fornita'))
    fatti.append('[R7] e [R8] aggiunti ai Riferimenti')

    # ------------------------------------------------ 7. punti aperti
    to = D.trova_tabella(d, '#', 'Questione')
    for r in to.rows[1:]:
        if r.cells[0].text.strip() == 'BO-6':
            D.riscrivi_cella(
                r.cells[1], 'Chiuso in questa versione. Se il registro delle postazioni '
                            'rientri nel perimetro')
            D.riscrivi_cella(
                r.cells[2], 'Deciso: la pagina rientra ed è descritta in questa versione, '
                            'ma appartiene al remote delle operazioni di postazione e non '
                            'al back-office. Restano aperte la struttura su cui poggia '
                            '(BO-18) e le colonne mancanti (BO-19).')
            break
    else:
        raise SystemExit('BO-6 non trovato')
    for sigla, questione, perche in NUOVI_BO:
        D.clona_riga(to, (sigla, questione, perche))
    fatti.append('BO-6 chiuso; BO-18…BO-22 aperti')

    # ------------------------------------------------ 8. testata e storia
    for tab in d.tables:
        if tab.rows[0].cells[0].text.strip().lower().startswith('area organizzativa'):
            for r in tab.rows:
                v = {'Versione': '0.6',
                     'Documento': 'DISEGNO_Back-Office_ANSC_v0.6'}.get(
                        r.cells[0].text.strip())
                if v:
                    D.riscrivi_cella(r.cells[1], v)
            break
    D.storia(d, '02/10/2026', '0.6',
             'Contesto tecnico · Testata e piè di pagina · Registro delle pagine · Le '
             'pagine · Mappa · Copertura · Riferimenti · Punti aperti',
             'Rigenerate tutte le diciotto figure, che mostravano ancora il piè di pagina '
             'a tre colonne: la versione aggiornata del design system ne prevede due e '
             'non ha più la colonna «Menu». Riscritto di conseguenza il capitolo sul '
             'contenuto del piè di pagina sulla nuova evidenza. Aggiunta la pagina '
             '«Postazioni e certificati», che chiude BO-6: è già realizzata in versione '
             'autonoma e appartiene al remote delle operazioni di postazione, non alle '
             'quattro aree del back-office. Aggiunto al registro delle pagine il capitolo '
             'sulla deroga del menu da ConfigMap per il primo rilascio, con il confronto '
             'fra le due vie e le tre condizioni che rendono il rientro una migrazione di '
             'dati. Cinque punti aperti nuovi.')
    fatti.append('testata e storia aggiornate')

    # ------------------------------------------------ 9. grassetti
    def grassetti(p):
        if '**' not in p.text or D.ha_commenti(p._p):
            return 0
        pezzi = D.segmenta('', p.text)
        for r in list(p.runs):
            r._r.getparent().remove(r._r)
        for testo, gr in pezzi:
            run = p.add_run(testo)
            run.bold = gr
        return 1
    n = sum(grassetti(p) for p in d.paragraphs)
    for tab in d.tables:
        for r in tab.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    n += grassetti(p)
    fatti.append('%d paragrafi con grassetto applicato' % n)

    d.save(DST)
    dopo = commenti(DST)
    if dopo != prima:
        raise SystemExit('COMMENTI PERSI: erano %d, sono %d' % (prima, dopo))
    fatti.append('commenti di Word conservati: %d → %d' % (prima, dopo))

    print('\n'.join(' · ' + f for f in fatti))
    print('capitoli/tabelle/immagini:', D.riepilogo(DST))
    print('scritto:', os.path.relpath(DST, BASE))


if __name__ == '__main__':
    main()
