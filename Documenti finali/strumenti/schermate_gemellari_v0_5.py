# -*- coding: utf-8 -*-
"""Ipotesi di schermata, nello stile di SIPO, del caso 1 del parto plurimo (gemelli con lo stesso
UC), analisi delle nascite gemellari v0.5 (21/11/2026). Primitive di `schermate_sipo_wf`.

Decisioni dell'utente (21/11/2026): dopo la divisione una pagina di RIEPILOGO mostra i dati che
il numeratore assegnerà a ciascun gemello, senza riservarli; un solo DEFINISCI stacca i numeri,
prenota gli atti e accompagna un gemello alla volta per anteprima, validazione, firma del
dichiarante, conformità e firma USC, definendo in SIPO ciascun atto subito dopo la sua firma USC;
un errore si riprova o sospende; un parto interrotto si riprende dal riepilogo.

  * gem5_riepilogo.png — il riepilogo dei gemelli, con i numeri comunali previsti;
  * gem5_definisci.png — DEFINISCI in corso: il gemello 1 formato e definito, la firma USC del
                         gemello 2 non riuscita, RIPROVA o SOSPENDI;
  * gem5_ripresa.png   — il riepilogo di un parto interrotto: numeri già staccati, stato letto in
                         ANSC per ciascun gemello, il passo da cui si riprende, RIPRENDI.
Nomi e codici sono di esempio; nessun dato di persone reali.

    /Library/Developer/CommandLineTools/usr/bin/python3 schermate_gemellari_v0_5.py
"""
import os

import schermate_sipo_wf as S

DIR = os.path.join(S.IMG, 'gemellari')
UC = "11111000"
NATI = (("1", "NATO 1 — COGNOME NOME", "M", "Nato vivo", "13617"),
        ("2", "NATO 2 — COGNOME NOME", "F", "Nato vivo", "13618"),
        ("3", "NATO 3 — COGNOME NOME", "F", "Nato vivo", "13619"))


def _colore(testo, colore):
    def scrivi(dr, x, y):
        dr.text((x, y), testo, font=S.f(S.N_BLD, 14), fill=colore)
    return scrivi


FATTO, ERRORE, ATTESA = '#2e6b43', '#b00020', '#7a7a7a'


def _testata(dr, y, gemello="gemello 1 di 3", sessione="OTP valido · 3 h 12 min"):
    y = S.pannello(dr, y, "Atto di nascita – parto plurimo", 112)
    larg = S.W - 2 * S.M - 24
    x = S.M + 12
    for quota, et, val in ((0.26, "Tipo atto", "1429 – gemelli in costanza di matrimonio"),
                           (0.14, "Numero gemelli", "3"), (0.18, "Atto in visione", gemello),
                           (0.20, "Caso d’uso ANSC comune", UC + " – Dic_Nasc_001"),
                           (0.22, "Sessione ANSC", sessione)):
        w = int(larg * quota) - 12
        S.campo(dr, x, y, w, et, val, 'lettura')
        x += w + 12
    return y + 78


def riepilogo(dest):
    im, dr, y = S.pagina("Dichiarazione Nascita – Riepilogo gemelli")
    y = S.avviso(dr, y, "La pratica è stata divisa in 3 atti, uno per ciascun nato. I nati hanno "
                 "lo stesso caso d’uso ANSC: gli atti si prenotano e si formano da SIPO. I numeri "
                 "comunali sono quelli previsti dal numeratore e non sono ancora riservati: si "
                 "staccano con DEFINISCI.", 'info')
    y = _testata(dr, y)
    cols = ("Pos.", "Nato", "Sesso", "Stato del nato", "Caso d’uso ANSC", "N. comunale previsto",
            "Identificativo nazionale", "Stato SIPO")
    larg = (50, 250, 70, 130, 150, 190, 230, 200)
    righe = [(p, n, s, st, UC, num, "—", "1 IN LAVORAZIONE") for p, n, s, st, num in NATI]
    y = S.pannello(dr, y, "Gemelli della pratica – dati che saranno assegnati", 60 + 34 * 4)
    y = S.tabella(dr, y, cols, larg, righe, x=S.M + 12) + 6
    y = S.avviso(dr, y, "DEFINISCI stacca i 3 numeri, prenota in ANSC i 3 atti con il caso d’uso "
                 "comune e poi presenta l’atto di ciascun gemello, uno alla volta, per la "
                 "validazione e per le firme del dichiarante, della conformità e dell’ufficiale. "
                 "Ogni atto firmato dall’ufficiale è definito subito anche in SIPO. Dopo DEFINISCI "
                 "il numero dei gemelli non si può più modificare.", 'attenzione')
    y = S.pulsantiera(dr, y + 8, [("INDIETRO", True)],
                      [("ANTEPRIMA GEMELLI", True), ("DEFINISCI", True)])
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    S.ritaglia(im, y, dest)
    return dest


