import {
  Component,
  AfterViewInit,
  ViewChildren,
  ElementRef,
  QueryList,
  Renderer2,
  Input,
  OnInit,
} from '@angular/core';
import { FormControl } from '@angular/forms';
import { CommonModule } from '@angular/common';

export enum KeyCode {
  Backspace = 'Backspace',
}

@Component({
  selector: 'app-rc-otp',
  templateUrl: './otp.component.html',
  styleUrls: ['./otp.component.scss'],
  standalone: true,
  imports: [CommonModule],
})
export class OtpComponent implements AfterViewInit, OnInit {
  @Input() id!: string;
  @Input() boxNumber: number = 5;
  @Input() type: string = 'text';
  @Input() handleChange?: (value: string) => void;
  @Input() formControl?: FormControl | null = undefined;

  @ViewChildren('otpInput') otpInputs!: QueryList<ElementRef>;

  private internalFormControl = new FormControl('');
  concatenatedItem = '';

  //controlla handleChange (per react) e formControl (per angular) non possono essere passati entrambi.
  ngOnInit(): void {
    const hasFormControl = this.formControl instanceof FormControl;
    const hasOnChange = this.handleChange && this.handleChange !== (() => {});

    if (hasFormControl && hasOnChange) {
      throw new Error(
        'OtpComponent: Non puoi passare sia formControl che handleChange. Passa solo uno dei due.',
      );
    }
  }

  constructor(private renderer: Renderer2) {}

  private setUpKeyNavigation() {
    const inputs = this.otpInputs.toArray();

    inputs.forEach((input, index) => {
      this.renderer.listen(input.nativeElement, 'keydown', (event: KeyboardEvent) => {
        const key = event.key;

        if (key === KeyCode.Backspace) {
          event.preventDefault();
          input.nativeElement.value = '';
          this.updateOtpValue();
          if (index > 0) {
            inputs[index - 1].nativeElement.focus();
          }
        } else if (/^[a-zA-Z0-9]$/.test(key)) {
          event.preventDefault();
          input.nativeElement.value = key;
          this.updateOtpValue();
          if (index < inputs.length - 1) {
            inputs[index + 1].nativeElement.focus();
          }
        }
      });
    });
  }

  ngAfterViewInit() {
    this.setUpKeyNavigation();
  }

  updateOtpValue() {
    const code = this.otpInputs.map((input) => input.nativeElement.value).join('');
    this.concatenatedItem = code;
    this.internalFormControl.setValue(code);
    if (this.formControl instanceof FormControl) {
      this.formControl.setValue(code);
    } else if (this.handleChange) {
      this.handleChange(code);
    }
  }

  // controlla il numero dei campi (box) necessari.
  getBoxArray(): number[] {
    return Array.from({ length: this.boxNumber }, (_, index) => index);
  }

  trackByIndex(index: number): number {
    return index;
  }
}
