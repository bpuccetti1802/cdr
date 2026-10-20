# -*- coding: utf-8 -*-
"""ANALISI_Identita-Profilazione-IAM v0.10 → v0.11 (20/10/2026).

Parte dalla v0.10 RIVISTA A MANO dall'utente (che ha spostato «Punti aperti» in coda).
Richiesta: i sottocapitoli «Un solo impianto per due generazioni di front-end» e «Perché non si
comincia dalla libreria» non convincono e confliggono con «Il vecchio ambiente: lasciarlo com'è».
Al loro posto: che cosa significherebbe portare il nuovo login sui Thymeleaf (numeri, interventi,
prove), i rischi e perché conviene lasciare tutto inalterato. Il BFF «non è stato digerito».

Decisioni concordate (20/10/2026):
  * il capitolo «Scelte effettuate per il TO BE» vale per il SOLO mondo nuovo; il vecchio resta
    com'è e il ragionamento sta qui, con il cap. dell'integrazione che rimanda;
  * il BFF esce dal TO BE (la piattaforma consegna il token in un cookie HttpOnly e il service
    mesh lo inoltra come Authorization: Bearer — AuthenticationFilter.java:125); resta in Parte II
    come variante non adottata; PI-19 chiuso, PI-29 riformulato;
  * NIENTE stime in giornate/uomo (dipendono dalle risorse): tolte anche quelle di [F10];
  * Figura 6 ridisegnata (`diagrammi_iam.mse_nuovo`).

Numeri verificati sul codice il 20/10/2026 (comandi in testa a ciascuna riga di PERIMETRO).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v0_11_iam_vecchio_tobe.py
"""
import os
import shutil
import sys

import docx
from docx.oxml.ns import qn
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
import diagrammi_iam      # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIN = os.path.join(BASE, 'Documenti finali')
IMG = os.path.join(FIN, 'strumenti', 'img')
SRC = os.path.join(FIN, 'ANALISI_Identita-Profilazione-IAM_v0.10.docx')
DST = os.path.join(FIN, 'ANALISI_Identita-Profilazione-IAM_v0.11.docx')

T_COSA = 'Portare il nuovo login sui front-end Thymeleaf: che cosa significherebbe'
T_PERCHE = 'Perché conviene lasciare il vecchio ambiente com’è'
T_BROWSER = 'Il token nel browser: tre requisiti'

# ------------------------------------------------------------------------------ testi
PERIMETRO = [
    ['Che cosa', 'Quanti', 'Dove si conta'],
    ['Front-end Thymeleaf', '35, tutti dipendenti dalla libreria web comune, che porta con sé '
     'quella di profilazione e quella di accesso ai servizi',
     'front-end/*, dichiarazione di CommonWeb nei pom.xml'],
    ['Maschere', '1.680 modelli di pagina', 'front-end/*/…/templates/*.html'],
    ['Classi controller dei front-end', '614', 'classi con @Controller in front-end/'],
    ['Classi che leggono il profilo di back-end', '628, con 4.781 chiamate a getRuoloBe()',
     'front-end/, sorgenti Java'],
    ['Punti in cui conta il primo ruolo', '4.829 chiamate a getRuoli().get(0)',
     'front-end/, sorgenti Java'],
    ['Moduli di back-end avviabili', '50, di cui 45 dichiarano la libreria di sicurezza '
     '(RestSecurity)', 'back-end/*, @SpringBootApplication e pom.xml'],
    ['Regole di autorizzazione nei back-end', '3.360 @PreAuthorize in 42 moduli, che decidono '
     'su un solo ruolo', 'back-end/, sorgenti Java'],
    ['Configurazioni con la chiave di firma condivisa', '57 file', 'RI-03'],
    ['Permessi da tradurre in profili', 'Le righe di R_UTENTI_RUOLI di produzione '
     '[DA VERIFICARE]', 'Non fra le sorgenti (PI-14)'],
]

