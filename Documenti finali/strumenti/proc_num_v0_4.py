# -*- coding: utf-8 -*-
"""PROCESSO_Numerazione-Comunale v0.4, dalla v0.3 dell'utente (27/10/2026).

Il capitolo «Il servizio be-numerazione-comunale» era un testo a spaziatura fissa incollato
(sottolineature con «=» e «-», colonne allineate a spazi). Lo riscrive per la consultazione da
parte degli sviluppatori, senza togliere né aggiungere contenuti: quadro d'insieme, tabella
delle operazioni, stati, oggetto di risposta e una sezione per operazione con tabelle dei
parametri, esempio e tabella degli errori. L'heading del capitolo resta quello originale,
perché porta il commento di Word.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/proc_num_v0_4.py
"""
import os
import sys

import docx
from docx.text.paragraph import Paragraph

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import docx_comune as D  # noqa: E402

BASE = os.path.dirname(QUI)
SRC = os.path.join(BASE, 'PROCESSO_Numerazione-Comunale_SIPO-ANSC_v0.3.docx')
OUT = os.path.join(BASE, 'PROCESSO_Numerazione-Comunale_SIPO-ANSC_v0.4.docx')
CAPITOLO = 'Il servizio be-numerazione-comunale'

DTO = '{ "idRichiesta": 120, "operatore": "admin", "dataRichiesta": "26/10/2026",'
DTO_501 = '"anno": 2026, "numero": 501, "idAnsc": null, "stato": "1", "idAttoSipo": null }'
DTO_502 = '"anno": 2026, "numero": 502, "idAnsc": null, "stato": "1", "idAttoSipo": null }'

