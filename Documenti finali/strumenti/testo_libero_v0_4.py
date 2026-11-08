# -*- coding: utf-8 -*-
"""v0.4 di «ANALISI_Atti-Testo-Libero_SIPO-ANSC» (07/11/2026), dalla v0.3 sul file reale.

Recepisce la comunicazione ANSC sui casi d'uso di servizio fornita dal committente
(`Sorgenti Documentali/Comunicazione_ANSC_Casi-uso-servizio_servizi-cooperativi.txt`, [A6]):
dal 09/09/2024 i 10 casi d'uso di servizio delle DICHIARAZIONI non sono disponibili tramite
servizi cooperativi; restano cooperativi i 5 delle TRASCRIZIONI e i 10 delle annotazioni, per
la fase ibrida; sulla web app ci sono tutti, e per i 10 l'ufficiale indica il motivo. I casi
d'uso di servizio non generano annotazioni automatiche, non controllano i metadati, non
predispongono le comunicazioni anagrafiche; ANSC ne chiede un uso monitorato e limitato e
suggerisce alle case software servizi di recupero degli atti registrati sulla web app.

Effetti: la v0.3 proponeva come riferimento il percorso interamente in SIPO per tutti gli atti
a testo libero. Ora si distingue per tipo di contenuto: DICHIARAZIONI -> le due strategie della
web app (Gestione 2 come percorso unico); TRASCRIZIONI -> terzo percorso in SIPO, finché dura la
fase ibrida. Nuovo TL-11 sugli automatismi che il caso d'uso di servizio non produce.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/testo_libero_v0_4.py
"""
import copy
import os
import sys

import docx
from docx.oxml.ns import qn
from docx.shared import Inches
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from genera_testo_libero import _versa   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Atti-Testo-Libero_SIPO-ANSC_v0.3.docx')
NOME = 'ANALISI_Atti-Testo-Libero_SIPO-ANSC_v0.4'
OUT = os.path.join(FIN, NOME + '.docx')
DATA = '07/11/2026'

d = docx.Document(SRC)


def _svuota(p):
    for r in list(p._p):
        if r.tag in (qn('w:r'), qn('w:hyperlink')):
            p._p.remove(r)


def trova(inizio, stile=None):
    trovati = [p for p in d.paragraphs if p.text.startswith(inizio)
               and (stile is None or p.style.name == stile)]
    if len(trovati) != 1:
        raise SystemExit('attesi 1, trovati %d: %s' % (len(trovati), inizio[:60]))
    if D.ha_commenti(trovati[0]._p):
        raise SystemExit('paragrafo commentato: ' + inizio[:60])
    return trovati[0]


def paragrafo(inizio, nuovo, stile=None):
    p = trova(inizio, stile)
    _svuota(p)
    if stile and stile.startswith('Heading'):
        p.add_run(nuovo)
    else:
        _versa(p, nuovo)
    return p


def elimina(inizio):
    p = trova(inizio)
    p._p.getparent().remove(p._p)


def dopo(p, testo, stile=None):
    nuovo = docx.oxml.OxmlElement('w:p')
    p._p.addnext(nuovo)
    q = Paragraph(nuovo, p._parent)
    if stile:
        q.style = d.styles[stile]
    elif p._p.pPr is not None:
        q._p.insert(0, copy.deepcopy(p._p.pPr))
    _versa(q, testo)
    return q


def riga_di(chiave, intestazione=None):
    trovate = []
    for t in d.tables:
        if intestazione and intestazione not in [c.text.strip() for c in t.rows[0].cells]:
            continue
        trovate += [(t, r) for r in t.rows if r.cells[0].text.strip() == chiave]
    if len(trovate) != 1:
        raise SystemExit('attesa 1 riga, trovate %d: %s' % (len(trovate), chiave))
    return trovate[0]


def scrivi_cella(c, testo, grassetto=False):
    for extra in c.paragraphs[1:]:
        extra._p.getparent().remove(extra._p)
    _svuota(c.paragraphs[0])
    _versa(c.paragraphs[0], testo, grassetto_forzato=grassetto, dim=9)


def cella(chiave, colonna, nuovo, intestazione=None):
    scrivi_cella(riga_di(chiave, intestazione)[1].cells[colonna], nuovo)


def nuova_riga(t, valori):
    tr = copy.deepcopy(t.rows[-1]._tr)
    t._tbl.append(tr)
    for c, v in zip(t.rows[-1].cells, valori):
        scrivi_cella(c, v)


