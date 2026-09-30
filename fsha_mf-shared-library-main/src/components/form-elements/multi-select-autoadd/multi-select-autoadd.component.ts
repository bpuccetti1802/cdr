import { Component, Input, OnInit } from '@angular/core';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { faClose } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

function defaultGetErrorMessage(formControl: FormControl): string | null {
  if (formControl?.errors) {
    if (formControl.hasError('required')) return 'Questo campo è obbligatorio.';
    if (formControl.hasError('pattern')) return 'Devi inserire un campo valido.';
    if (formControl.hasError('duplicate')) return 'Questa email è già stata aggiunta.';
  }
  return null;
}

@Component({
  selector: 'app-rc-multi-select-autoadd',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule, FontAwesomeModule],
  templateUrl: './multi-select-autoadd.component.html',
  styleUrls: ['./multi-select-autoadd.component.scss'],
})
export class MultiSelectAutoaddComponent implements OnInit {
  @Input() id: string = 'multi-select';
  @Input() label: string = 'Mailing List';
  @Input() placeholder: string = 'Scrivi...';
  @Input() formControl: FormControl = new FormControl();
  @Input() disabled: boolean = false;
  @Input() getErrorMessage: CallableFunction = defaultGetErrorMessage;
  @Input() required = false;
  @Input() tags: string[] = [];
  @Input() tagInput: string = '';

  get errorMessage() {
    return this.getErrorMessage(this.formControl);
  }

  faClose = faClose;

  ngOnInit(): void {
    if (this.formControl.value) this.tags = [...this.formControl.value];

    this.formControl.valueChanges.subscribe((value) => {
      if (Array.isArray(value)) {
        this.tags = [...value];
        this.validateRequired();
      }
    });

    if (this.required) {
      this.validateRequired();
    }
  }

  validateRequired(): void {
    if (!this.required) {
      this.formControl.setErrors(null);
      return;
    }

    const isValid =
      Array.isArray(this.tags) &&
      this.tags.length > 0 &&
      this.tags.every((tag) => tag.trim() !== '');

    this.formControl.setErrors(isValid ? null : { required: true });
  }

  addTag(): void {
    const newTag = this.tagInput.trim();

    if (!newTag) {
      if (this.required) this.validateRequired();
      return;
    }

    if (this.tags.includes(newTag)) {
      this.formControl.setErrors({ duplicate: true });
    } else {
      this.tags.push(newTag);
      this.formControl.setValue(this.tags);
      this.formControl.setErrors(null);
      this.tagInput = '';
    }

    this.formControl.markAsTouched();
  }

  removeTag(index: number): void {
    this.tags.splice(index, 1);
    this.formControl.setValue(this.tags);
    this.validateRequired();
  }

  trackByTag(_: number, tag: string): string {
    return tag;
  }
}
