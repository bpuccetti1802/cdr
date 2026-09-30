# -*- coding: utf-8 -*-
"""Il ponte fra i due alberi: dal percorso del modello evento al percorso del DTO di SIPO.

Il raccordo per solo nome di campo non funziona — il mapping ANSC nomina «Cognome» senza dire
di chi, e una maschera di nascita ha undici cognomi diversi: provandolo, «Provincia» finiva su
`deceduto.attoNascita.serie` e «Motivo ritardo» su `figlio1.mortoAnteDenuncia`. Il ponte è
quindi in due tempi, e nell'ordine conta il primo:

    1. IL SOGGETTO   evento.intestatari[]        ↔  deceduto            (tabella SOGGETTI)
    2. IL CAMPO      .idComuneNascita            ↔  .comuneNascita      (regole FOGLIE)

Il primo tempo è giudizio, ed è scritto a mano qui sotto: sono poche righe per area, ciascuna
con la sua nota. Il secondo è meccanico e riusabile, perché ANSC descrive la persona sempre
con lo stesso schema — `ModelSoggetto` ricorre 49 volte nel modello evento — e SIPO con tre o
quattro classi. Mappare la persona una volta copre la maggior parte dei campi di ogni UC: è
lo stesso principio per cui il payload si costruisce sull'albero e non per caso d'uso.

⚠️ Ciò che il ponte NON trova è informazione, non scarto: un campo che ANSC chiede e SIPO non
ha è precisamente il risultato che si cerca, e va riportato con il suo grado di certezza.
"""
import re

import sipo_modello as SM

