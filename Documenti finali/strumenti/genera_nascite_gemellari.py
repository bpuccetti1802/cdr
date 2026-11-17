# -*- coding: utf-8 -*-
"""Genera la v0.1 di «ANALISI_Nascite-Gemellari_SIPO-ANSC» (17/11/2026).

Richiesta dell'utente: la gestione degli atti di nascita nei PARTI GEMELLARI, con ciascun
nato vivo, nato morto o nato vivo e poi morto prima della dichiarazione, in SIPO e in ANSC,
e la modalità di integrazione se esiste. Dove servono immagini: segnaposto.

Fatti verificati (rapporti del 17/11 sul codice SIPO e sul repository ANSC):
  SIPO  · tipi atto «un figlio»/«gemelli» sullo stesso Modello (1515/1429 → 30), maschera
          attoNascitaTipo03; 145 tipi atto gemellari su 338, 774 atti su 42.239 nella
          ricognizione dei tipi atto;
        · una pratica con N figli (ATTO_NASCITA.N_TOT_GEMELLI, ATTO_NASCITA_SOGGETTO.POS_GEMELLO),
          divisa in N atti da PKG_PRATICA.CREA_ATTI_NASCITA_FIGLI
          (DettaglioAttiController:641), legati da ATTO.ID_LAVORAZIONE_PADRE;
          undo_atti_nascita_figli; definizione di tutti i gemelli in sequenza
          (AnteprimaAttoController FE:1615-1800), PDF in un secondo giro (runFlowGemelli);
        · FLG_NATO_MORTO/FLG_MORTO_PREDENUNCIA per nato; nato morto fuori dalla famiglia e
          dall'iscrizione ANPR (AllineamentoNascitaAnprSC:224-279); il morto prima della
          denuncia non ha effetti nel Java e va in ANPR come vivo.
  ANSC  · 143 UC di nascita, 108 dichiarazioni in terne 0/1/2 (36+36+36), gruppo 114 solo 0;
        · differenze nella terna: certificato medico, formula 41/40, luogoFiliazione;
        · ModelDatiDiNascita: natoMorto, natoVivoMaDeceduto, partoGemellare, numeroGemelli,
          progressivoGemello, attiGemelliPrec/Succ, tipoNascitaSoggetto (ANSC_107 1/2/3);
          i campi gemellari in nessuno dei 374 mapping;
        · R009 /prenota/evento: numeroGemelliNatiVivi, listaNumeriComunali, idUsecase →
          listaIdEvento, listaIdAnsc; guida cap. 8 p. 41-45; 11999999 non più cooperativo
          dal 09/09/2024.
  Side  · «Processo di Gestione Numeri atti gemellari v1.4» (pulsante PRENOTA GEMELLI,
          tabella atti_gemellari, bozza del gemello successivo).

    /Library/Developer/CommandLineTools/usr/bin/python3 strumenti/genera_nascite_gemellari.py
"""
import os
import shutil
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comune as D   # noqa: E402
from genera_testo_libero import testo, h, par, voce, tabella, _versa   # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(QUI))
TEMPLATE = os.path.join(BASE, 'Template documentale', 'template_DAD_roma-capitale.docx')
NOME = 'ANALISI_Nascite-Gemellari_SIPO-ANSC_v0.1'
OUT = os.path.join(BASE, 'Documenti finali', NOME + '.docx')
TAGLIA_DA = 29
DATA = '17/11/2026'
FIG = [0]


def costruisci():
    shutil.copyfile(TEMPLATE, OUT)
    d = docx.Document(OUT)
    body = d.element.body
    for ch in list(body.iterchildren())[TAGLIA_DA:]:
        if ch.tag != qn('w:sectPr'):
            body.remove(ch)
    for p in d.paragraphs:
        if '“Lorem Ipsum”' in p.text:
            testo(p, '“Integrazione SIPO – ANSC”')
        elif p.style.name == 'Subtitle':
            testo(p, 'Gli atti di nascita nei parti gemellari — nati vivi, nati morti, nati vivi '
                     'e poi deceduti: come li gestisce SIPO, che cosa prevede ANSC e come '
                     'integrarli')
    return d


def segnaposto(d, contenuto, didascalia):
    """Riquadro grigio al posto di un'immagine ancora da produrre, con la didascalia."""
    FIG[0] += 1
    t = d.add_table(rows=1, cols=1)
    t.style = 'Table Grid'
    t.alignment = 1
    cel = t.cell(0, 0)
    cel.width = Inches(6.0)
    cel._tc.get_or_add_tcPr().append(
        parse_xml('<w:shd %s w:val="clear" w:color="auto" w:fill="EDEDED"/>' % nsdecls('w')))
    p = cel.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('[IMMAGINE DA INSERIRE]')
    r.bold = True
    r.font.size = Pt(10)
    p2 = cel.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _versa(p2, contenuto, dim=9, corsivo=True)
    for _ in range(3):
        cel.add_paragraph()
    cap = d.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _versa(cap, 'Figura %d – %s' % (FIG[0], didascalia), dim=9, corsivo=True)


# =================================================================== tabelle
GLOSSARIO = [
    ['Termine', 'Significato', 'Nota'],
    ['Parto plurimo (gemellare, plurigemellare)', 'Parto da cui nascono due o più figli.',
     'In SIPO si sceglie un tipo atto «gemelli»; in ANSC si usa la prenotazione degli atti.'],
    ['Nato vivo', 'Il nato che presenta segni di vita alla nascita e non muore prima della '
     'dichiarazione.', 'SIPO: nessun flag. ANSC: 6ª cifra dell’UC = 0; ANSC_107 = 1.'],
    ['Nato morto', 'Il nato privo di segni di vita alla nascita.', 'SIPO: FLG_NATO_MORTO = S. '
     'ANSC: 6ª cifra = 1; ANSC_107 = 2; natoMorto = SI.'],
    ['Nato vivo e poi deceduto («morto dopo»)', 'Il nato vivo che muore prima che la nascita '
     'sia dichiarata.', 'SIPO: FLG_MORTO_PREDENUNCIA = S («Morto prima della denuncia»). ANSC: '
     '6ª cifra = 2; ANSC_107 = 3; natoVivoMaDeceduto = SI.'],
    ['Pratica (SIPO)', 'La lavorazione unica in cui si raccolgono i dati di tutti i gemelli '
     'prima della divisione.', 'Una riga di ATTO_NASCITA con N righe di ATTO_NASCITA_SOGGETTO.'],
    ['Divisione', 'Il passo con cui SIPO trasforma la pratica in N atti, uno per nato.',
     'PKG_PRATICA.CREA_ATTI_NASCITA_FIGLI.'],
    ['Prenotazione (ANSC)', 'Il servizio che crea in un colpo gli atti di tutti i gemelli e ne '
     'restituisce gli identificativi.', 'R009 /prenota/evento.'],
    ['idAnsc', 'Identificativo nazionale dell’atto.', 'Assegnato da ANSC.'],
    ['UC', 'Caso d’uso di ANSC: codice numerico che compone le scelte fatte (registro, tipo, '
     'dichiarante, stato del nato…).', 'Es. 11111000 = Dic_Nasc_001.'],
    ['Modello', 'Struttura del Comune di Roma che lega il tipo atto alla maschera.',
     'CONF_TIPO_ATTI.ID_MODELLO_ATTO.'],
    ['USC', 'Ufficiale dello stato civile.', ''],
]