def larghezze(t, pollici):
    for riga in t.rows:
        for c, w in zip(riga.cells, pollici):
            c.width = Inches(w)
    griglia = t._tbl.find(qn('w:tblGrid'))
    for col, w in zip(griglia.findall(qn('w:gridCol')), pollici):
        col.set(qn('w:w'), str(int(round(Inches(w).twips))))


# ================================================================ riferimenti
t_rif, r = riga_di('[A5]')
nuova_riga(t_rif, ['[A6]', 'Comunicazione ANSC sui casi d’uso di servizio tramite servizi '
                           'cooperativi, in vigore dal 09/09/2024 (testo in `Sorgenti '
                           'Documentali/Comunicazione_ANSC_Casi-uso-servizio_servizi-'
                           'cooperativi.txt`). Corrisponde alla voce «ID 120» del rilascio '
                           '1.33.0.', 'Documentazione ANSC'])
cella('[A5]', 1, '`ansc/docs/Changelog.md` — rilascio 1.33.0 (03/10/2024), rilascio 1.34.0 '
                 '(04/11/2024) e le altre voci sui casi d’uso di servizio.')
paragrafo('Riprende il capitolo «Atti a Testo Libero»',
          'Riprende il capitolo «Atti a Testo Libero» dell’analisi di integrazione [R1], con '
          'le due strategie proposte, e lo sviluppa in quattro direzioni: che cosa sono questi '
          'atti in SIPO e in ANSC, quando si ricorre a essi, che cosa distingue le due '
          'strategie e quale conviene, quali servizi ANSC occorrono. Tiene conto della '
          'comunicazione ANSC sui casi d’uso di servizio [A6], che decide quale percorso sia '
          'praticabile per le dichiarazioni e quale per le trascrizioni. Le decisioni ancora da '
          'prendere sono raccolte in coda, come punti aperti TL-01…TL-11.')

# ================================================================ §2.2
t_uc = [t for t in d.tables if [c.text.strip() for c in t.rows[0].cells]
        == ['Codice', 'Caso d’uso di servizio', 'Tipo contenuto']]
assert len(t_uc) == 1
t_uc = t_uc[0]
t_uc.add_column(Inches(1.5))
for i, riga in enumerate(t_uc.rows):
    tipo = riga.cells[2].text
    if i == 0:
        scrivi_cella(riga.cells[3], 'Servizi cooperativi', grassetto=True)
    elif tipo.startswith('1'):
        scrivi_cella(riga.cells[3], 'Non disponibile dal 09/09/2024')
    else:
        scrivi_cella(riga.cells[3], 'Disponibile (fase ibrida)')
larghezze(t_uc, [0.9, 2.7, 1.3, 1.6])

paragrafo('Il catalogo ANSC_03 ne conta 25',
          'Il catalogo ANSC_03 ne conta 25: uno per tipologia di evento e per macrocategoria, '
          'cioè 10 per la formazione di atti, 5 per le trascrizioni e 10 per le annotazioni '
          '[A4]. Questi ultimi registrano solo annotazioni di tipo integrativo e non riguardano '
          'il presente documento; restano comunque disponibili tramite servizi cooperativi '
          '[A6]. ')
paragrafo('I quindici elementi pertinenti',
          'I quindici elementi pertinenti (10 per gli atti e 5 per le trascrizioni) sono i '
          'seguenti. L’ultima colonna dice se il gestionale li può depositare con i servizi '
          'cooperativi [A6]; sulla web app sono tutti disponibili:')
paragrafo('Il motivo del recupero è obbligatorio',
          'Il motivo del recupero è obbligatorio in tutti i dieci casi d’uso di servizio di '
          'formazione, e solo in quelli [A4]. Dice ad ANSC perché l’atto arriva fuori dall’albero '
          'dei casi d’uso, ed è lo strumento con cui ANSC ne sorveglia l’uso: sulla web app '
          'l’ufficiale deve indicarlo, e i motivi servono a far emergere casistiche nuove, da '
          'correggere o da aggiungere al catalogo [A6]. Per le trascrizioni è facoltativo. Per gli '
          'atti di questo documento il valore è il 3:')
