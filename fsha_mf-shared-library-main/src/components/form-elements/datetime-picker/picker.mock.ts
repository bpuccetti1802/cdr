import { Component, EventEmitter, forwardRef, Input, Output } from '@angular/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';
import { DateTime } from 'luxon';
@Component({
  selector: 'app-rc-picker',
  template: '',
  standalone: true,
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => MockPickerComponent),
      multi: true,
    },
  ],
})
export class MockPickerComponent implements ControlValueAccessor {
  @Input() placeholder: string = 'Seleziona una data';
  @Input() options: unknown = {};
  @Output() dateChange = new EventEmitter<DateTime | null>();
  @Input() date: DateTime | null = null;
  @Input() disabled: boolean = false;
  @Input() id: string = 'mock-picker';
  private onChange: (value: DateTime | null) => void = () => {};
  private onTouched: () => void = () => {};
  writeValue(value: DateTime | null): void {
    this.date = value;
  }
  registerOnChange(function_: (value: DateTime | null) => void): void {
    this.onChange = function_;
  }
  registerOnTouched(function_: () => void): void {
    this.onTouched = function_;
  }
  setDisabledState(isDisabled: boolean): void {
    this.disabled = isDisabled;
  }
}
