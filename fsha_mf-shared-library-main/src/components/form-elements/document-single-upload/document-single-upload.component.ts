import { CommonModule } from '@angular/common';
import {
  Component,
  ElementRef,
  EventEmitter,
  inject,
  Input,
  OnInit,
  ViewChild,
} from '@angular/core';
import { IconComponent } from '../../icon/icon.component';
import { RouterModule } from '@angular/router';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { IconSize } from 'test-library-frankmd93';
import { BaseHrefService } from '@mf/services/base-href/base-href.service';

function defaultGetErrorMessage(formControl: FormControl): string | null {
  if (formControl?.errors && formControl.errors['required']) {
    return 'Questo campo è obbligatorio.';
  }
  return null;
}
@Component({
  selector: 'app-rc-document-single-upload',
  standalone: true,
  imports: [CommonModule, RouterModule, IconComponent, ReactiveFormsModule],
  templateUrl: './document-single-upload.component.html',
  styleUrl: './document-single-upload.component.scss',
})
export class DocumentSingleUploadComponent implements OnInit {
  @Input() uploadedFileNote = 'File obbligatorio';
  @Input() urlDownload!: string | null;
  @Input() useWindowVisualizza = true;
  @Input() visualizza = new EventEmitter<string>();
  @Input() idAllegato!: string;
  @Input() nomeFile!: string;
  @Input() descrizione = '';
  @Input() note = 'File obbligatorio, che richiede firma digitale.';
  @Input() id: string = 'fileInputId';
  @Input() formControl!: FormControl;
  @Input() required = false;
  @Input() getErrorMessage: CallableFunction = defaultGetErrorMessage;
  @Input() disabled = false;
  @Input() accept: string = '*/*';
  @Input() readonly: boolean = false;
  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;
  @Input() useExternalUrlDownload = false;

  maxFileNameLength = 20;
  baseUrl = '/mfSharedLibrary';
  private baseHrefService = inject(BaseHrefService);
  IconSize = IconSize;

  fileName!: string | null;

  fileURL!: string | null;

  getErrorMessageElaborated() {
    let error = defaultGetErrorMessage(this.formControl);
    error = this.getErrorMessage(this.formControl);
    return error;
  }
  get errorMessage() {
    return this.getErrorMessageElaborated();
  }

  get hasFile() {
    return this.useExternalUrlDownload
      ? this.idAllegato !== '' && !!this.idAllegato && this.urlDownload
      : this.fileName ||
          (this.idAllegato !== '' && !!this.idAllegato && (this.urlDownload || this.fileURL));
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.formControl.markAsTouched();

    if (input.files && input.files.length > 0) {
      const file = input.files[0];

      const formData = new FormData();
      formData.append('file', file, file.name);
      formData.set('addFile', 'true');

      // UI state
      this.fileName = file.name;

      // Crea un URL temporaneo e aprilo
      this.fileURL = URL.createObjectURL(file);

      this.formControl.setValue(formData, { emitEvent: true });
      this.formControl.markAsDirty();
      this.formControl.updateValueAndValidity({ emitEvent: false });

      // permette di riselezionare lo stesso file
      if (this.fileInput) this.fileInput.nativeElement.value = '';
    }
  }

  removeFile(): void {
    this.formControl.markAsTouched();
    this.fileName = null;
    this.fileURL = null;

    if (this.idAllegato && this.idAllegato.trim() !== '') {
      const formData = new FormData();
      formData.set('idAllegato', this.idAllegato);
      formData.set('deleteFile', 'true');

      this.formControl.setValue(formData, { emitEvent: true });
    } else {
      this.formControl.setValue(null, { emitEvent: true });
    }

    this.formControl.markAsDirty();
    this.formControl.updateValueAndValidity({ emitEvent: false });

    if (this.fileInput) this.fileInput.nativeElement.value = '';
  }

  resetFileInput() {
    this.fileInput.nativeElement.value = '';
    this.fileInput.nativeElement.click();
  }

  ngOnInit() {
    this.baseUrl = this.baseHrefService.baseUrl + this.baseUrl;
  }

  viewFile(event: Event): void {
    event.stopPropagation();
    if (this.urlDownload && this.useWindowVisualizza) {
      window.open(this.urlDownload, '_blank');
    } else if (this.fileURL && this.useWindowVisualizza) {
      window.open(this.fileURL, '_blank');
    } else {
      this.visualizza.emit(this.urlDownload || '');
    }
  }
  getShortFileName(name: string): string {
    if (name && name.length > this.maxFileNameLength) {
      const extensionIndex = name.lastIndexOf('.');
      const extension = extensionIndex === -1 ? '' : name.slice(Math.max(0, extensionIndex));
      return name.slice(0, Math.max(0, this.maxFileNameLength)) + '...' + extension;
    }
    return name;
  }
  get valid() {
    return !!this.formControl?.valid;
  }

  get touched() {
    return !!this.formControl?.touched;
  }
}
