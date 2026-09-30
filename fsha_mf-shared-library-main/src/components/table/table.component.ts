import { CommonModule } from '@angular/common';
import {
  Component,
  Input,
  Output,
  EventEmitter,
  SimpleChanges,
  OnChanges,
  HostListener,
  ElementRef,
  ViewChild,
  AfterViewInit,
  Type,
  Injector,
  OnInit,
  ViewChildren,
  QueryList,
  ChangeDetectorRef,
} from '@angular/core';
import { CardWrapperComponent } from '../card-wrapper/card-wrapper.component';
import {
  FormArray,
  FormBuilder,
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
} from '@angular/forms';
import {
  faEye,
  faPenToSquare,
  faTrash,
  faEllipsisVertical,
  IconDefinition,
  faDownload,
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { IconComponent } from '../icon/icon.component';
import { Colors, ColumnProperties, IconSize, RowProperties } from 'test-library-frankmd93';
import { CheckboxComponent } from '../form-elements/checkbox/checkbox.component';
import { ImageComponent } from '../image/image.component';
import { GroupByTableHelper, RowSpanMap } from './helper/group-by-table.helper';

/**
 * @deprecated use version from test-library
 */
interface ReactCellSpec {
  type: unknown;
  props: Record<string, unknown>;
}

/**
 * @deprecated use version from test-library
 */
interface RowItem extends RowProperties {
  actionComponent?: boolean;
}

/**
 * @deprecated use version from test-library
 */
interface TableColumns<T> extends ColumnProperties<keyof T, T> {
  id: Extract<keyof T, string>;
  sortDirection?: 'asc' | 'desc';
  groupBy?: boolean;
}
@Component({
  selector: 'app-rc-table',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    FontAwesomeModule,
    CardWrapperComponent,
    IconComponent,
    CheckboxComponent,
    FormsModule,
    ReactiveFormsModule,
    ImageComponent,
  ],
  templateUrl: './table.component.html',
  styleUrl: './table.component.scss',
})
export class TableComponent<T extends RowItem> implements OnChanges, AfterViewInit, OnInit {
  @Input() serverPaginated: boolean = false;
  @Input() shouldValidateVisibility: boolean = false;
  @Input() totalItems?: number = 0;
  @Input() shouldShowAllItems = false;
  @Input() baseUrl: string = '/mfSharedLibrary';
  faEye: IconDefinition = faEye;
  faEllipsisVertical: IconDefinition = faEllipsisVertical;
  faPenToSquare: IconDefinition = faPenToSquare;
  faTrash: IconDefinition = faTrash;
  faDownload: IconDefinition = faDownload;
  IconSize = IconSize;
  // si può disabilitare l'action a livello di elemento con baserow con boolean actionView,actionEdit,actionDelete,actionDownload.
  @Input() actionView?: boolean; // Necessario per far comparire correttamente la testata della tabella quando gli elementi hanno l'action se si passa a livello di base row actionView true l'action nel menu si vedra' e sarà abilitata
  @Input() actionEdit?: boolean; // Necessario per far comparire correttamente la testata della tabella quando gli elementi hanno l'action se si passa a livello di base row actionEdit true l'action nel menu si vedra' e sarà abilitata
  @Input() actionDelete?: boolean; // Necessario per far comparire correttamente la testata della tabella quando gli elementi hanno l'action se si passa a livello di base row actionDelete true l'action nel menu si vedra' e sarà abilitata
  @Input() actionDownload?: boolean; // Necessario per far comparire correttamente la testata della tabella quando gli elementi hanno l'action se si passa a livello di base row actionDownload true l'action nel menu si vedra' e sarà abilitata
  @Input() id: string = '';
  @Input() data: T[] = [];
  @Input() columns: TableColumns<T>[] = [];

  @Input() itemsPerPage: number = 5;

