# -*- coding: utf-8 -*-
"""L'albero dei dati di SIPO: il corrispettivo di `model_evento.yaml` per il lato comunale.

Il capitolo 9 dell'analisi stabilisce che il payload ANSC non si costruisce per UC ma una
volta sola sull'albero del modello evento. Il lato SIPO ha la stessa forma, e finora non era
stata usata: la maschera Thymeleaf scrive `th:field="*{padre.cognome}"`, cioè un PERCORSO
nell'albero del DTO radice (`AttoNascitaModel`, `AttoDecessoModel`), esattamente come il
mapping ANSC scrive `evento.datiGenitori.padre.cognome`.

    ANSC   ModelEvento          →  evento.datiGenitori.padre.cognome
    SIPO   AttoNascitaModel     →  padre.cognome        (GenitoreModel.cognome)
                                      ↓ maschera        attoNascitaTipo01.html:412, «Cognome»
                                      ↓ salvataggio     soggetto.setCognome(g.getCognome())
                                   SOGGETTO.COGNOME

Costruire i due alberi e raccordarli PER SOGGETTO è ciò che rende la mappatura verificabile:
il raccordo per solo nome di campo è inservibile, perché il mapping ANSC nomina «Cognome»
senza dire di chi, e una maschera di nascita ha undici cognomi diversi.

⚠️ Ogni riga porta la propria evidenza (`file:riga`) e il proprio grado di certezza. Dove la
catena si interrompe si scrive perché: una colonna proposta non è una colonna accertata.
"""
import glob
import os
import re

import sipo_dizionario as SD

BASE = SD.BASE

# Le due aree per cui esiste una ricognizione funzionale, e quindi le due che si possono
# mappare per intero. La radice è il DTO che il controller riceve nel corpo della POST di
# salvataggio: è la stessa classe che la maschera lega con th:object.
AREE = {
    'decessi': {
        'model_fe': 'front-end/decessi-web/DecessiWeb/src/main/java/it/romaCapitale/sipo/'
                    'decessiWeb/model',
        'radici': ['AttoDecessoModel'],
        'templates': 'front-end/decessi-web/DecessiWeb/src/main/resources/templates/'
                     'gestioneDecessi',
        'properties': 'front-end/decessi-web/DecessiWeb/src/main/resources/messages.properties',
        'prefisso_maschere': 'attoMorte',
        'salvataggi': ['back-end/decessi-be/DecessiBL/src/main/java/it/romaCapitale/sipo/'
                       'decessiBE/controller'],
        'moduli_entity': ('decessi-entities',),
    },
    'nascita': {
        'model_fe': 'front-end/nascita-web/NascitaWeb/src/main/java/it/romaCapitale/sipo/'
                    'nascitaWeb/model',
        'radici': ['AttoNascitaModel'],
        'templates': 'front-end/nascita-web/NascitaWeb/src/main/resources/templates/'
                     'gestioneNascita',
        'properties': 'front-end/nascita-web/NascitaWeb/src/main/resources/messages.properties',
        'prefisso_maschere': 'attoNascita',
        'salvataggi': ['back-end/nascita-be/NascitaBL/src/main/java/it/romaCapitale/sipo/'
                       'nascitaBE/controller'],
        # nascita-be persiste con le entity dello stato civile, non con entity proprie
        'moduli_entity': ('matrim-entities', 'anagrafe-entities'),
    },
}

RE_ATTRIBUTO = re.compile(
    r'^\s*(?:private|protected|public)\s+'
    r'([\w<>, .\[\]]+?)\s+(\w+)\s*(?:=[^;]*)?;')
RE_LISTA = re.compile(r'^(?:List|ArrayList|Set|Collection)<\s*([\w.]+)\s*>')


def _classe_utile(tipo):
    """Il nome della classe DTO dentro un tipo dichiarato, se è un DTO e non uno scalare."""
    tipo = tipo.strip()
    m = RE_LISTA.match(tipo)
    lista = bool(m)
    if m:
        tipo = m.group(1)
    tipo = tipo.split('.')[-1].replace('[]', '')
    return (tipo, lista) if tipo.endswith('Model') else (None, lista)


