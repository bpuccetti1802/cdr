import { Component, Input, OnInit } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { IconComponent } from '@mf/components/icon/icon.component';
import { IconSize, SelectItem } from 'test-library-frankmd93';

function defaultGetErrorMessage(formControl: FormControl): string | null {
  if (formControl?.errors && formControl.errors['required']) {
    return 'Questo campo è obbligatorio.';
  }
  return null;
}

@Component({
  selector: 'app-rc-select',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, IconComponent],
  templateUrl: './select.component.html',
  styleUrls: ['./select.component.scss'],
})
export class SelectComponent implements OnInit {
  @Input() id!: string; // ID dinamico
  @Input() label: string = ' ';
  @Input() placeholder: string = '';
  @Input() formControl: FormControl = new FormControl();
  @Input() options: SelectItem[] = [];
  @Input() disabled: boolean = false;
  @Input() value?: string;
  @Input() handleChange?: (element?: string) => void;
  @Input() getErrorMessage: CallableFunction = defaultGetErrorMessage;
  @Input() required = false;
  @Input() placeholderValue: null | undefined | string = '';
  protected showDropdown = false;
  IconSize = IconSize;

  ngOnInit() {
    // Inizializza il control dall'input `value` SOLO se il chiamante l'ha passato
    // esplicitamente. Altrimenti il control mantiene il valore che gia' ha (patchato
    // dal chiamante via reactive forms), evitando di azzerarlo ad ogni rimontaggio
    // del SelectComponent (es. quando il DynamicLoader ricrea il componente al cambio
    // di inputsAndHandlers).
    if (this.value !== undefined) {
      this.formControl?.setValue(this.value);
    }
  }

  onChange(event: Event) {
    event.stopPropagation();
    this.showDropdown = !this.showDropdown;
    const selectElement = event.target as HTMLSelectElement;
    if (this.handleChange) {
      this.handleChange(selectElement.value);
    }
  }

  get errorMessage() {
    return this.getErrorMessage(this.formControl);
  }

  trackByOption(_: number, option: { value: string; label: string }): string {
    return option.value;
  }

  get valid() {
    return !!this.formControl?.valid;
  }

  get touched() {
    return !!this.formControl?.touched;
  }

  onKeyDown(event: KeyboardEvent) {
    if (!this.disabled) return;

    const keysThatOpen = ['ArrowDown', 'ArrowUp', ' ', 'Enter'];

    if (keysThatOpen.includes(event.key) || (event.altKey && event.key === 'ArrowDown')) {
      event.preventDefault();
      event.stopPropagation();
    }
  }

  onMouseDown(event: MouseEvent) {
    if (!this.disabled) return;

    event.preventDefault();
    event.stopPropagation();
  }
}
