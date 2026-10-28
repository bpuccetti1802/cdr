# -*- coding: utf-8 -*-
"""I diagrammi a stati delle pagine nuove del workflow SIPO-ANSC.

Documento: WORKFLOW_Interfacce-SIPO-ANSC (dalla v0.2, 21/10/2026). Cinque figure: il
comportamento comune alle quattro pagine nuove (sessione, esiti da accertare, interruzione e
ripresa, eliminazione dell'evento) e un diagramma per ciascuna pagina — Validazione, Firme
dei dichiaranti, Conformità, Firma dell'USC.

Gli stati sono quelli DELLA PAGINA, non dell'atto: il diagramma dell'atto (coppia stato SIPO ·
stato ANSC) è diagrammi_workflow_stati.py. Ogni passaggio ha la sua fonte, dichiarata nella
tabella delle transizioni che accompagna la figura nel documento:
  · contratti ANSC R006, R007, R009, R010, R012, R014 e «Codici d'errore.xlsx» (ansc/docs/openapi);
  · il documento di Milano sull'attestato di conformità (Sorgenti Documentali, CdMI SIDe…) per
    le regole di abilitazione dei pulsanti della conformità;
  · le schermate di Side del capitolo 13.1 dell'analisi;
  · la decisione dell'utente (21/10/2026): dopo le firme dei dichiaranti si torna ai dati solo
    se tutti i firmatari sono in condizione di firmare di nuovo, altrimenti è inibito.

    /Library/Developer/CommandLineTools/usr/bin/python3 diagrammi_pagine_wf.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import diagrammi_comune as G   # noqa: E402

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
ROSSO, VERDE, VIOLA = '#b03a48', '#3f8f5f', '#7b5aa6'


class Diagramma:
    """Stati come riquadri, passaggi come percorsi fra lati dei riquadri."""

    def __init__(self, w, h, titolo, sotto):
        self.im, self.dr = G.tela(w, h, titolo, sotto)
        self.w, self.h = w, h
        self.s = {}

    def stato(self, k, x, y, w, h, colore, titolo, sotto=None, ts=19, ss=15):
        self.s[k] = (x, y, w, h)
        G.box(self.dr, x, y, w, h, colore, titolo, sotto, ts=ts, ss=ss)

    def uscita(self, k, x, y, w, testo):
        """Pagina o esito fuori dalla pagina: riquadro grigio a bordo tratteggiato."""
        h = 56
        self.s[k] = (x, y, w, h)
        bordo, fondo = G.C['grigio']
        self.dr.rounded_rectangle([x, y, x + w, y + h], radius=28, fill='white',
                                  outline=bordo, width=2)
        f = G.fnt(G.F_BLD, 16)
        righe = G.avvolgi(self.dr, testo, f, w - 30)
        cy = y + (h - 21 * len(righe)) / 2
        for r in righe:
            G.centra(self.dr, r, f, x + w / 2, cy, G.INK)
            cy += 21

    def iniziale(self, x, y):
        self.dr.ellipse([x - 11, y - 11, x + 11, y + 11], fill=G.INK)
        return (x, y)

    def p(self, k, lato, q=0.5):
        x, y, w, h = self.s[k]
        return {'n': (x + w * q, y), 's': (x + w * q, y + h), 'o': (x, y + h * q),
                'e': (x + w, y + h * q)}[lato]

    def passo(self, punti, colore=G.ARROW, tratteggio=False):
        pts = [self.p(*q) if isinstance(q[0], str) else q for q in punti]
        G.percorso(self.dr, pts, colore, tratteggio)

    def etichetta(self, testo, x, y, colore=G.ARROW, ts=15, fondo=True):
        f = G.fnt(G.F_REG, ts)
        righe = testo.split('\n')
        if fondo:
            larg = max(G.larghezza(self.dr, r, f) for r in righe)
            self.dr.rectangle([x - 4, y - 2, x + larg + 4, y + len(righe) * (ts + 4)],
                              fill='white')
        for i, r in enumerate(righe):
            self.dr.text((x, y + i * (ts + 4)), r, font=f, fill=colore)

    def nota(self, testo, y, ts=15):
        f = G.fnt(G.F_ITA, ts)
        for i, r in enumerate(G.avvolgi(self.dr, testo, f, self.w - 120)):
            self.dr.text((60, y + i * (ts + 5)), r, font=f, fill=G.MUTED)

    def legenda(self, y):
        G.legenda(self.dr, 60, y, [('blu', 'lavoro sulla pagina'),
                                   ('giallo', 'in attesa di ANSC o di SIPO'),
                                   ('verde', 'esito che fa avanzare'),
                                   ('rosso', 'esito negativo o eccezione'),
                                   ('viola', 'stati locali')], ss=15)

    def salva(self, nome):
        dest = os.path.join(IMG, nome)
        self.im.save(dest)
        return dest


# ----------------------------------------------------------------------------- comune
def comune():
    d = Diagramma(1700, 1000, "Il comportamento comune delle pagine nuove",
                  "vale in Validazione, Firme dei dichiaranti, Conformità e Firma dell’USC; "
                  "le figure seguenti lo danno per presupposto")
    d.stato('P', 640, 400, 420, 120, 'blu', "Pagina attiva",
            "una delle quattro pagine nuove, nel proprio stato interno")
    d.stato('S', 1240, 150, 400, 110, 'giallo', "Sessione da rinnovare",
            "ANSC rifiuta l’OTP di sessione: 406001 non valido, 406002 scaduto")
    d.stato('E', 1240, 560, 400, 120, 'rosso', "Esito da accertare",
            "nessuna risposta o errore 5xx su R009, R006, R012, R007, R014")
    d.uscita('N', 1270, 800, 340, "Stato successivo della pagina")
    d.stato('Sp', 60, 150, 400, 110, 'viola', "Interrotta",
            "nessun contrassegno: la riga resta all’ultimo salvataggio")
    d.stato('R', 60, 560, 400, 120, 'viola', "Ripresa",
            "dalla ricerca degli atti; OTP e credenziali di firma si chiedono di nuovo")
    d.uscita('A', 670, 820, 360, "Annullato: ANSC 3 (R011)")
    i = d.iniziale(850, 300)
    d.passo([(850, 311), ('P', 'n')])
    d.etichetta("ingresso: dal percorso o dalla ripresa", 596, 330)

    d.passo([('P', 'e', 0.25), (1150, 430), (1150, 230), ('S', 'o', 0.7)])
    d.etichetta("chiamata rifiutata\nper l’OTP", 1016, 250)
    d.passo([('S', 's', 0.5), (1440, 330), (1160, 330), (1160, 455), ('P', 'e', 0.45)], VERDE)
    d.etichetta("nuovo OTP consegnato:\nsi ripete l’azione", 1180, 372, VERDE)

    d.passo([('P', 'e', 0.75), (1150, 490), (1150, 600), ('E', 'o', 0.33)], ROSSO)
    d.etichetta("nessuna risposta", 1000, 540, ROSSO)
    d.passo([('E', 'n', 0.8), (1560, 472), ('P', 'e', 0.6)], G.ARROW)
    d.etichetta("R005: l’operazione non è avvenuta,\nsi può ripetere", 1300, 486)
    d.passo([('E', 's'), ('N', 'n')], VERDE)
    d.etichetta("R005: avvenuta", 1450, 730, VERDE)

    d.passo([('P', 'o', 0.3), (560, 436), (560, 205), ('Sp', 'e')], VIOLA)
    d.etichetta("INTERROMPI, fine della sessione\nSIPO, OTP non rinnovato", 480, 280, VIOLA)
    d.passo([('Sp', 's'), ('R', 'n')], VIOLA)
    d.etichetta("riapertura", 270, 400, VIOLA)
    d.passo([('R', 'e', 0.4), ('P', 'o', 0.75)], VERDE)
    d.etichetta("R005: lo stato reale è quello\nregistrato → COD_PAGINA_RIPRESA", 470, 545,
                VERDE)
    d.passo([('R', 's'), (260, 848), ('A', 'o')], G.MUTED, True)
    d.etichetta("R005: atto annullato o cambiato\nsulla web app → lo stato letto prevale",
                90, 740, G.MUTED)
    d.passo([('P', 's'), ('A', 'n')], ROSSO)
    d.etichetta("ELIMINA EVENTO confermato\n(con idAnsc, prima della firma USC)", 866, 690,
                ROSSO)
    d.legenda(930)
    return d.salva('wf_sd_comune.png')


# ------------------------------------------------------------------------- validazione
def validazione():
    d = Diagramma(1700, 1020, "Validazione: gli stati della pagina",
                  "R009 /validazione/evento; i tempi scaduti e l’OTP seguono il "
                  "comportamento comune")
    d.iniziale(40, 300)
    d.stato('V0', 90, 150, 380, 100, 'blu', "Pronta da validare",
            "in ANSC nessun atto; modello evento e numero comunale presenti")
    d.stato('V1', 90, 350, 380, 100, 'viola', "Da rivalidare (stato 0)",
            "atto già confermato in ANSC, dati cambiati dopo la validazione")
    d.passo([(40, 289), (40, 200), ('V0', 'o')])
    d.passo([(40, 311), (40, 400), ('V1', 'o')])
    d.stato('V2', 640, 250, 400, 100, 'giallo', "Validazione in corso",
            "R009 /validazione/evento")
    d.stato('V3', 1230, 120, 420, 100, 'rosso', "Respinta",
            "400, 404, 416: errori elencati per pagina; in ANSC nulla")
    d.stato('V4', 1230, 330, 420, 110, 'rosso', "Forzabile",
            "anomalie superabili e codice di forzatura concesso da ANSC")
    d.stato('V5', 640, 560, 400, 120, 'verde', "Validata",
            "ANSC 2 CONFERMATO: idAnsc e identificativi dei soggetti salvati")
    d.uscita('XD', 1230, 600, 420, "Pagine dei dati: Dettaglio, Riepilogo, Anteprima")
    d.uscita('XF', 330, 840, 380, "Firme dei dichiaranti")
    d.uscita('XC', 970, 840, 380, "Conformità")

    d.passo([('V0', 'e'), ('V2', 'o', 0.3)], VERDE)
    d.etichetta("VALIDA", 520, 238, VERDE)
    d.passo([('V1', 'e'), (560, 400), (560, 320), ('V2', 'o', 0.7)], VERDE)
    d.etichetta("VALIDA, riferita all’atto\nesistente: numero comunale\ne idAnsc", 480, 420,
                VERDE)
    d.passo([('V2', 'n', 0.7), (920, 170), ('V3', 'o')], ROSSO)
    d.etichetta("400, 404, 416", 960, 146, ROSSO)
    d.passo([('V2', 'e', 0.7), (1135, 320), (1135, 385), ('V4', 'o')], ROSSO)
    d.etichetta("errori con\nforcingCode", 1080, 400, ROSSO)
    d.passo([('V2', 's'), ('V5', 'n')], VERDE)
    d.etichetta("200: atto depositato", 856, 470, VERDE)
    d.passo([('V3', 'e', 0.5), (1680, 170), (1680, 628), ('XD', 'e')], ROSSO)
    d.etichetta("VAI ALLA PAGINA\no INDIETRO:\nsi corregge", 1515, 232, ROSSO)
    d.passo([('V4', 's', 0.3), ('XD', 'n', 0.3)], G.ARROW)
    d.etichetta("si corregge invece\ndi forzare", 1250, 500)
    d.passo([('V4', 'n', 0.15), (1293, 290), (1000, 290), (1000, 250)], G.ARROW)
    d.etichetta("conferma dell’USC e\nVALIDA CON FORZATURA", 1060, 250, G.ARROW)
    d.passo([('V5', 'e', 0.7), ('XD', 'o', 0.7)], VIOLA, True)
    d.etichetta("INDIETRO e modifica\ndei dati → stato 0", 1060, 660, VIOLA)
    d.passo([('V5', 's', 0.25), (740, 760), (520, 760), ('XF', 'n')], VERDE)
    d.etichetta("AVANTI [ci sono firmatari]", 450, 730, VERDE)
    d.passo([('V5', 's', 0.75), (940, 760), (1160, 760), ('XC', 'n')], VERDE)
    d.etichetta("AVANTI [nessun firmatario]", 1000, 730, VERDE)
    d.legenda(950)
    return d.salva('wf_sd_validazione.png')


# ------------------------------------------------------------------- firme dichiaranti
def firme():
    d = Diagramma(1700, 1330, "Firme dei dichiaranti: gli stati della pagina",
                  "in alto l’atto, in basso ciascun firmatario; R006 firma autografa, R012 "
                  "firma digitale")
    d.iniziale(40, 230)
    d.stato('F0', 90, 180, 360, 100, 'blu', "Firme da raccogliere",
            "ANSC 2; firmatari e modalità dal riepilogo")
    d.passo([(51, 230), ('F0', 'o')])
    d.stato('F1', 640, 180, 380, 100, 'giallo', "Firme in corso",
            "almeno un documento caricato o un link inviato")
    d.stato('F2', 1230, 180, 400, 100, 'verde', "Firmato dai dichiaranti",
            "ANSC 4 FIRMATO DAL DICHIARANTE: AVANTI abilitato")
    d.stato('F3', 640, 440, 380, 110, 'viola', "Dati riaperti",
            "stato 0, firme azzerate; dopo la nuova validazione si firma di nuovo")
    d.uscita('XV', 90, 380, 360, "Validazione (INDIETRO)")
    d.uscita('XD', 90, 600, 360, "Pagine dei dati")
    d.uscita('XA', 1230, 470, 400, "Annullato (R011) e atto nuovo")
    d.uscita('XC', 1230, 640, 400, "Conformità")

    d.passo([('F0', 'e'), ('F1', 'o')])
    d.etichetta("CARICA (R006) o\nINVIA LINK (R012)", 470, 186)
    d.passo([('F1', 'e'), ('F2', 'o')], VERDE)
    d.etichetta("VERIFICA STATO EVENTO:\nANSC porta l’atto a 4", 1036, 186, VERDE)
    d.passo([('F1', 'n', 0.3), (754, 150), (906, 150), ('F1', 'n', 0.7)], ROSSO)
    d.etichetta("documento scartato, link scaduto (412001)\no annullato: si ripete", 700, 104,
                ROSSO)
    d.passo([('F0', 's', 0.5), ('XV', 'n')], G.ARROW, True)
    d.etichetta("INDIETRO: i dati restano validi", 280, 326, G.MUTED)
    d.passo([('F0', 's', 0.15), (144, 340), (60, 340), (60, 628), ('XD', 'o')], VIOLA)
    d.etichetta("TORNA ALLA COMPILAZIONE\n(nessuna firma acquisita)\n→ stato 0", 72, 470,
                VIOLA)
    d.passo([('F2', 's', 0.2), (1310, 400), (963, 400), ('F3', 'n', 0.85)], VIOLA)
    d.passo([('F1', 's', 0.5), ('F3', 'n', 0.5)], VIOLA)
    d.etichetta("TORNA ALLA COMPILAZIONE [tutti i firmatari\npossono firmare di nuovo, "
                "confermato\ndall’operatore firmatario per firmatario]", 840, 318, VIOLA)
    d.passo([('F3', 'o'), (560, 495), (560, 628), ('XD', 'e')], VIOLA)
    d.etichetta("si correggono i dati,\npoi nuova validazione", 470, 560, VIOLA)
    d.passo([('F2', 's', 0.5), ('XA', 'n')], ROSSO, True)
    d.etichetta("[non tutti possono firmare\ndi nuovo]: TORNA ALLA\nCOMPILAZIONE inibito,\n"
                "resta ELIMINA EVENTO", 1442, 306, ROSSO)
    d.passo([('F2', 'e', 0.8), (1665, 260), (1665, 668), ('XC', 'e')], VERDE)
    d.etichetta("AVANTI", 1595, 560, VERDE)

    # ciascun firmatario
    y0 = 760
    d.dr.rounded_rectangle([40, y0, 1660, 1230], radius=16, outline=G.C['grigio'][0], width=2)
    d.dr.text((60, y0 + 12), "Per ciascun firmatario (tabella firmatari: ty_firma, "
              "cd_stato_firma, id_presa_visione)", font=G.fnt(G.F_BLD, 17), fill=G.INK)
    ya, yb = y0 + 70, y0 + 260
    d.dr.text((60, ya + 34), "Autografa", font=G.fnt(G.F_BLD, 16), fill=G.MUTED)
    d.dr.text((60, yb + 34), "Digitale", font=G.fnt(G.F_BLD, 16), fill=G.MUTED)
    kw = dict(ts=16, ss=14)
    d.stato('a1', 170, ya, 260, 90, 'blu', "Da firmare", "anteprima stampata", **kw)
    d.stato('a2', 560, ya, 300, 90, 'giallo', "Documento in verifica",
            "R006; stato ANSC_08 in elaborazione", **kw)
    d.stato('a3', 1000, ya, 260, 90, 'verde', "Inserito", "firma acquisita", **kw)
    d.stato('a4', 1340, ya, 280, 90, 'rosso', "Scartato", "il documento va ricaricato", **kw)
    d.passo([('a1', 'e'), ('a2', 'o')])
    d.etichetta("CARICA", 462, ya + 20)
    d.passo([('a2', 'e'), ('a3', 'o')], VERDE)
    d.etichetta("VERIFICA", 890, ya + 20, VERDE)
    d.passo([('a2', 's', 0.7), (770, ya + 130), (1480, ya + 130), ('a4', 's')], ROSSO)
    d.etichetta("VERIFICA: scartato", 1040, ya + 108, ROSSO)
    d.passo([('a4', 'n'), (1480, ya - 20), (300, ya - 20), ('a1', 'n')], ROSSO, True)
    d.etichetta("si ricarica", 820, ya - 42, ROSSO)
    d.stato('d1', 170, yb, 260, 90, 'blu', "Link da inviare", "email del firmatario", **kw)
    d.stato('d2', 560, yb, 300, 90, 'giallo', "Da visionare",
            "R012 invio-email; presa visione 0", **kw)
    d.stato('d3', 1000, yb, 260, 90, 'verde', "Visionato e firmato", "presa visione 1", **kw)
    d.stato('d4', 1340, yb, 280, 90, 'rosso', "Annullato o scaduto",
            "presa visione 2, oppure 412001", **kw)
    d.passo([('d1', 'e'), ('d2', 'o')])
    d.etichetta("INVIA LINK", 448, yb + 20)
    d.passo([('d2', 'e'), ('d3', 'o')], VERDE)
    d.etichetta("AGGIORNA (pooling)", 866, yb + 20, VERDE)
    d.passo([('d2', 's', 0.7), (770, yb + 130), (1480, yb + 130), ('d4', 's')], ROSSO)
    d.etichetta("ANNULLA LINK o scadenza", 1010, yb + 108, ROSSO)
    d.passo([('d4', 'n'), (1480, yb - 20), (300, yb - 20), ('d1', 'n')], ROSSO, True)
    d.etichetta("INVIA DI NUOVO", 820, yb - 42, ROSSO)
    d.legenda(1262)
    return d.salva('wf_sd_firme.png')


# --------------------------------------------------------------------------- conformità
def conformita():
    d = Diagramma(1700, 1000, "Conformità: gli stati della pagina",
                  "regole di abilitazione dei pulsanti dal processo di Milano (Side, versione "
                  "ANSC 1.40); R010 genera l’attestazione, R007 la firma")
    d.iniziale(40, 300)
    d.stato('C1', 90, 250, 380, 110, 'blu', "Selezione degli allegati",
            "la prima volta preselezionati quelli da attestare; poi le scelte salvate")
    d.passo([(51, 300), ('C1', 'o', 0.45)])
    d.stato('C2', 90, 540, 380, 110, 'blu', "Nessun allegato selezionato",
            "GENERA disabilitato, CONTINUA abilitato")
    d.stato('C3', 640, 250, 400, 110, 'giallo', "Anteprima generata",
            "R010 /anteprima/attestazione; FIRMA abilitata, utenza precompilata")
    d.stato('C4', 1230, 250, 400, 110, 'giallo', "Firma in corso", "R007 /attestazione/firma")
    d.stato('C5', 1230, 540, 400, 110, 'verde', "Firmato per conformità",
            "ANSC 11 FIRMATO PER CONFORMITÀ")
    d.uscita('XU', 660, 820, 380, "Firma dell’USC")
    d.uscita('XD', 640, 560, 400, "Pagine dei dati")
    d.uscita('XS', 640, 110, 400, "Firma dell’USC, senza questa pagina")

    d.passo([(40, 289), (40, 138), ('XS', 'o', 0.5)], G.MUTED, True)
    d.etichetta("[l’atto non ha allegati da attestare]", 120, 70, G.MUTED)
    d.passo([('C1', 's', 0.35), ('C2', 'n', 0.35)])
    d.etichetta("deseleziona tutto", 110, 440)
    d.passo([('C2', 'n', 0.7), ('C1', 's', 0.7)])
    d.etichetta("seleziona un allegato", 300, 470)
    d.passo([('C1', 'e', 0.3), ('C3', 'o', 0.3)], VERDE)
    d.etichetta("GENERA\n(salva le scelte)", 486, 220, VERDE)
    d.passo([('C3', 'o', 0.75), ('C1', 'e', 0.75)])
    d.etichetta("cambia la selezione:\nl’anteprima decade", 486, 350)
    d.passo([('C3', 'e', 0.3), ('C4', 'o', 0.3)], VERDE)
    d.etichetta("FIRMA", 1110, 250, VERDE)
    d.passo([('C4', 'o', 0.75), ('C3', 'e', 0.75)], ROSSO)
    d.etichetta("406001, 406004:\nPIN da reinserire", 1070, 350, ROSSO)
    d.passo([('C4', 's'), ('C5', 'n')], VERDE)
    d.etichetta("esito positivo", 1450, 450, VERDE)
    d.passo([('C2', 's'), (280, 848), ('XU', 'o')], VERDE)
    d.etichetta("CONTINUA (salva le scelte)", 300, 800, VERDE)
    d.passo([('C5', 's'), (1430, 848), ('XU', 'e')], VERDE)
    d.etichetta("AVANTI", 1240, 800, VERDE)
    d.passo([('C1', 's', 0.92), (440, 588), ('XD', 'o')], VIOLA, True)
    d.etichetta("TORNA ALLA COMPILAZIONE\n[nessuna firma dei dichiaranti,\n"
                "o tutti possono rifirmare]", 460, 470, VIOLA)
    d.legenda(930)
    return d.salva('wf_sd_conformita.png')


# --------------------------------------------------------------------------- firma USC
def firma_usc():
    d = Diagramma(1700, 940, "Firma dell’USC: gli stati della pagina",
                  "CHIUDI = R007 /firma_usc, poi R014 se richiesta la comunicazione anagrafica, "
                  "poi il salvataggio in SIPO")
    d.iniziale(40, 225)
    d.stato('U0', 90, 170, 380, 110, 'blu', "Pronta alla firma",
            "ANSC 11, oppure 4 o 2 se non c’era nulla da attestare")
    d.passo([(51, 225), ('U0', 'o')])
    d.stato('U1', 660, 170, 380, 110, 'giallo', "Firma in corso", "R007 /firma_usc")
    d.stato('U2', 1240, 170, 400, 110, 'verde', "Firmato dall’USC",
            "ANSC 5: l’atto è formato; INDIETRO ed ELIMINA EVENTO disabilitati")
    d.stato('U3', 1240, 450, 400, 100, 'giallo', "Data di validità",
            "R014 /evento/data-validita")
    d.stato('U4', 660, 450, 380, 110, 'giallo', "Salvataggio in SIPO",
            "/finalizzaAtto → InitFlow")
    d.stato('U5', 90, 720, 380, 100, 'verde', "Chiuso", "SIPO 2 DEFINITO")
    d.stato('U6', 660, 720, 380, 110, 'rosso', "Chiuso, sospeso in SIPO",
            "SIPO 3: aggiornamento anagrafico non riuscito o in attesa")
    d.stato('U7', 90, 450, 380, 110, 'rosso', "Formato in ANSC, non in SIPO",
            "eccezione: si ripete il salvataggio, mai la firma")

    d.passo([('U0', 'n', 0.3), (204, 130), (356, 130), ('U0', 'n', 0.7)])
    d.etichetta("ANTEPRIMA DELL’ATTO (R010)", 150, 92)
    d.passo([('U0', 'e', 0.3), ('U1', 'o', 0.3)], VERDE)
    d.etichetta("CHIUDI", 530, 170, VERDE)
    d.passo([('U1', 'o', 0.75), ('U0', 'e', 0.75)], ROSSO)
    d.etichetta("406001, 406002,\n406004", 500, 270, ROSSO)
    d.passo([('U1', 'e', 0.5), ('U2', 'o', 0.5)], VERDE)
    d.etichetta("esito\npositivo", 1078, 178, VERDE)
    G.linea(d.dr, [(1140, 120), (1140, 360)], ROSSO, True, 3)
    d.dr.text((1150, 330), "punto di non ritorno", font=G.fnt(G.F_BLD, 15), fill=ROSSO)
    d.passo([('U2', 's'), ('U3', 'n')], G.ARROW)
    d.etichetta("[comunicazione\nanagrafica]", 1450, 370)
    d.passo([('U2', 's', 0.15), (1300, 400), (850, 400), ('U4', 'n')], G.ARROW)
    d.etichetta("[senza comunicazione anagrafica]", 880, 372)
    d.passo([('U3', 'o'), ('U4', 'e', 0.45)], G.ARROW)
    d.etichetta("esito positivo, o negativo\nsegnalato al back-office", 1046, 560)
    d.passo([('U4', 's', 0.2), (736, 640), (280, 640), ('U5', 'n')], VERDE)
    d.etichetta("SIPO 2", 480, 612, VERDE)
    d.passo([('U4', 's', 0.7), ('U6', 'n', 0.7)], ROSSO)
    d.etichetta("SIPO 3", 940, 650, ROSSO)
    d.passo([('U4', 'o', 0.35), ('U7', 'e', 0.35)], ROSSO)
    d.etichetta("errore", 530, 456, ROSSO)
    d.passo([('U7', 'e', 0.75), ('U4', 'o', 0.75)], VERDE)
    d.etichetta("RIPROVA", 530, 540, VERDE)
    d.passo([('U6', 'o', 0.5), ('U5', 'e', 0.55)], VERDE)
    d.etichetta("/annullaSospensioneAtto", 476, 740, VERDE)
    d.legenda(880)
    return d.salva('wf_sd_firma_usc.png')


DIAGRAMMI = (comune, validazione, firme, conformita, firma_usc)


def disegna_tutti():
    return [fn() for fn in DIAGRAMMI]


if __name__ == '__main__':
    for p in disegna_tutti():
        print('scritto:', p)