def classi_dto(area):
    """Nome della classe → {proprietà: (tipo, classe DTO, lista, riga)}, e il file.

    Si leggono le classi del FRONT-END: sono quelle che la maschera lega. Il back-end ha le
    stesse classi con lo stesso nome — il FE serializza il proprio modello e il BE lo
    deserializza nel proprio — e dove servisse il BE si cerca per nome di classe.
    """
    fuori = {}
    for radice in (AREE[area]['model_fe'],
                   'common/common-fe-be-sc/CommonFeBeSc/src/main/java',
                   'front-end/statocivile-web/StatoCivileWeb/src/main/java'):
        for f in glob.glob(os.path.join(BASE, radice, '**', '*Model.java'), recursive=True):
            classe = os.path.basename(f)[:-5]
            if classe in fuori:            # vince la classe dell'area: è quella che la
                continue                   # maschera dell'area lega davvero
            campi = {}
            for i, riga in enumerate(open(f, encoding='utf-8', errors='replace'), 1):
                nuda = riga.strip()
                if nuda.startswith(('//', '*', '/*')):
                    continue
                m = RE_ATTRIBUTO.match(riga)
                if not m or m.group(2) in ('serialVersionUID',):
                    continue
                tipo = m.group(1).strip()
                if tipo in ('class', 'static', 'final', 'return'):
                    continue
                dto, lista = _classe_utile(tipo)
                campi[m.group(2)] = {'tipo': tipo, 'dto': dto, 'lista': lista, 'riga': i}
            fuori[classe] = {'classe': classe, 'file': SD._rel(f), 'campi': campi}
    return fuori


class ModelloSipo:
    """Indice piatto dell'albero del DTO: percorso → caratteristiche del campo.

    Stessa forma della classe `Modello` di `mappatura_uc`, di proposito: i due alberi si
    confrontano, e confrontarli è più facile se hanno la stessa faccia.
    """

    def __init__(self, area):
        self.area = area
        self.classi = classi_dto(area)
        self.campi = {}
        for radice in AREE[area]['radici']:
            self._espandi(radice, '', {radice})

    def _espandi(self, classe, prefisso, visti):
        c = self.classi.get(classe)
        if not c:
            return
        for nome, v in c['campi'].items():
            perc = f'{prefisso}.{nome}' if prefisso else nome
            self.campi[perc] = {
                'percorso': perc, 'proprieta': nome, 'classe': classe,
                'tipo': v['tipo'], 'dto': v['dto'], 'lista': v['lista'],
                'evidenza': f'{c["file"]}:{v["riga"]}',
            }
            # ⚠️ la ricorsione si tronca alla ripetizione della classe, come per il modello
            # evento: `AttoNascitaModel` contiene dieci figli e ciascun figlio rimanda a
            # strutture che tornano indietro. Il troncamento va dichiarato, non subìto.
            if v['dto'] and v['dto'] in self.classi and v['dto'] not in visti:
                self._espandi(v['dto'], perc + ('[]' if v['lista'] else ''),
                              visti | {v['dto']})

    def foglie(self):
        return {k: v for k, v in self.campi.items() if not v['dto']}


# ------------------------------------------------------------------ le maschere
def maschere(area, etich=None):
    """percorso del DTO → elenco delle maschere che lo espongono, con etichetta ed evidenza.

    Un percorso compare in più maschere: se ne conservano tutte, perché l'insieme delle
    maschere in cui un campo compare è esattamente ciò che dice a quali Modelli di atto quel
    campo appartiene.
    """
    cfg = AREE[area]
    etich = etich if etich is not None else SD.etichette(
        os.path.join(BASE, cfg['properties']))[0]
    cartella = os.path.join(BASE, cfg['templates'])
    fuori = {}
    for f in sorted(os.listdir(cartella)):
        if not (f.startswith(cfg['prefisso_maschere']) and f.endswith('.html')):
            continue
        nome = f[:-5]
        for c in SD.campi_maschera(os.path.join(cartella, f), etich):
            perc = re.sub(r'\[\d+\]', '[]', c['campo'])
            fuori.setdefault(perc, []).append({
                'maschera': nome, 'etichetta': c['etichetta'],
                'certezza_etichetta': c['certezza'],
                'evidenza': f'{c["file"]}:{c["riga"]}',
            })
    return fuori