# --------------------------------------------------------------------- 1. i soggetti
# blocco del modello evento → percorso nell'albero del DTO di SIPO, con il perché.
# `None` significa: il blocco NON ha corrispondente in SIPO, e la ragione è dichiarata.
SOGGETTI = {
    'decessi': [
        ('intestatari[]', 'deceduto',
         'L’intestatario dell’atto di morte è il defunto.'),
        ('coniuge', 'deceduto.coniuge',
         'ANSC descrive il coniuge con lo schema completo del soggetto; SIPO ne conserva '
         'solo gli estremi essenziali in ConiugeModel.'),
        ('dichiarante', 'dichiarante', ''),
        ('datiDichiarante', 'dichiarante', ''),
        ('datiDiMorte', '',
         'I dati dell’evento stanno nella radice di AttoDecessoModel, non in un blocco '
         'dedicato: in SIPO l’atto e l’evento sono la stessa maschera.'),
        ('datiEventoMorte.attoNascitaDeceduto', 'deceduto.attoNascita', ''),
        ('trascrizioneMorte.attoNascitaDeceduto', 'deceduto.attoNascita', ''),
        ('trascrizioneMorte.atto', 'attoIscritto',
         'Atto formato altrove e trascritto a Roma: in SIPO è la sezione «atto iscritto».'),
        ('trascrizioneMorte.attoEstero', 'attoEstero', ''),
        ('datiEventoMorte', '', ''),
        ('trascrizioneMorte', '', ''),
        ('', '', 'Campi di formazione dell’atto: numero, data, ora, parte e serie.'),
        # blocchi senza corrispondente: si dichiarano, perché l'assenza è il risultato
        ('datiEventoMorte.comparente1', None,
         'SIPO non raccoglie i comparenti nella maschera dell’atto di morte.'),
        ('datiEventoMorte.comparente2', None,
         'SIPO non raccoglie i comparenti nella maschera dell’atto di morte.'),
        ('interprete', None,
         'L’ausilio dell’interprete non è previsto dalle maschere dei decessi.'),
        ('enteDichiarante', None,
         'La dichiarazione da parte di un ente non ha corrispondente nella maschera.'),
        ('datiAnnotazione[]', None,
         'Le annotazioni contestuali sono un flusso separato di SIPO '
         '(/creaAnnotazioniContestuali), fuori dalla maschera dell’atto.'),
        ('datiAnnotazioneModificativa', None, 'Come sopra: flusso separato.'),
        ('composizioneCompleta', None,
         'La minuta è composta da ANSC secondo le formule ministeriali (OP-51).'),
        ('eventoCollegato', None,
         'L’atto collegato esiste in SIPO (ATTO_CORRELATO) ma non è esposto dalla maschera '
         'nella forma che ANSC chiede, e SIPO non sa cercare un atto per identificativo '
         'nazionale: è il nodo di OP-29 e OP-30.'),
        ('datiRettifica', None,
         'La rettifica è un procedimento separato di SIPO, non un blocco della maschera '
         'dell’atto.'),
    ],
    'nascita': [
        ('intestatari[]', 'figlio1',
         '⚠️ Corrispondenza 1:N. ANSC forma un atto per ciascun nato (v3.7), mentre la '
         'pratica di SIPO porta fino a dieci figli (figlio1…figlio10): il raccordo vale per '
         'il primo, gli altri si ottengono per indice. È il verso comunale di OP-31.'),
        ('datiDiNascita', 'figlio1',
         'I dati dell’evento di nascita appartengono al neonato in entrambi i modelli.'),
        ('padre', 'padre', ''),
        ('madre', 'madre', ''),
        ('dichiarante', 'dichiarante', ''),
        ('datiDichiarante', 'dichiarante', ''),
        ('interprete', 'dichiarante.interprete',
         'In SIPO l’interprete pende dal soggetto che assiste; ANSC lo dichiara una volta '
         'per evento.'),
        ('riconoscimentoMadre', '',
         'Gli estremi dell’atto di riconoscimento materno stanno nella radice, nei campi '
         '*AttoPreRiconMadre.'),
        ('riconoscimentoPadre', '',
         'Gli estremi dell’atto di riconoscimento paterno stanno nella radice, nei campi '
         '*AttoPreRiconPadre.'),
        ('', '', 'Campi di formazione dell’atto: numero, data, ora, parte e serie.'),
        ('ufficialeStatoCivile', None,
         'L’ufficiale che forma l’atto viene dalla sessione, non dalla maschera; in ANSC '
         'l’identità è già portata dal token (i campi operatore* sono deprecati).'),
        ('luogoRedazione', None,
         'Il luogo di redazione è il comune stesso: SIPO non lo chiede nella maschera.'),
        ('enteDichiarante', None,
         'La dichiarazione da parte di un ente non ha corrispondente nella maschera.'),
        ('attoNotarileConsensoMadre', None,
         'Gli estremi dell’atto notarile di consenso non sono raccolti dalla maschera.'),
        ('attoNotarileConsensoPadre', None, 'Come sopra.'),
        ('datiAdozioneMultiIntestatario', None,
         'L’adozione con più intestatari usa un servizio di deposito dedicato (R020), non '
         'coperto dal concentratore: si veda OP-45.'),
        ('datiAdozioneMinoriInternazionale', None,
         'L’adozione internazionale usa il servizio R015: si veda OP-45.'),
        ('datiAnnotazione[]', None,
         'Le annotazioni contestuali sono un flusso separato di SIPO.'),
        ('datiAnnotazioneModificativa', None, 'Come sopra: flusso separato.'),
        ('composizioneCompleta', None,
         'La minuta è composta da ANSC secondo le formule ministeriali (OP-51).'),
        ('eventoCollegato', None,
         'Come per la morte: l’atto collegato non è esposto nella forma che ANSC chiede e '
         'SIPO non sa cercarlo per identificativo nazionale (OP-29, OP-30).'),
        ('datiRettifica', None,
         'La rettifica è un procedimento separato di SIPO.'),
        ('consensoMadre', None,
         '⚠️ ANSC struttura il consenso in sei elementi (tipo, atto, sentenza, altro '
         'ufficiale…); SIPO ne conserva uno solo, e in forma libera: '
         'AttoNascitaModel.datiDelConsenso è una stringa. Il dato non è mappabile così '
         'com’è.'),
        ('trascrizioneNascita', None,
         'Le trascrizioni hanno maschere proprie, non coperte dalla ricognizione '
         'disponibile: vanno rilevate a parte.'),
        ('datiEventoRiconoscimento', None,
         'Il riconoscimento ha in SIPO un proprio atto e una propria maschera '
         '(saveAttoRiconoscimento), distinta da quella di nascita.'),
        ('separazione', None,
         'Dominio dei matrimoni, non delle nascite: fuori dalle due aree rilevate.'),
        ('coniuge', None,
         'Dominio dei matrimoni: fuori dalle due aree rilevate.'),
        ('datiDiMorte', None,
         'Blocco della famiglia morte, citato da un caso d’uso di nascita (nato morto): il '
         'raccordo è quello dell’area decessi.'),
    ],
}

