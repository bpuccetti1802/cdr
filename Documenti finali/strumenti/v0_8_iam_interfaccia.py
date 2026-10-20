# -*- coding: utf-8 -*-
"""ANALISI_Identita-Profilazione-IAM v0.7 → v0.8 (15/10/2026).

Parte dalla v0.7 SALVATA DALL'UTENTE alle 17:32 (aperta in Word, rivista a mano: tolti i «⚠️»
e le formule di versione dal corpo, capitolo 6 rinominato «Scelte effettuate per il TO BE").
⚠️ Per questo NON si rigenera la v0.7 da `v0_7_iam_mse.py`: si perderebbero le sue modifiche.

Interventi:
  1. nel capitolo dell'integrazione, il sottocapitolo «L’interfaccia di amministrazione»:
     la piattaforma la dichiara ([F12] §6.2), il codice non è fra le sorgenti; serve, e per
     SIPO dipende dalla modalità (A: sola lettura, B: unico punto di gestione, da estendere);
  2. PI-36 riformulato di conseguenza;
  3. stesso stile della revisione dell'utente sulle parti che la v0.7 aveva introdotto e che
     l'utente non aveva ancora toccato: niente «⚠️», niente «dalla versione 0.7» / «v0.7:»;
  4. il rimando al capitolo rinominato.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v0_8_iam_interfaccia.py
"""
import os
import shutil
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIN = os.path.join(BASE, 'Documenti finali')
SRC = os.path.join(FIN, 'ANALISI_Identita-Profilazione-IAM_v0.7.docx')
DST = os.path.join(FIN, 'ANALISI_Identita-Profilazione-IAM_v0.8.docx')

INTERFACCIA_SIPO = [
    ['Modalità', 'L’interfaccia della piattaforma, per SIPO'],
    ['A — SIPO resta la fonte',
     'Non serve, e anzi **non deve poter modificare i profili dell’applicazione SIPO**: sarebbe '
     'un secondo posto in cui si scrive. Per SIPO è in sola lettura; gli accessi si '
     'amministrano in AnagrafeWeb.'],
    ['B — la piattaforma è la fonte',
     'È **l’unico punto di gestione** degli accessi di SIPO, e va esteso, non duplicato: '
     'un’interfaccia costruita nel back-office ANSC o in AnagrafeWeb ricreerebbe la gestione '
     'parallela esclusa (modalità C).'],
]

PI36 = ('Il codice del front-end di amministrazione della piattaforma, che [F12] §6.2 dichiara '
        'e che non è fra le sorgenti, o in sua assenza una dimostrazione. Va visto prima di '
        'scegliere la modalità B, per accertare se realizzi già il filtro per ambito e '
        'l’attribuzione del nodo organizzativo, e se impedisca di modificare i profili di '
        'un’applicazione tenuta in sola lettura.')

FAMIGLIE = [
    ['Famiglia', 'Dove sta', 'Che cosa ne sarà'],
    ['Chiavi e client di IAM',
     'In IAM; un segreto per applicazione nella configurazione di roma-capitale-auth.',
     'Restano.'],
    ['La chiave di firma di SIPO e le sue utenze tecniche',
     'Condivisa dai quarantaquattro back-end, in cinquantasette file di configurazione (RI-03); '
     'un’utenza tecnica per profilo di back-end.',
     'Spariscono nella seconda fase, quando i back-end verificano il token della piattaforma.'],
    ['La chiave di firma della piattaforma e i suoi segreti',
     'Nella configurazione di management, in chiaro, insieme alle password del database e di '
     'Redis; le utenze tecniche della piattaforma in management (MA-14).',
     'Restano le uniche, e vanno confinate all’emittente (PI-31).'],
]

RISCHIO_SEGRETI = (
    'Durante la transizione convivono tre famiglie di segreti: quelli di IAM, la chiave '
    'condivisa dei back-end di SIPO e quella della piattaforma', 'Alta', 'Alto',
    'Confinare la chiave della piattaforma prima dell’ingresso (MA-14, PI-31); dismettere la '
    'chiave condivisa di SIPO nella seconda fase; un inventario dei segreti con il titolare e la '
    'data di rotazione di ciascuno.')

PI38 = ('PI-38',
        'Se per le applicazioni di SIPO la piattaforma possa escludere il login con nome utente e '
        'password su database, e come sia valorizzata la colonna della password, che il modello '
        'dichiara obbligatoria, per gli utenti che entrano soltanto da IAM.',
        'Titolare della piattaforma')

