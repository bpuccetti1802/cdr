# -*- coding: utf-8 -*-
"""ANALISI_Identita-Profilazione-IAM v0.1 → v0.2 (02/10/2026).

Aggiunge alla parte TO-BE il capitolo delle soluzioni possibili, ordinate dalla più
conservativa alla più coerente con l'architettura di destinazione, valutate contro i tre
vincoli dichiarati dal committente: front-end Angular, back-end Java, esercizio in
Kubernetes. Per ciascuna, pro e contro — comprese le due che le analisi di partenza non
avevano considerato.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/diagrammi_iam.py img
    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v0_2_iam_soluzioni.py
"""
import os
import re
import shutil
import sys

import docx
from docx.shared import Inches, Pt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(BASE, 'Documenti finali', 'ANALISI_Identita-Profilazione-IAM_v0.1.docx')
DST = os.path.join(BASE, 'Documenti finali', 'ANALISI_Identita-Profilazione-IAM_v0.2.docx')
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')

VINCOLI = [
    ['Vincolo', 'Come pesa sulla scelta'],
    ['**Front-end Angular**',
     'Le applicazioni nuove sono micro-frontend Angular e **non possono usare la modalità '
     'header**: non esiste una pagina prodotta dal server su cui iniettare intestazioni. '
     '⚠️ Ne discende il criterio che ordina tutta la scala: una soluzione che serva solo i '
     'trentacinque front-end Java lascia le applicazioni nuove su un altro impianto.'],
    ['**Back-end Java**',
     'I quarantaquattro servizi sono Spring Boot 2.1 con il modulo OAuth2 fuori supporto. '
     'Verificare un gettone firmato asimmetricamente è alla loro portata; emetterlo in modo '
     'sicuro lo è molto meno. ⚠️ Questo spinge verso un emittente unico e contro i '
     'quarantaquattro emittenti di oggi.'],
    ['**Esercizio in Kubernetes**',
     'Un componente in più non è un costo di esercizio rilevante: il cluster ne ospita già '
     'ottanta. Il costo vero è il percorso formale — manuale operativo, richiesta di risorse, '
     'alta affidabilità — e il fatto che un componente sul percorso del login, se cade, '
     'impedisce a tutti di entrare. ⚠️ I segreti distribuiti a molti contenitori sono invece '
     'meno gravi che altrove: un solo oggetto di tipo Secret, riferito da tutti i '
     'deployment dello spazio dei nomi.'],
]

CONFRONTO = [
    ['', 'S0', 'S1', 'S2', 'S3', 'S4'],
    ['Componenti nuovi da esercire', 'nessuno', 'nessuno', 'uno, di terzi', 'uno, proprio',
     'nessuno'],
    ['Registrazioni presso IAM', '—', '35', '1', '1', 'già fatta'],
    ['Dove vive il segreto del client', '—', '35 deployment', 'nel Broker', 'nel gateway',
     'in msAuth'],
    ['Chiude la fiducia negli header', 'No', 'Sì', 'Sì', 'Sì', 'Sì'],
    ['Porta l’identità ai back-end', 'No', 'No', 'Possibile', 'Sì', 'Da accertare'],
    ['Serve anche ai front-end Angular', 'No', 'No', 'Possibile', 'Possibile',
     '**Già li serve**'],
    ['Crea un secondo impianto', '—', 'Sì', 'Forse', 'Sì', '**No**'],
    ['Dipendenza da terzi', 'Nessuna', 'Solo IAM', 'Alta', 'Solo IAM', 'Interna all’ente'],
    ['Effort indicativo', '5-10 gg', '45-60 gg', '40-55 gg', '55-75 gg', 'da stimare'],
]

