import { Component, Input, OnInit, SimpleChanges, OnChanges } from '@angular/core';
import flatpickr from 'flatpickr';
import { PickerComponent } from '../picker/picker.component';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { DateTime } from 'luxon';
import { CommonModule } from '@angular/common';
import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

type DateLike = DateTime | Date | string | null | undefined;
type DateLikeOrFunction = DateLike | (() => DateLike);

interface DateValidatorOptions {
  inclusive?: boolean; // default: true (>= min, <= max)
  format?: string; // default: 'dd/MM/yyyy HH:mm'
}

/** Helpers */
const defaultFormat = 'dd/MM/yyyy HH:mm';

const dateValidatorOptions = {
  inclusive: true,
  format: defaultFormat,
};

const resolve = (value?: DateLikeOrFunction): DateLike =>
  typeof value === 'function' ? (value as () => DateLike)() : value;

const toDateTime = (value?: DateLike, format = defaultFormat): DateTime | null => {
  if (!value) return null;
  if (DateTime.isDateTime(value)) return value.isValid ? value : null;
  if (value instanceof Date) return DateTime.fromJSDate(value);
  if (typeof value === 'string') {
    let dt = DateTime.fromISO(value);
    if (!dt.isValid) dt = DateTime.fromFormat(value, format);
    if (!dt.isValid) dt = DateTime.fromFormat(value, 'dd/MM/yyyy');
    return dt.isValid ? dt : null;
  }
  return null;
};

const parseControlValue = (value: DateTime | null, format = defaultFormat): DateTime | null => {
  if (typeof value === 'string') {
    let dt = DateTime.fromFormat(value, format);
    if (!dt.isValid) dt = DateTime.fromFormat(value, 'dd/MM/yyyy');
    return dt.isValid ? dt : null;
  }
  if (value instanceof Date) return DateTime.fromJSDate(value);
  if (DateTime.isDateTime(value)) return (value as DateTime).isValid ? value : null;
  return null;
};

const toMillisUTC = (dt: DateTime | null): number | null => (dt ? dt.toUTC().toMillis() : null);

/**
 * Validator che verifica che una DATA sia compresa tra
 * 01/01/{yearMin} e 31/12/{yearMax}.
 * - Se la data è assente o non valida → lascia ad altri validator (ritorna null).
 * - Se presente e valida → verifica i limiti (inclusivi di default).
 * @param {DateLikeOrFunction} min - La data di riferimento per il limite minimo
 * @param {DateValidatorOptions} options - Opzioni per il validator
 * @returns {(control: AbstractControl) => ValidationErrors | null} - Funzione di validazione
 */
export function minDateValidator(min: DateLikeOrFunction, options: DateValidatorOptions = {}) {
  const inclusive = options.inclusive ?? true;
  const fmt = options.format ?? defaultFormat;

  return (control: AbstractControl): ValidationErrors | null => {
    const value = control.value;
    if (value == null || value === '') return null; // lascia a required

    const parsed = parseControlValue(value, fmt);
    if (!parsed) return null; // lascia ad un validator "invalidDate"

    const minDT = toDateTime(resolve(min), fmt);
    if (!minDT) return null; // nessun limite

    const p = toMillisUTC(parsed.startOf('day'));
    const m = toMillisUTC(minDT.startOf('day'));

    if (p == null || m == null) return null;

    // errore se parsed < min (inclusivo) oppure parsed <= min (esclusivo)
    const invalid = inclusive ? p < m : p <= m;
    return invalid ? { minDate: { min: minDT } } : null;
  };
}

/**
 * Validator che verifica che una DATA sia compresa tra
 * 01/01/{yearMin} e 31/12/{yearMax}.
 * - Se la data è assente o non valida → lascia ad altri validator (ritorna null).
 * - Se presente e valida → verifica i limiti (inclusivi di default).
 * @param {DateLikeOrFunction} max - La data di riferimento per il limite massimo
 * @param {DateValidatorOptions} options - Opzioni per il validator
 * @returns {(control: AbstractControl) => ValidationErrors | null} - Funzione di validazione
 */
