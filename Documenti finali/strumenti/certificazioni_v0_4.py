# -*- coding: utf-8 -*-
"""v0.4 di «ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC» (11/11/2026).

Si modifica il FILE REALE della v0.3 salvata dall'utente. Richiesta: aggiungere il flusso
applicativo attuale della ricerca dell'atto a partire dall'intestatario (ufficio certificati,
area «Stato Civile»), come descritto in conversazione.

Fatti (cert-be, anagrafe-entities, sipo-root/sql):
  * intestatario = ANAG_USR.SOGGETTO.ID_SOGGETTO → CERTIFICATI.ID_SOGGETTO_INT;
  * R_CONF_CERT_ANPR: 3→5, 5→1, 6→3, 25→2 → ANPR 3002 all'aggiunta
    (PraticaCertificatiController:1196); trovato → 6001, SIPO non cerca l'atto; non trovato
    (o morte cancellata senza decesso) → AttoRepository: findAttoNascitaResRomaBySoggetto
    (NASCITA.ID_COMUNE = 6333), findAttoMorteBySoggetto, findAttoMatrimonioBySoggetto,
    findAttoUnioneCivileBySoggetto, tutte con numero, anno e parte non nulli → anpr = 0;
  * ramo locale (CertificatiController:823-985, 1109-1135): SOGGETTO.ID_NASCITA → NASCITA.
    ID_ATTO; SOGGETTO.ID_MORTE → MORTE.ID_ATTO; MATRIMONIO (marito o moglie, FLAG_ANPR ≠ 'N',
    il più recente) e UNIONECIVILE (primo o secondo, la più recente) → ID_ATTO;
  * DocCertificatoSempliceComuneRoma:110-160 stampa l'atto di nascita e l'atto dell'evento,
    ID_ATTO_ANSC se manca NUMERO_ATTO;
  * ATTO esiste in ANAG_USR (Atto.java, con ID_ATTO_ANSC…) e in MATR_USR (AttoMatr.java, solo
    i riferimenti ANSC dell'atto trascritto); la DDL di collaudo di ANAG_USR.ATTO (19 colonne)
    non ha le colonne ANSC.
Il rilievo sulla precedenza dell'OR in findAttoMatrimonioBySoggetto NON entra nel documento
(i difetti del codice sono un tema separato, decisione dell'utente).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/certificazioni_v0_4.py
"""
import os
import sys

import docx
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from genera_testo_libero import h, par, voce, tabella, figura   # noqa: E402
import diagrammi_certificazioni as DC   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC_v0.3.docx')
NOME = 'ANALISI_Certificazioni-Stato-Civile_SIPO-ANSC_v0.4'
OUT = os.path.join(FIN, NOME + '.docx')
DATA = '11/11/2026'

d = docx.Document(SRC)
body = d.element.body
fatti = []


def innesta_prima(prima, scrivi):
    sect = body.find(qn('w:sectPr'))
    visti = set(body.iterchildren())
    scrivi()
    nuovi = [ch for ch in body.iterchildren() if ch not in visti and ch is not sect]
    for ch in nuovi:
        prima.addprevious(ch)
    return nuovi


def paragrafo(inizio, stile=None):
    pp = [p for p in d.paragraphs if p.text.startswith(inizio)
          and (stile is None or p.style.name == stile)]
    if len(pp) != 1:
        raise SystemExit('paragrafo non univoco (%d): %s' % (len(pp), inizio))
    return pp[0]


def tab(*intest):
    for t in d.tables:
        if [c.text.strip() for c in t.rows[0].cells][:len(intest)] == list(intest):
            return t
    raise SystemExit('tabella non trovata: %s' % (intest,))


def S(v, n, a, e):
    D.sostituisci(d, v, n, attese=a, etichetta=e, fatti=fatti)


