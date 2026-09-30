# -*- coding: utf-8 -*-
"""Genera «ANALISI_Front-End-Angular» — l'impostazione grafica e Angular del progetto.

Nasce da due fonti che non concordano: la **Proposta Tecnica** (Angular 21, Bootstrap Italia
2.18) e la **libreria condivisa** che il progetto deve usare (Angular 18.2.8, Bootstrap Italia
2.10). La decisione del committente è Angular 21: la libreria sale. Il documento lo dice, ne
misura il costo e non lo nasconde dietro una tabella di versioni.

⚠️ Perimetro: il front-end dell'integrazione ANSC. Le regole valgono per tutto il front-end,
ma gli esempi e le schermate sono quelli del pilota.

⚠️ Niente dati inventati: dove la fonte tace si scrive [DA VERIFICARE], come prescrive il
metodo di lavoro del workspace.

    /Library/Developer/CommandLineTools/usr/bin/python3 genera_frontend_angular.py
"""
import os
import shutil
import sys

import docx
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATE = os.path.join(BASE, 'Template documentale', 'template_DAD_roma-capitale.docx')
OUT = os.path.join(BASE, 'Documenti finali', 'ANALISI_Front-End-Angular_v0.2.docx')
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
TAGLIA_DA = 29


# ------------------------------------------------------------------ primitive

def _testo(par, s):
    if par.runs:
        par.runs[0].text = s
        for r in par.runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        par.add_run(s)


def apri():
    shutil.copyfile(TEMPLATE, OUT)
    d = docx.Document(OUT)
    body = d.element.body
    for ch in list(body.iterchildren())[TAGLIA_DA:]:
        if ch.tag != qn('w:sectPr'):
            body.remove(ch)
    for p in d.paragraphs:
        if '“Lorem Ipsum”' in p.text:
            _testo(p, '“Integrazione SIPO – ANSC”')
        elif p.style.name == 'Subtitle':
            _testo(p, 'Il front-end: impostazione grafica e Angular')
    return d


def h(d, liv, t):
    p = d.add_paragraph(style=f'Heading {liv}')
    p.add_run(t)
    return p


def par(d, t, stile='Normal'):
    p = d.add_paragraph(style=stile)
    for pezzo, grassetto in D.segmenta('', t):
        p.add_run(pezzo).bold = grassetto
    return p


def voce(d, testa, corpo):
    p = d.add_paragraph(style='List Paragraph')
    p.add_run(testa + ' ').bold = True
    for pezzo, grassetto in D.segmenta('', corpo):
        p.add_run(pezzo).bold = grassetto
    return p


def tab(d, righe, larghezze=None):
    t = d.add_table(rows=len(righe), cols=len(righe[0]))
    t.style = 'Table Grid'
    for i, r in enumerate(righe):
        for j, v in enumerate(r):
            cel = t.cell(i, j)
            cel.text = ''
            run = cel.paragraphs[0].add_run(str(v))
            run.bold = (i == 0)
            run.font.size = Pt(9)
    if larghezze:
        for j, w in enumerate(larghezze):
            for r in t.rows:
                r.cells[j].width = Inches(w)
    d.add_paragraph()
    return t


def figura(d, nome, pollici, didascalia):
    p = d.add_paragraph()
    p.add_run().add_picture(os.path.join(IMG, nome), width=Inches(pollici))
    c = d.add_paragraph()
    r = c.add_run(didascalia)
    r.italic = True
    r.font.size = Pt(9)
    return p


def mono(d, righe):
    for riga in righe:
        p = d.add_paragraph()
        r = p.add_run(riga)
        r.font.name = 'Courier New'
        r.font.size = Pt(8)
        p.paragraph_format.space_after = Pt(0)
    d.add_paragraph()


# ------------------------------------------------------------------ contenuti

GLOSSARIO = [
    ['Termine', 'Significato'],
    ['Micro-frontend', 'Applicazione autonoma, con il proprio ciclo di rilascio, che viene '
                       'caricata dentro una applicazione ospite e ne condivide le dipendenze.'],
    ['Shell (host)', 'L’applicazione che ospita i micro-frontend: governa le rotte di primo '
                     'livello, il layout comune e il caricamento della configurazione.'],
    ['Remote', 'Un micro-frontend, dal punto di vista della shell che lo carica.'],
    ['Module Federation', 'Il meccanismo di webpack con cui un remote pubblica moduli '
                          '(remoteEntry.js) e la shell li carica a runtime.'],
    ['Native Federation', 'L’equivalente indipendente da webpack, pensato per il builder '
                          'esbuild introdotto dalle versioni recenti di Angular.'],
    ['Libreria condivisa', 'mf-shared-library: il remote che pubblica design system, '
                           'componenti e servizi trasversali usati da tutti gli altri.'],
    ['Design system', 'L’insieme di regole visive e di componenti che rende coerenti le '
                      'applicazioni: qui Bootstrap Italia più il tema di Roma Capitale.'],
    ['Bootstrap Italia', 'Il design system della Pubblica Amministrazione italiana, curato da '
                         'Designers Italia, costruito su Bootstrap.'],
    ['Storybook', 'Lo strumento che pubblica i componenti come catalogo navigabile, ciascuno '
                  'con i propri stati ed esempi.'],
    ['Standalone', 'Il modo con cui Angular dichiara un componente autosufficiente, senza '
                   'bisogno di un NgModule che lo contenga.'],
    ['Sessione OTP', 'La sessione di quattro ore verso ANSC, aperta dal codice che l’ufficiale '
                     'genera sulla web app di ANSC. Non è l’autenticazione a SIPO.'],
]

RIFERIMENTI = [
    ['ID', 'Riferimento', 'Contenuto'],
    ['[F1]', 'Proposta_Tecnica_Angular.docx — Sistemi Informativi',
     'Proposta per lo sviluppo front-end (progetto Firma Certificati di Postazione): stack di '
     'riferimento, punti critici, domande aperte.'],
    ['[F2]', 'fsha_mf-shared-library — it.sistinf.roma-capitale:rc-fe-mf-shared-library:1.1.4.27',
     'La libreria condivisa: sorgenti, configurazione di build, design system, componenti.'],
    ['[F3]', 'ANALISI_Integrazione-ANSC_v3.21.docx',
     'L’analisi funzionale e tecnica dell’integrazione: requisiti, back-office, modello dati.'],
    ['[F4]', 'PROCEDURA_Formazione-Atto_SIPO-ANSC_v0.1.docx',
     'Il percorso dell’operatore in otto passi, da cui discende la mappa delle schermate.'],
    ['[F5]', 'Bootstrap Italia — Designers Italia',
     'Il design system della Pubblica Amministrazione su cui la libreria è costruita.'],
    ['[F6]', 'Naming_convention_X_API_v1.00.docx',
     'Lo standard aziendale per le API che il front-end consuma.'],
]

STACK = [
    ['Componente', 'Proposta Tecnica [F1]', 'Libreria condivisa [F2]', 'Baseline adottata'],
    ['Angular', 'v21', '18.2.8', '18.2.8 — quella della libreria'],
    ['Angular CDK', 'non dichiarato', '18.2.9', '18.2.9'],
    ['Bootstrap', 'v5.3.8', '5.2.3', '5.2.3, quella portata da Bootstrap Italia'],
    ['Bootstrap Italia', 'v2.18.2', '2.10.0', '2.10.0'],
    ['TypeScript', 'non dichiarato', '5.5.4', '5.5.4'],
    ['Node', 'non dichiarato', '≥ 20.18 (requisito dichiarato nel README)', '≥ 20.18'],
    ['Builder', 'non dichiarato', 'ngx-build-plus:browser 18 (webpack)', 'invariato'],
    ['Federazione', 'non dichiarata', '@angular-architects/module-federation 18.0.6',
     'invariata'],
    ['Autenticazione', 'da integrare con l’esistente', 'keycloak-angular 16 · keycloak-js 25',
     'Keycloak, come la libreria'],
    ['Catalogo componenti', 'non previsto', 'Storybook 8.5, pubblicato su /storybook',
     'Storybook, come la libreria'],
]

VERSIONI = [
    ['Versione', 'Rilascio', 'Fine supporto attivo', 'Fine supporto esteso (LTS)',
     'Stato a settembre 2026'],
    ['Angular 17', 'novembre 2023', 'maggio 2024', 'maggio 2025', 'fuori supporto'],
    ['Angular 18', 'maggio 2024', 'novembre 2024', 'novembre 2025',
     'fuori supporto — è la versione adottata'],
    ['Angular 19', 'novembre 2024', 'maggio 2025', 'maggio 2026', 'fuori supporto'],
    ['Angular 20', 'maggio 2025', 'novembre 2025', 'novembre 2026',
     'in supporto esteso, in scadenza'],
    ['Angular 21', 'novembre 2025', 'maggio 2026', 'maggio 2027', 'in supporto esteso'],
]