# ------------------------------------------------------------------ le destinazioni sul DB
def destinazioni(area, ent=None):
    """(classe DTO, proprietà) → destinazione sul DB, letta dai salvataggi del back-end.

    La chiave è la CLASSE, non la variabile: il salvataggio scrive `soggetto.setCognome(
    g.getCognome())` dentro un metodo che riceve `GenitoreModel g`, e quel metodo vale per il
    padre come per la madre. Ancorare alla classe è ciò che permette di risolvere
    `padre.cognome` e `madre.cognome` con la stessa evidenza, senza confonderli fra loro.
    """
    cfg = AREE[area]
    ent = ent if ent is not None else SD.entita(('common', 'back-end'))
    cost = costanti(area)
    fuori = {}
    for radice in cfg['salvataggi']:
        for f in sorted(glob.glob(os.path.join(BASE, radice, '*.java'))):
            for (classe, prop), b in _catena_per_classe(f, ent, cfg['moduli_entity'],
                                                        cost).items():
                fuori.setdefault((classe, prop), []).extend(b)
    return fuori


RE_PARAM = re.compile(r'\b(?:private|public|protected)\s+[\w<>\[\], .]+?\s+(\w+)\s*\(([^)]*)\)')
RE_TIPO_VAR = re.compile(r'^([A-Z][\w.]*)\s+(\w+)$')


def _sorgenti_dto(testo):
    """variabile → classe DTO, per i parametri di metodo e le dichiarazioni locali.

    ⚠️ È il punto che prima mancava: la catena riconosceva la sola variabile letterale «ip»,
    e perdeva le 222 assegnazioni che in `SalvataggioController` passano per «n», più tutte
    quelle dei metodi ausiliari. Il DTO non si riconosce dal nome ma dal TIPO.
    """
    fuori = {}
    for m in RE_PARAM.finditer(testo):
        for par in m.group(2).split(','):
            par = re.sub(r'@\w+(\([^)]*\))?', '', par).strip()
            t = RE_TIPO_VAR.match(par)
            if t and t.group(1).endswith('Model'):
                fuori[t.group(2)] = t.group(1).split('.')[-1]
    for m in re.finditer(r'\b([A-Z][\w.]*Model)\s+(\w+)\s*=', testo):
        fuori.setdefault(m.group(2), m.group(1).split('.')[-1])
    return fuori


RE_COSTANTE = re.compile(r'static\s+final\s+String\s+(\w+)\s*=\s*"([^"]*)"')
RE_ESTESO = re.compile(r'\b\w*[Ee]xtend\s*\(\s*"([A-Z0-9_]+)"\s*,')
RE_MAP_PUT = re.compile(r'\bmap\.(?:put|get)\s*\(\s*(?:\w+\.)?([A-Z][A-Z0-9_]*)')


def costanti(area):
    """Nome della costante → valore, per le classi `Costanti*` dell'area.

    Servono perché la chiave con cui il dato è scritto nei campi estesi non è nel testo della
    riga ma in una costante: `map.put(CostantiSalvataggioRicerca.CONIUGENOME, …)` scrive un
    campo che sul DB si chiama «CONIUGE_NOME».
    """
    fuori = {}
    for radice in AREE[area]['salvataggi']:
        base = os.path.dirname(os.path.join(BASE, radice))
        for f in glob.glob(os.path.join(base, '**', 'Costanti*.java'), recursive=True):
            for m in RE_COSTANTE.finditer(open(f, encoding='utf-8', errors='replace').read()):
                fuori.setdefault(m.group(1), m.group(2))
    return fuori


