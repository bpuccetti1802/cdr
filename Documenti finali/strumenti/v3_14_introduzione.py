# -*- coding: utf-8 -*-
"""v3.14 — il capitoletto che spiega la configurazione, e un esempio compilato per intero.

Il capitolo descriveva le tabelle una per una senza dire prima che cosa la configurazione
faccia nel suo insieme: chi non ha seguito la discussione arrivava alle colonne senza sapere
a quale domanda rispondessero. Qui si antepone la spiegazione e si posticipa un esempio
completo, con dati veri.

⚠️ I nomi di colonna dell'esempio sono verificati sul codice, non plausibili:
`ATTO_NASCITA.ID_DICHIARANTE` (AttoNascita.java:83), `ATTO_NASCITA_SOGGETTO.FLG_NATO_MORTO`
(:59) e `.FLG_MORTO_PREDENUNCIA` (:65), chiave di giunzione `ID_ATTO_NASCITA`. Il lato SIPO
dei campi viene dal foglio compilato a mano di `Dic_Nasc_001`.
"""
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(BASE, 'Documenti finali', 'ANALISI_Integrazione-ANSC_v3.14.docx')

INTRO = [
    ('p', 'Prima del dettaglio delle tabelle conviene dire che cosa la configurazione faccia, '
          'perché è una sola cosa: mettere il componente in condizione di rispondere a quattro '
          'domande davanti a un atto che l’operatore ha appena compilato in SIPO. Quale caso '
          'd’uso di ANSC sta formando; da dove si prende ciascun dato che il payload richiede; '
          'quali documenti vanno allegati; quali diciture vanno inserite nell’atto. Nessuna di '
          'queste risposte è nel codice: stanno tutte in tabelle, e sono i funzionari del '
          'Comune a scriverle.'),
    ('p', 'Le tabelle che rispondono sono cinque, e si leggono nell’ordine in cui le domande '
          'si presentano.'),
    ('tab', [['Tabella', 'A quale domanda risponde'],
             ['ANSC_CFG_UC',
              'Quali casi d’uso di ANSC il Comune adotta, e per ciascuno a quale Modello di '
              'atto si applica, con quale interfaccia si deposita e con quale priorità va '
              'considerato rispetto agli altri UC dello stesso Modello. Una riga per caso '
              'd’uso.'],
             ['ANSC_CFG_UC_CONDIZIONE',
              'Quando quel caso d’uso è quello giusto. È un’interrogazione sui dati che SIPO '
              'ha già registrato per l’atto: il primo UC la cui condizione risponde vince.'],
             ['ANSC_CFG_CAMPO',
              'Quali percorsi del modello evento valgono per quell’UC, se siano obbligatori e '
              'da quale tabella e colonna di SIPO si prenda il valore.'],
             ['ANSC_CFG_ALLEGATO',
              'Quali documenti quell’UC richiede, quali sono obbligatori e a quale condizione.'],
             ['ANSC_CFG_FORMULA',
              'Quali diciture ministeriali sono previste per quell’UC, quali obbligatorie e '
              'quali il Comune sceglie di offrire all’ufficiale.']]),
    ('p', 'Le ultime tre pendono dall’UC e non dal Modello, ed è la ragione per cui la '
          'determinazione viene prima di tutto il resto: finché non si sa quale caso d’uso si '
          'sta formando non si sa neppure quali campi siano obbligatori né quale certificato '
          'serva. Il percorso completo, dall’atto salvato in SIPO al payload pronto per il '
          'deposito, è quindi questo.'),
    ('v', ('Si parte dal tipo atto.',
           'L’atto che l’operatore ha compilato porta il proprio tipo, e da CONF_TIPO_ATTI '
           'discendono il Modello e la maschera. È l’unico aggancio con la configurazione che '
           'SIPO già possiede.')),
    ('v', ('Si determina il caso d’uso.',
           'Fra gli UC configurati per quel Modello, in ordine di priorità, si valutano le '
           'condizioni sui dati dell’atto: la prima che risponde stabilisce l’UC. Se nessuna '
           'risponde la lavorazione si ferma qui, con un messaggio che dice quale Modello non '
           'ha trovato un caso d’uso.')),
    ('v', ('Si verifica ciò che l’UC richiede.',
           'Letti i campi dichiarati per quell’UC, si controlla che i valori ci siano e siano '
           'validi; letti gli allegati, che i documenti richiesti siano stati caricati. È il '
           'pre-filtro: nessun servizio di ANSC è ancora stato chiamato.')),
    ('v', ('Si costruisce il payload.',
           'La colonna SIPO di ciascun campo dice da dove prendere il valore; le regole di '
           'generazione calcolano i derivati; le formule adottate accompagnano l’atto.')),
    ('v', ('Si deposita e si firma.',
           'Solo a questo punto si chiama ANSC, e l’ufficiale firma con il proprio OTP.')),
    ('p', 'Chi scrive tutto questo sono i funzionari, dal back-office. Poiché le righe sono '
          'decine di migliaia, l’importazione dal mapping ufficiale le prepara e l’operatore '
          'le esamina: ogni riga porta con sé se sia stata soltanto proposta o se qualcuno '
          'l’abbia guardata, e la reimportazione successiva tocca le sole righe che nessuno ha '
          'ancora esaminato.'),
]

