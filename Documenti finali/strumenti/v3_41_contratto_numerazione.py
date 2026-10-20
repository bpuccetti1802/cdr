# -*- coding: utf-8 -*-
"""Contratto ansc-numerazione-v1.yaml allineato alla v3.41 dell'analisi (15/10/2026).

⚠️ Assunto del Comune (15/10/2026): il numero comunale è di SEI cifre e la serie NON è per
registro. Quindi una sola serie per anno (SEQ_NUM_COMUNALE_<anno>, MAXVALUE 999999), e il
registro sparisce dai percorsi, dai corpi e dalle risposte.

⚠️ Le fonti ANSC dicono cinque caratteri (model_evento.yaml:149 e R005:543 `maxLength: 5`;
Changelog: «ammessi massimo 5 caratteri»): il conflitto è dichiarato nell'analisi (OP-73), non
qui — il contratto descrive ciò che il servizio fa.

Ogni sostituzione dichiara quante occorrenze attende e si ferma se non tornano.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/v3_41_contratto_numerazione.py
"""
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YAML = os.path.join(BASE, 'ansc-numerazione-v1.yaml')

S = [
    # ── info e descrizione generale
    ('  version: 1.0.0\n', '  version: 1.1.0\n', 1),
    ('dalla serie per registro e anno e governo', 'dalla serie annuale e governo', 1),
    ("    sequence Oracle **per registro e per anno**, così che la numerazione riparta ogni anno.",
     "    sequence Oracle **per anno**, unica per tutti i registri, così che la numerazione\n"
     "    riparta ogni anno. Il numero è di sei cifre al massimo.", 1),
    ('`ANALISI_Integrazione-ANSC_v3.39.docx`', '`ANALISI_Integrazione-ANSC_v3.41.docx`', 1),
    ("      Le richieste di numeri. Una richiesta stacca uno o più numeri consecutivi dalla serie di un\n"
     "      registro e di un anno e li registra come disponibili.",
     "      Le richieste di numeri. Una richiesta stacca uno o più numeri consecutivi dalla serie di un\n"
     "      anno e li registra come disponibili.", 1),
    ('      Le serie dei numeri, una per registro e per anno, con i loro',
     '      Le serie dei numeri, una per anno, con i loro', 1),
    # ── creaPrenotazione
    ("        Stacca uno o più numeri consecutivi dalla serie del registro e dell'anno indicati e li",
     "        Stacca uno o più numeri consecutivi dalla serie dell'anno indicato e li", 1),
    ("                  codRegistro: '2'\n                  numAnno: 2027\n                  numNumeri: 1",
     "                  numAnno: 2027\n                  numNumeri: 1", 1),
    ("                  codRegistro: '1'\n                  numAnno: 2027\n                  numNumeri: 3",
     "                  numAnno: 2027\n                  numNumeri: 3", 1),
    ("                      codRegistro: '1'\n", '', 1),
    ('          description: Registro, anno o quantità non ammessi.',
     '          description: Anno o quantità non ammessi.', 1),
    ("La serie del registro 2 per l'anno 2027 non è stata creata",
     "La serie dell'anno 2027 non è stata creata", 1),
    ("        - codice: REGISTRO_NON_VALIDO\n"
     "          condizione: Il registro non appartiene alla decodifica ANSC_01.\n", '', 1),
    ("          condizione: La sequence del registro e dell'anno non esiste.",
     "          condizione: La sequence dell'anno non esiste.", 1),
    ('valore massimo di cinque cifre.', 'valore massimo di sei cifre.', 1),
    # ── elencaPrenotazioni
    ('        registro, anno, operatore, intervallo di date e stato dei numeri.',
     '        anno, operatore, intervallo di date e stato dei numeri.', 1),
    ("        - $ref: '#/components/parameters/CodRegistroFiltro'\n", '', 1),
    # ── elencaSerie / creaSerie
    ('        Restituisce le serie, una per registro e per anno, con il prossimo numero, i conteggi per\n'
     '        stato e il numero dei buchi.',
     '        Restituisce le serie, una per anno, con il prossimo numero, i conteggi per stato e il\n'
     '        numero dei buchi.', 1),
    ("a dicembre per controllare che quelle dell'anno successivo siano state create.",
     "a dicembre per controllare che quella dell'anno successivo sia stata creata.", 1),
    ('                            description: Le serie, per anno e registro.',
     '                            description: Le serie, per anno.', 1),
    ('      summary: Crea le serie dei cinque registri per un anno',
     '      summary: Crea la serie di un anno', 1),
    ("        Crea, per l'anno indicato, le sequence dei cinque registri che ancora mancano, eseguendo",
     "        Crea, per l'anno indicato, la sequence della serie se ancora manca, eseguendo", 1),
    ("        Si usa all'installazione, per l'anno in corso, e quando il job non ha creato le serie\n"
     "        dell'anno successivo.",
     "        Si usa all'installazione, per l'anno in corso, e quando il job non ha creato la serie\n"
     "        dell'anno successivo.", 1),
    ('        **Effetti**: crea le sequence mancanti. **Ripetibile senza effetti ulteriori**: le serie\n'
     '        già esistenti non sono toccate.',
     "        **Effetti**: crea la sequence, se manca. **Ripetibile senza effetti ulteriori**: una\n"
     "        serie già esistente non è toccata.", 1),
    ('                summary: Le serie del 2028', '                summary: La serie del 2028', 1),
    ("          description: Le cinque serie dell'anno, dopo l'esecuzione.",
     "          description: La serie dell'anno, dopo l'esecuzione.", 1),
    ('                            description: Quante serie sono state create da questa esecuzione.',
     '                            description: 1 se la serie è stata creata da questa esecuzione, 0 se esisteva già.', 1),
    ('                          serie:\n'
     '                            type: array\n'
     "                            description: Le cinque serie dell'anno.\n"
     "                            items: { $ref: '#/components/schemas/Serie' }",
     "                          serie: { $ref: '#/components/schemas/Serie' }", 1),
    ("        Crea le sequence mancanti dell'anno. Ripetibile senza effetti ulteriori.",
     "        Crea la sequence dell'anno, se manca. Ripetibile senza effetti ulteriori.", 1),
    # ── percorsi: il registro esce dalla risorsa
    ('  /ansc/v1/numerazione/serie/{codRegistro}/{numAnno}:', '  /ansc/v1/numerazione/serie/{numAnno}:', 1),
    ('  /ansc/v1/numerazione/serie/{codRegistro}/{numAnno}/numeri:',
     '  /ansc/v1/numerazione/serie/{numAnno}/numeri:', 1),
    ('  /ansc/v1/numerazione/serie/{codRegistro}/{numAnno}/numeri/{numAtto}:',
     '  /ansc/v1/numerazione/serie/{numAnno}/numeri/{numAtto}:', 1),
    ("      - $ref: '#/components/parameters/CodRegistro'\n", '', 3),
    # ── limiti del numero
    ('maximum: 99999 }', 'maximum: 999999 }', 3),
    ("dall'intervallo da 1 a 99999.", "dall'intervallo da 1 a 999999.", 1),
    ('Il numero 1532 della serie 2/2027 è già legato', 'Il numero 1532 della serie 2027 è già legato', 1),
    ('      description: Il numero comunale, da 1 a 99999.', '      description: Il numero comunale, da 1 a 999999.', 1),
    ('          minimum: 1\n          maximum: 99999\n', '          minimum: 1\n          maximum: 999999\n', 1),
    # ── componenti
    ("    CodRegistro:\n"
     "      name: codRegistro\n"
     "      in: path\n"
     "      required: true\n"
     "      description: Registro secondo la decodifica ANSC_01 — 1 nascita, 2 morte, 3 matrimonio, 4 unione civile, 5 cittadinanza.\n"
     "      schema: { type: string, enum: ['1', '2', '3', '4', '5'] }\n"
     "      example: '2'\n", '', 1),
    ("    CodRegistroFiltro:\n"
     "      name: codRegistro\n"
     "      in: query\n"
     "      required: false\n"
     "      description: Limita a un registro della decodifica ANSC_01.\n"
     "      schema: { type: string, enum: ['1', '2', '3', '4', '5'] }\n", '', 1),
    ('      required: [codRegistro, numAnno, numNumeri]', '      required: [numAnno, numNumeri]', 1),
    ("        codRegistro:\n"
     "          type: string\n"
     "          enum: ['1', '2', '3', '4', '5']\n"
     "          description: Registro secondo la decodifica ANSC_01. Corrisponde a ty_evento.\n", '', 1),
    ("        codRegistro: { type: string, description: 'Registro secondo la decodifica ANSC_01.' }\n", '', 2),
    ("      description: La richiesta di creazione delle serie di un anno.",
     "      description: La richiesta di creazione della serie di un anno.", 1),
    ("          description: Anno di cui creare le serie dei cinque registri. Il corrente o il successivo.",
     "          description: Anno di cui creare la serie. Il corrente o il successivo.", 1),
    ('      description: Una serie di numeri, per registro e anno.',
     '      description: La serie dei numeri di un anno, unica per tutti i registri.', 1),
    ("        codRegistro: { type: string, description: 'Registro della serie. Corrisponde a ty_evento.' }\n", '', 1),
]


def main():
    testo = open(YAML, encoding='utf-8').read()
    for vecchio, nuovo, attese in S:
        n = testo.count(vecchio)
        if n != attese:
            raise SystemExit(f'«{vecchio[:70]}»: attese {attese}, trovate {n}')
        testo = testo.replace(vecchio, nuovo)
    for residuo in ('codRegistro', 'CodRegistro', 'registro e', '99999 ', 'cinque'):
        if residuo in testo.replace('999999', ''):
            print('  ⚠️ residuo:', residuo)
    import yaml
    yaml.safe_load(testo)
    open(YAML, 'w', encoding='utf-8').write(testo)
    print(f'  {len(S)} sostituzioni, contratto valido: {YAML}')


if __name__ == '__main__':
    main()