RISCHI_EOL = [
    ['Rischio', 'In che cosa consiste', 'Come lo si contiene'],
    ['Correzioni di sicurezza',
     'Sul ramo 18 non vengono più pubblicate correzioni. Se una vulnerabilità riguardasse '
     'Angular o una delle librerie allineate ad esso, non esisterebbe un aggiornamento '
     'ufficiale da applicare.',
     'Sorveglianza automatica delle vulnerabilità delle dipendenze a ogni costruzione, e una '
     'via di risalita già decisa in anticipo per il caso in cui serva.'],
    ['Irrigidimento progressivo dell’ecosistema',
     'Le librerie di contorno — catalogo dei componenti, client di autenticazione, calendario, '
     'editor, grafici, mappe — si allineano alle versioni correnti di Angular. Con il tempo '
     'aggiornarne una diventa impossibile senza salire.',
     'Congelare le versioni in una baseline dichiarata e non aggiornare le dipendenze senza '
     'ragione: ogni aggiornamento isolato avvicina il punto di rottura.'],
    ['Propagazione del vincolo alla piattaforma',
     'Angular 18 determina le versioni ammesse di Node e di TypeScript, che hanno a loro volta '
     'un proprio ciclo di vita. Il vincolo non resta nel codice: arriva alle immagini di '
     'costruzione e di esecuzione.',
     'Verificare il ciclo di vita di Node e TypeScript insieme a quello di Angular, non '
     'separatamente. [DA VERIFICARE: la data di fine supporto della linea di Node adottata]'],
    ['Crescita del costo di recupero',
     'Il debito non resta fermo: oggi separano tre versioni maggiori dalla corrente, fra un '
     'anno saranno cinque. Il costo non cresce in proporzione, perché a ogni salto si sommano '
     'quelli dell’ecosistema.',
     'Datare la decisione invece di lasciarla implicita, e riesaminarla a una scadenza fissata.'],
    ['Effetto di scala del modello federato',
     'La versione condivisa è un vincolo globale: il giorno in cui un solo applicativo avesse '
     'bisogno di salire, dovrebbero salire tutti insieme. È il rovescio del vantaggio che oggi '
     'la condivisione offre.',
     'Trattare il salto come un intervento di programma, con un proprio momento e un proprio '
     'budget, non come una attività di manutenzione di un singolo progetto.'],
    ['Distanza dagli strumenti e dalla documentazione',
     'Esempi, generatori di codice e materiale di riferimento si allineano alle versioni '
     'correnti: chi sviluppa incontra indicazioni che non valgono per la versione in uso.',
     'Fissare nella baseline anche le versioni degli strumenti di sviluppo, così che non siano '
     'le impostazioni locali a determinarle.'],
]

FAMIGLIE = [
    ['Famiglia', 'Componenti', 'N.'],
    ['Struttura e navigazione',
     'header · footer · navbar · menu · sidebar · recursive-sidebar · breadcrumb · '
     'layout-router-outlet · tabs-horizontal · tabs-horizontal-v2 · tabs-vertical · stepper · '
     'navigation-button', '13'],
    ['Presentazione dei dati',
     'table · table-toolbar · checkbox-table · grid · card-wrapper · accordion · carousel · '
     'badge · icon · image · map · pdf-viewer · charts (doughnut, barre impilate)', '14'],
    ['Elementi di modulo',
     'input · input-number · input-password · textarea · select · select-2v · '
     'select-autocomplete · multi-select-autoadd · checkbox · radio · picker · date-picker · '
     'daterange-picker · datetime-picker · time-picker · timerange-picker · otp · rich-text · '
     'upload · document-single-upload · upload-drag-drop', '21'],
    ['Azione e stato',
     'button · button-icon · toggle-icon · modal · spinner · notification-toast · '
     'notification-container', '7'],
    ['Stati eccezionali', 'error-boundary · file-not-found · under-construction', '3'],
    ['Classi astratte', 'abstract-chart · abstract-subscriptions-tracker', '2'],
    ['Totale', '', '60'],
]

SERVIZI = [
    ['Servizio esposto', 'A che cosa serve', 'Che cosa risolve'],
    ['AuthenticationService · AuthenticationGuard · AuthenticationIAMGuard',
     'Identità dell’operatore su Keycloak; i dati di sessione sono conservati nel browser sotto '
     'la chiave «auth» e includono struttura, ufficio e tributo.',
     'Il punto 3.1 della Proposta Tecnica: non si introduce un secondo meccanismo di '
     'autenticazione.'],
    ['AuthorizationService · AuthorizationGuard · AbilityService',
     'Modello a abilitazioni: una lista di stringhe sul profilo dell’operatore, con cui si '
     'filtrano voci di menu, rotte e azioni.',
     'Il punto 3.2: il modello dei permessi esiste già e va popolato, non progettato.'],
    ['ConfigService',
     'Legge un config.json servito accanto all’applicazione, con ripiego su environment.ts se '
     'il file manca.',
     'Il punto 3.3: quattro ambienti, un solo artefatto, nessun build per ambiente.'],
    ['HttpClientService · i tre intercettori',
     'Client HTTP comune, con intercettori per autenticazione, errori e indicatore di '
     'caricamento.',
     'Coerenza del trattamento degli errori e delle attese su tutte le applicazioni.'],
    ['ResponsiveService · BaseHrefService · NavigationFragmentService · LocalStorageService',
     'Punti di rottura, base href dei micro-frontend, frammenti di navigazione, memoria locale.',
     'Le necessità ricorrenti di una applicazione federata.'],
    ['EventBus · GlobalErrorHandler',
     'Comunicazione fra micro-frontend e raccolta centralizzata degli errori non gestiti.',
     'Il disaccoppiamento fra remote che non si conoscono fra loro.'],
]

SCHERMATE = [
    ['Schermata / passo', 'Componenti esistenti', 'Da costruire'],
    ['1 — Scelta dell’operazione dal menu', 'menu · navbar · breadcrumb', '—'],
    ['2 — Acquisizione del codice di sessione', 'otp · notification-toast · modal',
     'la maschera che consegna il codice al concentratore e mostra il tempo residuo'],
    ['3 — Compilazione dell’atto', 'i 21 elementi di modulo · accordion · grid',
     'i campi che ANSC richiede e SIPO non raccoglie'],
    ['4 — Ricerca degli intestatari in ANSC', 'select-autocomplete · table · modal', '—'],
    ['5 — Dati e documenti richiesti dall’UC', 'stepper · table · badge', '—'],
    ['6 — Caricamento dei documenti',
     'upload-drag-drop · document-single-upload · pdf-viewer',
     'le maschere di caricamento: l’area di stato civile non gestisce allegati'],
    ['7 — Deposito e firma', 'stepper · spinner · modal · notification-toast', '—'],
    ['8 — Atto formato', 'card-wrapper · notification-toast',
     'lo stato ANSC nelle maschere di ricerca e di dettaglio'],
    ['Back-office — supervisione',
     'table · table-toolbar · checkbox-table · tabs-horizontal · badge · modal', '—'],
    ['Back-office — notifiche', 'table · table-toolbar · modal · notification-toast', '—'],
    ['Back-office — configurazione', 'table · form-elements · accordion · tabs-vertical', '—'],
]