INTERVENTI = [
    ['Strato', 'Che cosa cambierebbe', 'Che cosa ne segue'],
    ['Portale', 'Smettere di iniettare l’identità nelle intestazioni, oppure continuare a farlo '
     'durante la transizione con una regola di rete che impedisca di scavalcarlo.',
     'I due modi di entrare convivono per tutta la transizione.'],
    ['Libreria di profilazione', 'Diventare client della piattaforma: reindirizzamento a '
     'roma-capitale-auth, ritorno, costruzione dell’oggetto utente in sessione dal token e da '
     'roma-capitale-management invece che da ANAG_USR.', 'Sta nella libreria web comune: un suo '
     'rilascio è un rilascio dei trentacinque front-end.'],
    ['Libreria di accesso ai servizi', 'Sostituire il gettone dell’utenza tecnica con il token '
     'dell’operatore, rinnovandolo prima della scadenza.', 'Tutte le chiamate dei front-end '
     'cambiano credenziale insieme.'],
    ['Back-end', 'Verificare il token della piattaforma con la chiave pubblica; ricavarne il '
     'ruolo su cui decidono le @PreAuthorize, che il token oggi non porta (MI-06); leggere chi '
     'opera dal token e non dal corpo della richiesta.', 'Quarantacinque moduli da rilasciare; '
     'le 3.360 regole non cambiano, ma vanno ricollaudate.'],
    ['Chiave condivisa e utenze tecniche', 'Convivenza delle due firme durante la transizione, '
     'poi dismissione della chiave condivisa.', 'Due catene di fiducia, e tre famiglie di '
     'segreti, finché la transizione non si chiude.'],
    ['Permessi', 'Tradurre la quaterna utente × ruolo × area × funzionalità in profili e '
     'abilitazioni, con le eccezioni.', 'Qualcuno può perdere o guadagnare una funzione.'],
    ['Gestione degli accessi', 'AnagrafeWeb diventa sola lettura, oppure la proiezione della '
     'piattaforma (modalità A o B).', 'Cambia il lavoro di chi amministra gli accessi.'],
    ['Piattaforma', 'Aggiungere le applicazioni SIPO, oggi scritte nel codice (MI-10); profilo '
     'principale (MI-06), nodo organizzativo (MI-05), revoca che abbia effetto (MI-09), storia '
     'delle assegnazioni (MI-01); manutenzioni di priorità alta.', 'Rilasci di un’altra area, '
     'con le sue priorità (PI-33).'],
]

PROVE = [
    ['Prova', 'Che cosa verifica', 'Su quale perimetro'],
    ['Regressione funzionale', 'Ogni maschera si apre e opera come prima.',
     'I 35 front-end e le 1.680 maschere, per ciascun profilo di back-end.'],
    ['Autorizzazione', 'Ogni regola concede e nega come prima.', 'Le 3.360 @PreAuthorize, con '
     'almeno un caso che concede e uno che nega per regola.'],
    ['Utenti con più ruoli', 'Il ruolo che conta resta lo stesso.', 'I 4.829 punti del primo '
     'ruolo, con un confronto prima e dopo su un campione di utenti reali.'],
    ['Migrazione dei permessi', 'Nessuno perde o guadagna una funzione.', 'Un report di '
     'differenza su tutte le righe di R_UTENTI_RUOLI.'],
    ['Sessione', 'Scadenza, rinnovo, uscita, passaggio fra applicazioni, rientro dopo '
     'un’indisponibilità di IAM o della piattaforma.', 'Tutti i front-end.'],
    ['Catena verso ANPR e ANSC', 'Operatore e postazione dichiarati sono quelli reali.',
     'I servizi che dialogano con i sistemi nazionali.'],
    ['Trattamenti pianificati', 'Continuano a girare con la loro utenza tecnica.',
     'Tutti i trattamenti pianificati.'],
    ['Carico', 'auth, management e service mesh reggono il traffico di tutto SIPO.',
     'I volumi di SIPO [DA VERIFICARE].'],
    ['Sicurezza', 'Intestazioni contraffatte, accesso diretto ai pod, token di un’altra '
     'applicazione o scaduto.', 'Il perimetro e i back-end.'],
    ['Ritorno indietro', 'Ogni passaggio si annulla per configurazione, ambiente per ambiente.',
     'Ogni fase.'],
]

RISCHI = [
    ['Rischio', 'Perché è concreto'],
    ['Regressioni diffuse, per un cambiamento che l’operatore non vede', 'Vanno ricollaudate '
     '1.680 maschere, 3.360 regole di autorizzazione e 4.829 punti in cui conta il primo ruolo. '
     'Il comportamento funzionale non deve cambiare: un errore non lo segnala nessun requisito '
     'nuovo, lo si scopre in esercizio.'],
    ['Lo stato civile dipende da una piattaforma di un’altra area', 'auth, management e service '
     'mesh diventano obbligati per ogni accesso e ogni chiamata: un loro fermo ferma lo '
     'sportello. Il titolare ha le sue priorità (PI-33).'],
    ['I permessi tradotti male', 'La quaterna di SIPO non ha corrispondenza diretta con i '
     'profili e le eccezioni non sono misurate (PI-14): un errore toglie o concede una funzione '
     'a qualcuno.'],
    ['Si importano i difetti della piattaforma', 'Revoca senza effetto (MA-01, MA-02), percorsi '
     'interni pubblici e chiave in chiaro (MA-12, MA-14): vanno chiusi prima, e non dipende da '
     'SIPO.'],
    ['Interventi sulla piattaforma per far entrare SIPO', 'Profilo principale, nodo '
     'organizzativo, storia delle assegnazioni, configurabilità delle applicazioni (MI-01, '
     'MI-05, MI-06, MI-10): rilasci di un’altra area.'],
    ['Un doppio regime lungo', 'Per tutta la transizione convivono due modi di entrare, due '
     'firme dei token e due gestioni degli accessi. È la fase più fragile, e per trentacinque '
     'applicazioni non è breve.'],
]

