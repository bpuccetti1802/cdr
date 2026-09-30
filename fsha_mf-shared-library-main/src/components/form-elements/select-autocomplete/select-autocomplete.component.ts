import {
  Component,
  Input,
  AfterViewInit,
  ElementRef,
  ViewChild,
  OnInit,
  Renderer2,
  EventEmitter,
  Output,
  SimpleChanges,
  OnChanges,
  OnDestroy,
} from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import {
  debounceTime,
  distinctUntilChanged,
  startWith,
  Subject,
  Subscription,
  tap,
  filter,
  takeUntil,
} from 'rxjs';
import { IconComponent } from '@mf/components/icon/icon.component';
import { IconSize, SelectItem } from 'test-library-frankmd93';
import { AbstractDestroyTrackerComponent } from '../../abstract-subscriptions-tracker/abstract-destroy-tracker.component';

function defaultGetErrorMessage(formControl: FormControl): string | null {
  if (formControl?.errors && formControl.errors['required']) {
    return 'Questo campo è obbligatorio.';
  }
  return null;
}

@Component({
  selector: 'app-rc-select-autocomplete',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, IconComponent],
  templateUrl: './select-autocomplete.component.html',
  styleUrls: ['./select-autocomplete.component.scss'],
})
export class SelectAutocompleteComponent
  extends AbstractDestroyTrackerComponent
  implements OnInit, AfterViewInit, OnChanges, OnDestroy
{
  @Input() serverSearch = false;
  @Input() id!: string;
  @Input() label: string = '';
  @Input() placeholder: string = 'Seleziona...';
  @Input() errorMessage: string = 'Seleziona un valore valido';
  @Input() formControl: FormControl = new FormControl();
  @Input() options: SelectItem[] = [];
  @Input() disabled: boolean = false;
  @Input() required = false;
  @Input() position: string = 'absolute';
  @Input() minSearchLength = 0;
  @Input() onSelectOption: (option: SelectItem, isOnChange?: boolean) => void = () => {};
  @Input() getErrorMessage: CallableFunction = defaultGetErrorMessage;
  @Input() minCharacters: number = 1; // non toccare il default 1, impatta su molte chiamate
  /**
   * Flag per decidere se, allo svuotamento del campo, deve essere emesso l'evento onClear.
   * Di default è false per mantenere il comportamento attuale.
   */
  @Input() clearCallEvnt: boolean = true;
  /**
   * Funzione da eseguire allo svuotamento del campo.
   * Di default è una funzione vuota.
   */
  @Input() onClear: () => void = () => {};

  @ViewChild('inputRef', { static: false }) inputRef!: ElementRef<HTMLInputElement>;

  get errorMessageComputed() {
    return this.getErrorMessage(this.formControl);
  }

  @Output() search = new EventEmitter<string>();

  private input$ = new Subject<string>();
  private inputSub?: Subscription;
  filteredOptions: { value: string; label: string }[] = [];
  showDropdown = false;
  term: string = '';

  /**
   * Diventa `true` solo dopo una reale interazione utente (digitazione o selezione),
   * così da non marcare `touched` il formControl per focus/blur programmatici (es. in init).
   */
  private hasUserInteracted = false;

  @ViewChild('autocompleteWrapper', { static: false }) autocompleteWrapper!: ElementRef;
  @ViewChild('dropdownRef', { static: false }) dropdownRef!: ElementRef;

  IconSize = IconSize;

  constructor(private renderer: Renderer2) {
    super();
  }

  formControlSubscription!: Subscription;

  ngOnInit(): void {
    this.formControl.valueChanges
      .pipe(
        takeUntil(this.destroyed$),
        filter((v) => !v),
        tap(() => {
          this.term = '';
        }),
      )
      .subscribe();
    this.inputSub = this.input$.pipe(debounceTime(400), distinctUntilChanged()).subscribe((q) => {
      if (q.length >= this.minSearchLength) {
        this.search.emit(q);
      } else {
        this.filteredOptions = [];
        this.showDropdown = false;
        this.search.emit('');
      }
    });
    if (!this.serverSearch) {
      const currentValue = this.formControl.value;
      this.term = this.options?.find((option) => option.value === currentValue)?.label || '';
      this.filteredOptions = this.getFilteredOptions();
      this.formControlSubscription = this.formControl.valueChanges
        .pipe(
          startWith(this.formControl.value),
          distinctUntilChanged(),
          tap((v) => {
            const match = this.options?.find((opt) => opt?.value === v);
            this.term = match?.label ?? '';
            this.filteredOptions = this.getFilteredOptions();
          }),
        )
        .subscribe();
      this.updateDropdownPosition();
    }
  }

  clearValue() {
    this.formControl.setValue(null);
  }

  getFilteredOptions(): SelectItem[] {
    if (this.serverSearch) {
      return this.options;
    }
    return this.options?.filter((option) =>
      option.label.toLowerCase().includes(this.term.toLowerCase()),
    );
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['options']) {
      const currentValue = this.formControl.value;
      this.filteredOptions = this.getFilteredOptions();
      if (this.serverSearch) {
        const match = this.options.find(
          (opt) => opt.label === currentValue || opt.value === currentValue,
        );
        if (match) {
          this.formControl.setValue(match.value, { emitEvent: false });
          this.term = match.label;
          this.filteredOptions = this.getFilteredOptions();
          this.showDropdown = false;
          this.onSelectOption(match, true);
          return;
        }
        if (currentValue) {
          this.formControl.setValue(currentValue, { emitEvent: false });
          this.term = currentValue;
        }
        if (
          this.filteredOptions.length > 0 &&
          (this.term.length >= this.minSearchLength || currentValue?.length >= this.minSearchLength)
        ) {
          this.showDropdown = true;
          setTimeout(() => this.updateDropdownPosition(), 0);
        } else {
          this.showDropdown = false;
        }
        setTimeout(() => this.inputRef?.nativeElement.focus(), 0);
      } else {
        this.term =
          this.options?.find((option) => option.value === currentValue)?.label || this.term || '';
        this.filteredOptions = this.getFilteredOptions();
      }
    }
  }

  ngAfterViewInit(): void {
    document.addEventListener('click', (event) => {
      if (!this.autocompleteWrapper?.nativeElement.contains(event.target)) {
        this.showDropdown = false;
      }
    });

    window.addEventListener('scroll', this.onScrollOutside, true);
  }

  // Chiude il drowdown solo se lo scroll avviene al di fuori di se stesso
  onScrollOutside = (event: Event) => {
    if (!this.dropdownRef?.nativeElement.contains(event.target)) {
      this.closeDropdown();
    }
  };

  closeDropdown() {
    this.showDropdown = false;
    this.inputRef?.nativeElement.blur();
  }

  openDropdown(): void {
    if (this.disabled) {
      return;
    }
    this.showDropdown = true;
    setTimeout(() => this.updateDropdownPosition(), 0);
  }

  get valid() {
    return this.formControl?.valid;
  }

  get touched() {
    return this.formControl?.touched;
  }

  updateDropdownPosition(): void {
    if (!this.dropdownRef || !this.autocompleteWrapper) return;

    const wrapperRect = this.autocompleteWrapper.nativeElement.getBoundingClientRect();
    const dropdownElement = this.dropdownRef.nativeElement;
    this.renderer.setStyle(dropdownElement, 'position', this.position);
    this.renderer.setStyle(dropdownElement, 'width', `${wrapperRect.width}px`);
    this.renderer.setStyle(dropdownElement, 'z-index', '2050');
  }

  trackByFn(_: number, item: { value: string; label: string }): string {
    return item.value; // Unique identifier for each option
  }

  onInputChange(event: Event): void {
    const inputElement = event.target as HTMLInputElement | null;
    if (!inputElement) return;

    this.hasUserInteracted = true;

    const value = inputElement.value;
    this.term = value;

    // Mantieni sincronizzato anche il formControl
    // (solo se è serverSearch, l'HTML mostra sempre quello che digiti)
    if (this.serverSearch) {
      this.formControl.setValue(value, { emitEvent: false });
    }

    if (!value && this.clearCallEvnt) {
      this.onClear();
    }

    if (this.serverSearch) {
      this.showDropdown = true;
    } else {
      this.filteredOptions = this.getFilteredOptions();
      this.showDropdown =
        this.minSearchLength === 0
          ? this.filteredOptions.length > 0
          : this.filteredOptions.length > 0 && value.length >= this.minSearchLength;
    }

    setTimeout(() => this.updateDropdownPosition(), 0);
    if (value.length === 0) {
      this.formControl.setValue('');
      return;
    }
    //in diversi casi il backend restituisce un errore se si inviano meno di 2 caratteri
    // è stato configurato un input per mandare da fuori il numero minimo di caratteri per scatenare la chiamata
    if (value.length > this.minCharacters) {
      this.input$.next(value);
    }
  }

  selectOption(option: SelectItem): void {
    this.hasUserInteracted = true;
    // 1) aggiorna il formControl “vero” col valore interno
    this.formControl.setValue(option.value);
    this.onSelectOption(option);
    // 2) chiudi la dropdown: ora il getter `selectedLabel` troverà la label corretta
    this.term = option.label;
    this.filteredOptions = this.getFilteredOptions();
    this.showDropdown = false;
  }

  onBlur(event: FocusEvent): void {
    const next = event.relatedTarget as HTMLElement | null;

    // Se il focus sta andando dentro il dropdown, NON chiudere
    if (next && this.dropdownRef?.nativeElement.contains(next)) {
      return;
    }

    // Alla perdita di focus il campo è "toccato" solo se l'utente ha realmente
    // interagito (digitazione o selezione): evita il touched da focus/blur programmatici.
    if (this.hasUserInteracted) {
      this.formControl.markAsTouched();
    }

    // recupera il valore attuale del formControl
    const currentValue = this.formControl.value;
    // trova l'opzione corrispondente (se esiste)
    const selectedOption = this.options.find((o) => o.value === currentValue);

    if (selectedOption) {
      this.formControl.setValue(selectedOption?.value);
      this.term = selectedOption.label;
      this.filteredOptions = this.getFilteredOptions();
    }

    // in ogni caso, chiudi la dropdown
    this.showDropdown = false;
  }

  onScroll = () => {
    if (this.showDropdown) {
      this.showDropdown = false;
      this.inputRef?.nativeElement.blur();
    }
  };

  override ngOnDestroy(): void {
    window.removeEventListener('scroll', this.onScroll, true);
    this.formControlSubscription?.unsubscribe();
    this.inputSub?.unsubscribe();
  }

  onKeyDown(event: KeyboardEvent) {
    if (!this.disabled) return;

    const keysThatOpen = ['ArrowDown', 'ArrowUp', ' ', 'Enter'];

    if (keysThatOpen.includes(event.key) || (event.altKey && event.key === 'ArrowDown')) {
      event.preventDefault();
      event.stopPropagation();
    }
  }

  onMouseDown(event: MouseEvent) {
    if (!this.disabled) return;

    event.preventDefault();
    event.stopPropagation();
  }
}