REQUISITI = [
    ['ID', 'Requisito', 'Nota'],
    ['RF-FE-1', 'Il front-end è realizzato come micro-frontend caricato da una shell, con la '
                'libreria condivisa come unica fonte di componenti e di stile.',
     'Vale per tutte le applicazioni del progetto.'],
    ['RF-FE-2', 'Nessuna schermata definisce colori, tipografia o spaziature proprie: usa le '
                'utility del tema.',
     'Se una utility manca si aggiunge alla libreria, non alla schermata.'],
    ['RF-FE-3', 'Nessun componente della libreria viene riscritto localmente; le varianti si '
                'ottengono estendendo il componente condiviso.',
     'È ciò che distingue un design system da una sua copia per progetto.'],
    ['RF-FE-4', 'L’identità dell’operatore è quella di Keycloak; la sessione OTP verso ANSC è '
                'cosa distinta e non si confonde con essa.',
     'Due sessioni, due scadenze, due conseguenze diverse quando cadono.'],
    ['RF-FE-5', 'Il front-end non raggiunge mai ANSC: ogni chiamata passa dal concentratore.',
     'Discende dal fatto che la chiave privata e l’OTP risiedono nel concentratore [F3].'],
    ['RF-FE-6', 'La visibilità di voci di menu, rotte e azioni discende dalle abilitazioni '
                'dell’operatore.',
     'Il servizio esiste; l’elenco delle abilitazioni del dominio stato civile è da definire.'],
    ['RF-FE-7', 'La configurazione dei quattro ambienti è letta a runtime; l’artefatto è uno '
                'solo.', 'Nessuna ricompilazione per ambiente.'],
    ['RF-FE-8', 'Le maschere mostrano il tempo residuo della sessione ANSC e avvisano prima '
                'che scada.', 'Soglia di guardia proposta: 15 minuti [F3].'],
    ['RF-FE-9', 'Ogni componente nuovo entra nella libreria con la propria storia di Storybook.',
     'La storia è il modo in cui il componente si mostra a chi non l’ha scritto.'],
    ['RF-FE-10', 'Le maschere sono utilizzabili con la sola tastiera e conformi al livello di '
                 'accessibilità richiesto alla Pubblica Amministrazione.',
     '[DA VERIFICARE: livello applicabile e chi ne conduce la verifica]'],
]

RNF = [
    ['ID', 'Requisito', 'Valore'],
    ['RNF-FE-1', 'Dimensione del pacchetto iniziale', 'Il budget della libreria è oggi fissato '
                 'a 2 MB come errore di build: il margine è scarso e va sorvegliato.'],
    ['RNF-FE-2', 'Browser supportati', '[DA VERIFICARE: browser e versioni in uso sulle '
                 'postazioni degli uffici]'],
    ['RNF-FE-3', 'Tempo di risposta percepito', 'Ogni operazione che supera la soglia di attesa '
                 'mostra l’indicatore di caricamento comune; nessuna schermata resta muta.'],
    ['RNF-FE-4', 'Accessibilità', '[DA VERIFICARE: livello richiesto]. Bootstrap Italia nasce '
                 'conforme; la conformità si perde con le personalizzazioni, non con la base.'],
    ['RNF-FE-5', 'Lingua', 'Italiano. I messaggi di errore predefiniti della libreria sono già '
                 'in italiano.'],
    ['RNF-FE-6', 'Compatibilità con la libreria', 'Shell e micro-frontend condividono una sola '
                 'istanza di Angular: la versione deve coincidere ovunque.'],
]

RISCHI = [
    ['Classe', 'Rischio', 'Perché', 'Mitigazione proposta'],
    ['A — Alta', 'La versione adottata è fuori supporto',
     'Angular 18 ha concluso il supporto esteso; le correzioni, comprese quelle di sicurezza, '
     'non vengono più pubblicate su quel ramo, e l’ecosistema si allinea alle versioni '
     'correnti.',
     'Il capitolo «Il ciclo di vita della versione adottata» espone le misure che contengono '
     'il rischio senza rimettere in discussione la scelta.'],
    ['A — Alta', 'La dipendenza da un pacchetto di terzi non istituzionale',
     'Il pacchetto test-library-frankmd93 fornisce i tipi portanti — AuthData, HttpResponse, '
     'AbstractRemoteCall, AppConfig, NavbarItem — ed è importato in oltre venti punti.',
     'Accertare chi lo pubblica e dove stanno i sorgenti; se non è governato dal Comune, '
     'prevederne l’assorbimento dentro la libreria.'],
    ['B — Media', 'L’assenza di test automatici',
     'Nella libreria non esiste alcun file di test. Un componente condiviso senza test rende '
     'ogni aggiornamento una verifica manuale su tutti i progetti che lo usano.',
     'Introdurre i test sui componenti toccati dal progetto, non su tutti in una volta: '
     'sono anche la verifica del giorno in cui la libreria salirà di versione.'],
    ['B — Media', 'L’allineamento delle dipendenze di contorno',
     'Catalogo dei componenti, client di autenticazione, calendario, editor, grafici e mappe '
     'sono allineati alla versione adottata: aggiornarne una isolatamente può romperne la '
     'compatibilità.',
     'Congelare le versioni in una baseline dichiarata e verificata alla costruzione.'],
    ['B — Media', 'Prefissi dei selettori non uniformi',
     'Convivono app-rc- (35 componenti) e app-mf- (6): in un contesto federato il prefisso è '
     'ciò che evita le collisioni fra remote.',
     'Fissare il prefisso per i componenti nuovi e uniformare gli esistenti quando li si tocca.'],
    ['C — Bassa', 'Configurazioni di ambiente nei sorgenti',
     'Il Dockerfile porta l’indirizzo del proxy aziendale e il file .npmrc porta le credenziali '
     'del registry interno; la configurazione di nginx consente qualunque origine.',
     'Spostare indirizzi e credenziali nella configurazione di esecuzione; restringere le '
     'origini ammesse.'],
]

TEST = [
    ['Tipologia', 'Che cosa verifica', 'Strumento'],
    ['Unitari sui componenti', 'Il comportamento di un componente isolato: stati, validazione, '
                               'eventi emessi.', 'Karma, già configurato nella libreria'],
    ['Visivi sul catalogo', 'Che il componente si presenti come deve in ciascuno dei suoi '
                            'stati.', 'Storybook, già in esercizio'],
    ['Di integrazione fra remote', 'Che la shell carichi i micro-frontend e che la libreria sia '
                                   'condivisa in una sola istanza.', 'da definire'],
    ['Percorso completo', 'Gli otto passi della formazione dell’atto, dal menu alla firma.',
     'da definire — richiede un ambiente con il concentratore'],
    ['Accessibilità', 'Navigazione da tastiera, contrasto, etichette.',
     '[DA VERIFICARE: strumento e livello]'],
]

OPEN_POINT = [
    ['#', 'Questione', 'Owner'],
    ['OP-FE-1', 'Chi governa la libreria condivisa e con quali tempi accoglie una modifica: '
                'serve ad altri progetti, e il progetto ANSC non può essere l’unico a decidere.',
     'Cliente / Sistemi Informativi'],
    ['OP-FE-2', 'Data di riesame della scelta della versione di Angular, e occasione a cui '
                'legarla (fine del pilota, aggiornamento della libreria, esigenza di un altro '
                'applicativo).', 'Cliente / Sistemi Informativi'],
    ['OP-FE-3', 'Natura, titolarità e sorgenti del pacchetto test-library-frankmd93.',
     'Sistemi Informativi'],
    ['OP-FE-4', 'Livello di accessibilità richiesto, strumento di verifica e responsabile.',
     'Cliente'],
    ['OP-FE-5', 'Elenco delle abilitazioni del dominio stato civile, da cui discende la '
                'visibilità di rotte e azioni.', 'Cliente'],
    ['OP-FE-6', 'Browser e postazioni supportati negli uffici.', 'Cliente'],
    ['OP-FE-7', 'Disegno grafico delle schermate nuove: oggi esistono soltanto gli schizzi '
                'funzionali dell’analisi, che non sono un progetto grafico.', 'Analisi / Cliente'],
    ['OP-FE-8', 'Perimetro e ordine della migrazione delle maschere di stato civile oggi in '
                'Thymeleaf: il presente documento copre il pilota, non l’intero front-end.',
     'Cliente'],
    ['OP-FE-9', 'Come si procede se una vulnerabilità riguardasse la versione adottata, per la '
                'quale non sono più pubblicate correzioni: chi decide e con quale percorso.',
     'Cliente / Sistemi Informativi'],
    ['OP-FE-10', 'Fine supporto della linea di Node e di TypeScript ammesse dalla versione '
                 'adottata, che determinano le immagini di costruzione e di esecuzione.',
     'Sistemi Informativi'],
]


COPERTINA = [
    ('Area Organizzativa', 'Dipartimento Trasformazione Digitale'),
    ('RTI', 'IBM, TIM, Sistemi Informativi, Leonardo, Deloitte, Webgenesys'),
    ('Società', 'Sistemi Informativi S.r.l.'),
    ('Contratto Esecutivo', 'CIG B9DA959E80'),
    ('AQ', 'CIG A02590F330 - Accordo Quadro avente ad oggetto servizi applicativi'),
    ('Progetto', 'Integrazione SIPO – ANSC'),
    ('Data consegna', '18/09/2026'),
    ('Versione', '0.2'),
    ('Documento', '[codice documento da assegnare]'),
    ('N. Pagine', '[da assegnare]'),
    ('Codice Area Applicativa', '06'),
    ('Codice Asset', '[da assegnare]'),
]

