# -*- coding: utf-8 -*-
"""Diagramma entità-relazioni delle annotazioni verso ANSC, in PowerPoint (14/11/2026).

Rifà img/annullamento/erd_annotazioni_ansc.png (PIL) con forme e connettori nativi, modificabile
dall'utente, su due indicazioni:
  · TUTTE le tabelle stanno in MATR_USR (anche quelle con prefisso ANSC_): non ci sono più
    confini di schema, quindi i legami possono diventare FK dichiarate;
  · il legame con ANSC_STATO_ATTO mancava come relazione esplicita: ANSC_ANNOTAZIONE.ID_ATTO_SIPO
    è FK verso ANSC_STATO_ATTO (l'annotazione verso ANSC presuppone un atto digitale), e
    ANSC_STATO_ATTO.ID_ATTO_SIPO è FK verso ATTO.

Linea piena = FK; tratteggio = riferimento per valore (numerazione, configurazione dei campi) o
corrispondenza logica. I connettori sono agganciati alle tabelle: spostandole seguono.

    /Library/Developer/CommandLineTools/usr/bin/python3 diagramma_annotazioni_erd_pptx.py
    qlmanage -t -s 2400 -o img/annullamento img/annullamento/erd_annotazioni_matr_usr.pptx
"""
import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diagramma_workflow_pptx import INK, MUTED, PAL, _punta, gomito, rgb, testo  # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(QUI, 'img', 'annullamento', 'erd_annotazioni_matr_usr.pptx')
W, H = 16.0, 9.2


def tabella(sl, x, y, w, colore, titolo, righe, nota=None, nuova=False):
    """Una tabella = una forma sola (così i connettori restano agganciati quando la si sposta).
    righe = [(chiave, colonna)] con chiave in PK/FK/UK o vuota."""
    h = 0.32 + 0.142 * len(righe) + (0.15 if nota else 0) + 0.05
    s = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    bordo, fondo = PAL[colore]
    s.fill.solid()
    s.fill.fore_color.rgb = rgb('ffffff')
    s.line.color.rgb = rgb(bordo)
    s.line.width = Pt(2.25 if nuova else 1.25)
    s.shadow.inherit = False
    tf = s.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = tf.margin_right = Inches(0.08)
    tf.margin_top, tf.margin_bottom = Inches(0.04), Inches(0.02)

    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = titolo + ("  (nuova)" if nuova else "")
    r.font.size, r.font.bold, r.font.name = Pt(10), True, 'Arial'
    r.font.color.rgb = rgb(bordo)
    p.space_after = Pt(3)
    for chiave, col in righe:
        p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        if chiave:
            rk = p.add_run()
            rk.text = chiave + "  "
            rk.font.size, rk.font.bold, rk.font.name = Pt(7.5), True, 'Arial'
            rk.font.color.rgb = rgb(bordo)
        rc = p.add_run()
        rc.text = col if chiave else "        " + col
        rc.font.size, rc.font.name = Pt(8), 'Arial'
        rc.font.color.rgb = rgb(INK)
    if nota:
        p = tf.add_paragraph()
        r = p.add_run()
        r.text = nota
        r.font.size, r.font.italic, r.font.name = Pt(7.5), True, 'Arial'
        r.font.color.rgb = rgb(MUTED)
    # fascia del titolo, dietro al testo: una seconda forma non serve, basta il colore del bordo
    s.fill.fore_color.rgb = rgb(fondo) if nuova else rgb('ffffff')
    return s


def lega(sl, figlio, cf, padre, cp, colore, tratteggio=False, spessore=1.5):
    """Connettore a gomito dal figlio (che porta la FK) al padre, agganciato alle due tabelle.
    Siti di aggancio: 0 alto, 1 sinistra, 2 basso, 3 destra."""
    c = sl.shapes.add_connector(MSO_CONNECTOR.ELBOW, 0, 0, 0, 0)
    c.begin_connect(figlio, cf)
    c.end_connect(padre, cp)
    c.line.color.rgb = rgb(colore)
    c.line.width = Pt(spessore)
    if tratteggio:
        c.line.dash_style = 4
    _punta(c)
    return c


def etichetta(sl, x, y, t, col, w=1.6):
    return testo(sl, x, y, w, 0.18, t, 7.5, False, col, PP_ALIGN.CENTER)


