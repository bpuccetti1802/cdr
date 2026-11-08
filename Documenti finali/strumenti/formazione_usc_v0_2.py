"""Corso USC v0.2: dalla v0.1 MODIFICATA A MANO dall'utente (07/11/2026).

Non rigenera il corso (formazione_usc_pptx.js produrrebbe la v0.1 senza le modifiche dell'utente):
apre il .pptx reale, riscrive la slide 6 e aggiunge due slide dopo di essa.
  6  Come è fatto un caso d'uso (UC)          (era «Il caso d'uso: ogni atto ha il suo percorso»)
  7  Tipologie di atti in SIPO e casi d'uso di ANSC
  8  La struttura del payload: il modello evento
Uso: python formazione_usc_v0_2.py   (dalla cartella Documenti finali)
"""
import copy
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor  # noqa: F401
from pptx.enum.dml import MSO_THEME_COLOR as T
from pptx.oxml.ns import qn
from lxml import etree

SRC = "FORMAZIONE_USC_Nuove-funzionalita-SIPO-ANSC_v0.1.pptx"
OUT = "FORMAZIONE_USC_Nuove-funzionalita-SIPO-ANSC_v0.2.pptx"
M = 0.6
TITOLI = "+mj-lt"

pres = Presentation(SRC)


# ------------------------------------------------------------------ primitive
def _colore(fmt, c):
    fmt.theme_color = c


def scheda(s, x, y, w, h, fill=T.BACKGROUND_2, line=None, dash=False):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.adjustments[0] = min(0.5, 0.08 / min(w, h))
    sh.fill.solid(); _colore(sh.fill.fore_color, fill)
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.width = Pt(1.25 if dash else 1); _colore(sh.line.color, line)
    sh.shadow.inherit = False
    return sh


