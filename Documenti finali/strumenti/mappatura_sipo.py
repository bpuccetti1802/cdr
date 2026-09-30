# -*- coding: utf-8 -*-
"""Congiunge le due metà della mappatura: il fabbisogno ANSC e la colonna del DB SIPO.

`mappatura_uc.py` dice CHE COSA ANSC chiede (percorso del modello evento, obbligatorietà,
condizione); `sipo_dizionario.py` dice DOVE sta il dato in SIPO (tabella e colonna, o nodo
XML). Qui si incontrano, e il punto d'incontro è l'ETICHETTA della maschera: è l'unico nome
che compare in entrambi i mondi, perché la ricognizione funzionale è stata fatta guardando le
maschere.

    ricognizione: «Cognome»  →  binding ANSC  evento.intestatari[0].cognome
    maschera:     «Cognome»  →  *{deceduto.cognome}
    salvataggio:  deceduto.cognome            →  SOGGETTO.COGNOME

Ogni riga porta il proprio grado di certezza e le proprie evidenze: dove la catena si
interrompe si scrive perché, non si tira a indovinare.
"""
import glob
import os
import re
import unicodedata

import mappatura_uc as MU
import sipo_dizionario as SD

BASE = SD.BASE
# Le due aree applicative coperte dalle ricognizioni disponibili. Sono diverse per struttura,
# e la differenza va tenuta: i decessi hanno UN salvataggio (le 11 maschere condividono
# `AttoMorteTipo00Controller`), le nascite ne hanno una ventina, uno per tipologia di atto.
AREE = {
    'decessi': {
        'fe': 'front-end/decessi-web/DecessiWeb/src/main/resources',
        'templates': 'gestioneDecessi', 'prefisso': 'attoMorte',
        'salvataggi': ['back-end/decessi-be/DecessiBL/src/main/java/it/romaCapitale/sipo/'
                       'decessiBE/controller/SalvataggioAttoController.java'],
        'moduli': ('decessi-entities',),
    },
    'nascita': {
        'fe': 'front-end/nascita-web/NascitaWeb/src/main/resources',
        'templates': 'gestioneNascita', 'prefisso': 'attoNascita',
        'salvataggi': sorted(glob.glob(os.path.join(
            BASE, 'back-end/nascita-be/NascitaBL/src/main/java/it/romaCapitale/sipo/'
                  'nascitaBE/controller/Salvataggio*.java'))),
        'moduli': ('matrim-entities',),      # nascita-be usa le entity dello stato civile
    },
}

# ⚠️ Non tutta la persistenza è leggibile dalle assegnazioni: `nascita-be` usa un ModelMapper
# (`utilities/ModelMapperHolder`), che copia per NOME della proprietà. Dove la catena esplicita
# si interrompe si può ancora proporre la colonna per convenzione, ma è una PROPOSTA e va
# scritta come tale: si dichiara la via, non si spaccia per accertamento.
ENTITA_AREA = {
    'decessi': ['AttoDecesso', 'AttoDec', 'SoggettoDec', 'AttoDecessoEstero',
                'AttoDecessoExtend', 'AttoDecessoAgenzia'],
    'nascita': ['AttoNascita', 'AttoNascitaSoggetto', 'AttoNascitaExtend',
                'AttoNascitaInterprete', 'AttoMatr', 'Soggetto'],
}


def per_convenzione(ris, campo_dto):
    """La colonna che porta lo stesso nome della proprietà, nelle entity dell'area."""
    memo = ris.setdefault('_memo_convenzione', {})
    if campo_dto in memo:
        return memo[campo_dto]
    b = _per_convenzione(ris, campo_dto)
    memo[campo_dto] = b
    return b


def _per_convenzione(ris, campo_dto):
    foglia = campo_dto.split('.')[-1].lower()
    cfg = AREE[ris['area']]
    trovate = []
    for classe in ENTITA_AREA.get(ris['area'], []):
        e = SD.cerca_entita(ris['entita'], classe, cfg['moduli'])
        if not e:
            continue
        for prop, c in e['campi'].items():
            if prop.lower() == foglia:
                trovate.append({'genere': 'convenzione', 'tabella': e['tabella'],
                                'colonna': c['colonna'], 'tipo_java': c['tipo_java'],
                                'entity': classe,
                                'evidenza': f'{e["file"]}:{c["riga"]}'})
    if not trovate:
        return None
    b = dict(trovate[0])
    if len(trovate) > 1:
        b['ambiguo'] = ' / '.join(f'{t["tabella"]}.{t["colonna"]}' for t in trovate)
    return b
