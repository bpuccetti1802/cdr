import { CommonModule } from '@angular/common';
import {
  Component,
  Input,
  ViewChild,
  ViewContainerRef,
  ContentChild,
  TemplateRef,
  AfterViewInit,
  ChangeDetectorRef,
} from '@angular/core';
import { WideContainerDirective } from '@mf/directives/wide-container/wide-container.directive';

@Component({
  selector: 'app-rc-card-wrapper',
  standalone: true,
  imports: [CommonModule, WideContainerDirective],
  templateUrl: './card-wrapper.component.html',
  styleUrls: ['./card-wrapper.component.scss'],
})
export class CardWrapperComponent implements AfterViewInit {
  @ViewChild('contentContainer', { read: ViewContainerRef, static: true })
  contentContainer!: ViewContainerRef;
  @ContentChild(TemplateRef) projectedContent?: TemplateRef<unknown>;

  @Input() bgClass = 'bg-white';

  @Input() usePadding = true;

  @Input() useShadow = true;

  @Input() width: 'auto' | 'medium' | 'large' | 'full' = 'auto';

  @Input() h100: boolean = true;

  @Input() container: boolean = false;

  useDynamicContent = false;

  constructor(private cdr: ChangeDetectorRef) {}

  get widthClass(): string {
    return `width-${this.width}`;
  }

  ngAfterViewInit(): void {
    Promise.resolve().then(() => {
      this.useDynamicContent = !this.projectedContent && !this.contentContainer?.createEmbeddedView;
      if (this.useDynamicContent && this.contentContainer && this.projectedContent) {
        this.contentContainer.createEmbeddedView(this.projectedContent);
        this.cdr.detectChanges();
      }
    });
  }
}
