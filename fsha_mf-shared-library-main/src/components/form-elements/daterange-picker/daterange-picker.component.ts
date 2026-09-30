import { Component, Input, OnInit, SimpleChanges, OnChanges } from '@angular/core';
import flatpickr from 'flatpickr';
import { PickerComponent } from '../picker/picker.component';
import {
  AbstractControl,
  FormControl,
  ReactiveFormsModule,
  ValidationErrors,
} from '@angular/forms';
import { DateTime } from 'luxon';
import { CommonModule } from '@angular/common';

function defaultGetErrorMessage(formControl: FormControl): string | null {
  if (formControl?.errors && formControl.errors['required']) {
    return 'Questo campo è obbligatorio.';
  }

  if (formControl?.errors && formControl.errors['incompleteRange']) {
    return 'Devi selezionare una data di inizio e una di fine.';
  }

  return null;
}

function validatorCompleteRange(control: AbstractControl): ValidationErrors | null {
  const value = control.value;

  if (!value) return null;

  if (typeof value === 'string') {
    const parts = value.split(' al ');

    return parts.length === 2 ? null : { incompleteRange: true }; // non valido
  }

  return null;
}

@Component({
  selector: 'app-rc-daterange-picker',
  standalone: true,
  templateUrl: './daterange-picker.component.html',
  styleUrls: ['./daterange-picker.component.scss'],
  imports: [PickerComponent, ReactiveFormsModule, CommonModule],
})
export class DateRangePickerComponent implements OnInit, OnChanges {
  @Input() placeholder: string = 'Seleziona un intervallo di date';
  @Input() changeCallback: (value: DateTime | string | Date | null) => void = () => {};
  @Input() date: DateTime | string | Date | null = null;
  @Input() formControl: FormControl = new FormControl();
  @Input() label!: string;
  @Input() width: string = '';
  @Input() class: string = 'active';
  @Input() disabled: boolean = false; // solo informativa, non usarla nel codice
  @Input() id: string = 'sample-range-picker';
  @Input() getErrorMessage: CallableFunction = defaultGetErrorMessage;
  @Input() minDate: DateTime | null = null;
  @Input() maxDate: DateTime | null = null;
  @Input() required = false;
  @Input() enableTime: boolean = false;

  dateTime: DateTime | null = null;
  format!: string;

  validatorCompleteRange = validatorCompleteRange;

  get errorMessage() {
    return this.getErrorMessage(this.formControl);
  }

  options: flatpickr.Options.Options = {
    mode: 'range',
    minDate: this.minDate?.toJSDate(),
    maxDate: this.maxDate?.toJSDate(),
    disable: [],
  };

  ngOnInit() {
    this.updateDisabledState = this.updateDisabledState.bind(this);
    this.onChange = this.onChange.bind(this);
    this.format = this.enableTime ? 'dd/MM/yyyy HH:mm' : 'dd/MM/yyyy';
    this.dateTime = this.parseToDateTime(this.date, this.format);
    this.options = {
      ...this.options,
      enableTime: this.enableTime,
      dateFormat: this.enableTime ? 'd/m/Y H:i' : 'd/m/Y',
      minDate: this.minDate?.toJSDate(),
      maxDate: this.maxDate?.toJSDate(),
    };
    this.validatorCompleteRange = this.validatorCompleteRange.bind(this);
    this.formControl.addValidators(this.validatorCompleteRange);
  }

  onChange(stringDate: DateTime | string | Date | null) {
    if (this.changeCallback) {
      this.changeCallback(stringDate);
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['date']) {
      this.dateTime = this.parseToDateTime(changes['date'].currentValue, this.format);
    }
    if (changes['disabled']) {
      this.updateDisabledState(this.formControl);
    }
  }

  private parseToDateTime(input: unknown, format: string): DateTime | null {
    if (!input) return null;

    if (DateTime.isDateTime(input)) return input;

    if (typeof input === 'string') {
      const parsed = DateTime.fromFormat(input, format);
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