  @Input() currentPage: number = 1;
  @Input() cardWrapper: boolean = true;
  @Output() pageChange = new EventEmitter<number>();
  @Input() pageChangeReact!: (page: number) => void;
  @Input() itemsPerPageChangeReact!: (page: number) => void;
  @Input() visibilityPressReact?: (cell: T, page?: number) => Promise<T>;
  @Output() itemsPerPageChange = new EventEmitter<number>();
  // se la tabella è contenuta in una modale va passato true per renderizzare correttamente le action
  // la modale deve avere una classe di riferimento .modal
  // in alternativa se .modal non esiste è possibile passare una classe di riferimento attraverso: modalClassReference
  @Input() modalClassReference: string | null = null;
  @Input() modalContainer: boolean = false;
  @Input() useToggleCompact = true;
  @Input() useManageColumnsVisibility = true;
  @Input() onSort?: (column?: TableColumns<T>) => void;
  @Input() enabledSort: boolean = false;

  // EventEmitter per le azioni delle righe
  @Output() view = new EventEmitter<T>();
  @Output() edit = new EventEmitter<T>();
  @Output() delete = new EventEmitter<T>();
  @Output() download = new EventEmitter<T>();

  @Input() actionComponent: Type<unknown> | null = null;
  @Input() emptyTableMessage = 'Nessun dato presente!';

  // Input per gestire le colonne visibili
  @Input() columnsForm!: FormGroup;
  @Input() columnsArray!: FormArray<FormControl<boolean>>;
  // Input per gestire l'esportazione in excel della lista
  @Input() exportExcelCallback?: () => void;
  // Input per gestire l'esportazione in excel della lista
  @Input() exportPdfCallback?: () => void;
  // Input per gestire il reload dei dati
  @Input() reloadDataCallback?: () => void;
  // Input per gestire il raggruppamento sulle righe

  /**
   * Array con le chiavi delle colonne da raggruppare
   */
  groupByList: Array<Extract<keyof T, string>> = [];
  rowSpans: Array<RowSpanMap<T>> = [];

  @ViewChild('tableContent', { static: false }) tableContentRef!: ElementRef;
  @ViewChild('actionDropdown', { static: false }) actionDropdown!: ElementRef<HTMLDivElement>;
  dropdownVisible = false;
  dropdownPosition = { top: 0, left: 0 };
  selectedRow: T | null = null;
  private dropdownAnchorButton!: HTMLElement;

  @ViewChild('columnsDropdown', { static: false })
  columnsDropdown!: ElementRef<HTMLDivElement>;

  columnsMenuVisible = false;
  private columnsAnchorButton!: HTMLElement;

  private columnsScrollableParents: HTMLElement[] = [];

  onExportExcelCallback(): void {
    this.exportExcelCallback?.();
  }

  onExportPdfCallback(): void {
    this.exportPdfCallback?.();
  }

  onReloadDataCallback(): void {
    this.reloadDataCallback?.();
  }

  private onColumnsParentScroll = () => {
    if (this.columnsMenuVisible) {
      this.closeColumnsMenu();
    }
  };

  trackByIndex(index: number): number {
    return index;
  }