RIFERIMENTI = [
    ['#', 'Riferimento', 'Natura'],
    ['[R1]', 'ANALISI_Integrazione-ANSC (versione corrente) — concentratore all-ansc-sipo, '
     'store ANSC_STATO_ATTO, prenotazione per il parto plurimo, OP-31 e OP-46.',
     'Documento di progetto'],
    ['[R2]', 'ANALISI_Atti-Testo-Libero_SIPO-ANSC (versione corrente) — la strategia per gli '
     'atti che si formano sulla web app: compilazione in SIPO, stacco del numero, ritorno con '
     'DEFINISCI.', 'Documento di progetto'],
    ['[R3]', 'PROCESSO_Numerazione-Comunale_SIPO-ANSC (versione corrente) e '
     'ansc-numerazione-v1.yaml — il servizio be-numeratore-comunale.', 'Documento di progetto'],
    ['[R4]', 'MAPPA_Nascite_Schermate-Servizi-Tabelle_v0.1 — schermate, servizi e tabelle '
     'dell’area nascite.', 'Documento di analisi'],
    ['[M1]', 'CdMI SIDe MI_ANSC — Processo di Gestione Numeri atti gemellari v1.4 (Comune di '
     'Milano, 18/03/2024).', 'Sorgente documentale'],
    ['[M2]', 'Nascite_ANSC_07.08.2026.xlsx — ricognizione UC ↔ tipi atto e Modelli delle '
     'nascite; ricognizione dei tipi atto con la frequenza d’uso.', 'Sorgente documentale'],
    ['[A1]', 'ansc/docs/openapi/R009_validazione.yaml, v1.4.0 — /prenota/evento (righe '
     '103-137, 194-232).', 'Contratto ANSC'],
    ['[A2]', 'ansc/docs/openapi/model_evento.yaml — ModelDatiDiNascita (righe 1547-1583).',
     'Contratto ANSC'],
    ['[A3]', 'Guida operativa ANSC, cap. 8 «parto gemellare e plurigemellare», p. 41-45.',
     'Guida ANSC'],
    ['[A4]', 'ansc/docs/Mapping_casi_uso — 3_dec_use_case.csv e cartella nascita/ (143 UC); '
     'Dic_Nasc_999.csv.', 'Sorgente ANSC'],
    ['[A5]', 'ansc/docs/Decodifiche — ANSC_03 casi d’uso, ANSC_11 stati, ANSC_107 tipo stato '
     'di nascita.', 'Sorgente ANSC'],
    ['[A6]', 'ansc/docs/Changelog.md e changelog_mapping — 1.0.2, 1.9.0, 1.23.0, 1.23.1, '
     '1.26.0, 1.33.0.', 'Sorgente ANSC'],
    ['[A7]', 'Comunicazione ANSC sui casi d’uso di servizio tramite servizi cooperativi '
     '(Sorgenti Documentali, = voce «ID 120» del rilascio 1.33.0).', 'Comunicazione ANSC'],
    ['[A8]', 'ansc/docs/CasiTest/payload_test/R009_prenotazione_numeri_parti_gemellari.json.',
     'Sorgente ANSC'],
    ['[S1]', 'front-end/nascita-web, back-end/nascita-be — maschere attoNascitaTipo01/03/04/07, '
     'frammenti gemello01…10, SalvataggioController, RicercaController.',
     'Sorgente applicativo'],
    ['[S2]', 'front-end/statocivile-web, back-end/statocivile-be — DettaglioAttoStatoCivile, '
     'AnteprimaAttoController, DettaglioAttiController, AttoNasciteFlow.',
     'Sorgente applicativo'],
    ['[S3]', 'common/matrim-entities — AttoMatr, AttoNascita, AttoNascitaSoggetto, '
     'AttoMatrRepository.', 'Sorgente applicativo'],
    ['[S4]', 'back-end/all-anpr-sipo — AllineamentoNascitaAnprSC, ConvertSC, Constant.',
     'Sorgente applicativo'],
]

TRE_STATI = [
    ['Aspetto', 'Nato vivo', 'Nato morto', 'Nato vivo e poi deceduto'],
    ['SIPO — come si indica', 'Nessun flag.', 'Casella «Nato morto» → FLG_NATO_MORTO = S.',
     'Casella «Morto prima della denuncia» → FLG_MORTO_PREDENUNCIA = S.'],
    ['SIPO — dove sta', '—', 'ATTO_NASCITA_SOGGETTO, per singolo nato.',
     'ATTO_NASCITA_SOGGETTO, per singolo nato.'],
    ['SIPO — quando è disponibile', '—', 'Solo nell’iscrizione da pubblico ufficiale; nella '
     'trascrizione da ospedale il flag è forzato a N.', 'Come per il nato morto.'],
    ['ANSC — UC', '6ª cifra 0 (es. 11111000, Dic_Nasc_001).',
     '6ª cifra 1 (es. 11111100, Dic_Nasc_002).', '6ª cifra 2 (es. 11111200, Dic_Nasc_003).'],
    ['ANSC — modello evento', 'natoMorto = NO, natoVivoMaDeceduto = NO.', 'natoMorto = SI.',
     'natoVivoMaDeceduto = SI.'],
    ['ANSC — ANSC_107 (tipoNascitaSoggetto)', '1 nato vivo', '2 nato morto',
     '3 nato vivo ma successivamente deceduto'],
    ['ANSC — allegato obbligatorio in più', '—', 'Certificato medico attestante che il bambino '
     'è nato morto.', 'Certificato medico attestante che il bambino è nato vivo e poi '
     'deceduto.'],
    ['ANSC — formula caratteristica', 'Formula 1.', 'Formula 41 (senza la formula 1).',
     'Formula 40 (con la formula 1).'],
    ['ANSC — luogo di filiazione', 'Obbligatorio.', 'Obbligatorio.', 'Facoltativo.'],
    ['ANPR (SIPO oggi)', 'Iscrizione 1001, o A001 se AIRE.', 'Nessuna chiamata: flusso '
     '«occasionale», stato del soggetto «nato morto».', 'Iscrizione come nato vivo; nessuna '
     'cancellazione legata al flag.'],
    ['Famiglia anagrafica (SIPO)', 'Entra nei rapporti di parentela.', 'Escluso.',
     'Entra come il nato vivo.'],
]

SIPO_TIPI = [
    ['Gruppo di tipi atto (cluster)', 'Un figlio', 'Gemelli', 'Modello'],
    ['Dichiarazione da pubblico ufficiale nei termini, in costanza di matrimonio',
     '1515 … 1521', '1429 … 1435', '30 … 36 (lo stesso per i due tipi)'],
    ['Dichiarazione da pubblico ufficiale tardiva, in costanza di matrimonio',
     '1703 … 1709', '1673 … 1679', 'Lo stesso per i due tipi'],
    ['Dichiarazione da pubblico ufficiale nei termini, fuori dal matrimonio',
     '1551 … 1563', '1437 … 1458', 'Lo stesso per i due tipi'],
    ['Dichiarazione tardiva, fuori dal matrimonio', '1712, 1720 … 1723',
     '1688 … 1691, 1702', 'Lo stesso per i due tipi'],
    ['Gemelli abbandonati', '—', '1522, 1710', '—'],
    ['Maschera (MASCHERA_UI)', 'attoNascitaTipo01', 'attoNascitaTipo03 (e Tipo04, Tipo07, '
     'testo libero)', ''],
]

SIPO_FREQ = [
    ['Tipo atto', 'Modello', 'Descrizione', 'Atti nella ricognizione'],
    ['1429', '30', 'Iscrizione da pubblico ufficiale, gemelli nati in costanza di matrimonio',
     '221'],
    ['1608', '06', 'Trascrizione da ospedale, gemelli nati fuori dal matrimonio', '155'],
    ['1601', '01', 'Trascrizione da ospedale, gemelli nati in costanza di matrimonio', '144'],
    ['1449', '49', 'Iscrizione da pubblico ufficiale, gemelli nati fuori dal matrimonio', '82'],
    ['1437', '38', 'Iscrizione da pubblico ufficiale, gemelli nati fuori dal matrimonio', '44'],
    ['1438', '39', 'Iscrizione da pubblico ufficiale, gemelli nati fuori dal matrimonio', '44'],
    ['1602', '02', 'Trascrizione da ospedale, gemelli nati in costanza di matrimonio', '28'],
    ['Altri 138', '', 'Ciascuno con 12 atti o meno', '56'],
    ['Totale', '', '145 tipi atto gemellari su 338 dell’area nascite', '774 su 42.239'],
]