export function maxDateValidator(
  max: DateLikeOrFunction,
  options: DateValidatorOptions = {},
): ValidatorFn {
  const inclusive = options.inclusive ?? true;
  const fmt = options.format ?? defaultFormat;

  return (control: AbstractControl): ValidationErrors | null => {
    const value = control.value;
    if (value == null || value === '') return null;

    const parsed = parseControlValue(value, fmt);
    if (!parsed) return null;

    const maxDT = toDateTime(resolve(max), fmt);
    if (!maxDT) return null;

    const p = toMillisUTC(parsed);
    const M = toMillisUTC(maxDT);
    if (p == null || M == null) return null;

    // errore se parsed > max (inclusivo) oppure parsed >= max (esclusivo)
    const invalid = inclusive ? p > M : p >= M;
    return invalid ? { maxDate: { max: maxDT } } : null;
  };
}

export const validDate: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
  const value = control.value;
  if (!value) return null;
  if (typeof value === 'string') {
    const date = DateTime.fromFormat(value, 'dd/MM/yyyy');
    return date.isValid ? null : { invalidDate: true };
  }
  const isValid = value ? (value as DateTime)?.isValid : false;
  return isValid ? null : { invalidDate: true };
};

function defaultGetErrorMessage(formControl: FormControl): string | null {
  if (
    formControl?.errors?.['invalidDate'] &&
    formControl?.value &&
    !DateTime.fromFormat(formControl.value, 'dd/MM/yyyy').isValid
  ) {
    return 'Questo campo non è una data valida.';
  }
  if (formControl?.errors && formControl.errors['required']) {
    return 'Questo campo è obbligatorio.';
  }
  return null;
}
@Component({
  selector: 'app-rc-date-picker',
  standalone: true,
  templateUrl: './date-picker.component.html',
  imports: [PickerComponent, ReactiveFormsModule, CommonModule],
  styleUrls: ['./date-picker.component.scss'],
})
export class DatePickerComponent implements OnInit, OnChanges {
  @Input() placeholder: string = 'Seleziona una data';
  @Input() date: DateTime | null = null;
  @Input() formControl: FormControl = new FormControl();
  @Input() label!: string;
  @Input() width: string = '';
  @Input() class: string = 'active';
  @Input() disabled: boolean = false;
  @Input() id: string = 'sample-picker';
  @Input() minDate: DateTime | null = null;
  @Input() maxDate: DateTime | null = null;
  @Input() disableArrayDayDate: DateTime[] = [];
  dateTime: DateTime | null = null;
  @Input() getErrorMessage: CallableFunction = defaultGetErrorMessage;
  @Input() required = false;
  format = 'dd/MM/yyyy';

  get errorMessage() {
    return this.getErrorMessage(this.formControl);
  }

  options: flatpickr.Options.Options = {
    mode: 'single',
    enableTime: false,
    dateFormat: 'd/m/Y',
  };

  ngOnInit() {
    this.updateDisabledState.bind(this);
    this.dateTime = this.date || null;
    this.options = {
      ...this.options,
      minDate: this.minDate?.toJSDate(),
      maxDate: this.maxDate?.toJSDate(),
      disable: this.disableArrayDayDate.map((disableDayDate) => disableDayDate.toJSDate()),
    };
    if (this.formControl) {
      const validators = [];
      validators.push(validDate);
      if (this.minDate) {
        validators.push(minDateValidator(this.minDate, dateValidatorOptions));
      }
      if (this.maxDate) {
        validators.push(maxDateValidator(this.maxDate, dateValidatorOptions));
      }
      this.formControl.addValidators(validators);
    }
  }
  ngOnChanges(changes: SimpleChanges) {
    if (changes['disabled']) {
      this.updateDisabledState(this.formControl);
    }
  }

  private updateDisabledState(formControl: FormControl) {
    if (!formControl) {
      return;
    }
    if (this.disabled) {
      formControl.disable({ emitEvent: false });
    } else {
      formControl.enable({ emitEvent: false });
    }
  }
}
