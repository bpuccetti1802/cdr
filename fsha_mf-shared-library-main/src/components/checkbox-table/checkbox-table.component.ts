import { CommonModule } from '@angular/common';
import {
  AfterViewInit,
  Component,
  ElementRef,
  EventEmitter,
  HostListener,
  Injector,
  Input,
  OnChanges,
  OnInit,
  Output,
  QueryList,
  SimpleChanges,
  Type,
  ViewChild,
  ViewChildren,
} from '@angular/core';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import {
  faDownload,
  faEllipsisVertical,
  faEye,
  faPenToSquare,
  faTrash,
  IconDefinition,
} from '@fortawesome/free-solid-svg-icons';
import { IconComponent } from '@mf/components/icon/icon.component';
import { CheckboxTableRowProperties, Colors, IconSize } from 'test-library-frankmd93';
import { CardWrapperComponent } from '../card-wrapper/card-wrapper.component';
import { CheckboxComponent } from '../form-elements/checkbox/checkbox.component';

/**
 * @deprecated use version from test-library
 */
interface TableColumns {
  id: keyof unknown;
  label: string;
  width?: string;
  class?: string;
  selectable?: boolean;
  hidden?: boolean;
  maxWidth?: string;
  sortDirection?: 'asc' | 'desc' | null;
}

/**
 * @deprecated use version from test-library
 */