DUE_MONDI = [
    ['Aspetto', 'Vecchio ambiente: resta com’è', 'Applicazioni nuove: la piattaforma'],
    ['Chi autentica', 'Il portale, con le intestazioni di IAM.', 'IAM, per il tramite di '
     'roma-capitale-auth.'],
    ['Prova dell’identità', 'Intestazioni non firmate, di cui ci si fida.', 'Un token firmato, '
     'che si verifica.'],
    ['Profili', 'ANAG_USR: ruoli, aree tematiche, funzionalità, R_UTENTI_RUOLI.',
     'roma-capitale-management: profili e abilitazioni per applicazione.'],
    ['Gestione degli accessi', 'La schermata di gestione degli utenti di AnagrafeWeb.',
     'L’interfaccia di amministrazione della piattaforma.'],
    ['Verso i back-end', 'Un’utenza tecnica per profilo di back-end; chi opera è nel corpo '
     'della richiesta.', 'Il token dell’operatore; chi opera è nel token.'],
    ['Chi emette i gettoni', 'I back-end, con una chiave condivisa (RI-03).',
     'Solo roma-capitale-auth (PI-31).'],
    ['Per chi sviluppa', 'LOGIN_USER in sessione.', 'Le abilitazioni dell’utente, dalla '
     'libreria della piattaforma.'],
    ['Applicazioni', 'I trentacinque front-end Thymeleaf e i loro back-end.',
     'Le applicazioni Angular, a cominciare dal back-office ANSC.'],
]

TRATTE = [
    ['Tratta', 'Che cosa viaggia', 'Come', 'Chi lo verifica'],
    ['Browser → roma-capitale-auth', 'Ambito e applicazione; al ritorno da IAM, il codice da '
     'scambiare.', 'Reindirizzamenti, con PKCE.', 'roma-capitale-auth e IAM.'],
    ['roma-capitale-auth → browser', 'Il token della piattaforma.', 'Un cookie «Bearer», '
     'HttpOnly.', '—'],
    ['Browser → service mesh', 'Il token.', 'Lo stesso cookie, che il browser allega da sé.',
     'Il service mesh.'],
    ['Service mesh → back-end', 'Il token.', 'Intestazione «Authorization: Bearer», aggiunta '
     'dal service mesh.', 'Il back-end, con la chiave pubblica della piattaforma (PI-31).'],
    ['Back-end → back-end', 'Lo stesso token, inoltrato senza riemetterlo.',
     '«Authorization: Bearer».', 'Il back-end chiamato.'],
    ['Trattamenti pianificati', 'Il token di un’utenza tecnica dedicata al trattamento.',
     '«Authorization: Bearer».', 'Il back-end.'],
]

REGOLE = [
    ['Regola', 'Perché, e che cosa accade se salta'],
    ['Il token non va mai nella stringa di interrogazione', 'Gli indirizzi finiscono nei '
     'registri di accesso e nel riferimento di provenienza del browser: un token in un registro '
     'è un token compromesso.'],
    ['I back-end accettano traffico solo dal service mesh', 'Altrimenti si raggiungono per '
     'un’altra strada, e la verifica del mesh non serve.'],
    ['Il cookie è Secure, HttpOnly e con SameSite', 'HttpOnly tiene il token fuori dalla portata '
     'degli script; SameSite limita le richieste partite da altri siti.'],
]

REQUISITI = [
    ['Requisito', 'Oggi', 'Che cosa serve'],
    ['Il token non torna nel corpo delle risposte', 'L’operazione di decodifica lo restituisce '
     'insieme ai dati dell’utente (MA-16).', 'Restituire i soli dati dell’utente e le '
     'abilitazioni.'],
    ['Il browser non lo conserva', 'La libreria Angular salva i dati di autenticazione, token '
     'compreso, in localStorage sotto la chiave «auth», e li scrive nella console.',
     'Conservare solo i dati dell’utente; togliere la scrittura nella console.'],
    ['Protezione dalle richieste indotte', 'Con l’autorizzazione in un cookie il browser la '
     'allega anche a una richiesta partita da un altro sito; fra le origini ammesse con '
     'credenziali c’è «null» (MA-16).', 'Un gettone anti-CSRF, oppure SameSite rigoroso con '
     'verifica dell’origine; origini ammesse esplicite (PI-29).'],
]


# ------------------------------------------------------------------------------ primitive
def blocchi(d, prima, lista, modello):
    for tipo, contenuto in lista:
        if tipo == 'p':
            D.para(d, prima, pezzi=D.segmenta('', contenuto)) if '**' in contenuto \
                else D.para(d, prima, contenuto)
        elif tipo == 'v':
            D.voce(d, prima, *contenuto)
        elif tipo == 'h2':
            D.para(d, prima, contenuto, stile='Heading 2')
        elif tipo == 'tab':
            righe, larghezze = contenuto
            D.tabella(d, prima, righe, modello, larghezze)


