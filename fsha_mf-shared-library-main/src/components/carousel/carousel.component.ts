import {
  ChangeDetectorRef,
  Component,
  Input,
  TemplateRef,
  ViewChild,
  ViewContainerRef,
  AfterViewInit,
  ElementRef,
  QueryList,
  ViewChildren,
} from '@angular/core';
import { AbstractDestroyTrackerComponent } from '../abstract-subscriptions-tracker/abstract-destroy-tracker.component';
import { CommonModule } from '@angular/common';
import Splide from '@splidejs/splide';
import { SlideItem } from 'test-library-frankmd93';

@Component({
  selector: 'app-rc-carousel',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './carousel.component.html',
  styleUrl: './carousel.component.scss',
})
export class CarouselComponent extends AbstractDestroyTrackerComponent implements AfterViewInit {
  @Input() internalProjectedContent!: TemplateRef<unknown>;
  @Input() useComponent: boolean = true;
  @Input() slides!: SlideItem[];
  @ViewChild('carousel', { static: false }) carousel!: ElementRef;
  splide!: Splide;

  ngAfterViewInit() {
    this.splide = new Splide(this.carousel.nativeElement, {
      perPage: 1,
      breakpoints: {
        768: { perPage: 1 },
      },
    });
    this.splide.mount();
    this.splide.on('move', (next: number, previous: number, destination: number) => {
      this.scrollSlide(destination > previous ? 'right' : 'left', Math.abs(destination - previous));
    });
    this.onSelectSlide(0);
  }

  startIndex = 0;

  scrollSlide(direction: 'left' | 'right', increment: number) {
    let newTabIndex = this.selectedSlideIndex;
    if (direction === 'right' && this.selectedSlideIndex !== this.slides.length - 1) {
      newTabIndex += increment;
    } else if (direction === 'left' && this.selectedSlideIndex !== 0) {
      newTabIndex -= increment;
    }
    this.onSelectSlide(newTabIndex);
  }

  selectedSlideIndex!: number;

  data = { slideIndex: 1 };

  constructor(private cdr: ChangeDetectorRef) {
    super();
  }

  onSelectSlide(index: number) {
    this.splide.go(index);
    this.selectedSlideIndex = index;
    this.renderContent(this.selectedSlideIndex + 1);
  }

  @ViewChildren('contentContainer', { read: ViewContainerRef })
  contentContainers!: QueryList<ViewContainerRef>;

  get selectedContainer(): ViewContainerRef | null {
    return this.contentContainers.toArray()[this.selectedSlideIndex] || null;
  }
  private renderContent(tabIndex: number): void {
    if (this.internalProjectedContent && this.selectedContainer && !this.useComponent) {
      this.selectedContainer?.clear();
      const context = { $implicit: { tabIndex } };
      this.selectedContainer?.createEmbeddedView(this.internalProjectedContent, context);
      this.cdr.detectChanges();
    }
  }

  trackByIndex(_: number, slide: SlideItem): number {
    return slide.index;
  }
}
