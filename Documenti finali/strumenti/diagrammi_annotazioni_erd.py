# -*- coding: utf-8 -*-
"""Diagramma entità-relazioni delle tabelle per le annotazioni verso ANSC (14/11/2026).

Le due tabelle nuove, ANSC_ANNOTAZIONE e ANSC_ANNOTAZIONE_CORREZIONE, in relazione con quelle
esistenti:
  · MATR_USR — la proposta di annotazione di SIPO (ANNOTAZIONE_ATTO, ANNOTAZIONE_TAG_VALUES,
    dalle entity di common/matrim-entities), l'atto (ATTO) e la formula (CONF_FORMULA_ANNOTAZIONE);
  · ANSC_USR — lo stato dell'atto (ANSC_STATO_ATTO), l'audit (ANSC_LOG_AUDIT), la configurazione
    dei campi (ANSC_CFG_CAMPO) e la numerazione comunale (DATI_ATTO_ESTERNO).
Linea piena = FK dichiarata; tratteggio = riferimento per valore (nessuna FK fra schemi).

    /Library/Developer/CommandLineTools/usr/bin/python3 diagrammi_annotazioni_erd.py
"""
import os

from diagrammi_comune import (C, F_BLD, F_ITA, INK, MUTED, banda, fnt, legenda, percorso,
                              scheda, tela)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'annullamento',
                   'erd_annotazioni_ansc.png')
W, H = 2300, 1340


