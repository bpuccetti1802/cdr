import { Component, Input, OnChanges, SimpleChanges, TemplateRef } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-grid',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './grid.component.html',
  styleUrls: ['./grid.component.scss'],
})
export class GridComponent implements OnChanges {
  /** Numero di righe da visualizzare */
  @Input() rows = 1;
  /** Numero di colonne da visualizzare */
  @Input() columns = 1;
  /** Breakpoint Bootstrap per le classi `.col-{breakpoint}-{n}` */
  @Input() breakpoint: 'sm' | 'md' | 'lg' | 'xl' = 'md';
  /**
   * Array opzionale di classi CSS per ogni colonna.
   * Ad es. ['col-md-4','col-md-8'] per due colonne di larghezza 4 e 8.
   * Se non fornito, calcola automaticamente `col-{breakpoint}-{12/columns}`.
   */
  @Input() colClasses?: string[];
  /**
   * Array opzionale di classi di offset per ogni colonna.
   * Ad es. ['','offset-md-2',''] per applicare un offset alla seconda colonna.
   */
  @Input() offsetClasses: string[] = [];
  /**
   * Matrice 2D di `TemplateRef` da iniettare in ciascuna cella.
   * Ogni cella riceve il corrispondente `TemplateRef` e il contesto `{ row, col }`.
   */
  @Input() cellTemplates: (TemplateRef<{ row: number; col: number }> | string)[][] = [];

  /** Array di indici per le righe */
  rowsArray: number[] = [];
  /** Array di indici per le colonne */
  colsArray: number[] = [];

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['rows']) {
      this.rowsArray = Array.from({ length: this.rows }, (_, index) => index);
    }
    if (changes['columns']) {
      this.colsArray = Array.from({ length: this.columns }, (_, index) => index);
    }
  }

  /** Restituisce la classe `.col-` da applicare a questa colonna */
  getColClass(index: number): string {
    if (this.colClasses && this.colClasses[index]) {
      return this.colClasses[index];
    }
    const width = Math.floor(12 / this.columns);
    return `col-${this.breakpoint}-${width}`;
  }

  /** Restituisce la classe `.offset-` da applicare a questa colonna */
  getOffsetClass(index: number): string {
    return this.offsetClasses[index] ?? '';
  }

  /** `trackBy` per ottimizzare il rendering delle righe e colonne */
  trackByIndex(_: number, index: number): number {
    return index;
  }

  isTemplate(cell: unknown): cell is TemplateRef<{ row: number; col: number }> {
    return cell instanceof TemplateRef;
  }
}