SIPO_TABELLE = [
    ['Tabella (MATR_USR)', 'Colonna', 'Ruolo nel parto plurimo'],
    ['ATTO_NASCITA', 'N_TOT_GEMELLI', 'Numero dei nati, scelto nella tendina «Numero Gemelli» '
     '(da 2 a 10).'],
    ['ATTO_NASCITA', 'FLG_PARTO_PLURIMO', 'Indicatore del parto plurimo. Lo leggono i servizi '
     'dei gemelli successivo e precedente; nel codice Java nessuno lo scrive, quindi lo '
     'valorizza la base dati.'],
    ['ATTO_NASCITA_SOGGETTO', 'POS_GEMELLO', 'Posizione del nato, da 1 a N; valorizzata solo '
     'se i figli sono più di uno.'],
    ['ATTO_NASCITA_SOGGETTO', 'FLG_PRIMO_FIGLIO', 'Per i tipi atto dei gemelli è spuntato e '
     'non modificabile (dalla ricognizione [M2]).'],
    ['ATTO_NASCITA_SOGGETTO', 'DATAORARIO_NASCITA', 'Data e ora del singolo nato: è ciò che '
     'distingue l’ordine di nascita.'],
    ['ATTO_NASCITA_SOGGETTO', 'FLG_NATO_MORTO, FLG_MORTO_PREDENUNCIA', 'Stato del singolo '
     'nato.'],
    ['ATTO_NASCITA_SOGGETTO', 'CODICE_FAMIGLIA, ID_CODICE_LEGAME, ID_ATTRIBUZIONE_FAMIGLIA',
     'Famiglia anagrafica, applicata a tutti i figli non nati morti.'],
    ['ATTO', 'ID_LAVORAZIONE_PADRE', 'Dopo la divisione, punta all’ID_ATTO del primo atto: è '
     'il legame fra i gemelli.'],
    ['ATTO', 'NUMERO_ATTO, PARTE, SERIE, ESPONENTE, ID_STATO_PRATICA', 'Numerazione e stato '
     'di ciascun atto.'],
]

SIPO_SERVIZI = [
    ['Momento', 'Servizio', 'Che cosa fa'],
    ['Compilazione', 'nascita-be /findAndDeleteFiglio', 'Elimina i figli di posizione più '
     'alta se l’operatore riduce il numero dei gemelli.'],
    ['Riepilogo', 'statocivile-be /performAttiPlurigemellari', 'Esegue '
     'PKG_PRATICA.CREA_ATTI_NASCITA_FIGLI: la pratica diventa N atti.'],
    ['Anteprima', '/checkPartoPlurimoAndGemSucc, /checkPartoPlurimoAndGemPrec', 'Dicono se '
     'esiste un gemello successivo o precedente (FLG_PARTO_PLURIMO = S).'],
    ['Anteprima', '/getNextATTONascitaGemello', 'PKG_PRATICA.getNextATTONascitaGemello: '
     'l’atto del gemello successivo.'],
    ['Anteprima, «indietro»', '/undoAttiNascitaFigli', 'PKG_PRATICA.undo_atti_nascita_figli: '
     'annulla la divisione (non per il testo libero).'],
    ['Definizione', '/finalizzaAtto, una chiamata per gemello', 'Definisce gli atti in '
     'sequenza (DEFINISCI GEMELLI).'],
    ['Definizione', '/generaPDFAttoFromFormularioGemelli', 'Genera i PDF in un secondo giro, '
     'quando tutti gli atti sono numerati (AttoNasciteFlow.runFlowGemelli).'],
    ['Allineamento', 'all-anpr-sipo /allineamentoNascitaSC, una chiamata per atto',
     'Iscrizione anagrafica dei nati vivi.'],
]

ANSC_UC = [
    ['Gruppo di UC di nascita', 'UC', '6ª cifra 0', '6ª cifra 1', '6ª cifra 2'],
    ['Dichiarazioni (gruppi 111, 112, 113)', '108', '36', '36', '36'],
    ['Riconosciuti prima della nascita (gruppo 114)', '22', '22', '—', '—'],
    ['Caso d’uso di servizio (11999999, Dic_Nasc_999)', '1', '', '', ''],
    ['Annotazioni (144 … 149)', '12', '', '', ''],
    ['Totale cartella nascita/', '143', '', '', ''],
]

ANSC_TERNA = [
    ['Riga del mapping', '11111000 Dic_Nasc_001 (vivo)', '11111100 Dic_Nasc_002 (nato morto)',
     '11111200 Dic_Nasc_003 (vivo poi deceduto)'],
    ['Allegato «Certificato medico … nato morto»', '—', 'Obbligatorio', '—'],
    ['Allegato «Certificato medico … nato vivo e poi deceduto»', '—', '—', 'Obbligatorio'],
    ['Formula 1', 'Sì', '—', 'Sì'],
    ['Formula 41', '—', 'Sì', '—'],
    ['Formula 40', '—', '—', 'Sì'],
    ['evento.datiDiNascita.luogoFiliazione', 'Obbligatorio', 'Obbligatorio', 'Facoltativo'],
]

ANSC_CAMPI = [
    ['Campo di ModelDatiDiNascita', 'Significato', 'Nei 374 mapping'],
    ['partoGemellare', 'SI / NO.', 'Assente'],
    ['numeroGemelli', 'Numero totale dei gemelli nati.', 'Assente'],
    ['progressivoGemello', 'Posizione del nato fra i gemelli.', 'Assente'],
    ['attiGemelliPrec[]', 'Identificativi nazionali degli atti dei gemelli precedenti.',
     'Assente'],
    ['attiGemelliSucc[]', 'Identificativi nazionali degli atti dei gemelli successivi.',
     'Assente'],
    ['natoMorto', 'SI / NO.', 'In 130 mapping, facoltativo'],
    ['natoVivoMaDeceduto', 'SI / NO.', 'In 130 mapping, facoltativo'],
    ['tipoNascitaSoggetto', 'Decodifica ANSC_107: 1 vivo, 2 nato morto, 3 vivo poi deceduto.',
     'Solo in Dic_Nasc_999 (caso d’uso di servizio)'],
]

PRENOTA = [
    ['Elemento', 'Contenuto', 'Osservazioni'],
    ['Percorso', 'POST /prenota/evento/{version}', 'Terza operazione di R009, accanto alla '
     'validazione e al collegamento.'],
    ['Richiesta: numeroGemelliNatiVivi', 'Numero dei gemelli nati vivi (stringa).',
     'Obbligatorio. Il nome dice «nati vivi», mentre numeroGemelli del modello dice «il numero '
     'totale dei gemelli nati».'],
    ['Richiesta: listaNumeriComunali[]', 'Il numero comunale di ciascun gemello.',
     'Obbligatorio. I numeri vanno quindi staccati prima della prenotazione.'],
    ['Richiesta: idUsecase', 'Il caso d’uso.', 'Obbligatorio e unico per tutta la chiamata. '
     'Il payload di test usa 11111000, l’esempio del contratto «1170».'],
    ['Risposta: listaIdEvento[]', 'Gli identificativi interni degli eventi creati.', ''],
    ['Risposta: listaIdAnsc[]', 'Gli identificativi nazionali degli atti creati.',
     'Sono quelli da scrivere nell’atto di ciascun gemello e negli elenchi dei fratelli.'],
    ['Stato degli atti creati', 'La guida li chiama «eventi in bozza» e li fa recuperare con '
     '«Recupero evento in bozza» o per identificativo nazionale.', 'Il contratto non dichiara '
     'lo stato; nessuna fonte cita esplicitamente ANSC_11 = 1.'],
]

CONFRONTO = [
    ['Aspetto', 'SIPO oggi', 'ANSC', 'Conseguenza per l’integrazione'],
    ['Unità di lavoro', 'Una pratica con N figli, poi N atti.', 'N atti fin dalla '
     'prenotazione.', 'La divisione di SIPO è il punto naturale in cui prenotare.'],
    ['Legame fra gli atti', 'ATTO.ID_LAVORAZIONE_PADRE verso il primo atto.',
     'attiGemelliPrec[] e attiGemelliSucc[] in ciascun atto, con gli idAnsc.', 'Gli elenchi '
     'si calcolano dal legame di SIPO; servono gli idAnsc di tutti prima di validare il primo.'],
    ['Ordine dei gemelli', 'POS_GEMELLO nella pratica; dopo la divisione l’ordine delle query '
     'è quello di ID_ATTO.', 'progressivoGemello.', 'Va fissata una regola unica: ordine di '
     'nascita = POS_GEMELLO = progressivoGemello.'],
    ['Numerazione', 'Numero provvisorio, definitivo alla definizione; logica nei pacchetti '
     'PL/SQL.', 'I numeri comunali di tutti i gemelli entrano nella prenotazione.',
     'Stacco in blocco da be-numeratore-comunale prima della prenotazione.'],
    ['Stato del singolo nato', 'Due flag per nato.', 'UC diverso per stato (6ª cifra); '
     'natoMorto, natoVivoMaDeceduto, tipoNascitaSoggetto.', 'Un parto misto produce atti con '
     'UC diversi, mentre la prenotazione ne accetta uno solo.'],
    ['Testo dell’atto', 'Formulario in base dati, composto quando tutti gli atti hanno il '
     'numero.', 'Minuta (composizioneCompleta) con le formule ministeriali e gli '
     'identificativi dei gemelli scritti dall’ufficiale.', 'Il testo va composto dopo la '
     'prenotazione.'],
    ['Firma del dichiarante', 'Cartacea.', 'Solo cartacea per i parti gemellari, acquisita '
     'come processo verbale.', 'Nessun cambiamento di prassi.'],
    ['Definizione', 'Tutti i gemelli in sequenza, con un solo comando.', 'Un gemello alla '
     'volta: si passa al successivo dopo la firma dell’USC.', 'Il comando unico va spezzato '
     'in N finalizzazioni, ciascuna con la propria firma.'],
    ['Anagrafe', 'Iscrizione ANPR dei nati vivi, per atto; nato morto escluso.',
     'Comunicazione anagrafica generata da ANSC.', 'Chi comunica con ANPR per un atto '
     'formato in ANSC è un tema dell’analisi di integrazione [R1], non specifico dei gemelli.'],
]

