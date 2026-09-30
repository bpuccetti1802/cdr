import { CommonModule } from '@angular/common';
import {
  Component,
  Input,
  OnInit,
  HostListener,
  ElementRef,
  ViewChild,
  AfterViewInit,
} from '@angular/core';
import { CardWrapperComponent } from '@mf/components/card-wrapper/card-wrapper.component';
import { IconComponent } from '../icon/icon.component';
import { RemoteApplicationType, TabProperties } from 'test-library-frankmd93';

@Component({
  selector: 'app-rc-tabs-vertical',
  standalone: true,
  imports: [CommonModule, CardWrapperComponent, IconComponent],
  templateUrl: './tabs-vertical.component.html',
  styleUrl: './tabs-vertical.component.scss',
})
export class TabsVerticalComponent<T = undefined> implements OnInit, AfterViewInit {
  RemoteApplicationType = RemoteApplicationType;
  @Input() tabs: TabProperties<T>[] = [
    {
      label: 'Tab 1',
      link: 'tab1',
      component: CardWrapperComponent,
      callback: () => {
        return;
      },
    },
    {
      label: 'Tab 2',
      link: 'tab2',
      component: CardWrapperComponent,
      callback: () => {
        return;
      },
    },
  ];
  @Input() applicationType: RemoteApplicationType = RemoteApplicationType.ANGULAR;
  @Input() activeTab?: TabProperties<T> | null = null;

  selectedTab: TabProperties<T> | null = null;
  isMobile: boolean = window.innerWidth < 768;
  showLeftArrow = false;
  showRightArrow = false;

  useDynamicContent = false;

  @ViewChild('tabsWrapper', { static: false }) tabsWrapper!: ElementRef<HTMLDivElement>;

  @HostListener('window:resize', ['$event'])
  onResize(event: Event): void {
    const target = event.target as Window;
    this.isMobile = target.innerWidth < 768;
    this.updateScrollButtons();
  }

  ngOnInit(): void {
    this.selectedTab =
      this.tabs.find((tab) => tab.label === this.activeTabItem?.label) || this.tabs[0];
    this.isMobile = window.innerWidth < 768;
  }

  ngAfterViewInit(): void {
    setTimeout(() => {
      this.updateScrollButtons();
      if (this.isMobile) this.enableTouchScroll();
    }, 100);
  }

  get activeTabItem(): TabProperties<T> {
    return this.activeTab as TabProperties<T>;
  }

  get remoteApplicationType(): RemoteApplicationType {
    return this.applicationType;
  }

  onSelectTab(tab: TabProperties<T>): void {
    this.selectedTab = tab;
    if (this.selectedTab && this.selectedTab.callback) {
      this.selectedTab.callback(this.selectedTab as T);
    }
  }

  scrollTabs(direction: 'left' | 'right'): void {
    if (!this.isMobile) return;
    const wrapper = this.tabsWrapper.nativeElement;
    const scrollAmount = 150;

    if (direction === 'left') {
      wrapper.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    } else {
      wrapper.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }

    setTimeout(() => this.updateScrollButtons(), 300);
  }

  updateScrollButtons(): void {
    const wrapper = this.tabsWrapper.nativeElement;
    const tabs = wrapper.children;

    if (tabs.length === 0) {
      this.showLeftArrow = false;
      this.showRightArrow = false;
      return;
    }

    const tabsArray = Array.prototype.slice.call(tabs) as HTMLElement[];
    const firstTab = tabsArray[0];
    const lastTab = tabsArray.at(-1);

    const wrapperRect = wrapper.getBoundingClientRect();
    const firstTabRect = firstTab.getBoundingClientRect();
    const lastTabRect = lastTab?.getBoundingClientRect();

    this.showLeftArrow = firstTabRect.left < wrapperRect.left;
    this.showRightArrow = lastTabRect ? lastTabRect.right > wrapperRect.right : false;
  }

  enableTouchScroll(): void {
    const wrapper = this.tabsWrapper.nativeElement;
    let isDown = false;
    let startX: number;
    let scrollLeft: number;

    wrapper.addEventListener('touchstart', (event: TouchEvent) => {
      isDown = true;
      startX = event.touches[0].pageX - wrapper.offsetLeft;
      scrollLeft = wrapper.scrollLeft;
    });

    wrapper.addEventListener('touchmove', (event: TouchEvent) => {
      if (!isDown) return;
      event.preventDefault();
      const x = event.touches[0].pageX - wrapper.offsetLeft;
      const walk = (x - startX) * 1.5;
      wrapper.scrollLeft = scrollLeft - walk;
      this.updateScrollButtons();
    });

    wrapper.addEventListener('touchend', () => {
      isDown = false;
    });
  }

  onArrowKeyDown(event: KeyboardEvent): void {
    if (event.key === 'Enter' || event.key === ' ') {
      this.scrollTabs('left');
    }
  }

  trackByTab(_: number, tab: TabProperties<T>): string {
    return tab.label;
  }
}
