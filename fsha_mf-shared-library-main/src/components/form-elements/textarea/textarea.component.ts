import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { Subscription, tap } from 'rxjs';

function defaultGetErrorMessage(formControl: FormControl): string | null {
  if (formControl?.errors && formControl.errors['required']) {
    return 'Questo campo è obbligatorio.';
  }
  return null;
}

@Component({
  selector: 'app-rc-textarea',
  standalone: true,
  imports: [CommonModule, FontAwesomeModule, ReactiveFormsModule],
  templateUrl: './textarea.component.html',
  styleUrls: ['./textarea.component.scss'],
})
export class TextAreaComponent implements OnInit, OnDestroy {
  @Input() id!: string;
  @Input() label: string = '';
  @Input() placeholder: string = '';
  @Input() formControl: FormControl = new FormControl();
  @Input() width: string = '';
  @Input() disabled: boolean = false;
  @Input() rows: number = 3;
  @Input() resize: string = 'none';
  @Input() getErrorMessage: CallableFunction = defaultGetErrorMessage;
  @Input() required = false;
  @Input() maxLength?: string | number;

  subscription!: Subscription;

  ngOnDestroy(): void {
    if (this.subscription) this.subscription.unsubscribe();
  }

  textLength = 0;

  get textLengthIndicator(): string | null {
    // Se maxLength non è valorizzato, esci subito
    if (this.maxLength == null || this.maxLength === '' || this.maxLength === 0) {
      return null;
    }

    // Converte in numero se è stringa
    const max =
      typeof this.maxLength === 'string' ? Number.parseInt(this.maxLength, 10) : this.maxLength;

    // Se non è un numero valido o <= 0, esci
    if (Number.isNaN(max) || max <= 0) {
      return null;
    }

    // Restituisce la frazione
    return `${this.textLength}/${max}`;
  }

  ngOnInit() {
    this.textLength = this.formControl.value ? this.formControl.value?.length : 0;
    this.subscription = this.formControl.valueChanges
      .pipe(
        tap((value: string) => {
          this.textLength = value ? value?.length : 0;
        }),
      )
      .subscribe();
  }

  get valid() {
    return !!this.formControl?.valid;
  }

  get touched() {
    return !!this.formControl?.touched;
  }

  get errorMessage() {
    return this.getErrorMessage(this.formControl);
  }
  get isDisabledClass() {
    return this.disabled ? 'textarea-disabled' : '';
  }
}
