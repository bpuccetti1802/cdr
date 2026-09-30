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

/** MIN DATE: richiede data >= min (default inclusivo) */
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

    const p = toMillisUTC(parsed);
    const m = toMillisUTC(minDT);
    if (p == null || m == null) return null;

    // errore se parsed < min (inclusivo) oppure parsed <= min (esclusivo)
    const invalid = inclusive ? p < m : p <= m;
    return invalid ? { minDate: { min: minDT } } : null;
  };
}

/** ✅ MAX DATE: richiede data <= max (default inclusivo) */
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

export const validDateTime: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
  const value = control.value;
  if (!value) return null;

  if (typeof value === 'string') {
    const date = DateTime.fromFormat(value, 'dd/MM/yyyy HH:mm');
    return date.isValid ? null : { invalidDate: true };
  }

  const isValid = (value as DateTime)?.isValid;
  return isValid ? null : { invalidDate: true };
};

function defaultGetErrorMessage(formControl: FormControl): string | null {
  if (
    formControl.errors?.['invalidDate'] &&
    formControl.value &&
    !DateTime.fromFormat(formControl.value, 'dd/MM/yyyy HH:mm').isValid
  ) {
    return 'Questo campo non è una data valida.';
  }

  if (formControl?.errors && formControl.errors['required']) {
    return 'Questo campo è obbligatorio.';
  }

  return null;
}

@Component({
  selector: 'app-rc-datetime-picker',
  standalone: true,
  templateUrl: './datetime-picker.component.html',
  styleUrls: ['./datetime-picker.component.scss'],
  imports: [PickerComponent, ReactiveFormsModule, CommonModule],
})
export class DateTimePickerComponent implements OnInit, OnChanges {
  @Input() placeholder: string = 'Seleziona una data';
  @Input() changeCallback: (value: DateTime | string | Date | null) => void = () => {};
  @Input() date: DateTime | string | Date | null = null;
  @Input() formControl: FormControl = new FormControl();
  @Input() label!: string;
  @Input() width: string = '';
  @Input() class: string = 'active';
  @Input() disabled: boolean = false; // solo informativa, non usarla nel codice
  @Input() id: string = 'sample-picker';
  @Input() getErrorMessage: CallableFunction = defaultGetErrorMessage;
  @Input() minDate: DateTime | null = null;
  @Input() maxDate: DateTime | null = null;
  @Input() required = false;

  dateTime: DateTime | null = null;
  format = 'dd/MM/yyyy HH:mm';

  get errorMessage() {
    return this.getErrorMessage(this.formControl);
  }

  options: flatpickr.Options.Options = {
    mode: 'single',
    enableTime: true,
    dateFormat: 'd/m/Y H:i',
    minDate: this.minDate?.toJSDate(),
    maxDate: this.maxDate?.toJSDate(),
  };

  ngOnInit() {
    this.updateDisabledState = this.updateDisabledState.bind(this);
    this.onChange = this.onChange.bind(this);
    this.dateTime = this.parseToDateTime(this.date);
    this.options = {
      ...this.options,
      minDate: this.minDate?.toJSDate(),
      maxDate: this.maxDate?.toJSDate(),
    };

    if (this.formControl) {
      const validators = [];
      validators.push(validDateTime);
      if (this.minDate) {
        validators.push(minDateValidator(this.minDate, dateValidatorOptions));
      }
      if (this.maxDate) {
        validators.push(maxDateValidator(this.maxDate, dateValidatorOptions));
      }
      this.formControl.addValidators(validators);
    }
  }

  onChange(stringDate: DateTime | string | Date | null) {
    if (this.changeCallback) {
      this.changeCallback(stringDate);
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['date']) {
      this.dateTime = this.parseToDateTime(changes['date'].currentValue);
    }
    if (changes['disabled']) {
      this.updateDisabledState(this.formControl);
    }
  }

  private parseToDateTime(input: unknown): DateTime | null {
    if (!input) return null;

    if (DateTime.isDateTime(input)) return input;

    if (typeof input === 'string') {
      const parsed = DateTime.fromFormat(input, this.format);
      return parsed.isValid ? parsed : null;
    }

    if (input instanceof Date) {
      return DateTime.fromJSDate(input);
    }

    return null;
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