def flusso():
    h(d, 2, 'Dall’intestatario all’atto: il flusso della ricerca')
    par(d, 'Nell’ufficio certificati l’operatore non sceglie un atto: sceglie la persona. '
           'L’atto si ricava dalle relazioni della persona nello schema ANAG_USR, per strade '
           'diverse secondo il certificato e il momento, l’aggiunta alla pratica oppure '
           'l’emissione. La figura riassume il flusso; i passi sono descritti di seguito.')
    figura(d, DC.ricerca_atto(), 6.5,
           'Figura 5 — Ufficio certificati, area «Stato Civile»: dall’intestatario all’atto.')
    voce(d, '1. L’intestatario.', 'L’operatore lo trova con «Cerca» nella pagina «Nuovo '
         'certificato a sportello»; la pratica ne conserva `ANAG_USR.SOGGETTO.ID_SOGGETTO` in '
         '`CERTIFICATI.ID_SOGGETTO_INT`.')
    voce(d, '2. Il certificato si chiede ad ANPR?', 'Lo dice la tabella `R_CONF_CERT_ANPR`. '
         'Nell’area «Stato Civile» passano da ANPR quattro certificati: 5 nascita, 6 '
         'matrimonio, 25 morte, 3 cittadinanza. Gli altri si producono sempre in locale.')
    voce(d, '3. La ricerca della persona in ANPR.', 'Per i quattro certificati, all’aggiunta '
         'alla pratica cert-be cerca la persona in ANPR con l’operazione 3002, inviando codice '
         'fiscale e dati anagrafici ma non il codice individuale (PraticaCertificatiController, '
         'riga 1196). Se ANPR la trova, il certificato lo emette ANPR con l’operazione 6001 e '
         'SIPO non cerca alcun atto: il contenuto lo compone ANPR dalla scheda della persona.')
    voce(d, '4. La verifica dell’atto in locale.', 'Se ANPR non trova la persona (per la morte '
         'anche quando la trova cancellata ma senza i dati del decesso), cert-be cerca l’atto in '
         'ANAG_USR con le interrogazioni di `AttoRepository`. Tutte richiedono numero, anno e '
         'parte dell’atto valorizzati; se l’atto c’è, la pratica annota «anpr = 0» e il '
         'certificato seguirà il ramo locale, altrimenti la richiesta è respinta con '
         '«Impossibile rilasciare il certificato».')
    tabella(d, [
        ['Certificato', 'Interrogazione', 'Come trova l’atto'],
        ['5 Nascita', 'findAttoNascitaResRomaBySoggetto', 'ATTO ← NASCITA ← SOGGETTO della '
         'persona, con NASCITA.ID_COMUNE = 6333 (Roma).'],
        ['25 Morte', 'findAttoMorteBySoggetto', 'ATTO ← MORTE ← SOGGETTO della persona.'],
        ['6 Matrimonio', 'findAttoMatrimonioBySoggetto', 'ATTO del matrimonio più recente in '
         'cui la persona è marito o moglie.'],
        ['44 Unione civile', 'findAttoUnioneCivileBySoggetto', 'ATTO dell’unione più recente '
         'in cui la persona è primo o secondo soggetto.'],
    ], [1.3, 2.4, 2.8])
    voce(d, '5. Il ramo locale.', 'All’anteprima e all’emissione l’atto si raggiunge seguendo '
         'le relazioni della persona caricate con l’intestatario (CertificatiController, righe '
         '823-985 e 1109-1135):')
    tabella(d, [
        ['Certificato', 'Catena fino all’atto'],
        ['Nascita (5, 18)', 'SOGGETTO.ID_NASCITA → NASCITA.ID_ATTO → ATTO'],
        ['Morte (25)', 'SOGGETTO.ID_MORTE → MORTE.ID_ATTO → ATTO'],
        ['Matrimonio (6, 63)', "MATRIMONIO in cui la persona è ID_SOGGETTO_MARITO o "
         "ID_SOGGETTO_MOGLIE, con FLAG_ANPR diverso da 'N', il più recente per DATA_EVENTO → "
         "ID_ATTO → ATTO"],
        ['Unione civile (44)', 'UNIONECIVILE in cui la persona è ID_SOGGETTO_PRIMO o '
         'ID_SOGGETTO_SECONDO, la più recente per DATA_EVENTO → ID_ATTO → ATTO'],
    ], [1.6, 4.9])
    voce(d, '6. Che cosa stampa il certificato.', 'Il modello «Certificato_semplice» riporta '
         'sempre l’atto di nascita della persona e, per matrimonio, unione civile e morte, '
         'l’atto dell’evento: numero, parte, serie, anno e comune di trascrizione. Se il numero '
         'dell’atto è vuoto stampa `ATTO.ID_ATTO_ANSC` (DocCertificatoSempliceComuneRoma, '
         'righe 110-160).')

    par(d, 'Tre caratteristiche del flusso contano per l’integrazione con ANSC:')
    voce(d, 'Verifica ed emissione leggono l’atto per due strade.', 'La verifica all’aggiunta '
         'usa le interrogazioni di `AttoRepository`, con le loro condizioni (comune di Roma per '
         'la nascita, numero, anno e parte); l’emissione segue le relazioni della persona, che '
         'quelle condizioni non hanno. L’instradamento verso ANSC va deciso su un atto solo, lo '
         'stesso nei due momenti (CE-20).')
    voce(d, 'Per matrimonio e unione civile vale l’evento più recente.', 'Un certificato su un '
         'evento precedente della stessa persona non si raggiunge da questo flusso.')
    voce(d, 'La tabella ATTO è quella di ANAG_USR.', 'cert-be si collega come ANAG_USR, quindi '
         'legge `ANAG_USR.ATTO`, che non è la tabella ATTO dello stato civile:')
    tabella(d, [
        ['', 'ANAG_USR.ATTO', 'MATR_USR.ATTO'],
        ['Entità', 'Atto (anagrafe-entities)', 'AttoMatr (matrim-entities)'],
        ['Chi la legge', 'I back-end collegati come ANAG_USR, fra cui cert-be',
         'I back-end collegati come MATR_USR, fra cui statocivile-be e i moduli d’area'],
        ['A che cosa è collegata', 'Agli eventi della persona: NASCITA, MORTE, MATRIMONIO, '
         'UNIONECIVILE', 'Alla pratica e all’atto redatto dallo sportello di stato civile'],
        ['Identificativo ANSC', 'Quello dell’atto stesso: ID_ATTO_ANSC, ANNO_ANSC, '
         'NUMERO_NAZIONALE, NUMERO_COMUNALE, DATA_ANSC', 'Solo i riferimenti dell’atto '
         'trascritto, formato altrove (ATTO_TRASCR_NUMERO_ANSC e affini)'],
    ], [1.5, 2.5, 2.5])
    par(d, 'La colonna su cui decidere l’instradamento è quindi `ANAG_USR.ATTO.ID_ATTO_ANSC`. '
           'Le colonne ANSC risultano dall’entità Java ma non dalla DDL di collaudo di '
           '`ANAG_USR.ATTO` (19 colonne, nessuna ANSC), che è anteriore: la loro presenza in '
           'esercizio va confermata (CE-21). Chi le valorizzi per gli atti formati con il nuovo '
           'percorso è OP-29 di [R1].')


