# -*- coding: utf-8 -*-
"""Lo schema ANSC_USR: l'operativo alla base, configurazione e dizionari sopra.

⚠️ L'impaginazione non è estetica ma dice una cosa del disegno: **la parte operativa sta alla
base**, e sopra di essa stanno la configurazione e i dizionari, che esistono per servirla.

⚠️ I collegamenti si disegnano con percorsi ORTOGONALI dentro i corridoi fra le tabelle, non
con segmenti diretti: con quattordici tabelle e venti legami, le diagonali attraversano i
riquadri e il diagramma diventa illeggibile — è già successo. Ogni legame dichiara quindi la
propria uscita, il corridoio che percorre e il lato di arrivo. Le coordinate dei corridoi sono
in CORR_V e CORR_H: se si sposta una tabella, si sposta anche il corridoio.

⚠️ Va rigenerato a ogni modifica del modello dati: modello e diagramma sono una coppia.

    /Library/Developer/CommandLineTools/usr/bin/python3 diagrammi_erd.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import diagrammi_comune as G   # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')

W, H = 1700, 1454
LARG = 350                                  # larghezza di ogni scheda
COL = {1: 60, 2: 470, 3: 880, 4: 1290}      # ascisse delle quattro colonne
RIGA = {1: 176, 2: 392, 3: 592, 4: 796}     # ordinate delle quattro righe della configurazione
OPER = 1046                                 # ordinata della fascia operativa
CORR_V = {'1-2': 440, '2-3': 850, '3-4': 1260}   # corridoi verticali fra le colonne
CORR_H = {'1-2': 366, '2-3': 576, '2-3b': 586, 'sotto': 984}  # corridoi orizzontali fra le righe

# (colonna, riga, colore, titolo, righe, nota)
TABELLE = [
    # ─────────── riga 1: i cataloghi e ciò che si replica da ANSC
    (1, 1, 'verde', 'ANSC_CFG_UC', [
        ('PK', 'ID_UC_CFG'), ('UK', 'COD_UC_ANSC + ID_VERSIONE'),
        ('', 'ID_MODELLO_ATTO, ID_CONF_TIPO_ATTO'),
        ('', 'MASCHERA_UI, SERIE, NUM_PRIORITA'),
        ('FK', 'ID_DOMINIO=1 + COD_LOGICA'), ('FK', 'ID_VERSIONE')],
     'quale UC, e quando si applica'),
    (2, 1, 'giallo', 'ANSC_ANA_UC', [
        ('PK', 'ID_UC'), ('', 'COD_UC_ANSC, COD_MOTORE'),
        ('', 'COD_FAMIGLIA, COD_VERSIONE'),
        ('', 'ID_TIPO_EVENTO (ANSC_01)'),
        ('', 'ID_TIPO_DOCUMENTO, validità')], 'il catalogo degli UC'),
    (3, 1, 'verde', 'ANSC_CFG_SEZIONE', [
        ('PK', 'ID_SEZIONE'), ('FK', 'ID_UC → ANA_UC'),
        ('', 'SEZIONE_FE_ANSC, OGGETTO_ANSC'),
        ('FK', 'ID_DOMINIO=2 + COD_LOGICA'), ('FK', 'ID_VERSIONE')],
     'quando una sezione si popola'),
    (4, 1, 'viola', 'DOMINIO_DECODIFICA', [
        ('PK', 'id_dominio + nm_dominio'), ('', 'il nome è IN CHIAVE: 134 e 135'),
        ('', 'cd_versione (da R901)')],
     'le decodifiche pubblicate da ANSC'),

    # ─────────── riga 2: ciò che pende dai cataloghi
    (1, 2, 'verde', 'LOGICHE_DI_SCELTA', [
        ('PK', 'ID_DOMINIO + COD_LOGICA_DI_SCELTA'),
        ('', 'DESC_LOGICA_DI_SCELTA'),
        ('', 'TXT_LOGICA (espressione)')], 'le logiche, scritte una volta sola'),
    (2, 2, 'verde', 'ANSC_CFG_FORMULA', [
        ('PK', 'ID_FORMULA'), ('FK', 'ID_UC → ANA_UC'), ('FK', 'ID_VERSIONE')],
     'le diciture dell’atto'),
    (3, 2, 'verde', 'ANSC_CFG_CAMPO', [
        ('PK', 'ID_CAMPO'), ('FK', 'ID_SEZIONE'),
        ('', 'OGGETTO_ANSC + CAMPO_ANSC'), ('', 'SCHEMA_/TABELLA_/CAMPO_SIPO'),
        ('', 'ID_ / NM_DECODIFICA_ANSC'),
        ('FK', 'ID_DOMINIO=3 + ID_BUSINESS_LOGIC'),
        ('', 'FLG_OBBLIGATORIO, VALORE_DEFAULT')],
     'da dove viene ogni dato'),
    (4, 2, 'viola', 'VALORE_DOMINIO', [
        ('PK', 'id_dominio + nm_dominio'), ('', '+ id_valore'),
        ('', 'ds_valore, validità'), ('', 'nr_ordinamento'),
        ('', 'tx_attributi (JSON)')],
     'si legge per chiave: dominio + valore'),

    # ─────────── riga 3: le due radici che tutti richiamano
    (1, 3, 'verde', 'TIPO_LOGICHE_DI_SCELTA', [
        ('PK', 'ID_DOMINIO'), ('', '1 scelta dell’UC'),
        ('', '2 attivazione di sezione'),
        ('', '3 logica dei campi')], 'i domini di logica'),
    (2, 3, 'giallo', 'ANSC_CFG_VERSIONE', [
        ('PK', 'ID_VERSIONE'), ('', 'COD_STATO: bozza/attiva/storica'),
        ('FK', '← da CFG_UC, CFG_SEZIONE, CFG_CAMPO,'),
        ('', '   CFG_FORMULA, ALLEGATI_USECASE'),
        ('', '   e da STATO_ATTO (timbro storico)')],
     'la baseline: sei rimandi, frecce omesse'),
    (3, 3, 'verde', 'ALLEGATI_USECASE', [
        ('PK', 'cd_usecase + ty_allegato'), ('', '+ id_versione'),
        ('', 'ty_presenza, cd_logica'), ('', 'fg_operante, nr_ordinamento')],
     'i documenti richiesti — nomi di Side'),

    (4, 3, 'verde', 'RICONCILIAZ_DIZIONARI', [
        ('PK', 'ID_RICONCILIAZIONE'), ('UK', 'DECODIFICA + VALORE_ANSC'),
        ('', '+ CAMPO_SIPO · VALORE_SIPO'),
        ('', 'SCHEMA/TABELLA_SIPO, CAMPO_SIPO'),
        ('FK', 'ID_DOMINIO_SIPO (in alternativa)'), ('', 'validità temporale')],
     'il corrispondente locale di un valore ANSC'),

    # ─────────── alla base: ciò che accade agli atti
    (1, 'op', 'blu', 'ANSC_STATO_ATTO', [
        ('PK', 'ID_STATO_ATTO'), ('', 'ID_ATTO_SIPO, ID_MODELLO_ATTO'),
        ('', 'ID_TIPO_EVENTO, ID_TIPO_CONTENUTO'),
        ('', 'ID_UC_ANSC, COD_LOGICA, COD_ORIGINE_UC'),
        ('', 'COD_FASE'),
        ('', 'STATO (replica ANSC), TIPO_ESITO'),
        ('', 'ID_ANSC, NUM_COMUNALE'),
        ('', 'TXT_PAYLOAD, FLG_EMERGENZA'), ('FK', 'ID_VERSIONE')],
     'l’atto: che cosa è stato deciso, inviato e ottenuto'),
    (2, 'op', 'blu', 'ANSC_LOG_AUDIT', [
        ('PK', 'ID_AUDIT'), ('FK', 'ID_STATO_ATTO'),
        ('', 'FASE, ESITO'), ('', 'RICHIESTA / RISPOSTA')], 'la traccia di ogni passo'),
    # ⚠️ ALLEGATO sta in MATR_USR, non in ANSC_USR: si disegna in grigio per distinguerla
    # dalle altre e la nota lo dichiara. ⚠️ «fg_extra» era il nome superato dalla v3.29.
    (3, 'op', 'grigio', 'ALLEGATO', [
        ('PK', 'id_allegato'), ('', 'id_atto_sipo, id_ansc_allegato'),
        ('', 'oj_allegato (BLOB), cd_hash'),
        ('', 'cd_stato, fg_testo_libero')], 'i documenti — in MATR_USR, da Side'),
    (4, 4, 'verde', 'ANSC_CFG_DOMINIO_SIPO', [
        ('PK', 'ID_DOMINIO_SIPO'),
        ('', 'ID_DOMINIO + NM_DOMINIO (il dominio)'),
        ('', 'SCHEMA_SIPO (facoltativo)'),
        ('', 'TABELLA_SIPO, CAMPO_SIPO'),
        ('UK', 'DECODIFICA — colonna virtuale')],
     'dove vive in SIPO un dominio ANSC'),
    (4, 'op', 'blu', 'ANSC_NOTIFICA', [
        ('PK', 'ID_NOTIFICA'), ('', 'ID_ANSC, genere, stato')], 'il flusso in ingresso'),
]

# (da, lato_da, corridoi, a, lato_a, tratteggio)
#   «corridoi» sono i punti intermedi: 'v:<nome>' un corridoio verticale, 'h:<nome>' uno
#   orizzontale. Il percorso si costruisce a gomiti, mai in diagonale.
LEGAMI = [
    # chiavi esterne dichiarate nel DDL
    ('ANSC_CFG_SEZIONE', 's', [], 'ANSC_ANA_UC', 'd', False),
    ('ANSC_CFG_CAMPO', 'g', [], 'ANSC_CFG_SEZIONE', 'b', False),
    ('ANSC_CFG_FORMULA', 'g', [], 'ANSC_ANA_UC', 'b', False),
    ('VALORE_DOMINIO', 'g', [], 'DOMINIO_DECODIFICA', 'b', False),
    ('LOGICHE_DI_SCELTA', 'b', [], 'TIPO_LOGICHE_DI_SCELTA', 'g', False),
    ('ANSC_CFG_UC', 'b', [], 'LOGICHE_DI_SCELTA', 'g', False),
    ('ANSC_CFG_SEZIONE', 'b', ['h:1-2'], 'LOGICHE_DI_SCELTA', 'd', False),
    ('ALLEGATI_USECASE', 's', ['h:2-3'], 'LOGICHE_DI_SCELTA', 'b', False),
    ('ANSC_CFG_CAMPO', 'b', ['h:2-3b'], 'LOGICHE_DI_SCELTA', 'b', False),
    ('ANSC_LOG_AUDIT', 's', [], 'ANSC_STATO_ATTO', 'd', False),
    # riferimenti per valore, senza vincolo di integrità
    ('ANSC_CFG_UC', 'd', [], 'ANSC_ANA_UC', 's', True),
    ('ALLEGATI_USECASE', 'g', ['v:2-3'], 'ANSC_ANA_UC', 'd', True),
    ('ANSC_CFG_CAMPO', 'd', [], 'VALORE_DOMINIO', 's', True),
    ('RICONCILIAZ_DIZIONARI', 'g', [], 'VALORE_DOMINIO', 'b', True),
    ('ANSC_CFG_DOMINIO_SIPO', 'g', [], 'RICONCILIAZ_DIZIONARI', 'b', False),
    ('ANSC_CFG_DOMINIO_SIPO', 's', [], 'DOMINIO_DECODIFICA', 's', True),
]


def disegna(percorso=None):
    percorso = percorso or os.path.join(IMG, 'erd_ansc_usr.png')
    im, dr = G.tela(W, H, 'Schema ANSC_USR',
                    'le tabelle operative sono la base: configurazione e dizionari esistono '
                    'per metterle in grado di lavorare. In grigio l’unica tabella che non '
                    'sta in ANSC_USR')
    G.banda(dr, 40, 140, W - 40, 980, '#3f8f5f',
            'CONFIGURAZIONE — la decide il Comune · REPLICHE — le pubblica ANSC', '#a8801a')
    G.banda(dr, 40, 1016, W - 40, 1276, '#2f6bb0',
            'OPERATIVE — ciò che accade agli atti', '#25548a')

    riq = {}
    for colonna, riga, colore, titolo, righe, nota in TABELLE:
        y = OPER if riga == 'op' else RIGA[riga]
        riq[titolo] = G.scheda(dr, COL[colonna], y, LARG, colore, titolo, righe, nota)

    def bordo(nome, lato):
        x1, y1, x2, y2 = riq[nome]
        return {'d': (x2, (y1 + y2) / 2), 's': (x1, (y1 + y2) / 2),
                'g': ((x1 + x2) / 2, y1), 'b': ((x1 + x2) / 2, y2)}[lato]

    for da, lato_da, corridoi, a, lato_a, tratteggio in LEGAMI:
        p1, p2 = bordo(da, lato_da), bordo(a, lato_a)
        punti = [p1]
        for c in corridoi:
            tipo, nome = c.split(':')
            if tipo == 'v':
                x = CORR_V.get(nome, COL[1] - 26)
                punti += [(x, punti[-1][1]), (x, p2[1])]
            else:
                y = CORR_H[nome]
                punti += [(punti[-1][0], y), (p2[0], y)]
        if not corridoi and abs(p1[0] - p2[0]) > 4 and abs(p1[1] - p2[1]) > 4:
            # gomito unico: si esce in orizzontale se il lato è destro o sinistro
            punti.append((p2[0], p1[1]) if lato_da in 'ds' else (p1[0], p2[1]))
        punti.append(p2)
        colore = G.MUTED if tratteggio else G.ARROW
        G.percorso(dr, punti, colore, tratteggio, 2)

    G.percorso(dr, [(860, 982), (860, 1042)], '#25548a', False, 4)
    dr.text((876, 994), 'la configurazione guida ciò che accade agli atti',
            font=G.fnt(G.F_ITA, 17), fill='#25548a')

    G.legenda(dr, 60, 1304, [('verde', 'decise dal Comune'), ('giallo', 'replicate da ANSC'),
                             ('viola', 'dizionari'), ('blu', 'operative')])
    y = 1348
    G.linea(dr, [(62, y + 8), (122, y + 8)], G.ARROW, False, 3)
    dr.text((132, y), 'chiave esterna dichiarata nel DDL', font=G.fnt(G.F_REG, 16),
            fill=G.MUTED)
    G.linea(dr, [(560, y + 8), (620, y + 8)], G.MUTED, True, 3)
    dr.text((630, y), 'riferimento per valore, senza vincolo: domini di guasto separati',
            font=G.fnt(G.F_REG, 16), fill=G.MUTED)
    im.save(percorso)
    return percorso


if __name__ == '__main__':
    os.makedirs(IMG, exist_ok=True)
    print('scritto:', disegna())
