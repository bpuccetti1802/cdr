import { Component, Input, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { InputComponent } from '../input/input.component';
import { CommonModule } from '@angular/common';

function defaultGetErrorMessage(formControl: FormControl): string | null {
  if (formControl?.errors) {
    if (formControl.errors['required']) {
      return 'Questo campo è obbligatorio.';
    }
    if (formControl.errors['pattern']) {
      return `Devi inserire un valore numerico valido.`;
    }
    if (formControl.errors['max']) {
      return `Devi inserire un valore numerico minore di ` + formControl.errors['max']?.max;
    }
    if (formControl.errors['min']) {
      return `Devi inserire un valore numerico maggiore di ` + formControl.errors['min']?.min;
    }
  }
  return null;
}

@Component({
  selector: 'app-rc-input-number',
  standalone: true,
  imports: [InputComponent, CommonModule],
  templateUrl: './input-number.component.html',
})
export class InputNumberComponent implements OnInit {
  @Input() id!: string;
  @Input() label: string = '';
  @Input() formControl: FormControl<number | null> = new FormControl(null);
  @Input() width: string = '';
  @Input() class: string = '';
  @Input() maxLength?: string;
  @Input() max?: number;
  @Input() min?: number;
  @Input() getErrorMessage: CallableFunction = defaultGetErrorMessage;
  @Input() disabled = false;
  @Input() required = false;
  @Input() pattern: string | null = String.raw`^\d+$`;
  @Input() placeholder: string = '';

  getErrorMessageElaborated() {
    let error = defaultGetErrorMessage(this.formControl);
    error = this.getErrorMessage(this.formControl, this.min || 0, this.max || Infinity);
    return error;
  }

  constructor() {
    this.getErrorMessageElaborated = this.getErrorMessageElaborated.bind(this);
  }

  ngOnInit(): void {
    const validators = [];
    if (this.pattern) {
      validators.push(Validators.pattern(this.pattern));
    }

    if (this.min !== undefined) {
      validators.push(Validators.min(this.min));
    }

    if (this.max !== undefined) {
      validators.push(Validators.max(this.max));
    }

    this.formControl.addValidators(validators);
  }
}
