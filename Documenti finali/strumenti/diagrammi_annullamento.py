# -*- coding: utf-8 -*-
"""Figura della mappa «azione di SIPO × stato dell'atto in ANSC» per il documento
ANALISI_Annullamento-Cancellazione-Rettifiche_SIPO-ANSC.

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/diagrammi_annullamento.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import diagrammi_comune as G   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(QUI, 'img', 'annullamento')

COLONNE = [
    ("Atto non in ANSC", "nessuna riga su ANSC_STATO_ATTO, oppure riga senza idAnsc"),
    ("In ANSC, prima della firma USC", "idAnsc presente · stati 1, 2, 4, 11"),
    ("In ANSC, firmato dall'USC", "stato 5 FIRMATO DA USC · l'atto è formato"),
]

RIGHE = [
    ("CANCELLA PRATICA", "pagina di ricerca dell'area · pratica 1 IN LAVORAZIONE",
     [("verde", "Come oggi", "pkg_pratica.annullaPRATICA; stato 9 locale se la riga esiste"),
      ("viola", "R011 /evento/elimina", "a esito positivo stato 9 CANCELLATO, poi annullaPRATICA; a errore la pratica resta"),
      ("rosso", "Non ammessa", "SIPO 1 con ANSC 5 è un disallineamento: si legge lo stato con R005")]),
    ("ANNULLA ATTO", "dettaglio dell'atto · pratica 2 DEFINITO o 3 SOSPESO",
     [("verde", "Come oggi", "pkg_pratica.annullaATTO e annullamento dell'operazione ANPR"),
      ("grigio", "Non si presenta", "nel percorso SIPO 2 DEFINITO coincide con la firma dell'USC"),
      ("giallo", "Annotazione per rettifica, tipo annullamento", "R013 con idTipoRettifica 0; oggi sulla web app, poi riallineamento in SIPO")]),
    ("RETTIFICA ATTO", "dettaglio dell'atto · entro le 23:59 del giorno della pratica",
     [("verde", "Come oggi", "l'atto torna 1 IN LAVORAZIONE con FLG_RETTIFICA_INCORSO"),
      ("blu", "Ritorno ai dati", "non è una rettifica: stato 0, nuova validazione dello stesso atto"),
      ("giallo", "L'atto non si riapre", "nota tecnica (web app) · errore materiale art. 98 · rettifica di modifica (R013)")]),
]


def mappa():
    W, H = 1900, 1060
    im, dr = G.tela(W, H, "Le tre azioni di SIPO e lo stato dell'atto in ANSC",
                    "che cosa accade a ciascuna azione secondo dove si trova l'atto · "
                    "la colonna decide lo strumento, non il pulsante")
    x0, y0 = 40, 110
    w_testa, w_cella, h_testa, h_riga, gap = 360, 470, 110, 215, 18
    for j, (tit, sot) in enumerate(COLONNE):
        x = x0 + w_testa + gap + j * (w_cella + gap)
        G.box(dr, x, y0, w_cella, h_testa, 'grigio', tit, sot, ts=21, ss=15)
    for i, (az, dove, celle) in enumerate(RIGHE):
        y = y0 + h_testa + gap + i * (h_riga + gap)
        G.box(dr, x0, y, w_testa, h_riga, 'blu', az, dove, ts=23, ss=16)
        for j, (col, tit, sot) in enumerate(celle):
            x = x0 + w_testa + gap + j * (w_cella + gap)
            G.box(dr, x, y, w_cella, h_riga, col, tit, sot, ts=21, ss=16)
    G.legenda(dr, 60, H - 45, [('blu', 'azione di SIPO'), ('verde', 'come oggi'),
                               ('viola', 'chiamata ad ANSC'),
                               ('giallo', 'strumento ANSC diverso dal pulsante'),
                               ('rosso', 'non ammessa'), ('grigio', 'caso che non si presenta')])
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, 'mappa_azioni.png')
    im.save(p)
    return p



# ---------------------------------------------------------------- nota tecnica (v0.2)
def nota_tecnica():
    """Il processo della nota tecnica sulla web app, dalla guida dei servizi di ausilio."""
    W, H = 1500, 1330
    im, dr = G.tela(W, H, "La correzione dell'atto tramite nota tecnica",
                    "solo web app ANSC · Altri servizi → Correzione evento tramite nota tecnica · "
                    "Guida servizi di ausilio § 3.5")
    x, w, h, gap = 330, 840, 120, 42
    passi = [
        ('grigio', "Atto firmato e chiuso con metadati errati",
         "malfunzionamento di ANSC o del gestionale, errore dell'ufficiale"),
        ('viola', "Evento da modificare: numero nazionale (idAnsc)",
         "ANSC verifica: atto del comune in sessione · stato 5 FIRMATO DA USC · "
         "nessuna annotazione modificativa successiva"),
        ('viola', "Motivo e testo della nota tecnica",
         "il motivo è obbligatorio dalla versione 1.27.5 · conferma della modifica"),
        ('viola', "Correzione dei dati dell'atto",
         "dati errati · sezioni obbligatorie mancanti · dati eccedenti · annotazioni contestuali"),
        ('viola', "Allegati e conclusione",
         "allegati e attestazione di conformità (1.27.0) · firma dell'ufficiale [DA VERIFICARE]"),
        ('verde', "Effetti in ANSC",
         "la nota si consulta come un'annotazione · certificati ed estratti con i dati corretti · "
         "conservazione · comunicazioni anagrafiche e notifiche rigenerate"),
    ]
    y = 110
    for i, (col, t, s) in enumerate(passi):
        G.box(dr, x, y, w, h, col, t, s, ts=22, ss=16)
        if i < len(passi) - 1:
            G.freccia(dr, (x + w / 2, y + h), (x + w / 2, y + h + gap))
        y += h + gap
    G.box(dr, 60, 1085, 1380, 170, 'giallo', "Che cosa le fonti non dicono",
          "se l'ufficiale firmi la nota con OTP · che cosa distingua NOTATECNICA (2) da "
          "NOTATECNICARETTIFICA (3) in ANSC_79 · come un gestionale venga a sapere che è stata "
          "fatta: nessuna notifica dedicata, solo la consultazione R005 per evento",
          ts=21, ss=17)
    G.legenda(dr, 60, H - 45, [('grigio', 'situazione'), ('viola', 'passo sulla web app'),
                               ('verde', 'esito'), ('giallo', 'lacune delle fonti')])
    p = os.path.join(OUT, 'nota_tecnica_webapp.png')
    im.save(p)
    return p


def rettifica_tecnica_sipo():
    """Il flusso proposto: avvio da SIPO, nota tecnica sulla web app, riallineamento in SIPO."""
    W, H = 1900, 1420
    im, dr = G.tela(W, H, "La rettifica tecnica di un atto firmato e chiuso: il flusso SIPO ↔ web app",
                    "l'atto non si riapre in SIPO · si corregge in ANSC con la nota tecnica · "
                    "SIPO legge il risultato e si riallinea")
    G.banda(dr, 30, 100, 930, H - 80, '#2f6db5', "SIPO", '#2f6db5')
    G.banda(dr, 970, 100, 1870, H - 80, '#7c5cae', "Web app ANSC", '#7c5cae')
    xl, xr, w, h = 90, 1030, 780, 130
    s = [
        (xl, 160, 'blu', "Dettaglio dell'atto: «RETTIFICA TECNICA»",
         "al posto di «RETTIFICA ATTO» per l'atto con idAnsc e stato 5"),
        (xl, 360, 'blu', "Pagina di avvio",
         "idAnsc e numero comunale in evidenza · istruzioni · COPIA IDANSC · "
         "nota sull'atto: rettifica tecnica in corso"),
        (xr, 360, 'viola', "Correzione evento tramite nota tecnica",
         "numero nazionale · motivo · testo della nota"),
        (xr, 560, 'viola', "Correzione dei dati e conclusione",
         "dati errati, mancanti, eccedenti · annotazioni contestuali · allegati"),
        (xr, 760, 'verde', "Atto corretto in ANSC",
         "nota tecnica fra le annotazioni · certificati con i dati corretti"),
        (xl, 760, 'blu', "«RIALLINEA DA ANSC»",
         "R005 note tecniche (idEvento) e R005 evento (idAnsc)"),
        (xl, 960, 'blu', "Confronto SIPO ↔ ANSC",
         "campo per campo, sulla configurazione dell'UC (ANSC_CFG_CAMPO) · "
         "differenze evidenziate · testo della nota tecnica"),
        (xl, 1160, 'verde', "Conferma e aggiornamento",
         "dati di SIPO aggiornati senza riaprire l'atto · stato resta 2 DEFINITO · "
         "traccia in ANSC_LOG_AUDIT"),
    ]
    for (x, y, col, t, ss) in s:
        G.box(dr, x, y, w, h, col, t, ss, ts=21, ss=16)
    c = w / 2
    G.freccia(dr, (xl + c, 290), (xl + c, 360))
    G.freccia(dr, (xl + w, 425), (xr, 425), etichetta="web app")
    G.freccia(dr, (xr + c, 490), (xr + c, 560))
    G.freccia(dr, (xr + c, 690), (xr + c, 760))
    G.freccia(dr, (xr, 825), (xl + w, 825), etichetta="rientro")
    G.freccia(dr, (xl + c, 890), (xl + c, 960))
    G.freccia(dr, (xl + c, 1090), (xl + c, 1160))
    G.box(dr, xr, 960, w, 330, 'giallo', "Indicazioni",
          "nessuna chiamata ad ANPR da SIPO: le comunicazioni anagrafiche le genera ANSC "
          "(1.43.0) · nessuna notifica avvisa SIPO: il riallineamento è un adempimento "
          "dell'ufficio, come per la riconciliazione · se R005 non mostra note tecniche "
          "nuove, nulla cambia in SIPO", ts=21, ss=17)
    G.legenda(dr, 60, H - 45, [('blu', 'pagina o passo di SIPO'), ('viola', 'web app ANSC'),
                               ('verde', 'esito'), ('giallo', 'indicazione')])
    p = os.path.join(OUT, 'rettifica_tecnica_flusso.png')
    im.save(p)
    return p


if __name__ == '__main__':
    print(mappa())
    print(nota_tecnica())
    print(rettifica_tecnica_sipo())
