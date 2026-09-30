import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  OnInit,
  Output,
  SimpleChanges,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { IconComponent } from '../../icon/icon.component';
import { PipesModule } from '@mf/pipe/pipes.module';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { ButtonIconComponent } from '../../button-icon/button-icon.component';
import { FileExtended } from 'test-library-frankmd93';

@Component({
  selector: 'app-rc-upload',
  standalone: true,
  imports: [CommonModule, IconComponent, PipesModule, ReactiveFormsModule, ButtonIconComponent],
  templateUrl: './upload.component.html',
  styleUrl: './upload.component.scss',
})
export class UploadComponent implements OnChanges, OnInit {
  filesList: FileExtended[] = [];
  @Input() label: string = '';
  @Input() id: string = '';
  @Input() placeholder: string = 'Carica file';
  @Input() formControl: FormControl = new FormControl();
  @Input() accept: string = '*/*';
  @Input() multiple: boolean = false;
  @Input() disabled: boolean = false;
  @Input() files: FileExtended[] = [];
  @Output() handleUpload = new EventEmitter();
  @Input() required = false;
  @Output() handleRemove = new EventEmitter();
  @Input() color: string = 'white';

  async onFileSelected(event: Event): Promise<void> {
    const target = event.target as HTMLInputElement;
    const uploadedFiles: FileList | null = target.files;

    if (uploadedFiles !== null) {
      const files = this.fileListTransform(uploadedFiles);
      const elaboratedFiles = await Promise.all(files.map((file) => this.readFile(file)));
      this.handleUpload.emit(elaboratedFiles);
    }
  }

  async onRemove(file?: File): Promise<void> {
    this.handleRemove.emit(file);
  }

  private fileListTransform(fileList: FileList): FileExtended[] {
    const _files: File[] = [];
    for (let index = 0; index < fileList.length; index++) {
      const _file = fileList.item(index);
      if (_file) {
        _files.push(_file);
      }
    }
    return _files;
  }

  private readFile(file: File): Promise<FileExtended> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.addEventListener('load', (event) => {
        const { result } = event.target || {};
        if (result) {
          resolve({
            ...file,
            name: file.name,
            size: file.size,
            type: file.type,
            raw: (result as string).split(',')[1],
          });
        } else {
          reject('error in upload file');
        }
      });
      reader.readAsDataURL(file);
    });
  }

  ngOnInit(): void {
    console.log(this.files);
    this.filesList = this.files;
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['files']) {
      this.filesList = changes['files'].currentValue;
    }
  }

  trackByFile(_: number, file: FileExtended): string {
    return file.name;
  }
}