# (vecchio, nuovo, occorrenze attese) — solo marcature introdotte dalla v0.7
PULIZIA = [
    ('Dalla versione 0.7 il documento valuta anche', 'Il documento valuta anche', 1),
    ('Dalla versione 0.7 quel punto ha un nome diverso:', 'Quel punto ha poi trovato un nome '
     'diverso:', 1),
    ('Due proprietà che la versione 0.6 dava per acquisite', 'Due proprietà che il disegno '
     'iniziale dava per acquisite', 1),
    ('La registrazione dell’accesso, che la v0.6 attribuiva al componente di autenticazione,',
     'La registrazione dell’accesso, che il disegno iniziale attribuiva al componente di '
     'autenticazione,', 1),
    ('⚠️ Dalla versione 0.7 il livello della capacità esiste già, fuori da SIPO:',
     'Il livello della capacità esiste già, fuori da SIPO:', 1),
    (' v0.7: risolto sul codice [F13].', ' Risolto sul codice [F13].', 1),
    (' ⚠️ v0.7: il token della piattaforma porta già le abilitazioni;',
     ' Il token della piattaforma porta già le abilitazioni;', 1),
    ('Una per funzionalità e area. ⚠️ Il codice arriva', 'Una per funzionalità e area. Il '
     'codice arriva', 1),
    ('Il capitolo «Scelte effettuate» ne trae le conseguenze.',
     'Il capitolo «Scelte effettuate per il TO BE» ne trae le conseguenze.', 1),
]