interface ReactCellSpec {
  type: unknown;
  props: Record<string, unknown>;
}
@Component({
  selector: 'app-rc-checkbox-table',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    FontAwesomeModule,
    IconComponent,
    CardWrapperComponent,
    CheckboxComponent,
  ],
  templateUrl: './checkbox-table.component.html',
  styleUrl: './checkbox-table.component.scss',
})
export class CheckboxTableComponent<T extends CheckboxTableRowProperties>
  implements OnChanges, AfterViewInit, OnInit
{
  private static _seq = 0;
  readonly uid = `rc-ckx-${++CheckboxTableComponent._seq}`;

  faEye: IconDefinition = faEye;
  faEllipsisVertical: IconDefinition = faEllipsisVertical;
  faPenToSquare: IconDefinition = faPenToSquare;
  faTrash: IconDefinition = faTrash;
  faDownload: IconDefinition = faDownload;
  IconSize = IconSize;
  @Input() serverPaginated: boolean = false;
  @Input() totalItems?: number = 0;
  @Input() shouldShowAllItems = false;
  // si può disabilitare l'action a livello di elemento con baserow con boolean actionView,actionEdit,actionDelete,actionDownload.
  @Input() actionView?: boolean; // Necessario per far comparire correttamente la testata della tabella quando gli elementi hanno l'action se si passa a livello di base row actionView true l'action nel menu si vedra' e sarà abilitata
  @Input() actionEdit?: boolean; // Necessario per far comparire correttamente la testata della tabella quando gli elementi hanno l'action se si passa a livello di base row actionEdit true l'action nel menu si vedra' e sarà abilitata
  @Input() actionDelete?: boolean; // Necessario per far comparire correttamente la testata della tabella quando gli elementi hanno l'action se si passa a livello di base row actionDelete true l'action nel menu si vedra' e sarà abilitata
  @Input() actionDownload?: boolean; // Necessario per far comparire correttamente la testata della tabella quando gli elementi hanno l'action se si passa a livello di base row actionDownload true l'action nel menu si vedra' e sarà abilitata
  @Input() id: string = '';
  @Input() data: T[] = [];
  @Input() columns: TableColumns[] = [];
  @Input() itemsPerPage: number = 5;
  @Input() currentPage: number = 1;
  @Input() cardWrapper: boolean = true;
  @Input() singleSelection = false;
  @Input() preselectedIds?: Array<string | number>;
  @Input() preselectedProp?: keyof T & string;
  @Input() isRowPreselected?: (row: T, index: number) => boolean;
  @Input() pageChangeReact: (page: number) => void = () => {};
  @Input() itemsPerPageChangeReact: (items: number) => void = () => {};
  @Input() visibilityPressReact?: (cell: T, page?: number) => Promise<T>;
  @Output() itemsPerPageChange = new EventEmitter<number>();
  @Output() selectedRowsChange = new EventEmitter<T[]>();
  @Output() pageChange = new EventEmitter<number>();
  @ViewChild('tableContent', { static: false }) tableContentRef!: ElementRef;
  @Input() useToggleCompact = false;
  @Input() actionComponent: Type<unknown> | null = null;
  @Input() emptyTableMessage = 'Nessun dato presente!';

  @Input() onSort?: (column?: TableColumns) => void;
  @Input() enabledSort: boolean = false;

  // se la tabella è contenuta in una modale va passato true per renderizzare correttamente le action
  // la modale deve avere una classe di riferimento .modal
  // in alternativa se .modal non esiste è possibile passare una classe di riferimento attraverso: modalClassReference
  @Input() modalClassReference: string | null = null;
  @Input() modalContainer: boolean = false;

  selectedRow: T | null = null;

  @ViewChild('actionDropdown', { static: false }) actionDropdown!: ElementRef<HTMLDivElement>;

  actionComponentChildInjector!: Injector;
  private dropdownAnchorButton!: HTMLElement;

  // EventEmitter per le azioni delle righe
  @Output() view = new EventEmitter<T>();
  @Output() edit = new EventEmitter<T>();
  @Output() delete = new EventEmitter<T>();
  @Output() download = new EventEmitter<T>();

  checkboxColor = Colors.secondary;

  dropdownVisible = false;

  @ViewChildren('placeholder', { read: ElementRef })
  placeholders!: QueryList<ElementRef>;
  private _selezioneSingolaFormArray!: FormControl[];
  private _selezionaMultiplaFormControl!: FormControl;

  get selezioneSingolaFormArray() {
    return this._selezioneSingolaFormArray;
  }

  get selezionaMultiplaFormControl() {
    return this._selezionaMultiplaFormControl;
  }

  constructor(private sanitizer: DomSanitizer) {}

  private injectorCache = new WeakMap<CheckboxTableRowProperties, Injector>();

  createRowInjector(row: CheckboxTableRowProperties): Injector {
    if (!this.injectorCache.has(row)) {
      const injector = Injector.create({
        providers: [{ provide: 'row', useValue: row }],
      });
      this.injectorCache.set(row, injector);
    }
    return this.injectorCache.get(row)!;
  }

  getSelectedRows(): T[] {
    return this.data.filter((_, index) => this._selezioneSingolaFormArray[index]?.value);
  }

  isCompact: boolean = true;

  toggleCompact() {
    this.isCompact = !this.isCompact;
  }

  private emitSelectedRows() {
    const selected = this.getSelectedRows();
    this.selectedRowsChange.emit(selected);
  }

  get hasActions(): boolean {
    return this.data.some(
      (row) => row.actionView || row.actionEdit || row.actionDelete || row.actionDownload,
    );
  }

  ngOnInit(): void {
    this.actionComponentChildInjector = Injector.create({
      providers: [{ provide: 'selectedRow', useValue: this.selectedRow }],
    });
    this.buildControls();
    this.initHeaderControl();
    // L'header viene creato dopo buildControls: riallineo lo stato della selezione multipla
    // alle righe già preselezionate al primo render.
    this.syncSelezionaMultiplaConRigheVisualizzate();
  }

  private initHeaderControl() {
    this._selezionaMultiplaFormControl = new FormControl(false);
    this._selezionaMultiplaFormControl.valueChanges.subscribe((checked) => {
      if (!this.singleSelection) {
        this._selezioneSingolaFormArray.forEach((ctrl) => ctrl.setValue(checked));
        this.emitSelectedRows();
      }
    });
  }

  onView(row: T): void {
    this.view.emit(row);
    if (this.visibilityPressReact) {
      this.visibilityPressReact(row, this.currentPage);
    }
    this.closeDropdown();
  }

  onEdit(row: T): void {
    this.edit.emit(row);
    this.closeDropdown();
  }

  onDelete(row: T): void {
    this.delete.emit(row);
    this.closeDropdown();
  }

  onDownload(row: T): void {
    this.download.emit(row);
    this.closeDropdown();
  }

  // Chiude il dropdown quando si clicca fuori
  @HostListener('document:click')
  closeDropdown() {
    if (!this.actionDropdown?.nativeElement || !this.dropdownAnchorButton) return;

    const dropdownElement = this.actionDropdown.nativeElement;

    dropdownElement.style.left = `0px`;
    dropdownElement.style.top = `0px`;
    dropdownElement.classList.add('invisible');
    dropdownElement.classList.remove('visible');
    this.dropdownVisible = false;
    this.selectedRow = null;

    // Rimuovi tutti gli scroll listener
    this.scrollableParents.forEach((element) => {
      element.removeEventListener('scroll', this.onParentScroll);
    });
    this.scrollableParents = [];
  }

  handleKeydown(event: KeyboardEvent, action: string, row: T): void {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      switch (action) {
        case 'view': {
          this.onView(row);
          break;
        }
        case 'edit': {
          this.onEdit(row);
          break;
        }
        case 'delete': {
          this.onDelete(row);
          break;
        }
        case 'download': {
          this.onDownload(row);
          break;
        }
      }
    }
  }

  private scrollableParents: HTMLElement[] = [];

  private findScrollableParents(element: HTMLElement): HTMLElement[] {
    const scrollables: HTMLElement[] = [];
    let parent = element.parentElement;

    while (parent) {
      const style = getComputedStyle(parent);
      const overflowY = style.overflowY;

      if (overflowY === 'auto' || overflowY === 'scroll') {
        scrollables.push(parent);
      }

      parent = parent.parentElement;
    }

    return scrollables;
  }
  toggleDropdown(event: MouseEvent, row: T) {
    event.preventDefault();
    event.stopPropagation();
    this.selectedRow = row;
    this.dropdownVisible = true;

    this.actionComponentChildInjector = Injector.create({
      providers: [{ provide: 'selectedRow', useValue: this.selectedRow }],
    });

    const button = event.target as HTMLElement;
    this.dropdownAnchorButton = button;
    this.positionDropdown();

    this.actionDropdown?.nativeElement?.classList.remove('invisible');
    this.actionDropdown?.nativeElement?.classList.add('visible');

    // Trova scrollable parents e aggiungi scroll listener
    this.scrollableParents = this.findScrollableParents(button);
    this.scrollableParents.forEach((element) => {
      element.addEventListener('scroll', this.onParentScroll, { passive: true });
    });
  }

  /**
   * Recupera il FormControl associato a una specifica riga della tabella.
   * Se non trova la riga o il controllo non esiste, restituisce un nuovo controllo di default (false).
   * * @param row L'oggetto riga di cui cercare il controllo
   * @returns Il FormControl per gestire la selezione della riga
   */
  getControlForRow(row: T): FormControl {
    const index = this.data.findIndex((item) => item.id === row.id);

    if (
      index === -1 ||
      !this._selezioneSingolaFormArray ||
      !this._selezioneSingolaFormArray[index]
    ) {
      return new FormControl(false);
    }
    return this._selezioneSingolaFormArray[index];
  }

  private onParentScroll = () => {
    if (this.dropdownVisible) {
      this.closeDropdown();
    }
  };

  private positionDropdown() {
    if (!this.dropdownAnchorButton || !this.actionDropdown) return;

    const buttonRect = this.dropdownAnchorButton.getBoundingClientRect();
    const dropdown = this.actionDropdown.nativeElement;

    const dropdownWidth = dropdown.offsetWidth || 150;
    const dropdownHeight = dropdown.offsetHeight || 200;

    let left = buttonRect.left + buttonRect.width / 2 - dropdownWidth / 2;
    let top = buttonRect.bottom + 5;

    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;

    // overflow orizzontale
    if (left + dropdownWidth > viewportWidth) {
      left = viewportWidth - dropdownWidth - 10;
    } else if (left < 0) {
      left = 10;
    }

    // Previeni overflow verticale
    if (top + dropdownHeight > viewportHeight) {
      top = buttonRect.top - dropdownHeight - 5;
    }

    // Modal logic: usa position absolute rispetto al contenitore scrollabile
    if (this.modalContainer) {
      const referenceClass = this.modalClassReference ?? 'modal';
      const modalWrapper = dropdown.closest(`.${referenceClass}`);
      if (modalWrapper) {
        dropdown.style.position = 'absolute';
        dropdown.style.left = `${left - modalWrapper.getBoundingClientRect().left}px`;
        dropdown.style.top = `${top - modalWrapper.getBoundingClientRect().top}px`;

        // Assicura che sia figlio del contenitore corretto
        if (dropdown.parentElement !== modalWrapper) {
          modalWrapper.append(dropdown);
        }

        return;
      }
    }

    // Default (fuori da modale): position fixed
    dropdown.style.position = 'fixed';
    dropdown.style.left = `${left}px`;
    dropdown.style.top = `${top}px`;
  }

  @HostListener('window:resize')
  @HostListener('window:scroll')
  onWindowChange() {
    if (this.dropdownVisible) {
      this.closeDropdown();
    }
  }

  onSortChange(column: TableColumns, direction?: 'asc' | 'desc') {
    this.columns = this.columns.map((col) => {
      if (col.id === column.id) {
        return {
          ...col,
          sortDirection: col.sortDirection
            ? col.sortDirection === 'asc'
              ? 'desc'
              : 'asc'
            : direction,
        };
      }
      return col;
    });

    if (this.onSort) {
      this.onSort(this.columns.find((col) => col.id === column.id));
      return;
    }
  }

  private buildControls() {
    this._selezioneSingolaFormArray = this.data.map((row, index) => {
      let initial = this.isPreselected(row, index);
      if (this.singleSelection && initial) {
        const alreadyTrue = this._selezioneSingolaFormArray?.some?.((c) => c.value) ?? false;
        if (alreadyTrue) initial = false;
      }
      const c = new FormControl(initial);
      c.valueChanges.subscribe((checked) => {
        if (!checked && this._selezionaMultiplaFormControl.value) {
          this._selezionaMultiplaFormControl.setValue(false, { emitEvent: false });
        }
        if (this.singleSelection && checked) {
          // deseleziona gli altri senza loop infinito
          this._selezioneSingolaFormArray.forEach((ctrl, index_) => {
            if (index_ !== index) ctrl.setValue(false, { emitEvent: false });
          });
        }
        // In selezione multipla, se dopo il toggle tutte le righe visualizzate sono selezionate
        // viene spuntata anche la checkbox "seleziona tutto".
        if (!this.singleSelection) {
          this.syncSelezionaMultiplaConRigheVisualizzate();
        }
        this.emitSelectedRows();
      });
      return c;
    });
    if (!this.singleSelection && this._selezionaMultiplaFormControl) {
      const allSelected = this._selezioneSingolaFormArray.every((c) => c.value === true);
      this._selezionaMultiplaFormControl.setValue(allSelected, { emitEvent: false });
    }
  }

  ngAfterViewInit() {
    this.actionDropdown?.nativeElement?.classList.add('invisible');

    // associa a ciascun <div> lo spec corrispondente
    this.placeholders.forEach((elementReference, index) => {
      const col = this.columns[Math.floor(index / this.data.length)];
      const row = this.data[index % this.data.length];
      const spec = row[col.id] as ReactCellSpec;
      (
        elementReference.nativeElement as HTMLDivElement & { __reactSpec: ReactCellSpec }
      ).__reactSpec = spec;
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    const dataChanged = !!changes['data'];
    const presetChanged = !!(
      changes['preselectedIds'] ||
      changes['preselectedProp'] ||
      changes['isRowPreselected']
    );

    if (dataChanged) {
      const previous = changes['data'].previousValue;
      const current = changes['data'].currentValue;

      // ricrea anche se la lunghezza è uguale ma è un array nuovo
      if (!previous || !current || previous.length !== current.length || previous !== current) {
        this.buildControls();
      }
      if (
        Array.isArray(previous) &&
        Array.isArray(current) &&
        previous.length === 0 &&
        current.length > 0
      ) {
        this.resetComponentState();
      }
    }

    if (presetChanged && this.data?.length) {
      this.buildControls();
    }

    this.syncSelezionaMultiplaConRigheVisualizzate();
  }

  /**
   * Allinea la checkbox di selezione multipla allo stato delle righe visualizzate:
   * se tutte le righe attualmente mostrate sono selezionate la checkbox viene selezionata.
   * L'aggiornamento è silenzioso (`emitEvent: false`) per non propagare la selezione alle righe.
   */
  private syncSelezionaMultiplaConRigheVisualizzate(): void {
    if (
      this.singleSelection ||
      !this._selezionaMultiplaFormControl ||
      !this._selezioneSingolaFormArray
    ) {
      return;
    }
    const controlliRigheVisualizzate = this.getControlliRigheVisualizzate();
    const tutteRigheSelezionate =
      controlliRigheVisualizzate.length > 0 &&
      controlliRigheVisualizzate.every((controllo) => controllo.value);
    if (this._selezionaMultiplaFormControl.value !== tutteRigheSelezionate) {
      this._selezionaMultiplaFormControl.setValue(tutteRigheSelezionate, { emitEvent: false });
    }
  }

  /**
   * Restituisce i controlli di selezione relativi alle sole righe attualmente visualizzate
   * (la pagina corrente in caso di paginazione client-side, tutte in caso di paginazione server-side).
   *
   * @returns {FormControl[]} Controlli delle righe visualizzate.
   */
  private getControlliRigheVisualizzate(): FormControl[] {
    if (!this._selezioneSingolaFormArray) return [];
    if (this.serverPaginated) return this._selezioneSingolaFormArray;
    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    return this._selezioneSingolaFormArray.slice(startIndex, startIndex + this.itemsPerPage);
  }

  private resetComponentState(): void {
    this.currentPage = 1;
  }

  get visiblePageNumbers(): number[] {
    const totalPages = this.totalPages;
    // Mostra fino a 3 pagine centrali attorno alla corrente
    const start = Math.max(1, this.currentPage - 1);
    const end = Math.min(totalPages, this.currentPage + 1);

    return Array.from({ length: end - start + 1 }, (_, index) => start + index);
  }

  get paginatedData() {
    if (this.serverPaginated) {
      return this.data;
    }
    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    return this.data.slice(startIndex, startIndex + this.itemsPerPage);
  }

  get totalPages() {
    if (this.serverPaginated) {
      return Math.ceil((this.totalItems || 0) / this.itemsPerPage);
    }
    return Math.ceil(this.data.length / this.itemsPerPage);
  }

  get pageNumbers() {
    return Array.from({ length: this.totalPages }, (_, index) => index + 1);
  }

  onPageChange(page: number) {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
      this.pageChangeReact?.(page);
      this.pageChange.emit(page);
    }
  }

  onItemsPerPageChange(items: number) {
    this.itemsPerPageChangeReact?.(items);
    this.itemsPerPageChange.emit(items);
    this.onPageChange(1);
  }

  trackByColumn(_: number, column: { label: string }): string {
    return column.label;
  }

  trackByColumnId(_: number, column: { id: string }): string {
    return column.id;
  }

  trackByPage(_: number, page: number): number {
    return page;
  }

  trackByRow(_: number, row: T): string | number {
    return row?.id || _;
  }

  isHtml(value: string): boolean {
    return typeof value === 'string' && value.startsWith('<');
  }

  isFunction(value: unknown): boolean {
    return typeof value === 'function';
  }

  isComponent(value: unknown): boolean {
    let isComponent = false;

    if (this.isFunction(value) || this.isHtml(value as string) || this.isAngularComponent(value)) {
      isComponent = true;
    }

    return isComponent;
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  isAngularComponent(value: any): boolean {
    return typeof value === 'function' && value.ɵcmp !== undefined;
  }

  renderComponent(function_: unknown): string | SafeHtml {
    if (this.isFunction(function_)) {
      const componentFunction = function_ as () => string;
      console.log(componentFunction, 'componentFunction');
      return this.sanitizer.bypassSecurityTrustHtml(componentFunction() as string);
    }

    if (this.isHtml(function_ as string)) {
      console.log(function_, 'componentFunction1');
      return this.sanitizer.bypassSecurityTrustHtml(function_ as string);
    }

    return '';
  }

  private isPreselected(row: T, index: number): boolean {
    if (this.isRowPreselected) return !!this.isRowPreselected(row, index);

    if (this.preselectedIds && row?.id != null) {
      return this.preselectedIds.some((v) => String(v) === String(row.id));
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    if (this.preselectedProp && (row as any)?.[this.preselectedProp] != null) {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      return !!(row as any)[this.preselectedProp];
    }

    return false;
  }

  elementPerPageArray = [5, 10, 50, 100, 200];

  trackByElementPerPage(_: number, elementPerPage: number): number {
    return elementPerPage;
  }
}