p = trova('I dati facoltativi possono restare vuoti')
dopo(p, 'Il caso d’uso di servizio **non genera annotazioni automatiche**, **non consente il '
        'controllo dei metadati** e **non predispone le comunicazioni automatiche di '
        'aggiornamento anagrafico** [A6]. Per questo ANSC ne chiede un uso monitorato e '
        'limitato ai soli casi strettamente necessari, e lo sconsiglia in particolare per le '
        'trascrizioni delle sentenze di adozione, dove solo il caso d’uso specifico garantisce '
        'la segretezza e le condizioni della copia integrale.')

# ================================================================ §2.3
paragrafo('Il deposito del caso d’uso di servizio: che cosa dice ANSC',
          'Il deposito del caso d’uso di servizio: dichiarazioni e trascrizioni',
          stile='Heading 2')
p = paragrafo('Il rilascio ANSC 1.33.0 del 03/10/2024',
              'Una comunicazione di ANSC [A6], che il changelog riporta come «Disabilitazione casi '
              'd’uso di servizio lato servizi cooperativi (ID 120)» nel rilascio 1.33.0 [A5], '
              'fissa la regola. **Dal 9 settembre 2024 i dieci casi d’uso di servizio delle '
              'dichiarazioni non sono più disponibili tramite servizi cooperativi**: un gestionale '
              'non li può depositare con R009, e l’atto si forma solo sulla web app. **Restano '
              'disponibili i cinque delle trascrizioni** e i dieci delle annotazioni, necessari '
              'alla fase ibrida, cioè alle trascrizioni fra comuni finché tutti non avranno '
              'aderito ad ANSC. Sulla web app sono disponibili tutti.')
for inizio in ('Tre elementi successivi vanno anzi in senso contrario',
               'La correzione del rilascio 1.46.2',
               'La prenotazione degli identificativi per il parto plurimo. È un servizio',
               'I contrassegni dei certificati emissibili. Il rilascio 1.34.0'):
    elimina(inizio)
paragrafo('Non è quindi accertato che un gestionale',
          'Ne discende che il percorso dipende dal **tipo di contenuto** dell’atto. Per una '
          '**dichiarazione** a testo libero l’atto si forma sulla web app, ed è il caso delle '
          'due strategie del capitolo successivo. Per una **trascrizione** a testo libero il '
          'gestionale può depositare l’atto con il caso d’uso di servizio, e l’atto si forma '
          'interamente in SIPO: è il terzo percorso, descritto nelle considerazioni. Il secondo '
          'vale finché dura la fase ibrida, la cui fine ANSC lega all’adesione di tutti i comuni '
          'senza indicarne la data.')
p = trova('Ne discende che il percorso dipende dal tipo di contenuto')
dopo(p, 'La stessa comunicazione suggerisce alle case software di sviluppare servizi per '
        '**recuperare gli atti registrati sulla web app**, così da mantenere allineati i sistemi '
        'locali e svolgere gli adempimenti successivi [A6]. È esattamente il ritorno in SIPO '
        'delle due strategie, e l’aggancio di un atto formato sulla web app già previsto '
        'dall’analisi [R1].')

# ================================================================ §3
paragrafo('La regola che ne discende:',
          'La regola che ne discende: **il testo libero è l’esito di un caso che ANSC non '
          'prevede, non il rimedio a un dato sbagliato o a una configurazione incompleta.** È '
          'anche ciò che ANSC chiede, quando raccomanda un uso dei casi d’uso di servizio '
          'limitato ai soli casi strettamente necessari [A6]: un atto formato così non genera '
          'annotazioni automatiche né comunicazioni anagrafiche. Se il testo libero diventasse '
          'il ripiego ordinario per ogni «UC non determinato», quegli atti crescerebbero proprio '
          'dove la configurazione è più debole. Per questo il messaggio di rinvio va mostrato '
          'solo dopo che i dati sono stati confermati, e la categoria «UC non determinato» del '
          'back-office resta distinta da quella degli atti in attesa della web app. Per le '
          'trascrizioni l’esito «testo libero» non porta alla web app ma al terzo percorso, '
          'interamente in SIPO.')

# ================================================================ §4
paragrafo('L’analisi [R1] propone due modalità',
          'L’analisi [R1] propone due modalità, che la figura mette a confronto su tre corsie: '
          'SIPO, lo stato dell’atto, la web app ANSC. In entrambe l’atto si forma sulla web app '
          'e il numero comunale esce da SIPO, perché SIPO è l’unico luogo in cui la serie è '
          'governata [R1]. Cambia il momento in cui il caso si riconosce, e con esso quante '
          'volte si immettono i dati. Sono le strategie delle **dichiarazioni**, per le quali la '
          'web app è l’unica via [A6].')

