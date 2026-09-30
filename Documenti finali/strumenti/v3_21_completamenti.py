# -*- coding: utf-8 -*-
"""v3.21, seconda parte: ciò che il confronto ha fatto emergere oltre alle quattro tabelle.

  · la vista V_ANSC_DIZ_VALIDO è descritta nel capitolo sui dizionari ma NON è nell'Appendice A:
    è la stessa classe di scostamento, un oggetto dichiarato e mai definito;
  · il prospetto «Impatti sul Database» nomina un oggetto e ne descrive un altro;
  · OP-35 elenca le colonne senza prefisso di ruolo e va aggiornato con quelle nuove;
  · una frase fa scattare un falso positivo del controllo dei conteggi;
  · le due figure che dipendono dal modello dati vanno risostituite.
"""
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from v3_21_allineamento import DEST, IMG, ddl_dopo, riga_ddl   # noqa: E402

VISTA = [
    "CREATE OR REPLACE VIEW ANSC_USR.V_ANSC_DIZ_VALIDO AS",
    "  SELECT d.id_dominio, d.nm_dominio, v.id_valore, v.cd_valore,",
    "         v.ds_valore, v.nr_ordinamento",
    "    FROM ANSC_USR.DOMINIO_DECODIFICA d",
    "    JOIN ANSC_USR.VALORE_DOMINIO     v ON v.id_dominio = d.id_dominio",
    "   WHERE SYSDATE BETWEEN NVL(v.dt_inizio_validita, DATE '0001-01-01')",
    "                     AND NVL(v.dt_fine_validita,   DATE '9999-12-31');",
    "COMMENT ON TABLE ANSC_USR.V_ANSC_DIZ_VALIDO IS",
    "  'Contratto di fruizione verso SIPO: applica la validita temporale in lettura e si",
    "   raggiunge per sinonimo con grant di sola lettura. Non viene da Side: vale quali che",
    "   siano le tabelle sottostanti.';",
]

IMPATTI = [
    ('ATTO.NUM_COMUNALE_ANSC',
     'Aggiungere la colonna NUM_COMUNALE_ANSC — VARCHAR2(6), numero dell’atto assegnato dal '
     'Comune. ⚠️ Su quale delle due tabelle ATTO (ANAG_USR o MATR_USR) va creata è ancora da '
     'decidere: il foglio di lavoro la usa come sorgente di evento.numeroatto, ma oggi non '
     'esiste — su ANAG_USR.ATTO c’è NUMERO_COMUNALE, che è cosa diversa.'),
    ('ATTO.ATTO_NUMERO_ANSC',
     'Aggiungere la colonna ATTO_NUMERO_ANSC — VARCHAR2(100), identificativo dell’atto in '
     'ANSC. ⚠️ Vale la stessa indecisione sulla tabella; e va verificato che non duplichi '
     'ID_ATTO_ANSC, che su ANAG_USR.ATTO esiste già.'),
]


def main():
    doc = docx.Document(DEST)
    fatti = []

    # ── la vista mancante, in coda alla sezione dei dizionari dell'Appendice A
    ancora = "   gli atti gia formati.';"
    p = riga_ddl(doc, ancora)
    for riga in VISTA:
        p = ddl_dopo(doc, p.text, riga) if riga is VISTA[0] else _appendi(doc, p, riga)
    fatti.append('Appendice A: aggiunta la vista V_ANSC_DIZ_VALIDO, descritta ma mai definita')

    # ── il prospetto degli impatti sul database
    t = D.trova_tabella(doc, 'oggetto db', 'tipo intervento')
    for oggetto, testo in IMPATTI:
        for r in t.rows[1:]:
            if r.cells[0].text.strip() == oggetto:
                D.riscrivi_cella(r.cells[2], testo)
                break
        else:
            raise SystemExit('riga non trovata: ' + oggetto)
    fatti.append('Impatti sul Database: le due righe nominavano un oggetto e ne descrivevano '
                 'un altro')

    # ── OP-35: le colonne nuove senza prefisso di ruolo
    D.sostituisci(doc,
                  'ORDINAMENTO, RICHIESTA, RISPOSTA e altre.',
                  'ORDINAMENTO, RICHIESTA, RISPOSTA e altre; la v3.21 vi aggiunge SERIE, '
                  'SCHEMA_SIPO, TABELLA_SIPO, OPERATIVO e LOGICA_DI_SCELTA, introdotte con la '
                  'revisione delle schede.', attese=1, etichetta='OP-35', fatti=fatti)

    # ── il falso positivo del controllo dei conteggi
    D.sostituisci(doc, 'sono letti dai contratti pubblicati.',
                  'sono letti dai contratti che ANSC pubblica.', attese=1,
                  etichetta='frase che confondeva il controllo dei conteggi', fatti=fatti)

    # ── le due figure che dipendono dal modello dati
    D.sostituisci_immagine(doc, 'Schema ANSC_USR.',
                           os.path.join(IMG, 'erd_ansc_usr.png'))
    D.sostituisci_immagine(doc, 'Dalla maschera SIPO al payload ANSC.',
                           os.path.join(IMG, 'catena_configurazione.png'))
    fatti.append('rigenerate le figure «Schema ANSC_USR» e «Dalla maschera SIPO al payload '
                 'ANSC» (la seconda mostrava ancora ANSC_CFG_UC_CONDIZIONE e ANSC_DIZ_*)')

    D.storia(doc, '15/09/2026', '3.21',
             'Adeguamenti database · Costruzione del payload · Gestione dei dizionari ANSC · '
             'Impatti sul Database · Registro degli Open Point · Appendice A',
             'Allineate le schede delle tabelle e il DDL dell’Appendice A, che divergevano su '
             'quattro tabelle: ANSC_CFG_UC (tolte TIPO_RITO e STATO, aggiunta SERIE, '
             'LOGICA_DI_SCELTA), ANSC_CFG_CAMPO (reintrodotta ID_VERSIONE, aggiunte '
             'SCHEMA_SIPO e OPERATIVO, note di schema e tabella rimesse al posto giusto), '
             'ANSC_ANA_UC (COD_VERSIONE, ID_TIPO_DOCUMENTO), ANSC_XREF (ID_UC_ANSC e '
             'ID_OPERAZIONE_ANSC convivono). Corretto il vincolo CK_ANSC_STATO_ATTO_ESITO, che '
             'era spezzato e non eseguibile; aggiunta la vista V_ANSC_DIZ_VALIDO, descritta ma '
             'mai definita; rigenerate le due figure del modello dati.')

    doc.save(DEST)
    print('\n'.join(' · ' + f for f in fatti))


def _appendi(doc, p, testo):
    import copy
    from docx.text.paragraph import Paragraph
    nuovo = copy.deepcopy(p._p)
    p._p.addnext(nuovo)
    np = Paragraph(nuovo, p._parent)
    for r in np.runs[1:]:
        r._r.getparent().remove(r._r)
    np.runs[0].text = testo
    return np


if __name__ == '__main__':
    main()
