// Corso di formazione per gli USC: le nuove funzionalità di SIPO per ANSC.
// ⚠️ Genera SOLO la v0.1. Dal 07/11/2026 il .pptx è stato modificato a mano: le versioni successive
// si fanno sul file reale (formazione_usc_v0_2.py e seguenti), non rieseguendo questo script.
// Uso: NODE_PATH=<cartella con node_modules/pptxgenjs> node formazione_usc_pptx.js <uscita.pptx>
// Le schermate sono segnaposto da sostituire in PowerPoint.

const path = require("path");
const pptxgen = require("pptxgenjs");

const OUT = process.argv[2] || "FORMAZIONE_USC_Nuove-funzionalita-SIPO-ANSC_v0.1.pptx";

const THEME = {
  name: "Roma Capitale - Formazione USC",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "231F20", lt1: "FFFFFF", dk2: "8C0029", lt2: "F5EEF0",
    accent1: "8C0029", accent2: "C9A227", accent3: "5F5A5C", accent4: "2E7D5B",
    accent5: "B4485A", accent6: "E4D6DA", hlink: "8C0029", folHlink: "5F5A5C",
  },
};
const HEX = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Le nuove funzionalità di SIPO per ANSC";
pres.subject = "Formazione degli Ufficiali dello Stato Civile";
pres.author = "Sistemi Informativi";
pres.company = "Sistemi Informativi";
const C = pres.SchemeColor;

const W = 13.333, M = 0.6;
const FOOT = "Sistemi Informativi  ·  Formazione USC  ·  Le nuove funzionalità di SIPO per ANSC";

// ---------------------------------------------------------------- layout
pres.defineSlideMaster({
  title: "COPERTINA",
  background: { color: HEX.dk2 },
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: M, y: 1.5, w: 9, h: 0.5, fontSize: 16, bold: true, color: C.accent2, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: M, y: 2.05, w: 10.5, h: 2.0, fontSize: 44, bold: true, color: C.background1, fontFace: THEME.headFontFace, valign: "top", align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: M, y: 4.2, w: 10, h: 1.2, fontSize: 18, color: C.background1, valign: "top", margin: 0 }, text: "" } },
  ],
});

pres.defineSlideMaster({
  title: "CONTENUTO",
  background: { color: HEX.lt1 },
  margin: [0.5, 0.6, 0.8, 0.6],
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: M, y: 0.38, w: 11, h: 0.36, fontSize: 13, bold: true, color: C.accent1, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.74, w: W - 2 * M, h: 0.85, fontSize: 32, bold: true, color: C.text1, fontFace: THEME.headFontFace, valign: "top", align: "left", margin: 0 }, text: "" } },
    { text: { text: FOOT, options: { x: M, y: 7.02, w: 10, h: 0.3, fontSize: 10, color: C.accent3, margin: 0 } } },
  ],
  slideNumber: { x: W - M - 0.6, y: 7.02, w: 0.6, h: 0.3, fontSize: 10, color: C.accent3, align: "right", margin: 0 },
});

pres.defineSlideMaster({
  title: "CHIUSURA",
  background: { color: HEX.dk2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.55, w: W - 2 * M, h: 0.9, fontSize: 34, bold: true, color: C.background1, fontFace: THEME.headFontFace, align: "left", margin: 0 }, text: "" } },
    { text: { text: FOOT, options: { x: M, y: 7.02, w: 10, h: 0.3, fontSize: 10, color: C.accent6, margin: 0 } } },
  ],
  slideNumber: { x: W - M - 0.6, y: 7.02, w: 0.6, h: 0.3, fontSize: 10, color: C.accent6, align: "right", margin: 0 },
});

// ---------------------------------------------------------------- primitive
const SEZ = [
  "Dall'atto cartaceo all'atto digitale",
  "La tecnologia di ANSC",
  "L'integrazione SIPO → ANSC",
  "La numerazione comunale",
  "Operare con la web app ANSC",
];
let nOgg = 0;
const nome = (p) => `${p}_${++nOgg}`;

function contenuto(sez, titolo, note) {
  const s = pres.addSlide({ masterName: "CONTENUTO", sectionTitle: SEZ[sez - 1] });
  s.addText(`${sez}  ·  ${SEZ[sez - 1].toUpperCase()}`, { placeholder: "kicker" });
  s.addText(titolo, { placeholder: "title" });
  if (note) s.addNotes(note);
  return s;
}

function testo(s, t, o) {
  s.addText(t, Object.assign({ isTextBox: true, fontSize: 15, color: C.text1, valign: "top", margin: 0, objectName: nome("testo") }, o));
}

function elenco(s, voci, o) {
  const runs = voci.map((v, i) => {
    const r = Array.isArray(v) ? v : [{ text: v }];
    return r.map((p, j) => ({
      text: p.text,
      options: Object.assign({ bullet: j === 0 ? { indent: 16 } : undefined, breakLine: j === r.length - 1 && i < voci.length - 1, paraSpaceAfter: 6 }, p.options || {}),
    }));
  }).flat();
  s.addText(runs, Object.assign({ isTextBox: true, fontSize: 15, color: C.text1, valign: "top", margin: 0, objectName: nome("elenco") }, o));
}

function scheda(s, x, y, w, h, o = {}) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.08, objectName: nome("scheda"),
    fill: { color: o.fill || C.background2 }, line: { color: o.line || o.fill || C.background2, width: 1 },
  });
}

function cerchio(s, x, y, d, etichetta, o = {}) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: o.fill || C.accent1 }, line: { color: o.fill || C.accent1 }, objectName: nome("cerchio") });
  s.addText(String(etichetta), { isTextBox: true, x, y, w: d, h: d, align: "center", valign: "middle", margin: 0, bold: true, fontSize: o.fontSize || 18, color: o.color || C.background1, fontFace: THEME.headFontFace, objectName: nome("num") });
}

function freccia(s, x1, y1, x2, y2, o = {}) {
  s.addShape(pres.shapes.LINE, {
    x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1) || 0.001, h: Math.abs(y2 - y1) || 0.001,
    flipH: x2 < x1, flipV: y2 < y1, objectName: nome("freccia"),
    line: { color: o.color || C.accent3, width: o.width || 2, endArrowType: "triangle", dashType: o.dash || "solid" },
  });
}

function segnaposto(s, x, y, w, h, etichetta) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.06, objectName: nome("segnaposto"),
    fill: { color: C.background2 }, line: { color: C.accent1, width: 1.25, dashType: "dash" },
  });
  s.addText([
    { text: "SCHERMATA DA INSERIRE", options: { bold: true, fontSize: 12, color: C.accent1, breakLine: true } },
    { text: etichetta, options: { fontSize: 12, color: C.accent3 } },
  ], { isTextBox: true, x: x + 0.2, y, w: w - 0.4, h, align: "center", valign: "middle", margin: 0, objectName: nome("segnaposto_testo") });
}