PASSI = ("Documenti", "Anteprima e validazione", "Firma dichiarante", "Conformità", "Firma USC",
         "Definito in SIPO")


def definisci(dest):
    im, dr, y = S.pagina("Dichiarazione Nascita – Definisci gemelli")
    y = S.avviso(dr, y, "La firma dell’ufficiale sull’atto del gemello 2 non è riuscita: codice "
                 "OTP scaduto (ANSC 406002). Il gemello 1 è formato in ANSC e definito in SIPO. "
                 "L’atto del gemello 2 resta 11 FIRMATO PER CONFORMITÀ: si può riprovare la firma, "
                 "anche con un nuovo codice OTP, oppure sospendere e riprendere più tardi dal "
                 "riepilogo. Il gemello 3 attende.", 'errore')
    y = _testata(dr, y, gemello="gemello 2 di 3", sessione="OTP scaduto")
    cols = ("Pos.", "N. comunale", "Identificativo nazionale") + PASSI + ("Stato ANSC",)
    larg = (46, 104, 232, 92, 168, 132, 100, 92, 132, 196)
    ok, err, att = (_colore("fatto", FATTO), _colore("ERRORE", ERRORE),
                    _colore("in attesa", ATTESA))
    righe = [
        ("1", "13617", "2026-10527618-13617-058091", ok, ok, ok, ok, ok, ok, "5 FIRMATO DA USC"),
        ("2", "13618", "2026-10527619-13618-058091", ok, ok, ok, ok, err, att,
         "11 FIRMATO PER CONF."),
        ("3", "13619", "2026-10527620-13619-058091", att, att, att, att, att, att, "1 BOZZA"),
    ]
    y = S.pannello(dr, y, "Avanzamento del parto – un gemello alla volta", 60 + 34 * 4)
    y = S.tabella(dr, y, cols, larg, righe, x=S.M + 12) + 6
    y = S.pulsantiera(dr, y + 8, [("SOSPENDI", True)],
                      [("NUOVO CODICE OTP", True), ("RIPROVA LA FIRMA", True)])
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    S.ritaglia(im, y, dest)
    return dest


def ripresa(dest):
    im, dr, y = S.pagina("Dichiarazione Nascita – Riepilogo gemelli")
    y = S.avviso(dr, y, "La definizione di questo parto è stata interrotta il 21/11/2026 alle "
                 "11:42. I numeri comunali sono già staccati e gli atti sono già prenotati in "
                 "ANSC: non se ne staccano né se ne prenotano altri. Lo stato di ciascun atto è "
                 "stato riletto in ANSC (R005) all’apertura della pagina.", 'attenzione')
    y = _testata(dr, y)
    cols = ("Pos.", "N. comunale", "Identificativo nazionale", "Stato letto in ANSC",
            "Stato SIPO", "Si riprende da")
    larg = (50, 120, 290, 250, 200, 360)
    righe = [
        ("1", "13617", "2026-10527618-13617-058091", "5 FIRMATO DA USC", "2 DEFINITO",
         _colore("concluso", FATTO)),
        ("2", "13618", "2026-10527619-13618-058091", "11 FIRMATO PER CONFORMITÀ",
         "1 IN LAVORAZIONE", _colore("firma dell’ufficiale", ERRORE)),
        ("3", "13619", "2026-10527620-13619-058091", "1 BOZZA", "1 IN LAVORAZIONE",
         _colore("documenti, dopo il gemello 2", ATTESA)),
    ]
    y = S.pannello(dr, y, "Gemelli della pratica – stato della definizione", 60 + 34 * 4)
    y = S.tabella(dr, y, cols, larg, righe, x=S.M + 12) + 6
    y = S.avviso(dr, y, "RIPRENDI riparte dal primo gemello non concluso, dal passo che il suo "
                 "stato in ANSC indica. RINUNCIA AL PARTO (cancellazione in ANSC degli atti "
                 "prenotati con R011 e scarto dei numeri comunali) è possibile solo finché nessun "
                 "gemello è firmato dall’ufficiale: qui il gemello 1 è già formato.", 'info')
    y = S.pulsantiera(dr, y + 8, [("INDIETRO", True), ("RINUNCIA AL PARTO", False)],
                      [("RIPRENDI", True)])
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    S.ritaglia(im, y, dest)
    return dest


if __name__ == '__main__':
    print(riepilogo(os.path.join(DIR, 'gem5_riepilogo.png')))
    print(definisci(os.path.join(DIR, 'gem5_definisci.png')))
    print(ripresa(os.path.join(DIR, 'gem5_ripresa.png')))