PASSI_A = [
    ['#', 'Pagina o momento in SIPO', 'Che cosa succede', 'Servizi', 'Esito'],
    ['1', 'Compilazione della pratica (maschera dei gemelli)', 'Come oggi: dati dei genitori, '
     'numero dei gemelli, dati di ciascun nato con i due flag.', 'nascita-be', 'Pratica '
     'salvata.'],
    ['2', 'Riepilogo → Conferma', 'Come oggi: la pratica è divisa in N atti.',
     '/performAttiPlurigemellari', 'N atti in SIPO legati da ID_LAVORAZIONE_PADRE.'],
    ['3', 'Riepilogo del gemello 1 → PRENOTA GEMELLI (nuovo)', 'Si determinano gli UC dei '
     'singoli nati e si chiedono N numeri comunali consecutivi; poi si chiama la prenotazione.',
     'be-numeratore-comunale POST /richiesta; all-ansc-sipo → R009 /prenota/evento',
     'N righe in ANSC_STATO_ATTO in BOZZA, ciascuna con numero comunale e idAnsc; righe in '
     'ATTI_GEMELLARI.'],
    ['4', 'Anteprima del gemello k', 'Il testo riporta gli identificativi dei fratelli; il '
     'concentratore valorizza i campi gemellari e lo stato del nato.', 'all-ansc-sipo',
     'Modello evento completo.'],
    ['5', 'Validazione del gemello k', 'R009 sulla bozza prenotata (con quale campo: OP-46).',
     'R009 /validazione/evento', 'Atto CONFERMATO.'],
    ['6', 'Firme del gemello k', 'Firma cartacea del dichiarante acquisita come processo '
     'verbale; firma dell’USC.', 'R001 / R006, R007', 'Atto FIRMATO DA USC; definizione in '
     'SIPO del solo gemello k.'],
    ['7', 'GEMELLO SUCCESSIVO', 'Si ripetono i passi 4-6 per il gemello k+1.',
     '/getNextATTONascitaGemello', 'Fino all’ultimo gemello.'],
    ['8', 'Chiusura', 'Allineamento anagrafico secondo [R1]; atti prenotati e non usati chiusi '
     'con R011 e numero comunale scartato.', 'R011, PUT /scarta', 'Nessuna bozza aperta in '
     'ANSC.'],
]

PASSI_B = [
    ['#', 'Dove', 'Che cosa succede'],
    ['1', 'SIPO', 'Compilazione e divisione come oggi (passi 1 e 2 del percorso A).'],
    ['2', 'SIPO', 'Stacco dei numeri comunali dei gemelli, in blocco, prima di andare sulla web '
     'app.'],
    ['3', 'SIPO, pagina «Dati per ANSC»', 'L’ufficiale vede, per ciascun gemello, i dati da '
     'riportare; lo store registra gli atti nello stato WA · ATTESA WEBAPP [R2].'],
    ['4', 'Web app ANSC', 'Prenotazione con i numeri staccati, completamento e firma di '
     'ciascun gemello, come prescrive la guida [A3].'],
    ['5', 'SIPO, DEFINISCI su ciascun gemello', 'Aggancio all’atto ANSC (R005 per numero '
     'comunale o idAnsc), verifica dell’abbinamento, definizione dell’atto in SIPO.'],
]

ATTI_GEMELLARI = [
    ['Colonna', 'Tipo', 'Da Side', 'Note'],
    ['id_atto_gemellare', 'NUMBER (PK)', 'No', 'Chiave tecnica della riga (IDENTITY).'],
    ['id_richiesta_prenotazione', 'NUMBER', 'Sì', 'Raggruppa i gemelli di un parto: una '
     'prenotazione R009.'],
    ['id_lavorazione_padre', 'NUMBER', 'No', 'ATTO.ID_LAVORAZIONE_PADRE di SIPO: la pratica '
     'di origine.'],
    ['id_atto_sipo', 'NUMBER', 'Sì, come id_evento', 'L’atto SIPO del gemello.'],
    ['ty_use_case', 'VARCHAR2(10)', 'Sì', 'UC del singolo gemello.'],
    ['nr_gemelli', 'NUMBER(2)', 'Sì', 'Numero totale dei gemelli.'],
    ['nr_progressivo_gemello', 'NUMBER(2)', 'Sì', 'Posizione del gemello = POS_GEMELLO = '
     'progressivoGemello.'],
    ['nr_atto_comunale', 'NUMBER(6)', 'No', 'Numero comunale staccato per il gemello.'],
    ['fg_stesura_atto', 'CHAR(1)', 'Sì', '0 da stendere, 1 steso.'],
    ['cd_operatore', 'VARCHAR2(40)', 'Sì', 'Chi ha fatto la prenotazione.'],
    ['ts_operazione', 'TIMESTAMP', 'Sì', 'Quando.'],
]

ADATTAMENTI = [
    ['Scelta di Side', 'Per Roma', 'Ragione'],
    ['Colonna id_evento (chiave dell’atto di Side).', 'id_atto_sipo.', 'SIPO non ha la tabella '
     'evento di Side: l’atto è ATTO di MATR_USR.'],
    ['Colonne idAnsc, atti_gemelli_prec, atti_gemelli_succ.', 'Non si registrano.',
     'L’idAnsc sta già in ANSC_STATO_ATTO (un dato, un posto). I due elenchi si calcolano '
     'dalle righe dello stesso parto ordinate per progressivo: registrarli darebbe una seconda '
     'copia che può divergere.'],
    ['Colonna cd_ente.', 'Non si registra.', 'Roma è l’unico ente.'],
    ['—', 'id_lavorazione_padre e nr_atto_comunale.', 'Il legame con la pratica SIPO e con il '
     'numero staccato.'],
    ['Campi fg_parto_gemellare, nr_gemelli, nr_progressivo_gemello sulla tabella dei dati di '
     'nascita.', 'Non si aggiungono a SIPO.', 'SIPO li ha già: FLG_PARTO_PLURIMO, N_TOT_GEMELLI, '
     'POS_GEMELLO.'],
    ['Bozza del gemello successivo creata copiando i dati del primo.', 'Non serve.', 'In SIPO '
     'la pratica unica raccoglie già i dati comuni e la divisione crea tutti gli atti.'],
]

