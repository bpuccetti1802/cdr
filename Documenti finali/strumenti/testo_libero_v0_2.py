# -*- coding: utf-8 -*-
"""v0.2 di «ANALISI_Atti-Testo-Libero_SIPO-ANSC» (07/11/2026), dalla v0.1 RIVISTA A MANO
dall'utente (salvata alle 14:31): si modifica il file reale, `genera_testo_libero.py`
non va più rieseguito.

Correzione: la v0.1 affermava che un gestionale «non può depositare con R009» un atto con
caso d'uso di servizio. ANSC non lo dice. L'unica fonte è una riga del changelog 1.33.0
(03/10/2024): «Disabilitazione casi d'uso di servizio lato servizi cooperativi (ID 120)»,
senza altro dettaglio. In senso contrario: 1.46.2 (20/11/2025) corregge con la sigla
[SC/WA] il caso d'uso di servizio 52999; la prenotazione dei gemelli (R009 /prenota) crea
atti 11999999; 1.34.0 (04/11/2024) aggiunge al modello evento flagCertificatoSemplice e
flagEstrattoPerRiassunto, propri dei casi d'uso di servizio; il contratto R009 e i codici
di errore non portano restrizioni.

Implicazioni riallineate: §2.2 (i certificati emissibili si fissano anche al deposito,
non solo sulla web app), §2.3, §5.2 (proposta condizionata), §5.3 (il terzo percorso non
è escluso e coprirebbe anche il caso scoperto al Riepilogo), §6 (riga R009), TL-01,
TL-02, TL-10, riferimenti [A3]/[A5], Storia.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/testo_libero_v0_2.py
"""
import os
import sys

import docx
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from genera_testo_libero import _versa   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(QUI)
SRC = os.path.join(FIN, 'ANALISI_Atti-Testo-Libero_SIPO-ANSC_v0.1.docx')
NOME = 'ANALISI_Atti-Testo-Libero_SIPO-ANSC_v0.2'
OUT = os.path.join(FIN, NOME + '.docx')
DATA = '07/11/2026'

d = docx.Document(SRC)


def _svuota(p):
    for r in list(p._p):
        if r.tag in (qn('w:r'), qn('w:hyperlink')):
            p._p.remove(r)


def paragrafo(inizio, nuovo):
    """Riscrive il paragrafo che comincia con «inizio» (deve essere uno solo)."""
    trovati = [p for p in d.paragraphs if p.text.startswith(inizio)]
    if len(trovati) != 1:
        raise SystemExit('attesi 1, trovati %d: %s' % (len(trovati), inizio[:60]))
    p = trovati[0]
    if D.ha_commenti(p._p):
        raise SystemExit('paragrafo commentato: ' + inizio[:60])
    _svuota(p)
    _versa(p, nuovo)
    return p


def dopo(p, testo, stile=None):
    """Nuovo paragrafo dopo p, con lo stesso stile salvo indicazione."""
    nuovo = docx.oxml.OxmlElement('w:p')
    p._p.addnext(nuovo)
    q = Paragraph(nuovo, p._parent)
    q.style = d.styles[stile] if stile else p.style
    if p._p.pPr is not None and stile is None:
        q._p.insert(0, __import__('copy').deepcopy(p._p.pPr))
    _versa(q, testo)
    return q


def cella(chiave, colonna, nuovo, intestazione=None):
    """Riscrive la cella «colonna» della riga la cui prima cella vale «chiave».

    «intestazione»: limita alle tabelle che hanno quella cella nella prima riga.
    """
    trovate = []
    for t in d.tables:
        if intestazione and intestazione not in [c.text.strip() for c in t.rows[0].cells]:
            continue
        for r in t.rows:
            if r.cells[0].text.strip() == chiave:
                trovate.append(r)
    if len(trovate) != 1:
        raise SystemExit('attesa 1 riga, trovate %d: %s' % (len(trovate), chiave))
    c = trovate[0].cells[colonna]
    for extra in c.paragraphs[1:]:
        extra._p.getparent().remove(extra._p)
    p = c.paragraphs[0]
    _svuota(p)
    _versa(p, nuovo, dim=9)