  checkboxColor = Colors.primary;

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: MouseEvent) {
    const target = event.target as Node;

    // --- CHIUSURA DROPDOWN AZIONI RIGA ---
    if (this.dropdownVisible) {
      const dropdownElement = this.actionDropdown?.nativeElement ?? null;
      const anchorElement = this.dropdownAnchorButton ?? null;

      const insideActions =
        (!!dropdownElement && dropdownElement.contains(target)) ||
        (!!anchorElement && anchorElement.contains(target));

      if (!insideActions) {
        this.closeActionsDropdown();
      }
    }

    // --- CHIUSURA TOOLTIP / DROPDOWN COLONNE ---
    if (this.columnsMenuVisible) {
      const dropdownElement = this.columnsDropdown?.nativeElement;
      const anchorElement = this.columnsAnchorButton;

      const inside =
        (!!dropdownElement && dropdownElement.contains(target)) ||
        (!!anchorElement && anchorElement.contains(target));

      console.log(inside, 'inside');

      if (!inside) {
        this.closeColumnsMenu();
      }
    }
  }

  private syncColumnsDisabledState(): void {
    if (!this.columnsArray) return;

    const canDisable = this.hasMoreThanOneColumnSelected;

    this.columnsArray.controls.forEach((ctrl) => {
      if (canDisable) {
        if (ctrl.disabled) {
          ctrl.enable({ emitEvent: false });
        }
      } else {
        if (ctrl.enabled && ctrl.value === true) {
          ctrl.disable({ emitEvent: false });
        }
      }
    });
  }

  get hasMoreThanOneColumnSelected(): boolean {
    if (!this.columnsArray) return false;

    return this.columnsArray.controls.filter((ctrl) => ctrl.value === true).length > 1;
  }

  private positionColumnsDropdown() {
    if (!this.columnsAnchorButton || !this.columnsDropdown) return;

    const buttonRect = this.columnsAnchorButton.getBoundingClientRect();
    const dropdown = this.columnsDropdown.nativeElement;

    const dropdownWidth = dropdown.offsetWidth || 260;
    const dropdownHeight = dropdown.offsetHeight || 240;

    let left = buttonRect.left + buttonRect.width / 2 - dropdownWidth / 2;
    let top = buttonRect.bottom + 6;

    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;

    // overflow orizzontale
    if (left + dropdownWidth > viewportWidth) left = viewportWidth - dropdownWidth - 10;
    if (left < 0) left = 10;

    // overflow verticale
    if (top + dropdownHeight > viewportHeight) {
      top = buttonRect.top - dropdownHeight - 6;
    }

    // Modal logic (come già fai per actionDropdown)
    if (this.modalContainer) {
      const referenceClass = this.modalClassReference ?? 'modal';
      const modalWrapper = dropdown.closest(`.${referenceClass}`);
      if (modalWrapper) {
        dropdown.style.position = 'absolute';
        dropdown.style.left = `${left - modalWrapper.getBoundingClientRect().left}px`;
        dropdown.style.top = `${top - modalWrapper.getBoundingClientRect().top}px`;

        if (dropdown.parentElement !== modalWrapper) {
          modalWrapper.append(dropdown);
        }
        return;
      }
    }

    // Default fuori modale
    dropdown.style.position = 'fixed';
    // dropdown.style.left = `${left}px`;
    dropdown.style.right = '20px';
    dropdown.style.top = `${top}px`;
  }

  asAngularComponent(value: unknown): Type<unknown> | null {
    return this.isAngularComponent(value) ? (value as Type<unknown>) : null;
  }

  actionComponentChildInjector!: Injector;

  @ViewChildren('placeholder', { read: ElementRef })
  placeholders!: QueryList<ElementRef>;

  constructor(
    private sanitizer: DomSanitizer,
    private fb: FormBuilder,
    private cdr: ChangeDetectorRef,
  ) {}

  private injectorCache = new WeakMap<RowItem, Injector>();

  get columnsNotHidden() {
    return this.columns.filter((col) => !col?.hidden);
  }

  isCompact: boolean = true;

  toggleCompact() {
    this.cdr.detectChanges();
    this.isCompact = !this.isCompact;
  }

  createRowInjector(row: RowItem): Injector {
    if (!this.injectorCache.has(row)) {
      const injector = Injector.create({
        providers: [{ provide: 'row', useValue: row }],
      });
      this.injectorCache.set(row, injector);
    }
    return this.injectorCache.get(row)!;
  }

  ngOnInit(): void {
    this.actionComponentChildInjector = Injector.create({
      providers: [{ provide: 'selectedRow', useValue: this.selectedRow }],
    });

    this.buildColumnsForm();
    if (this.groupByList?.length) this.recomputeGrouping();
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
  toggleActionsDropdown(event: MouseEvent, row: T) {
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

  onColumnVisiilityChange() {
    this.cdr.detectChanges();
  }

  toggleColumnsMenu(event: MouseEvent) {
    this.cdr.detectChanges();
    if (!this.useManageColumnsVisibility) return;

    event.preventDefault();
    event.stopPropagation();

    this.columnsMenuVisible = !this.columnsMenuVisible;

    if (!this.columnsMenuVisible) {
      this.closeColumnsMenu();
      return;
    }

    this.columnsAnchorButton = event.currentTarget as HTMLElement;

    this.positionColumnsDropdown();

    const element = this.columnsDropdown?.nativeElement;
    element?.classList.remove('d-none');
    element?.classList.add('d-block');
  }

  private onParentScroll = () => {
    this.onWindowScroll();
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
      this.closeActionsDropdown();
    }
    if (this.columnsMenuVisible) {
      this.closeColumnsMenu();
    }
  }

  // // Chiude il dropdown quando si clicca fuori
  // @HostListener('document:click')
  closeActionsDropdown() {
    if (!this.actionDropdown?.nativeElement || !this.dropdownAnchorButton) return;

    const dropdownElement = this.actionDropdown.nativeElement;

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

  ngAfterViewInit() {
    if (localStorage.getItem('compactMode') === 'true') {
      this.isCompact = true;
    }
    this.actionDropdown?.nativeElement?.classList.add('invisible');
    this.columnsDropdown?.nativeElement?.classList.add('d-none');

    if (this.groupByList?.length) return; // evita mapping errato con rowspan

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

  // se vuoi persistere la scelta per tabella
  private get columnsStorageKey() {
    return `rc-table-columns-visibility:${this.id || 'default'}`;
  }

  @HostListener('window:resize')
  onWindowResize() {
    if (this.dropdownVisible) this.closeActionsDropdown();
    if (this.columnsMenuVisible) this.closeColumnsMenu();
  }

  @HostListener('window:scroll')
  onWindowScroll() {
    if (this.dropdownVisible) this.closeActionsDropdown();
    if (this.columnsMenuVisible) this.closeColumnsMenu();
  }

  closeColumnsMenu() {
    if (!this.columnsDropdown?.nativeElement) return;

    const element = this.columnsDropdown.nativeElement;

    element.classList.add('d-none');
    element.classList.remove('d-block');

    this.columnsMenuVisible = false;

    // rimuovi scroll listener
    this.columnsScrollableParents.forEach((p) => {
      p.removeEventListener('scroll', this.onColumnsParentScroll);
    });
    this.columnsScrollableParents = [];
  }

  private buildColumnsForm() {
    this.columnsArray = this.fb.array(
      this.columns.filter((c) => !c.hidden).map(() => new FormControl(true, { nonNullable: true })),
    );

    this.columnsForm = this.fb.group({
      columns: this.columnsArray,
    });

    // Persistenza automatica
    this.columnsArray.valueChanges.subscribe(() => {
      this.syncColumnsDisabledState();
    });
  }

  get visibleColumns(): TableColumns<T>[] {
    if (!this.columnsArray) return this.columns;

    return this.columns
      .filter((c) => !c.hidden)
      .filter((_, index) => this.columnsArray.at(index)?.value);
  }

  private restoreColumnsVisibility() {
    const raw = localStorage.getItem(this.columnsStorageKey);
    if (!raw || !this.columnsArray) return;

    const saved: Array<{ id: string; visible: boolean }> = JSON.parse(raw);

    saved.forEach((s) => {
      const index = this.columns.filter((c) => !c.hidden).findIndex((c) => c.id === s.id);
      if (index !== -1) {
        this.columnsArray.at(index)?.setValue(s.visible, { emitEvent: false });
      }
    });
    this.syncColumnsDisabledState();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['columns'] && Array.isArray(this.columns) && this.columns.length > 0) {
      this.buildGroupByColumns();
      this.buildColumnsForm();
      this.restoreColumnsVisibility();
    }
    if (changes['data']) {
      const previousData = changes['data'].previousValue;
      const currentData = changes['data'].currentValue;

      if (
        Array.isArray(previousData) &&
        Array.isArray(currentData) &&
        previousData.length === 0 &&
        currentData.length > 0
      ) {
        this.resetComponentState();
      }
    }

    const shouldRecompute =
      !!changes['data'] ||
      !!changes['currentPage'] ||
      !!changes['itemsPerPage'] ||
      !!changes['groupBy'] ||
      !!changes['serverPaginated'];

    // Ricalcola i rowspans del groupBy
    if (shouldRecompute) {
      this.recomputeGrouping();
    }
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
    if (!Array.isArray(this.data)) return [];

    // Se non c’è groupBy ritorna i dati normali
    if (!this.groupByList?.length) {
      if (this.serverPaginated) return this.data;

      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      return this.data.slice(startIndex, startIndex + this.itemsPerPage);
    }

    // Se c’è groupBy e data contiene più di un elemento
    // riordina gli elementi per rendere contigue le righe con la stessa chiave di groupBy
    const clustered =
      this.data.length > 1
        ? GroupByTableHelper.groupRowsForRowspan(this.data, this.groupByList)
        : this.data;

    // Se c'è paginazione server-side rimando i dati che rappresentano la singola pagina così come sono
    if (this.serverPaginated) {
      return clustered;
    }

    // Altrimenti suddivido i dati raggruppati in pagine per la paginazione client-side
    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    return clustered.slice(startIndex, startIndex + this.itemsPerPage);
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
      if (this.groupByList?.length) this.recomputeGrouping();
      if (this.pageChangeReact) {
        this.pageChangeReact(page);
      } else {
        console.log({ page, data: this.paginatedData });
        this.pageChange.emit(page);
      }
    }
  }

  onItemsPerPageChange(items: number) {
    if (this.itemsPerPageChangeReact) {
      this.itemsPerPageChangeReact(items);
    } else {
      this.itemsPerPageChange.emit(items);
    }
    this.onPageChange(1);
    if (this.groupByList?.length) this.recomputeGrouping();
  }

  onSortChange(column: TableColumns<T>, direction?: 'asc' | 'desc') {
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

  onView(row: T): void {
    this.view.emit(row);
    if (this.visibilityPressReact) {
      this.visibilityPressReact(row, this.currentPage);
    }
    this.closeActionsDropdown();
  }

  onEdit(row: T): void {
    this.edit.emit(row);
    this.closeActionsDropdown();
  }

  onDelete(row: T): void {
    this.delete.emit(row);
    this.closeActionsDropdown();
  }

  onDownload(row: T): void {
    this.download.emit(row);
    this.closeActionsDropdown();
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

  get hasActions(): boolean {
    return this.data.some(
      (row) => row.actionView || row.actionEdit || row.actionDelete || row.actionDownload,
    );
  }

  trackByColumn(_: number, column: TableColumns<T>): string {
    return column.label;
  }

  trackByColumnId(_: number, column: TableColumns<T>): string {
    return column.id;
  }

  trackByPage(_: number, page: number): number {
    return page;
  }

  trackByRow(_: number, row: RowItem): string | number {
    return row.id || '';
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

  // IMPLEMENTAZIONE GROUP BY

  /**
   * Controlla se la colonna fa parte di quelle da raggruppare nel groupBy
   * @param colId
   * @returns
   */
  isGrouped(colId: Extract<keyof T, string>): boolean {
    return Array.isArray(this.groupByList) && this.groupByList.includes(colId);
  }

  /**
   * Estrae il numero di rowspan da applicare sulla colonna per una data riga
   * @param r index della riga
   * @param colId id della colonna di cui trovare il rowspan
   * @returns numero di rowspan da applicare
   */
  getRowSpan(r: number, colId: Extract<keyof T, string>): number {
    return Number(this.rowSpans?.[r]?.[colId] ?? 0);
  }

  /**
   * Costruisce l'array delle colonne su cui applicare il groupBy
   */
  private buildGroupByColumns() {
    // Per ogni colonna controlla se l'attributo gruopBy è true
    this.columns.forEach((col) => {
      if (col.groupBy) {
        // Se lo è aggiunge l'id della colonna all'array
        this.groupByList.push(col.id);
      }
    });
  }

  /**
   * Ricalcola la mappa dei rowspan usata dal template per il rendering con groupBy.
   * Deve essere richiamato quando cambiano data/paginazione/groupBy.
   */
  private recomputeGrouping(): void {
    const rows = this.paginatedData; // se groupBy è attivo le righe sono già state raggruppate dal get di paginatedData

    // Se non è specificato il groupBy assegna a rowspan una struttura vuota
    if (!this.groupByList?.length) {
      this.rowSpans = rows.map(() => ({}));
      return;
    }

    // Calcola il numero di rowspan da applicare ad ogni colonna presente nell'array di groupBy di ogni riga
    // e lo inserisce nella struttura dati utilizzata dal template
    // Es [{foglio: 2, numero: 2, subalterno: 2}, {foglio: 0, numero: 0, subalterno: 0}, ...]
    this.rowSpans = GroupByTableHelper.calcRowSpans(rows, this.groupByList);
  }

  elementPerPageArray = [5, 10, 50, 100, 200];

  trackByElementPerPage(_: number, elementPerPage: number): number {
    return elementPerPage;
  }
}