SOLUZIONI = [
    ('S0 — Consolidamento in modalità header',
     ['Non è un’integrazione ed è bene dirlo subito: è **il pavimento**. Si resta sugli '
      'header e si chiudono i difetti che non dipendono da come si entra — la clausola di '
      'chiusura nei resource server, la rimozione del percorso alternativo, gli attributi e '
      'la durata della sessione, la regola di rete che impedisca di raggiungere i servizi '
      'scavalcando il proxy.',
      '⚠️ **Va fatta comunque, qualunque sia la soluzione scelta**, e conviene farla per '
      'prima: non dipende da nessuna delle sei decisioni, non richiede alcun presidio '
      'esterno e rimuove il rilievo più grave. È l’unica voce della scala che si può '
      'cominciare questa settimana.'],
     [['Pro', 'Contro'],
      ['Giorni, non mesi. Nessuna decisione preliminare, nessun interlocutore esterno, '
       'nessun rischio di regressione sul percorso di accesso.',
       'Non chiude la fiducia negli header, che resta il difetto strutturale: '
       'l’identità continua a essere ciò che la richiesta dichiara.'],
      ['Rimuove il rilievo critico RI-01, che tutte le altre soluzioni lasciano aperto.',
       'Non porta alcuna identità ai back-end: le utenze tecniche restano.'],
      ['Riduce la gravità di tutto il resto: un difetto sfruttabile solo da dentro la rete '
       'è un’altra cosa da uno sfruttabile da fuori.',
       '⚠️ **Non è praticabile per i front-end Angular.** Senza una pagina prodotta dal '
       'server non c’è dove iniettare intestazioni: le applicazioni nuove resterebbero '
       'comunque su un impianto diverso.']],
     'Kubernetes: nessun componente nuovo. Va però istituita o verificata la regola di rete '
     'che consente di raggiungere i servizi soltanto attraverso il proxy — è ciò che '
     'trasforma RI-01 e RI-04 da sfruttabili a teorici (PI-12).'),

    ('S1 — OIDC dentro la libreria condivisa',
     ['È l’opzione A delle analisi di partenza, e la via più breve per sostituire gli '
      'header. La libreria di profilazione diventa il componente che dialoga con IAM: punto '
      'di ingresso, callback, scambio fuori banda, convalida del gettone, mappatura sui '
      'campi dell’oggetto di sessione.',
      'Sul piano realizzativo va scritta con una callback esplicita e non affidandosi al '
      'supporto nativo del framework: la versione in uso è antecedente a quello che '
      'servirebbe, e le librerie necessarie sono già presenti come dipendenza indiretta. '
      'È la decisione D5.'],
     [['Pro', 'Contro'],
      ['Nessun componente nuovo da esercire: l’intervento è concentrato in una libreria che '
       'i trentacinque front-end già condividono.',
       '**Trentacinque indirizzi di ritorno** da registrare presso IAM e da tenere '
       'allineati, oppure altrettanti client.'],
      ['È il modello che la specifica dell’ente descrive e che quindi il presidio conosce.',
       'Il segreto del client va distribuito a trentacinque contenitori. ⚠️ In Kubernetes è '
       'meno grave di quanto suoni — un solo oggetto Secret riferito da tutti — ma resta '
       'una superficie più ampia.'],
      ['Il contratto verso le applicazioni non cambia: si configurano, non si riscrivono.',
       'Ogni front-end deve raggiungere IAM in uscita per lo scambio fuori banda e per il '
       'materiale di verifica: regole di uscita da trentacinque pod.'],
      ['Reversibile, se scritta dietro un’interfaccia che separi il reindirizzamento dal '
       'ritorno.',
       '⚠️ **Il gettone di IAM non è spendibile verso i back-end**: il destinatario '
       'dichiarato è il client IAM. La decisione D4 resta intera, e con essa RI-02.'],
      ['', '⚠️ **Non serve ai front-end Angular**, che quella libreria non la usano. Il '
           'doppio impianto resta.']],
     'Kubernetes: nessun deployment nuovo, ma trentacinque che cambiano configurazione e '
     'vanno rilasciati e ricollaudati. Le callback vanno esposte attraverso gli ingress già '
     'esistenti, con la corrispondenza esatta degli indirizzi registrati.'),

    ('S2 — Identity Broker di terze parti',
     ['È l’opzione B delle analisi. Un intermediario si registra presso IAM come unico '
      'client, normalizza gli attributi ed emette un proprio gettone verso le applicazioni. '
      'SIPO parlerebbe con lui e non direttamente con IAM.',
      '⚠️ **È l’unica soluzione della scala che oggi non raccomanderei**, e non per '
      'preferenza. La sua documentazione descrive l’integrazione con due prodotti diversi '
      'dall’IAM di Roma Capitale: la compatibilità è da dimostrare, non da assumere. E porta '
      'un comportamento che su un percorso di login è difficile da accettare.'],
     [['Pro', 'Contro'],
      ['Una sola registrazione presso IAM, un solo segreto, un solo punto di uscita verso '
       'l’esterno.',
       '⚠️ **Se la verifica della firma fallisce, ricade sulla lettura dei claim senza '
       'validarla.** Un guasto transitorio — una rotazione di chiavi, un recupero del '
       'materiale di verifica andato storto — si converte in un aggiramento '
       'dell’autenticazione. Per atti di stato civile non è accettabile se non è '
       'disattivabile.'],
      ['Il suo gettone potrebbe diventare quello da propagare ai back-end, chiudendo anche '
       'la decisione D4 con lo stesso componente.',
       'Legge i claim da un endpoint che la specifica dell’ente dichiara non utilizzabile '
       'per scopi diversi dall’autenticazione: va riconfigurato.'],
      ['È un fornitore già indicato per l’accesso unico, quindi con un rapporto '
       'contrattuale esistente.',
       'Il modello normalizzato che espone non contiene il tipo di utente né alcuno dei '
       'claim della seconda fase del front office: senza estensione si perde la '
       'distinzione fra dipendente e cittadino.'],
      ['Potrebbe servire anche i front-end Angular, evitando il doppio impianto.',
       'Aggiunge un componente di terze parti sul percorso critico del login, con la sua '
       'disponibilità e i suoi tempi di intervento.']],
     'Kubernetes: un componente in più, dentro o fuori dal cluster, con la propria alta '
     'affidabilità. ⚠️ Prima di valutarla servono tre risposte (PI-09): supporto all’IAM '
     'dell’ente, claim applicativi nel gettone, disattivabilità del ripiego senza verifica.'),

    ('S3 — Gateway di autenticazione proprio di SIPO',
     ['È l’opzione C delle analisi: un servizio Java che fa da unico interlocutore verso IAM '
      'ed emette gettoni di SIPO, firmati asimmetricamente e con i claim applicativi — '
      'identificativo dell’utente, ruoli, profilo, organizzazione, postazione. I back-end '
      'smettono di essere emittenti e diventano soltanto verificatori.',
      'È la soluzione architetturalmente più pulita fra quelle che comportano una '
      'costruzione: **chiude D1 e D4 con lo stesso componente**, ed è lì che vive il '
      'beneficio di sicurezza vero, perché RI-02, RI-09, RI-16 e RI-18 si chiudono solo '
      'quando l’identità della persona attraversa la catena.'],
     [['Pro', 'Contro'],
      ['Una sola registrazione e un solo segreto presso IAM, sotto controllo di SIPO.',
       'È un componente nuovo da progettare, esercire e mantenere, con il percorso formale '
       'che ne consegue: manuale operativo, richiesta di risorse, collaudo.'],
      ['Risolve la propagazione ai back-end: i quarantaquattro emittenti diventano uno, e la '
       'revoca torna possibile.',
       '⚠️ **Se cade, nessuno entra.** Un componente sul percorso del login richiede alta '
       'affidabilità vera, non dichiarata.'],
      ['I back-end Java devono solo verificare una firma asimmetrica: è la cosa che il loro '
       'stack, pur datato, sa fare bene.',
       '⚠️ **Duplicherebbe msAuth**, se msAuth fa già questo. Si costruirebbe un secondo '
       'servizio di autenticazione dell’ente accanto a uno esistente.'],
      ['Potrebbe servire anche i front-end Angular, unificando vecchio e nuovo.',
       'L’effort è il più alto della scala, perché somma la fase 1 alla costruzione '
       'dell’emittente.']],
     'Kubernetes: un deployment senza stato, replicabile, con un oggetto Secret e una regola '
     'di uscita verso IAM. ⚠️ La sonda di prontezza non deve dipendere dalla '
     'raggiungibilità di IAM: un disservizio esterno non deve far riavviare il gateway.'),

    ('S4 — Convergenza sul servizio che già esiste',
     ['Non compare nelle analisi di partenza, ed è la ragione per cui va messa in fondo alla '
      'scala. La libreria Angular condivisa dell’ente, in assenza di gettone, rinvia a '
      '**/msAuth/api/v1/autenticazione/loginIAM**; il logout va a **/msAuth/api/v1/'
      'autenticazione/logout**. Il prefisso segue la convenzione dei microservizi dell’ente, '
      'l’interfaccia è versionata, e il profilo che restituisce contiene struttura, ufficio '
      'e un elenco di abilitazioni.',
      '⚠️ **Funzionalmente è S3, e qualcuno l’ha già costruito.** Un componente centrale che '
      'fa da interlocutore verso IAM ed emette alle applicazioni un proprio gettone con '
      'claim applicativi: è esattamente il ruolo dell’opzione C. Se così fosse, la decisione '
      'D1 non è «quale componente costruire» ma «adottare quello che l’ente già usa».',
      'Il profilo è peraltro già vicino a quello che serve: struttura e ufficio sono le '
      'nozioni che in SIPO si chiamano organizzazione e sede di municipio, e le abilitazioni '
      'sono la forma verso cui il catalogo delle funzionalità dovrebbe convergere.'],
     [['Pro', 'Contro'],
      ['Nessun componente nuovo da costruire né da esercire: costa un accertamento, non uno '
       'sviluppo.',
       '⚠️ **Tre incognite decidono se la strada regge** e nessuna è verificabile dal lato '
       'client: copre anche i dipendenti o solo i cittadini? il suo gettone può portare '
       'ruoli, aree e funzionalità con la granularità di SIPO? è spendibile verso i '
       'back-end?'],
      ['⚠️ **È l’unica soluzione che non crea un secondo impianto di autenticazione** '
       'accanto a quello che le applicazioni Angular già usano.',
       'Dipendenza da un servizio che SIPO non governa: tempi di intervento e priorità '
       'altrui sul percorso critico del login.'],
      ['Chiuderebbe D1 e D4 insieme, come S3, senza il costo di costruzione.',
       '⚠️ Nel codice della guardia che vi rinvia c’è il commento «manca codice ambito e '
       'applicazione»: chi l’ha scritta la dichiara incompleta.'],
      ['Fa convergere i trentacinque front-end Java e i micro-frontend Angular sulla stessa '
       'via di accesso, che è la direzione in cui l’ente si sta muovendo comunque.',
       'L’effort non è stimabile finché le incognite restano: potrebbe essere il minore '
       'della scala o richiedere un’estensione del servizio.']],
     'Kubernetes: nessun componente nuovo per SIPO. Va garantita la raggiungibilità del '
     'servizio dallo spazio dei nomi dei front-end e verificato che la sua disponibilità sia '
     'adeguata a reggere anche il carico di SIPO.'),
]