function chip(s, x, y, w, h, t, o = {}) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.1, fill: { color: o.fill || C.accent1 }, line: { color: o.line || o.fill || C.accent1, width: 1 }, objectName: nome("chip") });
  s.addText(t, { isTextBox: true, x, y, w, h, align: "center", valign: "middle", margin: 2, fontSize: o.fontSize || 13, bold: o.bold !== false, color: o.color || C.background1, objectName: nome("chip_testo") });
}

// ================================================================ 1 copertina
{
  pres.addSection({ title: "Apertura" });
  const s = pres.addSlide({ masterName: "COPERTINA", sectionTitle: "Apertura" });
  s.addText("CORSO DI FORMAZIONE PER GLI UFFICIALI DELLO STATO CIVILE", { placeholder: "kicker" });
  s.addText("Le nuove funzionalità di SIPO per l'Archivio Nazionale dello Stato Civile", { placeholder: "title" });
  s.addText("Dall'atto cartaceo all'atto digitale: come si forma un atto in ANSC lavorando in SIPO", { placeholder: "body" });
  // segnaposto dei loghi
  [["LOGO ROMA CAPITALE", 0.6], ["LOGO SISTEMI INFORMATIVI", 3.6]].forEach(([t, x]) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 5.9, w: 2.7, h: 0.9, rectRadius: 0.06, fill: { color: HEX.dk2 }, line: { color: C.accent2, width: 1, dashType: "dash" }, objectName: nome("logo") });
    s.addText(t, { isTextBox: true, x, y: 5.9, w: 2.7, h: 0.9, align: "center", valign: "middle", fontSize: 11, bold: true, color: C.accent2, margin: 0, objectName: nome("logo_testo") });
  });
  s.addText([
    { text: "A cura di Sistemi Informativi", options: { bold: true, breakLine: true } },
    { text: "Dipartimento Trasformazione Digitale · Roma Capitale" },
  ], { isTextBox: true, x: 7.6, y: 5.9, w: 5.1, h: 0.9, align: "right", valign: "middle", fontSize: 14, color: C.background1, margin: 0, objectName: nome("autore") });
  s.addNotes("Benvenuto. Il corso presenta le funzioni che SIPO offre per formare gli atti nell'Archivio Nazionale dello Stato Civile (ANSC). Durata indicativa: 60-75 minuti, con spazio per le domande alla fine di ogni parte. Le schermate tratteggiate sono segnaposto: verranno sostituite con le immagini dell'applicativo rilasciato.");
}