OPEN = [
    ['#', 'Tema', 'Questione', 'Stato'],
    ['GE-01', 'Completamento da gestionale', 'La guida dice che i gemelli si completano con un '
     'caso d’uso di servizio, e il caso di servizio delle nascite (11999999) non è più '
     'disponibile tramite servizi cooperativi dal 09/09/2024 [A7]. Il payload di test della '
     'prenotazione usa invece 11111000. Va chiesto a Sogei se la prenotazione e il '
     'completamento delle bozze con l’UC ordinario del singolo nato siano possibili da '
     'gestionale. Decide fra il percorso A e il percorso B. Coincide in parte con OP-46 [R1].',
     'Aperto'],
    ['GE-02', 'Riconoscimento della bozza', 'Con quale campo la validazione riconosce l’atto '
     'già creato dalla prenotazione (id o idAnsc). Un errore produce un duplicato, non un '
     'errore. È OP-46 [R1]; da provare in preproduzione.', 'Aperto'],
    ['GE-03', 'Nati morti nella prenotazione', 'Il campo della richiesta è '
     'numeroGemelliNatiVivi. Va chiarito se un gemello nato morto si prenota insieme agli altri '
     'o si forma a parte, e se compare negli elenchi dei fratelli.', 'Aperto'],
    ['GE-04', 'Parto misto e UC unico', 'La prenotazione accetta un solo idUsecase, ma in un '
     'parto con un gemello vivo e uno nato morto gli UC dei due atti sono diversi (es. '
     '11111000 e 11111100). Va chiarito quale UC passare e se l’UC della bozza si possa '
     'cambiare al completamento.', 'Aperto'],
    ['GE-05', 'Nato vivo e poi deceduto: atto di morte', 'Le fonti ANSC non dicono se per l’UC '
     'di nato vivo poi deceduto si formi anche un atto di morte, né con quale UC. In SIPO il '
     'flag non ha effetti e non c’è legame con l’area decessi. Va accertata la prassi '
     'dell’ufficio e chiesto a Sogei.', 'Aperto'],
    ['GE-06', 'Nato vivo e poi deceduto: anagrafe', 'Oggi SIPO iscrive il nato in ANPR come '
     'vivo e non lo cancella. Va accertato come si chiude la posizione anagrafica e se con '
     'ANSC la comunicazione anagrafica la gestisca.', 'Aperto'],
    ['GE-07', 'Corpi dei pacchetti PL/SQL', 'CREA_ATTI_NASCITA_FIGLI, getNextATTONascitaGemello, '
     'undo_atti_nascita_figli, get_temp_numatto, CompletaATTO e PKG_FORMULARI non sono fra le '
     'sorgenti: senza, non si sa come SIPO numera i gemelli, quali dati copia fra gli atti e '
     'come le formule citano gli altri gemelli. Da chiedere al DBA.', 'Aperto'],
    ['GE-08', 'Ordine dei gemelli', 'Dopo la divisione SIPO ordina i gemelli per ID_ATTO, non '
     'per POS_GEMELLO. Per ANSC progressivoGemello e gli elenchi dei fratelli devono seguire '
     'l’ordine di nascita: va verificato che CREA_ATTI_NASCITA_FIGLI crei gli atti in quell’'
     'ordine.', 'Aperto'],
    ['GE-09', 'Annullamento della divisione', 'Oggi il pulsante «indietro» dell’anteprima '
     'annulla la divisione. Dopo la prenotazione gli atti esistono in ANSC: l’annullamento '
     'della divisione deve chiudere le bozze con R011 e scartare i numeri, oppure va '
     'impedito.', 'Aperto'],
    ['GE-10', 'Formule ministeriali', 'La guida cita le formule 35, 36, 37 per il parto '
     'gemellare, che non compaiono in nessun mapping. Va stabilito come la minuta le '
     'riporti e come il formulario di SIPO vi si allinei.', 'Aperto'],
    ['GE-11', 'Trascrizioni da ospedale', 'I tipi atto più usati dopo il 1429 sono '
     'trascrizioni da ospedale di gemelli (1608, 1601, 1602), dove SIPO forza i due flag a N. '
     'Va verificato a quali UC ANSC corrispondano e se la prenotazione valga anche per loro.',
     'Aperto'],
    ['GE-12', 'Sessione OTP', 'Un parto trigemino richiede tre finalizzazioni consecutive con '
     'tre firme dell’USC: la soglia di guardia della sessione va valutata sull’intera '
     'lavorazione [R1].', 'Aperto'],
]


