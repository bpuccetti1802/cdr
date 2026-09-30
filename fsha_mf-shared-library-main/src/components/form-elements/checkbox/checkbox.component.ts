import {
  Component,
  EventEmitter,
  forwardRef,
  Input,
  OnDestroy,
  OnInit,
  Output,
} from '@angular/core';
import {
  ControlValueAccessor,
  FormControl,
  NG_VALUE_ACCESSOR,
  ReactiveFormsModule,
} from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Colors } from 'test-library-frankmd93';
import { Subscription, tap } from 'rxjs';

export function defaultGetErrorMessage(formControl: FormControl): string | null {
  if (formControl?.errors && formControl.errors['required']) {
    return 'Questo campo è obbligatorio.';
  } else if (formControl?.errors && formControl.errors['requiredTrue']) {
    return 'Questo campo è obbligatorio.';
  }
  return null;
}

@Component({
  selector: 'app-rc-checkbox',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './checkbox.component.html',
  styleUrls: ['./checkbox.component.scss'],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => CheckboxComponent),
      multi: true,
    },
  ],
})
export class CheckboxComponent implements ControlValueAccessor, OnInit, OnDestroy {
  @Input() id!: string;
  @Input() label: string = '';
  @Input() useValue = false;
  @Input() formControl?: FormControl | null = new FormControl();
  @Input() width: string = '';
  @Input() class: string = 'active';
  @Input() disabled: boolean = false;
  @Input() getErrorMessage: CallableFunction = defaultGetErrorMessage;
  @Input() required = false;
  @Input() bgWhite = false;
  @Input() color: Colors = Colors.primary;
  @Input() fontWeight = 'normal';
  @Input() value: boolean = false;
  @Input() handleChange: (value: boolean, formControl?: FormControl | null) => void = () => {};
  @Output() changeEvent = new EventEmitter();

  formControlSubscription?: Subscription;

  ngOnInit(): void {
    if (!this.useValue) {
      this.formControlSubscription = this.formControl?.valueChanges
        .pipe(tap((v) => this.changeEvent.emit(v)))
        .subscribe();
    }
    if (this.disabled) {
      this.formControl?.disable();
    }
  }

  ngOnDestroy(): void {
    if (this.formControlSubscription) this.formControlSubscription.unsubscribe();
  }

  get valid() {
    return this.formControl?.valid;
  }

  get touched() {
    return this.formControl?.touched;
  }
  getErrorMessageElaborated() {
    if (this.formControl) {
      let error = defaultGetErrorMessage(this.formControl);
      error = this.getErrorMessage(this.formControl);
      return error;
    }
    return;
  }

  get errorMessage() {
    return this.getErrorMessageElaborated();
  }

  onTouched = () => {};

  onKeydown(event: KeyboardEvent) {
    // Tab deve solo spostare il focus
    if (event.key === 'Tab') return;

    // attiva/disattiva con Space o Enter
    if (event.key === ' ' || event.key === 'Spacebar' || event.key === 'Enter') {
      event.preventDefault(); // evita scroll con Space
      this.handleCheckboxChange(!this.value);
    }
  }

  handleCheckboxChange(value: boolean): void {
    this.value = value;
    this.handleChange(value, this.formControl);
    this.onTouched();
  }

  writeValue(value: boolean): void {
    this.value = value;
  }

  registerOnChange(function_: (value: boolean) => void): void {
    this.handleChange = function_;
  }

  registerOnTouched(function_: () => void): void {
    this.onTouched = function_;
  }
}