# (tipo, contenuto): p paragrafo · h2/h3 heading · tab (righe, larghezze) · mono righe · v voce
BLOCCHI = [
    ('p', 'Il servizio espone le operazioni per staccare numeri comunali consecutivi, '
          'cercarli e cambiarne lo stato. Le convenzioni comuni a tutte le operazioni sono '
          'le seguenti.'),
    ('tab', ([['Elemento', 'Valore'],
              ['Base path', '/api/v1/numerazione-comunale'],
              ['Content-Type', 'application/json'],
              ['Chiave di un numero', 'La coppia (idRichiesta, numero). Nei corpi delle '
                                      'operazioni PUT la stessa coppia si chiama '
                                      '(idPrenotazioneAtti, numeroAttoComunale).']],
             [1.9, 4.6])),

    ('h2', 'Le operazioni in sintesi'),
    ('tab', ([['#', 'Operazione', 'Che cosa fa', 'Esito positivo', 'Errori'],
              ['1', 'POST /richiesta', 'Stacca uno o più numeri consecutivi e li registra '
                                       'in stato 1 (disponibile).',
               '200 OK, lista di NumerazioneComunaleRispostaDTO', '400'],
              ['2', 'GET /ricerca', 'Ricerca paginata dei numeri staccati.',
               '200 OK, PagedModel<NumerazioneComunaleRispostaDTO>', '400'],
              ['3', 'PUT /utilizza', 'Porta un numero allo stato 2 (utilizzato) e registra '
                                     'l’atto SIPO che lo ha usato.',
               '204 No Content', '400, 404'],
              ['4', 'PUT /scarta', 'Porta un numero allo stato 3 (scartato).',
               '204 No Content', '400, 404']],
             [0.3, 1.2, 2.4, 1.8, 0.8])),

    ('h2', 'Gli stati del numero'),
    ('tab', ([['Codice', 'Stato', 'Come ci si arriva'],
              ['1', 'disponibile', 'Alla creazione: un numero nasce sempre in questo stato '
                                   '(POST /richiesta).'],
              ['2', 'utilizzato', 'PUT /utilizza.'],
              ['3', 'scartato', 'PUT /scarta.'],
              ['4', 'evento acquisito', 'Non viene impostato da questi servizi.']],
             [0.8, 1.5, 4.2])),

    ('h2', 'L’oggetto di risposta: NumerazioneComunaleRispostaDTO'),
    ('p', 'Lo restituiscono POST /richiesta (uno per numero staccato) e GET /ricerca (dentro '
          'la pagina di risultati).'),
    ('tab', ([['Campo', 'Tipo', 'Descrizione'],
              ['idRichiesta', 'Long', 'PRENOTAZIONE_ATTI.ID_PRENOTAZIONE_ATTI.'],
              ['operatore', 'String', 'Operatore della richiesta (oggi sempre "admin").'],
              ['dataRichiesta', 'String', 'Formato gg/MM/yyyy.'],
              ['anno', 'Integer', 'Anno di numerazione.'],
              ['numero', 'Integer', 'Numero comunale.'],
              ['idAnsc', 'String', 'Identificativo ANSC; null in risposta a /richiesta.'],
              ['stato', 'String', 'Codice dello stato (vedi «Gli stati del numero»).'],
              ['idAttoSipo', 'Long', 'DATI_ATTO_ESTERNO.ID_ATTO_SIPO; null se il numero non è '
                                     'assegnato a un atto.']],
             [1.5, 0.9, 4.1])),

    # ── 1 ──
    ('h2', 'POST /richiesta – stacco dei numeri'),
    ('p', 'Stacca uno o più numeri comunali consecutivi, registra la richiesta e crea un '
          'record per ogni numero in stato 1 (disponibile). Tutto avviene in un’unica '
          'transazione: in caso di errore il contatore non avanza.'),
    ('h3', 'Corpo della richiesta'),
    ('p', 'Il corpo è obbligatorio, con entrambi i campi.'),
    ('tab', ([['Campo', 'Tipo', 'Obbligatorio', 'Vincolo'],
              ['anno', 'Integer', 'Sì', 'Da 2023 a 9999'],
              ['numeroElementi', 'Integer', 'Sì', 'Da 1 a 999']],
             [1.7, 1.0, 1.1, 2.7])),
    ('h3', 'Esempio'),
    ('p', 'Richiesta:'),
    ('mono', ['{ "anno": 2026, "numeroElementi": 3 }']),
    ('p', 'Risposta 200 OK, una voce per ogni numero staccato:'),
    ('mono', ['[',
              '  ' + DTO,
              '    ' + DTO_501[:-2] + ' },',
              '  ' + DTO,
              '    ' + DTO_502,
              ']']),
    ('h3', 'Errori'),
    ('tab', ([['HTTP', 'Condizione', 'Messaggio'],
              ['400', 'Corpo mancante', '—'],
              ['400', 'anno mancante', '"Anno obbligatorio"'],
              ['400', 'numeroElementi mancante', '"Numero elementi obbligatorio"'],
              ['400', 'anno fuori intervallo', '"L\'anno deve essere tra 2023 e 9999"'],
              ['400', 'numeroElementi fuori intervallo',
               '"Il numero di elementi deve essere tra 1 e 999"']],
             [0.7, 2.4, 3.4])),

    # ── 2 ──
    ('h2', 'GET /ricerca – ricerca dei numeri'),
    ('p', 'Ricerca paginata dei numeri staccati. Ogni filtro non valorizzato viene ignorato.'),
    ('h3', 'Parametri di query'),
    ('tab', ([['Parametro', 'Tipo', 'Default', 'Significato'],
              ['anno', 'Integer', '—', 'Filtro.'],
              ['stato', 'String', '—', 'Filtro (1, 2, 3, 4).'],
              ['idRichiesta', 'Long', '—', 'Filtro.'],
              ['idAttoSipo', 'Long', '—', 'Filtro.'],
              ['numero', 'Integer', '—', 'Filtro.'],
              ['richiestaDa', 'LocalDate (yyyy-MM-dd)', '—',
               'Data della richiesta maggiore o uguale (inclusa).'],
              ['richiestaA', 'LocalDate (yyyy-MM-dd)', '—',
               'Data della richiesta minore o uguale (inclusa l’intera giornata).'],
              ['operatore', 'String', '—', 'Filtro per uguaglianza esatta.'],
              ['pageOffset', 'int', '0', 'Numero di pagina (base 0); deve essere ≥ 0.'],
              ['pageSize', 'int', '10', 'Deve essere ≥ 1.']],
             [1.3, 1.7, 0.8, 2.7])),
    ('h3', 'Esempio'),
    ('p', 'Richiesta:'),
    ('mono', ['GET /api/v1/numerazione-comunale/ricerca?anno=2026&stato=1&pageOffset=0'
              '&pageSize=20']),
    ('p', 'Risposta 200 OK, PagedModel<NumerazioneComunaleRispostaDTO>:'),
    ('mono', ['{',
              '  "content": [',
              '    ' + DTO,
              '      ' + DTO_501,
              '  ],',
              '  "page": { "size": 20, "number": 0, "totalElements": 1, "totalPages": 1 }',
              '}']),
    ('h3', 'Errori'),
    ('tab', ([['HTTP', 'Condizione'],
              ['400', 'pageOffset negativo o pageSize minore di 1'],
              ['400', 'richiestaDa successiva a richiestaA']],
             [0.7, 5.8])),

    # ── 3 ──
    ('h2', 'PUT /utilizza – numero utilizzato'),
    ('p', 'Segna il numero come utilizzato (stato 2) e, se indicato, registra l’atto SIPO che '
          'lo ha usato.'),
    ('h3', 'Corpo della richiesta'),
    ('tab', ([['Campo', 'Tipo', 'Obbligatorio', 'Significato'],
              ['idPrenotazioneAtti', 'Long', 'Sì', 'Corrisponde a idRichiesta.'],
              ['numeroAttoComunale', 'Integer', 'Sì', 'Corrisponde a numero.'],
              ['idAttoSipo', 'Long', 'No', 'Atto che ha usato il numero.']],
             [1.8, 0.9, 1.1, 2.7])),
    ('p', 'Nota: idAttoSipo viene sempre scritto sul record; se è omesso nel corpo, il valore '
          'salvato è null.'),
    ('h3', 'Esempio'),
    ('p', 'Richiesta:'),
    ('mono', ['{ "idPrenotazioneAtti": 120, "numeroAttoComunale": 501, "idAttoSipo": 98765 }']),
    ('p', 'Risposta: 204 No Content.'),
    ('h3', 'Errori'),
    ('tab', ([['HTTP', 'Condizione'],
              ['400', 'idPrenotazioneAtti o numeroAttoComunale mancanti'],
              ['404', 'Numero non trovato per quella richiesta']],
             [0.7, 5.8])),

    # ── 4 ──
    ('h2', 'PUT /scarta – numero scartato'),
    ('p', 'Segna il numero come scartato (stato 3): non verrà usato.'),
    ('h3', 'Corpo della richiesta'),
    ('tab', ([['Campo', 'Tipo', 'Obbligatorio', 'Significato'],
              ['idPrenotazioneAtti', 'Long', 'Sì', 'Corrisponde a idRichiesta.'],
              ['numeroAttoComunale', 'Integer', 'Sì', 'Corrisponde a numero.']],
             [1.8, 0.9, 1.1, 2.7])),
    ('h3', 'Esempio'),
    ('p', 'Richiesta:'),
    ('mono', ['{ "idPrenotazioneAtti": 120, "numeroAttoComunale": 502 }']),
    ('p', 'Risposta: 204 No Content.'),
    ('h3', 'Errori'),
    ('tab', ([['HTTP', 'Condizione'],
              ['400', 'Campi obbligatori mancanti'],
              ['404', 'Numero non trovato per quella richiesta']],
             [0.7, 5.8])),
]