# =================================================================== testo
def scrivi(d):
    # ------------------------------------------------------------ 1
    h(d, 1, 'Scopo e perimetro')
    par(d, 'Il documento descrive come si formano gli atti di nascita quando il parto è '
           'plurimo e ciascun nato può essere nato vivo, nato morto oppure nato vivo e poi '
           'deceduto prima della dichiarazione. Per ognuno dei due sistemi coinvolti — SIPO, il '
           'gestionale del Comune, e ANSC, l’Anagrafe Nazionale dello Stato Civile — riporta '
           'come il caso è trattato oggi, e poi individua se e come i due possano essere '
           'integrati.')
    par(d, 'Il perimetro sono le **dichiarazioni di nascita** con più nati. Il nato singolo vi '
           'compare solo come termine di confronto. Le trascrizioni da ospedale sono richiamate '
           'dove i dati lo richiedono, ma la loro corrispondenza con gli UC di ANSC resta un '
           'punto aperto (GE-11).')
    par(d, 'Ogni affermazione è ricondotta a una fonte. Dove le fonti tacciono il documento lo '
           'dice e apre un punto, invece di colmare con ipotesi. Le figure non ancora prodotte '
           'sono indicate con un riquadro segnaposto che ne descrive il contenuto.')
    h(d, 2, 'Glossario')
    tabella(d, GLOSSARIO, [1.7, 2.6, 2.3])
    h(d, 2, 'Riferimenti')
    tabella(d, RIFERIMENTI, [0.6, 4.6, 1.4])

    # ------------------------------------------------------------ 2
    h(d, 1, 'In sintesi')
    voce(d, 'In SIPO il parto plurimo è un tipo atto a sé.', 'Si compila una sola pratica con '
         'tutti i nati, che al riepilogo viene divisa in un atto per nato; i gemelli si '
         'definiscono poi con un comando unico. Lo stato del nato (vivo, nato morto, morto '
         'prima della denuncia) è un dato di ciascun gemello, quindi lo stesso parto può '
         'contenerli tutti e tre.')
    voce(d, 'In ANSC i gemelli sono atti distinti che si citano a vicenda.', 'Ciascun atto '
         'riporta gli identificativi nazionali dei fratelli, e un atto depositato non si '
         'aggiorna. Per questo ANSC offre la prenotazione (R009 /prenota/evento): crea in una '
         'chiamata gli atti di tutti i gemelli, che poi si completano e si firmano uno alla '
         'volta. Lo stato del nato cambia l’UC: la 6ª cifra vale 0, 1 o 2.')
    voce(d, 'L’integrazione esiste nel contratto, ma la sua praticabilità non è accertata.',
         'La guida fa completare i gemelli con un caso d’uso di servizio, e il caso di '
         'servizio delle nascite non è più accettato tramite servizi cooperativi dal 9 '
         'settembre 2024. Il documento propone quindi due percorsi: **A**, tutto da SIPO, se '
         'Sogei conferma che le bozze prenotate si completano con l’UC ordinario del singolo '
         'nato; **B**, prenotazione e firme sulla web app con ritorno in SIPO, che è la '
         'strategia già adottata per gli atti che SIPO non può formare [R2]. La scelta dipende '
         'da GE-01.')
    voce(d, 'Tre questioni restano senza risposta nelle fonti.', 'Se un gemello nato morto si '
         'prenoti insieme ai vivi (GE-03), quale UC si passi alla prenotazione di un parto '
         'misto (GE-04) e che cosa avvenga, in ANSC e in anagrafe, per il nato vivo e poi '
         'deceduto (GE-05, GE-06).')

    # ------------------------------------------------------------ 3
    h(d, 1, 'I tre stati del nato')
    par(d, 'Il parto plurimo moltiplica gli atti, ma ciascun atto resta quello di un solo nato, '
           'con il suo stato. La tabella mette a confronto come i due sistemi rappresentano i tre '
           'stati e che cosa ne discende.')
    tabella(d, TRE_STATI, [1.5, 1.6, 1.8, 1.8])
    par(d, 'Due osservazioni. La prima: le due rappresentazioni non coincidono. SIPO usa due '
           'flag indipendenti, ANSC un codice a tre valori (la 6ª cifra dell’UC, e in parallelo '
           'la decodifica ANSC_107, che però numera da 1 a 3). La combinazione dei due flag '
           'entrambi a S non ha corrispondente in ANSC e va respinta prima del deposito. La '
           'seconda: il nato morto e il nato vivo poi deceduto differiscono in ANSC per un '
           'allegato obbligatorio — il certificato medico che attesta lo stato — che in SIPO '
           'non ha oggi un posto. Gli allegati sono trattati dall’analisi di integrazione [R1].')

    # ------------------------------------------------------------ 4
    h(d, 1, 'SIPO oggi')
    h(d, 2, 'I tipi atto e le maschere')
    par(d, 'Ogni tipo atto di nascita ha un gemello «gemelli»: la ricognizione [M2] li elenca a '
           'coppie, per esempio 1515 (un figlio) e 1429 (gemelli). I due tipi condividono il '
           'Modello e differiscono per la maschera: attoNascitaTipo01 per il figlio unico, '
           'attoNascitaTipo03 per i gemelli. Le maschere dei gemelli (Tipo03, Tipo04 per i '
           'gemelli abbandonati, Tipo07 e quella a testo libero) portano la tendina «Numero '
           'Gemelli», da 2 a 10, e un frammento di dati per ciascun nato (gemello01 … '
           'gemello10).')
    tabella(d, SIPO_TIPI, [2.6, 1.2, 1.6, 1.3])
    par(d, 'I numeri d’uso, dalla ricognizione dei tipi atto: **145 tipi atto gemellari su 338** '
           'dell’area nascite, per **774 atti su 42.239** (circa l’1,8 per cento). L’uso si '
           'concentra su pochi tipi.')
    tabella(d, SIPO_FREQ, [0.9, 0.8, 3.6, 1.4])
    segnaposto(d, 'Schermata di SIPO: maschera attoNascitaTipo03, con la tendina «Numero '
                  'Gemelli» e i dati del secondo gemello, comprese le caselle «Nato morto» e '
                  '«Morto prima della denuncia». Coprire nomi e codici fiscali.',
               'La maschera dei gemelli in SIPO')

    h(d, 2, 'La pratica unica e i dati per gemello')
    par(d, 'Durante la compilazione il parto è **una sola pratica**: una riga di ATTO_NASCITA '
           'con il numero dei gemelli e una riga di ATTO_NASCITA_SOGGETTO per ciascun nato, con '
           'la sua posizione. I dati dei genitori e del dichiarante si inseriscono una volta '
           'sola. Se l’operatore riduce il numero dei gemelli, i nati di posizione più alta sono '
           'eliminati; per i gemelli il controllo dei duplicati non si applica.')
    tabella(d, SIPO_TABELLE, [1.6, 2.0, 3.1])

    h(d, 2, 'La divisione in N atti')
    par(d, 'Salvata la pratica, la pagina di riepilogo avverte: «Se si conferma, la pratica verrà '
           'divisa in N atti diversi, ciascuno per ogni nato». Con «Conferma» il servizio '
           '/performAttiPlurigemellari esegue la procedura PKG_PRATICA.CREA_ATTI_NASCITA_FIGLI, '
           'che crea gli atti. Dopo la divisione i gemelli restano legati da '
           'ATTO.ID_LAVORAZIONE_PADRE, che punta al primo atto; i servizi dell’anteprima trovano '
           'il gemello successivo e quello precedente con questo legame, ordinando per ID_ATTO. '
           'Il pulsante «indietro» dell’anteprima annulla la divisione '
           '(PKG_PRATICA.undo_atti_nascita_figli).')
    par(d, 'Il corpo delle procedure non è fra le sorgenti. Restano quindi da conoscere il modo in '
           'cui i dati comuni sono copiati sugli atti, l’ordine di creazione e l’assegnazione '
           'dei numeri (GE-07, GE-08).')
    segnaposto(d, 'Schermata di SIPO: riepilogo della pratica gemellare con il messaggio «Se si '
                  'conferma, la pratica verrà divisa in N atti diversi…» e il pulsante Conferma.',
               'La divisione della pratica in un atto per nato')

    h(d, 2, 'L’anteprima e la definizione')
    par(d, 'Divisa la pratica, l’anteprima scorre i gemelli con i pulsanti GEMELLO SUCCESSIVO e '
           'GEMELLO PRECEDENTE; la posizione dell’«occhio» del registro si alterna da un gemello '
           'all’altro. Il comando DEFINISCI GEMELLI chiede conferma («Il nascituro è gemello con '
           'altri, se si conferma, saranno definiti gli atti: …») e definisce **tutti i gemelli '
           'in sequenza**, con una chiamata a /finalizzaAtto per ciascuno; i PDF degli atti si '
           'generano in un secondo giro, presumibilmente perché il testo di ciascuno richiede '
           'che tutti abbiano già il proprio numero.')
    tabella(d, SIPO_SERVIZI, [1.3, 2.4, 3.0])
    segnaposto(d, 'Schermata di SIPO: anteprima dell’atto di un gemello con i pulsanti GEMELLO '
                  'PRECEDENTE, GEMELLO SUCCESSIVO e DEFINISCI GEMELLI.',
               'L’anteprima dei gemelli')

    h(d, 2, 'La numerazione')
    par(d, 'In compilazione l’atto riceve un numero provvisorio '
           '(PKG_PRATICA.get_temp_numatto); il definitivo si assegna alla definizione, dentro i '
           'pacchetti PL/SQL. Il codice Java non dice se i numeri dei gemelli siano consecutivi: '
           'la logica sta nelle procedure non disponibili (GE-07).')

    h(d, 2, 'Nato morto e morto prima della denuncia')
    par(d, 'I due flag stanno sul singolo nato e si impostano con due caselle nel frammento di '
           'ciascun gemello, visibili solo nell’iscrizione da pubblico ufficiale; nella '
           'trascrizione da ospedale sono forzati a N. Nessun validatore li legge: non ci sono '
           'campi che diventino obbligatori o spariscano secondo lo stato del nato.')
    voce(d, 'Nato morto.', 'È escluso dai rapporti di parentela; il pulsante «Gestione Rapporti '
         'di Parentela» si disabilita solo se tutti i gemelli sono nati morti. Ha una stampa '
         'propria, il permesso di seppellimento (modello 803). Non è iscritto in ANPR.')
    voce(d, 'Morto prima della denuncia.', 'Si salva e si rilegge, ma nel codice non produce '
         'effetti: non arriva ad ANPR, non è nella vista di allineamento e non ha alcun legame '
         'con l’area decessi. Non si forma alcun atto di morte, né automatico né guidato.')

    h(d, 2, 'L’allineamento anagrafico')
    par(d, 'L’allineamento con ANPR avviene **per atto**, dopo la divisione: ogni gemello ha la '
           'sua chiamata al concentratore all-anpr-sipo, che sceglie l’operazione. La richiesta '
           'porta il solo indicatore del nato morto.')
    voce(d, 'Nato vivo.', 'Iscrizione 1001, oppure A001 se il nato è iscritto all’AIRE.')
    voce(d, 'Nato morto.', 'Nessuna chiamata ad ANPR: il soggetto è registrato come '
         '«occasionale» con lo stato «nato morto», residente o non residente.')
    voce(d, 'Nato vivo e poi deceduto.', 'Iscritto come nato vivo, senza cancellazione '
         'successiva (GE-06).')

    # ------------------------------------------------------------ 5
    h(d, 1, 'ANSC')
    h(d, 2, 'Gli UC di nascita e i tre stati')
    par(d, 'Il catalogo ANSC conta 143 UC di nascita. Le 108 dichiarazioni sono organizzate in '
           '**terne**: per ogni combinazione di filiazione, termine e dichiarante esistono tre UC '
           'che differiscono solo per la 6ª cifra — 0 nato vivo, 1 nato morto, 2 nato vivo ma '
           'morto prima della dichiarazione. Le descrizioni concordano con la cifra in tutti i '
           '108 casi. I codici motore non sono consecutivi: 11112000, 11112100 e 11112200 sono '
           'Dic_Nasc_004, 005 e 077.')
    tabella(d, ANSC_UC, [2.8, 0.7, 1.0, 1.0, 1.0])
    par(d, 'La regola non vale fuori dalle dichiarazioni. Gli UC dei riconosciuti prima della '
           'nascita hanno solo la variante del nato vivo; nei riconoscimenti e nelle trascrizioni '
           'di nascita nessuna descrizione nomina il nato morto o il deceduto; fra gli UC di '
           'morte nessuno riguarda il neonato.')

    h(d, 2, 'Che cosa cambia fra le tre varianti')
    par(d, 'Il mapping delle tre varianti è quasi identico. Nella terna di riferimento '
           'differiscono sei righe, e lo stesso schema si ripete su tutte le 36 terne: i due '
           'certificati medici in 36 su 36, il luogo di filiazione obbligatorio, obbligatorio, '
           'facoltativo in 36 su 36, le formule 41 e 40 in 33 terne. Nessuna variante dichiara '
           'campi sulla data o sull’ora della morte: la morte non si descrive nell’atto di '
           'nascita.')
    tabella(d, ANSC_TERNA, [2.3, 1.4, 1.5, 1.5])

    h(d, 2, 'I campi del modello evento')
    par(d, 'Il blocco dei dati di nascita del modello evento ha i campi per lo stato del nato e '
           'per il parto plurimo. I campi gemellari **non compaiono in nessuno dei 374 mapping**, '
           'neppure come facoltativi: la configurazione importata non li conterrà e a '
           'valorizzarli dovrà essere il concentratore. Lo stato del nato invece è nei mapping '
           'delle dichiarazioni, ma solo come facoltativo, perché l’UC lo dichiara già.')
    tabella(d, ANSC_CAMPI, [1.7, 3.2, 1.8])
    par(d, 'Gli elenchi dei fratelli sono la ragione della prenotazione. L’atto del primo nato '
           'deve citare l’identificativo del secondo e viceversa, e ANSC non consente di '
           'aggiornare un atto depositato: senza un’assegnazione anticipata degli identificativi '
           'la dipendenza è circolare.')

    h(d, 2, 'La prenotazione')
    tabella(d, PRENOTA, [1.7, 2.3, 2.7])
    par(d, 'La guida operativa [A3] descrive il percorso sulla web app: si indica il numero dei '
           'gemelli, poi il numero comunale di ciascuno; il servizio «restituisce gli '
           'identificativi unici nazionali … e predispone gli atti di ciascun gemello, che dovrai '
           'completare acquisendo metadati e firme». La storia del servizio è instabile: nel '
           'rilascio 1.9.0 era stato aggiunto un idContenitore «per legare tra di loro gli atti '
           'dei gemelli», che non è più nel contratto senza che il changelog ne dichiari la '
           'rimozione; la prenotazione è stata corretta nel rilascio 1.23.0.')
    segnaposto(d, 'Schermata della web app ANSC: prenotazione degli atti del parto gemellare '
                  '(numero dei gemelli e numeri comunali), dalla guida operativa, cap. 8.',
               'La prenotazione sulla web app ANSC')

    h(d, 2, 'Il completamento di ciascun atto')
    voce(d, 'Con quale UC.', 'La guida: «il caso d’uso predisposto per i parti gemellari è un '
         'caso d’uso di servizio, in cui nessun dato è obbligatorio a meno del soggetto '
         'intestatario». Il caso di servizio delle nascite, 11999999 (Dic_Nasc_999), dichiara '
         'però 33 campi obbligatori — numero comunale, data e ora di formazione, motivo del '
         'recupero, nome, sesso, data, ora e stato di nascita del nato, composizione completa — '
         'ed è l’unico mapping che porti tipoNascitaSoggetto. Il payload di test della '
         'prenotazione passa invece l’UC ordinario 11111000. Nessuna fonte chiude la '
         'questione (GE-01, GE-04).')
    voce(d, 'Con quale testo.', 'La minuta va scritta dall’ufficiale con le formule ministeriali '
         'del parto gemellare (35, 36, 37 secondo la guida) e con gli identificativi assegnati '
         'dalla prenotazione. Non c’è automatismo: un identificativo sbagliato si corregge solo '
         'con una nota tecnica. Le formule 35-37 non compaiono in nessun mapping (GE-10).')
    voce(d, 'Con quale firma.', 'La firma dei dichiaranti è solo cartacea, riacquisita come '
         'processo verbale; la firma elettronica è esclusa per i parti gemellari.')
    voce(d, 'In quale ordine.', 'Un gemello alla volta: dopo la firma remota dell’USC si passa '
         'all’atto predisposto per il gemello successivo.')
    voce(d, 'Come si riconosce la bozza.', 'Il modello evento porta sia l’identificativo interno '
         'sia quello nazionale, entrambi «assegnati dal sistema»; nessuna fonte dice quale '
         'valorizzare per completare la bozza prenotata invece di crearne una nuova (GE-02).')
    voce(d, 'Che cosa fare di un atto prenotato e non usato.', 'Nessuna fonte lo dice. La via '
         'disponibile è la cancellazione logica (R011, stato 9 CANCELLATO); l’identificativo '
         'resta consumato.')

    h(d, 2, 'Il vincolo del 9 settembre 2024')
    par(d, 'Dal 9 settembre 2024 i casi d’uso di servizio delle dichiarazioni, fra cui '
           '11999999, non sono più disponibili tramite servizi cooperativi e restano utilizzabili '
           'solo sulla web app [A7]. La comunicazione non nomina la prenotazione, che resta nel '
           'contratto. Se il completamento dei gemelli richiede davvero il caso di servizio, '
           'dal gestionale si può prenotare ma non completare; se invece le bozze si completano '
           'con l’UC ordinario del singolo nato, come suggerisce il payload di test, il percorso '
           'cooperativo è intatto. È la questione da cui dipende tutto il capitolo '
           'sull’integrazione (GE-01).')

    h(d, 2, 'Ciò che le fonti non dicono')
    voce(d, 'Il parto misto.', 'Nessuna fonte tratta il caso di un gemello vivo con un gemello '
         'nato morto o deceduto. Due indizi: la richiesta conta i «gemelli nati vivi», e il caso '
         'di servizio dichiara lo stato di nascita del singolo nato (GE-03, GE-04).')
    voce(d, 'L’atto di morte del nato vivo e poi deceduto.', 'Nessuna fonte dice se ANSC lo '
         'formi, lo richieda come atto separato o lo ricavi dall’atto di nascita (GE-05).')
    voce(d, 'L’anagrafe.', 'Nessuna fonte dice come la comunicazione anagrafica tratti il nato '
         'morto e il nato vivo poi deceduto (GE-06).')

    # ------------------------------------------------------------ 6
    h(d, 1, 'SIPO e ANSC a confronto')
    par(d, 'I due sistemi organizzano lo stesso fatto in modo diverso: SIPO raccoglie e poi '
           'divide, ANSC divide subito e poi completa. La tabella mette in fila le differenze e '
           'ciò che ciascuna chiede all’integrazione.')
    tabella(d, CONFRONTO, [1.2, 1.8, 1.8, 1.9])

    # ------------------------------------------------------------ 7
    h(d, 1, 'La modalità di integrazione')
    par(d, 'Una modalità di integrazione esiste: ANSC espone la prenotazione tramite servizi '
           'cooperativi, e la struttura di SIPO — pratica unica, divisione, definizione gemello '
           'per gemello — vi si adatta senza essere stravolta. Non è però accertato che le bozze '
           'prenotate si possano completare dal gestionale (GE-01). Si propongono quindi due '
           'percorsi, con lo stesso inizio in SIPO: **A** è il percorso di riferimento se Sogei '
           'conferma il completamento con l’UC ordinario; **B** è il ripiego, e coincide con la '
           'strategia adottata per gli atti che SIPO non può formare [R2].')
    segnaposto(d, 'Diagramma a corsie (SIPO · be-numeratore-comunale · all-ansc-sipo · ANSC): '
                  'compilazione, divisione, PRENOTA GEMELLI (stacco di N numeri, R009 '
                  '/prenota/evento, N bozze), poi per ciascun gemello anteprima, validazione e '
                  'firme, fino all’ultimo gemello. Ramo tratteggiato per il percorso B verso la '
                  'web app.',
               'I due percorsi di integrazione')

    h(d, 2, 'Percorso A — tutto da SIPO')
    par(d, 'Il percorso inserisce nel flusso di SIPO un solo passo nuovo, **PRENOTA GEMELLI**, e '
           'spezza il comando DEFINISCI GEMELLI in una finalizzazione per gemello. Il pulsante '
           'riprende la scelta di Side [M1], che lo ha separato dalla validazione perché gli '
           'identificativi devono entrare nel testo dell’atto prima che sia validato. In SIPO il '
           'posto naturale è subito dopo la divisione: gli atti esistono, i dati di ciascun nato '
           'sono noti e il testo non è ancora composto.')
    tabella(d, PASSI_A, [0.3, 1.5, 2.1, 1.5, 1.4])
    par(d, 'Regole del passo PRENOTA GEMELLI, riprese da Side [M1] e adattate:')
    voce(d, 'Quando compare.', 'Solo sul primo gemello di una pratica divisa, finché la '
         'prenotazione non è fatta. VALIDA resta inibito sugli atti dei gemelli fino a '
         'prenotazione avvenuta.')
    voce(d, 'Conferma.', 'Una finestra avverte che, prenotati gli atti, il numero dei gemelli non '
         'si può più cambiare. Dopo la prenotazione l’annullamento della divisione chiude le '
         'bozze o va impedito (GE-09).')
    voce(d, 'Numeri comunali.', 'Si staccano in blocco, tanti quanti gli atti da prenotare, con '
         'una sola richiesta al servizio be-numeratore-comunale, che garantisce numeri '
         'consecutivi [R3].')
    voce(d, 'UC.', 'Si determina per ciascun gemello dai suoi due flag; quale UC passare alla '
         'prenotazione di un parto misto è GE-04.')
    voce(d, 'Esito.', 'Gli identificativi restituiti si assegnano ai gemelli nell’ordine di '
         'nascita: una riga di ANSC_STATO_ATTO in BOZZA per ciascun atto, con numero comunale e '
         'idAnsc, e una riga della tabella dei gemelli descritta più avanti.')
    par(d, 'Il concentratore, a ogni validazione, valorizza i campi che nessun mapping dichiara: '
           'partoGemellare, numeroGemelli, progressivoGemello e gli elenchi dei fratelli, '
           'calcolati dalle righe dello stesso parto; e lo stato del nato (natoMorto, '
           'natoVivoMaDeceduto) dai flag di SIPO. La combinazione dei due flag entrambi a S è '
           'respinta dal pre-filtro locale.')
    segnaposto(d, 'Ipotesi di schermata SIPO: riepilogo del primo gemello dopo la divisione, con '
                  'il pulsante PRENOTA GEMELLI e la finestra di conferma; dopo la prenotazione, '
                  'l’elenco dei gemelli con numero comunale, idAnsc e stato ANSC di ciascuno.',
               'Il passo PRENOTA GEMELLI')

    h(d, 2, 'Percorso B — la web app e il ritorno in SIPO')
    par(d, 'Se il completamento da gestionale non è possibile, il parto plurimo segue la strategia '
           'degli atti che SIPO non può formare [R2]: la compilazione e i numeri restano in SIPO, '
           'la prenotazione e le firme si fanno sulla web app, e ciascun atto torna in SIPO con '
           'DEFINISCI, che lo aggancia all’atto ANSC.')
    tabella(d, PASSI_B, [0.3, 1.8, 4.6])
    par(d, 'Il prezzo è il doppio inserimento dei dati sulla web app, che per un parto plurimo si '
           'moltiplica per il numero dei nati. Il percorso non tocca la logica dei gemelli di '
           'SIPO, salvo il comando DEFINISCI GEMELLI, che diventa un aggancio per gemello.')

    h(d, 2, 'Nato morto e nato vivo poi deceduto nel parto plurimo')
    voce(d, 'UC.', 'Ogni gemello ha l’UC della propria variante: in un parto misto gli atti '
         'hanno UC diversi (GE-04).')
    voce(d, 'Allegati.', 'Il certificato medico che attesta lo stato è obbligatorio per il nato '
         'morto e per il nato vivo poi deceduto: va acquisito per il singolo gemello, con il '
         'processo degli allegati dell’analisi di integrazione [R1].')
    voce(d, 'Prenotazione.', 'Se i nati morti non si prenotano (GE-03), il loro atto si forma a '
         'parte con l’UC ordinario della variante, e gli elenchi dei fratelli degli altri atti '
         'non lo citano.')
    voce(d, 'Morte e anagrafe.', 'Per il nato vivo e poi deceduto il documento non propone '
         'automatismi verso l’area decessi né verso ANPR finché GE-05 e GE-06 non sono chiusi.')

    h(d, 2, 'Effetti sul disegno')
    par(d, 'Per tenere insieme i gemelli di un parto lato ANSC si adotta la tabella di Side '
           '[M1] con i nomi di origine e con gli adattamenti dichiarati sotto. Una riga per '
           'atto prenotato; le righe di un parto condividono la richiesta di prenotazione.')
    tabella(d, ATTI_GEMELLARI, [1.8, 1.2, 1.0, 2.7])
    for riga in [
        'CREATE TABLE ANSC_USR.ATTI_GEMELLARI (',
        '  id_atto_gemellare         NUMBER GENERATED ALWAYS AS IDENTITY,',
        '  id_richiesta_prenotazione NUMBER            NOT NULL,',
        '  id_lavorazione_padre      NUMBER            NOT NULL,',
        '  id_atto_sipo              NUMBER            NOT NULL,',
        '  ty_use_case               VARCHAR2(10 CHAR) NOT NULL,',
        '  nr_gemelli                NUMBER(2)         NOT NULL,',
        '  nr_progressivo_gemello    NUMBER(2)         NOT NULL,',
        '  nr_atto_comunale          NUMBER(6),',
        '  fg_stesura_atto           CHAR(1 CHAR) DEFAULT \'0\' NOT NULL,',
        '  cd_operatore              VARCHAR2(40 CHAR) NOT NULL,',
        '  ts_operazione             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,',
        '  CONSTRAINT atti_gemellari_pk PRIMARY KEY (id_atto_gemellare),',
        '  CONSTRAINT atti_gemellari_atto_uk UNIQUE (id_atto_sipo),',
        '  CONSTRAINT atti_gemellari_prog_uk',
        '    UNIQUE (id_richiesta_prenotazione, nr_progressivo_gemello),',
        '  CONSTRAINT atti_gemellari_num_ck CHECK (nr_gemelli BETWEEN 2 AND 10),',
        '  CONSTRAINT atti_gemellari_prog_ck',
        '    CHECK (nr_progressivo_gemello BETWEEN 1 AND nr_gemelli),',
        '  CONSTRAINT atti_gemellari_stesura_ck CHECK (fg_stesura_atto IN (\'0\',\'1\'))',
        ');',
    ]:
        p = d.add_paragraph()
        r = p.add_run(riga)
        r.font.name = 'Courier New'
        r.font.size = Pt(8)
        p.paragraph_format.space_after = Pt(0)
    d.add_paragraph()
    tabella(d, ADATTAMENTI, [2.1, 1.6, 3.0])
    voce(d, 'Contratto del concentratore.', 'Va aggiunta ad ansc-v1.yaml l’operazione di '
         'prenotazione dei gemelli, che stacca i numeri, chiama R009 /prenota/evento e registra '
         'store e tabella dei gemelli in una sola azione; la chiusura riusa l’annullamento già '
         'previsto.')
    voce(d, 'Store.', 'ANSC_STATO_ATTO riceve le righe dei gemelli alla prenotazione, in BOZZA. '
         'Una prenotazione dimenticata è un atto aperto in ANSC: la vista di supervisione del '
         'back-office deve mostrarla.')
    voce(d, 'Numerazione.', 'Il numero comunale di SIPO ha sei cifre, mentre il modello evento '
         'ne ammette cinque: è il punto già aperto nell’analisi di integrazione [R1] e vale '
         'per ciascun gemello.')

    # ------------------------------------------------------------ 8
    h(d, 1, 'Punti aperti')
    tabella(d, OPEN, [0.6, 1.4, 4.0, 0.7])