STORIA = [
    ('18/09/2026', '0.1', 'Tutti',
     'Prima stesura, redatta assumendo Angular 21 come indicato dalla proposta tecnica.'),
    ('18/09/2026', '0.2', 'Tecnologie · Architettura · Ciclo di vita della versione · '
                          'Classi di rischio · Punti aperti',
     'Recepita la scelta del committente di adottare **Angular 18**, la versione della libreria '
     'condivisa, per compatibilità con il patrimonio applicativo esistente. Rimosso il capitolo '
     'sull’adeguamento a Angular 21 e introdotto il capitolo «Il ciclo di vita della versione '
     'adottata», con il quadro delle versioni, i rischi che la scelta comporta e le misure che '
     'li contengono senza rimetterla in discussione.'),
]


def intestazioni(d):
    """Riempie le due tabelle di copertina del modello."""
    t = d.tables[0]
    atteso = [e for e, _ in COPERTINA]
    for riga in t.rows:
        etichetta = riga.cells[0].text.strip()
        if etichetta in atteso:
            D.riscrivi_cella(riga.cells[1], dict(COPERTINA)[etichetta])
    s = d.tables[1]
    for i, riga in enumerate(STORIA, start=1):
        for cella, valore in zip(s.rows[i].cells, riga):
            D.riscrivi_cella(cella, valore.replace('**', ''))


# ------------------------------------------------------------------ stesura

def costruisci():
    d = apri()

    # ═══════════════════════════════════════════════ 1. Scopo
    h(d, 1, 'Scopo del documento')
    par(d, 'Il presente documento stabilisce come si realizza il front-end dell’integrazione '
           'fra SIPO e ANSC: con quale tecnologia, dentro quale architettura, secondo quale '
           'design system e con quali regole di lavoro. Nasce da due fonti — la proposta '
           'tecnica per lo sviluppo front-end [F1] e la libreria grafica che il progetto deve '
           'adottare [F2] — e dalla necessità di conciliarle, perché non concordano su un '
           'punto che decide tutto il resto: la versione di Angular.')
    par(d, 'Il perimetro è il front-end dell’integrazione ANSC: le maschere che servono a '
           'formare un atto e a depositarlo, quelle per caricare i documenti, il back-office '
           'di supervisione, delle notifiche e della configurazione. **Le regole valgono però '
           'per tutto il front-end del progetto**: sono scritte una volta qui perché il pilota '
           'è il primo luogo in cui si applicano e si verificano, non perché valgano solo lì.')
    par(d, '⚠️ Il documento non è un progetto grafico. Non contiene tavole di disegno né '
           'prototipi navigabili: stabilisce l’impostazione — che cosa si usa, che cosa non si '
           'riscrive, dove si interviene — e mappa le schermate sui componenti che già '
           'esistono. Il disegno delle schermate nuove resta un punto aperto.')

    h(d, 2, 'Glossario')
    tab(d, GLOSSARIO, [1.7, 4.6])
    h(d, 2, 'Riferimenti')
    tab(d, RIFERIMENTI, [0.6, 2.3, 3.4])

    # ═══════════════════════════════════════════════ 2. Contesto
    h(d, 1, 'Contesto di riferimento della Soluzione')
    par(d, 'Il front-end di SIPO è oggi costituito da **trentacinque moduli Spring Boot che '
           'servono pagine con Thymeleaf**, per un totale di circa **milleseicentottanta '
           'template HTML**. Le pagine sono composte dal server, la sessione è del server, la '
           'navigazione è una successione di richieste HTTP, e una tendina si riempie con una '
           'query eseguita mentre la pagina si costruisce.')
    par(d, 'Il passaggio ad Angular non è un cambio di aspetto. Sposta il rendering nel '
           'browser, trasforma i back-end in interfacce applicative, sostituisce la sessione '
           'del server con un token, e affida al browser il compito di tenere lo stato fra una '
           'schermata e l’altra. ⚠️ **Ne discende che cose oggi immediate diventano un '
           'contratto da progettare**: la tendina degli stati esteri, che oggi è una query, '
           'diventa una chiamata a un servizio che qualcuno deve esporre, versionare e '
           'documentare.')
    par(d, 'Questo documento non decide se e quando migrare l’intero front-end: è una '
           'questione di programma che eccede l’integrazione ANSC ed è registrata fra i punti '
           'aperti. Stabilisce però che **le parti nuove nascono in Angular**, perché nascere '
           'in Thymeleaf significherebbe scrivere oggi ciò che andrà riscritto domani, e '
           'perché le funzioni che servono all’integrazione — il caricamento dei documenti, il '
           'tempo residuo di una sessione, una worklist che si aggiorna — sono esattamente '
           'quelle che una pagina composta dal server fa male.')

    h(d, 2, 'Le due fonti e il loro disaccordo')
    par(d, 'La proposta tecnica [F1] è stata redatta per un altro progetto — la firma dei '
           'certificati di postazione — e il presente documento la usa per il metodo e per i '
           'punti critici che solleva, non per il contenuto. I punti critici sono però gli '
           'stessi che si porrebbero qui, ed è utile notare che **quattro dei sei hanno già '
           'risposta nella libreria**: l’integrazione con l’autenticazione esistente, il '
           'modello dei permessi, la molteplicità degli ambienti e la conformità a un design '
           'system. La proposta si chiedeva anche se usare Bootstrap o Bootstrap Italia e se '
           'esistesse un design system formalizzato: esiste, ed è Bootstrap Italia con il tema '
           'di Roma Capitale.')
    par(d, 'Restano due punti che la libreria non risolve e che questo documento affronta: '
           'l’estrazione di dati che a database non ci sono e l’adeguamento del modello dati. '
           'Sono questioni di back-end, non di front-end, e in questo progetto hanno il loro '
           'corrispettivo nei campi che ANSC richiede e SIPO non raccoglie.')
    par(d, '⚠️ **Il disaccordo vero è sulla versione.** La proposta dichiara Angular 21, '
           'Bootstrap 5.3.8 e Bootstrap Italia 2.18.2; la libreria è ad Angular 18.2.8, '
           'Bootstrap 5.2.3 e Bootstrap Italia 2.10.0. Non è uno scostamento di targa: la '
           'libreria è caricata a runtime con le dipendenze dichiarate come singleton a '
           'versione stretta, il che significa che **shell e micro-frontend condividono una '
           'sola istanza di Angular e la versione deve coincidere ovunque**. Le due versioni '
           'non possono convivere nella stessa pagina.')
    par(d, '**La decisione del committente è di adottare Angular 18**, cioè la versione della '
           'libreria condivisa. La ragione è la compatibilità con il patrimonio applicativo da '
           'cui il progetto eredita parte delle funzionalità: la libreria non serve soltanto '
           'questo progetto, e allinearla a una versione diversa comporterebbe muovere insieme '
           'tutti gli applicativi che la caricano. È un vincolo reale e la scelta lo rispetta; '
           'per il progetto significa poter cominciare senza dipendere da un intervento che non '
           'governa.')
    par(d, 'La scelta ha però un costo, che non riguarda il funzionamento ma il tempo: la '
           'versione adottata ha concluso il proprio ciclo di supporto. Il capitolo «Il ciclo '
           'di vita della versione adottata» lo espone per intero — non per rimettere in '
           'discussione la decisione, ma perché una scelta di questo tipo si governa solo se è '
           'dichiarata.')

    # ═══════════════════════════════════════════════ 3. Stakeholder
    h(d, 1, 'Stakeholder')
    par(d, 'Il front-end dell’integrazione serve quattro figure, che usano schermate diverse e '
           'hanno bisogni diversi.')
    voce(d, 'Ufficiale di stato civile.', 'Forma gli atti. È l’unico che possa firmare e '
            'l’unico che possa aprire una sessione verso ANSC, perché la apre con la propria '
            'identità digitale. Lavora nelle maschere di SIPO e incontra ANSC come passo di '
            'finalizzazione.')
    voce(d, 'Operatore di sportello o di municipio.', 'Compila gli atti e prepara le pratiche. '
            'Può arrivare fino alla soglia del deposito ma non oltre.')
    voce(d, 'Amministratore del back-office.', 'Governa la configurazione, le versioni della '
            'configurazione e i dizionari; sorveglia gli atti non conclusi.')
    voce(d, 'Archivista.', 'Lavora le notifiche che riguardano atti cartacei e le comunicazioni '
            'destinate all’archivio. ⚠️ È una figura che le maschere di SIPO oggi non '
            'conoscono, e che il flusso in ingresso introduce.')

    h(d, 2, 'Caratteristiche di accesso per utenti interni')
    par(d, 'Tutte le figure sopra sono utenti interni, autenticati su Keycloak. La visibilità '
           'di rotte, voci di menu e azioni discende dalle **abilitazioni** presenti nel '
           'profilo: la libreria offre già il servizio che filtra gli elementi in base a esse, '
           'e le guardie che proteggono le rotte. ⚠️ L’elenco delle abilitazioni del dominio '
           'stato civile non è ancora definito ed è registrato come punto aperto.')
    par(d, '⚠️ **Due autenticazioni, da non confondere.** L’accesso a SIPO è quello di '
           'Keycloak e dura quanto la giornata di lavoro. La sessione verso ANSC è un’altra '
           'cosa: nasce da un codice che l’ufficiale genera sulla web app di ANSC con smart '
           'card o identità digitale, dura quattro ore, e serve soltanto per le operazioni che '
           'toccano la piattaforma nazionale. Un operatore autenticato a SIPO può non avere '
           'alcuna sessione ANSC, e questo è normale.')

    h(d, 2, 'Caratteristiche di accesso per utenti esterni')
    par(d, 'Il perimetro dell’integrazione non prevede accesso di utenti esterni: il cittadino '
           'non entra in queste schermate. Il front-end non espone quindi alcuna area pubblica.')

    h(d, 2, 'Criteri di riservatezza delle informazioni')
    par(d, 'Le schermate trattano dati personali e dati relativi a eventi di stato civile. Ne '
           'discendono tre regole per il front-end: non si conservano dati di atto nella '
           'memoria del browser oltre la durata della schermata; il registro delle chiamate '
           'che il browser produce non contiene dati personali; e il codice di sessione ANSC '
           'non viene mai scritto nella memoria locale, perché è una credenziale.')
    return d