def main():
    if os.path.exists(OUT):
        raise SystemExit('esiste già: ' + OUT)
    doc = docx.Document(SRC)
    elementi = D.sezione(doc, CAPITOLO, livello=1)
    assert elementi, 'capitolo non trovato'
    testa, corpo = elementi[0], elementi[1:]
    for ch in corpo:
        if D.ha_commenti(ch):
            raise SystemExit('un elemento da sostituire porta un commento')
    dopo = corpo[-1].getnext()
    for ch in corpo:
        ch.getparent().remove(ch)
    modello = D.trova_tabella(doc, 'Campo', 'Tipo', 'Descrizione', 'Alimentazione')
    for tipo, c in BLOCCHI:
        if tipo == 'p':
            D.para(doc, dopo, c)
        elif tipo == 'h2':
            D.para(doc, dopo, c, stile='Heading 2')
        elif tipo == 'h3':
            D.para(doc, dopo, c, stile='Heading 3')
        elif tipo == 'tab':
            D.tabella(doc, dopo, c[0], modello, larghezze=c[1])
            D.para(doc, dopo, '')
        elif tipo == 'mono':
            D.ddl(doc, dopo, c)
            D.para(doc, dopo, '')
    D.storia(doc, '27/10/2026', '0.4', 'Il servizio be-numerazione-comunale',
             'Capitolo riscritto per la consultazione da parte degli sviluppatori, a contenuti '
             'invariati: convenzioni comuni, tabella delle operazioni, stati del numero, '
             'oggetto di risposta e una sezione per operazione con parametri, esempio ed '
             'errori in tabella.')
    D.frontespizio(doc, '0.4', 'PROCESSO_Numerazione-Comunale_SIPO-ANSC_v0.4')
    doc.save(OUT)
    print('scritto:', OUT)


if __name__ == '__main__':
    main()