# ------------------------------------------------------------------ §2.2
paragrafo('Quali certificati l’atto possa produrre',
          'Quali certificati l’atto possa produrre (certificato semplice, estratto per '
          'riassunto) si decide per singolo atto. Il modello evento porta i due '
          'contrassegni `flagCertificatoSemplice` e `flagEstrattoPerRiassunto` dal '
          'rilascio 1.34.0 [A3], quindi la scelta può viaggiare con l’atto; la modifica '
          'successiva si fa con una funzione che esiste solo sulla web app [A2]. '
          'L’estratto integrale è sempre disponibile.')

# ------------------------------------------------------------------ §2.3
titolo = [p for p in d.paragraphs
          if p.style.name == 'Heading 2' and p.text.strip() == 'Perché si passa dalla web app']
assert len(titolo) == 1
_svuota(titolo[0])
titolo[0].add_run('Il deposito del caso d’uso di servizio: che cosa dice ANSC')

p1 = paragrafo('Il rilascio ANSC 1.33.0 del 03/10/2024',
               'Il rilascio ANSC 1.33.0 del 03/10/2024 registra fra le funzioni aggiunte la '
               '«**Disabilitazione casi d’uso di servizio lato servizi cooperativi** (ID 120)» '
               '[A5]. È l’unica fonte sul tema, e non dice di più: non nomina il servizio di '
               'deposito (R009), non dice se valga per tutti i casi d’uso di servizio o per '
               'alcuni, né per quali operazioni. Il contratto di R009 non pone restrizioni sui '
               'casi d’uso ammessi, e fra i codici di errore pubblicati nessuno la segnala [A3].')
p2 = paragrafo('La portata della disabilitazione non è descritta',
               'Tre elementi successivi vanno anzi in senso contrario:')
v1 = dopo(p2, '**La correzione del rilascio 1.46.2 (20/11/2025).** Riguarda il caso d’uso di '
              'servizio delle trascrizioni di cittadinanza (52999) e porta la sigla [SC/WA], '
              'con cui il changelog marca le modifiche che valgono per i servizi cooperativi '
              'e per la web app [A5].', stile='List Paragraph')
v2 = dopo(v1, '**La prenotazione degli identificativi per il parto plurimo.** È un servizio '
              'cooperativo (R009 `/prenota/evento`) e predispone atti con il caso d’uso di '
              'servizio 11999999 [A1].', stile='List Paragraph')
v3 = dopo(v2, '**I contrassegni dei certificati emissibili.** Il rilascio 1.34.0 (04/11/2024), '
              'un mese dopo la disabilitazione, aggiunge al modello evento due campi propri dei '
              'casi d’uso di servizio [A3]. È un indizio debole, perché lo stesso modello è '
              'anche ciò che le consultazioni restituiscono.', stile='List Paragraph')
dopo(v3, 'Non è quindi accertato che un gestionale comunale non possa depositare con R009 un '
         'atto con caso d’uso di servizio. Le due strategie del capitolo successivo, che '
         'passano dalla web app, sono una **scelta prudente** in attesa della risposta del '
         'fornitore ANSC (TL-02), non un obbligo che ANSC imponga. Se la via cooperativa '
         'risultasse aperta, diventerebbe praticabile un terzo percorso, interamente in SIPO, '
         'descritto più avanti.', stile='Normal')

# ------------------------------------------------------------------ §5.2
paragrafo('Così la doppia immissione non scompare',
          'Così la doppia immissione non scompare: diventa un **controllo**. Il prezzo è '
          'accettare che, nel caso scoperto tardi, il lavoro fatto in SIPO serva da riscontro '
          'e non da fonte. La proposta presuppone che l’atto debba formarsi sulla web app: '
          'se il fornitore confermasse la via cooperativa (TL-02), il terzo percorso '
          'descritto qui sotto la supererebbe.')

# ------------------------------------------------------------------ §5.3
p = paragrafo('Sarebbe il percorso più coerente',
              'Sarebbe il percorso più coerente con un sistema che resta SIPO-centrico: un solo '
              'luogo di immissione, nessuno stato sospeso, nessuna transcodifica inversa, nessun '
              'ritorno da presidiare. Coprirebbe anche il caso scoperto al Riepilogo: senza UC '
              'determinato, l’atto passerebbe alla pagina del testo libero di SIPO conservando i '
              'dati già compilati, invece di essere steso di nuovo sulla web app. Le fonti ANSC '
              'non lo escludono: la sola riga del rilascio 1.33.0 non basta a dichiararlo '
              'impraticabile, e la risposta del fornitore decide se adottarlo.')