def main():
    if os.path.exists(DST):
        os.remove(DST)
    shutil.copy(SRC, DST)
    d = docx.Document(DST)
    fatti = []

    # la figura del raccordo scala di uno: la nuova scala la precede
    for p in d.paragraphs:
        if p.text.strip().startswith('Figura 4 —'):
            D.testo_di(p, re.sub(r'^Figura 4 —', 'Figura 5 —', p.text.strip()))
            fatti.append('figura del raccordo rinumerata 4 → 5')
            break

    ancora = D.h(d, 2, 'Che cosa l’integrazione chiude')

    def par(t, stile='Normal'):
        D.para(d, ancora._p, t, stile=stile)

    def tabella(righe, larghezze):
        t = D.tabella(d, ancora._p, righe, modello=d.tables[-1], larghezze=larghezze)
        return t

    par('Le soluzioni possibili, dalla più conservativa alla più coerente', 'Heading 2')
    par('Le decisioni del capitolo precedente dicono che cosa va scelto. Questo capitolo '
        'mette in fila **le soluzioni fra cui scegliere**, ordinate su un solo asse: da '
        'quella che conserva di più e sviluppa di meno a quella più coerente con '
        'l’architettura verso cui l’ente si sta muovendo. ⚠️ L’effort cresce lungo quell’asse '
        'ma **non in modo monotono**: l’ultima costa meno della penultima, ed è la ragione '
        'per cui l’ordinamento non è per costo.')
    par('Le soluzioni sono valutate contro i tre vincoli dichiarati dal committente, che non '
        'sono dettagli realizzativi ma criteri di scelta.')
    tabella(VINCOLI, [1.3, 5.2])

    d.add_paragraph()  # separatore prima della figura
    p = D.para(d, ancora._p, '')
    p.add_run().add_picture(os.path.join(IMG, 'iam_scala.png'), width=Inches(6.4))
    cap = D.para(d, ancora._p, 'Figura 4 — Le cinque soluzioni. L’altezza del gradino è la '
                               'coerenza architetturale, non l’effort.', corsivo=True)
    cap.runs[0].font.size = Pt(9)

    for titolo, prosa, prcontro, nota_k8s in SOLUZIONI:
        par(titolo, 'Heading 3')
        for t in prosa:
            par(t)
        tabella(prcontro, [3.25, 3.25])
        par(nota_k8s)

    par('Il confronto in una tabella', 'Heading 3')
    tabella(CONFRONTO, [1.7, 0.95, 0.95, 0.95, 0.95, 1.0])
    par('⚠️ **Due righe meritano di essere lette insieme**: «crea un secondo impianto» e '
        '«serve anche ai front-end Angular». Sono la stessa domanda vista da due lati, e '
        'distinguono S4 da tutte le altre. Se SIPO adotta una soluzione che serve soltanto i '
        'front-end Java, l’ente si ritrova due vie di accesso allo stesso IAM: due '
        'registrazioni, due segreti, due comportamenti al logout, e un operatore che nella '
        'stessa giornata le attraversa entrambe. È lo stesso errore, a vent’anni di '
        'distanza, che ha prodotto le due copie della libreria di profilazione.')

    par('La raccomandazione', 'Heading 3')
    par('**Prima di tutto S0, e subito**: non dipende da nessuna decisione, si fa in giorni e '
        'rimuove il rilievo più grave. Nessuna delle altre quattro lo include.')
    par('**Poi l’accertamento su S4**, che è la decisione con il rapporto più alto fra '
        'impatto e costo: tre domande al presidio che possiedono msAuth. Se il servizio '
        'copre i dipendenti, può portare la granularità dei profili di SIPO ed è spendibile '
        'verso i back-end, **è la soluzione**: chiude D1 e D4 insieme, senza costruire nulla, '
        'e fa convergere il vecchio e il nuovo.')
    par('**Se S4 non regge, S1 per la prima fase — dichiarando però fin d’ora che l’approdo '
        'è S3.** Presentare S1 come la soluzione significa farsi chiedere in seconda fase di '
        'costruire comunque l’emittente, e sembrare un cambio di piano. Presentare «S1 '
        'adesso, S3 come architettura» è una proposta sola, e più difendibile.')
    par('⚠️ **S2 non la proporrei allo stato attuale.** Non per preferenza fra fornitori, ma '
        'perché un componente che in caso di errore accetta asserzioni senza verificarne la '
        'firma non è collocabile sul percorso di autenticazione di un sistema che forma atti '
        'di stato civile. Se le tre risposte di PI-09 fossero rassicuranti, rientrerebbe '
        'nella valutazione al posto di S1.')
    par('Vale per tutte: **il codice dietro un’interfaccia** che separi la costruzione del '
        'reindirizzamento dalla gestione del ritorno. È ciò che rende la scelta reversibile, '
        'e quindi consente di cominciare prima che tutte le risposte siano arrivate.')
    fatti.append('capitolo delle soluzioni con cinque disamine, confronto e raccomandazione')

    # punti aperti nuovi
    t = D.trova_tabella(d, '#', 'Questione')
    for voce in (
        ('PI-17', 'Se il servizio di autenticazione usato dalle applicazioni Angular copra '
                  'anche le utenze dei dipendenti, con quale granularità di profilo e se il '
                  'gettone che emette sia verificabile dai back-end di SIPO. ⚠️ È '
                  'l’accertamento che decide fra S4 e le altre soluzioni.',
         'Presidio del servizio / Referenti SIPO'),
        ('PI-18', 'Se esista già una decisione d’ente sull’unificazione delle vie di accesso '
                  'fra applicazioni esistenti e nuove, che renderebbe la scelta non più solo '
                  'di SIPO.', 'Dipartimento'),
    ):
        D.clona_riga(t, voce)
    fatti.append('PI-17 e PI-18 aperti')

    for tab in d.tables:
        if tab.rows[0].cells[0].text.strip().lower().startswith('area organizzativa'):
            for r in tab.rows:
                v = {'Versione': '0.2',
                     'Documento': 'ANALISI_Identita-Profilazione-IAM_v0.2'
                     }.get(r.cells[0].text.strip())
                if v:
                    D.riscrivi_cella(r.cells[1], v)
            break
    D.storia(d, '02/10/2026', '0.2', 'Parte II — Soluzioni (nuovo) · Punti aperti',
             'Aggiunto il capitolo delle soluzioni possibili, ordinate dalla più '
             'conservativa alla più coerente con l’architettura di destinazione e valutate '
             'contro i tre vincoli dichiarati: front-end Angular, back-end Java, esercizio in '
             'Kubernetes. Cinque disamine con pro e contro — le tre delle analisi di partenza '
             'più il consolidamento senza integrazione e la convergenza sul servizio di '
             'autenticazione che le applicazioni Angular già usano, che le analisi non '
             'avevano considerato. Tabella di confronto e raccomandazione argomentata. Due '
             'punti aperti nuovi.')
    fatti.append('testata e storia aggiornate')

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
    print('\n'.join(' · ' + f for f in fatti))
    print('capitoli/tabelle/immagini:', D.riepilogo(DST))
    print('scritto:', os.path.relpath(DST, BASE))


if __name__ == '__main__':
    main()
