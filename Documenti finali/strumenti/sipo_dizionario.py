# -*- coding: utf-8 -*-
"""Dizionario del lato SIPO: dalla maschera alla colonna Oracle, leggendo il codice.

La ricognizione funzionale nomina i campi con l'ETICHETTA della maschera («Data decesso»);
la configurazione ANSC ha bisogno della COLONNA (`ATTO_DECESSO.DATA_DECESSO`). Il legame non
sta in nessun documento: sta nel codice, in tre anelli che si tengono per nome.

    etichetta          messages.properties      label.dataDecesso = Data decesso
      ↓                template Thymeleaf       th:field="*{dataDecesso}"
    proprietà del DTO  (FE e BE hanno la stessa forma: il FE serializza il proprio modello)
      ↓                controller di salvataggio  attoDec.setDataDecesso(ip.getDataDecesso())
    proprietà entity   @Column(name="DATA_DECESSO")  su @Table(name="ATTO_DECESSO")
      ↓
    COLONNA

⚠️ Non tutto finisce in una colonna: `SOGGETTO` ha nove colonne e un XMLType
`DETTAGLIO_STATOCIVILE` che contiene cittadinanza, stato civile, residenza, nascita e perfino
un contenitore generico EXTRAFIELDS/FIELD. Per quei dati la «colonna» è un percorso XML, e va
detto, non nascosto.

Ogni risultato porta la propria evidenza (file:riga): è la regola del workspace, non si
afferma nulla che non si possa ricondurre a una sorgente.
"""
import glob
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SALVATAGGIO_DECESSI = os.path.join(
    BASE, 'back-end', 'decessi-be', 'DecessiBL', 'src', 'main', 'java', 'it', 'romaCapitale',
    'sipo', 'decessiBE', 'controller', 'SalvataggioAttoController.java')
MASCHERE_DECESSI = os.path.join(
    BASE, 'front-end', 'decessi-web', 'DecessiWeb', 'src', 'main', 'resources')


def _rel(p):
    return os.path.relpath(p, BASE)


# ------------------------------------------------------------------ entity JPA
RE_TABELLA = re.compile(r'@Table\s*\(\s*name\s*=\s*"([^"]+)"')
RE_COLONNA = re.compile(r'@(?:Column|JoinColumn)\s*\(([^)]*)\)', re.S)
RE_NOME = re.compile(r'name\s*=\s*"([^"]+)"')
RE_DICHIARA = re.compile(r'private\s+([\w<>\[\], .]+?)\s+(\w+)\s*;')


def entita(radici=('common',)):
    """Nome della classe entity → tabella, e proprietà → colonna.

    Si legge il sorgente riga per riga perché l'annotazione precede la dichiarazione: la
    coppia si forma per adiacenza, che è esattamente come la scrive lo sviluppatore.
    """
    fuori = {}
    for radice in radici:
        for f in glob.glob(os.path.join(BASE, radice, '**', 'entities', '*.java'),
                           recursive=True):
            testo = open(f, encoding='utf-8', errors='replace').read()
            m = RE_TABELLA.search(testo)
            if not m:
                continue
            classe = os.path.basename(f)[:-5]
            campi = {}
            colonna = None
            for i, riga in enumerate(testo.splitlines(), 1):
                nuda = riga.strip()
                if nuda.startswith('//') or nuda.startswith('*') or nuda.startswith('/*'):
                    continue
                c = RE_COLONNA.search(riga)
                if c:
                    n = RE_NOME.search(c.group(1))
                    colonna = (n.group(1) if n else None, 'XMLType' in c.group(1))
                    continue
                d = RE_DICHIARA.search(riga)
                if d and colonna and colonna[0]:
                    campi[d.group(2)] = {
                        'colonna': colonna[0], 'tipo_java': d.group(1).strip(),
                        'xmltype': colonna[1], 'riga': i,
                    }
                    colonna = None
                elif d:
                    colonna = None
            # ⚠️ la stessa classe esiste in più moduli e le varianti DIVERGONO (CONF_STATO_ESTERO
            # ne è l'esempio noto): si conservano tutte, e chi interroga dichiara il modulo.
            modulo = _rel(f).split(os.sep)[1]
            fuori.setdefault(classe, []).append(
                {'classe': classe, 'modulo': modulo, 'tabella': m.group(1),
                 'file': _rel(f), 'campi': campi})
    return fuori