FAMIGLIA_AREA = {'morte': 'decessi', 'nascita': 'nascita'}
FONTE_FAMIGLIA = {'morte': 'Decessi_ANSC.xlsx', 'nascita': 'Nascite_ANSC_07.08.2026.xlsx'}


def _n(s):
    """Normalizza un'etichetta per il confronto: accenti, apostrofi, spazi, maiuscole."""
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.replace('’', "'").replace('‘', "'")
    return re.sub(r'[\s]+', ' ', s).strip().lower().rstrip(':').strip()


def risolutore(area='decessi', ent=None):
    """(maschera, etichetta) → campo del DTO → destinazione sul DB, con le evidenze.

    Si costruisce una volta per area applicativa. Per i decessi il salvataggio è uno solo
    (`/saveAttoDecessoData` di `SalvataggioAttoController`) perché le 11 maschere condividono
    lo stesso backbone: è il motivo per cui una sola catena copre tutte le varianti.
    """
    cfg = AREE[area]
    ent = ent if ent is not None else SD.entita()
    fe = os.path.join(BASE, cfg['fe'])
    etich, _ = SD.etichette(os.path.join(fe, 'messages.properties'))
    cat = {}
    for s in cfg['salvataggi']:
        s = s if os.path.isabs(s) else os.path.join(BASE, s)
        if not os.path.exists(s):
            continue
        for k, v in SD.catena(s, ent, cfg['moduli']).items():
            cat.setdefault(k, []).extend(v)
    maschere = os.path.join(fe, 'templates', cfg['templates'])
    per_maschera, ovunque, per_nome, nome_ovunque = {}, {}, {}, {}
    for f in sorted(os.listdir(maschere)):
        if not f.startswith(cfg['prefisso']):
            continue
        nome = f[:-5]
        for c in SD.campi_maschera(os.path.join(maschere, f), etich):
            voce = {
                'maschera': nome, 'campo_dto': c['campo'], 'etichetta': c['etichetta'],
                'certezza_etichetta': c['certezza'],
                'evidenza_maschera': f'{c["file"]}:{c["riga"]}',
                'destinazioni': cat.get(c['campo'], []),
            }
            # ⚠️ i campi senza etichetta NON si scartano: numeroAtto, anno, parte, serie ed
            # esponente sono <input hidden> valorizzati dal flusso di numerazione, e sono
            # proprio i campi che ANSC chiede (evento.numeroatto). Si indicizzano per nome.
            foglia = c['campo'].split('.')[-1]
            per_nome.setdefault((nome, foglia.lower()), voce)
            nome_ovunque.setdefault(foglia.lower(), voce)
            if c['etichetta']:
                per_maschera.setdefault((nome, _n(c['etichetta'])), voce)
                ovunque.setdefault(_n(c['etichetta']), voce)
    indice = {}
    for (m, et), v in per_maschera.items():
        indice.setdefault(m, []).append((et, v))
    return {'area': area, 'per_maschera': per_maschera, '_per_maschera_indice': indice,
            'ovunque': ovunque,
            'per_nome': per_nome, 'nome_ovunque': nome_ovunque, 'catena': cat, 'entita': ent}


RE_QUALIF = re.compile(r'^(.*?)\s*\(([^)]+)\)\s*$')


def _camel(etichetta):
    """«Data decesso» → «datadecesso»: la forma con cui confrontare il nome del campo."""
    return re.sub(r'[^a-z0-9]', '', _n(etichetta))