# --------------------------------------------------------------------- 2. le foglie
# I prefissi con cui ANSC scompone un dato che in SIPO è uno solo. Il primo elemento è ciò
# che si toglie, il secondo la nota da riportare: la scomposizione È la conversione.
PREFISSI = [
    ('id', 'ANSC vuole il codice nazionale, SIPO conserva l’identificativo locale: la '
           'traduzione passa per le tabelle territoriali (CODICE_ANPR, DV-32).'),
    ('nome', 'ANSC vuole la denominazione per esteso accanto al codice: si ricava dalla '
             'stessa tabella territoriale.'),
    ('sigla', 'ANSC vuole la sigla della provincia accanto al codice: dalla tabella '
              'PROVINCIA.'),
    ('descrizione', 'ANSC vuole la descrizione accanto al codice: dalla decodifica '
                    'replicata in locale.'),
    ('flag', ''),
    ('testo', ''),
]

# Sinonimi dichiarati: i due mondi chiamano lo stesso dato con nomi diversi. Sono pochi e
# vanno scritti, non indovinati — è la parte che richiede di conoscere il dominio.
SINONIMI = {
    'codicefiscale': ['codiceIndividuale'],
    'nazionalita': ['cittadinanza'],
    'idnazionalita': ['cittadinanza'],
    'anni': ['eta'],
    'irreperibile': ['flgIrreperibile'],
    'statocivile': ['statoCivile'],
    'idstatocivile': ['statoCivile'],
    'descrizionestatocivile': ['statoCivile'],
    'sesso': ['sesso'],
    'descrizionesesso': ['sesso'],
    'idanpr': [], 'idsoggettoanpr': [],      # non esiste in SIPO: è il risultato, non un buco
    'dataformazione': ['dataAtto'],
    'ora': ['oraAtto'], 'minuto': ['oraAtto'],
    'numeroatto': ['numeroAtto'],
    'annoatto': ['anno'],
    'parte': ['parte'], 'serie': ['serie'], 'esponente': ['esponente'],
    # l'evento di morte: ANSC dice «morte», SIPO dice «decesso»
    'datamorte': ['dataDecesso'], 'oramorte': ['oraDecesso'], 'minutomorte': ['oraDecesso'],
    'luogomorte': ['luogoDecesso'], 'idcomunemorte': ['comuneDecesso'],
    'nomecomunemorte': ['comuneDecesso'], 'idprovinciamorte': ['provinciaDecesso'],
    'siglaprovinciamorte': ['provinciaDecesso'], 'idstatomorte': ['statoDecesso'],
    'nomestatomorte': ['statoDecesso'], 'comuneestero': ['comuneDecesso'],
    'indirizzomorte': ['luogoDecesso'],
    'ritrovamento': ['tipoCadavere'],
    # la nascita
    'oranascita': ['oraNascita'], 'minutonascita': ['oraNascita'],
    'natomorto': ['flgNatoMorto', 'mortoAnteDenuncia'],
    'partogemellare': ['flgParto', 'nTotGemelli'],
    'numerogemelli': ['nTotGemelli', 'numeroFigli'],
    'sceltacognome': ['cognomeNuovo', 'flgDoppioCognome'],
    'luogofiliazione': ['comuneOspedale', 'denominazioneOspedale'],
    'indirizzoevento': ['comuneNascitaFuoriOspedale'],
}

