import { Component, Input, OnInit } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';

function defaultGetErrorMessage(formControl?: FormControl | null): string | null {
  if (formControl?.errors) {
    if (formControl.errors['required']) {
      return 'Questo campo è obbligatorio.';
    }
    if (formControl.errors['pattern']) {
      return `Devi inserire un valore valido.`;
    }
  }
  return null;
}
@Component({
  selector: 'app-rc-input',
  standalone: true,
  imports: [CommonModule, FontAwesomeModule, ReactiveFormsModule],
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.scss'],
})
export class InputComponent implements OnInit {
  @Input() id!: string;
  @Input() label: string = '';
  @Input() placeholder: string = '';
  @Input() formControl?: FormControl | null = undefined;
  @Input() width: string = '';
  @Input() value: string = '';
  @Input() type: string = 'text';
  @Input() maxLength?: string;
  @Input() disabled: boolean = false;
  @Input() getErrorMessage: CallableFunction = defaultGetErrorMessage;
  @Input() required = false;
  @Input() onChange: (value: Event) => void = () => {};
  @Input() pattern?: string | null;
  @Input() onlyUpperCase?: boolean = false;
  @Input() misuratoreSicurezza: boolean = false;

  // VARIABILI PER MISURATORE DI SICUREZZA
  strength: number = 0;
  strengthText: string = '';
  strengthClass: string = 'bg-muted';
  widthClass: string = 'w-0';

  ngOnInit(): void {
    if (!this.formControl || !this.pattern) return;

    const patternValidator = Validators.pattern(this.pattern);

    this.formControl.addValidators(patternValidator);
    this.formControl.updateValueAndValidity({ emitEvent: false });
  }

  onChangeInput(event: Event) {
    if (this.onlyUpperCase) {
      const input = event.target as HTMLInputElement;
      const value = input.value.toUpperCase();
      input.value = value;
      if (this.formControl) {
        this.formControl.setValue(value, { emitEvent: false });
      }
    }
    this.onChange(event);
    if (this.misuratoreSicurezza) {
      this.checkStrength(event);
    }
  }

  getErrorMessageElaborated() {
    let error = defaultGetErrorMessage(this.formControl);
    if (this.getErrorMessage) {
      error = this.getErrorMessage(this.formControl);
    }
    return error;
  }

  get errorMessage() {
    return this.getErrorMessageElaborated();
  }

  get valid() {
    return this.formControl?.valid;
  }

  get touched() {
    return this.formControl?.touched;
  }

  // Funzione che serve a valorizzare la barra del misuratore di sicurezza
  checkStrength(event: Event) {
    const input = event.target as HTMLInputElement;
    const value = input.value;

    let score = 0;

    if (value.length < 8) {
      this.strength = 0;
      this.strengthText = 'Password troppo breve';
      return;
    }

    // Verifica se c'è almeno una minuscola
    if (/[a-z]/.test(value)) score += 25;
    // Verifica se c'è almeno una maiuscola
    if (/[A-Z]/.test(value)) score += 25;
    // Verifica se c'è almeno un numero
    if (/[0-9]/.test(value)) score += 25;
    // Verifica se c'è almeno un carattere speciale
    if (/[^A-Za-z0-9]/.test(value)) score += 25;

    this.strength = score;
    this.widthClass = `w-${score}`;

    if (score <= 25) {
      this.strengthText = 'Password debole';
      this.strengthClass = 'bg-danger';
    } else if (score <= 50) {
      this.strengthText = 'Password mediocre';
      this.strengthClass = 'bg-warning';
    } else if (score <= 75) {
      this.strengthText = 'Password buona';
      this.strengthClass = 'bg-info';
    } else {
      this.strengthText = 'Password forte';
      this.strengthClass = 'bg-success';
    }
  }
}