def cerca_entita(ent, classe, moduli=()):
    """La variante della classe nel modulo preferito, altrimenti la prima disponibile."""
    v = ent.get(classe) or []
    for m in moduli:
        for x in v:
            if x['modulo'] == m:
                return x
    return v[0] if v else None


# ------------------------------------------------------------------ etichette di maschera
RE_ETICHETTA = re.compile(r'^\s*(label\.[\w.]+)\s*=\s*(.*?)\s*$')


def etichette(percorso_properties):
    """chiave → testo dell'etichetta. ⚠️ Il file ha chiavi ripetute: vince l'ultima, come
    fa Java, e le ripetizioni si segnalano perché sono una fonte di ambiguità reale."""
    fuori, ripetute = {}, set()
    for riga in open(percorso_properties, encoding='utf-8', errors='replace'):
        m = RE_ETICHETTA.match(riga)
        if not m:
            continue
        k, v = m.group(1), m.group(2)
        if k in fuori and fuori[k] != v:
            ripetute.add(k)
        fuori[k] = v
    return fuori, ripetute


RE_CAMPO_HTML = re.compile(r'th:field\s*=\s*"\*\{([\w.\[\]]+)\}"')
RE_LABEL_HTML = re.compile(r'#\{(label\.[\w.]+)\}')
RE_TAG = re.compile(r'<\s*(input|select|textarea|label)\b', re.I)
RE_FRAMMENTO = re.compile(r'th:(?:insert|replace|include)\s*=\s*"([\w/]+)\s*::')
ETI_DECORATIVE = {'label.obbligatorio', 'label.facoltativo', 'label.obbligatorioCondizionale'}


def campi_maschera(percorso_html, etich):
    """Coppie (etichetta, proprietà) nell'ordine in cui compaiono nel template.

    Le etichette e i controlli non sono annidati nello stesso tag: il template dichiara prima
    la riga di etichette, poi la riga di controlli. Si appaiano per SEQUENZA all'interno del
    blocco, che è l'unica relazione che il markup esprime davvero.
    """
    testo = open(percorso_html, encoding='utf-8', errors='replace').read()
    campi, lab = [], []
    for i, riga in enumerate(testo.splitlines(), 1):
        if riga.strip().startswith('<!--'):
            continue
        for m in RE_LABEL_HTML.finditer(riga):
            if m.group(1) not in ETI_DECORATIVE:
                lab.append((m.group(1), i))
        for m in RE_CAMPO_HTML.finditer(riga):
            # lo stesso campo compare due volte quando il template ha due rami th:if
            if not campi or campi[-1][0] != m.group(1):
                campi.append((m.group(1), i))
    per_nome = {}
    for k, r in lab:
        per_nome.setdefault(k[len('label.'):].lower(), (k, r))
    fuori = []
    # i frammenti sono parte della maschera: il campo che l'utente vede sta lì dentro, e il
    # percorso di binding e' gia' completo (*{deceduto.cognome}), quindi si accodano e basta
    fuori = []
    radice = os.path.dirname(os.path.dirname(percorso_html))
    for m in RE_FRAMMENTO.finditer(testo):
        f = os.path.join(radice, m.group(1) + '.html')
        if os.path.exists(f):
            fuori.extend(campi_maschera(f, etich))
    for j, (campo, riga) in enumerate(campi):
        foglia = campo.split('.')[-1].split('[')[0]
        k, r = per_nome.get(foglia.lower(), (None, None))
        certezza = 'nome'
        if not k:                       # ripiego: la sequenza del markup
            k, r = lab[j] if j < len(lab) else (None, None)
            certezza = 'sequenza'
        fuori.append({'campo': campo, 'chiave': k, 'certezza': certezza if k else '',
                      'etichetta': etich.get(k, '') if k else '',
                      'riga': riga, 'riga_etichetta': r, 'file': _rel(percorso_html)})
    return fuori