ESEMPIO = [
    ('p', 'Per rendere concreto quanto precede si riporta la configurazione completa di un '
          'caso d’uso, quello osservato anche sulla web app di ANSC: la dichiarazione di '
          'nascita di un bambino nato vivo, resa dal padre entro dieci giorni, in costanza di '
          'matrimonio. In ANSC è l’UC 11111000, codice motore Dic_Nasc_001.'),
    ('p', 'La riga di ANSC_CFG_UC dichiara che il Comune adotta quel caso d’uso e a quale '
          'Modello si applica.'),
    ('tab', [['Colonna', 'Valore'],
             ['COD_UC_ANSC', '11111000'],
             ['COD_TIPO_EVENTO / COD_TIPO_OPERAZIONE', 'NASCITA / CREAZIONE'],
             ['ID_MODELLO_ATTO', '30'],
             ['ID_CONF_TIPO_ATTO', '1515'],
             ['MASCHERA_UI', 'attoNascitaTipo01'],
             ['SERVIZIO_ANSC / ID_MAPPER', 'R009 / NascitaDichiarazione'],
             ['NUM_PRIORITA', '10 — prima di 11111100 (nato morto) e 11111200 (nato vivo e '
                              'poi deceduto), che condividono il Modello 30'],
             ['FLG_TRASCRIZIONE / FLG_FIRMA / FLG_ATTIVO', 'N / S / S']]),
    ('p', 'La condizione stabilisce quando quel caso d’uso è quello giusto, interrogando i '
          'dati che SIPO ha già scritto. I due discriminanti stanno sul soggetto e non '
          'sull’atto, ed è la ragione per cui la condizione deve poter congiungere due '
          'tabelle: con una terna campo-operatore-valore non si esprimerebbe.'),
    ('ddl', ['SELECT 1',
             '  FROM MATR_USR.ATTO_NASCITA an',
             '  JOIN MATR_USR.ATTO_NASCITA_SOGGETTO ans',
             '    ON ans.ID_ATTO_NASCITA = an.ID_ATTO_NASCITA',
             ' WHERE an.ID_ATTO_NASCITA = :id_atto',
             "   AND an.ID_DICHIARANTE = 1                          -- padre",
             "   AND NVL(ans.FLG_NATO_MORTO, 'N') = 'N'",
             "   AND NVL(ans.FLG_MORTO_PREDENUNCIA, 'N') = 'N'"]),
    ('p', 'La descrizione che accompagna la condizione, obbligatoria, dice in lingua corrente '
          'ciò che la query riconosce: «dichiarazione resa dal padre, bambino nato vivo e non '
          'deceduto prima della denuncia».'),
    ('p', 'I campi dichiarati per quell’UC sono 207 nel mapping ufficiale; se ne riporta un '
          'estratto con il lato SIPO come risulta dalla ricognizione.'),
    ('tab', [['Campo ANSC', 'Campo SIPO', 'Obbl.', 'Origine'],
             ['evento.numeroatto', 'ATTO.NUM_COMUNALE_ANSC', 'S', 'Modificato'],
             ['evento.dataformazione', 'ATTO.DATA_RILASCIO', 'S', 'Confermato'],
             ['evento.tipoDichiarante', 'ATTO_NASCITA.ID_DICHIARANTE', 'S', 'Confermato'],
             ['evento.madre.cognome', 'SOGGETTO.COGNOME', 'N', 'Confermato'],
             ['evento.madre.nome', 'SOGGETTO.NOME', 'S', 'Confermato'],
             ['evento.madre.idStatoNascita', 'SOGGETTO.DETTAGLIO_STATOCIVILE (nodo XML)', 'S',
              'Modificato'],
             ['evento.datiDiNascita.luogoFiliazione', 'ATTO_NASCITA_SOGGETTO.ID_OSPEDALE', 'S',
              'Modificato'],
             ['evento.intestatari[0].idStatoNascita', '— (valore fisso: Italia)', 'S',
              'Inserito']]),
    ('p', 'Gli allegati previsti sono cinque, dei quali uno obbligatorio a condizione.'),
    ('tab', [['Documento', 'Obbl.', 'Condizione'],
             ['Attestazione di nascita', 'S',
              'evento.datiDiNascita.tipoAccertamento = 1'],
             ['Constatazione di avvenuto parto', 'N',
              'evento.datiDiNascita.tipoAccertamento = 2'],
             ['Dichiarazione di nascita sostitutiva resa da dichiarante', 'N',
              'evento.datiDiNascita.tipoAccertamento = 3'],
             ['Autorizzazione del tribunale', 'N', '—'],
             ['Documento autorizzativo', 'N', '—']]),
    ('p', 'Le formule previste sono due, entrambe obbligatorie e quindi sempre adottate. Sono '
          'anche il punto in cui questo caso d’uso si distingue dai due fratelli che '
          'condividono il Modello 30: il nato morto porta la 41 al posto della 1, il nato vivo '
          'e poi deceduto aggiunge la 40. Un errore nella determinazione non produrrebbe '
          'alcun rifiuto da parte di ANSC — i campi sono quasi identici — ma formerebbe l’atto '
          'con la dicitura sbagliata.'),
    ('tab', [['Formula', 'Obbligatoria', 'Adottata', 'Campo di testo libero'],
             ['1', 'S', 'S', '—'],
             ['14', 'S', 'S', '—']]),
    ('p', 'Messo tutto insieme, davanti a un atto di nascita del Modello 30 il componente '
          'scorre gli UC configurati in ordine di priorità, esegue la condizione del primo e '
          'la trova soddisfatta, e da quel momento sa che deve verificare 207 campi secondo '
          'l’obbligatorietà dichiarata per 11111000, pretendere l’attestazione di nascita se '
          'l’accertamento è di tipo 1, comporre il payload prendendo i valori dalle colonne '
          'indicate e accompagnare l’atto con le formule 1 e 14. Nessuno di questi quattro '
          'esiti è scritto nel codice del componente.'),
]