// ================================================================ 2 agenda
{
  const s = pres.addSlide({ masterName: "CONTENUTO", sectionTitle: "Apertura" });
  s.addText("PROGRAMMA", { placeholder: "kicker" });
  s.addText("Cinque passaggi, dall'idea all'operatività", { placeholder: "title" });
  const descr = [
    "Che cosa cambia quando l'atto nasce digitale e nazionale",
    "Come è fatto ANSC: casi d'uso, sessione, firma, stati dell'atto",
    "Il percorso dell'atto nelle pagine di SIPO, pulsante per pulsante",
    "Chi assegna il numero dell'atto e come si evita di perderlo",
    "Le funzioni che restano sulla web app nazionale",
  ];
  SEZ.forEach((t, i) => {
    const y = 1.95 + i * 0.95;
    cerchio(s, M, y, 0.7, i + 1);
    testo(s, t, { x: M + 1.0, y: y + 0.02, w: 6.2, h: 0.4, fontSize: 20, bold: true, fontFace: THEME.headFontFace });
    testo(s, descr[i], { x: M + 1.0, y: y + 0.42, w: 6.4, h: 0.35, fontSize: 14, color: C.accent3 });
  });
  scheda(s, 8.3, 1.95, 4.43, 4.6, { fill: C.background2 });
  testo(s, "A chi serve", { x: 8.6, y: 2.2, w: 3.9, h: 0.4, fontSize: 18, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
  elenco(s, [
    "Ufficiali dello stato civile che formano e firmano gli atti",
    "Operatori di sportello che preparano l'atto in SIPO",
    "Referenti che seguono le eccezioni dal back-office",
  ], { x: 8.6, y: 2.75, w: 3.9, h: 2.0, fontSize: 15 });
  testo(s, "Le parti 2 e 3 contengono cenni tecnici: servono a capire che cosa succede dietro ogni pulsante, non sono necessari per operare.", { x: 8.6, y: 4.95, w: 3.9, h: 1.4, fontSize: 13, italic: true, color: C.accent3 });
  s.addNotes("Presentare il percorso. Le prime due parti danno il quadro; la terza è il cuore operativo; la quarta e la quinta chiudono su due temi che generano molte domande: il numero dell'atto e quando usare la web app invece di SIPO.");
}

// ================================================================ 3 cartaceo vs digitale
{
  pres.addSection({ title: SEZ[0] });
  const s = contenuto(1, "Dal registro cartaceo all'atto nativo digitale",
    "L'atto non è più una pagina del registro del Comune: nasce digitale, firmato digitalmente, e vive nell'archivio nazionale. Il fondamento è l'art. 10 del DL 78/2015, che istituisce ANSC, e il D.M. 18/10/2022 che ne disciplina il funzionamento. Sottolineare che cambia il supporto, non la responsabilità: l'atto resta dell'ufficiale dello stato civile che lo forma.");
  const col = (x, titolo, voci, scuro) => {
    scheda(s, x, 1.95, 5.5, 4.75, { fill: scuro ? C.accent1 : C.background2 });
    testo(s, titolo, { x: x + 0.35, y: 2.15, w: 4.8, h: 0.5, fontSize: 20, bold: true, fontFace: THEME.headFontFace, color: scuro ? C.background1 : C.accent1 });
    elenco(s, voci, { x: x + 0.35, y: 2.8, w: 4.85, h: 3.7, fontSize: 15, color: scuro ? C.background1 : C.text1 });
  };
  col(M, "Ieri: il registro del Comune", [
    "L'atto è redatto e firmato a mano sul registro",
    "Lo individuano anno, parte, serie e numero",
    "Le annotazioni si scrivono a margine",
    "Le comunicazioni ad altri Comuni ed enti viaggiano per posta o PEC",
    "Una correzione si fa sul foglio, entro la giornata",
  ], false);
  col(W - M - 5.5, "Oggi: l'atto in ANSC", [
    "L'atto si forma nell'archivio nazionale, con firma digitale",
    "Riceve un identificativo nazionale unico (idAnsc)",
    "Le annotazioni arrivano come notifiche da confermare",
    "La comunicazione all'anagrafe parte dall'atto stesso",
    "Dopo la firma dell'ufficiale l'atto non si modifica più",
  ], true);
  cerchio(s, W / 2 - 0.35, 3.95, 0.7, "→", { fill: C.accent2, fontSize: 22 });
}

// ================================================================ 4 cosa cambia
{
  const s = contenuto(1, "Tre novità che cambiano il lavoro dell'ufficiale",
    "Identificativo: il formato è ANNO-progressivo nazionale-progressivo comunale-codice ISTAT del Comune; SIPO lo registra sull'atto e lo mostra nelle ricerche. Firma: oggi a Roma un atto si corregge fino a mezzanotte; con ANSC la finestra si chiude con la firma dell'ufficiale, dopo serve una rettifica. Adesione progressiva: per gli atti che restano su carta, le annotazioni arrivano come notifica e vanno riportate sul registro.");
  const box = [
    ["1", "Un identificativo nazionale", "Ogni atto riceve l'idAnsc al momento della validazione. Lo compongono anno, progressivo nazionale, progressivo comunale e codice ISTAT del Comune.", "ANNO - NAZ - COM - ISTAT"],
    ["2", "La firma chiude l'atto", "Oggi un atto si corregge fino a fine giornata. Con ANSC, dopo la firma dell'ufficiale l'atto è formato: si interviene solo con rettifica o annotazione.", "Firma = punto di non ritorno"],
    ["3", "Carta e digitale convivono", "Molti atti precedenti restano cartacei. Se ANSC annota un atto cartaceo di Roma, la notifica va confermata e l'annotazione riportata sul registro.", "Adesione progressiva"],
  ];
  box.forEach(([n, t, d, k], i) => {
    const x = M + i * 4.13, w = 3.83;
    scheda(s, x, 1.95, w, 4.75);
    cerchio(s, x + 0.35, 2.2, 0.65, n);
    testo(s, t, { x: x + 0.35, y: 3.05, w: w - 0.7, h: 0.8, fontSize: 19, bold: true, fontFace: THEME.headFontFace });
    testo(s, d, { x: x + 0.35, y: 3.85, w: w - 0.7, h: 2.0, fontSize: 14 });
    testo(s, k, { x: x + 0.35, y: 6.0, w: w - 0.7, h: 0.4, fontSize: 14, bold: true, italic: true, color: C.accent1 });
  });
}

// ================================================================ 5 ANSC in sintesi
{
  pres.addSection({ title: SEZ[1] });
  const s = contenuto(2, "ANSC: un archivio nazionale, due porte di accesso",
    "ANSC è la piattaforma nazionale del Ministero dell'Interno, realizzata e gestita da Sogei. Si accede in due modi: la web app nel browser, oppure il gestionale del Comune tramite servizi (API). Roma ha scelto il gestionale: si lavora in SIPO. La web app resta però necessaria per alcune funzioni (parte 5). I numeri: 374 casi d'uso in 7 famiglie, 25 servizi applicativi, 11 stati possibili di un atto.");
  // due porte
  const porta = (x, titolo, sotto, scelta) => {
    scheda(s, x, 1.95, 3.6, 1.9, { fill: scelta ? C.accent1 : C.background2 });
    testo(s, titolo, { x: x + 0.3, y: 2.12, w: 3.0, h: 0.5, fontSize: 19, bold: true, fontFace: THEME.headFontFace, color: scelta ? C.background1 : C.accent1 });
    testo(s, sotto, { x: x + 0.3, y: 2.65, w: 3.05, h: 1.1, fontSize: 14, color: scelta ? C.background1 : C.text1 });
  };
  porta(M, "Web app ANSC", "Il browser dell'ufficiale, con smart card o SPID. Copre tutti i casi d'uso.", false);
  porta(M + 3.9, "Gestionale: SIPO", "Le maschere di SIPO, collegate ad ANSC tramite servizi. È la scelta di Roma.", true);
  chip(s, M + 7.8, 2.55, 1.0, 0.7, "→", { fill: C.accent2, fontSize: 20 });
  scheda(s, M + 9.1, 1.95, 3.03, 1.9, { fill: C.text1 });
  testo(s, "ANSC", { x: M + 9.4, y: 2.12, w: 2.5, h: 0.5, fontSize: 22, bold: true, fontFace: THEME.headFontFace, color: C.background1 });
  testo(s, "Archivio Nazionale dello Stato Civile · Ministero dell'Interno · Sogei", { x: M + 9.4, y: 2.65, w: 2.5, h: 1.1, fontSize: 13, color: C.background1 });
  // numeri
  [["374", "casi d'uso"], ["7", "famiglie di atti"], ["25", "servizi applicativi"], ["11", "stati di un atto"]].forEach(([n, l], i) => {
    const x = M + i * 3.07;
    testo(s, n, { x, y: 4.35, w: 2.9, h: 1.2, fontSize: 64, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
    testo(s, l, { x, y: 5.55, w: 2.9, h: 0.4, fontSize: 16, color: C.accent3 });
  });
  testo(s, "Fonte: repository ufficiale ANSC (decodifiche ANSC_03 e ANSC_11, contratti dei servizi R001-R024 e R901).", { x: M, y: 6.35, w: 12, h: 0.35, fontSize: 11, color: C.accent3, italic: true });
}

// ================================================================ 6 caso d'uso
{
  const s = contenuto(2, "Il caso d'uso: ogni atto ha il suo percorso",
    "Ogni atto in ANSC appartiene a un caso d'uso (UC), che decide quali dati, documenti e formule servono. Il codice si compone di scelte successive: l'esempio è la dichiarazione di nascita entro 10 giorni resa dal padre (11111000). Cambiando dichiarante cambia il caso d'uso. In SIPO l'operatore non sceglie il codice: SIPO lo determina dai dati dell'atto nella pagina di Riepilogo. Il grafico mostra quanti casi d'uso ha ciascuna famiglia.");
  testo(s, "Esempio: UC 1.1.1.1.1.0.0.0", { x: M, y: 1.9, w: 6, h: 0.4, fontSize: 17, bold: true, color: C.accent1 });
  const passi = [["1", "Nascita"], ["1", "Dichiarazione all'USC"], ["1", "Filiazione nel matrimonio"], ["1", "Entro 10 giorni"], ["1", "Resa dal padre"], ["0", "Nato vivo"]];
  passi.forEach(([c, t], i) => {
    const y = 2.45 + i * 0.66;
    cerchio(s, M, y, 0.5, c, { fontSize: 15 });
    testo(s, t, { x: M + 0.7, y: y + 0.08, w: 4.6, h: 0.4, fontSize: 15 });
  });
  scheda(s, M, 6.45 - 0.05, 5.7, 0.45, { fill: C.background2 });
  testo(s, "SIPO determina il caso d'uso dai dati: l'operatore non lo digita.", { x: M + 0.2, y: 6.45, w: 5.4, h: 0.35, fontSize: 13, bold: true, color: C.accent1 });
  s.addChart(pres.charts.BAR, [{
    name: "Casi d'uso",
    labels: ["Nascita", "Cittadinanza", "Trascrizioni", "Matrimoni", "Morte", "Unioni civili", "Riconoscimenti"],
    values: [143, 64, 55, 40, 25, 24, 23],
  }], {
    x: 6.75, y: 1.85, w: 6.0, h: 4.9, barDir: "bar", objectName: "grafico_famiglie",
    showTitle: true, title: "Casi d'uso per famiglia (374 in tutto)", titleFontSize: 14, titleColor: HEX.dk1, titleFontFace: "+mn-lt",
    chartColors: [HEX.accent1], showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 12, dataLabelColor: HEX.dk1, dataLabelFontFace: "+mn-lt",
    catAxisLabelColor: HEX.accent3, catAxisLabelFontSize: 12, catAxisLabelFontFace: "+mn-lt", catAxisOrientation: "maxMin",
    valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false, barGapWidthPct: 45,
  });
}

// ================================================================ 7 architettura
{
  const s = contenuto(2, "Cenni tecnici: chi parla con chi",
    "Dalla postazione l'operatore usa solo SIPO. SIPO non chiama ANSC direttamente: passa da un componente dedicato, il concentratore, che custodisce il certificato del Comune e il codice di sessione dell'ufficiale e firma ogni chiamata. Il browser non parla mai con ANSC per gli atti. Accanto ci sono due servizi di supporto: la numerazione comunale e i dizionari ANSC (le tabelle di decodifica nazionali, aggiornate su comando).");
  const nodi = [
    [M, "Postazione USC", "Browser con SIPO · certificato di postazione · smart card o SPID per il codice OTP"],
    [M + 3.2, "SIPO", "Maschere di stato civile · base dati del Comune · pagine nuove per ANSC"],
    [M + 6.4, "Concentratore ANSC", "Custodisce certificato del Comune e codice di sessione · firma le chiamate"],
    [M + 9.6, "ANSC", "Archivio nazionale · servizi R001-R024 · web app"],
  ];
  nodi.forEach(([x, t, d], i) => {
    scheda(s, x, 2.0, 2.53, 2.55, { fill: i === 2 ? C.accent1 : i === 3 ? C.text1 : C.background2 });
    const chiaro = i >= 2;
    testo(s, t, { x: x + 0.22, y: 2.15, w: 2.1, h: 0.75, fontSize: 17, bold: true, fontFace: THEME.headFontFace, color: chiaro ? C.background1 : C.accent1 });
    testo(s, d, { x: x + 0.22, y: 2.95, w: 2.1, h: 1.5, fontSize: 13, color: chiaro ? C.background1 : C.text1 });
    if (i < 3) freccia(s, x + 2.58, 3.27, x + 3.15, 3.27, { color: C.accent1, width: 2.5 });
  });
  // supporto
  [[M + 3.2, "Numerazione comunale", "be-numeratore-comunale: assegna il numero dell'atto"], [M + 6.4, "Dizionari ANSC", "Tabelle di decodifica nazionali, lette da SIPO"]].forEach(([x, t, d]) => {
    scheda(s, x, 5.15, 2.53, 1.3, { fill: C.lt1 || C.background1, line: C.accent6 });
    testo(s, t, { x: x + 0.22, y: 5.25, w: 2.1, h: 0.4, fontSize: 14, bold: true, color: C.accent1 });
    testo(s, d, { x: x + 0.22, y: 5.65, w: 2.1, h: 0.75, fontSize: 12, color: C.accent3 });
    freccia(s, x + 1.26, 5.1, x + 1.26, 4.6, { color: C.accent3, width: 1.5, dash: "dash" });
  });
  scheda(s, M + 9.6, 5.15, 2.53, 1.3, { fill: C.background2 });
  testo(s, "Il browser non parla mai con ANSC per formare gli atti.", { x: M + 9.8, y: 5.25, w: 2.15, h: 1.1, fontSize: 13, bold: true, color: C.accent1, valign: "middle" });
}

// ================================================================ 8 sessione e firma
{
  const s = contenuto(2, "Sessione e firma: due prove di presenza dell'ufficiale",
    "Il codice OTP di sessione si genera sulla web app OTP di ANSC con smart card o SPID e vale 4 ore; SIPO lo chiede alla prima operazione che serve e ne mostra il tempo residuo. Se sta per scadere (proposta: meno di 15 minuti) SIPO ne chiede uno nuovo prima di iniziare, per non interrompere una sequenza a metà. La firma, invece, richiede un OTP per ogni singolo atto: non può essere automatizzata. Per questo non esistono invii in blocco.");
  const col = (x, n, t, voci) => {
    scheda(s, x, 1.95, 5.85, 4.75);
    cerchio(s, x + 0.35, 2.2, 0.75, n, { fill: C.accent2, color: C.text1, fontSize: 16 });
    testo(s, t, { x: x + 1.3, y: 2.3, w: 4.3, h: 0.6, fontSize: 20, bold: true, fontFace: THEME.headFontFace, color: C.accent1 });
    elenco(s, voci, { x: x + 0.35, y: 3.2, w: 5.2, h: 3.3, fontSize: 15 });
  };
  col(M, "4 h", "Il codice di sessione", [
    "Si genera sulla web app OTP di ANSC, con smart card o SPID",
    "Si inserisce in SIPO una volta e vale fino a 4 ore",
    "SIPO mostra il tempo residuo e ne chiede uno nuovo prima che scada",
    "Lo custodisce il concentratore, legato a ufficiale e postazione",
  ]);
  col(W - M - 5.85, "1:1", "La firma dell'atto", [
    "Ogni firma richiede un codice OTP dedicato",
    "Firmano i dichiaranti, poi l'ufficiale",
    "Nessuna firma automatica e nessun invio in blocco",
    "La firma dell'ufficiale forma l'atto",
  ]);
}

// ================================================================ 9 stati
{
  const s = contenuto(2, "Gli stati dell'atto in ANSC",
    "Lo stato dell'atto è un dato di ANSC (decodifica ANSC_11) e SIPO lo replica. Il percorso ordinario va da BOZZA, dopo la validazione, a FIRMATO DA USC. Le uscite: CANCELLATO se si elimina l'atto prima della firma dell'ufficiale (servizio R011); ANNULLATO con una rettifica su atto formato; INEFFICACE solo dalla web app, funzione oggi disabilitata da ANSC (rilascio 1.52.0). Gli altri stati riguardano annotazioni e notifiche.");
  const linea = [["1", "BOZZA", "dopo VALIDA, con idAnsc"], ["4", "FIRMATO DAL DICHIARANTE", ""], ["11", "FIRMATO PER CONFORMITÀ", "se ci sono documenti"], ["5", "FIRMATO DA USC", "atto formato"]];
  linea.forEach(([n, t, d], i) => {
    const x = M + i * 3.1;
    chip(s, x, 2.2, 2.7, 0.9, `${n} · ${t}`, { fill: i === 3 ? C.accent4 : C.accent1, fontSize: 13 });
    if (d) testo(s, d, { x, y: 3.17, w: 2.7, h: 0.35, fontSize: 13, color: C.accent3, align: "center" });
    if (i < 3) freccia(s, x + 2.72, 2.65, x + 3.08, 2.65, { color: C.accent3 });
  });
  testo(s, "Le uscite dal percorso", { x: M, y: 3.95, w: 6, h: 0.4, fontSize: 18, bold: true, fontFace: THEME.headFontFace, color: C.accent1 });
  [["9 · CANCELLATO", "Atto eliminato prima della firma dell'ufficiale (ELIMINA EVENTO)"],
   ["3 · ANNULLATO", "Rettifica di annullamento su un atto già formato"],
   ["10 · INEFFICACE", "Solo dalla web app; oggi disabilitato da ANSC"]].forEach(([t, d], i) => {
    const y = 4.5 + i * 0.72;
    chip(s, M, y, 2.7, 0.55, t, { fill: C.background2, color: C.accent1, line: C.accent6 });
    testo(s, d, { x: M + 2.95, y: y + 0.1, w: 4.6, h: 0.45, fontSize: 14 });
  });
  scheda(s, 8.55, 3.95, 4.18, 2.75);
  testo(s, "Altri stati", { x: 8.85, y: 4.1, w: 3.6, h: 0.4, fontSize: 16, bold: true, color: C.accent1 });
  elenco(s, ["2 · CONFERMATO", "6 · GENERATO DA SISTEMA", "7 · APPROVATO", "8 · RIFIUTATA"], { x: 8.85, y: 4.55, w: 3.6, h: 1.4, fontSize: 14 });
  testo(s, "Riguardano annotazioni, notifiche e provvedimenti di rifiuto.", { x: 8.85, y: 6.0, w: 3.6, h: 0.6, fontSize: 12, italic: true, color: C.accent3 });
}

// ================================================================ 10 SIPO al centro
{
  pres.addSection({ title: SEZ[2] });
  const s = contenuto(3, "SIPO resta al centro del lavoro",
    "Il principio dell'integrazione: si continua a lavorare in SIPO. L'atto si registra prima nella base dati del Comune e poi passa ad ANSC: ANSC è il passo che lo finalizza. Non c'è una coda di invii in differita, perché ogni atto richiede la presenza dell'ufficiale. Se una risposta di ANSC non arriva, SIPO non ritenta alla cieca: verifica lo stato reale dell'atto in ANSC e solo dopo decide.");
  scheda(s, M, 1.95, 4.6, 4.75, { fill: C.accent1 });
  testo(s, "«Si lavora nelle maschere di SIPO. ANSC è il passo che forma l'atto, non un nuovo programma da imparare.»", { x: M + 0.4, y: 2.3, w: 3.8, h: 3.0, fontSize: 22, italic: true, color: C.background1, fontFace: THEME.headFontFace });
  testo(s, "Principio dell'integrazione", { x: M + 0.4, y: 5.9, w: 3.8, h: 0.4, fontSize: 13, bold: true, color: C.accent2 });
  const righe = [
    ["Le maschere di sempre", "Dati anagrafici e dettaglio dell'atto restano quelli di SIPO; si aggiungono solo le pagine per validazione, firme e chiusura."],
    ["Prima SIPO, poi ANSC", "L'atto è salvato nella base dati del Comune e da lì inviato ad ANSC."],
    ["Ogni atto è presidiato", "Nessuna coda di invii automatici: validazione e firma avvengono con l'ufficiale presente."],
    ["Mai un secondo invio alla cieca", "Se l'esito è incerto, SIPO legge lo stato reale in ANSC prima di ripetere."],
  ];
  righe.forEach(([t, d], i) => {
    const y = 1.95 + i * 1.2;
    cerchio(s, 5.65, y + 0.05, 0.55, i + 1, { fontSize: 15 });
    testo(s, t, { x: 6.45, y, w: 6.2, h: 0.4, fontSize: 17, bold: true });
    testo(s, d, { x: 6.45, y: y + 0.42, w: 6.25, h: 0.7, fontSize: 14, color: C.accent3 });
  });
}

// ================================================================ 11 quattro fasi
{
  const s = contenuto(3, "Il percorso dell'atto in quattro fasi",
    "A: nei dati anagrafici l'intestatario va cercato in ANSC (servizio R005); è obbligatorio cercarlo, non trovarlo. B: nel Riepilogo SIPO determina il caso d'uso, si indicano i firmatari e si caricano i documenti; una verifica locale segnala i dati mancanti prima dell'invio. C: all'Anteprima si assegna il numero comunale, si vede l'atto come lo comporrà ANSC e con VALIDA lo si deposita: ANSC restituisce l'idAnsc e l'atto è in BOZZA. D: firme dei dichiaranti, attestazione di conformità se ci sono documenti, firma dell'ufficiale (Definisci: in SIPO l'atto è DEFINITO), poi Chiudi.");
  const fasi = [
    ["A", "Dati e dettaglio", ["Maschere SIPO di sempre", "Ricerca dell'intestatario in ANSC (R005)"]],
    ["B", "Riepilogo", ["Caso d'uso determinato da SIPO", "Firmatari", "Documenti caricati (R001)", "Verifica locale dei dati"]],
    ["C", "Anteprima e VALIDA", ["Numero comunale", "Anteprima dell'atto (R010)", "VALIDA: deposito (R009), idAnsc, BOZZA"]],
    ["D", "Firme e chiusura", ["Firme dei dichiaranti", "Attestazione di conformità", "Firma USC · Definisci", "Chiudi"]],
  ];
  fasi.forEach(([l, t, v], i) => {
    const x = M + i * 3.1, w = 2.85;
    scheda(s, x, 1.95, w, 4.15, { fill: i === 3 ? C.accent1 : C.background2 });
    const chiaro = i === 3;
    cerchio(s, x + 0.3, 2.15, 0.7, l, { fill: chiaro ? C.accent2 : C.accent1, color: chiaro ? C.text1 : C.background1, fontSize: 20 });
    testo(s, t, { x: x + 0.3, y: 3.0, w: w - 0.5, h: 0.5, fontSize: 18, bold: true, fontFace: THEME.headFontFace, color: chiaro ? C.background1 : C.accent1 });
    elenco(s, v, { x: x + 0.3, y: 3.55, w: w - 0.5, h: 2.5, fontSize: 14, color: chiaro ? C.background1 : C.text1 });
    if (i < 3) freccia(s, x + w + 0.02, 4.0, x + 3.08, 4.0, { color: C.accent1, width: 2.5 });
  });
  scheda(s, M, 6.3, W - 2 * M, 0.5, { fill: C.lt1 || C.background1, line: C.accent2 });
  testo(s, "Punto di non ritorno: la firma dell'ufficiale. Fino a lì si può tornare ai dati; dopo, l'atto è formato.", { x: M + 0.25, y: 6.37, w: W - 2 * M - 0.5, h: 0.36, fontSize: 14, bold: true, color: C.accent1 });
}

// ================================================================ 12 dietro ogni pulsante
{
  const s = contenuto(3, "Che cosa succede dietro ogni pulsante",
    "Tabella di consultazione per chi vuole sapere quale servizio ANSC si attiva. Non serve ricordare i codici: servono a parlare con l'assistenza quando qualcosa non va. Stato SIPO 2 = DEFINITO dopo la firma dell'ufficiale.");
  const h = (t) => ({ text: t, options: { bold: true, color: C.background1, fill: { color: C.accent1 } } });
  const righe = [
    ["Ricerca del soggetto", "Cerca l'intestatario e le persone dell'atto in ANSC", "R005", "—"],
    ["Carica documento", "Invia il documento e ne segue la verifica antivirus", "R001", "documento: Inserito"],
    ["Anteprima", "Assegna il numero comunale e mostra l'atto composto", "R010", "—"],
    ["VALIDA", "Deposita l'atto e riceve l'identificativo nazionale", "R009", "BOZZA, con idAnsc"],
    ["Firma del dichiarante", "Registra la firma di ciascun dichiarante", "R006", "FIRMATO DAL DICHIARANTE"],
    ["Attestazione di conformità", "Genera e firma l'attestazione dei documenti", "R010 · R007", "FIRMATO PER CONFORMITÀ"],
    ["Firma USC · Definisci", "L'ufficiale firma: l'atto è formato", "R007", "FIRMATO DA USC · SIPO DEFINITO"],
    ["Chiudi", "Registra la data di validità dell'atto firmato", "R014", "—"],
    ["ELIMINA EVENTO", "Cancella l'atto non ancora firmato dall'ufficiale", "R011", "CANCELLATO"],
  ];
  const corpo = righe.map((r, i) => r.map((c, j) => ({ text: c, options: { bold: j === 0, color: j === 2 ? C.accent1 : C.text1, fill: { color: i % 2 ? C.background1 : C.background2 } } })));
  s.addTable([[h("Pulsante"), h("Che cosa fa"), h("Servizio ANSC"), h("Stato dopo")], ...corpo], {
    x: M, y: 1.9, w: W - 2 * M, colW: [2.75, 4.85, 1.55, 2.98], fontSize: 13, fontFace: THEME.bodyFontFace, rowH: 0.47,
    border: { type: "solid", pt: 0.5, color: HEX.accent6 }, valign: "middle", margin: [0.03, 0.1, 0.03, 0.1], objectName: "tabella_pulsanti",
  });
}

// ================================================================ 13 documenti
{
  const s = contenuto(3, "I documenti allegati all'atto",
    "Ogni caso d'uso dichiara quali documenti servono: obbligatori, facoltativi o richiesti solo in certe condizioni. Il documento caricato passa per la verifica di ANSC: si procede solo quando è nello stato Inserito. Formati ammessi da ANSC: PDF, JPG, TIF e P7M. Nell'attestazione di conformità l'ufficiale sceglie, atto per atto, quali documenti includere; SIPO li propone tutti selezionati.");
  testo(s, "Quali documenti", { x: M, y: 1.95, w: 6, h: 0.4, fontSize: 18, bold: true, fontFace: THEME.headFontFace, color: C.accent1 });
  [["O", "Obbligatorio", "senza, l'atto non si valida"], ["F", "Facoltativo", "a giudizio dell'ufficiale"], ["C", "Condizionato", "richiesto solo in certi casi"]].forEach(([l, t, d], i) => {
    const y = 2.5 + i * 0.75;
    cerchio(s, M, y, 0.55, l, { fontSize: 16 });
    testo(s, t, { x: M + 0.75, y: y + 0.02, w: 2.2, h: 0.5, fontSize: 15, bold: true, valign: "middle" });
    testo(s, d, { x: M + 2.6, y: y + 0.02, w: 3.6, h: 0.5, fontSize: 14, color: C.accent3, valign: "middle" });
  });
  testo(s, "Il percorso del documento in ANSC", { x: M, y: 4.85, w: 6.3, h: 0.4, fontSize: 18, bold: true, fontFace: THEME.headFontFace, color: C.accent1 });
  const st = [["Ricevuto", C.background2, C.accent1], ["In verifica", C.background2, C.accent1], ["Inserito", C.accent4, C.background1]];
  st.forEach(([t, f, c], i) => {
    const x = M + i * 2.1;
    chip(s, x, 5.4, 1.8, 0.55, t, { fill: f, color: c, line: C.accent6 });
    if (i < 2) freccia(s, x + 1.82, 5.67, x + 2.08, 5.67, { color: C.accent3 });
  });
  testo(s, "Solo «Inserito» consente di proseguire. «Rifiutato» chiede un nuovo caricamento. Formati: PDF, JPG, TIF, P7M.", { x: M, y: 6.1, w: 6.3, h: 0.6, fontSize: 13, color: C.accent3 });
  segnaposto(s, 7.25, 1.95, 5.48, 4.75, "Pagina SIPO dei documenti dell'atto: elenco, stato di ciascun documento, pulsante Carica documento");
}

// ================================================================ 14 correggere
{
  const s = contenuto(3, "Correggere, tornare indietro, cancellare",
    "Prima di VALIDA i dati si modificano come sempre. Dopo VALIDA si può tornare ai dati: SIPO rifà la validazione dello stesso atto. Dopo che i dichiaranti hanno firmato il ritorno è ammesso solo se tutti possono firmare di nuovo. Se cambia il caso d'uso l'atto va cancellato e rifatto (comportamento da confermare). ELIMINA EVENTO, prima della firma dell'ufficiale, porta l'atto in CANCELLATO: SIPO scarta anche il numero comunale. Dopo la firma dell'ufficiale si interviene solo con una rettifica o un'annotazione.");
  const fasi = [
    ["Prima di VALIDA", "Si modifica liberamente", ["Dati e documenti si correggono in SIPO come oggi", "Nessun dato è ancora in ANSC"], C.background2, C.accent1],
    ["Dopo VALIDA", "Si torna ai dati", ["SIPO rifà la validazione dello stesso atto", "Dopo le firme dei dichiaranti: solo se tutti possono firmare di nuovo", "Se cambia il caso d'uso: atto nuovo"], C.background2, C.accent1],
    ["Prima della firma USC", "Si può cancellare", ["ELIMINA EVENTO → CANCELLATO", "Il numero comunale viene scartato", "SIPO verifica l'esito in ANSC"], C.background2, C.accent1],
    ["Dopo la firma USC", "L'atto è formato", ["Solo rettifica o annotazione", "La nota tecnica si fa sulla web app (parte 5)"], C.accent1, C.background1],
  ];
  fasi.forEach(([k, t, v, f, c], i) => {
    const x = M + i * 3.1, w = 2.85;
    scheda(s, x, 1.95, w, 4.75, { fill: f });
    testo(s, k.toUpperCase(), { x: x + 0.3, y: 2.15, w: w - 0.5, h: 0.35, fontSize: 12, bold: true, color: i === 3 ? C.accent2 : C.accent3 });
    testo(s, t, { x: x + 0.3, y: 2.5, w: w - 0.5, h: 0.8, fontSize: 19, bold: true, fontFace: THEME.headFontFace, color: c });
    elenco(s, v, { x: x + 0.3, y: 3.4, w: w - 0.5, h: 3.2, fontSize: 14, color: i === 3 ? C.background1 : C.text1 });
  });
}

// ================================================================ 15 notifiche e supervisione
{
  const s = contenuto(3, "Notifiche da confermare ed eccezioni da seguire",
    "Notifiche: quando un altro Comune forma un atto che riguarda un atto di Roma, ANSC invia una notifica. Confermarla è un atto dell'ufficiale: collega l'annotazione e sblocca la comunicazione all'anagrafe, che non parte finché tutti i Comuni coinvolti non hanno confermato; un solo rifiuto la blocca. La conferma è una per notifica. Eccezioni: il back-office mostra gli atti che non hanno concluso il percorso, raggruppati per motivo, con le azioni possibili per ciascuno.");
  scheda(s, M, 1.95, 5.85, 2.3);
  testo(s, "Le notifiche in ingresso", { x: M + 0.3, y: 2.1, w: 5.2, h: 0.4, fontSize: 18, bold: true, fontFace: THEME.headFontFace, color: C.accent1 });
  elenco(s, [
    "Si confermano dal back-office, una alla volta",
    "La conferma sblocca la comunicazione all'anagrafe",
    "Un solo rifiuto e l'atto non ha effetti anagrafici",
  ], { x: M + 0.3, y: 2.6, w: 5.3, h: 1.6, fontSize: 14 });
  scheda(s, M, 4.4, 5.85, 2.3);
  testo(s, "Gli atti da riprendere", { x: M + 0.3, y: 4.55, w: 5.2, h: 0.4, fontSize: 18, bold: true, fontFace: THEME.headFontFace, color: C.accent1 });
  elenco(s, [
    "Atti interrotti a metà percorso",
    "Esito di ANSC da accertare",
    "Validazione rifiutata, firma non riuscita",
  ], { x: M + 0.3, y: 5.05, w: 5.3, h: 1.6, fontSize: 14 });
  segnaposto(s, 6.75, 1.95, 5.98, 4.75, "Back-office ANSC: elenco degli atti in eccezione con categoria, stato ANSC e azioni disponibili");
}

// ================================================================ 16 numerazione: regole
{
  pres.addSection({ title: SEZ[3] });
  const s = contenuto(4, "Il numero dell'atto lo assegna il Comune",
    "ANSC non assegna il numero comunale: lo deve indicare il Comune nell'atto. A Roma lo assegna un servizio dedicato, unico per tutti gli operatori, che evita doppioni quando molti uffici lavorano insieme. La serie è una per anno e riparte da 1 con il primo atto dell'anno; il numero è di sei cifre (la lunghezza massima ammessa da ANSC è in verifica con Sogei). Il numero si assegna all'Anteprima, prima della validazione. Se l'operazione fallisce il numero non viene consumato.");
  [["1", "serie per anno", "riparte da 1 a gennaio, senza registri separati"], ["6", "cifre", "fino a 999.999 atti l'anno"], ["0", "numeri persi per un errore", "un'operazione fallita non consuma il numero"]].forEach(([n, l, d], i) => {
    const x = M + i * 4.13, w = 3.83;
    scheda(s, x, 1.95, w, 2.65);
    testo(s, n, { x: x + 0.35, y: 2.05, w: w - 0.7, h: 1.25, fontSize: 66, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
    testo(s, l, { x: x + 0.35, y: 3.3, w: w - 0.7, h: 0.45, fontSize: 18, bold: true });
    testo(s, d, { x: x + 0.35, y: 3.78, w: w - 0.7, h: 0.75, fontSize: 14, color: C.accent3 });
  });
  testo(s, "Quando si assegna", { x: M, y: 4.95, w: 6, h: 0.4, fontSize: 18, bold: true, fontFace: THEME.headFontFace, color: C.accent1 });
  const p = ["Riepilogo", "Anteprima: numero assegnato", "VALIDA", "Firme"];
  p.forEach((t, i) => {
    const x = M + i * 3.1;
    chip(s, x, 5.5, 2.7, 0.65, t, { fill: i === 1 ? C.accent1 : C.background2, color: i === 1 ? C.background1 : C.accent1, line: C.accent6, fontSize: 14 });
    if (i < 3) freccia(s, x + 2.72, 5.82, x + 3.08, 5.82, { color: C.accent3 });
  });
  testo(s, "Un servizio unico per tutti gli uffici: nessun doppione anche con molti operatori al lavoro.", { x: M, y: 6.3, w: 12, h: 0.4, fontSize: 13, italic: true, color: C.accent3 });
}

// ================================================================ 17 numerazione: ciclo
{
  const s = contenuto(4, "La vita di un numero comunale",
    "Il numero richiesto è Disponibile; diventa Utilizzato quando l'atto lo porta in ANSC; passa a Evento acquisito quando l'atto è stato formato. Se l'atto viene cancellato il numero si scarta e resta visibile come buco nella serie, con il motivo. Per il parto plurimo si richiedono più numeri insieme, uno per gemello. Dal back-office, nelle pagine Richiesta e Ricerca, si consultano i numeri assegnati e le serie dell'anno.");
  const st = [["1", "Disponibile", "richiesto, non ancora usato"], ["2", "Utilizzato", "portato dall'atto in ANSC"], ["4", "Evento acquisito", "l'atto è formato"]];
  st.forEach(([n, t, d], i) => {
    const y = 2.0 + i * 1.25;
    cerchio(s, M, y, 0.75, n, { fill: i === 2 ? C.accent4 : C.accent1 });
    testo(s, t, { x: M + 1.0, y: y + 0.02, w: 3.6, h: 0.4, fontSize: 18, bold: true });
    testo(s, d, { x: M + 1.0, y: y + 0.42, w: 3.6, h: 0.35, fontSize: 14, color: C.accent3 });
    if (i < 2) freccia(s, M + 0.375, y + 0.8, M + 0.375, y + 1.2, { color: C.accent3 });
  });
  cerchio(s, M + 3.3, 3.25, 0.75, "3", { fill: C.accent3 });
  testo(s, "Scartato", { x: M + 4.25, y: 3.27, w: 2.2, h: 0.4, fontSize: 18, bold: true });
  testo(s, "atto cancellato: il buco resta visibile", { x: M + 4.25, y: 3.67, w: 2.2, h: 0.75, fontSize: 13, color: C.accent3 });
  freccia(s, M + 0.8, 2.6, M + 3.25, 3.5, { color: C.accent3, dash: "dash", width: 1.5 });
  scheda(s, M, 5.85, 6.3, 0.85, { fill: C.background2 });
  testo(s, "Parto plurimo: si richiedono più numeri insieme, uno per ciascun gemello.", { x: M + 0.25, y: 5.95, w: 5.9, h: 0.65, fontSize: 14, bold: true, color: C.accent1, valign: "middle" });
  segnaposto(s, 7.25, 1.95, 5.48, 4.75, "Back-office: pagine «Numerazione comunale — richiesta» e «— ricerca», con le serie dell'anno e i buchi");
}

// ================================================================ 18 web app: cosa resta
{
  pres.addSection({ title: SEZ[4] });
  const s = contenuto(5, "Che cosa resta sulla web app ANSC",
    "Anche lavorando in SIPO, sei funzioni restano sulla web app nazionale, accessibile a tutti gli ufficiali che formano atti. Tre di queste, codice OTP, nota tecnica e annullamento per inefficacia, cambiano lo stato o il contenuto di un atto senza passare da SIPO: per questo serve il riallineamento della slide successiva. L'annullamento per inefficacia è oggi disabilitato da ANSC (rilascio 1.52.0, giugno 2026).");
  const f = [
    ["Codice OTP di sessione", "Si genera all'inizio del lavoro e vale 4 ore", true],
    ["Nota tecnica", "Corregge un errore materiale su un atto formato", true],
    ["Annullamento per inefficacia", "Oggi disabilitato da ANSC", true],
    ["Certificati", "Emissione dei certificati non disponibili in SIPO", false],
    ["Allegati errati", "Gestione dei documenti segnalati come errati", false],
    ["Avvisi di sistema", "Comunicazioni di ANSC: nuove versioni e fermi", false],
  ];
  f.forEach(([t, d, tocca], i) => {
    const col = i % 3, riga = Math.floor(i / 3);
    const x = M + col * 4.13, y = 1.95 + riga * 2.2, w = 3.83;
    scheda(s, x, y, w, 1.95, { fill: tocca ? C.accent1 : C.background2 });
    cerchio(s, x + 0.3, y + 0.3, 0.6, i + 1, { fill: tocca ? C.accent2 : C.accent1, color: tocca ? C.text1 : C.background1, fontSize: 15 });
    testo(s, t, { x: x + 1.1, y: y + 0.3, w: w - 1.3, h: 0.65, fontSize: 16, bold: true, color: tocca ? C.background1 : C.accent1, valign: "middle" });
    testo(s, d, { x: x + 0.3, y: y + 1.05, w: w - 0.6, h: 0.8, fontSize: 14, color: tocca ? C.background1 : C.text1 });
  });
  testo(s, "In bordeaux: le funzioni che cambiano un atto senza passare da SIPO.", { x: M, y: 6.4, w: 12, h: 0.35, fontSize: 13, italic: true, color: C.accent3 });
}

// ================================================================ 19 due procedure
{
  const s = contenuto(5, "Due procedure da conoscere sulla web app",
    "Codice OTP: si genera sulla web app OTP di ANSC con smart card o SPID dalla propria postazione e si inserisce in SIPO quando lo chiede; se scade o viene invalidato si rigenera. Nota tecnica: si apre sulla web app per l'atto da correggere; subito dopo, dal back-office di SIPO, si riallinea l'atto: SIPO rilegge lo stato in ANSC. Se si salta questo passo, SIPO non sa della correzione.");
  const proc = (x, titolo, passi, foto) => {
    testo(s, titolo, { x, y: 1.9, w: 5.9, h: 0.45, fontSize: 19, bold: true, fontFace: THEME.headFontFace, color: C.accent1 });
    passi.forEach((p, i) => {
      const y = 2.45 + i * 0.6;
      cerchio(s, x, y, 0.45, i + 1, { fontSize: 13 });
      testo(s, p, { x: x + 0.6, y: y + 0.02, w: 5.3, h: 0.5, fontSize: 14, valign: "middle" });
    });
    segnaposto(s, x, 4.95, 5.85, 1.75, foto);
  };
  proc(M, "Generare il codice OTP", [
    "Accedere alla web app OTP di ANSC con smart card o SPID",
    "Generare il codice di sessione",
    "Inserirlo in SIPO alla prima richiesta",
    "Scaduto o invalidato? Generarne uno nuovo",
  ], "Web app OTP di ANSC e finestra di SIPO per l'inserimento del codice");
  proc(W - M - 5.85, "Nota tecnica e riallineamento", [
    "Aprire l'atto formato sulla web app ANSC",
    "Compilare e confermare la nota tecnica",
    "Subito dopo, in SIPO: back-office › Riallinea atto",
    "Controllare che lo stato in SIPO sia aggiornato",
  ], "Web app ANSC: nota tecnica · Back-office SIPO: riallineamento dell'atto");
}

// ================================================================ 20 chiusura
{
  pres.addSection({ title: "Chiusura" });
  const s = pres.addSlide({ masterName: "CHIUSURA", sectionTitle: "Chiusura" });
  s.addText("Cinque regole da portare allo sportello", { placeholder: "title" });
  const r = [
    ["Si lavora in SIPO", "ANSC si raggiunge dalle pagine nuove: validazione, firme, chiusura"],
    ["Cercare sempre l'intestatario in ANSC", "Senza la ricerca gli automatismi nazionali non scattano"],
    ["Prima di firmare, controllare l'anteprima", "Dopo la firma dell'ufficiale l'atto non si modifica più"],
    ["Il numero comunale lo assegna SIPO", "All'Anteprima: non si scrive a mano"],
    ["Dopo la web app, riallineare SIPO", "Nota tecnica e altre operazioni esterne vanno riportate subito"],
  ];
  r.forEach(([t, d], i) => {
    const y = 1.75 + i * 0.95;
    cerchio(s, M, y, 0.65, i + 1, { fill: C.accent2, color: C.text1 });
    testo(s, t, { x: M + 0.95, y: y - 0.02, w: 7.0, h: 0.42, fontSize: 19, bold: true, color: C.background1 });
    testo(s, d, { x: M + 0.95, y: y + 0.4, w: 7.0, h: 0.38, fontSize: 14, color: C.accent6 });
  });
  scheda(s, 9.0, 1.75, 3.73, 4.55, { fill: HEX.dk2, line: C.accent2 });
  testo(s, "Domande?", { x: 9.3, y: 2.0, w: 3.2, h: 0.7, fontSize: 30, bold: true, fontFace: THEME.headFontFace, color: C.accent2 });
  testo(s, "Assistenza applicativa", { x: 9.3, y: 2.9, w: 3.2, h: 0.4, fontSize: 15, bold: true, color: C.background1 });
  testo(s, "[DA COMPLETARE: recapito dell'assistenza di Sistemi Informativi]", { x: 9.3, y: 3.35, w: 3.2, h: 1.2, fontSize: 13, italic: true, color: C.accent6 });
  testo(s, "Materiale del corso a cura di Sistemi Informativi per Roma Capitale.", { x: 9.3, y: 5.0, w: 3.2, h: 1.0, fontSize: 13, color: C.accent6 });
  s.addNotes("Riepilogare le cinque regole e aprire alle domande. Il recapito dell'assistenza va completato prima della consegna del materiale.");
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");
  await applyTheme(OUT, THEME);
  console.log("scritto", OUT);
})();
