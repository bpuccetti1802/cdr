import {
  AfterViewInit,
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  Component,
  ElementRef,
  EventEmitter,
  HostListener,
  inject,
  Input,
  Output,
  ViewChild,
  OnChanges,
  SimpleChanges,
  NgZone,
  OnDestroy,
} from '@angular/core';
import { ProgressDonut } from 'bootstrap-italia';
import { CommonModule } from '@angular/common';
import { IconComponent } from '@mf/components/icon/icon.component';
import { RouterModule } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { IconSize } from 'test-library-frankmd93';
import { BaseHrefService } from '@mf/services/base-href/base-href.service';

@Component({
  standalone: true,
  selector: 'app-rc-upload-drag-drop',
  templateUrl: './upload-drag-drop.component.html',
  styleUrl: './upload-drag-drop.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule, RouterModule, IconComponent],
})
export class ItUploadDragDropComponent implements AfterViewInit, OnDestroy, OnChanges {
  @Input() accept: string = '*';
  @Input() isMultiUpload: boolean = false;
  @Input() baseUrl: string = '/mfSharedLibrary';
  @Input() dragIcon: string = `/assets/images/icona-pdf.svg`;
  @Input() disabled: boolean = false;
  @Input() set progress(value: number) {
    this.progressSubject.next(value);
  }
  @Input() fileName?: string;
  @Input() extension?: string;
  @Input() fileSize?: string;
  @Output() fileStartUpload = new EventEmitter<File[]>();

  @ViewChild('donutElement') private donutElement?: ElementRef<HTMLDivElement>;
  @Input() protected isLoading = false;
  protected isDragover: boolean = false;
  protected donut?: ProgressDonut;
  protected isSuccess: boolean = false;
  protected readonly _changeDetectorRef: ChangeDetectorRef;
  private isDonutAlreadyLoaded = false;
  private progressSubject = new BehaviorSubject<number>(0);
  IconSize = IconSize;

  get progress(): number {
    return this.progressSubject.getValue();
  }

  constructor(
    private ngZone: NgZone,
    private baseHref: BaseHrefService,
  ) {
    this._changeDetectorRef = inject(ChangeDetectorRef);
    // Metto gli asset e url base icone con baseHref calcolato automaticamente
    this.baseUrl = this.baseHref.baseUrl + this.baseUrl;
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (!this.isDonutAlreadyLoaded && this.donutElement) {
      this.donut = ProgressDonut.getOrCreateInstance(this.donutElement.nativeElement);
      this.isDonutAlreadyLoaded = true;
    }

    if (changes['progress']) {
      this.updateDonut(this.progress);
    }

    if (changes['fileName']) {
      this.fileName = changes['fileName'].currentValue;
    }

    if (changes['isLoading']) {
      this.isLoading = changes['isLoading'].currentValue;
    }

    this._changeDetectorRef.detectChanges();
  }

  ngAfterViewInit(): void {
    console.log(this.donut);
    console.log(this.isMultiUpload);
  }

  ngOnDestroy(): void {
    console.log('[ItUploadDragDropComponent] Destroyed');
  }

  // Dragover listener
  @HostListener('dragover', ['$event'])
  public onDragOver(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragover = !this.isLoading;
  }

  // Dragleave listener
  @HostListener('dragleave', ['$event'])
  public onDragLeave(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragover = false;
  }

  // Drop leave listener
  @HostListener('drop', ['$event'])
  public onDrop(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();

    this.isDragover = false;
    const files = event.dataTransfer?.files;

    if (this.isLoading || !files?.length) {
      return;
    }

    const fileArray = [...(files as unknown as File[])];
    this.start(fileArray); // passa tutti
  }

  onLoadFile(event: Event): void {
    const files = (event.target as HTMLInputElement)?.files;
    if (!files?.length) {
      return;
    }
    const fileArray = [...(files as unknown as File[])];
    this.start(fileArray); // passa tutti
  }

  public start(files: File[]): void {
    const acceptedFiles: File[] = files.filter(
      (file) => this.accept === '*' || this.accept.includes(file.type),
    );
    if (acceptedFiles.length === 0) {
      return;
    }
    this.reset();
    this.isLoading = true;
    // eslint-disable-next-line unicorn/prefer-at
    const lastFile = acceptedFiles[acceptedFiles.length - 1];
    const splitName = lastFile.name.split('.');
    this.fileName = splitName[0];
    this.extension = splitName[1]?.toUpperCase();
    this.fileSize = this.getFileSizeString(lastFile);
    this.fileStartUpload.emit(acceptedFiles);
    console.log(acceptedFiles);
  }

  public success(): void {
    this.isLoading = false;
    this.isSuccess = true;
  }

  getFileSizeString(file: File, decimals = 2): string {
    const bytes = file.size;
    if (!+bytes) {
      return '0 Bytes';
    }
    const k = 1024;
    const dm = Math.max(decimals, 0);
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    const index = Math.floor(Math.log(bytes) / Math.log(k));
    return `${Number.parseFloat((bytes / Math.pow(k, index)).toFixed(dm))} ${sizes[index]}`;
  }

  public reset(): void {
    this.isLoading = false;
    this.isSuccess = false;
    this.fileName = this.extension = this.fileSize = undefined;
    this.donut?.set(0);
  }

  private updateDonut(value: number): void {
    if (value >= 100) {
      this.success();
    } else {
      this.donut?.set(Math.max(value, 0) / 100);
    }
  }
}