def risolvi_etichetta(ris, maschera, etichetta):
    """Trova il campo della maschera, dichiarando per quale via lo si è trovato.

    Le vie sono in ordine di forza: l'etichetta nella maschera dichiarata è l'evidenza piena;
    il nome del campo è altrettanto verificabile ma vale per i campi nascosti; il
    qualificatore fra parentesi («Data Atto (Ora)») è una lettura della ricognizione, e come
    tale va dichiarata; l'altra maschera è un'analogia, e va guardata prima di adottarla.
    """
    # ⚠️ la ricognizione scrive la maschera con annotazioni fra parentesi
    # («attoNascitaTipo03 (gemelli)»): senza normalizzarla ogni riscontro finirebbe declassato
    # a «altra maschera», che è falso
    maschera = re.sub(r'\s*\(.*?\)\s*', '', maschera or '').strip()
    e = _n(etichetta)
    v = ris['per_maschera'].get((maschera, e))
    if v:
        return v, 'etichetta nella maschera dichiarata', ''
    v = ris['per_nome'].get((maschera, _camel(etichetta)))
    if v:
        return v, 'nome del campo nella maschera dichiarata', ''
    q = RE_QUALIF.match(etichetta or '')
    if q:
        base, qual = _n(q.group(1)), _n(q.group(2))
        testa = base.split()[-1] if base else ''
        for et, voce in ris.setdefault('_per_maschera_indice', {}).get(maschera, ()):
            if qual in et.split() and testa and testa in et.split():
                return voce, 'qualificatore fra parentesi', ''
        v = ris['per_maschera'].get((maschera, base))
        if v:
            return v, 'campo di base del qualificatore', (
                f'Componente «{q.group(2)}» di un campo unico di SIPO: in SIPO il dato è uno '
                f'solo, in ANSC è diviso — la conversione lo scompone.')
    v = ris['ovunque'].get(e) or ris['nome_ovunque'].get(_camel(etichetta))
    if v:
        return v, 'altra maschera della stessa area', ''
    return None, '', ''


def _destinazione(voce):
    """La destinazione preferita fra quelle trovate: una colonna vera batte un nodo XML,
    e un nodo XML batte un esito ignoto. Le altre si conservano come annotazione."""
    d = voce.get('destinazioni') or []
    ordine = {'colonna': 0, 'xml': 1, 'ignoto': 2}
    return sorted(d, key=lambda b: ordine.get(b['genere'], 3))[0] if d else None


# --------------------------------------------------------------- conversioni SIPO → ANSC
def conversione(campo_ansc, dest):
    """Che cosa serve fare al dato di SIPO perché diventi il dato di ANSC.

    La classe di conversione del solo lato ANSC (in `mappatura_uc`) dice il genere del campo
    di destinazione; qui si guarda anche il TIPO DI PARTENZA, che è ciò che rende la
    conversione necessaria o superflua.
    """
    if not dest or dest['genere'] == 'ignoto':
        return '', ''
    tipo_sipo = dest.get('tipo_java', '')
    ansc_tipo = (campo_ansc or {}).get('tipo', '')
    ansc_formato = (campo_ansc or {}).get('formato', '')
    dec = (campo_ansc or {}).get('decodifica', '')
    if dest['genere'] == 'convenzione':
        base = ('Colonna proposta per convenzione dei nomi (il salvataggio passa da un '
                'ModelMapper): da confermare sul campo prima di configurarla.')
    elif dest['genere'] == 'xml':
        base = ('Estrazione da XML: il dato non è una colonna ma un nodo di '
                f'{dest["tabella"]}.{dest["colonna"]} ({dest["percorso_xml"]}). '
                'Va letto con XMLTABLE/XPath, e può essere assente nel documento.')
    else:
        base = ''
    parti = [base] if base else []
    if dest['genere'] == 'convenzione':
        parti = [base]
    if dec:
        parti.append(f'Traduzione di codifica: il valore SIPO è un identificativo locale, '
                     f'ANSC attende un codice della decodifica {dec} (dizionario replicato, '
                     f'RF-10).')
    elif re.search(r'id(Stato|Comune|Provincia|Nazionalita|Cittadinanza)', campo_ansc.get('percorso', '')
                   if campo_ansc else ''):
        parti.append('Traduzione territoriale: da ID locale (COMUNE/PROVINCIA/'
                     'CONF_STATO_ESTERO) al codice nazionale ANPR (CODICE_ANPR, DV-32).')
    if ansc_formato in ('date', 'date-time'):
        parti.append('Data: da DATE/Timestamp di Oracle a ISO 8601; attenzione alle date '
                     'parziali e al fatto che in SIPO data e ora sono spesso due campi.')
    if ansc_tipo == 'boolean':
        parti.append("Contrassegno: in SIPO è CHAR(1) S/N o un boolean del modello; "
                     "l'assenza del dato non equivale a «falso».")
    if ansc_tipo in ('integer', 'number') and tipo_sipo in ('String',):
        parti.append('Tipo: la sorgente è testo, la destinazione numerica.')
    if ansc_tipo == 'string' and tipo_sipo in ('BigDecimal', 'Long', 'Integer'):
        parti.append('Tipo: la sorgente è numerica, la destinazione testo.')
    if not parti:
        parti.append('Trasferimento diretto: restano da verificare lunghezza massima e '
                     'normalizzazione (in più punti SIPO applica toUpperCase in salvataggio).')
    return ('Sì' if len(parti) > 1 or base or dec else 'No'), ' '.join(parti)


