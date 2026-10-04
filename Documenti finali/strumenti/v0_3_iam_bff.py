# -*- coding: utf-8 -*-
"""ANALISI_Identita-Profilazione-IAM v0.2 → v0.3 (02/10/2026).

Aggiunge dentro S3 la variante del Backend For Frontend, con la spiegazione di che cosa
sia: non una sesta soluzione sulla scala, ma un modo di percorrere S3 in due tempi.

⚠️ Si riparte dal file reale, che porta le modifiche manuali del committente: fra queste
la rimozione di due tabelle e alcune riformulazioni. Si corregge inoltre lo stile del
titolo di S4, rimasto «Normal» dopo l'edizione manuale: era un titolo di terzo livello e
senza quello stile non compare nell'indice.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v0_3_iam_bff.py
"""
import os
import shutil
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(BASE, 'Documenti finali', 'ANALISI_Identita-Profilazione-IAM_v0.2.docx')
DST = os.path.join(BASE, 'Documenti finali', 'ANALISI_Identita-Profilazione-IAM_v0.3.docx')

BILANCIO = [
    ['Problema', 'Il BFF lo risolve?', 'Perché'],
    ['Il gettone sta nel browser',
     '**Sì, ed è il guadagno più immediato**',
     'Oggi le applicazioni Angular conservano il gettone in localStorage, dove è leggibile da '
     'qualunque script che riesca a eseguire nella pagina. Con un BFF il browser tiene solo '
     'un cookie di sessione e il gettone non lo raggiunge mai. ⚠️ È un miglioramento che vale '
     'di per sé, indipendente dagli header, da OIDC e da tutta la scala delle soluzioni.'],
    ['L’identità non arriva ai back-end',
     'Sì, ma non gratis',
     'Il BFF è il punto naturale in cui l’identità reale — dagli header oggi, dal gettone '
     'domani — si converte in qualcosa da propagare a valle. Non toglie ai servizi il lavoro '
     'di verificarla, ma lo localizza: un componente invece di trentacinque.'],
    ['Le applicazioni a pagina singola non possono usare la modalità header',
     'Tecnicamente sì, in pratica no',
     'Il BFF è lato server e riceve gli header su ogni chiamata, non solo sul caricamento '
     'iniziale: con lui la modalità header tornerebbe praticabile. ⚠️ Ma le applicazioni '
     'Angular non sono in attesa di essere collegate — hanno già una via di accesso che gli '
     'header non li usa. Costruire un BFF perché possano usarli sarebbe un passo indietro.'],
    ['La fiducia negli header',
     '**No**',
     'Un BFF che legge le intestazioni e si fida si fida esattamente come prima: il difetto '
     'non si chiude, **si sposta e si concentra**. Il guadagno è di presidio, non di '
     'architettura: la regola di rete che impedisce di scavalcare il proxy va scritta e '
     'mantenuta per un componente invece che per trentacinque.'],
]