# ------------------------------------------------------------------ assegnazioni del BE
RE_DECL = re.compile(r'\b([A-Z]\w+)\s+(\w+)\s*=\s*([^;]*)')
RE_SET = re.compile(r'\b(\w+)\.set([A-Z]\w*)\s*\(')
RE_GET = re.compile(r'\bip\.((?:get\w+\(\)\.)*get\w+\(\))')


def assegnazioni(percorso_java):
    """Assegnazioni e dichiarazioni del salvataggio, nell'ordine in cui compaiono.

    È un'analisi per espressione, non un parser Java: legge la riga, non il programma. Basta
    perché il salvataggio è scritto in forma piatta — un'assegnazione per riga — ma il limite
    va dichiarato: un'assegnazione spezzata su più righe non viene vista. Le dichiarazioni si
    tengono in LISTA e non in dizionario, perché lo stesso nome (`nascita`) è dichiarato una
    volta per soggetto: vale la più vicina che precede, non la prima incontrata.
    """
    decl, scritture = [], []
    for i, riga in enumerate(open(percorso_java, encoding='utf-8', errors='replace'), 1):
        nuda = riga.strip()
        if nuda.startswith('//') or nuda.startswith('*'):
            continue
        for m in RE_DECL.finditer(riga):
            decl.append({'riga': i, 'var': m.group(2), 'classe': m.group(1),
                         'init': m.group(3).strip()})
        s = RE_SET.search(riga)
        if not s:
            continue
        g = RE_GET.search(riga)
        prop = s.group(2)
        scritture.append({
            'oggetto': s.group(1), 'proprieta': prop[0].lower() + prop[1:],
            'dto': re.sub(r'get(\w+)\(\)', lambda m: m.group(1)[0].lower() + m.group(1)[1:],
                          g.group(1)) if g else '',
            'riga': i, 'file': _rel(percorso_java),
        })
    return scritture, decl


def indice_decl(decl):
    """Le dichiarazioni raggruppate per nome di variabile.

    Serve solo a non ripercorrere l'intera lista per ogni assegnazione: su un controller di
    tremila righe la ricerca lineare rende quadratica la lettura dell'intero file.
    """
    fuori = {}
    for d in decl:
        fuori.setdefault(d['var'], []).append(d)
    return fuori


def _dichiarazione(decl, var, riga):
    """La dichiarazione di `var` più vicina che precede la riga: è l'ambito, approssimato."""
    candidate = decl.get(var, ()) if isinstance(decl, dict) else (
        d for d in decl if d['var'] == var)
    trovate = [d for d in candidate if d['riga'] <= riga]
    return trovate[-1] if trovate else None


RE_XML = re.compile(r'unmarshallerObj\s*\(\s*(\w+)\.getDettaglio\w*\(\)')
RE_PADRE = re.compile(r'^(\w+)\.get(\w+)\(\)')


def bersaglio(scrittura, decl, ent, moduli=()):
    """Dove finisce il dato: una colonna, oppure un nodo dell'XML dentro una colonna.

    Risale la catena delle dichiarazioni finché non incontra una entity (→ tabella) o
    l'estrazione dell'XMLType (→ percorso XML). Restituisce sempre anche l'evidenza.
    """
    var, nodi, visti = scrittura['oggetto'], [], 0
    riga = scrittura['riga']
    while visti < 8:
        visti += 1
        d = _dichiarazione(decl, var, riga)
        classe = d['classe'] if d else None
        e = cerca_entita(ent, classe, moduli) if classe else None
        if e:
            if nodi:                      # si scriveva in un oggetto JAXB dentro l'XMLType
                col = next((c for c in e['campi'].values() if c['xmltype']), None)
                return {'genere': 'xml',
                        'tabella': e['tabella'],
                        'colonna': col['colonna'] if col else 'DETTAGLIO_STATOCIVILE',
                        'percorso_xml': '/' + '/'.join(reversed(nodi)) + '/'
                                        + scrittura['proprieta'].upper(),
                        'tipo_java': 'XMLType', 'entity': classe,
                        'riga_entity': col['riga'] if col else None}
            c = e['campi'].get(scrittura['proprieta'])
            if not c:
                return {'genere': 'ignoto', 'entity': classe, 'tabella': e['tabella'],
                        'motivo': f'la proprietà {scrittura["proprieta"]} non è una colonna '
                                  f'di {e["tabella"]}'}
            return {'genere': 'colonna', 'tabella': e['tabella'], 'colonna': c['colonna'],
                    'tipo_java': c['tipo_java'], 'entity': classe, 'riga_entity': c['riga']}
        if not d:
            return {'genere': 'ignoto', 'motivo': f'variabile «{var}» non dichiarata nel file'}
        x = RE_XML.search(d['init'])
        if x:                             # ...SSC = unmarshaller(<soggetto>.getDettaglio...())
            nodi.append(d['classe'])
            var, riga = x.group(1), d['riga']
            continue
        pad = RE_PADRE.match(d['init'])
        if pad:
            # il nome del getter È il nodo XML (getNASCITA() → NASCITA): si accoda sempre,
            # anche quando coincide col nome della classe, altrimenti il ramo si perde
            nodi.append(pad.group(2))
            var, riga = pad.group(1), d['riga']
            continue
        return {'genere': 'ignoto', 'entity': d['classe'],
                'motivo': f'la variabile «{var}» ({d["classe"]}) nasce da «{d["init"][:60]}»'}
    return {'genere': 'ignoto', 'motivo': 'catena di dichiarazioni troppo lunga'}