def unico(d, inizio, stile=None):
    ps = [p for p in d.paragraphs if p.text.strip().startswith(inizio)
          and (stile is None or p.style.name == stile)]
    if len(ps) != 1:
        raise SystemExit(f'atteso 1 paragrafo «{inizio}», trovati {len(ps)}')
    return ps[0]


def togli_fra(da, a):
    """Toglie gli elementi del corpo da «da» (compreso) ad «a» (escluso)."""
    el, n = da, 0
    while el is not a:
        nxt = el.getnext()
        assert not D.ha_commenti(el), 'elemento con commento'
        el.getparent().remove(el)
        el, n = nxt, n + 1
        assert el is not None, 'fine del corpo raggiunta'
    return n


def riga(t, testa):
    rr = [r for r in t.rows if r.cells[0].text.strip().startswith(testa)]
    assert len(rr) == 1, (testa, len(rr))
    return rr[0]


def togli_riga(t, testa):
    r = riga(t, testa)
    r._tr.getparent().remove(r._tr)


def immagine_proporzionata(d, inizio_didascalia, png):
    """Come D.sostituisci_immagine, ma riallinea l'altezza alle proporzioni del PNG nuovo."""
    D.sostituisci_immagine(d, inizio_didascalia, png)
    ps = d.paragraphs
    i = [k for k, p in enumerate(ps) if p.text.strip().startswith(inizio_didascalia)][0]
    w, h = Image.open(png).size
    for tag in ('wp:extent', 'a:ext'):
        for e in ps[i - 1]._p.iter(qn(tag)):
            e.set('cy', str(int(int(e.get('cx')) * h / w)))