def blocchi(doc, elenco, modello):
    fuori = []
    for tipo, contenuto in elenco:
        fuori.append((tipo if tipo != 'tab' else 'tab',
                      contenuto if tipo != 'tab' else (contenuto, modello)))
    return fuori


def applica(doc):
    fatti = []
    modello = D.trova_tabella(doc, 'Colonna', 'Tipo', 'Note')
    ancora = D.h(doc, 3, 'I tre mondi della configurazione')
    prima = ancora._p

    D.para(doc, prima, 'Come funziona la configurazione', stile='Heading 3')
    for tipo, contenuto in INTRO:
        if tipo == 'p':
            D.para(doc, prima, contenuto)
        elif tipo == 'v':
            D.voce(doc, prima, *contenuto)
        elif tipo == 'tab':
            D.tabella(doc, prima, contenuto, modello=modello)
    fatti.append(f'capitoletto «Come funziona la configurazione» ({len(INTRO)} blocchi)')
    return fatti, modello


def esempio(doc, modello):
    """L'esempio SOSTITUISCE quello vecchio, che era parziale e portava un valore impossibile.

    ⚠️ L'esempio delle versioni precedenti dichiarava «Modello = DICH_ABITAZIONE» in una
    colonna VARCHAR2(5): era rimasto alla semantica della v2.x, quando quella colonna si
    chiamava COD_CASISTICA ed era una stringa di trenta caratteri. Rimuoverlo è parte della
    correzione, non un effetto collaterale.
    """
    fatti = []
    from docx.text.paragraph import Paragraph
    corpo = list(doc.element.body)
    inizio = next(i for i, ch in enumerate(corpo)
                  if ch.tag.endswith('}p')
                  and Paragraph(ch, doc).text.strip().startswith('Esempio (morte, creazione'))
    fine = next(i for i in range(inizio + 1, len(corpo))
                if corpo[i].tag.endswith('}p')
                and Paragraph(corpo[i], doc).style.name.startswith('Heading'))
    prima = corpo[fine]
    for ch in corpo[inizio:fine]:
        ch.getparent().remove(ch)
    fatti.append(f'rimosso l’esempio superato (morte/DICH_ABITAZIONE, {fine - inizio} elementi)')
    D.para(doc, prima, 'Un esempio completo: la dichiarazione di nascita resa dal padre',
           stile='Heading 3')
    for tipo, contenuto in ESEMPIO:
        if tipo == 'p':
            D.para(doc, prima, contenuto)
        elif tipo == 'ddl':
            D.ddl(doc, prima, contenuto)
        elif tipo == 'tab':
            D.tabella(doc, prima, contenuto, modello=modello)
    fatti.append(f'esempio completo di configurazione ({len(ESEMPIO)} blocchi)')
    return fatti


if __name__ == '__main__':
    doc = docx.Document(DOC)
    fatti, modello = applica(doc)
    fatti += esempio(doc, modello)
    for f in fatti:
        print('  ·', f)
    doc.save(DOC)
    print('salvato')