# ⚠️ I casi in cui SIPO ha «qualcosa», ma non il dato che ANSC chiede. Trattarli come
# corrispondenze sarebbe peggio che dichiararli mancanti: si crederebbe di avere il dato.
# Sono nati da verifiche puntuali sul codice, e ciascuno cita ciò che SIPO ha davvero.
PARZIALI = {
    'datapresuntamorteda': 'SIPO non conserva l’intervallo di date presunte ma il solo '
                           'contrassegno booleano ATTO_DECESSO.FLAG_DATA_PRESUNTA '
                           '(SalvataggioAttoController:509): il dato che ANSC chiede non '
                           'esiste, va introdotto.',
    'orapresuntamorteda': 'Come sopra: in SIPO la presunzione è un contrassegno, non un '
                          'intervallo.',
}
PARZIALI['datapresuntamortea'] = PARZIALI['datapresuntamorteda']
PARZIALI['orapresuntamortea'] = PARZIALI['orapresuntamorteda']
PARZIALI['testodatapresuntamorte'] = PARZIALI['datapresuntamorteda']

# La scomposizione data/ora: SIPO tiene un timestamp unico dove ANSC vuole tre campi.
FUSI = {
    'dataformazione': 'In SIPO data e ora dell’atto sono fuse in un solo istante '
                      '(improveDataOra → ATTO.DATA_INS_ATTO): ANSC le vuole in tre campi '
                      'distinti (data, ora, minuto), e la conversione le separa.',
}
FUSI['ora'] = FUSI['minuto'] = FUSI['dataformazione']


def _varianti(foglia):
    """I nomi con cui cercare la foglia ANSC nell'albero di SIPO, dal più forte al più debole."""
    fuori, base = [], foglia
    yield_ = fuori.append
    yield_(foglia)
    for pref, _ in PREFISSI:
        if foglia.lower().startswith(pref) and len(foglia) > len(pref):
            resto = foglia[len(pref):]
            base = resto[0].lower() + resto[1:]
            yield_(base)
            break
    for k in (foglia.lower(), base.lower()):
        for s in SINONIMI.get(k, ()):
            yield_(s)
    return fuori


def _normalizza_indici(percorso):
    """`intestatari[0]` e `intestatari[]` sono la stessa cosa: il mapping numera, il ponte no.

    ⚠️ Senza questo, NESSUN percorso di lista si risolve — e sono i più importanti, perché
    l'intestatario è la persona centrale dell'atto: 2.053 righe di nascita e 549 di morte.
    L'indice 0 è il primo elemento e coincide con il soggetto dichiarato. Un indice
    successivo è un ALTRO soggetto (il secondo intestatario di un matrimonio): si normalizza
    lo stesso, perché la struttura è quella, ma lo si dichiara — la sorgente SIPO può essere
    un'altra colonna, e chi legge deve poterlo verificare.
    """
    return re.sub(r'\[\d+\]', '[]', percorso), bool(re.search(r'\[[1-9]\d*\]', percorso))


def _nota_prefisso(foglia):
    for pref, nota in PREFISSI:
        if foglia.lower().startswith(pref) and len(foglia) > len(pref) and nota:
            return nota
    return ''