def parte_seconda(d):
    # ═══════════════════════════════════════════════ 4. Ambienti e strumenti
    h(d, 1, 'Ambienti e Strumenti')
    h(d, 2, 'Tecnologie Utilizzate')
    par(d, 'La tabella mette a confronto ciò che la proposta dichiara, ciò che la libreria è '
           'oggi e la baseline che si adotta.')
    tab(d, STACK, [1.3, 1.5, 1.8, 1.7])
    par(d, 'La baseline coincide dunque con la libreria, e questo ha un effetto immediato e '
           'positivo: **non c’è nulla da adeguare prima di cominciare**. Il builder resta '
           'quello basato su webpack, che è ciò che permette la configurazione di federazione; '
           'le novantanove esposizioni restano come sono; le dipendenze di contorno sono già '
           'allineate fra loro e collaudate insieme.')
    par(d, '⚠️ **La baseline va però dichiarata e verificata, non lasciata implicita.** Le '
           'versioni della tabella sono quelle con cui la libreria è stata costruita e '
           'collaudata; un ambiente di sviluppo che ne usasse altre — una versione di Node '
           'diversa, uno strumento aggiornato per conto proprio — produrrebbe differenze '
           'difficili da ricondurre alla causa. Si propone che l’elenco sia verificato alla '
           'costruzione, e non affidato alla configurazione delle singole postazioni.')

    h(d, 2, 'Ambienti')
    par(d, 'Gli ambienti sono quattro — sviluppo, collaudo, pre-produzione e produzione — e la '
           'libreria li risolve senza moltiplicare gli artefatti: il servizio di configurazione '
           'legge all’avvio un file **config.json** servito accanto all’applicazione, e ripiega '
           'sulle costanti compilate solo se il file manca. Ne discende che **si costruisce una '
           'volta e si promuove lo stesso pacchetto** da un ambiente all’altro, cambiando il '
           'file di configurazione. È la risposta al punto 3.3 della proposta tecnica.')

    h(d, 2, 'Distribuzione')
    par(d, 'La libreria si distribuisce come immagine contenitore: il pacchetto viene costruito, '
           'servito da nginx, e accanto ad esso viene pubblicato il catalogo dei componenti '
           'all’indirizzo /storybook. L’artefatto è versionato su Nexus come componente Maven — '
           'oggi alla versione 1.1.4.27 — e **la versione dell’artefatto è il contratto**: in un '
           'sistema federato è ciò che dice a un micro-frontend quale libreria sta caricando. '
           'Il numero dichiarato nel file di pacchetto npm è invece fermo al valore iniziale e '
           'non va usato come riferimento.')
    par(d, '⚠️ L’immagine porta cablato l’indirizzo del proxy aziendale e il file di '
           'configurazione del registro npm contiene le credenziali di accesso: entrambe sono '
           'informazioni di ambiente e andrebbero passate all’esecuzione, non scritte nei '
           'sorgenti. È registrato fra i rischi.')

    h(d, 2, 'Strumenti di qualità')
    par(d, 'La libreria porta già linting, formattazione automatica e controlli prima della '
           'consegna del codice. ⚠️ **Non porta test**: non esiste alcun file di test nei '
           'sorgenti. Per una libreria che altri progetti caricano a runtime è il rischio '
           'principale, ed è trattato nel capitolo sulle strategie di test.')

    # ═══════════════════════════════════════════════ 5. Architettura
    h(d, 1, 'Architettura di Riferimento della Soluzione')
    h(d, 2, 'Il modello a micro-frontend')
    par(d, 'L’applicazione non è un blocco unico. Una **shell** governa le rotte di primo '
           'livello, il layout comune e il caricamento della configurazione; dentro di essa '
           'vengono caricati a runtime i **micro-frontend**, ciascuno con il proprio ciclo di '
           'rilascio. La **libreria condivisa** è essa stessa un micro-frontend, ma di natura '
           'diversa: non porta schermate, porta ciò che tutti usano — il design system, i '
           'componenti, il client HTTP con i suoi intercettori, i servizi di autenticazione, di '
           'autorizzazione e di configurazione.')
    figura(d, 'fe_architettura.png', 6.3,
           'L’architettura del front-end. Le frecce tratteggiate sono dipendenze dalla libreria '
           'condivisa; le continue sono chiamate. Il browser non raggiunge mai ANSC.')
    par(d, 'Per il perimetro dell’integrazione si prevedono **tre micro-frontend**: le maschere '
           'di stato civile, la parte di integrazione ANSC (finalizzazione, documenti, '
           'sessione) e il back-office. La suddivisione non è un dettaglio implementativo: '
           'segue i tre gruppi di utenti e i tre ritmi di rilascio. Il back-office cambia '
           'quando cambia la configurazione, cioè spesso; le maschere di stato civile cambiano '
           'quando cambia la normativa, cioè di rado.')

    h(d, 2, 'La federazione e il vincolo di versione')
    par(d, 'Oggi la libreria pubblica i propri moduli con Module Federation su webpack e ne '
           'espone **novantanove**: intercettori, servizi, componenti e moduli. ⚠️ Una chiave è '
           'dichiarata due volte: è innocuo, ma dice che quel file non viene riletto. Le '
           'dipendenze sono dichiarate come condivise in **singola istanza e a versione '
           'stretta**, con due sole eccezioni.')
    par(d, 'Questa impostazione ha una conseguenza che va compresa prima di scegliere la '
           'versione di Angular, e non dopo: **non si possono mescolare versioni**. Se shell e '
           'libreria fossero su versioni diverse il caricamento fallirebbe; se si allentasse il '
           'vincolo per farlo funzionare, si avrebbero due istanze di Angular nella stessa '
           'pagina, con due sistemi di iniezione delle dipendenze e due rilevatori di '
           'cambiamento che non si parlano. Non è una configurazione da tentare.')
    par(d, 'Adottando la versione della libreria il vincolo è soddisfatto all’origine, e il '
           'meccanismo resta quello in esercizio: nessuna esposizione da riportare, nessun '
           'cambio di builder. ⚠️ Va però tenuto presente che il legame è **reciproco e '
           'permanente**: non solo il progetto non può salire da solo, ma nemmeno la libreria '
           'può farlo senza portare con sé tutti i suoi consumatori. È la ragione per cui il '
           'giorno in cui la versione dovrà cambiare sarà un intervento di programma e non di '
           'progetto — e per cui conviene saperlo ora.')

    h(d, 2, 'Autenticazione e sessione')
    par(d, 'L’identità dell’operatore è quella di Keycloak: la libreria porta il client, il '
           'servizio che espone i dati di sessione e le guardie che proteggono le rotte. I dati '
           'di sessione comprendono, oltre all’utente, la **struttura, l’ufficio e il tributo** '
           'di appartenenza: sono i valori con cui il front-end sa a quale contesto '
           'organizzativo l’operatore appartiene.')
    par(d, '⚠️ **La sessione verso ANSC è un’altra cosa e il front-end la tratta come tale.** '
           'Non è un accesso: è un codice temporaneo che l’ufficiale genera altrove e consegna '
           'a SIPO, che lo inoltra al concentratore. Il front-end non lo conserva, non lo '
           'firma, non lo usa per chiamare ANSC — non chiama ANSC affatto. Ciò che deve fare è '
           'più semplice e più visibile: **offrire la maschera con cui il codice si consegna, '
           'mostrare il tempo residuo e avvisare prima che scada**, con una soglia di guardia '
           'sotto la quale conviene rinnovare invece di iniziare una operazione lunga.')

    h(d, 2, 'Autorizzazione')
    par(d, 'Il modello è a **abilitazioni**: una lista di stringhe nel profilo dell’operatore. '
           'La libreria offre il servizio che filtra un insieme di elementi confrontando le '
           'abilitazioni richieste con quelle possedute, e le guardie che applicano lo stesso '
           'criterio alle rotte. È un modello semplice e adeguato; ciò che manca non è il '
           'meccanismo ma il **vocabolario**: quali abilitazioni esistano nel dominio dello '
           'stato civile, e quale azione ciascuna consenta.')
    par(d, '⚠️ Va notato che per l’integrazione ANSC esiste una seconda dimensione, che le '
           'abilitazioni non colgono: **la firma**. Chi possa firmare un atto non è una '
           'proprietà del profilo applicativo ma dell’ordinamento, ed è già registrata come '
           'questione aperta nell’analisi. Il front-end non deve risolverla: deve però non '
           'dare per scontato che chi vede il pulsante possa premerlo.')

    h(d, 2, 'Gli intercettori e il trattamento degli errori')
    par(d, 'Ogni chiamata passa dal client HTTP della libreria e attraversa tre intercettori: '
           'quello che aggiunge le credenziali, quello che traduce gli errori e quello che '
           'accende l’indicatore di attesa. È il punto in cui il comportamento diventa uniforme '
           'senza che ogni schermata debba ricordarsene.')
    par(d, 'Per l’integrazione questo comporta una regola: **gli errori che vengono da ANSC non '
           'si mostrano così come sono**. Il concentratore li traduce in una forma comprensibile '
           'e il front-end li presenta con il messaggio che la configurazione prevede per quel '
           'campo. Mostrare all’operatore il codice di errore della piattaforma nazionale '
           'significa chiedergli di fare un lavoro che spetta alla configurazione.')

    h(d, 2, 'I servizi che la libreria mette a disposizione')
    tab(d, SERVIZI, [2.0, 2.3, 2.0])
    return d


