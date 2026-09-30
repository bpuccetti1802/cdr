# -*- coding: utf-8 -*-
"""Diagramma «Dalla maschera SIPO al payload ANSC: la catena della configurazione».

Tre fasce: le fonti che ANSC pubblica, la configurazione che il Comune ne ricava, e
l'esecuzione che la usa quando l'operatore forma un atto.

⚠️ La fascia delle fonti NON è un elenco di file: dice **per quale canale** ciò che ANSC
pubblica entra nel nostro database. I canali sono due — l'importazione dei fogli Excel e il
comando R901 — e i CSV del repository non sono nessuno dei due: sono il riscontro. La prima
stesura di questa figura li mostrava come sorgenti, ed era sbagliata.

⚠️ Le frecce si disegnano **ortogonali**, in corsie orizzontali dentro i corridoi: in diagonale
attraversavano il titolo della fascia e i riquadri.

⚠️ L'ordine dei riquadri della configurazione segue il canale: a sinistra ciò che il Comune
scrive (nessuna freccia in entrata), al centro ciò che arriva dai fogli, a destra ciò che
arriva da R901. Così ogni freccia è corta e nessuna scende dove sta il titolo della fascia.

    /Library/Developer/CommandLineTools/usr/bin/python3 diagrammi_catena.py <cartella>
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diagrammi_comune import (  # noqa: E402
    F_BLD, F_ITA, F_REG, MUTED, banda, box, centra, fnt, legenda, linea, percorso, tela)

W, H = 1780, 1180
ROSSO, GIALLO, BLU, VERDE = '#8d2f3a', '#a8801a', '#25548a', '#2f6b47'

# ────────────────────────────────────── fascia 1: ciò che ANSC pubblica, e per quale canale
PUBBLICA = [
    ('Il contratto model_evento', 'la struttura del payload:\n90 schemi, 8.256 percorsi'),
    ('Il mapping dei casi d’uso', 'che cosa serve a ciascun UC:\ncampi, allegati, formule'),
    ('Il changelog del mapping', 'che cosa è cambiato\na ogni rilascio: 66 revisioni'),
]
P_LARGH, P_GAPP, P_YY = 390, 16, 126

DECODIFICHE = ('Le decodifiche di ANSC', 'i valori ammessi, e fra esse il catalogo\n'
               'degli UC (ANSC_03): 143 identificativi')

# i due canali: (x1, x2, colore, titolo, sottotitolo)
CANALI = [
    (60, 1262, '#d9a441', 'CANALE 1 · I FOGLI EXCEL',
     'il Comune prepara i tracciati, il back-office li importa: le righe nascono «proposte»'),
    (1300, 1720, '#7b5aa6', 'CANALE 2 · R901',
     'comando di allineamento, su richiesta'),
]
CANALE_Y = 290

# ───────────────────────────────────────────── fascia 2: la configurazione
CONF = [
    ('ANSC_CFG_UC', 'scritta dal Comune',
     'l’UC adottato, il Modello,\nla priorità, il codice della logica', 'verde'),
    ('TIPO_LOGICHE_DI_SCELTA e\nLOGICHE_DI_SCELTA', 'scritte dal Comune',
     'le logiche: scelta dell’UC,\nsezioni e campi', 'verde'),
    ('ANSC_CFG_SEZIONE', 'dai fogli', 'i blocchi richiesti\ne quando si popolano', 'verde'),
    ('ANSC_CFG_CAMPO', 'dai fogli',
     'campo ANSC ↔ colonna SIPO,\ndecodifica, obbligatorietà', 'verde'),
    ('ALLEGATI_USECASE\ne ANSC_CFG_FORMULA', 'dai fogli',
     'documenti e diciture\nrichiesti dall’UC', 'verde'),
    ('DOMINIO_DECODIFICA\ne VALORE_DOMINIO', 'da R901',
     'valori ammessi; si leggono\nper chiave: dominio + valore', 'giallo'),
    ('RICONCILIAZ_DIZIONARI', 'scritta dal Comune',
     'come un valore di SIPO\ndiventa un valore di ANSC', 'verde'),
    ('ANSC_ANA_UC', 'da R901, più il codice motore',
     'catalogo degli UC,\ncon il tipo evento', 'giallo'),
]
C_LARG, C_GAP, C_Y = 198, 10, 408

# quali riquadri della configurazione alimenta ciascun canale
ALIMENTA = [(0, [2, 3, 4]), (1, [5, 6])]   # il canale 2 non alimenta la riconciliazione

# ───────────────────────────────────────────────── fascia 3: l'esecuzione
PASSI = [
    ('L’atto in SIPO', 'già salvato sulle tabelle:\nè lì che si va a leggere',
     'CONF_TIPO_ATTI\ndà Modello e maschera', 'blu'),
    ('Determinazione\ndell’UC', 'la logica di ciascun UC,\nin ordine di priorità',
     'ANSC_CFG_UC\n+ VALORI_DOMINIO', 'blu'),
    ('Requisiti dell’UC', 'sezioni, campi, allegati\ne formule che servono',
     'ANSC_CFG_SEZIONE · _CAMPO\nALLEGATI_USECASE · _FORMULA', 'blu'),
    ('Prevalidazione\nlocale', 'mancanze segnalate prima\ndi consumare un idAnsc',
     'RF-9 · nessuna chiamata\nad ANSC', 'blu'),
    ('Costruzione\ndel payload', 'ogni CAMPO_SIPO nel suo percorso,\ncon la transcodifica '
     'dichiarata', 'model_evento\n(l’albero unico)', 'blu'),
    ('Validazione ANSC\ne deposito', 'R009: valida e deposita,\nrestituisce l’idAnsc',
     'e poi le firme:\nR006 · R007', 'verde'),
]
P_LARG, P_GAP, P_Y = 262, 22, 756


def riquadro(dr, x, y, larg, alt, titolo, sotto, fonte, colore):
    bordo, fondo = (('#d9a441', '#fdf1d6') if colore == 'giallo' else
                    ('#3f8f5f', '#dcefe1') if colore == 'verde' else
                    ('#2f6bb0', '#dbe6f5'))
    dr.rounded_rectangle([x, y, x + larg, y + alt], radius=10, fill=fondo, outline=bordo,
                         width=3)
    yy = y + 12
    for riga in titolo.split('\n'):
        centra(dr, riga, fnt(F_BLD, 16), x + larg / 2, yy, '#1f2937')
        yy += 20
    if sotto:
        yy += 2
        for riga in sotto.split('\n'):
            centra(dr, riga, fnt(F_ITA, 14), x + larg / 2, yy, bordo)
            yy += 19
        yy += 5
    for riga in fonte.split('\n'):
        centra(dr, riga, fnt(F_REG, 14), x + larg / 2, yy, MUTED)
        yy += 18
    return x + larg / 2


def figura(dest):
    im, dr = tela(W, H, 'Dalla maschera SIPO al payload ANSC: la catena della configurazione',
                  'Ogni riga di configurazione ha una fonte dichiarata; ogni passo '
                  'dell’esecuzione ha una tabella che lo guida')

    # ---------------- 1 · ciò che ANSC pubblica
    banda(dr, 40, 86, W - 40, 356, '#b03a48',
          '1 · LE FONTI E I CANALI — che cosa pubblica ANSC, e per quale via entra nel '
          'database', ROSSO)
    centri_pub = []
    for i, (t, s_) in enumerate(PUBBLICA):
        x = 60 + i * (P_LARGH + P_GAPP)
        dr.rounded_rectangle([x, P_YY, x + P_LARGH, 246], radius=10, fill='#f6dfe1',
                             outline='#b03a48', width=3)
        yy = P_YY + 14
        for riga in t.split('\n'):
            centra(dr, riga, fnt(F_BLD, 17), x + P_LARGH / 2, yy, '#1f2937')
            yy += 22
        yy += 6
        for riga in s_.split('\n'):
            centra(dr, riga, fnt(F_REG, 15), x + P_LARGH / 2, yy, MUTED)
            yy += 19
        centri_pub.append(x + P_LARGH / 2)

    dr.rounded_rectangle([1300, P_YY, 1720, 246], radius=10, fill='#f6dfe1',
                         outline='#b03a48', width=3)
    centra(dr, DECODIFICHE[0], fnt(F_BLD, 17), 1510, P_YY + 14, '#1f2937')
    for k, riga in enumerate(DECODIFICHE[1].split('\n')):
        centra(dr, riga, fnt(F_REG, 15), 1510, P_YY + 58 + k * 19, MUTED)

    # i due canali
    centri_canali = []
    for x1, x2, colore, titolo, sotto in CANALI:
        dr.rounded_rectangle([x1, CANALE_Y, x2, CANALE_Y + 52], radius=10, fill='white',
                             outline=colore, width=3)
        centra(dr, titolo, fnt(F_BLD, 16), (x1 + x2) / 2, CANALE_Y + 6, colore)
        centra(dr, sotto, fnt(F_ITA, 14), (x1 + x2) / 2, CANALE_Y + 28, MUTED)
        centri_canali.append((x1 + x2) / 2)
    for x in centri_pub:
        percorso(dr, [(x, 248), (x, CANALE_Y - 2)], ROSSO, True, 2)
    percorso(dr, [(1510, 248), (1510, CANALE_Y - 2)], ROSSO, True, 2)

    # ---------------- 2 · la configurazione
    banda(dr, 40, 376, W - 40, 700, '#d9a441',
          '2 · LA CONFIGURAZIONE — la baseline versionata, in ANSC_USR', GIALLO)
    centri_conf = []
    for i, (t, f, n, col) in enumerate(CONF):
        x = 60 + i * (C_LARG + C_GAP)
        centri_conf.append(riquadro(dr, x, C_Y, C_LARG, 148, t, f, n, col))

    for i_canale, destinazioni in ALIMENTA:
        for d in destinazioni:
            xd = centri_conf[d]
            percorso(dr, [(xd, CANALE_Y + 54), (xd, C_Y - 2)],
                     CANALI[i_canale][2], True, 2)

    y = 580
    dr.text((60, y), 'La configurazione la decidono i funzionari: l’importazione prepara le '
                     'righe in stato «proposto», l’operatore le esamina, conferma o corregge.',
            font=fnt(F_BLD, 16), fill=GIALLO)
    for i, t in enumerate([
        'Ogni riga dichiara la propria origine — proposto · confermato · modificato · '
        'inserito — e la reimportazione riscrive SOLO le righe che nessuno ha ancora guardato.',
        'La baseline (ANSC_CFG_VERSIONE) tiene insieme le tabelle decise dal Comune: si '
        'attivano e si storicizzano in blocco, mai una per volta.',
    ]):
        dr.text((60, y + 26 + i * 24), t, font=fnt(F_ITA, 16), fill=MUTED)
    dr.text((60, y + 76), 'ATTENZIONE: i file del repository non sono un canale, sono il '
                          'riscontro; in esercizio si legge e si scrive solo sul database. Il '
                          'catalogo degli UC e i dizionari non stanno nella baseline: sono '
                          'repliche, con validità temporale.', font=fnt(F_ITA, 16), fill=ROSSO)

    # ---------------- 3 · l'esecuzione
    banda(dr, 40, 724, W - 40, 1074, '#2f6bb0',
          '3 · L’ESECUZIONE — che cosa accade quando l’operatore forma un atto', BLU)
    for i, (t, s, f, col) in enumerate(PASSI):
        x = 60 + i * (P_LARG + P_GAP)
        riquadro(dr, x, P_Y, P_LARG, 186, t, s, f, col)
        if i < len(PASSI) - 1:
            percorso(dr, [(x + P_LARG + 3, P_Y + 93), (x + P_LARG + P_GAP - 3, P_Y + 93)],
                     '#4b5563', larg=3)

    dr.text((60, 964), 'Il passaggio che dà il nome al capitolo è il quinto: il payload non si '
                       'costruisce per UC, si costruisce UNA VOLTA sull’albero del modello e si '
                       'riempie secondo la configurazione.', font=fnt(F_BLD, 16), fill=BLU)
    dr.text((60, 990), 'È la ragione per cui l’adattatore di mappatura è uno solo per tutte le '
                       'famiglie di atti, e non uno per famiglia.', font=fnt(F_ITA, 16),
            fill=MUTED)

    box(dr, 60, 1016, 820, 48, 'grigio', 'Che cosa fa il pre-filtro',
        'campi obbligatori dell’UC, documenti richiesti, valori validi contro i dizionari',
        ts=17, ss=15)
    box(dr, 900, 1016, 820, 48, 'rosso', 'Che cosa NON può fare',
        'accertare la scansione antivirus (R001) e sostituire la validazione di R009',
        ts=17, ss=15)

    legenda(dr, 56, H - 44,
            [('rosso', 'fonti ANSC'), ('giallo', 'replicato da ANSC'),
             ('verde', 'deciso dal Comune'), ('blu', 'esecuzione'),
             ('grigio', 'portata del pre-filtro')])
    im.save(dest)
    return dest


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'img')
    os.makedirs(out, exist_ok=True)
    print('scritto:', figura(os.path.join(out, 'catena_configurazione.png')))