class Ponte:
    """Risolve un percorso del modello evento in un percorso dell'albero DTO di SIPO."""

    def __init__(self, area, albero_sipo=None, ent=None):
        self.area = area
        self.albero = albero_sipo if albero_sipo is not None else SM.albero(area, ent)
        self.soggetti = SOGGETTI[area]
        # dal blocco più lungo al più corto: «datiEventoMorte.attoNascitaDeceduto» deve
        # vincere su «datiEventoMorte»
        self._ordinati = sorted(self.soggetti, key=lambda t: -len(t[0]))
        # indice per confronto senza maiuscole dentro un dato prefisso di SIPO
        self._per_prefisso = {}
        for p in self.albero:
            testa, _, foglia = p.rpartition('.')
            self._per_prefisso.setdefault(testa, {})[foglia.lower()] = p

    def soggetto(self, percorso):
        """(blocco ANSC, prefisso SIPO o None, nota, resto del percorso)."""
        for blocco, prefisso, nota in self._ordinati:
            if blocco == '':
                continue
            if percorso == blocco or percorso.startswith(blocco + '.'):
                return blocco, prefisso, nota, percorso[len(blocco):].lstrip('.')
        # la radice: vale solo se il percorso non ha blocchi
        if '.' not in percorso:
            for blocco, prefisso, nota in self.soggetti:
                if blocco == '':
                    return '(radice)', prefisso, nota, percorso
        return '', '<sconosciuto>', '', percorso

    def risolvi(self, percorso):
        """Il percorso SIPO corrispondente, con il grado di certezza e le note.

        Gradi: «struttura» = trovato per soggetto e nome; «sinonimo» = trovato per un nome
        dichiarato diverso; «assente» = il soggetto c'è ma il campo no; «soggetto assente» =
        il blocco intero non ha corrispondente; «soggetto ignoto» = blocco non mappato.
        """
        percorso, indice_alto = _normalizza_indici(percorso)
        blocco, prefisso, nota, resto = self.soggetto(percorso)
        if indice_alto:
            nota = ('⚠️ Indice di lista successivo al primo: la struttura è la stessa, il '
                    'soggetto no. Verificare la sorgente SIPO. ' + nota).strip()
        esito = {'blocco': blocco, 'prefisso_sipo': prefisso, 'nota_soggetto': nota,
                 'foglia_ansc': resto, 'percorso_sipo': '', 'grado': '',
                 'nota_campo': _nota_prefisso(resto.split('.')[-1] if resto else '')}
        if prefisso is None:
            esito['grado'] = 'soggetto assente in SIPO'
            return esito
        if prefisso == '<sconosciuto>':
            esito['grado'] = 'soggetto non mappato'
            return esito
        if not resto:
            esito['grado'] = 'blocco'
            return esito
        # il resto può avere una sua profondità (documentoRiconoscimento.numero): si cerca la
        # foglia dentro il prefisso, poi, se non c'è, il percorso intero
        testa, _, foglia = resto.rpartition('.')
        base = f'{prefisso}.{testa}'.strip('.') if testa else prefisso
        indice = self._per_prefisso.get(base) or {}
        for i, variante in enumerate(_varianti(foglia)):
            trovato = indice.get(variante.lower())
            if trovato:
                esito['percorso_sipo'] = trovato
                esito['grado'] = 'struttura' if i == 0 else 'sinonimo'
                if foglia.lower() in FUSI:
                    esito['nota_campo'] = (FUSI[foglia.lower()] + ' '
                                           + esito['nota_campo']).strip()
                return esito
        esito['grado'] = 'assente in SIPO'
        if foglia.lower() in PARZIALI:
            esito['nota_campo'] = (PARZIALI[foglia.lower()] + ' '
                                   + esito['nota_campo']).strip()
        return esito

    def dettaglio(self, percorso_sipo):
        """Ciò che si sa del campo di SIPO: maschere, etichetta, colonna, evidenze."""
        return self.albero.get(percorso_sipo)


if __name__ == '__main__':
    import collections

    import mappatura_uc as MU
    m = MU.Modello()
    righe = MU.mappatura(m, {})
    ent = SM.SD.entita(('common', 'back-end'))
    for fam, area in (('Morte', 'decessi'), ('Nascita', 'nascita')):
        p = Ponte(area, ent=ent)
        perc = sorted({r['percorso'] for r in righe
                       if r['famiglia'] == fam and r['percorso'] and r['risolto']})
        g = collections.Counter()
        con_col = 0
        esempi = []
        for x in perc:
            e = p.risolvi(x)
            g[e['grado']] += 1
            d = p.dettaglio(e['percorso_sipo']) if e['percorso_sipo'] else None
            if d and d['destinazione'] and d['destinazione']['genere'] != 'ignoto':
                con_col += 1
                if len(esempi) < 8:
                    esempi.append((x, e['percorso_sipo'], d['etichetta'],
                                   f'{d["destinazione"].get("tabella")}.'
                                   f'{d["destinazione"].get("colonna")}'))
        print(f'=== {fam}: {len(perc)} percorsi ANSC distinti')
        for k, v in g.most_common():
            print(f'     {k:26} {v:5}')
        print(f'     → con colonna di SIPO      {con_col}')
        for e in esempi:
            print(f'       {e[0][:38]:40} → {e[1][:26]:28} «{e[2][:18]:20}» {e[3]}')