def parte_terza(d):
    # ═══════════════════════════════════════════════ 6. Flussi in uscita
    h(d, 1, 'Flussi informativi in uscita')
    par(d, 'Il front-end parla con tre interlocutori, e con nessun altro.')
    voce(d, 'I back-end di SIPO.', 'Per tutto ciò che riguarda l’atto: caricarlo, salvarlo, '
            'cercarlo. Sono le interfacce che sostituiscono le pagine composte dal server.')
    voce(d, 'Il concentratore.', 'Per tutto ciò che riguarda ANSC: consegna del codice di '
            'sessione, pre-verifica, ricerca del soggetto, deposito, firma, notifiche. Le '
            'operazioni sono quelle del contratto del componente [F6].')
    voce(d, 'Il componente dei dizionari.', 'Per le decodifiche, quando servono al back-office '
            'o alla diagnosi. Le maschere ordinarie leggono invece i dizionari dalla base dati, '
            'per la scelta motivata nell’analisi [F3].')
    par(d, '⚠️ **Non parla con ANSC.** È la regola più importante di tutto il capitolo e '
           'discende dall’architettura: la chiave privata del certificato e il codice di '
           'sessione risiedono nel concentratore, che costruisce e firma i token. Un front-end '
           'che chiamasse ANSC dovrebbe avere quelle credenziali nel browser, e non le avrà mai.')

    # ═══════════════════════════════════════════════ 7. Design system
    h(d, 1, 'Il design system')
    par(d, 'La domanda che la proposta tecnica lasciava aperta — se esista un design system '
           'formalizzato — ha risposta affermativa, e la risposta è già scritta nella libreria. '
           'Il design system è **Bootstrap Italia**, cioè il design system della Pubblica '
           'Amministrazione italiana, personalizzato con il tema di Roma Capitale.')

    h(d, 2, 'La catena del tema')
    figura(d, 'fe_tema.png', 6.3,
           'La catena del tema: si personalizza in un punto solo, e ciò che sta a valle eredita.')
    par(d, 'La catena ha cinque anelli e una sola regola: **si interviene su un anello solo**. '
           'Bootstrap Italia non si modifica, perché è ciò che garantisce la conformità alle '
           'linee guida. La personalizzazione è un file, e contiene poche righe: il colore '
           'primario e le correzioni di comportamento. Le utility del tema si estendono quando '
           'manca qualcosa. I componenti si usano. Le schermate non tematizzano nulla.')

    h(d, 2, 'Il tema di Roma Capitale')
    par(d, 'Il colore primario è **#8E001C**, il rosso del Comune, con quattro gradazioni; '
           'accanto ad esso sono definite altre sei famiglie semantiche — secondario, '
           'informazione, successo, avviso, errore e una scala di grigi a dieci passi. La '
           'tipografia è quella di Designers Italia: **Titillium Web** per il testo, **Lora** '
           'per i titoli editoriali, **Roboto Mono** per il monospaziato, servite come risorse '
           'dell’applicazione e non prelevate da servizi esterni — il che è anche una scelta '
           'corretta rispetto alla protezione dei dati.')
    par(d, 'Oltre al colore, il tema definisce venti gruppi di utility — spaziature, '
           'dimensioni, disposizione a righe e colonne, griglia, punti di rottura, visibilità, '
           'posizione, bordi, troncamento del testo — e otto correzioni di comportamento su '
           'componenti nativi. ⚠️ **È la ragione per cui una schermata non ha bisogno di CSS '
           'proprio**: se una cosa non si ottiene con le utility esistenti, manca una utility, '
           'e la si aggiunge dove stanno le altre.')

    h(d, 2, 'L’inventario dei componenti')
    par(d, 'La libreria contiene **sessanta componenti**, di cui due astratti, raggruppabili in '
           'sei famiglie. Sono componenti autosufficienti, con i moduli dichiarati al proprio '
           'interno; i moduli tradizionali che sopravvivono servono alla compatibilità con chi '
           'li importava prima.')
    tab(d, FAMIGLIE, [1.5, 4.1, 0.5])
    par(d, 'Tre osservazioni utili al progetto. **La prima**: gli elementi di modulo sono '
           'ventuno e coprono l’intero repertorio che le maschere di stato civile richiedono, '
           'comprese quattro varianti di selezione e sei di data e ora. **La seconda**: esiste '
           'già un componente per il **codice usa e getta**, che è esattamente ciò che serve '
           'alla consegna del codice di sessione ANSC. **La terza**: esistono il visualizzatore '
           'di PDF e tre componenti di caricamento file, che sono i mattoni della gestione '
           'documentale che all’area di stato civile manca.')

    h(d, 2, 'Il catalogo come contratto')
    par(d, 'I componenti sono pubblicati in un catalogo navigabile, generato dai sorgenti e '
           'servito accanto all’applicazione. ⚠️ Il catalogo non è documentazione accessoria: è '
           'il modo in cui chi sviluppa una schermata scopre che un componente esiste, e quindi '
           '**è ciò che impedisce che venga riscritto**. Da qui la regola: un componente nuovo '
           'entra nella libreria con la propria storia, e un componente senza storia è un '
           'componente che qualcun altro riscriverà.')

    h(d, 2, 'Le regole d’uso')
    voce(d, 'Si usa ciò che c’è.', 'Prima di scrivere un componente si guarda il catalogo. '
            'Sessanta componenti coprono la quasi totalità di ciò che le schermate del pilota '
            'richiedono.')
    voce(d, 'Le varianti si ottengono estendendo, non copiando.', 'Se un componente non fa '
            'esattamente ciò che serve, si estende quello condiviso e la variante torna a tutti. '
            'Copiarlo nel proprio progetto significa che al prossimo cambio di colore ce ne '
            'saranno due da aggiornare, e uno verrà dimenticato.')
    voce(d, 'Nessun CSS di schermata.', 'Colori, font e spaziature vengono dalle utility. Una '
            'schermata che dichiara un colore sta creando un secondo design system.')
    voce(d, 'Il prefisso è parte del contratto.', 'In un contesto federato il prefisso del '
            'selettore evita le collisioni fra applicazioni caricate nella stessa pagina. ⚠️ '
            'Oggi ne convivono due, e la cosa va sanata: si veda il capitolo sui rischi.')
    voce(d, 'I messaggi sono in italiano e vengono dalla configurazione.', 'La libreria porta '
            'già messaggi predefiniti in italiano per gli errori di modulo; per i campi '
            'dell’integrazione il messaggio è invece quello che la configurazione dichiara per '
            'quel campo, perché è lì che il funzionario lo scrive.')

    h(d, 2, 'Accessibilità')
    par(d, 'Bootstrap Italia nasce per soddisfare i requisiti di accessibilità della Pubblica '
           'Amministrazione, e questo è il motivo principale per cui lo si adotta invece di '
           'partire da un framework generico. ⚠️ La conformità però **non si eredita '
           'automaticamente**: si perde con le personalizzazioni — un contrasto insufficiente '
           'fra un colore nuovo e lo sfondo, un campo senza etichetta, un componente che si '
           'raggiunge solo con il mouse. Le regole di questo capitolo servono anche a questo: '
           'meno si personalizza, meno conformità si mette a rischio.')
    par(d, '[DA VERIFICARE: il livello di conformità richiesto al progetto, lo strumento con cui '
           'si verifica e chi conduce la verifica.] Il documento registra la questione come '
           'punto aperto perché non è deducibile dalle fonti disponibili.')
    return d