# ================================================================ §5.2 / §5.3
paragrafo('Così la doppia immissione non scompare',
          'Così la doppia immissione non scompare: diventa un **controllo**. Il prezzo è '
          'accettare che, nel caso scoperto tardi, il lavoro fatto in SIPO serva da riscontro e '
          'non da fonte. La proposta vale per le dichiarazioni; per le trascrizioni il percorso '
          'è il terzo, descritto qui sotto.')
p = trova('L’atto importato porta pochi dati.')
dopo(p, '**L’atto non produce gli automatismi.** Formato con il caso d’uso di servizio, l’atto '
        'non genera annotazioni automatiche e non predispone le comunicazioni di aggiornamento '
        'anagrafico [A6]. Ciò che negli altri atti fa ANSC — l’annotazione sugli atti collegati, '
        'la comunicazione all’anagrafe — va quindi fatto dall’ufficio, e SIPO deve dirlo '
        'all’ufficiale alla conclusione dell’atto invece di lasciarlo alla memoria. Vale per '
        'tutti i percorsi, compreso il terzo (TL-11).', stile='List Paragraph')

# ================================================================ §5.4
paragrafo('Il terzo percorso: l’atto formato interamente in SIPO',
          'Il terzo percorso: la trascrizione formata interamente in SIPO', stile='Heading 2')
paragrafo('Le due strategie nascono da un presupposto',
          'Per le trascrizioni la web app non è necessaria. I cinque casi d’uso di servizio delle '
          'trascrizioni restano disponibili tramite servizi cooperativi [A6], SIPO ha già la '
          'pagina del testo libero, e il caso d’uso di servizio chiede poco più della minuta. '
          'Una trascrizione a testo libero può quindi formarsi **interamente in SIPO**, con i '
          'servizi cooperativi, senza andare sulla web app e senza importazione. Per le '
          'dichiarazioni questo percorso non è praticabile.')
cella('5', 1, 'Deposito con `idUsecase` del caso d’uso di servizio della trascrizione, il motivo '
              'del recupero (facoltativo) e i contrassegni dei certificati emissibili.',
      intestazione='Servizio ANSC')
paragrafo('Rispetto al percorso degli altri atti',
          'Rispetto al percorso degli altri atti cambiano due cose sole. Il **testo** viene dalla '
          'pagina del testo libero (`ATTO_TESTO_LIBERO`) invece di essere composto, e va in '
          '`composizioneCompleta`. L’**UC** non si determina: è il caso d’uso di servizio della '
          'trascrizione per il registro dell’atto, uno dei cinque del §2.2. Validazione, firme, '
          'attestazione di conformità e chiusura sono quelle già disegnate per gli altri atti '
          '[R1].')
paragrafo('È il percorso più coerente',
          'Per le trascrizioni è il percorso più coerente con un sistema che resta SIPO-centrico: '
          'un solo luogo di immissione, nessuno stato sospeso, nessuna transcodifica inversa, '
          'nessun ritorno da presidiare. Copre anche la trascrizione scoperta al Riepilogo: senza '
          'UC determinato, l’atto passa alla pagina del testo libero conservando i dati già '
          'compilati. Il documento lo propone quindi come **percorso delle trascrizioni**. È però '
          '**transitorio**: ANSC mantiene i casi d’uso di servizio delle trascrizioni per la fase '
          'ibrida, e la loro disponibilità cooperativa potrà cessare quando tutti i comuni avranno '
          'aderito. Il disegno deve perciò consentire di passare le trascrizioni alla Gestione 2 '
          'senza riprogettare nulla: il ritorno e l’importazione servono comunque alle '
          'dichiarazioni.')
paragrafo('Prima di costruirlo serve una verifica sola',
          'Prima di costruirlo conviene **provare in preproduzione il deposito con R009 di una '
          'trascrizione con caso d’uso di servizio**, per avere conferma del comportamento e degli '
          'esiti che i contratti non descrivono [A3]. Restano comunque sulla web app le funzioni '
          'che solo lì esistono: la modifica successiva dei certificati emissibili [A2] e la nota '
          'tecnica.')