def genera(percorso=OUT):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    sl.background.fill.solid()
    sl.background.fill.fore_color.rgb = rgb('ffffff')

    testo(sl, 0.3, 0.15, W - 0.6, 0.35, "Le annotazioni verso ANSC: tabelle nuove e tabelle "
          "esistenti, tutte in MATR_USR", 15, True, '1b3a5c', PP_ALIGN.CENTER)
    testo(sl, 0.3, 0.5, W - 0.6, 0.25, "La proposta resta in ANNOTAZIONE_ATTO; ciò che serve ad "
          "ANSC sta nelle due tabelle nuove, legate alla proposta e allo stato dell’atto in ANSC",
          9.5, False, MUTED, PP_ALIGN.CENTER, corsivo=True)

    grigio, blu, verde = PAL['grigio'][0], PAL['blu'][0], PAL['verde'][0]

    # ------------------------------------------------ SIPO: la proposta (esistenti)
    formula = tabella(sl, 0.7, 7.0, 3.3, 'grigio', "CONF_FORMULA_ANNOTAZIONE", [
        ("PK", "ID_FORMULA"),
        ("", "DESCRIZIONE  (es. 190 - Art. 98)"),
        ("", "TESTO con i tag"),
    ], nota="tag VALORE_ANTE, VALORE_CORRETTO")
    proposta = tabella(sl, 0.7, 2.55, 3.3, 'grigio', "ANNOTAZIONE_ATTO", [
        ("PK", "ID"),
        ("FK", "ID_ATTO_TARGET  → ATTO"),
        ("FK", "ID_FORMULA  → CONF_FORMULA_ANNOTAZIONE"),
        ("FK", "ID_CONF_STATO · ID_TIPO_ANNOTAZIONE"),
        ("", "TARGET_NUMERO_ATTO · _PARTE · _SERIE"),
        ("", "TARGET_ANNO · TARGET_ESPONENTE"),
        ("", "TESTO_ANNOTAZIONE"),
        ("", "DATA_PROPOSTA · ID_UTENTE_LOG"),
    ], nota="la proposta di SIPO: resta com’è")
    tag = tabella(sl, 0.7, 5.15, 3.3, 'grigio', "ANNOTAZIONE_TAG_VALUES", [
        ("FK", "ID_ANNOTAZIONE_ATTO  → ANNOTAZIONE_ATTO"),
        ("FK", "ID_TAG"),
        ("", "TAG_VALUE  (VALORE_ANTE, VALORE_CORRETTO)"),
        ("", "DATA_INS"),
    ], nota="i valori della formula, come testi liberi")
    atto = tabella(sl, 0.7, 1.0, 3.3, 'grigio', "ATTO", [
        ("PK", "ID_ATTO"),
        ("", "AREA · ID_STATO_PRATICA"),
        ("", "NUMERO_ATTO · PARTE · SERIE"),
        ("", "ESPONENTE · ANNO"),
    ])

    # ------------------------------------------------ nuove
    ann = tabella(sl, 5.0, 2.55, 4.2, 'verde', "ANSC_ANNOTAZIONE", [
        ("PK", "ID_ANNOTAZIONE"),
        ("FK", "ID_ANNOTAZIONE_ATTO  → ANNOTAZIONE_ATTO  (UK)"),
        ("FK", "ID_ATTO_SIPO  → ANSC_STATO_ATTO"),
        ("", "COD_SERVIZIO_ANSC · COD_UC_ANSC"),
        ("", "COD_FORMULA_ANSC · ID_TIPO_RETTIFICA"),
        ("", "ID_ANSC_COLLEGATO · ID_COMUNE_COLLEGATO"),
        ("", "NUMERO_ATTO_ / NUM_ANNO_COLLEGATO"),
        ("", "DATA_FORMAZIONE_ / ID_TIPO_REGISTRO_COLLEGATO"),
        ("", "DESC_ENTE · ID_COMUNE_ENTE · ID_PROVINCIA_ENTE"),
        ("", "COD_TIPO_ / NUM_ / DATA_PROVVEDIMENTO"),
        ("", "DESC_ESTREMI_DOCUMENTO"),
        ("", "TXT_DETTAGLIO_RETTIFICA · TXT_COMPOSIZIONE"),
        ("", "NUMERO_ATTO · NUM_ANNO · TS_FORMAZIONE"),
        ("", "ID_ANSC · ID_STATO · STATO"),
        ("", "COD_FASE · TXT_ERRORE"),
        ("", "TXT_EVENTO · TXT_EVENTO_MODIFICATO"),
        ("", "TS_/UTENTE_PROPOSTA · TS_/UTENTE_CONFERMA"),
        ("", "TS_DEPOSITO · TS_FIRMA · UTENTE_FIRMA"),
    ], nota="una riga per annotazione, dalla proposta alla firma", nuova=True)
    corr = tabella(sl, 5.0, 6.45, 4.2, 'verde', "ANSC_ANNOTAZIONE_CORREZIONE", [
        ("PK", "ID_CORREZIONE"),
        ("FK", "ID_ANNOTAZIONE  → ANSC_ANNOTAZIONE"),
        ("", "NUM_ORDINE · DESC_DATO"),
        ("", "COD_PERCORSO_ANSC · ALIAS_CAMPO_SIPO"),
        ("", "TXT_VALORE_ANTE (da ANSC) · TXT_VALORE_SIPO"),
        ("", "TXT_VALORE_NUOVO · FLG_VERIFICATO"),
        ("UK", "ID_ANNOTAZIONE, COD_PERCORSO_ANSC"),
    ], nota="una riga per dato corretto", nuova=True)

    # ------------------------------------------------ integrazione ANSC (esistenti)
    stato = tabella(sl, 10.2, 1.0, 3.0, 'blu', "ANSC_STATO_ATTO", [
        ("PK", "ID_ATTO_SIPO  (FK → ATTO)"),
        ("", "ID_ANSC · NUMERO_ATTO"),
        ("", "ID_STATO · STATO · COD_FASE"),
        ("", "TXT_EVENTO"),
    ], nota="lo stato in ANSC dell’atto annotato")
    audit = tabella(sl, 13.45, 1.0, 2.3, 'blu', "ANSC_LOG_AUDIT", [
        ("PK", "ID_AUDIT"),
        ("FK", "→ ANSC_STATO_ATTO"),
        ("", "FASE · RICHIESTA · RISPOSTA"),
        ("", "ESITO · OPERATORE"),
    ], nota="anche le chiamate R013 / R007")
    numer = tabella(sl, 10.2, 4.3, 3.0, 'blu', "DATI_ATTO_ESTERNO", [
        ("PK", "id_atto_esterno"),
        ("", "nr_anno_atto · nr_atto_comunale"),
        ("", "id_atto_sipo · id_ansc · stato"),
    ], nota="numeri staccati da be-numeratore-comunale")
    cfg = tabella(sl, 10.2, 6.65, 3.0, 'blu', "ANSC_CFG_CAMPO", [
        ("", "ID_VERSIONE · COD_UC_ANSC"),
        ("", "OGGETTO_ANSC · CAMPO_ANSC"),
        ("", "ALIAS_CAMPO_SIPO"),
    ], nota="percorso ANSC ↔ campo SIPO (senza chiavi)")

    # ------------------------------------------------ relazioni (figlio → padre)
    lega(sl, proposta, 0, atto, 2, grigio)                          # N:1 ID_ATTO_TARGET
    lega(sl, tag, 0, proposta, 2, grigio)                           # N:1
    # proposta → formula: spezzata lungo il margine sinistro (i quattro agganci sono occupati)
    yp = 2.55 + 0.6
    yf = 7.0 + 0.35
    gomito(sl, [(0.7, yp), (0.42, yp), (0.42, yf), (0.7, yf)], grigio, spessore=1.5)
    lega(sl, ann, 1, proposta, 3, verde, spessore=2.25)             # 0..1:1 ID_ANNOTAZIONE_ATTO
    lega(sl, ann, 0, stato, 2, verde, spessore=2.25)                # N:1 ID_ATTO_SIPO
    lega(sl, stato, 1, atto, 3, blu)                                # 0..1:1 ID_ATTO_SIPO
    lega(sl, audit, 1, stato, 3, blu)                               # N:1
    lega(sl, corr, 0, ann, 2, verde, spessore=2.25)                 # N:1
    lega(sl, ann, 3, numer, 1, blu, tratteggio=True)                # per valore
    lega(sl, corr, 3, cfg, 1, blu, tratteggio=True)                 # per valore
    lega(sl, corr, 1, tag, 3, verde, tratteggio=True)               # corrispondenza logica

    etichetta(sl, 2.45, 2.12, "N:1  ID_ATTO_TARGET", grigio, 1.4)
    etichetta(sl, 2.45, 4.72, "N:1", grigio, 0.4)
    etichetta(sl, 0.05, 6.75, "N:1  ID_FORMULA", grigio, 1.2)
    etichetta(sl, 4.0, 2.75, "0..1:1  ID_ANNOTAZIONE_ATTO", verde, 1.0)
    etichetta(sl, 8.15, 2.0, "N:1  ID_ATTO_SIPO", verde, 1.4)
    etichetta(sl, 6.2, 1.18, "0..1:1  ID_ATTO_SIPO", blu, 1.6)
    etichetta(sl, 13.08, 1.62, "N:1", blu, 0.35)
    etichetta(sl, 7.15, 6.05, "N:1", verde, 0.4)
    etichetta(sl, 9.27, 4.15, "numero proprio, per valore", blu, 0.9)
    etichetta(sl, 9.27, 6.55, "percorso, per valore", blu, 0.9)
    etichetta(sl, 4.05, 6.05, "stessa informazione, strutturata", verde, 0.9)

    # legenda
    yl = H - 0.55
    for k, (col, t) in enumerate([('verde', "tabella nuova"), ('grigio', "tabella esistente di SIPO"),
                                  ('blu', "tabella esistente dell’integrazione ANSC")]):
        xk = 0.4 + k * 3.0
        b = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(xk), Inches(yl), Inches(0.3),
                                Inches(0.16))
        b.fill.solid()
        b.fill.fore_color.rgb = rgb(PAL[col][1])
        b.line.color.rgb = rgb(PAL[col][0])
        b.shadow.inherit = False
        testo(sl, xk + 0.38, yl - 0.01, 2.5, 0.2, t, 8.5)
    testo(sl, 9.3, yl - 0.01, 6.4, 0.2, "linea piena = FK (freccia verso la tabella padre) · "
          "tratteggio = riferimento per valore o corrispondenza logica", 8.5, False, MUTED,
          corsivo=True)

    os.makedirs(os.path.dirname(percorso), exist_ok=True)
    prs.save(percorso)
    return percorso


if __name__ == '__main__':
    print('scritto:', genera(sys.argv[1] if len(sys.argv) > 1 else OUT))