def parte_quarta(d):
    # ═══════════════════════════════════════════════ 8. Processi front-end
    h(d, 1, 'Ambiente e Processi')
    h(d, 2, 'Processi Front-End')
    par(d, 'Il percorso di formazione di un atto si svolge in otto passi [F4]. La tabella '
           'seguente li mette in fila e indica, per ciascuno, quali componenti della libreria '
           'lo realizzano e che cosa invece va costruito.')
    figura(d, 'fe_schermate.png', 6.3,
           'Gli otto passi e i componenti che li realizzano. Le voci a destra sono le sole '
           'funzioni da costruire.')
    tab(d, SCHERMATE, [2.0, 2.6, 1.7])
    par(d, '⚠️ **Il risultato è il punto principale di questo documento**: su undici schermate, '
           'le funzioni realmente da costruire sono **quattro**, e nessuna di esse è un '
           'problema di grafica. Sono maschere che SIPO non ha — il caricamento dei documenti, '
           'i campi che ANSC richiede e SIPO non raccoglie, la consegna del codice di sessione, '
           'lo stato ANSC nelle maschere di ricerca. Tutto il resto è composizione di '
           'componenti esistenti.')

    h(d, 3, 'La maschera della sessione')
    par(d, 'È la più caratteristica, perché non ha equivalenti in SIPO. Deve consentire di '
           'incollare il codice generato sulla web app di ANSC, mostrare da quel momento il '
           'tempo residuo, e avvisare quando il residuo scende sotto la soglia di guardia. Il '
           'componente del codice usa e getta esiste; ciò che va costruito è il comportamento: '
           'la consegna al concentratore e il conto alla rovescia.')
    par(d, '⚠️ Va evitata una tentazione: **non si chiede il codice all’inizio di ogni '
           'operazione**. La sessione dura quattro ore e l’unità di verifica è l’azione, non la '
           'chiamata. Chiedere il codice a ogni passo trasformerebbe una sessione in una '
           'autenticazione continua, che è esattamente ciò che l’analisi ha escluso.')

    h(d, 3, 'Le maschere di caricamento dei documenti')
    par(d, 'L’area di stato civile di SIPO non gestisce alcun documento allegato: è una '
           'funzione mancante, non una funzione da riprogettare. Servono la maschera di '
           'caricamento, l’elenco dei documenti richiesti dal caso d’uso determinato, la loro '
           'anteprima e la segnalazione dello stato della scansione antivirus, che è di ANSC. '
           'I tre componenti di caricamento e il visualizzatore di PDF forniscono tutto il '
           'necessario sul lato visivo.')

    h(d, 3, 'I campi che ANSC richiede e SIPO non raccoglie')
    par(d, 'Non sono una schermata nuova ma un’aggiunta alle maschere esistenti, guidata dalla '
           'configurazione: è la configurazione a dichiarare quali campi servono per il caso '
           'd’uso determinato, con quale obbligatorietà e con quale messaggio. ⚠️ Ne discende '
           'che **queste parti di maschera non si scrivono a mano**: si generano dalla '
           'configurazione, altrimenti ogni revisione del mapping nazionale diventerebbe una '
           'modifica al codice.')

    h(d, 3, 'Lo stato ANSC nelle maschere di ricerca e di dettaglio')
    par(d, 'È la più piccola delle quattro e la più facile da dimenticare: l’operatore deve '
           'poter vedere, cercando un atto, se è stato depositato e in quale stato si trovi in '
           'ANSC. Il componente di etichetta di stato esiste; ciò che va deciso è dove '
           'collocarlo nelle maschere esistenti.')

    h(d, 2, 'Processi Back-End')
    par(d, 'Il presente documento non descrive i servizi, che sono oggetto dei contratti dei '
           'componenti [F6]. Ne registra però il vincolo che li riguarda dal lato del '
           'front-end: **ogni schermata consuma un contratto dichiarato**, e nessuna schermata '
           'legge direttamente la base dati. È una differenza sostanziale rispetto a oggi, dove '
           'la pagina composta dal server e la query vivono nello stesso modulo.')

    # ═══════════════════════════════════════════════ 9. Ciclo di vita della versione
    h(d, 1, 'Il ciclo di vita della versione adottata')
    par(d, 'Questo capitolo tratta un aspetto della scelta tecnologica che non riguarda ciò che '
           'il front-end sa fare, ma per quanto tempo lo saprà fare nelle condizioni di oggi. '
           'Non mette in discussione la decisione — che, come si è detto, risponde a un vincolo '
           'reale — ma la rende esplicita nelle sue conseguenze, perché una scelta di questo '
           'genere si governa soltanto se è scritta.')

    h(d, 2, 'Come Angular gestisce le proprie versioni')
    par(d, 'Angular pubblica una versione maggiore ogni sei mesi e ne dichiara il sostegno in '
           'due fasi: **sei mesi di supporto attivo**, nei quali riceve correzioni di ogni '
           'genere, e **dodici mesi ulteriori di supporto esteso**, nei quali riceve soltanto '
           'le correzioni critiche e quelle di sicurezza. Complessivamente diciotto mesi, dopo '
           'i quali il ramo non riceve più alcun aggiornamento.')
    par(d, 'Applicando questa regola alle versioni rilasciate finora si ottiene il quadro '
           'seguente. [DA VERIFICARE: le date sono ricavate dalla politica di supporto '
           'dichiarata e dalla cadenza semestrale dei rilasci; vanno confermate sulla tabella '
           'ufficiale prima della pubblicazione del documento.]')
    tab(d, VERSIONI, [0.9, 1.1, 1.2, 1.4, 1.7])
    par(d, 'La versione adottata si colloca quindi **fuori dal periodo di sostegno da circa '
           'dieci mesi**. Vale la pena notare che non è un caso isolato: alla data di questo '
           'documento anche la versione immediatamente successiva è uscita dal supporto, e '
           'quella ancora successiva vi rimarrà per poche settimane. Il ritmo semestrale rende '
           'la condizione frequente, e ciò che distingue una situazione governata da una subita '
           'non è la distanza dalla versione corrente, ma il fatto che sia nota e presidiata.')

    h(d, 2, 'Perché la scelta è comunque motivata')
    par(d, 'Prima di esporre i rischi conviene dire perché la decisione è ragionevole, così che '
           'il capitolo non venga letto come una riserva.')
    voce(d, 'Il vincolo è reale.', 'La libreria condivisa non appartiene a questo progetto: '
            'serve altri applicativi di Roma Capitale, e in un modello federato la versione è '
            'condivisa da tutti. Allineare il progetto a una versione diversa avrebbe '
            'significato chiedere a tutti gli altri di muoversi insieme.')
    voce(d, 'L’alternativa non era gratuita.', 'Portare la libreria a una versione recente è un '
            'intervento che attraversa tre versioni maggiori, tocca novantanove esposizioni, '
            'il meccanismo di federazione, il builder e l’intera catena delle dipendenze di '
            'contorno. Farlo mentre si sviluppa il pilota avrebbe sommato due rischi invece di '
            'affrontarne uno per volta.')
    voce(d, 'La versione adottata è collaudata.', 'È quella con cui la libreria è in esercizio '
            'da tempo, in un ambiente di produzione. Una versione recente ma non provata in '
            'quel contesto non sarebbe stata, di per sé, più sicura.')
    par(d, 'La scelta è dunque difendibile come **decisione di fase**: consente di consegnare '
           'il pilota senza introdurre un rischio di integrazione. Ciò che va evitato è che si '
           'trasformi in una condizione permanente per semplice inerzia — ed è l’unica cosa '
           'che questo capitolo chiede.')

    h(d, 2, 'I rischi che ne derivano')
    par(d, 'I rischi sono di natura diversa fra loro e non hanno tutti la stessa urgenza. Il '
           'primo è il solo che possa manifestarsi da un giorno all’altro; gli altri sono lenti '
           'e si aggravano con il tempo, che è ciò che li rende facili da rimandare.')
    tab(d, RISCHI_EOL, [1.5, 2.6, 2.2])
    par(d, '⚠️ Un chiarimento utile a non sopravvalutare il primo rischio: **l’assenza di '
           'correzioni non significa che esista oggi una vulnerabilità nota**. Significa che, '
           'se dovesse emergerne una, non ci sarebbe un aggiornamento da applicare e occorrerebbe '
           'decidere sul momento fra una correzione mantenuta in proprio, una mitigazione a '
           'livello di applicazione o una risalita di versione condotta in emergenza. È la '
           'differenza fra un problema tecnico e un problema di tempi, ed è per questo che il '
           'documento chiede che il percorso sia deciso prima e non durante.')
    par(d, 'Va aggiunto che il front-end non è l’unico strato esposto. Le protezioni che '
           'contano davvero per questi dati — autenticazione, autorizzazione, cifratura del '
           'trasporto, validazione — risiedono nei servizi e nel concentratore, e non dipendono '
           'dalla versione del framework di interfaccia. La versione del front-end incide sul '
           'rischio, non lo determina da sola.')

    h(d, 2, 'Le misure che contengono il rischio')
    par(d, 'Le misure seguenti non richiedono di rivedere la decisione: sono il modo di '
           'renderla sostenibile.')
    voce(d, 'Datare la decisione.', 'Registrarla con una scadenza di riesame e con '
            'l’occasione a cui legarla — la fine del pilota, un rilascio della libreria, '
            'l’esigenza di un altro applicativo. Una decisione senza data diventa una '
            'condizione, e nessuno se ne riprende la responsabilità.')
    voce(d, 'Scrivere codice che costi poco da portare avanti.', 'Componenti autosufficienti, '
            'iniezione delle dipendenze nella forma corrente, nessuna interfaccia già '
            'dichiarata obsoleta. La libreria è già in gran parte così: mantenere la disciplina '
            'sulle parti nuove riduce il costo del salto senza costare nulla oggi.')
    voce(d, 'Congelare e verificare la baseline.', 'Un solo elenco di versioni — framework, '
            'Node, TypeScript, design system, strumenti — dichiarato e verificato alla '
            'costruzione, così che nessuno lo sposti per conto proprio.')
    voce(d, 'Sorvegliare le dipendenze.', 'Un controllo automatico delle vulnerabilità note a '
            'ogni costruzione: non produce correzioni, ma fa la differenza fra accorgersene e '
            'non accorgersene.')
    voce(d, 'Non accumulare divergenze sulla libreria.', 'Ogni personalizzazione fatta oggi è '
            'lavoro da rifare al momento del salto. Le modifiche vanno proposte a chi la '
            'governa e rilasciate lì, non tenute in locale.')
    voce(d, 'Pianificare il salto come intervento a sé.', 'Con un proprio momento e un proprio '
            'budget, e non come manutenzione ordinaria di un progetto. In un modello federato è '
            'un intervento di programma, perché muove tutti gli applicativi insieme.')
    par(d, 'Tre di queste misure — la data di riesame, il percorso da seguire in caso di '
           'vulnerabilità e il ciclo di vita di Node e TypeScript — richiedono una decisione '
           'che eccede l’analisi e sono registrate fra i punti aperti.')

    return d


