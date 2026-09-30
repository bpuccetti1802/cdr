import { ChangeDetectorRef, Component, Input } from '@angular/core';
import { FormControl } from '@angular/forms';
import { InputComponent } from '../input/input.component';
import { IconComponent } from '@mf/components/icon/icon.component';
import { CommonModule } from '@angular/common';

function defaultGetErrorMessage(formControl: FormControl): string | null {
  if (formControl?.errors) {
    if (formControl.errors['required']) {
      return 'Questo campo è obbligatorio.';
    }
    if (formControl.errors['pattern']) {
      return `Devi inserire un campo valido.`;
    }
  }
  return null;
}

@Component({
  selector: 'app-rc-input-password',
  standalone: true,
  imports: [InputComponent, IconComponent, CommonModule],
  templateUrl: './input-password.component.html',
  styleUrl: './input-password.component.scss',
})
export class InputPasswordComponent {
  @Input() id!: string;
  @Input() label: string = 'Label';
  @Input() formControl!: FormControl;
  @Input() width: string = '';
  @Input() class: string = '';
  @Input() getErrorMessage: CallableFunction = defaultGetErrorMessage;
  @Input() misuratoreSicurezza: boolean = false;
  passwordVisible = true;

  getErrorMessageElaborated() {
    let error = defaultGetErrorMessage(this.formControl);
    error = this.getErrorMessage(this.formControl);
    return error;
  }

  constructor(private cDR: ChangeDetectorRef) {
    this.getErrorMessageElaborated = this.getErrorMessageElaborated.bind(this);
  }

  showHidePassword(): void {
    this.passwordVisible = !this.passwordVisible;
    this.cDR.detectChanges();
  }
}