dopo(p, 'Se lo si adotta, due cautele. Il deposito con un caso d’uso di servizio va provato '
        'in preproduzione prima di costruirvi sopra, perché è il punto su cui le fonti sono '
        'incerte. E restano sulla web app le funzioni che solo lì esistono, in particolare la '
        'modifica successiva dei certificati emissibili [A2] e la nota tecnica.')

# tabella del terzo percorso, passo 5: i contrassegni dei certificati
cella('5', 1, 'Deposito con `idUsecase` di servizio, `motivoRecupero` = 3 e i contrassegni '
              'dei certificati emissibili.', intestazione='Servizio ANSC')

# ------------------------------------------------------------------ §6
cella('R009 /validazione/evento', 1,
      'Nelle due strategie il deposito avviene sulla web app. Se il deposito cooperativo del '
      'caso d’uso di servizio sia ammesso è TL-02: il rilascio 1.33.0 ne annuncia una '
      'disabilitazione di portata non descritta [A5]. Nel terzo percorso SIPO lo chiama.')

# ------------------------------------------------------------------ punti aperti
cella('TL-01', 1, 'Quale strategia adottare: il terzo percorso, se il fornitore ANSC lo '
                  'consente (TL-02); altrimenti la Gestione 2 come percorso unico, con la '
                  'Gestione 1 ridotta a deviazione verso di essa (proposta di questo '
                  'documento), oppure entrambe.')
cella('TL-02', 1, 'Portata della disabilitazione dei casi d’uso di servizio sui servizi '
                  'cooperativi, riportata dal rilascio 1.33.0 senza altri dettagli: se '
                  'riguardi il deposito con R009, se valga per tutti i casi d’uso di servizio '
                  'o per alcuni, se sia ancora in vigore. Vanno in senso contrario la '
                  'correzione [SC/WA] del rilascio 1.46.2 sul caso d’uso 52999, la '
                  'prenotazione dei gemelli, che crea atti 11999999, e i contrassegni dei '
                  'certificati aggiunti al modello evento nel rilascio 1.34.0. Da chiedere al '
                  'fornitore e da provare in preproduzione: ne dipende il terzo percorso.')
cella('TL-10', 1, 'Quali certificati rendere emissibili per l’atto con caso d’uso di '
                  'servizio (certificato semplice, estratto per riassunto), e chi li sceglie: '
                  'al deposito con i contrassegni del modello evento, in seguito solo sulla '
                  'web app [A2].')

# ------------------------------------------------------------------ riferimenti
cella('[A3]', 1, 'Contratti dei servizi cooperativi ANSC (`ansc/docs/openapi/`, R001–R024, '
                 'R901), modello evento (`model_evento.yaml`) e codici di errore '
                 '(`Codici d’errore.xlsx`).')
cella('[A5]', 1, '`ansc/docs/Changelog.md` — rilasci 1.33.0 (03/10/2024), 1.34.0 '
                 '(04/11/2024) e 1.46.2 (20/11/2025), e le altre voci sui casi d’uso di '
                 'servizio.')

# ------------------------------------------------------------------ testa e storia
for fatto in D.frontespizio(d, '0.2', NOME):
    print('  ' + fatto)
D.storia(d, DATA, '0.2', '2.2 · 2.3 · 5.2 · 5.3 · 6 · Punti aperti · Riferimenti',
         'Corretta l’affermazione che un gestionale non possa depositare con R009 un atto '
         'con caso d’uso di servizio: ANSC non lo dichiara. L’unica fonte è la riga del '
         'rilascio 1.33.0, senza altro dettaglio, e tre elementi successivi vanno in senso '
         'contrario. Il passaggio dalla web app diventa una scelta prudente in attesa del '
         'fornitore; il terzo percorso, interamente in SIPO, non è escluso e coprirebbe anche '
         'il caso scoperto al Riepilogo. I certificati emissibili si fissano anche al deposito. '
         'Riallineati TL-01, TL-02 e TL-10.')

d.save(OUT)
print('scritto', os.path.relpath(OUT, os.path.dirname(FIN)))