def catena(percorso_java, ent, moduli=()):
    """percorso del DTO (es. «deceduto.cognome») → elenco delle destinazioni sul DB."""
    scritture, decl = assegnazioni(percorso_java)
    fuori = {}
    for s in scritture:
        if not s['dto']:
            continue
        b = bersaglio(s, decl, ent, moduli)
        b['evidenza'] = f'{s["file"]}:{s["riga"]}'
        fuori.setdefault(s['dto'], []).append(b)
    return fuori


if __name__ == '__main__':
    e = entita()
    var = [x for v in e.values() for x in v]
    print('classi entity distinte:', len(e), '· varianti per modulo:', len(var))
    print('tabelle distinte:', len({x['tabella'] for x in var}))
    print('colonne mappate:', sum(len(x['campi']) for x in var))
    for c in ('AttoDecesso', 'SoggettoDec', 'AttoDec'):
        x = cerca_entita(e, c, ('decessi-entities',))
        if x:
            print(f'  {c:14} {x["tabella"]:22} {len(x["campi"]):3} colonne  [{x["modulo"]}, '
                  f'{len(e[c])} varianti]')
    base = os.path.join(BASE, 'front-end', 'decessi-web', 'DecessiWeb', 'src', 'main', 'resources')
    et, rip = etichette(os.path.join(base, 'messages.properties'))
    print('etichette:', len(et), '· chiavi ripetute con testo diverso:', len(rip))
    cm = campi_maschera(os.path.join(base, 'templates', 'gestioneDecessi', 'attoMorteTipo01.html'), et)
    print('campi in attoMorteTipo01:', len(cm), '· con etichetta:', sum(1 for x in cm if x['etichetta']))
    for x in cm[:8]:
        print(f'    {x["etichetta"][:34]:36} → *{{{x["campo"]}}}  (riga {x["riga"]})')
    sc, de = assegnazioni(SALVATAGGIO_DECESSI)
    print('assegnazioni:', len(sc), '· con sorgente DTO:', sum(1 for x in sc if x['dto']),
          '· dichiarazioni:', len(de))
    cat = catena(SALVATAGGIO_DECESSI, e, ('decessi-entities',))
    import collections
    g = collections.Counter(b['genere'] for v in cat.values() for b in v)
    print('percorsi del DTO risolti:', len(cat), '·', dict(g))
    for k in ('deceduto.cognome', 'dataDecesso', 'deceduto.cittadinanza',
              'deceduto.comuneNascita', 'luogoDecesso', 'dichiarante.comuneResidenza'):
        for b in cat.get(k, [])[:1]:
            dove = (f'{b.get("tabella")}.{b.get("colonna")}' if b['genere'] != 'ignoto'
                    else 'IGNOTO: ' + b.get('motivo', ''))
            print(f'  {k:30} → {dove}{"  " + b.get("percorso_xml", "") if b["genere"] == "xml" else ""}')