def _catena_per_classe(percorso_java, ent, moduli, cost=None):
    """Come `SD.catena`, ma la sorgente è dichiarata dal tipo e la chiave è (classe, catena).

    Riconosce tre forme che la lettura per sola assegnazione perdeva, e tutte e tre cambiano
    ciò che si deve scrivere nella configurazione:

      · FUSIONE — `attoDec.setDataInsAtto(improveDataOra(ip.getDataAtto(), ip.getOraAtto()))`
        porta DUE campi del DTO in UNA colonna. ANSC li rivuole separati (data, ora, minuto):
        registrarne uno solo nasconderebbe metà del lavoro di conversione.
      · CAMPO ESTESO — `setAttoDecessiExtend("FLG_ORA_DECESSO_OMESSA", …)` non scrive una
        colonna ma una riga chiave/valore in ATTO_DECESSO_EXTEND.
      · EXTRAFIELDS — `map.put(CONIUGENOME, …)` finisce dentro l'XML di SOGGETTO, nel
        contenitore generico EXTRAFIELDS/FIELD.
    """
    testo = open(percorso_java, encoding='utf-8', errors='replace').read()
    dto = _sorgenti_dto(testo)
    if not dto:
        return {}
    cost = cost if cost is not None else {}
    scritture, decl = SD.assegnazioni(percorso_java)
    decl = SD.indice_decl(decl)
    lettura = re.compile(r'\b(' + '|'.join(sorted(map(re.escape, dto), key=len, reverse=True))
                         + r')\.((?:get|is)\w+\(\)(?:\.(?:get|is)\w+\(\))*)')
    righe = testo.splitlines()
    rel = SD._rel(percorso_java)
    fuori = {}

    def registra(classe, catena, b):
        fuori.setdefault((classe, catena), []).append(b)

    for i, riga in enumerate(righe, 1):
        letture = list(lettura.finditer(riga))
        if not letture:
            continue
        campi = [(dto[g.group(1)],
                  re.sub(r'(?:get|is)(\w+)\(\)',
                         lambda m: m.group(1)[0].lower() + m.group(1)[1:], g.group(2)))
                 for g in letture]
        # ---- campo esteso: la chiave è la stringa letterale del primo argomento
        e = RE_ESTESO.search(riga)
        if e:
            tab = ('ATTO_NASCITA_EXTEND' if 'ascit' in rel else 'ATTO_DECESSO_EXTEND')
            for classe, catena in campi:
                registra(classe, catena, {
                    'genere': 'esteso', 'tabella': tab, 'colonna': 'VALUE',
                    'chiave_estesa': e.group(1), 'tipo_java': 'String',
                    'evidenza': f'{rel}:{i}',
                    'motivo': f'Campo esteso: riga chiave/valore in {tab} con '
                              f'ID_EXT_FIELD = «{e.group(1)}», non una colonna.'})
            continue
        # ---- EXTRAFIELDS dentro l'XML: la chiave viene dalla costante vicina
        if '.put(' in riga and 'VALUE' in riga:
            chiave = ''
            for j in range(max(0, i - 9), min(len(righe), i + 9)):
                m = RE_MAP_PUT.search(righe[j])
                if m and m.group(1) not in ('VALUE', 'TYPE', 'NAME', 'STRING'):
                    chiave = cost.get(m.group(1), m.group(1))
                    break
            if chiave:
                for classe, catena in campi:
                    registra(classe, catena, {
                        'genere': 'xml', 'tabella': 'SOGGETTO',
                        'colonna': 'DETTAGLIO_STATOCIVILE',
                        'percorso_xml': f'/EXTRAFIELDS/FIELD[NAME="{chiave}"]/VALUE',
                        'tipo_java': 'String', 'evidenza': f'{rel}:{i}',
                        'motivo': 'Contenitore generico EXTRAFIELDS dell’XML del soggetto: '
                                  'il dato non ha una colonna propria.'})
                continue
        # ---- assegnazione ordinaria (eventualmente con più campi fusi in una colonna)
        s = SD.RE_SET.search(riga)
        if not s:
            continue
        prop = s.group(2)
        scrittura = {'oggetto': s.group(1), 'proprieta': prop[0].lower() + prop[1:],
                     'riga': i, 'file': rel}
        b = SD.bersaglio(scrittura, decl, ent, moduli)
        b['evidenza'] = f'{rel}:{i}'
        for classe, catena in campi:
            v = dict(b)
            if len(campi) > 1:
                v['fusione'] = ' + '.join(c for _, c in campi)
                v['motivo'] = (v.get('motivo', '') + ' ' if v.get('motivo') else '') + (
                    f'Più campi della maschera confluiscono in una sola colonna '
                    f'({v["fusione"]}): la conversione verso ANSC deve ricomporli o '
                    f'separarli.')
            registra(classe, catena, v)
    return fuori


