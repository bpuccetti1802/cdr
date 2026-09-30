import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
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
import { AbstractDestroyTrackerComponent } from '@mf/components/abstract-subscriptions-tracker/abstract-destroy-tracker.component';
import { isEmptyValue } from '@mf/utils/helpers';

/**
 * se dall'xml non mi arrivano limiti nel validatore l'utente può inserire orari in qualunque ordine
 * se ho solo uno dei due limiti nel validatore le date devono essere entrambe maggiori di min o minori di max e in ordine
 * se ho entrambi i limiti dal validatore le date devono essere nei limiti ed in ordine
 * nell'ultimo caso se max è minore di min diamo per scontato che il range di validazione scavalca la mezzanotte
 */
function timeRangeValidator(min: DateTime | null, max: DateTime | null): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    if (!control.value) {
      return null;
    }
    const { from, to } = control.value ?? {};
    if (isEmptyValue(from) && isEmptyValue(to)) {
      return { empty: true };
    }
    if (isEmptyValue(from)) {
      return { invalidFrom: true };
    }
    if (isEmptyValue(to)) {
      return { invalidTo: true };
    }
    if ((!max && min && (from < min || from > to)) || (max && !min && (to > max || from > to))) {
      // date fuori range o in ordine errato
      return { invalidRange: true };
    }
    if (max && min) {
      if (max < min) {
        // validazione con ora massima nel giorno successivo
        if ((from < min && from > max) || (to < min && to > max)) {
          // time from o to fuori range
          return { invalidRange: true };
        }
        if (from > to && (to > max || from < min)) {
          // ore inserite in giorni diversi ma nel giorno sbagliato
          return { invalidRange: true };
        }
        if (from < to && !((from >= min && to >= min) || (from <= max && to <= max))) {
          // ore inserite nello stesso giorno ma in ordine errato o fuori range
          return { invalidRange: true };
        }
      } else if (from < min || to > max || from > to) {
        // validazione per range nello stesso giorno ma ore inserite fuori range o in ordine errato
        return { invalidRange: true };
      }
    }
    return null;
  };
}

function defaultGetErrorMessage(formControl: FormControl): string | null {
  if (formControl?.errors && formControl.errors['required']) {
    return 'I campi sono obbligatori.';
  }
  if (formControl?.errors && formControl.errors['empty']) {
    return 'I campi sono obbligatori.';
  }
  return null;
}

@Component({
  selector: 'app-rc-time-picker',
  standalone: true,
  templateUrl: './timerange-picker.component.html',
  styleUrl: './timerange-picker.component.scss',
  imports: [PickerComponent, ReactiveFormsModule, CommonModule],
})
export class TimeRangePickerComponent
  extends AbstractDestroyTrackerComponent
  implements OnInit, OnChanges
{
  @Input() placeholder: string = 'Seleziona un orario';
  @Input() changeCallback: ({ from, to }: { from: string | null; to: string | null }) => void =
    () => {};
  @Input() defaultFrom: DateTime | string | Date | null = null;
  @Input() defaultTo: DateTime | string | Date | null = null;
  @Input() formControl: FormControl = new FormControl();
  @Input() labelFrom!: string;
  @Input() labelTo!: string;
  @Input() width: string = '';
  @Input() class: string = 'active';
  @Input() disabled: boolean = false; // solo informativa, non usarla nel codice
  @Input() id: string = 'sample-picker';
  @Input() getErrorMessage: CallableFunction = defaultGetErrorMessage;
  @Input() minTime: DateTime | null = null;
  @Input() maxTime: DateTime | null = null;
  @Input() required = false;

  formControlTo = new FormControl();
  formControlFrom = new FormControl();

  timeFrom: DateTime | null = null;

  timeTo: DateTime | null = null;

  format = 'HH:mm';

  optionsFrom: flatpickr.Options.Options = {
    mode: 'time',
    time_24hr: true,
  };

  optionsTo: flatpickr.Options.Options = {
    mode: 'time',
    time_24hr: true,
  };

  get errorMessage() {
    return this.getErrorMessage(this.formControl);
  }

  ngOnInit() {
    this.onChangeFrom = this.onChangeFrom.bind(this);
    this.onChangeTo = this.onChangeTo.bind(this);
    this.timeFrom = this.parseToDateTime(this.defaultFrom);
    this.timeTo = this.parseToDateTime(this.defaultTo);
    if (this.timeTo) {
      this.formControlTo.setValue(this.timeTo, { emitEvent: false });
    }
    if (this.timeFrom) {
      this.formControlFrom.setValue(this.timeFrom, { emitEvent: false });
    }
    if (this.formControl) {
      const validators = [];
      validators.push(timeRangeValidator(this.minTime, this.maxTime));
      this.formControl.addValidators(validators);
    }
  }

  onChangeFrom(time: DateTime | string | Date | null) {
    this.timeFrom = this.parseToDateTime(time);
    if (this.changeCallback) {
      this.changeCallback({
        from: this.timeFrom?.toFormat(this.format) ?? null,
        to: this.timeTo?.toFormat(this.format) ?? null,
      });
    }
  }

  onChangeTo(time: DateTime | string | Date | null) {
    this.timeTo = this.parseToDateTime(time);
    if (this.changeCallback) {
      this.changeCallback({
        from: this.timeFrom?.toFormat(this.format) ?? null,
        to: this.timeTo?.toFormat(this.format) ?? null,
      });
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['defaultFrom'] || changes['defaultTo']) {
      this.timeFrom = this.parseToDateTime(changes['defaultFrom'].currentValue);
      this.timeTo = this.parseToDateTime(changes['defaultTo'].currentValue);
    }
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
      this.formControlTo.setValue(null);
      this.formControlTo.disable();
      this.timeTo = null;
      this.formControlFrom.setValue(null);
      this.formControlFrom.disable();
      this.timeFrom = null;
    } else {
      formControl.enable({ emitEvent: false });
      this.formControlTo.enable();
      this.formControlFrom.enable();
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
