# -*- coding: utf-8 -*-
"""Il flusso operativo dall'atto salvato in SIPO all'atto formato in ANSC.

⚠️ La figura dice quattro cose che il testo da solo non tiene insieme: in quale ordine si
procede, **in quale fase** si è, **quale tabella guida** ciascun passo e **che cosa resta
scritto** quando il passo è finito. L'ultima è la ragione per cui esiste: una traccia che non
sia prevista nel disegno non viene scritta da nessuno, e la si scopre mancante il giorno in
cui si deve spiegare che cosa è successo a un atto.

    /Library/Developer/CommandLineTools/usr/bin/python3 diagrammi_flusso.py img
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import diagrammi_comune as G   # noqa: E402

# (fase, condizione di uscita della fase, COD_FASE raggiunto)
# v3.43: allineato al processo del capitolo «Il processo di gestione dei dati ANSC in SIPO».
# v3.48: le quattro fasi raggruppano le PAGINE di quel capitolo — A dati anagrafici e
# dettaglio, B riepilogo (UC, firmatari, documenti, verifica locale), C anteprima e VALIDA,
# D firme, «Definisci» e «Chiudi» — e il flusso dichiara il ritorno ai dati (stato 0).
FASI = {
    'A': ('FASE A — DATI ANAGRAFICI E DETTAGLIO', 'soggetti cercati in ANSC, intestatario '
          'obbligatorio; nessun dato richiesto mancante', '#2f6bb0'),
    'B': ('FASE B — RIEPILOGO', 'UC determinato, documenti accettati, verifica locale superata',
          '#7b5aa6'),
    'C': ('FASE C — ANTEPRIMA E VALIDA', 'numero comunale staccato, atto validato da ANSC',
          '#a8801a'),
    'D': ('FASE D — FIRME E DEFINIZIONE', 'con la firma dell’USC l’atto è formato e non torna '
          'più ai dati', '#b03a48'),
}

# (fase, numero, titolo, sottotitolo, legge, scrive, fase di audit, colore)
PASSI = [
    ('A', '1', 'Tipo atto e dati anagrafici', 'le maschere di SIPO; l’intestatario dai '
     'soggetti dell’UC', 'tabelle di SIPO\nSOGGETTI_USECASE (l’intestatario)',
     'l’atto in SIPO: ID_ATTO_SIPO\nstato SIPO 1 In lavorazione', '', 'grigio'),
    ('A', '2', 'Dettaglio: ricerca dei soggetti', 'R005 con l’OTP di sessione; per '
     'l’intestatario la ricerca è obbligatoria, il risultato no', 'ANSC (consultazione)',
     'ANSC_SOGGETTO_IDENTIFICATIVI · ANAG_USR.SOGGETTO\nANSC_STATO_ATTO (IN_LAVORAZIONE)\n'
     'e pagina di ripresa', 'SOGGETTO', 'rosso'),
    ('B', '3', 'Riepilogo: determinazione dell’UC', 'automatica; l’operatore sceglie solo se '
     'ambigua', 'ANSC_CFG_UC (baseline ATTIVA)\nLOGICHE_DI_SCELTA (dominio 1)',
     'ANSC_STATO_ATTO\nID_UC_ANSC · COD_LOGICA · COD_ORIGINE_UC\nID_VERSIONE · COD_FASE = '
     'UC_DETERMINATO', 'DETERMINAZIONE', 'blu'),
    ('B', '4', 'Riepilogo: firmatari', 'chi firma, con il contrassegno modificabile',
     'SOGGETTI_USECASE (fg_firmatario)', 'firmatari: chi firma e in quale modo', '', 'blu'),
    ('B', '5', 'Riepilogo: documenti e atti a testo libero', 'caricamento in SIPO e invio ad '
     'ANSC — R001', 'ALLEGATI_USECASE (che cosa serve)',
     'ALLEGATO\nid_ansc_allegato · cd_stato · fg_testo_libero\nCOD_FASE = DOCUMENTI_ACQUISITI',
     'ALLEGATI', 'viola'),
    ('B', '6', 'Riepilogo: verifica locale', 'pre-filtro RF-9: nessuna chiamata ad ANSC',
     'ANSC_CFG_SEZIONE · ANSC_CFG_CAMPO\nALLEGATI_USECASE · V_ANSC_DIZ_VALIDO',
     'esito a video; COD_FASE = PREVALIDATO', 'PREVERIFICA', 'giallo'),
    ('C', '7', 'Anteprima: numero comunale', 'stacco dalla serie dell’anno; il modello evento '
     'lo porta', 'num-ansc-sipo',
     'DATI_ATTO_ESTERNO (il numero e la sua sorte)\nANSC_STATO_ATTO.NUM_COMUNALE', '', 'blu'),
    ('C', '8', 'Anteprima: il modello evento', 'un solo adattatore, guidato dalla '
     'configurazione', 'ANSC_CFG_SEZIONE · ANSC_CFG_CAMPO\nANSC_CFG_FORMULA · dizionari',
     'ANSC_STATO_ATTO.TXT_EVENTO\n(il modello evento in redazione,\naggiornato a ogni salvataggio)',
     'PAYLOAD', 'blu'),
    ('C', '9', 'Anteprima del testo', 'R010 — facoltativa, prima della validazione',
     'il modello evento', 'nulla: è una lettura', 'ANTEPRIMA', 'giallo'),
    ('C', '10', '«VALIDA»: la validazione ANSC', 'R009 — da qui l’identificativo nazionale è '
     'consumato', 'il modello evento',
     'ANSC_STATO_ATTO: ID_ANSC · STATO = CONFERMATO\nCOD_FASE = VALIDATO\n'
     'TXT_HASH_VALIDATO: impronta del modello validato', 'DEPOSITO', 'rosso'),
    ('D', '11', 'Firme dei dichiaranti', 'R006 cartacea · R012 elettronica; senza firmatari '
     'si salta', 'firmatari (chi firma e come)',
     'firmatari: stato della firma\nANSC_STATO_ATTO: STATO = FIRMATO_DICHIARANTE',
     'FIRMA_DICH', 'rosso'),
    ('D', '12', 'Attestazione di conformità', 'R007 — firmata dall’USC',
     'ALLEGATO (documenti inclusi)', 'ANSC_STATO_ATTO: STATO = FIRMATO_CONFORMITA',
     'FIRMA_CONFORMITA', 'rosso'),
    ('D', '13', 'Firma dell’USC, «Definisci» e «Chiudi»', 'R007 con le credenziali di firma '
     'remota; la comunicazione anagrafica con R014 se l’UC la prevede',
     'lo stato reale dell’atto\ncomunicaz_anagrafica_usecase',
     'ANSC_STATO_ATTO: STATO = FIRMATO_USC\nCOD_FASE = FIRMATO · in SIPO 2 DEFINITO\n'
     'l’atto si blocca in SIPO', 'FIRMA_USC', 'rosso'),
]
ULTIMO = PASSI[-1][1]


def flusso(dest):
    im, dr = G.tela(1600, 2600, 'Il flusso operativo: dall’atto di SIPO all’atto formato',
                    'quattro fasi; per ogni passo la configurazione che lo guida, ciò che '
                    'resta scritto e la fase con cui l’audit lo registra')

    x0, y = 40, 150
    dr.text((x0 + 16, y), 'Passo', font=G.fnt(G.F_BLD, 17), fill='#25548a')
    dr.text((470, y), 'Che cosa legge', font=G.fnt(G.F_BLD, 17), fill='#3f8f5f')
    dr.text((900, y), 'Che cosa scrive', font=G.fnt(G.F_BLD, 17), fill='#25548a')
    dr.text((1370, y), 'ANSC_LOG_AUDIT', font=G.fnt(G.F_BLD, 17), fill='#b03a48')
    y += 30

    corrente = None
    for fase, num, titolo, sotto, legge, scrive, audit, colore in PASSI:
        if fase != corrente:
            corrente = fase
            nome, condizione, col = FASI[fase]
            dr.rounded_rectangle([x0, y, 1560, y + 34], radius=8, fill='#f3f4f6', outline=col,
                                 width=2)
            dr.text((x0 + 14, y + 8), nome, font=G.fnt(G.F_BLD, 17), fill=col)
            dr.text((x0 + 430, y + 9), '· ' + condizione, font=G.fnt(G.F_ITA, 16), fill=G.MUTED)
            y += 44

        alt = 100 if '\n' in scrive or '\n' in legge else 74
        bordo, fondo = G.C[colore]
        dr.rounded_rectangle([x0, y, 450, y + alt], radius=10, fill=fondo, outline=bordo,
                             width=2)
        dr.text((x0 + 18, y + 14), num + ' · ' + titolo, font=G.fnt(G.F_BLD, 17), fill=G.INK)
        for i, rg in enumerate(G.avvolgi(dr, sotto, G.fnt(G.F_ITA, 15), 380)):
            dr.text((x0 + 18, y + 40 + i * 20), rg, font=G.fnt(G.F_ITA, 15), fill=G.MUTED)

        for i, rg in enumerate(legge.split('\n')):
            dr.text((470, y + 16 + i * 22), rg, font=G.fnt(G.F_REG, 15), fill='#2f6b47')
        G.freccia(dr, (452, y + alt / 2), (466, y + alt / 2), G.MUTED, 2)

        for i, rg in enumerate(scrive.split('\n')):
            f = G.F_BLD if i == 0 else G.F_REG
            dr.text((900, y + 16 + i * 22), rg, font=G.fnt(f, 15), fill=G.INK)

        if audit:
            for i, rg in enumerate(audit.split(' · ')):
                dr.text((1370, y + 16 + i * 22), rg, font=G.fnt(G.F_REG, 15), fill='#b03a48')
        else:
            dr.text((1370, y + 16), '—', font=G.fnt(G.F_REG, 15), fill=G.MUTED)

        if num != ULTIMO:
            G.percorso(dr, [(x0 + 60, y + alt), (x0 + 60, y + alt + 12)], G.ARROW, False, 3)
        y += alt + 12

    y += 16
    dr.text((x0, y), 'Sei regole che il flusso impone', font=G.fnt(G.F_BLD, 19),
            fill='#25548a')
    for i, t in enumerate([
        'Ogni fase aggiorna lo stato dell’atto: COD_FASE dice a che punto è la lavorazione '
        'locale, STATO replica lo stato dichiarato da ANSC. Sono due cose diverse e non si '
        'confondono.',
        'Ogni passo lascia una riga in ANSC_LOG_AUDIT: anche quelli che non chiamano ANSC, '
        'perché sono le decisioni che spiegano il payload.',
        'Dal passo 10 in avanti l’identificativo nazionale è consumato: un esito indeterminato '
        'non si ritenta, si accerta con R005 e semmai si annulla con R011.',
        'Fino alla firma dell’USC si torna ai dati: se cambiano, l’atto va nello stato 0 e le '
        'firme si chiudono finché una nuova validazione dello stesso atto non lo riporta a '
        'CONFERMATO; dopo le firme dei dichiaranti, solo se tutti possono firmare di nuovo.',
        'Dopo la firma dell’USC l’atto non è più modificabile in SIPO, nemmeno nello stesso '
        'giorno: la correzione passa per gli istituti di ANSC (annotazione, rettifica, '
        'annullamento), non per la maschera.',
        'Dal passo 2 ogni salvataggio aggiorna ANSC_STATO_ATTO con il modello evento e la pagina '
        'raggiunta: la redazione si sospende e si riprende dal punto in cui era.',
    ]):
        for j, rg in enumerate(G.avvolgi(dr, t, G.fnt(G.F_REG, 16), 1480)):
            dr.text((x0 + 20, y + 34 + i * 60 + j * 22), ('· ' if j == 0 else '   ') + rg,
                    font=G.fnt(G.F_REG, 16), fill=G.MUTED)

    G.legenda(dr, x0, y + 400, [('grigio', 'SIPO'), ('blu', 'concentratore, in locale'),
                                ('viola', 'documenti'), ('giallo', 'verifica locale'),
                                ('rosso', 'chiamata ad ANSC')])
    im = im.crop((0, 0, 1600, y + 450))
    im.save(dest)
    return dest


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'img')
    os.makedirs(out, exist_ok=True)
    print('scritto:', flusso(os.path.join(out, 'flusso_operativo.png')))
