export type RowSpanMap<T> = Partial<Record<Extract<keyof T, string>, number>>;

export class GroupByTableHelper {
  /**
   * Costruisce una chiave di raggruppamento per una riga,
   * combinando i valori delle colonne indicate in groupBy.
   */
  static buildGroupKey<T>(row: T, groupBy: Array<Extract<keyof T, string>>): string {
    // Usa un separatore per ridurre il rischio di sovrapposizioni
    // tra valori concatenati (es. ["1","23"] vs ["12","3"])
    return groupBy.map((k) => String(row[k] ?? '')).join('␟');
  }

  /**
   * Raggruppa le righe rendendo contigue quelle che condividono la stessa chiave
   * di grouping (groupBy) per permettere il corretto funzionamento del rowspan
   * @param rows righe da ordinare
   * @param groupBy array di nomi di colonna su cui effettuare il raggruppamento
   * @returns lista di righe ordinate per chiave di raggruppamento
   */
  static groupRowsForRowspan<T>(rows: T[], groupBy: Array<Extract<keyof T, string>>): T[] {
    if (rows.length === 0 || groupBy?.length === 0) return rows;

    // Mappa: chiave di gruppo - righe appartenenti a quel gruppo
    const rowGroup = new Map<string, T[]>();
    // Tiengo traccia dell’ordine di comparsa dei gruppi
    const groupOrder: string[] = [];

    // Distribuisco le righe nei rispettivi gruppi
    for (const row of rows) {
      // Costruisco la chiave di raggruppamento
      const key = this.buildGroupKey(row, groupBy);

      // Se è la prima volta che incontra questa chiave
      // inizializza il gruppo e ne registra l'ordine
      if (!rowGroup.has(key)) {
        rowGroup.set(key, []);
        groupOrder.push(key);
      }

      // Inserisce la riga nel gruppo corrispondente
      rowGroup.get(key)!.push(row);
    }

    // Ricompone l'array finale seguendo l'ordine dei gruppi e l'ordine interno di ogni gruppo
    const result: T[] = [];
    for (const key of groupOrder) {
      result.push(...(rowGroup.get(key) ?? []));
    }

    return result;
  }

  /**
   * Costruisce la mappa dei rowspan per il rendering di una tabella raggruppata a livello gerarchico
   *
   * Per ciascun livello di `groupBy`, identifica blocchi contigui di righe
   * con lo stesso valore e assegna:
   * - il rowspan corretto alla prima riga del blocco
   * - 0 alle righe successive
   *
   * Nota: richiede che le righe siano già ordinate per `groupBy`.
   *
   * @param rows lista dati in ingresso
   * @param groupBy array di chiavi di colonne da raggruppare
   * @returns un array di oggetti con la mappa dei rowspan
   */
  static calcRowSpansByHierarchy<T>(
    rows: T[],
    groupBy: Array<Extract<keyof T, string>>,
  ): RowSpanMap<T>[] {
    // Inizializzo una rowspan vuota per ogni riga
    const spans: RowSpanMap<T>[] = rows.map(() => ({}));

    // Se non ci sono dati o colonne nel groupBy ritorno la struttura vuota
    if (rows.length === 0 || groupBy?.length === 0) return spans;

    // Applico il groupBy livello per livello (es. primo elemento, poi secondo, ecc.)
    for (let level = 0; level < groupBy.length; level++) {
      const groupColumn = groupBy[level];
      let startIndex = 0;

      while (startIndex < rows.length) {
        // Trovo l'indice della prima row che non matcha con il gruppo
        const endIndex = this.findBlockEndIndex(rows, groupBy, groupColumn, level, startIndex);

        // Stabilisco la grandezza del gruppo
        const groupSize = endIndex - startIndex;

        // Applico alla prima riga del gruppo lo span corretto e alle altre lo imposta a 0
        spans[startIndex][groupColumn] = groupSize;
        for (let index = startIndex + 1; index < endIndex; index++) {
          spans[index][groupColumn] = 0;
        }

        startIndex = endIndex;
      }
    }

    return spans;
  }

  /**
   * Costruisce la mappa dei rowspan per il rendering di una tabella raggruppata a livello di chaive univoca
   *
   * Per ciascuna chiave composita di `groupBy` identifica blocchi contigui di righe
   * con gli stessi valori e assegna:
   * - il rowspan corretto alla prima riga del blocco
   * - 0 alle righe successive
   *
   * Nota: richiede che le righe siano già ordinate per `groupBy`.
   *
   * @param rows lista dati in ingresso
   * @param groupBy array di chiavi di colonne da raggruppare
   * @returns un array di oggetti con la mappa dei rowspan
   */
  static calcRowSpans<T>(rows: T[], groupBy: Array<Extract<keyof T, string>>): RowSpanMap<T>[] {
    // Inizializzo una rowspan vuota per ogni riga
    const spans: RowSpanMap<T>[] = rows.map(() => ({}));

    // Se non ci sono dati o colonne nel groupBy ritorno la struttura vuota
    if (rows.length === 0 || groupBy?.length === 0) return spans;

    let startIndex = 0;

    while (startIndex < rows.length) {
      // Estraggo la chiave di raggruppamento
      const groupByKey = this.buildGroupKey(rows[startIndex], groupBy);

      let endIndex = startIndex + 1;
      // Trovo l'indice della prima row che non matcha con il gruppo
      while (endIndex < rows.length && this.buildGroupKey(rows[endIndex], groupBy) === groupByKey) {
        endIndex++;
      }

      // Stabilisco la grandezza del gruppo
      const groupSize = endIndex - startIndex;

      // Applico lo stesso rowspan del gruppo a tutte le colonne del groupBy
      for (const col of groupBy) {
        spans[startIndex][col] = groupSize;
        for (let index = startIndex + 1; index < endIndex; index++) {
          spans[index][col] = 0;
        }
      }

      startIndex = endIndex;
    }

    return spans;
  }

  /**
   * Trova l’indice della riga successiva a quella finale delle righe da raggruppare
   */
  private static findBlockEndIndex<T>(
    rows: T[],
    groupBy: Array<Extract<keyof T, string>>,
    groupColumn: Extract<keyof T, string>,
    level: number,
    startIndex: number,
  ): number {
    const startRow = rows[startIndex];
    let index = startIndex + 1;

    // Continua finché il prefisso di grouping (livelli precedenti) è uguale
    // e il valore della colonna corrente è uguale
    while (
      index < rows.length &&
      this.hasSamePrefix(startRow, rows[index], groupBy, level) &&
      rows[index][groupColumn] === startRow[groupColumn]
    ) {
      index++;
    }

    return index;
  }

  /**
   * Verifica se due righe condividono lo stesso prefisso di grouping.
   *
   * Esempio:
   * groupBy = ['foglio', 'numero']
   * - livello 0 - nessun prefisso - sempre true
   * - livello 1 - confronta solo 'foglio'
   */
  private static hasSamePrefix<T>(
    a: T,
    b: T,
    groupBy: Array<Extract<keyof T, string>>,
    level: number,
  ): boolean {
    for (let index = 0; index < level; index++) {
      const col = groupBy[index];
      if (a[col] !== b[col]) {
        return false;
      }
    }
    return true;
  }
}
