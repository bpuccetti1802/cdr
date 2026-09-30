import {
  Component,
  ElementRef,
  AfterViewInit,
  Input,
  Output,
  EventEmitter,
  forwardRef,
  OnInit,
} from '@angular/core';
import flatpickr from 'flatpickr';
import { DateTime } from 'luxon';
import {
  ControlValueAccessor,
  NG_VALUE_ACCESSOR,
  NG_VALIDATORS,
  Validator,
  ValidationErrors,
  FormControl,
  ReactiveFormsModule,
} from '@angular/forms';
import { Italian } from 'flatpickr/dist/l10n/it';
import { CommonModule } from '@angular/common';
import { ButtonIconComponent } from '@mf/components/button-icon/button-icon.component';
import { IconComponent } from '@mf/components/icon/icon.component';
import { Colors, IconSize } from 'test-library-frankmd93';

@Component({
  selector: 'app-rc-picker',
  standalone: true,
  templateUrl: './picker.component.html',
  imports: [CommonModule, ReactiveFormsModule, ButtonIconComponent, IconComponent],
  styleUrl: './picker.component.scss',
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => PickerComponent),
      multi: true,
    },
    {
      provide: NG_VALIDATORS,
      useExisting: forwardRef(() => PickerComponent),
      multi: true,
    },
  ],
})
export class PickerComponent implements AfterViewInit, ControlValueAccessor, Validator, OnInit {
  @Input() placeholder: string = 'Seleziona una data';
  @Input() options: flatpickr.Options.Options = {};
  @Output() dateChange = new EventEmitter<DateTime | null | string>();
  @Input() date: DateTime | null = null;
  @Input() formControl: FormControl = new FormControl();
  /**
   * Serve a gestire lo stile in modalità errore (rosso) quando il componente picker
   * è usato come range input in un time range picker che wrappa il componente.
   * Il main form control viene passato quando questo componente è richiamato da un
   * timerange picker in questo caso la validazione e quindi l'errore e la sua visualizzazione è gestita
   * dal main form control che ha l'informazione sui 2 campi range picker.
   */
  @Input() mainFormControl?: FormControl;
  @Input() label!: string;
  @Input() errorMessage!: string;
  @Input() width: string = '';
  @Input() class: string = 'active';
  @Input() type: string = 'text';
  @Input() disabled: boolean = false;
  @Input() id: string = 'sample-picker';
  @Input() required = false;
  flatpickrInstance: flatpickr.Instance | null = null;
  @Input() changeCallback: (value: string | DateTime | null) => void = () => {};

  private onChange: (value: DateTime | null | string) => void = () => {};
  private onTouched: () => void = () => {};
  protected Colors = Colors;
  protected IconSize = IconSize;

  constructor(private elementReference: ElementRef) {}

  get formControlStyle() {
    return this.mainFormControl ?? this.formControl;
  }

  get isTouchedErrored() {
    return this.formControlStyle && this.formControlStyle.invalid && this.formControl.touched;
  }

  hideLabel: boolean = false;

  ngOnInit(): void {
    if (this.formControl) {
      // Fa in modo che la label venga mostrata solo quando l'input non ha testo al suo interno
      //(Se l'input non è active, gli input active hanno la label fissa fuori).
      this.formControl.valueChanges?.subscribe((value) => {
        if (value !== '' && this.class !== 'active') this.hideLabel = true;
        else if (value === '' && this.class !== 'active') this.hideLabel = false;
      });
    } else {
      console.warn('formControl non è definito');
    }
  }

  ngAfterViewInit(): void {
    const inputElement = this.elementReference.nativeElement.querySelector('input');

    // Configurazione di flatpickr con il formato italiano
    this.flatpickrInstance = flatpickr(inputElement, {
      ...this.options,
      locale: Italian,
      onChange: (selectedDates: Date[]) => {
        let value;
        if (this.options.mode === 'range' && selectedDates.length === 2) {
          value =
            DateTime.fromJSDate(selectedDates[0]).toFormat('dd/MM/yyyy') +
            ' al ' +
            DateTime.fromJSDate(selectedDates[1]).toFormat('dd/MM/yyyy');
        } else {
          value = selectedDates.length > 0 ? DateTime.fromJSDate(selectedDates[0]) : null;
        }
        this.onChange(value);
        this.changeCallback(value);
        this.dateChange.emit(value);
      },
      onClose: () => this.onTouched(),
    });

    if (this.date) {
      // this.writeValue(this.date);
      this.flatpickrInstance.setDate(this.date.toJSDate(), false);
    }
  }

  // ControlValueAccessor Implementation
  writeValue(value: DateTime | string | null): void {
    if (this.flatpickrInstance) {
      if (value && (value as string)?.trim && (value as string)?.trim()) {
        this.flatpickrInstance.setDate(
          DateTime.fromFormat(value as string, 'dd/MM/yyyy').toJSDate(),
          true,
        ); // Imposta la data
      } else if (value && (value as DateTime)?.isValid) {
        this.flatpickrInstance.setDate((value as DateTime).toJSDate(), true);
      } else {
        this.flatpickrInstance.clear(); // Pulisce se il valore è null
      }
    }
  }

  registerOnChange(function_: (value: DateTime | null | string) => void): void {
    this.onChange = function_;
  }

  registerOnTouched(function_: () => void): void {
    this.onTouched = function_;
  }

  validate(): ValidationErrors | null {
    return null;
  }

  setDisabledState(isDisabled: boolean): void {
    this.disabled = isDisabled; // Aggiorna la proprietà
    const inputElement = this.elementReference.nativeElement.querySelector('input');
    if (inputElement) {
      inputElement.disabled = isDisabled;
    }
    if (this.flatpickrInstance) {
      this.flatpickrInstance.set('disable', isDisabled ? [true] : []); // Disabilita Flatpickr
    }
  }
}
