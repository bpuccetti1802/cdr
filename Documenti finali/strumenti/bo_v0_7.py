# -*- coding: utf-8 -*-
"""DISEGNO_Back-Office_ANSC v0.6 → v0.7 (07/10/2026).

Nuovo capitolo «Il codice di sessione verso ANSC», dettato dal committente: il bottone
OTP è della shell, sempre disponibile, e il capitolo ne descrive i quattro stati e il
percorso di immissione in cinque schermate.

⚠️ Le cinque immagini NON sono ancora arrivate: al loro posto ci sono segnaposto
(`img/otp_*.png`). Quando arrivano si sostituiscono con `D.sostituisci_immagine()`
individuandole dalla didascalia, senza rigenerare il documento.

⚠️ Il capitolo contraddice quattro punti della v0.6, che descrivevano l'OTP come un
distintivo accanto al titolo disegnato dal micro-frontend. Vengono allineati tutti e
quattro, e BO-15 si chiude: l'area dedicata della shell non è più «in corso di
predisposizione», è la sede del bottone.

⚠️ Due fatti verificati sull'analisi [R1] che il testo dettato non considera:
  · le quattro ore decorrono da quando ANSC GENERA il codice, non da quando SIPO lo
    salva: un conto alla rovescia che parta dal salvataggio sopravvaluta il residuo;
    il concentratore espone già scadenza e minuti residui;
  · un timeout può invalidare il codice PRIMA della scadenza: un bottone che resta
    verde per quattro ore su base oraria mente.
Entrambi entrano come nota e come punto aperto.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/bo_v0_7.py
"""
import os
import re
import shutil
import subprocess
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIN = os.path.join(BASE, 'Documenti finali')
SRC = os.path.join(FIN, 'DISEGNO_Back-Office_ANSC_v0.6.docx')
DST = os.path.join(FIN, 'DISEGNO_Back-Office_ANSC_v0.7.docx')
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')

STATI = [
    ['Stato', 'Aspetto del bottone', 'Tooltip', 'Che cosa è consentito'],
    ['Nessun codice', 'Spento: non c’è ancora stata alcuna immissione.', 'Assente',
     'Il bottone si può premere. Le funzioni che dialogano con ANSC sono inibite.'],
    ['Scaduto', 'Segnalato come non valido.', '**Scaduto**',
     'Il bottone si può premere. Le funzioni che dialogano con ANSC sono inibite, e '
     'ciascuna lo ricorda quando viene richiesta.'],
    ['Valido', 'Segnalato come attivo.', 'L’**orario di scadenza**',
     'Tutto. ⚠️ Il bottone **resta premibile anche con il codice valido**: serve a '
     'sostituirlo senza aspettare che scada.'],
    ['In scadenza', 'Da distinguere dal valido.', 'L’orario di scadenza',
     '⚠️ Stato proposto da questo documento e non presente nelle schermate: sotto una '
     'soglia di guardia — la proposta dell’analisi è quindici minuti — conviene invitare '
     'a rinnovare **prima** di cominciare una sequenza lunga, invece di lasciarla '
     'interrompere a metà.'],
]

DIALOG = [
    ['Elemento', 'Genere', 'Comportamento'],
    ['Codice', 'Campo',
     'Accoglie qualunque valore alfanumerico non nullo, **al massimo dieci caratteri**. '
     'All’apertura riporta l’eventuale valore immesso in precedenza.'],
    ['Recupera OTP', 'Collegamento',
     'Porta alla pagina su cui si ottiene un codice valido. ⚠️ È la web app di ANSC, '
     'esterna a SIPO: il codice si genera lì autenticandosi con smart card o identità '
     'digitale, e si copia. Non esiste alcun modo di ottenerlo per via programmatica.'],
    ['SALVA', 'Azione',
     '**Si abilita solo se il valore immesso è diverso da quello precedente.** Alla '
     'pressione la finestra si chiude e il bottone passa a valido.'],
    ['ANNULLA', 'Azione', 'Chiude senza modificare il codice in uso.'],
]

