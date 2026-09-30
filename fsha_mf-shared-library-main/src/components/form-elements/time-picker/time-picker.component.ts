import { Component, Input, OnInit } from '@angular/core';
import {
  AbstractControl,
  FormControl,
  ReactiveFormsModule,
  ValidationErrors,
  ValidatorFn,
} from '@angular/forms';
import flatpickr from 'flatpickr';
import { DateTime } from 'luxon';
import { PickerComponent } from '../picker/picker.component';
import { CommonModule } from '@angular/common';

export const validTime: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
  const value = control.value;
  if (!value) return null;
  if (typeof value === 'string') {
    const date = DateTime.fromFormat(value, 'HH:mm');
    return date.isValid ? null : { invalidTime: true };
  }
  const isValid = (value as DateTime)?.isValid;
  return isValid ? null : { invalidTime: true };
};

function defaultGetErrorMessage(formControl: FormControl): string | null {
  if (
    formControl.errors?.['invalidDate'] &&
    formControl.value &&
    !DateTime.fromFormat(formControl.value, 'HH:mm').isValid
  ) {
    return 'Questo campo non è un orario valido.';
  }
  if (formControl?.errors && formControl.errors['required']) {
    return 'Questo campo è obbligatorio.';
  }
  return null;
}

@Component({
  selector: 'app-rc-time-picker',
  standalone: true,
  templateUrl: './time-picker.component.html',
  styleUrl: './time-picker.component.scss',
  imports: [PickerComponent, ReactiveFormsModule, CommonModule],
})
export class TimePickerComponent implements OnInit {
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
  @Input() minTime: DateTime | null = null;
  @Input() maxTime: DateTime | null = null;
  @Input() required = false;

  dateTime: DateTime | null = null;

  format = 'HH:mm';

  options: flatpickr.Options.Options = {
    mode: 'time',
    time_24hr: true,
    minTime: this.minTime?.toJSDate(),
    maxTime: this.maxTime?.toJSDate(),
  };

  get errorMessage() {
    return this.getErrorMessage(this.formControl);
  }

  ngOnInit() {
    this.updateDisabledState = this.updateDisabledState.bind(this);
    this.onChange = this.onChange.bind(this);
    this.dateTime = this.parseToDateTime(this.date);
    this.options = {
      ...this.options,
      minTime: this.minTime?.toFormat(this.format),
      maxTime: this.maxTime?.toFormat(this.format),
    };
    if (this.formControl) {
      const validators = [];
      validators.push(validTime);
      if (this.minTime) {
        // validators.push(minDateValidator(this.minDate, dateValidatorOptions));
      }
      if (this.maxTime) {
        // validators.push(maxDateValidator(this.maxDate, dateValidatorOptions));
      }
      this.formControl.addValidators(validators);
    }
  }

  onChange(stringDate: DateTime | string | Date | null) {
    if (this.changeCallback) {
      this.changeCallback(stringDate);
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
}