def parte_quinta(d):
    # ═══════════════════════════════════════════════ 10. Requisiti
    h(d, 1, 'Requisiti Utente')
    par(d, 'I requisiti seguenti riguardano il modo in cui il front-end è fatto, e valgono per '
           'ogni schermata del progetto. I requisiti di ciò che le schermate devono fare sono '
           'nell’analisi dell’integrazione [F3].')
    tab(d, REQUISITI, [0.8, 3.0, 2.5])

    h(d, 1, 'Requisiti non funzionali')
    tab(d, RNF, [0.9, 1.8, 3.6])

    # ═══════════════════════════════════════════════ 11. Rischi
    h(d, 1, 'Classi di rischio')
    par(d, 'I rischi sono classificati secondo lo schema del modello documentale: alta, media e '
           'bassa. Tre sono di classe alta, e tutti e tre riguardano la libreria condivisa — '
           'non le schermate da scrivere.')
    tab(d, RISCHI, [0.8, 1.5, 2.1, 1.9])
    par(d, '⚠️ Va notato che i tre rischi alti hanno una radice comune: **la libreria è un bene '
           'condiviso che il progetto usa ma non governa**. È una situazione normale e anche '
           'desiderabile — è ciò che rende un design system tale — ma comporta che alcune '
           'decisioni del progetto dipendano da tempi altrui, e conviene dirlo prima di '
           'pianificare.')

    # ═══════════════════════════════════════════════ 12. Test
    h(d, 1, 'Strategie di test')
    h(d, 2, 'Metodologie e tecniche di test')
    par(d, 'Il punto di partenza va dichiarato: **nella libreria non esiste oggi alcun test '
           'automatico**. Per una libreria caricata a runtime da più applicazioni è il rischio '
           'più concreto, perché ogni modifica si verifica manualmente e su ogni progetto che '
           'la usa.')
    par(d, 'La proposta non è di colmare il vuoto in una volta, che sarebbe irrealistico, ma di '
           'legarlo al lavoro: **i componenti toccati dal progetto escono con i propri test**, e '
           'i componenti nuovi non entrano senza. In questo modo la copertura cresce dove il '
           'rischio è effettivo, invece di crescere dove è più facile scrivere test.')
    par(d, '⚠️ La cosa acquista un peso ulteriore per via della versione adottata: un '
           'insieme di test è anche ciò che, il giorno in cui la libreria dovrà salire di '
           'versione, dirà se è salita bene. Oggi quella verifica potrebbe farsi soltanto a '
           'mano, componente per componente e progetto per progetto.')
    tab(d, TEST, [1.5, 3.0, 1.8])

    h(d, 2, 'Cicli di test')
    par(d, 'Tre momenti, ciascuno con un proprio esito atteso. **Alla modifica di un '
           'componente**: test unitari e verifica visiva sul catalogo. **Al rilascio della '
           'libreria**: verifica che una applicazione di prova la carichi e che la versione '
           'condivisa sia una sola. **Al rilascio di una schermata**: percorso completo sui '
           'passi che la coinvolgono, con il concentratore attivo.')

    # ═══════════════════════════════════════════════ 13. Open point
    h(d, 1, 'Registro dei punti aperti')
    par(d, 'Le questioni seguenti vanno chiuse con il committente e con chi governa la libreria '
           'prima del consolidamento delle specifiche. Le prime tre condizionano l’avvio dello '
           'sviluppo.')
    tab(d, OPEN_POINT, [0.8, 4.2, 1.3])

    par(d, '⚠️ **Una avvertenza finale sul metodo.** Questo documento è stato scritto '
           'ricavando i fatti dai sorgenti della libreria e dalle fonti disponibili; dove le '
           'fonti tacciono si è scritto [DA VERIFICARE] invece di colmare con una ipotesi. Le '
           'voci così contrassegnate — le date esatte di fine supporto delle versioni, il ciclo '
           'di vita della linea di Node adottata, il livello di accessibilità richiesto e i '
           'browser supportati — non sono dimenticanze: sono le cose che nessuna delle due fonti dice, '
           'e che vanno chieste.')
    return d


def main():
    d = costruisci()
    intestazioni(d)
    parte_seconda(d)
    parte_terza(d)
    parte_quarta(d)
    parte_quinta(d)
    d.save(OUT)
    import docx as _d
    doc = _d.Document(OUT)
    print('scritto:', os.path.relpath(OUT, BASE))
    print('capitoli:', sum(1 for p in doc.paragraphs if p.style.name == 'Heading 1'),
          '· tabelle:', len(doc.tables),
          '· immagini:', len(doc.inline_shapes),
          '· paragrafi:', len(doc.paragraphs))


if __name__ == '__main__':
    main()