NUOVI_BO = [
    ('BO-23', 'Da dove si legge la scadenza mostrata nel tooltip',
     '⚠️ Le quattro ore decorrono da quando ANSC genera il codice, non da quando SIPO lo '
     'riceve: fra le due cose passa il tempo che l’operatore impiega a copiarlo. Un conto '
     'alla rovescia che parta dal salvataggio sopravvaluta il tempo residuo e mostra '
     'valido un codice già scaduto. Il concentratore espone scadenza e minuti residui '
     'senza contattare ANSC [R1]: è quella la fonte.'),
    ('BO-24', 'Come il monitoraggio si accorge di un’invalidazione anticipata',
     '⚠️ Un timeout su una chiamata può invalidare il codice **prima** della scadenza. Un '
     'bottone che resti verde per quattro ore su base oraria dichiara valido ciò che non '
     'lo è più. Il monitoraggio deve recepire anche l’esito negativo di un’operazione, '
     'non solo lo scorrere del tempo.'),
    ('BO-25', 'Se la finestra debba riproporre il codice immesso in precedenza',
     '⚠️ Il codice è una credenziale: identifica l’ufficiale verso la piattaforma '
     'nazionale per quattro ore. Mostrarlo in chiaro a chiunque apra la finestra su quella '
     'postazione è lo stesso rilievo già formulato per la parola d’ordine dei certificati '
     '(BO-19). Da valutare se riproporlo, se mascherarlo o se non riproporlo affatto.'),
    ('BO-26', 'Se il salvataggio debba restare impedito quando il valore è uguale al '
              'precedente',
     'La regola evita un salvataggio inutile, ma impedisce anche di reimmettere lo stesso '
     'codice quando reimmetterlo servirebbe — per esempio dopo che un’invalidazione ne ha '
     'fatto perdere traccia a SIPO mentre su ANSC è ancora valido. Da confermare che il '
     'caso non si dia.'),
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
    MOD = D.trova_tabella(d, 'Tabella', 'Che cosa dichiara')

    # ------------------------------------------------ 1. rinumerazione delle figure
    # ⚠️ Il capitolo nuovo si inserisce dopo la Figura 2, quindi le figure da 3 a 19
    # scalano di cinque. Si rinumera AL CONTRARIO, altrimenti la 3 diventa 8 e poi la
    # 8 (che è la vecchia 3) verrebbe toccata una seconda volta.
    # Verificato prima di procedere: nel corpo non esiste alcun rimando «Figura N».
    did = [p for p in d.paragraphs if re.match(r'^Figura \d+ —', p.text.strip())]
    assert len(did) == 19, 'attese 19 didascalie, trovate %d' % len(did)
    for p in reversed(did):
        n = int(re.match(r'^Figura (\d+) —', p.text.strip()).group(1))
        if n >= 3:
            D.testo_di(p, re.sub(r'^Figura \d+ —', 'Figura %d —' % (n + 5),
                                 p.text.strip()))
    fatti.append('figure 3…19 rinumerate 8…24 per far posto alle cinque nuove')

    # ------------------------------------------------ 2. il capitolo nuovo
    ancora = D.h(d, 1, 'Il registro delle pagine e del menu')

    def par(t, stile='Normal'):
        return D.para(d, ancora._p, t, stile=stile)

    def fig(png, didascalia):
        D.immagine(d, ancora._p, os.path.join(IMG, png), 6.2, didascalia)

    par('Il codice di sessione verso ANSC', 'Heading 1')
    par('Per ogni operazione che tocca la piattaforma nazionale non basta essere '
        'autenticati a SIPO: serve un **codice di sessione** che identifica l’ufficiale '
        'verso ANSC. Lo genera l’ufficiale stesso, di persona, sulla web app di ANSC, e '
        'vale quattro ore [R1]. Questo capitolo descrive come lo si consegna '
        'all’applicazione e come l’interfaccia ne mostra lo stato.')
    par('⚠️ **Sono due sessioni distinte e restano distinte.** Quella di SIPO dice chi sei; '
        'questa dice che puoi operare su ANSC adesso. Possono scadere in momenti diversi, '
        'e l’operatore ne vede due indicazioni: confonderle è il modo più facile di '
        'rendere incomprensibile un messaggio di errore.')

    par('Il bottone nella shell', 'Heading 2')
    par('**Il bottone del codice è della shell, non delle singole pagine**: sta una volta '
        'sola nella cornice ed è quindi disponibile a tutte le funzioni che lo richiedono, '
        'in qualunque area l’operatore si trovi. È la scelta corretta, e per una ragione '
        'che va oltre la comodità: il codice è uno solo per operatore e per postazione, e '
        'un elemento ripetuto in ogni pagina lascerebbe credere il contrario.')
    par('Il bottone ha quattro stati.')
    D.tabella(d, ancora._p, STATI, modello=MOD, larghezze=[1.0, 1.5, 1.1, 2.7])
    fig('otp_scaduto.png',
        'Figura 3 — Il bottone con il codice scaduto. Il suggerimento riporta «Scaduto».')

    par('Che cosa accade quando il codice è scaduto', 'Heading 2')
    par('Ogni funzione che richieda il codice viene inibita. ⚠️ **Inibita, non nascosta**: '
        'la funzione resta visibile e, quando la si richiede, ricorda che il codice è '
        'scaduto. È la stessa regola già enunciata per le azioni di pagina — un’azione non '
        'consentita dal profilo non si mostra, un’azione non eseguibile adesso si mostra '
        'disabilitata con la ragione — e qui si applica al caso più frequente di tutti.')
    fig('otp_inibito.png',
        'Figura 4 — Il messaggio che compare premendo «Scarica da ANSC» con il codice '
        'scaduto. La funzione non sparisce: spiega perché non può eseguire.')

    par('L’immissione del codice', 'Heading 2')
    par('L’operatore preme il bottone e si apre la finestra di immissione. ⚠️ **Il bottone '
        'si preme anche quando il codice è ancora valido**: serve a sostituirlo prima che '
        'scada, che è il modo di non farsi interrompere a metà di una sequenza lunga.')
    fig('otp_dialog.png',
        'Figura 5 — La finestra di immissione, con il collegamento per ottenere un codice '
        'valido.')
    D.tabella(d, ancora._p, DIALOG, modello=MOD, larghezze=[1.2, 0.9, 4.2])
    par('⚠️ **Due osservazioni sul campo, da sciogliere prima di realizzare.** La prima: la '
        'finestra ripropone il valore immesso in precedenza, ma quel valore è una '
        'credenziale — identifica l’ufficiale verso ANSC per quattro ore — e mostrarlo in '
        'chiaro a chiunque apra la finestra su quella postazione è lo stesso rilievo già '
        'formulato per la parola d’ordine dei certificati (BO-25). La seconda: non essendo '
        'previsto alcun controllo di forma, un codice digitato male non produce un errore '
        'all’immissione ma alla prima chiamata verso ANSC, dove l’operatore lo leggerà come '
        'un guasto del sistema invece che come un refuso suo.')

    par('Dopo il salvataggio', 'Heading 2')
    par('La finestra si chiude, il bottone passa a valido e il suggerimento riporta '
        'l’orario di scadenza. Lo stato del bottone si aggiorna da sé: l’interfaccia '
        'sorveglia la validità del codice senza che l’operatore debba ricaricare la pagina.')
    fig('otp_valido.png',
        'Figura 6 — Il bottone dopo il salvataggio. Il suggerimento riporta l’orario di '
        'scadenza.')
    par('⚠️ **Due precisazioni sul tempo, perché è il punto in cui un’interfaccia di questo '
        'tipo sbaglia più facilmente.** Le quattro ore **non decorrono dal salvataggio**: '
        'decorrono da quando ANSC ha generato il codice, e fra i due momenti passa il tempo '
        'che l’operatore impiega a copiarlo. Un conto alla rovescia avviato al salvataggio '
        'sopravvaluta il residuo e, nel caso peggiore, mostra valido un codice già scaduto. '
        'La scadenza va quindi letta dal concentratore, che la espone insieme ai minuti '
        'residui senza dover contattare ANSC [R1] (BO-23).')
    par('La seconda: **un timeout può invalidare il codice prima della scadenza**. Un '
        'bottone che resti valido per quattro ore contando soltanto il tempo dichiarerebbe '
        'utilizzabile una sessione che ANSC ha già rifiutato. La sorveglianza deve quindi '
        'recepire anche l’esito negativo di un’operazione, non solo lo scorrere '
        'dell’orologio (BO-24).')

    par('Il codice valido e l’uso', 'Heading 2')
    par('Con il codice valido le funzioni che dialogano con ANSC tornano disponibili. '
        'Nell’esempio l’operatore preme «Scarica da ANSC» e il servizio popola la tabella '
        'sottostante.')
    fig('otp_scarica.png',
        'Figura 7 — Con il codice valido «Scarica da ANSC» esegue e carica la tabella.')
    par('⚠️ **Una conseguenza di disegno che vale per tutte le pagine**: poiché il codice è '
        'unico e sta nella shell, una funzione non deve mai chiederlo per conto proprio. Se '
        'manca, rimanda al bottone; se c’è, lo usa. Una seconda via di immissione '
        'produrrebbe due stati che possono divergere, ed è esattamente ciò che avere il '
        'bottone nella cornice serve a impedire.')
    fatti.append('nuovo capitolo «Il codice di sessione verso ANSC» con 5 figure e 2 tabelle')

    # ------------------------------------------------ 3. allineamento dei quattro punti
    D.sostituisci(
        d, 'Le azioni che dialogano con ANSC sono disabilitate quando manca, con la '
           'ragione visibile; il distintivo in testa alla pagina ne mostra lo stato e il '
           'tempo residuo.',
        'Le azioni che dialogano con ANSC sono disabilitate quando manca, con la ragione '
        'visibile; il bottone nella cornice della shell ne mostra lo stato e il tempo '
        'residuo, come descritto nel capitolo dedicato.',
        attese=1, etichetta='«Autorizzazione e sessione» allineato al bottone di shell',
        fatti=fatti)
    D.sostituisci(
        d, 'Il distintivo OTP accanto al titolo dovrà essere l’unico elemento di stato '
           'presente in ogni pagina.',
        'Il bottone del codice di sessione, che la shell mostra nella cornice, è l’unico '
        'elemento di stato presente in ogni pagina.',
        attese=1, etichetta='«La home» allineata', fatti=fatti)
    D.sostituisci(
        d, 'Il titolo porta il distintivo OTP; le azioni di pagina stanno a destra, non '
           'fra i filtri.',
        'Le azioni di pagina stanno a destra del titolo, non fra i filtri. ⚠️ Lo stato '
        'della sessione verso ANSC, che in S.I.De. sta sul titolo, in questo disegno è nel '
        'bottone della shell.',
        attese=1, etichetta='convenzione S.I.De. allineata', fatti=fatti)
    D.sostituisci(
        d, 'Dove sta il distintivo della sessione ANSC, e dove andrà. Oggi è accanto al '
           'titolo della pagina, cioè dentro la fascia che il micro-frontend disegna: è il '
           'punto più vicino alle azioni che la sessione abilita. È però in corso di '
           'predisposizione, a livello di shell, un’area dedicata sotto la testata: quando '
           'sarà disponibile il distintivo vi si trasferirà, guadagnando la stessa '
           'posizione in tutte le applicazioni dell’ente. Il disegno non cambia, cambia '
           'chi lo ospita.',
        'Dove sta lo stato della sessione ANSC. **Nella cornice della shell**, in un '
        'bottone sempre presente: non è più un elemento che il micro-frontend disegna '
        'accanto al titolo. La scelta è stata compiuta e chiude il punto che le versioni '
        'precedenti lasciavano aperto; il comportamento del bottone è descritto nel '
        'capitolo «Il codice di sessione verso ANSC».',
        attese=1, etichetta='il piè di pagina non rinvia più a un’area futura',
        fatti=fatti)
    fatti.append('quattro punti della v0.6 allineati al bottone di shell')

    # ------------------------------------------------ 4. punti aperti
    to = D.trova_tabella(d, '#', 'Questione')
    for r in to.rows[1:]:
        if r.cells[0].text.strip() == 'BO-15':
            D.riscrivi_cella(
                r.cells[1], 'Chiuso in questa versione. Quando l’area dedicata della shell '
                            'sarà disponibile')
            D.riscrivi_cella(
                r.cells[2], 'Deciso: lo stato della sessione verso ANSC sta in un bottone '
                            'della cornice della shell, sempre presente e condiviso da '
                            'tutte le aree. Non è più un elemento disegnato dal '
                            'micro-frontend accanto al titolo.')
            break
    else:
        raise SystemExit('BO-15 non trovato')
    for sigla, q, perche in NUOVI_BO:
        D.clona_riga(to, (sigla, q, perche))
    fatti.append('BO-15 chiuso; BO-23…BO-26 aperti')

    # ------------------------------------------------ 5. testata e storia
    for tb in d.tables:
        if tb.rows[0].cells[0].text.strip().lower().startswith('area organizzativa'):
            for r in tb.rows:
                v = {'Versione': '0.7',
                     'Documento': 'DISEGNO_Back-Office_ANSC_v0.7'}.get(
                        r.cells[0].text.strip())
                if v:
                    D.riscrivi_cella(r.cells[1], v)
            break
    D.storia(d, '07/10/2026', '0.7',
             'Il codice di sessione verso ANSC (nuovo) · Contesto tecnico · Testata e piè '
             'di pagina · La home · Punti aperti',
             'Aggiunto il capitolo sul codice di sessione verso ANSC, su indicazione del '
             'committente: il bottone appartiene alla cornice della shell, è sempre '
             'disponibile e vale per tutte le funzioni che lo richiedono. Il capitolo ne '
             'descrive i quattro stati, l’inibizione delle funzioni quando il codice manca, '
             'la finestra di immissione e il comportamento dopo il salvataggio. La scelta '
             'chiude BO-15 e rende superate quattro formulazioni delle versioni precedenti, '
             'che davano lo stato della sessione come un elemento disegnato dal '
             'micro-frontend accanto al titolo: sono state allineate. Quattro punti aperti '
             'nuovi, due dei quali riguardano il tempo — le quattro ore decorrono dalla '
             'generazione del codice e non dal suo salvataggio, e un’invalidazione può '
             'precedere la scadenza. ⚠️ Le cinque immagini del capitolo sono segnaposto in '
             'attesa delle schermate.')
    fatti.append('testata e storia aggiornate')

    # ------------------------------------------------ 6. grassetti
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
    for tb in d.tables:
        for r in tb.rows:
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