def main():
    if os.path.exists(DST):
        os.remove(DST)
    shutil.copy(SRC, DST)
    d = docx.Document(DST)
    fatti = []

    # ⚠️ lo stile del titolo di S4 è rimasto «Normal» dopo l'edizione manuale: senza
    # «Heading 3» la sezione non compare nell'indice e la numerazione si rompe.
    for p in d.paragraphs:
        if p.text.strip().startswith('S4 —') and p.style.name != 'Heading 3':
            p.style = d.styles['Heading 3']
            fatti.append('ripristinato lo stile di titolo su «S4 —», rimasto Normal')
            break

    ancora = next(p for p in d.paragraphs if p.text.strip().startswith('S4 —'))

    def par(t, stile='Normal'):
        return D.para(d, ancora._p, t, stile=stile)

    par('Una variante di S3: il Backend For Frontend', 'Heading 4')
    par('**Un BFF — Backend For Frontend — è un componente lato server dedicato a un '
        'front-end, o a una famiglia di front-end, che si interpone fra il browser e i '
        'servizi.** Il browser parla soltanto con lui; è lui a tenere la sessione, a '
        'custodire i gettoni e a chiamare i servizi a valle per conto dell’utente. Nasce per '
        'le applicazioni a pagina singola, dove l’alternativa è tenere il gettone nel '
        'browser, ed è oggi il modo raccomandato di far dialogare una applicazione Angular '
        'con dei servizi protetti.')
    par('Non è un livello in più per gusto dell’architettura: risolve un problema che le '
        'applicazioni a pagina singola hanno per costruzione. Una pagina prodotta dal server '
        'ha una sessione lato server e il gettone non lascia mai la macchina; una '
        'applicazione che gira nel browser, se deve presentare un gettone, deve anche '
        'conservarlo da qualche parte — e ogni posto in cui può conservarlo è leggibile da '
        'chi riesca a far eseguire uno script nella pagina.')
    par('Per SIPO la variante è questa: **invece di costruire il gateway di S3 come servizio '
        'di sola autenticazione, lo si costruisce come BFF**, cioè gli si fa attraversare '
        'anche il traffico applicativo delle nuove applicazioni Angular. Il componente è lo '
        'stesso; cambia quanto gli si fa fare.')

    par('**Che cosa risolve e che cosa no.** La variante va valutata su quattro problemi '
        'distinti, e la risposta non è la stessa per tutti.')
    D.tabella(d, ancora._p, BILANCIO, modello=d.tables[13], larghezze=[1.5, 1.2, 3.8])

    par('⚠️ **Il motivo per cui questa variante merita di stare dentro S3 e non accanto è '
        'un altro, ed è di sequenza.** Il BFF è lo stesso componente che in S3 fa da '
        'interlocutore verso IAM. Costruirlo adesso, con la modalità header dietro, e '
        'commutarlo a OIDC quando le decisioni saranno prese, non è una deviazione: è **S3 '
        'pagato in due tempi**, con gli header come appoggio temporaneo. È anche il solo modo '
        'di cominciare a costruire prima che D1-D6 siano decise, perché il componente non '
        'cambia fra le due modalità — cambia soltanto da dove prende l’identità. La proprietà '
        'di commutazione fra le due modalità, prevista dalla decisione D6, troverebbe lì la '
        'sua casa naturale.')
    par('⚠️ **A una condizione, però**: il BFF deve nascere con l’interfaccia che separa «'
        'costruisci il reindirizzamento» da «gestisci il ritorno». Senza, commutarlo da '
        'header a OIDC costa quanto riscriverlo, e la variante perde la sua unica ragione.')

    par('**Quanti BFF, e che cosa comporta in Kubernetes.** Uno per ciascun micro-frontend '
        'sarebbe un errore di granularità: il disegno del back-office prevede quattro '
        'micro-frontend sotto un’unica shell, e il BFF naturale è **uno per shell**, cioè '
        'per famiglia di applicazioni che condividono la sessione. I trentacinque front-end '
        'esistenti non ne hanno bisogno: sono già server, la sessione ce l’hanno.')
    par('⚠️ Una conseguenza operativa da non scoprire dopo: **il BFF tiene la sessione, '
        'quindi non è senza stato.** Con più repliche servono o le sessioni appiccicate '
        'all’istanza o un archivio condiviso. È lo stesso nodo che il rilievo RI-19 segnala '
        'oggi per i front-end — sessione in memoria, nessun archivio condiviso — e la '
        'variante è l’occasione per risolverlo invece di ereditarlo. Vale infine, come per il '
        'gateway, che la sonda di prontezza non deve dipendere dalla raggiungibilità di IAM: '
        'un disservizio esterno non deve far riavviare il componente.')
    fatti.append('variante BFF dentro S3, con definizione, bilancio e nota su Kubernetes')

    t = D.trova_tabella(d, '#', 'Questione')
    D.clona_riga(t, (
        'PI-19', 'Se le nuove applicazioni Angular debbano adottare un BFF, e con quale '
                 'granularità. ⚠️ Oggi conservano il gettone in localStorage e chiamano i '
                 'servizi direttamente: la scelta riguarda la loro architettura, non solo '
                 'l’integrazione con IAM, e conviene prenderla prima che le applicazioni si '
                 'moltiplichino.',
        'Architettura / Referenti SIPO'))
    fatti.append('PI-19 aperto')

    for tab in d.tables:
        if tab.rows[0].cells[0].text.strip().lower().startswith('area organizzativa'):
            for r in tab.rows:
                v = {'Versione': '0.3',
                     'Documento': 'ANALISI_Identita-Profilazione-IAM_v0.3'
                     }.get(r.cells[0].text.strip())
                if v:
                    D.riscrivi_cella(r.cells[1], v)
            break
    D.storia(d, '02/10/2026', '0.3', 'Parte II — Soluzioni (S3)',
             'Aggiunta dentro S3 la variante del Backend For Frontend, con la definizione del '
             'pattern, il bilancio di che cosa risolve e che cosa no, e le conseguenze in '
             'Kubernetes. È inquadrata come variante e non come sesta soluzione, perché non è '
             'un’alternativa alle altre ma un modo di percorrere S3 in due tempi: il '
             'componente è lo stesso, e la modalità header può fargli da appoggio temporaneo '
             'finché le decisioni non sono prese. Ripristinato lo stile di titolo della '
             'sezione S4, rimasto «Normal» dopo l’edizione manuale. Un punto aperto nuovo.')
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
