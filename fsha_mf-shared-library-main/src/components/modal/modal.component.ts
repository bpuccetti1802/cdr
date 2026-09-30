import {
  Component,
  ElementRef,
  Input,
  OnDestroy,
  Type,
  ViewChild,
  OnChanges,
  SimpleChanges,
  Injector,
  OnInit,
  Output,
  EventEmitter,
} from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconDefinition } from '@fortawesome/free-solid-svg-icons';
import { faFilter, faPlus } from '@fortawesome/free-solid-svg-icons';
import { CommonModule } from '@angular/common';
import { noop, Subscription } from 'rxjs';

@Component({
  selector: 'app-rc-table-modal',
  standalone: true,
  imports: [CommonModule, FontAwesomeModule],
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss'],
})
export class ModalComponent implements OnDestroy, OnChanges, OnInit {
  faPlus: IconDefinition = faPlus;
  faFilter: IconDefinition = faFilter;
  state = false;
  openDelayed = false;
  openDialog = false;
  @Input() id: string = 'rc-modal';
  @Input() contentComponent: Type<unknown> | null = null;
  @Input() footerComponent: Type<unknown> | null = null;
  @Input() titleContent: string = 'Aggiungi';
  @Input() open: boolean = false;
  @Input() close: CallableFunction = noop;
  @Output() childCallback = new EventEmitter<unknown>();
  @Input() size: string = 'lg';
  @Input() componentProps?: Partial<Record<string, unknown>>;
  @Input() closable: boolean = true;
  @Input() level = 0; // max 3 levels 0,1,2.

  // Riferimento al contenitore principale del modal
  @ViewChild('closeModal') closeModal!: ElementRef<HTMLElement>;
  private subscription?: Subscription;

  componentChildInjector!: Injector;

  ngOnInit(): void {
    this.componentChildInjector = Injector.create({
      providers: [
        {
          provide: `componentChildInjector-${this.id}`,
          useValue: {
            childCallback: (item: unknown) => this.childCallback.emit(item),
            close: () => this.close(),
            componentProps: this.componentProps,
          },
        },
      ],
    });
  }

  ngOnDestroy() {
    this.subscription?.unsubscribe();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['open']) {
      this.state = changes['open'].currentValue;
      setTimeout(() => {
        this.openDelayed = changes['open'].currentValue;
        this.openDialog = changes['open'].currentValue;
      }, 100);
    }
  }
}
