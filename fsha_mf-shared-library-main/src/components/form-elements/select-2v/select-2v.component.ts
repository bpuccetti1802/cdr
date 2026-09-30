import { Component, Input, OnInit } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { IconSize, SelectItem } from 'test-library-frankmd93';
import { IconComponent } from '@mf/components/icon/icon.component';
import { AbstractDestroyTrackerComponent } from '@mf/components/abstract-subscriptions-tracker/abstract-destroy-tracker.component';
import { takeUntil, tap } from 'rxjs';

function defaultGetErrorMessage(formControl: FormControl): string | null {
  if (formControl?.errors && formControl.errors['required']) {
    return 'Questo campo è obbligatorio.';
  }
  return null;
}

@Component({
  selector: 'app-rc-select-2v',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, IconComponent],
  templateUrl: './select-2v.component.html',
  styleUrls: ['./select-2v.component.scss'],
})
export class Select2VersionComponent extends AbstractDestroyTrackerComponent implements OnInit {
  @Input() id!: string; // ID dinamico
  @Input() label: string = '';
  @Input() placeholder: string = '';
  @Input() formControl: FormControl = new FormControl();
  @Input() options: SelectItem[] = [];
  @Input() disabled: boolean = false;
  @Input() getErrorMessage: CallableFunction = defaultGetErrorMessage;
  @Input() emitChangeItem: (item: SelectItem | null) => void = () => {};
  @Input() required = false;
  @Input() placeholderValue: null | undefined | string = '';
  protected showDropdown = false;
  IconSize = IconSize;

  ngOnInit(): void {
    this.formControl.valueChanges
      .pipe(
        takeUntil(this.destroyed$),
        tap((v) => {
          const selectItem = this.options.find((o) => o.value === v);
          this.emitChangeItem(selectItem ?? null);
        }),
      )
      .subscribe();
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
