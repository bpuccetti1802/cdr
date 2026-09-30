import { Directive, HostListener, forwardRef } from '@angular/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';

@Directive({
  selector: '[appMockValueAccessor], [formControl], [formControlName]',
  standalone: true,
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => MockValueAccessorDirective),
      multi: true,
    },
  ],
})
export class MockValueAccessorDirective implements ControlValueAccessor {
  onChange: (event: unknown) => void = () => {};
  onTouched: (event: unknown) => void = () => {};

  writeValue(): void {}
  registerOnChange(function_: (event: unknown) => void): void {
    this.onChange = function_;
  }
  registerOnTouched(function_: (event: unknown) => void): void {
    this.onTouched = function_;
  }
  setDisabledState?(): void {}

  @HostListener('input', ['$event.target.value'])
  handleChange(value: unknown) {
    this.onChange(value);
  }
}