if __name__ == '__main__':
    S('Figura 6 — La sequenza', 'Figura 7 — La sequenza', 1, 'figura 6 → 7')
    S('Figura 5 — Dalla richiesta', 'Figura 6 — Dalla richiesta', 1, 'figura 5 → 6')
    innesta_prima(paragrafo('Come intervenire per permettere la visualizzazione',
                            'Heading 2')._p, flusso)
    fatti.append('sezione «Dall’intestatario all’atto: il flusso della ricerca» con la figura 5')
    S('La logica di instradamento è nel capitolo', 'Il flusso di oggi è nella sezione '
      'precedente; la logica di instradamento è nel capitolo', 1, 'rinvio alla sezione nuova')

    rif = tab('#', 'Riferimento', 'Natura')
    s4 = [r for r in rif.rows if r.cells[0].text == '[S4]'][0]
    D.riscrivi_cella(s4.cells[1], s4.cells[1].text.rstrip('.') + '; PraticaCertificatiController '
                     '(verifica in ANPR), AttoRepository e le entità Atto, Nascita, Morte, '
                     'Matrimonio, Unionecivile di common/anagrafe-entities; AttoMatr di '
                     'common/matrim-entities.')
    ce = tab('#', 'Questione', 'A chi spetta')
    for riga in [
        ('CE-20', 'Su quale atto decidere l’instradamento verso ANSC nell’ufficio certificati: '
         'la verifica all’aggiunta e l’emissione raggiungono l’atto per strade diverse, e per '
         'matrimonio e unione civile vale sempre l’evento più recente. Serve una sola regola, '
         'applicata nei due momenti.', 'Referenti SIPO / Architettura'),
        ('CE-21', 'Presenza in esercizio delle colonne ANSC di ANAG_USR.ATTO (ID_ATTO_ANSC, '
         'ANNO_ANSC, NUMERO_NAZIONALE, NUMERO_COMUNALE, DATA_ANSC): l’entità le mappa, la DDL '
         'di collaudo no.', 'DBA SIPO'),
    ]:
        D.clona_riga(ce, riga)
    fatti.append('[S4] esteso, CE-20 e CE-21')

    for f in D.frontespizio(d, '0.4', NOME, DATA):
        fatti.append(f)
    D.storia(d, DATA, '0.4', 'L’attuale processo di richiesta dei certificati · Punti aperti',
             'Nuova sezione sul flusso con cui l’ufficio certificati ricava l’atto '
             'dall’intestatario (ANPR 3002 e 6001, verifica locale, catene in ANAG_USR, '
             'ANAG_USR.ATTO e MATR_USR.ATTO), con figura; figure successive rinumerate; CE-20 e '
             'CE-21.')
    d.save(OUT)
    for f in fatti:
        print('  ' + f)
    print('scritto:', os.path.relpath(OUT, os.path.dirname(FIN)))
    cap, tb, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d' % (cap, tb, fig))