def main():
    if os.path.exists(DST):
        os.remove(DST)
    shutil.copy(SRC, DST)
    d = docx.Document(DST)
    modello = d.tables[3]
    fatti = []

    # ------------------------------------------------ Executive summary
    p = unico(d, 'Sull’integrazione con l’IAM il punto di partenza')
    D.testo_di(p, 'Sull’integrazione con l’IAM il punto di partenza è migliore di quanto '
               'sembri: SIPO non è fuori dall’IAM ma ne usa la modalità più debole. Le '
               'intestazioni «iv-» non sono un arrangiamento proprietario ma la modalità header '
               'prevista dal capitolo 3.2 della specifica dell’ente [F4]. Per il vecchio '
               'ambiente la raccomandazione è di restare lì: portarvi il nuovo login toccherebbe '
               'tutti i front-end e i back-end, con rischi che il beneficio non compensa. Il '
               'nuovo login, con il token firmato della piattaforma, si adotta per le '
               'applicazioni nuove.')
    fatti.append('Executive summary: tolta la frase sui front-end che «si configurano»')

    # ------------------------------------------------ Parte II: il BFF non adottato
    s4 = D.h(d, 3, 'S4 — Convergenza')
    D.para(d, s4._p, 'La variante non è stata adottata. La piattaforma scelta consegna il token '
           'al browser in un cookie non leggibile dagli script e lo fa leggere al service mesh: '
           'è un modello diverso dal BFF, che ottiene la stessa proprietà essenziale a tre '
           f'condizioni, fissate nel TO BE («{T_BROWSER}») invece di aggiungere un componente.')
    fatti.append('Parte II: BFF dichiarato non adottato')

    # ------------------------------------------------ cap. Scelte: perimetro
    intro = unico(d, 'La scelta è stata compiuta dal referente tecnico')
    D.para(d, intro._p.getnext(), pezzi=D.segmenta('', (
        '**Il perimetro della scelta è il mondo nuovo**: le applicazioni Angular, a cominciare '
        'dal back-office ANSC. Per i trentacinque front-end Thymeleaf la scelta è di lasciarli '
        f'come sono: che cosa comporterebbe portarvi la piattaforma, e perché non conviene, è nei '
        f'sottocapitoli «{T_COSA}» e «{T_PERCHE}».')))

    p = unico(d, 'Il punto di autenticazione di SIPO è dunque')
    vecchio = 'Il punto di autenticazione di SIPO è dunque'
    nuovo = 'Il punto di autenticazione delle applicazioni nuove di SIPO è dunque'
    if vecchio in p.runs[0].text:
        p.runs[0].text = p.runs[0].text.replace(vecchio, nuovo)
    else:
        D.testo_di(p, p.text.replace(vecchio, nuovo))

    D.testo_di(unico(d, 'Nel seguito si continua a chiamare token SIPO'), 'Nel seguito si '
               'chiama token della piattaforma quello che roma-capitale-auth emette per le '
               'applicazioni di SIPO. Che cosa contiene, e che cosa deve contenere.')
    png = os.path.join(IMG, diagrammi_iam.mse_nuovo(IMG))
    immagine_proporzionata(d, 'Figura 6', png)
    D.testo_di(unico(d, 'Figura 6'), 'Figura 6 — L’architettura adottata, per le applicazioni '
               'nuove. I numeri sono i passi del login; in verde ciò che esiste ed è adeguato, '
               'in giallo ciò che va adeguato, in viola le applicazioni nuove di SIPO, in grigio '
               'il vecchio ambiente, che resta com’è.')

    comp = D.trova_tabella(d, 'Componente', 'Che cosa fa', 'Stato')
    for testa in ('I 35 front-end Java', 'I back-end', 'Portale'):
        togli_riga(comp, testa)
    D.clona_riga(comp, ('Le applicazioni Angular nuove', 'La shell e i micro-frontend, con la '
                        'libreria che è il modulo comune della piattaforma: accesso con '
                        'roma-capitale-auth, menu e pagine sulle abilitazioni.',
                        'Da configurare: codici di ambito e di applicazione (PI-35) e i tre '
                        f'requisiti di «{T_BROWSER}».'))
    D.clona_riga(comp, ('I back-end delle applicazioni nuove', 'Verificano il token della '
                        'piattaforma con la chiave pubblica, decidono sulle abilitazioni e '
                        'leggono chi opera dal token.', 'Da costruire così fin dall’inizio.'))
    tok = D.trova_tabella(d, 'Che cosa dice')
    D.riscrivi_cella(riga(tok, 'Chi è').cells[2], 'Adeguato. Il raccordo è il codice fiscale, '
                     'come la piattaforma fa dal 4 marzo 2026 (decisione D3); la bonifica di '
                     'ANAG_USR.CODICE_FISCALE serve se gli utenti si alimentano dall’anagrafe di '
                     'SIPO (modalità A).')
    D.riscrivi_cella(riga(tok, 'Che cosa può fare').cells[2], 'Adeguato per le applicazioni '
                     'nuove, che decidono sulle abilitazioni, purché i codici siano univoci '
                     '(MA-07). Ruoli e profilo principale (MI-06) servirebbero solo se i '
                     'back-end esistenti dovessero accettare il token.')
    fatti.append('Figura 6 ridisegnata; componenti e token riferiti alle sole applicazioni nuove')

    # ------------------------------------------------ da «Un solo impianto» a «Scadenza»: rifatto
    da = D.h(d, 2, 'Un solo impianto per due generazioni di front-end')._p
    a = D.h(d, 2, 'Scadenza, uscite, indisponibilità')._p
    n = togli_fra(da, a)
    blocchi(d, a, [
        ('h2', T_COSA),
        ('p', 'Il nuovo login si adotta per le applicazioni nuove. Prima di dire perché non '
              'conviene estenderlo al vecchio ambiente, conviene dire con precisione che cosa '
              'significherebbe: quali componenti si toccano, quanti, con quali prove. I numeri '
              'sono verificati sul codice dei front-end e dei back-end di SIPO; le giornate di '
              'lavoro non si stimano, perché dipendono dalle risorse che eseguirebbero '
              'l’intervento.'),
        ('tab', (PERIMETRO, [2.0, 2.6, 1.8])),
        ('p', 'Il dato che pesa di più non è nessuno dei numeri preso da solo, ma la loro '
              'combinazione: tutti i front-end dipendono dalla stessa libreria web comune, che '
              'porta con sé quella di profilazione e quella di accesso ai servizi. Cambiare '
              'quelle librerie è una modifica in un punto solo, ma il suo effetto si collauda '
              'ovunque.'),
        ('p', 'Gli interventi, strato per strato:'),
        ('tab', (INTERVENTI, [1.4, 2.8, 2.2])),
        ('p', 'Le prove. Il comportamento delle maschere non deve cambiare, e proprio per questo '
              'va dimostrato su tutto il perimetro:'),
        ('tab', (PROVE, [1.5, 2.4, 2.5])),
        ('p', 'Se si decidesse di procedere, le strade possibili sono due. La prima fa della '
              'libreria di profilazione un client della piattaforma: un rilascio della libreria '
              'comune, e quindi dei trentacinque front-end, con l’intera campagna di prove. La '
              'seconda mette roma-capitale-auth davanti ai front-end, che continuano a leggere '
              'le intestazioni di oggi valorizzate però da dati verificati: nessuna modifica ai '
              'front-end nella prima fase, ma tutto il traffico del vecchio ambiente passa dalla '
              'piattaforma, e la strada è sicura solo con una regola di rete che impedisca di '
              'raggiungere i front-end senza passarvi. In entrambe i back-end dovrebbero '
              'accettare per tutta la transizione sia il gettone tecnico di oggi sia il token '
              'della piattaforma, e ogni passaggio dovrebbe potersi annullare per '
              'configurazione.'),

        ('h2', T_PERCHE),
        ('p', 'Il beneficio di portare il nuovo login nel vecchio ambiente è reale: l’identità '
              'della persona firmata fino ai back-end, il passaggio fra le applicazioni senza un '
              'nuovo accesso, una sola gestione degli accessi per l’ente. Va messo accanto a ciò '
              'che costa e a ciò che rischia.'),
        ('tab', (RISCHI, [2.2, 4.2])),
        ('p', 'Il vecchio ambiente funziona, non è destinato a crescere e sarà affiancato dalle '
              'applicazioni nuove: un intervento che lo tocca tutto, senza cambiarne il '
              'comportamento per chi lo usa, costa e rischia più di quanto rende. **Il '
              'suggerimento è di lasciare il vecchio ambiente tutto com’è**: accesso, '
              'profilazione e gestione degli accessi restano quelli di oggi, e la piattaforma '
              'si adotta per le applicazioni nuove, dove nasce senza un esistente da '
              'sostituire.'),
        ('tab', (DUE_MONDI, [1.4, 2.5, 2.5])),
        ('p', 'Lasciarlo com’è non vuol dire lasciarlo esposto. Tre interventi riguardano il '
              'vecchio ambiente e restano necessari, perché non dipendono dalla piattaforma e '
              'non ne cambiano i meccanismi.'),
        ('v', ('La clausola di chiusura dei back-end. ', 'I servizi che oggi rispondono senza '
               'token devono rifiutare tutto ciò che non è esplicitamente consentito (RI-01). È '
               'un intervento piccolo e non dipende da nessuna delle decisioni aperte.')),
        ('v', ('La fiducia nelle intestazioni del portale. ', 'Resta, e si contiene con le misure '
               'di S0: una regola di rete che impedisca di raggiungere i front-end senza passare '
               'dal portale, e il portale che cancella le intestazioni di identità arrivate dal '
               'browser.')),
        ('v', ('I segreti in chiaro. ', 'La chiave condivisa dei back-end (RI-03) va portata '
               'fuori dalla configurazione versionata, indipendentemente dal login.')),

        ('h2', 'Il login di un operatore nelle applicazioni nuove'),
        ('p', 'L’operatore apre un’applicazione nuova di SIPO — per prima il back-office ANSC — '
              'e non ha ancora il cookie della piattaforma. La shell chiama roma-capitale-auth '
              'con il codice di ambito e quello dell’applicazione; auth lo manda a IAM, che lo '
              'autentica con le credenziali, SPID o CIE — la scelta è di IAM, non nostra. Al '
              'ritorno auth scambia il codice con i token di IAM, ne ricava il codice fiscale e '
              'chiede a roma-capitale-management chi sia quella persona per quell’applicazione e '
              'quali abilitazioni abbia.'),
        ('p', 'Se l’utente non è censito o è disabilitato l’accesso dovrà essere negato con un '
              'messaggio esplicito: è un miglioramento concreto rispetto ad oggi, dove lo stesso '
              'caso si presenta all’operatore come un generico «utente senza ruoli» e manda il '
              'supporto a cercare nel posto sbagliato.'),
        ('p', 'Se tutto procede, auth emette il token della piattaforma in un cookie non leggibile '
              'dagli script e riporta l’operatore alla shell, che riceve i dati dell’utente e le '
              'abilitazioni — senza il token — e costruisce il menu. Un’altra applicazione nuova '
              'non richiede un nuovo accesso, perché il cookie è già presente sul dominio '
              'dell’ente. La registrazione dell’accesso, oggi, nella piattaforma non avviene '
              '(MA-17).'),

        ('h2', 'Le chiamate verso i back-end'),
        ('p', 'Il browser chiama i servizi con il cookie, che allega da sé: il codice della shell '
              'non tocca il token. Il service mesh legge il cookie, verifica il token e lo '
              'inoltra al back-end nell’intestazione «Authorization: Bearer» [F13]. Il back-end '
              'verifica firma, emittente, scadenza e destinatario, decide sulle abilitazioni e '
              'legge chi opera dal token, non dal corpo della richiesta.'),
        ('p', 'Da back-end a back-end lo stesso token viene inoltrato, così un servizio che '
              'dialoga con ANSC o con ANPR può dichiarare l’operatore reale. I processi senza '
              'utente — i trattamenti pianificati — non hanno una richiesta in corso: usano '
              'l’accesso tecnico della piattaforma, con un’utenza dedicata al trattamento e non '
              'il codice fiscale di una persona.'),

        ('h2', 'Il token, tratta per tratta'),
        ('tab', (TRATTE, [1.5, 1.7, 1.6, 1.6])),
        ('p', 'Tre regole tengono sicuro il trasporto:'),
        ('tab', (REGOLE, [2.2, 4.2])),
        ('p', 'Il vincolo di dimensione la piattaforma lo gestisce già: oltre una soglia, nel '
              'cookie va una versione del token senza abilitazioni e quella completa resta in '
              'Redis.'),

        ('h2', T_BROWSER),
        ('p', 'La piattaforma non usa un Backend For Frontend: è roma-capitale-auth a consegnare '
              'il token al browser, in un cookie non leggibile dagli script, ed è il service mesh '
              'a leggerlo. È un modello legittimo e si adotta così com’è, senza aggiungere '
              'componenti. Regge a tre condizioni, che oggi non sono tutte rispettate.'),
        ('tab', (REQUISITI, [1.8, 2.4, 2.2])),
        ('p', 'Con queste tre condizioni il token non passa mai dal codice della pagina: è la '
              'proprietà che un BFF avrebbe dato, ottenuta senza un componente in più.'),
    ], modello)
    fatti.append(f'cap. Scelte: tolti {n} elementi (impianto unico, libreria, login, chiamate, '
                 'tratte, BFF) e scritti sette sottocapitoli')

    # ------------------------------------------------ scadenza: l'ultima voce
    vv = unico(d, 'Intestazioni contraffatte inviate dal browser')
    D.voce(d, vv._p, 'Token manomesso, scaduto o di un’altra applicazione. ',
           'Firma, scadenza o destinatario non tornano e la chiamata è rifiutata.')
    vv._p.getparent().remove(vv._p)

    # ------------------------------------------------ via le due sequenze
    da = D.h(d, 2, 'Come ci si arriva: due sequenze')._p
    a = D.h(d, 2, 'La sostenibilità sull’architettura di destinazione')._p
    n = togli_fra(da, a)
    fatti.append(f'tolto «Come ci si arriva: due sequenze» ({n} elementi, stime comprese)')

    # ------------------------------------------------ sostenibilità
    p = unico(d, 'La soluzione è stata concepita a partire dal mondo Java')
    D.testo_di(p, 'Restano i punti da definire perché la piattaforma regga per le applicazioni '
               'nuove di SIPO, a cominciare dal back-office ANSC.')
    so = D.trova_tabella(d, 'Punto', 'Come sta oggi', 'Che cosa serve fare')
    r = riga(so, 'Il vocabolario dell’autorizzazione')
    D.riscrivi_cella(r.cells[0], 'Il vocabolario dell’autorizzazione')
    D.riscrivi_cella(r.cells[1], 'La libreria Angular decide su una lista di abilitazioni '
                     '(user.abilitazioni, usata da AbilitationService, AuthorizationService e '
                     'dalla guardia delle rotte). Il token della piattaforma porta le abilitazioni '
                     'dell’applicazione, ma come codici senza l’applicazione (MA-07).')
    D.riscrivi_cella(r.cells[2], 'Codici di abilitazione univoci su tutte le applicazioni di '
                     'SIPO, perché il menu del back-office ANSC poggia su '
                     'ANSC_CFG_PAGINA_ABILITAZ; i back-end nuovi decidono sulle stesse '
                     'abilitazioni, non su un ruolo.')
    togli_riga(so, 'Il gettone nel browser')
    r = riga(so, 'I micro-frontend e il BFF')
    D.riscrivi_cella(r.cells[0], 'I micro-frontend e il cookie')
    D.riscrivi_cella(r.cells[2], 'Va verificato da dove si serve il manifesto dei remote: se '
                     'manifesto e remote arrivano da un’altra origine le chiamate diventano '
                     'inter-origine, il cookie con SameSite non parte, e la shell si carica ma '
                     'le chiamate tornano non autorizzate.')
    r = riga(so, 'Il BFF non è senza stato')
    D.riscrivi_cella(r.cells[0], 'L’alta affidabilità della piattaforma')
    D.riscrivi_cella(r.cells[1], 'auth, management e service mesh sono sul percorso di ogni '
                     'accesso e di ogni chiamata delle applicazioni nuove.')
    D.riscrivi_cella(r.cells[2], 'Almeno due repliche di ciascuno, chiavi e token fuori dalla '
                     'memoria locale, e una sonda di prontezza che non dipenda dalla '
                     'raggiungibilità di IAM: altrimenti un disservizio esterno fa riavviare un '
                     'componente sano.')
    D.riscrivi_cella(riga(so, 'L’intercettore').cells[2], 'Con il token in un cookie il browser '
                     'lo allega da sé, e l’intercettore resta vuoto per scelta e non per '
                     'dimenticanza; servirà soltanto per l’eventuale intestazione anti-CSRF '
                     '(PI-29).')
    p = unico(d, 'Il primo punto della tabella è quello critico')
    D.testo_di(p, 'Il primo punto della tabella è quello critico perché è l’unico che possa '
               'fermare il back-office nuovo: il menu, nel disegno del back-office, è un dato, e '
               'se due applicazioni usano lo stesso codice di abilitazione la shell non sa a '
               'quale delle due si riferisca.')
    fatti.append('sostenibilità riferita alle sole applicazioni nuove')

    # ------------------------------------------------ via «Che cosa cambia rispetto a oggi»
    da = D.h(d, 2, 'Che cosa cambia rispetto a oggi')._p
    a = D.h(d, 2, 'Prerequisiti e adempimenti')._p
    togli_fra(da, a)
    pr = D.trova_tabella(d, 'Prerequisito', 'Perché', 'A chi compete')
    D.riscrivi_cella(riga(pr, 'La bonifica di ANAG_USR').cells[1], 'È la chiave che lega '
                     'l’utente di IAM a quello di SIPO, se gli utenti delle applicazioni nuove si '
                     'alimentano dall’anagrafe di SIPO (modalità A).')
    togli_riga(pr, 'La raggiungibilità diretta dei front-end')
    assert len(pr.rows) == 6          # «cinque cose»: intestazione + cinque
    fatti.append('tolti «Che cosa cambia rispetto a oggi» (confluito nella tabella dei due '
                 'mondi) e il prerequisito della sequenza B')

    # ------------------------------------------------ cap. integrazione: il vecchio ambiente
    h = D.h(d, 2, 'Il vecchio ambiente: lasciarlo com’è', esatto=True)
    tieni = unico(d, 'Ne discendono due conseguenze')
    togli_fra(h._p.getnext(), tieni._p)
    # dopo le conseguenze, tutto fino al capitolo seguente (bilancio, tabella, RI-01) è
    # confluito nel capitolo delle scelte
    togli_fra(tieni._p.getnext(), D.h(d, 1, 'Le strutture dati del servizio')._p)
    D.para(d, tieni._p, 'I rischi della tabella precedente confermano la raccomandazione del '
           'capitolo «Scelte effettuate per il TO BE»: per il vecchio ambiente si lascia tutto '
           'com’è, e la piattaforma si adotta per le applicazioni nuove. Che cosa comporterebbe '
           f'fare altrimenti, e perché non conviene, è nei sottocapitoli «{T_COSA}» e '
           f'«{T_PERCHE}»; qui conta che cosa la scelta comporta per la gestione degli accessi.')
    fatti.append('cap. integrazione: «Il vecchio ambiente» ridotto a rimando e conseguenze')

    # ------------------------------------------------ punti aperti
    pa = D.trova_tabella(d, '#', 'Questione', 'A chi compete')
    r = riga(pa, 'PI-19')
    D.riscrivi_cella(r.cells[1], 'Chiuso. ' + r.cells[1].text.strip() + ' Non si adotta un BFF: '
                     'la piattaforma consegna il token in un cookie HttpOnly e lo fa leggere al '
                     f'service mesh; le condizioni sono in «{T_BROWSER}».')
    r = riga(pa, 'PI-29')
    D.riscrivi_cella(r.cells[1], 'Quale protezione dalle richieste indotte adotta la piattaforma '
                     'per il cookie che porta il token: un gettone anti-CSRF a doppio invio, '
                     'un’intestazione dedicata, oppure cookie rigorosamente di primo sito con '
                     'verifica dell’origine. La questione nasce dal token in un cookie, e va '
                     'decisa prima di scrivere la shell (MA-16).')
    D.riscrivi_cella(r.cells[2], 'Titolare della piattaforma / Architettura')
    r = riga(pa, 'PI-20')
    D.riscrivi_cella(r.cells[1], 'Chiuso. ' + r.cells[1].text.strip() + ' Il token della '
                     'piattaforma porta già le abilitazioni, su cui decidono le applicazioni '
                     'nuove; ruoli e profilo principale servirebbero solo ai back-end del vecchio '
                     'ambiente, che resta com’è.')
    r = riga(pa, 'PI-21')
    D.riscrivi_cella(r.cells[1], 'Chiuso. ' + r.cells[1].text.strip() + ' La sequenza che '
                     'faceva attraversare il componente da tutto il traffico dei front-end non è '
                     'adottata.')
    fatti.append('PI-19, PI-20, PI-21 chiusi; PI-29 riformulato')

    D.storia(d, '20/10/2026', '0.11',
             'Executive summary · Parte II (S3) · Scelte effettuate per il TO BE · '
             'L’integrazione con la gestione AS-IS · Punti aperti',
             'Il capitolo delle scelte vale per le sole applicazioni nuove. Al posto dei '
             'sottocapitoli sull’impianto unico e sulla libreria, che cosa significherebbe '
             'portare il nuovo login sui front-end Thymeleaf — perimetro misurato sul codice, '
             'interventi per strato, prove — e perché conviene lasciare il vecchio ambiente '
             'com’è. Login, chiamate e token descritti sul modello della piattaforma, con il '
             'cookie e il service mesh; il BFF non è adottato e lascia il posto a tre requisiti '
             'sul token nel browser. Tolte le due sequenze di adozione e le relative stime. '
             'Figura 6 ridisegnata. PI-19, PI-20 e PI-21 chiusi, PI-29 riformulato.')
    for f in D.frontespizio(d, '0.11', 'ANALISI_Identita-Profilazione-IAM_v0.11'):
        fatti.append(f)

    d.save(DST)
    print('\n'.join('  · ' + f for f in fatti))
    cap, tab, fig = D.riepilogo(DST)
    print(f'  capitoli {cap}, tabelle {tab}, immagini {fig}')
    print('  scritto', DST)


if __name__ == '__main__':
    main()