# ================================================================ cap. 6
paragrafo('Nel percorso di riferimento SIPO usa i servizi',
          'Per le **trascrizioni** SIPO usa i servizi della formazione degli altri atti, elencati '
          'con i loro passi nel paragrafo «Il terzo percorso». Le tabelle che seguono riguardano '
          'le **dichiarazioni**: nelle due strategie SIPO non deposita e non firma, lo fa la web '
          'app, e i servizi che SIPO chiama sono quindi quasi tutti **letture**, concentrate nel '
          'ritorno. Nelle colonne G1 e G2, «sì» indica il servizio necessario, «cond.» quello '
          'necessario solo in una condizione, «facolt.» quello facoltativo, «ind.» quello usato '
          'indirettamente.')
cella('R009 /validazione/evento', 1,
      'Per le dichiarazioni il caso d’uso di servizio non è disponibile tramite servizi '
      'cooperativi dal 09/09/2024 [A6]: il deposito avviene sulla web app. Per le trascrizioni '
      'SIPO lo chiama, nel terzo percorso.')

# ================================================================ cap. 7
t_dis, _ = riga_di('`ANSC_STATO_ATTO`'.strip('`'))
nuova_riga(t_dis, ['Configurazione dei tipi atto a testo libero',
                   'Per ciascun tipo atto a testo libero, il caso d’uso di servizio da usare e '
                   'quindi il percorso: trascrizione in SIPO, dichiarazione sulla web app. Il '
                   'tipo di contenuto è la terza colonna della tabella del §2.2.'])
nuova_riga(t_dis, ['Conclusione dell’atto',
                   'Il promemoria degli adempimenti che il caso d’uso di servizio non automatizza: '
                   'annotazioni sugli atti collegati e comunicazione anagrafica (TL-11).'])

# ================================================================ punti aperti
paragrafo('Dieci questioni restano da chiudere.',
          'Undici questioni restano da chiudere. La prima è la scelta della strategia per le '
          'dichiarazioni; la seconda riguarda la durata del percorso delle trascrizioni; le altre '
          'servono a completare il disegno, e in buona parte riguardano le dichiarazioni '
          '(TL-03…TL-07). I punti si legano a OP-66, OP-71, OP-78 e OP-79 dell’analisi di '
          'integrazione [R1].')
cella('TL-01', 1, 'Quale strategia adottare per le dichiarazioni, che si formano sulla web app: '
                  'la Gestione 2 come percorso unico, con la Gestione 1 ridotta a deviazione '
                  'verso di essa (proposta di questo documento), oppure entrambe. Per le '
                  'trascrizioni si propone il terzo percorso, interamente in SIPO.')
cella('TL-02', 1, 'Chiuso nel merito dalla comunicazione ANSC [A6]: i casi d’uso di servizio '
                  'delle dichiarazioni sono solo sulla web app, quelli delle trascrizioni restano '
                  'cooperativi. Restano due domande: (a) fino a quando le trascrizioni restano '
                  'cooperative, e con quale preavviso ANSC ne annuncerà la fine; (b) la '
                  'prenotazione dei gemelli, che con R009 `/prenota/evento` predispone atti con il '
                  'caso d’uso 11999999, non più cooperativo: se prenotazione e completamento delle '
                  'bozze siano ancora possibili dal gestionale (si lega a OP-46 di [R1]).')
t_ap, _ = riga_di('TL-10')
nuova_riga(t_ap, ['TL-11', 'Gli automatismi che il caso d’uso di servizio non produce — '
                           'annotazioni automatiche e comunicazioni di aggiornamento anagrafico '
                           '[A6]: chi le esegue per gli atti a testo libero, con quale strumento, '
                           'e come SIPO lo ricorda all’ufficiale.', 'Cliente / Analisi'])

# ================================================================ storia
for fatto in D.frontespizio(d, '0.4', NOME):
    print('  ' + fatto)
D.storia(d, DATA, '0.4', '1 · 2.2 · 2.3 · 3 · 4 · 5.2 · 5.3 · 5.4 · 6 · 7 · Punti aperti',
         'Recepita la comunicazione ANSC sui casi d’uso di servizio: dal 09/09/2024 quelli delle '
         'dichiarazioni sono solo sulla web app, quelli delle trascrizioni restano cooperativi '
         'per la fase ibrida. Il percorso dipende ora dal tipo di contenuto: le dichiarazioni '
         'seguono le due strategie della web app, le trascrizioni il terzo percorso, '
         'interamente in SIPO e transitorio. Aggiunti gli automatismi che il caso d’uso di '
         'servizio non produce, il suggerimento di ANSC sui servizi di recupero e TL-11; TL-01 '
         'e TL-02 riscritti.')

d.save(OUT)
print('scritto', os.path.relpath(OUT, os.path.dirname(FIN)))