def arricchisci(famiglia='morte', ris=None, modello=None, sipo=None, righe=None):
    """Le righe del mapping ANSC della famiglia, con il lato SIPO risolto fino alla colonna."""
    ris = ris or risolutore(FAMIGLIA_AREA.get(famiglia, 'decessi'))
    modello = modello or MU.Modello()
    sipo = sipo if sipo is not None else MU.lato_sipo(modello)
    righe = [r for r in (righe if righe is not None else MU.mappatura(modello, sipo))
             if r['famiglia'].lower().startswith(famiglia[:5])]
    fuori = []
    for r in righe:
        rec, proprio = None, False
        if r['binding']:
            noti = sipo.get(r['percorso'], [])
            # ordine di preferenza: l'UC stesso, poi la stessa famiglia, poi un'altra famiglia
            # (che si mostra ma si dichiara come tale: lo stesso percorso vale su soggetti
            # diversi — l'intestatario è il defunto oppure il neonato)
            proprio = any(s for s in noti if r['motore'] in s['motori'])
            rec = (next((s for s in noti if r['motore'] in s['motori']), None)
                   or next((s for s in noti if s['fonte'] == FONTE_FAMIGLIA.get(famiglia)), None)
                   or (noti[0] if noti else None))
        voce, grado, nota_comp = None, None, ''
        if rec:
            voce, grado, nota_comp = risolvi_etichetta(
                ris, rec.get('maschera', ''), rec['campo'])
        dest = _destinazione(voce) if voce else None
        if voce and (not dest or dest['genere'] == 'ignoto'):
            dest = per_convenzione(ris, voce['campo_dto']) or dest
        campo_ansc = {'tipo': r['tipo'], 'formato': r['formato'],
                      'decodifica': r['decodifica'], 'percorso': r['percorso']}
        serve, regola = conversione(campo_ansc, dest)
        if nota_comp:
            serve, regola = 'Sì', (nota_comp + ' ' + regola).strip()
        fuori.append(dict(
            r,
            sipo_ricognizione=rec['campo'] if rec else '',
            sipo_area=rec.get('area') or rec.get('gruppo') if rec else '',
            sipo_maschera=rec.get('maschera', '') if rec else '',
            sipo_riferito_a_questo_uc='Sì' if proprio else ('No' if rec else ''),
            sipo_campo_dto=voce['campo_dto'] if voce else '',
            sipo_grado=grado or '',
            sipo_certezza_etichetta=voce['certezza_etichetta'] if voce else '',
            sipo_tabella=dest.get('tabella', '') if dest else '',
            sipo_colonna=dest.get('colonna', '') if dest else '',
            sipo_percorso_xml=dest.get('percorso_xml', '') if dest else '',
            sipo_tipo_java=dest.get('tipo_java', '') if dest else '',
            sipo_genere=dest['genere'] if dest else '',
            sipo_ambiguo=dest.get('ambiguo', '') if dest else '',
            sipo_motivo=dest.get('motivo', '') if dest else (
                '' if not rec else 'etichetta della ricognizione non trovata fra i campi '
                                   'delle maschere'),
            evidenza_maschera=voce['evidenza_maschera'] if voce else '',
            evidenza_salvataggio=dest.get('evidenza', '') if dest else '',
            conversione_richiesta=serve,
            conversione_regola=regola,
        ))
    return fuori


if __name__ == '__main__':
    import sys
    import collections
    r = arricchisci(sys.argv[1] if len(sys.argv) > 1 else 'morte')
    campi = [x for x in r if x['binding']]
    print('righe di mapping (morte):', len(r), '· campi:', len(campi))
    print('con ricognizione SIPO:', sum(1 for x in campi if x['sipo_ricognizione']))
    print('con campo del DTO:', sum(1 for x in campi if x['sipo_campo_dto']))
    print('con colonna o nodo XML:', sum(1 for x in campi if x['sipo_colonna']))
    print(collections.Counter(x['sipo_genere'] for x in campi))
    print(collections.Counter(x['sipo_grado'] for x in campi))
    print()
    for x in campi[:14]:
        dove = (f'{x["sipo_tabella"]}.{x["sipo_colonna"]}{x["sipo_percorso_xml"]}'
                if x['sipo_colonna'] else '—')
        print(f'  {x["percorso"][:44]:46} {x["sipo_ricognizione"][:18]:20} {dove}')