def intesta(d):
    for r in d.tables[0].rows:
        if len(r.cells) < 2:
            continue
        etichetta = r.cells[0].text.strip().lower()
        valore = {'progetto': 'SIPO — Integrazione con ANSC',
                  'data consegna': DATA}.get(etichetta)
        if valore:
            D.riscrivi_cella(r.cells[1], valore)
    for fatto in D.frontespizio(d, '0.1', NOME):
        print('  ' + fatto)
    storia = D.trova_tabella(d, 'versione', 'sintesi dei cambiamenti')
    for r in list(storia.rows[1:]):
        if not any(c.text.strip() for c in r.cells):
            r._tr.getparent().remove(r._tr)
    D.storia(d, DATA, '0.1', 'Tutti',
             'Prima stesura. I tre stati del nato in SIPO e in ANSC; il parto plurimo in SIPO '
             '(pratica unica, divisione, definizione, numerazione, ANPR) e in ANSC (UC a terne, '
             'campi del modello evento, prenotazione R009, completamento, vincolo del 9 settembre '
             '2024); confronto; due percorsi di integrazione e tabella ATTI_GEMELLARI ripresa da '
             'Side; dodici punti aperti. Figure come segnaposto.')


if __name__ == '__main__':
    doc = costruisci()
    scrivi(doc)
    intesta(doc)
    doc.save(OUT)
    print('scritto:', os.path.relpath(OUT, BASE))
    cap, tab, fig = D.riepilogo(OUT)
    print('capitoli %d | tabelle %d | figure %d | segnaposto %d' % (cap, tab, fig, FIG[0]))