def testo(s, t, x, y, w, h, size=15, bold=False, color=T.TEXT_1, font=None, italic=False,
          align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    """t: stringa, oppure lista di paragrafi; un paragrafo è stringa o lista di (testo, opzioni)."""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    paragrafi = t if isinstance(t, list) else [t]
    for i, par in enumerate(paragrafi):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        for frammento, o in (par if isinstance(par, list) else [(par, {})]):
            r = p.add_run(); r.text = frammento
            f = r.font
            f.size = Pt(o.get("size", size)); f.bold = o.get("bold", bold); f.italic = o.get("italic", italic)
            _colore(f.color, o.get("color", color))
            if o.get("font", font):
                f.name = o.get("font", font)
    return tb


def elenco(s, voci, x, y, w, h, size=14, color=T.TEXT_1, numeri=False):
    tb = testo(s, voci, x, y, w, h, size=size, color=color)
    for i, p in enumerate(tb.text_frame.paragraphs):
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", str(Inches(0.28))); pPr.set("indent", str(-Inches(0.28)))
        sp = etree.SubElement(pPr, qn("a:spcAft")); etree.SubElement(sp, qn("a:spcPts")).set("val", "600")
        if numeri:
            etree.SubElement(pPr, qn("a:buFont")).set("typeface", "+mj-lt")
            etree.SubElement(pPr, qn("a:buAutoNum")).set("type", "arabicPeriod")
        else:
            etree.SubElement(pPr, qn("a:buChar")).set("char", "•")
    return tb


def cerchio(s, x, y, d, etichetta, fill=T.ACCENT_1, color=T.BACKGROUND_1, size=16):
    sh = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    sh.fill.solid(); _colore(sh.fill.fore_color, fill); sh.line.fill.background(); sh.shadow.inherit = False
    testo(s, str(etichetta), x, y, d, d, size=size, bold=True, color=color, font=TITOLI,
          align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def linea(s, x1, y1, x2, y2, color=T.ACCENT_3, width=2, punta=True):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.width = Pt(width); _colore(c.line.color, color)
    if punta:
        ln = c.line._get_or_add_ln()
        etree.SubElement(ln, qn("a:tailEnd")).set("type", "triangle")
    return c


def riquadro(s, x, y, w, h, t, fill=T.ACCENT_1, color=T.BACKGROUND_1, size=13, bold=True, line=None):
    scheda(s, x, y, w, h, fill=fill, line=line)
    testo(s, t, x + 0.15, y, w - 0.3, h, size=size, bold=bold, color=color, anchor=MSO_ANCHOR.MIDDLE)


def note(s, t):
    ns = s.notes_slide
    if ns.notes_text_frame is None:
        # il notes master di pptxgenjs non ha il corpo: si copia quello delle note di una slide esistente
        modello = pres.slides[0].notes_slide
        for sh in modello.placeholders:
            if sh.placeholder_format.type == 2:  # BODY
                ns.shapes._spTree.append(copy.deepcopy(sh._element))
    ns.notes_text_frame.text = t


def imposta_testo(ph, t):
    """Riscrive il testo di un segnaposto conservando il primo run (e la sua formattazione)."""
    p = ph.text_frame.paragraphs[0]
    runs = p.runs
    runs[0].text = t
    for r in runs[1:]:
        r._r.getparent().remove(r._r)


def svuota(s):
    """Toglie tutto tranne i segnaposto (sezione, titolo, numero di pagina) e il grafico con la sua relazione."""
    for sh in list(s.shapes):
        if sh.is_placeholder:
            continue
        if sh.has_chart:
            rid = sh._element.graphic.graphicData.find(qn("c:chart")).get(qn("r:id"))
            s.part.drop_rel(rid)
        sh._element.getparent().remove(sh._element)


def nuova_dopo(rif):
    """Slide con il layout di rif, con i suoi segnaposto (compreso il numero di pagina), subito dopo rif."""
    s = pres.slides.add_slide(rif.slide_layout)
    for sh in list(s.shapes):
        sh._element.getparent().remove(sh._element)
    for sh in rif.shapes:
        if sh.is_placeholder:
            s.shapes._spTree.append(copy.deepcopy(sh._element))
    lst = pres.slides._sldIdLst
    nuovo = lst[-1]
    ids = [e.get("id") for e in lst]
    pos = ids.index(str(rif.slide_id))
    lst.remove(nuovo); lst.insert(pos + 1, nuovo)
    # sezione: dopo la slide di riferimento
    for e in pres.part._element.iter("{http://schemas.microsoft.com/office/powerpoint/2010/main}sldId"):
        if e.get("id") == str(rif.slide_id):
            n = copy.deepcopy(e); n.set("id", nuovo.get("id")); e.addnext(n)
            break
    return s


def segnaposti(s):
    ph = {p.placeholder_format.idx: p for p in s.placeholders}
    return ph[100], ph[101]


# ------------------------------------------------------------------ programma (slide 2)
agenda = pres.slides[1]
for sh in agenda.shapes:
    if sh.has_text_frame and sh.text_frame.text.startswith("Come è fatto ANSC"):
        imposta_testo(sh, "Casi d'uso, tipi atto, payload, sessione, firma, stati")

# ------------------------------------------------------------------ slide 6: come è fatto un UC
s6 = pres.slides[5]
svuota(s6)
k, t = segnaposti(s6)
imposta_testo(t, "Come è fatto un caso d'uso (UC)")

testo(s6, "Il codice: una risposta per ogni cifra", M, 1.95, 5.8, 0.4, size=18, bold=True, color=T.ACCENT_1, font=TITOLI)
cifre = [("1", "Registro", "Nascita"), ("1", "Tipo di evento", "Dichiarazione all'USC"),
         ("1", "Dichiarazione", "Filiazione nel matrimonio"), ("1", "Termine", "Entro 10 giorni"),
         ("1", "Dichiarante", "Il padre"), ("0", "Il nato", "Vivo")]
for i, (c, ruolo, val) in enumerate(cifre):
    y = 2.85 + i * 0.5
    cerchio(s6, M, y, 0.42, c, size=14)
    testo(s6, ruolo, M + 0.6, y + 0.07, 1.7, 0.35, size=13, color=T.ACCENT_3)
    testo(s6, val, M + 2.25, y + 0.05, 3.5, 0.35, size=15, bold=True)
testo(s6, [[("UC 11111000", {"bold": True, "color": T.ACCENT_1}),
            (" · codice motore Dic_Nasc_001", {})]],
      M, 2.38, 5.8, 0.4, size=13, color=T.ACCENT_3)
scheda(s6, M, 5.85, 5.8, 0.85)
testo(s6, [[("Cambia una risposta, cambia l'UC: ", {"bold": True, "color": T.ACCENT_1}),
            ("dichiara il procuratore del padre → 11114000; il bambino è nato morto → 11111100.", {})]],
      M + 0.2, 5.85, 5.4, 0.85, size=14, anchor=MSO_ANCHOR.MIDDLE)

testo(s6, "Che cosa dichiara ANSC per ogni UC", 6.75, 1.95, 5.98, 0.4, size=18, bold=True, color=T.ACCENT_1, font=TITOLI)
schede = [("Identità", "Codice, codice motore, descrizione, famiglia e tipo di contenuto (atto, annotazione, trascrizione)"),
          ("Sezioni e campi", "Dic_Nasc_001: 11 sezioni e 207 campi, ciascuno obbligatorio, facoltativo o condizionato"),
          ("Allegati", "I documenti richiesti e le condizioni in cui servono"),
          ("Formule", "Le diciture ministeriali previste per l'atto: da 1 a 22 per UC")]
for i, (tt, dd) in enumerate(schede):
    y = 2.5 + i * 1.07
    scheda(s6, 6.75, y, 5.98, 0.95)
    cerchio(s6, 6.95, y + 0.22, 0.5, i + 1, size=14)
    testo(s6, tt, 7.65, y + 0.1, 4.9, 0.35, size=15, bold=True)
    testo(s6, dd, 7.65, y + 0.43, 4.95, 0.5, size=13, color=T.ACCENT_3)
note(s6, "Ogni atto in ANSC appartiene a un caso d'uso (UC). Il codice non è un numero qualunque: ogni cifra è "
     "la risposta a una domanda, nell'ordine in cui la pone la web app. L'esempio 11111000 è la dichiarazione di "
     "nascita entro 10 giorni resa dal padre, nato vivo. Se dichiara il procuratore del padre l'UC diventa "
     "11114000; se il bambino è nato morto, 11111100. Per la morte i codici sono più corti (2101 = decesso in "
     "abitazione o in luogo pubblico). Per ogni UC ANSC pubblica un tracciato: sezioni (madre, padre, dichiarante, "
     "ufficiale…), campi con la loro obbligatorietà, documenti richiesti e formule. In tutto 374 UC in 7 famiglie.")

# ------------------------------------------------------------------ slide 7: tipi atto e UC
s7 = nuova_dopo(s6)
k, t = segnaposti(s7)
imposta_testo(k, "2  ·  LA TECNOLOGIA DI ANSC")
imposta_testo(t, "Tipologie di atti in SIPO e casi d'uso di ANSC")

XS, WS, XA, WA = M, 3.0, 5.2, 3.25
testo(s7, "SIPO · TIPO ATTO", XS, 1.95, WS, 0.3, size=12, bold=True, color=T.ACCENT_3)
testo(s7, "ANSC · CASO D'USO", XA, 1.95, WA, 0.3, size=12, bold=True, color=T.ACCENT_3)
testo(s7, "Decessi: un tipo atto, un UC", XS, 2.35, 7.8, 0.35, size=15, bold=True, color=T.ACCENT_1, font=TITOLI)
for i, (sipo, uc) in enumerate([("301 · Morte in abitazione a Roma", "2101 · Decesso in abitazione o in luogo pubblico"),
                                ("303 · Morte in ospedale a Roma", "2102 · Decesso in ospedale o casa di cura")]):
    y = 2.8 + i * 0.72
    riquadro(s7, XS, y, WS, 0.6, sipo, fill=T.BACKGROUND_2, color=T.TEXT_1)
    riquadro(s7, XA, y, WA, 0.6, uc, size=12)
    linea(s7, XS + WS + 0.05, y + 0.3, XA - 0.05, y + 0.3)
testo(s7, "Nascite: un tipo atto, più UC (decidono i dati del nato)", XS, 4.35, 7.8, 0.35, size=15, bold=True, color=T.ACCENT_1, font=TITOLI)
riquadro(s7, XS, 5.3, WS, 0.75, "1515 · Modello 30 · Nascita", fill=T.BACKGROUND_2, color=T.TEXT_1)
for i, uc in enumerate(["11111000 · nato vivo", "11111100 · nato morto", "11111200 · nato vivo, morto prima della denuncia"]):
    y = 4.8 + i * 0.66
    riquadro(s7, XA, y, WA, 0.54, uc, size=12)
    linea(s7, XS + WS + 0.05, 5.675, XA - 0.05, y + 0.27)
testo(s7, "Condizioni: FLG_NATO_MORTO e FLG_MORTO_PREDENUNCIA sul soggetto", XS, 6.15, 3.4, 0.6, size=11, italic=True, color=T.ACCENT_3)

scheda(s7, 8.75, 1.95, 3.98, 4.75)
testo(s7, "Come SIPO sceglie l'UC", 9.05, 2.15, 3.4, 0.4, size=18, bold=True, color=T.ACCENT_1, font=TITOLI)
elenco(s7, ["Il tipo atto indica gli UC possibili",
            "Per ogni UC una logica di scelta legge i dati dell'atto",
            "Vince il primo UC che risponde, in ordine di priorità",
            "Succede nel Riepilogo: se nessun UC risponde, SIPO lo segnala"],
       9.05, 2.7, 3.45, 2.9, size=14, numeri=True)
testo(s7, [[("435", {"bold": True, "color": T.ACCENT_1, "size": 20}), (" tipi atto in SIPO", {})],
           [("374", {"bold": True, "color": T.ACCENT_1, "size": 20}), (" casi d'uso in ANSC", {})]],
      9.05, 5.65, 3.45, 0.9, size=14)
note(s7, "SIPO non conosce gli UC: conosce i suoi tipi atto (CONF_TIPO_ATTI), con modello e maschera. La "
     "corrispondenza non è uno a uno. Per i decessi spesso sì: 301 morte in abitazione → UC 2101, 303 morte in "
     "ospedale → UC 2102. Per le nascite no: lo stesso tipo atto 1515 (Modello 30) porta a tre UC diversi secondo "
     "che il bambino sia nato vivo, nato morto o morto prima della denuncia (indicatori sul soggetto). Per questo la "
     "configurazione lega a ogni tipo atto i suoi UC possibili, con una logica di scelta e una priorità, e SIPO "
     "determina l'UC nel Riepilogo. L'operatore non sceglie il codice; se nessun UC risponde, l'atto va segnalato. "
     "Nella ricognizione delle nascite: 90 UC distribuiti su 15 modelli, e 12 UC senza modello in SIPO.")

# ------------------------------------------------------------------ slide 8: il payload
s8 = nuova_dopo(s7)
k, t = segnaposti(s8)
imposta_testo(k, "2  ·  LA TECNOLOGIA DI ANSC")
imposta_testo(t, "La struttura del payload: il modello evento")

scheda(s8, M, 1.95, 2.65, 4.75, fill=T.ACCENT_1)
testo(s8, "ModelEvento", M + 0.25, 2.15, 2.2, 0.5, size=22, bold=True, color=T.BACKGROUND_1, font=TITOLI)
testo(s8, ["Un solo modello per tutti gli atti di stato civile.",
           "La forma non cambia da un UC all'altro: idUsecase dice quali parti riempire.",
           "SIPO lo compone dai suoi dati e lo invia con VALIDA (R009)."],
      M + 0.25, 2.8, 2.2, 3.7, size=14, color=T.BACKGROUND_1)
for p in s8.shapes[-1].text_frame.paragraphs:
    pPr = p._p.get_or_add_pPr(); sp = etree.SubElement(pPr, qn("a:spcAft")); etree.SubElement(sp, qn("a:spcPts")).set("val", "900")

gruppi = [("Testata dell'atto", "idUsecase · idTipoEvento · idtipocontenuto · numeroatto · dataformazione · idComuneRegistrazione"),
          ("Le persone", "intestatari · madre · padre · dichiarante · interprete · ufficialeStatoCivile: stessa struttura di base per tutti"),
          ("I dati dell'evento", "datiDiNascita · datiDiMorte · datiEventoMatrimonio · datiEventoUnioneCivile · datiEventoCittadinanza …"),
          ("Documenti e collegamenti", "allegati · attiCollegati · datiAnnotazione · composizioneCompleta (il testo dell'atto)")]
XG, WG = 3.75, 5.0
tronco = 3.48
linea(s8, M + 2.65, 4.325, tronco, 4.325, punta=False)
centri = []
for i, (tt, dd) in enumerate(gruppi):
    y = 1.95 + i * 1.2
    scheda(s8, XG, y, WG, 1.05)
    testo(s8, tt, XG + 0.25, y + 0.1, WG - 0.5, 0.35, size=15, bold=True, color=T.ACCENT_1)
    testo(s8, dd, XG + 0.25, y + 0.45, WG - 0.45, 0.6, size=12, color=T.ACCENT_3)
    c = y + 0.525; centri.append(c)
    linea(s8, tronco, c, XG - 0.04, c)
linea(s8, tronco, centri[0], tronco, centri[-1], punta=False)

for i, (n, l) in enumerate([("111", "proprietà di primo livello"), ("374", "UC con lo stesso modello"),
                            ("154", "campi usati da un UC tipico (da 14 a 674)")]):
    y = 1.95 + i * 1.6
    testo(s8, n, 9.15, y, 3.58, 0.85, size=48, bold=True, color=T.ACCENT_1, font=TITOLI)
    testo(s8, l, 9.15, y + 0.85, 3.58, 0.6, size=14, color=T.ACCENT_3)
note(s8, "Il payload è il contenuto che SIPO invia ad ANSC: il modello evento (ModelEvento), definito nel contratto "
     "model_evento.yaml. È un unico albero per tutto lo stato civile, non una struttura per caso d'uso: 111 proprietà "
     "di primo livello raggruppabili in testata, persone, dati dell'evento per famiglia, documenti e collegamenti. "
     "Le persone condividono la stessa struttura di soggetto. Il campo idUsecase dice ad ANSC di quale UC si tratta, "
     "e quindi quali parti contano: un UC tipico ne usa circa 154 campi (da 14 a 674). SIPO costruisce il modello una "
     "sola volta dai dati dell'atto e dalla configurazione dei campi, lo mostra nell'Anteprima (R010) e lo deposita con "
     "VALIDA (R009). Lo stesso modello completo serve anche per la cancellazione (R011).")

pres.save(OUT)
print("scritto", OUT, "slide:", len(pres.slides))
