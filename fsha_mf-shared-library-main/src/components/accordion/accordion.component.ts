import { CommonModule } from '@angular/common';
import {
  AfterViewInit,
  ChangeDetectorRef,
  Component,
  ContentChild,
  EmbeddedViewRef,
  EventEmitter,
  Input,
  OnDestroy,
  Output,
  TemplateRef,
  ViewChild,
  ViewContainerRef,
} from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { Icon, IconComponent } from '../icon/icon.component';
import { IconSize } from 'test-library-frankmd93';

@Component({
  selector: 'app-rc-accordion',
  standalone: true,
  imports: [CommonModule, HttpClientModule, IconComponent],
  styleUrl: './accordion.component.scss',
  templateUrl: './accordion.component.html',
})
export class AccordionComponent implements AfterViewInit, OnDestroy {
  @ViewChild('contentContainer', { read: ViewContainerRef, static: true })
  contentContainer?: ViewContainerRef;

  // v1: contenuto proiettato via <ng-template>...</ng-template>
  @ContentChild(TemplateRef) projectedContent?: TemplateRef<unknown>;

  // v2: contenuto passato come input
  @Input() internalProjectedContent?: TemplateRef<unknown>;

  @Input() id: string = '';
  @Input() expanded: boolean = false;
  @Input() useIcons = false;
  @Input() title: string = '';
  @Input() iconTitle?: string;
  @Input() iconName?: string;
  @Input() iconColor?: string;
  @Input() icons?: Icon[];

  /**
   * v2 behaviour: se true, quando chiudi distrugge la view e libera memoria.
   * Default false = comportamento v1 (non smonta alla chiusura).
   */
  @Input() unmountOnCollapse: boolean = false;

  @Output() toggleAccordion = new EventEmitter<string>();

  /**
   * Output aggiuntivi (opzionali) per chi vuole qualcosa di esplicito.
   * Non rompe nulla perché sono nuovi.
   */
  @Output() toggled = new EventEmitter<{ id: string; expanded: boolean }>();
  @Output() toggledId = new EventEmitter<string>();
  @Output() toggledExpanded = new EventEmitter<boolean>();

  IconSize = IconSize;

  useDynamicContent = false;

  private viewRef?: EmbeddedViewRef<unknown>;
  private transitionHandler?: (element: TransitionEvent) => void;

  constructor(private cdr: ChangeDetectorRef) {}

  trackByIcon(_: number, icon: Icon): string {
    return icon.iconName ?? 'default-icon';
  }

  ngAfterViewInit(): void {
    // Nota: nella v1 c'era una logica strana su createEmbeddedView.
    // Qui manteniamo "useDynamicContent" come flag informativo, senza affidarsi a check errati.
    this.useDynamicContent = !this.projectedContent && !this.contentContainer?.createEmbeddedView;

    // Se parte aperto, garantiamo che il contenuto sia montato (v2) e visibile (v1)
    if (this.expanded) {
      this.ensureShownClass(true);
      this.mountTemplateIfNeeded();
      this.cdr.detectChanges();
    }
  }

  toggle(expanded?: boolean) {
    const next = typeof expanded === 'boolean' ? expanded : !this.expanded;
    this.expanded = next;

    // Emissioni per compatibilità (v1/v2) + nuove emissioni esplicite
    this.toggleAccordion.emit(this.id); // v2 payload

    // Gestione show class + transition (compat v1/v2)
    this.ensureShownClass(this.expanded);
    this.attachOneShotTransitionEnd();

    // Mount/unmount stile v2 (controllato via input per non regredire)
    if (this.expanded) {
      this.mountTemplateIfNeeded();
    } else if (this.unmountOnCollapse) {
      this.unmountTemplate();
    }

    this.cdr.detectChanges();
  }

  private getCollapseElement(): HTMLElement | null {
    return document.getElementById('collapse1b-' + this.id);
  }

  private ensureShownClass(expanded: boolean) {
    const element = this.getCollapseElement();
    if (!element) return;

    if (expanded) {
      element.classList.add('show');
    }
    // se chiude, lasciamo che sia la transitionend a togliere show (come nei tuoi componenti)
  }

  private attachOneShotTransitionEnd() {
    const element = this.getCollapseElement();
    if (!element) return;

    // rimuovi eventuale handler precedente
    if (this.transitionHandler) {
      element.removeEventListener('transitionend', this.transitionHandler);
      this.transitionHandler = undefined;
    }

    this.transitionHandler = () => {
      const element = this.getCollapseElement();
      if (!element) return;

      const hasShow = element.className.includes('show');

      if (!this.expanded && hasShow) {
        element.classList.remove('show');
      } else if (this.expanded && !hasShow) {
        element.classList.add('show');
      }

      // one-shot
      if (this.transitionHandler) {
        element.removeEventListener('transitionend', this.transitionHandler);
        this.transitionHandler = undefined;
      }

      this.cdr.detectChanges();
    };

    element.addEventListener('transitionend', this.transitionHandler);
  }

  private mountTemplateIfNeeded() {
    if (!this.contentContainer) return;

    const template = this.getTemplate();
    if (!template) return;

    // se già montato, non duplicare
    if (this.viewRef) return;

    this.contentContainer?.clear();
    this.viewRef = this.contentContainer?.createEmbeddedView(template, {
      expanded: this.expanded,
    });
  }

  private unmountTemplate() {
    this.viewRef?.destroy();
    this.viewRef = undefined;
    this.contentContainer?.clear();
  }

  ngOnDestroy(): void {
    const element = this.getCollapseElement();
    if (element && this.transitionHandler) {
      element.removeEventListener('transitionend', this.transitionHandler);
      this.transitionHandler = undefined;
    }
    this.unmountTemplate();
  }

  private getTemplate(): TemplateRef<unknown> | undefined {
    return this.internalProjectedContent ?? this.projectedContent;
  }
}