def arricchisci(famiglia, ponte, modello=None, ricognizione=None, righe=None):
    """Le righe del mapping di una famiglia, con il lato SIPO risolto DAL PONTE.

    Stesse chiavi prodotte da `mappatura_sipo.arricchisci`, così i fogli non cambiano: quel
    che cambia è da dove viene il percorso del DTO. Là si partiva dall'ETICHETTA della
    ricognizione funzionale e la si cercava fra i campi delle maschere; qui si parte dal
    PERCORSO del modello evento e si passa per il soggetto. La differenza non è di forma:
    l'etichetta «Cognome» non dice di chi, e una maschera di nascita ne ha undici.

    La ricognizione non sparisce, cambia ruolo: da sorgente diventa RISCONTRO. Resta nella
    colonna «Campo della maschera SIPO», ed è un'evidenza indipendente — dove concorda con il
    ponte la certezza è piena, dove diverge c'è qualcosa da guardare.
    """
    import mappatura_sipo as MS
    import mappatura_uc as MU

    modello = modello or MU.Modello()
    ricognizione = ricognizione if ricognizione is not None else MU.lato_sipo(modello)
    righe = righe if righe is not None else MU.mappatura(modello, ricognizione)
    fuori = []
    for r in righe:
        if not r['famiglia'].lower().startswith(famiglia[:5].lower()):
            continue
        if not r['binding']:
            fuori.append(r)
            continue
        e = ponte.risolvi(r['percorso'])
        d = ponte.dettaglio(e['percorso_sipo']) if e['percorso_sipo'] else None
        dest = (d or {}).get('destinazione')
        noti = ricognizione.get(r['percorso'], [])
        proprio = any(s for s in noti if r['motore'] in s['motori'])
        rec = (next((s for s in noti if r['motore'] in s['motori']), None)
               or (noti[0] if noti else None))
        campo_ansc = {'tipo': r['tipo'], 'formato': r['formato'],
                      'decodifica': r['decodifica'], 'percorso': r['percorso']}
        serve, regola = MS.conversione(campo_ansc, dest)
        motivo = ' '.join(x for x in (e['nota_soggetto'], e['nota_campo'],
                                      (dest or {}).get('motivo', '')) if x)
        fuori.append(dict(
            r,
            sipo_ricognizione=rec['campo'] if rec else '',
            sipo_area=(rec.get('area') or rec.get('gruppo') or '') if rec else '',
            sipo_maschera=(rec.get('maschera', '') if rec else '')
                          or ', '.join((d or {}).get('maschere', [])[:4]),
            sipo_riferito_a_questo_uc='Sì' if proprio else ('No' if rec else ''),
            sipo_campo_dto=e['percorso_sipo'],
            sipo_grado=e['grado'],
            sipo_certezza_etichetta=(d or {}).get('certezza_etichetta', ''),
            sipo_tabella=(dest or {}).get('tabella', ''),
            sipo_colonna=(dest or {}).get('colonna', ''),
            sipo_percorso_xml=(dest or {}).get('percorso_xml', ''),
            sipo_tipo_java=(dest or {}).get('tipo_java', ''),
            sipo_genere=(dest or {}).get('genere', ''),
            sipo_ambiguo=(d or {}).get('ambiguo', ''),
            sipo_motivo=motivo,
            evidenza_maschera=(d or {}).get('evidenza_maschera', ''),
            evidenza_salvataggio=(dest or {}).get('evidenza', ''),
            conversione_richiesta=serve,
            conversione_regola=regola,
        ))
    return fuori