def main():
    if os.path.exists(DST):
        os.remove(DST)                         # solo un'esecuzione precedente di questo script
    shutil.copy(SRC, DST)
    d = docx.Document(DST)
    modello = d.tables[3]
    fatti = []

    # dentro i run, così i grassetti restano; se il testo è spezzato fra run, ripiego
    def paragrafi():
        yield from d.paragraphs
        for t in d.tables:
            for r in t.rows:
                for c in dict.fromkeys(r.cells):
                    yield from c.paragraphs

    for vecchio, nuovo, attese in PULIZIA:
        n = 0
        for p in paragrafi():
            if vecchio not in p.text:
                continue
            n += 1
            for r in p.runs:
                if vecchio in r.text:
                    r.text = r.text.replace(vecchio, nuovo)
                    break
            else:                              # spezzato fra run: il grassetto si perde
                D.testo_di(p, p.text.replace(vecchio, nuovo))
        if n != attese:
            raise SystemExit(f'«{vecchio[:50]}»: attese {attese}, trovate {n}')
        fatti.append(f'{vecchio[:46]} — {n}')

    # ⚠️ esatto: «I rischi dell’intervento» (Parte II) comincia allo stesso modo e viene prima
    prima = D.h(d, 2, 'I rischi', esatto=True)._p
    blocchi = [
        ('h2', 'L’interfaccia di amministrazione'),
        ('b', 'Il documento della piattaforma dichiara un **front-end di amministrazione**, '
              'articolato in più micro-frontend, con cui gli amministratori definiscono i profili '
              'e li assegnano agli utenti [F12] §6.2; il diagramma dei componenti di quella '
              'sezione lega la shell della piattaforma a roma-capitale-management. Il back-end ha '
              'la forma di un servizio pensato per un’interfaccia — elenchi paginati con filtri e '
              'ordinamento, ricerche, scaricamento del manuale utente, avvisi, manutenzione — e '
              'la libreria Angular rinvia a un micro-frontend della manutenzione. **Il codice '
              'dell’interfaccia però non è fra le sorgenti**, e nessun client delle API di '
              'management compare nella libreria condivisa: che cosa faccia, e se aggiunga regole '
              'che il back-end non ha, non è accertabile (PI-36).'),
        ('p', 'L’interfaccia serve, per due ragioni.'),
        ('v', ('I miglioramenti proposti vivono in un’interfaccia. ',
               'La richiesta e l’approvazione di una concessione, la revisione periodica, la '
               'copia dei profili da un collega e il cambio di ufficio (MI-02, MI-04, MI-07) sono '
               'lavoro di chi amministra, non chiamate di servizio: senza un’interfaccia restano '
               'scritture dirette sulla base dati, senza traccia.')),
        ('v', ('Senza un’interfaccia, lo strumento diventa un altro. ',
               'L’interfaccia di documentazione delle API di management è attiva su un percorso '
               'pubblico, e nessuna operazione chiede un permesso (MA-12, PI-31): se chi '
               'amministra non ha uno strumento, finisce per usare quello. L’interfaccia è anche '
               'il posto naturale dell’amministrazione per ambito (MI-03).')),
        ('p', 'Per SIPO il bisogno dipende dalla modalità di integrazione.'),
        ('tab', (INTERFACCIA_SIPO, [2.0, 4.6])),
        ('p', 'Prima di scegliere la modalità B l’interfaccia va vista — in codice o almeno in una '
              'dimostrazione — per accertare se una parte di ciò che il capitolo dei '
              'miglioramenti segna come mancante, a cominciare dal filtro per ambito e '
              'dall’attribuzione del nodo organizzativo, non sia già realizzata lato interfaccia.'),
        ('h2', 'Le credenziali: che cosa si aggiunge'),
        ('p', 'Adottare la piattaforma aggiunge credenziali a quelle che SIPO ha già? La risposta '
              'dipende da quali credenziali, perché sono tre cose diverse.'),
        ('v', ('Le credenziali delle persone. ',
               '**No**: password, SPID e CIE restano soltanto in IAM. Due condizioni: per le '
               'applicazioni di SIPO la piattaforma non deve usare il login con nome utente e '
               'password su database, che consente applicazione per applicazione e che conserva '
               'le password in management con cifratura reversibile; e va accertato come sia '
               'valorizzata, per chi entra soltanto da IAM, la colonna della password che il '
               'modello dichiara obbligatoria (MA-10, PI-38).')),
        ('v', ('Il registro degli utenti e dei loro profili. ',
               '**Sì**: management è un terzo registro, accanto a IAM e ad ANAG_USR. È accettabile '
               'perché ciascun registro ha un ruolo distinto: l’identità sta soltanto in IAM; le '
               'autorizzazioni di SIPO stanno in ANAG_USR nella modalità A, con management come '
               'copia, e in management nella modalità B, con R_UTENTI_RUOLI come proiezione. Tre '
               'registri, mai due scrivibili per la stessa applicazione.')),
        ('v', ('I segreti tecnici. ',
               '**Sì, durante la transizione**. Convivono tre famiglie.')),
        ('tab', (FAMIGLIE, [1.7, 2.8, 2.1])),
        ('b', 'La terza famiglia è quella da presidiare. Entrando nella piattaforma SIPO **aggiunge '
              'quella chiave alla propria**, e le tiene entrambe finché non dismette i propri '
              'emittenti: il guadagno arriva soltanto alla fine del percorso, quando la chiave '
              'condivisa dei back-end di SIPO sparisce e resta, oltre a quelle di IAM, la sola '
              'chiave della piattaforma.'),
    ]
    for tipo, contenuto in blocchi:
        if tipo == 'p':
            D.para(d, prima, contenuto)
        elif tipo == 'b':
            D.para(d, prima, pezzi=D.segmenta('', contenuto))
        elif tipo == 'v':
            D.voce(d, prima, *contenuto)
        elif tipo == 'h2':
            D.para(d, prima, contenuto, stile='Heading 2')
        elif tipo == 'tab':
            righe, larghezze = contenuto
            D.tabella(d, prima, righe, modello, larghezze)
    fatti.append('nuovo sottocapitolo «L’interfaccia di amministrazione» (cap. integrazione)')

    pa = D.trova_tabella(d, '#', 'Questione', 'A chi compete')
    riga = [r for r in pa.rows if r.cells[0].text.strip() == 'PI-36']
    assert len(riga) == 1, 'PI-36 non trovato'
    D.riscrivi_cella(riga[0].cells[1], PI36)
    D.clona_riga(pa, PI38)
    fatti.append('PI-36 riformulato, PI-38 nuovo')

    # ⚠️ due tabelle hanno la stessa intestazione dei rischi (Parte II e integrazione):
    # quella dell'integrazione è l'ultima
    rischi = [t for t in d.tables if [c.text.strip() for c in t.rows[0].cells] ==
              ['Rischio', 'Probabilità', 'Impatto', 'Come si contiene']]
    assert len(rischi) == 2, len(rischi)
    D.clona_riga(rischi[-1], RISCHIO_SEGRETI)
    fatti.append('rischio nuovo: tre famiglie di segreti')

    D.storia(d, '15/10/2026', '0.8', 'L’integrazione con la gestione AS-IS di SIPO (due sottocapitoli, un rischio) · Punti aperti',
             'Aggiunto il sottocapitolo sull’interfaccia di amministrazione della piattaforma: la '
             'dichiara il documento di piattaforma ma il codice non è fra le sorgenti; serve, '
             'perché i miglioramenti della gestione sono lavoro di chi amministra e perché '
             'l’alternativa è l’interfaccia di documentazione delle API, pubblica; per SIPO è in '
             'sola lettura nella modalità A e unico punto di gestione, da estendere, nella '
             'modalità B. Aggiunto il sottocapitolo sulle credenziali: quelle delle persone '
             'restano in IAM, il registro degli utenti diventa il terzo con un ruolo distinto, i '
             'segreti tecnici convivono in tre famiglie durante la transizione; un rischio e '
             'PI-38 nuovi. Riformulato PI-36. Allineate allo stile della revisione le parti '
             'introdotte nella versione precedente, e il rimando al capitolo rinominato.')
    for f in D.frontespizio(d, '0.8', 'ANALISI_Identita-Profilazione-IAM_v0.8'):
        fatti.append(f)

    d.save(DST)
    print('\n'.join('  · ' + f for f in fatti))
    cap, tab, fig = D.riepilogo(DST)
    print(f'  capitoli {cap}, tabelle {tab}, immagini {fig}')
    print('  scritto', DST)


if __name__ == '__main__':
    main()