# ------------------------------------------------------------------ l'albero risolto
def proietta(modello, dest):
    """Le destinazioni lette dal codice, riportate sui percorsi dell'albero.

    ⚠️ Il salvataggio legge il DTO in due forme, e servono entrambe: dalla radice
    (`ip.getDeceduto().getCognome()`, ed è la forma dei decessi) o da una classe intermedia
    (`g.getCognome()` dentro un metodo che riceve `GenitoreModel g`, ed è la forma delle
    nascite). La seconda vale per TUTTI i nodi di quella classe — padre, madre e dichiarante
    insieme — ed è proprio questa moltiplicazione che rende il metodo unico riusabile.
    """
    # prefisso dell'albero → classe DTO che vi risiede; la radice è il prefisso vuoto
    prefissi = {'': [r for r in AREE[modello.area]['radici']]}
    for perc, c in modello.campi.items():
        if c['dto']:
            prefissi.setdefault(perc, []).append(c['dto'])
    per_classe = {}
    for perc, classi in prefissi.items():
        for cl in classi:
            per_classe.setdefault(cl, []).append(perc)
    fuori = {}
    for (classe, catena), v in dest.items():
        for prefisso in per_classe.get(classe, ()):
            perc = f'{prefisso}.{catena}' if prefisso else catena
            if perc in modello.campi:
                fuori.setdefault(perc, []).extend(v)
    return fuori


_ALBERI = {}


def albero(area, ent=None):
    """L'albero SIPO con, per ogni foglia, le maschere che la espongono e la sua colonna.

    Il risultato si tiene in memoria: costruirlo significa rileggere tutti i salvataggi
    dell'area, e nella stessa esecuzione lo chiedono sia il ponte sia il foglio inverso.
    """
    if area in _ALBERI:
        return _ALBERI[area]
    m = ModelloSipo(area)
    masc = maschere(area)
    dest = proietta(m, destinazioni(area, ent))
    ordine = {'colonna': 0, 'xml': 1, 'ignoto': 2}
    fuori = {}
    for perc, c in m.campi.items():
        viste = masc.get(perc, [])
        cand = dest.get(perc, [])
        d = sorted(cand, key=lambda b: ordine.get(b['genere'], 3))[0] if cand else None
        # ⚠️ più destinazioni con tabelle diverse per lo stesso percorso non sono un dettaglio:
        # o il dato è scritto in due punti (accade: SOGGETTO e il suo XML), oppure la lettura
        # del codice ha sbagliato ancoraggio. In entrambi i casi va dichiarato.
        tabelle = {f'{b.get("tabella")}.{b.get("colonna")}' for b in cand
                   if b['genere'] in ('colonna', 'xml')}
        fuori[perc] = dict(
            c,
            maschere=[v['maschera'] for v in viste],
            etichetta=next((v['etichetta'] for v in viste if v['etichetta']), ''),
            certezza_etichetta=next((v['certezza_etichetta'] for v in viste
                                     if v['etichetta']), ''),
            evidenza_maschera=viste[0]['evidenza'] if viste else '',
            destinazione=d,
            destinazioni=cand,
            ambiguo=' / '.join(sorted(tabelle)) if len(tabelle) > 1 else '',
        )
    _ALBERI[area] = fuori
    return fuori


if __name__ == '__main__':
    import collections
    ent = SD.entita(('common', 'back-end'))
    for area in AREE:
        a = albero(area, ent)
        foglie = {k: v for k, v in a.items() if not v['dto']}
        con_masc = {k: v for k, v in foglie.items() if v['maschere']}
        con_col = {k: v for k, v in con_masc.items()
                   if v['destinazione'] and v['destinazione']['genere'] != 'ignoto'}
        print(f'=== {area}')
        print(f'   classi DTO lette      {len(ModelloSipo(area).classi)}')
        print(f'   percorsi dell albero  {len(a)}  (foglie {len(foglie)})')
        print(f'   foglie in maschera    {len(con_masc)}')
        print(f'   con colonna o XML     {len(con_col)}')
        g = collections.Counter(v['destinazione']['genere'] for v in con_masc.values()
                                if v['destinazione'])
        print(f'   destinazioni          {dict(g)}')
        for k in list(con_col)[:6]:
            v = con_col[k]
            d = v['destinazione']
            print(f'     {k[:38]:40} «{v["etichetta"][:22]:24}» '
                  f'{d.get("tabella")}.{d.get("colonna")}')