def disegna(dest=OUT):
    im, dr = tela(W, H, "Le annotazioni verso ANSC: tabelle nuove e tabelle esistenti",
                  "La proposta resta in MATR_USR; ciò che serve ad ANSC sta in ANSC_USR, "
                  "collegato per valore")
    banda(dr, 30, 100, 760, 1260, C['grigio'][0], "MATR_USR — SIPO, stato civile", INK)
    banda(dr, 800, 100, W - 30, 1260, C['blu'][0], "ANSC_USR — integrazione con ANSC", INK)

    # ---------------------------------------------------------------- MATR_USR (esistenti)
    atto = scheda(dr, 70, 160, 330, 'grigio', "ATTO", [
        ("PK", "ID_ATTO"),
        ("", "AREA"),
        ("", "NUMERO_ATTO · PARTE · SERIE"),
        ("", "ESPONENTE · ANNO"),
        ("", "ID_STATO_PRATICA"),
    ])
    formula = scheda(dr, 430, 160, 300, 'grigio', "CONF_FORMULA_ANNOTAZIONE", [
        ("PK", "ID_FORMULA"),
        ("", "DESCRIZIONE (es. 190 - Art. 98)"),
        ("", "TESTO con i tag"),
    ], nota="tag VALORE_ANTE, VALORE_CORRETTO")
    proposta = scheda(dr, 70, 470, 420, 'grigio', "ANNOTAZIONE_ATTO", [
        ("PK", "ID"),
        ("FK", "ID_ATTO_TARGET  → ATTO"),
        ("FK", "ID_FORMULA  → CONF_FORMULA_ANN."),
        ("FK", "ID_CONF_STATO · ID_TIPO_ANNOTAZIONE"),
        ("", "TARGET_NUMERO_ATTO · _PARTE · _SERIE"),
        ("", "TARGET_ANNO · TARGET_ESPONENTE"),
        ("", "TESTO_ANNOTAZIONE"),
        ("", "DATA_PROPOSTA · ID_UTENTE_LOG"),
    ], nota="la proposta di SIPO: resta com'è")
    tag = scheda(dr, 70, 860, 420, 'grigio', "ANNOTAZIONE_TAG_VALUES", [
        ("FK", "ID_ANNOTAZIONE_ATTO  → ANNOT._ATTO"),
        ("FK", "ID_TAG"),
        ("", "TAG_VALUE  (VALORE_ANTE, VALORE_CORRETTO)"),
        ("", "DATA_INS"),
    ], nota="i valori della formula, come testi liberi")

    # ---------------------------------------------------------------- ANSC_USR (nuove)
    ann = scheda(dr, 840, 300, 560, 'verde', "ANSC_ANNOTAZIONE  (nuova)", [
        ("PK", "ID_ANNOTAZIONE"),
        ("", "ID_ANNOTAZIONE_ATTO   → ANNOTAZIONE_ATTO.ID"),
        ("", "ID_ATTO_SIPO   → ATTO / ANSC_STATO_ATTO"),
        ("", "COD_SERVIZIO_ANSC · COD_UC_ANSC"),
        ("", "COD_FORMULA_ANSC · ID_TIPO_RETTIFICA"),
        ("", "ID_ANSC_COLLEGATO   → ANSC_STATO_ATTO.ID_ANSC"),
        ("", "ID_COMUNE_ / NUMERO_ATTO_ / NUM_ANNO_COLLEGATO"),
        ("", "DATA_FORMAZIONE_ / ID_TIPO_REGISTRO_COLLEGATO"),
        ("", "DESC_ENTE · ID_COMUNE_ENTE · ID_PROVINCIA_ENTE"),
        ("", "COD_TIPO_ / NUM_ / DATA_PROVVEDIMENTO"),
        ("", "DESC_ESTREMI_DOCUMENTO"),
        ("", "TXT_DETTAGLIO_RETTIFICA · TXT_COMPOSIZIONE"),
        ("", "NUMERO_ATTO · NUM_ANNO   → DATI_ATTO_ESTERNO"),
        ("", "TS_FORMAZIONE · ID_ANSC · ID_STATO · STATO"),
        ("", "COD_FASE · TXT_ERRORE"),
        ("", "TXT_EVENTO · TXT_EVENTO_MODIFICATO"),
        ("", "TS_/UTENTE_PROPOSTA · TS_/UTENTE_CONFERMA"),
        ("", "TS_DEPOSITO · TS_FIRMA · UTENTE_FIRMA"),
        ("UK", "ID_ANNOTAZIONE_ATTO"),
    ], nota="una riga per annotazione, dalla proposta alla firma", cs=15)
    corr = scheda(dr, 840, 1010, 560, 'verde', "ANSC_ANNOTAZIONE_CORREZIONE  (nuova)", [
        ("PK", "ID_CORREZIONE"),
        ("FK", "ID_ANNOTAZIONE  → ANSC_ANNOTAZIONE"),
        ("", "NUM_ORDINE"),
        ("", "COD_PERCORSO_ANSC   → ANSC_CFG_CAMPO"),
        ("", "DESC_DATO · ALIAS_CAMPO_SIPO"),
        ("", "TXT_VALORE_ANTE (da ANSC) · TXT_VALORE_SIPO"),
        ("", "TXT_VALORE_NUOVO · FLG_VERIFICATO"),
        ("UK", "ID_ANNOTAZIONE, COD_PERCORSO_ANSC"),
    ], nota="una riga per dato corretto", cs=15)

    # ---------------------------------------------------------------- ANSC_USR (esistenti)
    stato = scheda(dr, 1480, 160, 380, 'blu', "ANSC_STATO_ATTO", [
        ("PK", "ID_ATTO_SIPO"),
        ("", "ID_ANSC · NUMERO_ATTO"),
        ("", "ID_STATO · STATO · COD_FASE"),
        ("", "TXT_EVENTO"),
    ], nota="lo stato in ANSC dell'atto annotato")
    audit = scheda(dr, 1900, 160, 360, 'blu', "ANSC_LOG_AUDIT", [
        ("PK", "ID_AUDIT"),
        ("FK", "→ ANSC_STATO_ATTO"),
        ("", "FASE · RICHIESTA · RISPOSTA"),
        ("", "ESITO · OPERATORE"),
    ], nota="le chiamate R013 / R007")
    numer = scheda(dr, 1480, 620, 380, 'blu', "DATI_ATTO_ESTERNO", [
        ("PK", "id_atto_esterno"),
        ("", "nr_anno_atto · nr_atto_comunale"),
        ("", "id_atto_sipo · id_ansc · stato"),
    ], nota="i numeri staccati da be-numeratore-comunale")
    cfg = scheda(dr, 1480, 1010, 380, 'blu', "ANSC_CFG_CAMPO", [
        ("", "ID_VERSIONE · COD_UC_ANSC"),
        ("", "OGGETTO_ANSC · CAMPO_ANSC"),
        ("", "ALIAS_CAMPO_SIPO"),
    ], nota="percorso ANSC ↔ campo SIPO")

    # ---------------------------------------------------------------- relazioni
    grig, blu, verde = C['grigio'][0], C['blu'][0], C['verde'][0]
    # FK esistenti in MATR_USR
    percorso(dr, [(235, atto[3]), (235, proposta[1])], grig, etichetta="N:1", pos=(258, 420))
    percorso(dr, [(580, formula[3]), (580, 440), (440, 440), (440, proposta[1])], grig,
             etichetta="N:1", pos=(605, 400))
    percorso(dr, [(280, proposta[3]), (280, tag[1])], grig, etichetta="1:N", pos=(303, 800))
    # FK nuova
    percorso(dr, [(1120, ann[3]), (1120, corr[1])], verde, larg=4, etichetta="1:N",
             pos=(1145, ann[3] + 20))
    # per valore: proposta ↔ annotazione ANSC (1:0..1)
    percorso(dr, [(proposta[2], 560), (ann[0], 560)], verde, tratteggio=True,
             etichetta="1:0..1  per valore", pos=(560, 528))
    # per valore: ATTO ↔ annotazione
    percorso(dr, [(235, atto[1]), (235, 140), (785, 140), (785, 380), (ann[0], 380)], verde,
             tratteggio=True, etichetta="ID_ATTO_SIPO  per valore", pos=(560, 118))
    # parallelismo tag ↔ correzioni
    percorso(dr, [(tag[2], 930), (790, 930), (790, 1100), (corr[0], 1100)], verde,
             tratteggio=True, etichetta="stessa informazione, strutturata", pos=(640, 904))
    # annotazione → stato atto
    percorso(dr, [(ann[2], 380), (1440, 380), (1440, 230), (stato[0], 230)], blu,
             tratteggio=True, etichetta="atto annotato", pos=(1440, 400))
    # stato → audit (FK esistente)
    percorso(dr, [(stato[2], 230), (audit[0], 230)], blu, etichetta="1:N", pos=(1880, 204))
    # annotazione → numerazione
    percorso(dr, [(ann[2], 710), (numer[0], 710)], blu, tratteggio=True,
             etichetta="numero proprio", pos=(1440, 684))
    # correzione → configurazione
    percorso(dr, [(corr[2], 1080), (cfg[0], 1080)], blu, tratteggio=True,
             etichetta="percorso", pos=(1440, 1090))

    legenda(dr, 60, 1290, [
        ('verde', "tabella nuova (ANSC_USR)"),
        ('blu', "tabella esistente in ANSC_USR"),
        ('grigio', "tabella esistente in MATR_USR"),
    ])
    dr.text((1180, 1294), "linea piena = FK dichiarata · tratteggio = riferimento per valore, "
            "nessuna FK fra schemi", font=fnt(F_ITA, 16), fill=MUTED)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    im.save(dest)
    return dest


if __name__ == '__main__':
    print(disegna())
