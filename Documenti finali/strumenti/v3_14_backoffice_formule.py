# -*- coding: utf-8 -*-
"""v3.14 — il back-office alla scala reale: allegati e formule nei volumi, e chi li configura.

⚠️ La tabella dei volumi del capitolo si fermava a UC, righe di mappatura, campi obbligatori e
regole: ignorava **1.569 righe di allegato e 2.200 di formula**, che sono lavoro di
configurazione quanto i campi. Con la v3.14 quel conto va rifatto, perché è il conto su cui il
capitolo fonda il disegno delle schermate.

⚠️ E va rovesciata la conclusione che ne discendeva. La prosa diceva che «l'importazione
diventa il meccanismo principale di popolamento» e che il lavoro «si misura in regole da
scrivere»: era vero finché la configurazione era un'importazione da rivedere. Ora la
configurazione la decidono i funzionari, e il lavoro si misura in **righe da esaminare**.
"""
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(BASE, 'Documenti finali', 'ANALISI_Integrazione-ANSC_v3.14.docx')

VOLUMI = [
    ['Oggetto da configurare', 'Nascite', 'Intero dominio'],
    ['UC da adottare', '143', '374'],
    ['Righe di mappatura fra campo ANSC e colonna SIPO', '16.934', 'oltre 60.000'],
    ['Campi dichiarati obbligatori', '4.690', '20.346'],
    ['Allegati richiesti', '—', '1.569 righe su 346 UC, di cui 320 obbligatorie'],
    ['Formule previste', '—', '2.200 righe su 366 UC, di cui 629 obbligatorie'],
    ['Testi di formula da trascrivere', '—', '233 (ANSC non li pubblica)'],
    ['Condizioni di applicabilità degli UC', 'una per UC', 'una per UC'],
]

PROSA = [
    ('Il confronto fra le righe contiene l’indicazione di disegno, ed è un confronto fra ordini '
     'di grandezza. Le condizioni di applicabilità sono una per caso d’uso e ciascuna è breve: '
     'sono scrivibili da una persona, e sono il luogo dove il giudizio del funzionario serve '
     'davvero, perché stabiliscono quale fattispecie nazionale corrisponda a un modello '
     'comunale. Campi, allegati e formule si contano invece a decine di migliaia: nessuno può '
     'scriverli a mano, ma nessuno può nemmeno accettarli senza guardarli, perché il mapping '
     'dichiara ciò che ANSC accetta e non ciò che il Comune registra.'),
    ('Da qui la ripartizione dei compiti fra le schermate, che nella presente versione cambia '
     'natura. Il catalogo degli UC resta una replica di ciò che ANSC dichiara e si consulta '
     'soltanto. Campi, allegati e formule si precompilano per importazione, ma la schermata '
     'che li presenta non è una superficie di revisione facoltativa: è la lista di lavoro. Ogni '
     'riga porta la propria origine, il filtro predefinito mostra ciò che nessuno ha ancora '
     'esaminato, e una riga esaminata non torna a chiedere attenzione alla revisione '
     'successiva del mapping.'),
    ('La conseguenza pratica è che il lavoro di configurazione di una nuova famiglia di atti si '
     'misura in righe da esaminare e in corrispondenze SIPO da stabilire, non in righe da '
     'immettere. Con 374 casi d’uso da adottare — anche procedendo per frequenza, dai modelli '
     'più usati ai rari — è un impegno che va dimensionato prima e non scoperto dopo: è la '
     'ragione per cui ANSC_CFG_UC porta un contrassegno di attivazione, che tiene distinto ciò '
     'che è configurato compiutamente da ciò che è soltanto censito.'),
    ('Le formule meritano una nota a parte, perché sono l’unico oggetto della configurazione '
     'che nessuna fonte precompila del tutto. Il mapping dice quali si applicano a ciascun UC e '
     'quali sono obbligatorie, ma non ne pubblica il testo, e nemmeno le decodifiche lo fanno. '
     'La schermata deve quindi consentire due cose distinte: scegliere fra le formule '
     'facoltative quali offrire all’ufficiale, e trascrivere le 233 diciture, che si scrivono '
     'una volta sola e valgono per tutti gli UC che le richiamano.'),
]

DIDASCALIE = [
    ('Wireframe — Configurazione (Operazioni): metadati per evento × operazione × Modello e '
     'versione attiva; «campi» apre i campi',
     'Wireframe — Configurazione (Casi d’uso): una riga per UC adottato con Modello, tipo atto, '
     'priorità e stato di attivazione; «campi» apre campi, allegati e formule'),
    ('Wireframe — Configurazione (Campi obbligatori): mapping campo ANSC ↔ SIPO e obbligatorietà '
     'con condizioni, importabili dal mapping ufficiale',
     'Wireframe — Configurazione (Campi, allegati e formule per UC): corrispondenza campo ANSC ↔ '
     'SIPO, documenti richiesti e diciture previste, con l’origine di ciascuna riga'),
]


def applica(doc):
    fatti = []

    t = D.trova_tabella(doc, 'Oggetto da configurare', 'Nascite', 'Intero dominio')
    from v3_14_configurazione import riscrivi_tabella
    riscrivi_tabella(t, VOLUMI[1:])
    fatti.append(f'tabella dei volumi: {len(VOLUMI) - 1} righe (con allegati e formule)')

    ancore = ['Il confronto fra l’ultima riga e le precedenti',
              'Da qui la ripartizione dei compiti fra le schermate',
              'La conseguenza pratica è che il lavoro di configurazione']
    for ancora, testo in zip(ancore, PROSA):
        p = next((x for x in doc.paragraphs if x.text.strip().startswith(ancora)), None)
        assert p is not None, f'paragrafo non trovato: {ancora}'
        D.testo_di(p, testo)
    # il quarto paragrafo, sulle formule, è nuovo: va dopo il terzo
    terzo = next(x for x in doc.paragraphs
                 if x.text.strip().startswith('La conseguenza pratica'))
    i = D.indice_di(doc, terzo)
    D.para(doc, doc.paragraphs[i + 1]._p, PROSA[3])
    fatti.append('prosa del governo della configurazione riscritta (+ nota sulle formule)')

    for vecchio, nuovo in DIDASCALIE:
        p = next((x for x in doc.paragraphs if x.text.strip().startswith(vecchio[:60])), None)
        if p is not None:
            D.testo_di(p, nuovo)
            fatti.append(f'didascalia: {nuovo[:52]}…')
    return fatti


if __name__ == '__main__':
    doc = docx.Document(DOC)
    for f in applica(doc):
        print('  ·', f)
    doc.save(DOC)
    print('salvato')
