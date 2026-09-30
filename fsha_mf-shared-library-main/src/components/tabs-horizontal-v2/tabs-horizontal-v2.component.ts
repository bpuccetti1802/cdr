import {
  Component,
  Input,
  Type,
  OnInit,
  ElementRef,
  ViewChild,
  HostListener,
  TemplateRef,
  ViewContainerRef,
  ChangeDetectorRef,
  Output,
  EventEmitter,
  AfterViewInit,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { CardWrapperComponent } from '@mf/components/card-wrapper/card-wrapper.component';
import { Icon, IconComponent } from '../icon/icon.component';
import { IconSize, RemoteApplicationType, TabProperties } from 'test-library-frankmd93';

/**
 * @deprecated use version from test-library
 */
type TabItem<T = undefined> = {
  label: string;
  link?: string;
  icons?: Icon[];
  iconName?: string;
  iconColor?: string;
  iconTitle?: string;
  component: Type<unknown> | null;
  disabled?: boolean;
  data?: T;
} & TabProperties<T>;

@Component({
  selector: 'app-rc-tabs-horizontal',
  standalone: true,
  imports: [CommonModule, IconComponent],
  templateUrl: './tabs-horizontal-v2.component.html',
  styleUrl: './tabs-horizontal-v2.component.scss',
})
export class TabsHorizontalVersion2Component<T = undefined> implements OnInit, AfterViewInit {
  @Input() internalProjectedContent!: TemplateRef<unknown>;
  @Input() useIcons = true;
  @Input() tabs: TabItem<T>[] = [
    { label: 'Tab 1', component: CardWrapperComponent },
    { label: 'Tab 2', component: CardWrapperComponent },
    { label: 'Tab 3', component: CardWrapperComponent },
    { label: 'Tab 4', component: CardWrapperComponent },
    { label: 'Tab 5', component: CardWrapperComponent },
    { label: 'Tab 6', component: CardWrapperComponent },
    { label: 'Tab 7', component: CardWrapperComponent },
  ];
  @Input() useComponent: boolean = true;
  @Output() selectTab = new EventEmitter<number>();
  @Input() activeIndex = 0;
  @Input() applicationType: RemoteApplicationType = RemoteApplicationType.ANGULAR;
  @Input() activeTab?: TabItem<T> | null = null;
  @ViewChild('contentContainer', { read: ViewContainerRef, static: true })
  contentContainer!: ViewContainerRef;
  @ViewChild('tabsWrapper', { static: true }) tabsWrapper!: ElementRef<HTMLUListElement>;

  IconSize = IconSize;
  selectedTab: TabItem<T> | null = null;
  showLeftArrow = false;
  showRightArrow = false;
  selectedTabIndex = 0;

  constructor(private cdr: ChangeDetectorRef) {}
  RemoteApplicationType = RemoteApplicationType;

  get activeTabItem(): TabProperties<T> {
    return this.activeTab as TabProperties<T>;
  }

  get remoteApplicationType(): RemoteApplicationType {
    return this.applicationType;
  }

  ngOnInit(): void {
    this.selectedTabIndex = this.activeIndex ?? 0;

    if (this.tabs.length > 0) {
      this.selectedTab =
        this.remoteApplicationType === RemoteApplicationType.ANGULAR
          ? this.tabs[this.selectedTabIndex]
          : this.tabs.find((tab) => tab.label === this.activeTabItem?.label) || this.tabs[0];
      this.renderContent(this.selectedTabIndex);
    }
  }

  private scrollToActiveTab(): void {
    if (!this.tabsWrapper) return;

    const wrapper = this.tabsWrapper.nativeElement as HTMLElement;
    const tabs = wrapper.children;
    if (!tabs || tabs.length === 0) return;

    const activeTab = tabs[this.activeIndex] as HTMLElement;
    if (!activeTab) return;

    // scrollIntoView con inline: 'start' allinea l'elemento al bordo sinistro del contenitore scrollabile
    // use requestAnimationFrame per essere sicuri che il layout sia stabile
    requestAnimationFrame(() => {
      try {
        activeTab.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' });
      } catch {
        // fallback se il browser non supporta le opzioni
        wrapper.scrollTo({ left: activeTab.offsetLeft, behavior: 'smooth' });
      }
      // aggiorna le frecce subito dopo
      setTimeout(() => this.updateScrollButtons(), 250);
    });
  }

  ngAfterViewInit(): void {
    this.scrollToActiveTab();
  }

  @HostListener('window:resize')
  onResize(): void {
    this.updateScrollButtons();
  }

  /**
   * Called when a tab is selected.
   * @param tab The selected tab.
   * @param index The index of the selected tab.
   * Emits the selectTab event with the index of the selected tab.
   * If the selected tab has a callback, it is called with the selected tab as argument.
   * Finally, it renders the content of the selected tab.
   */

  onSelectTab(tab: TabItem<T>, index: number): void {
    this.selectedTabIndex = index;
    this.selectedTab = tab;
    this.selectTab?.emit(this.selectedTabIndex);

    if (
      this.remoteApplicationType === RemoteApplicationType.REACT &&
      this.selectedTab &&
      this.selectedTab.callback
    ) {
      this.selectedTab.callback(this.selectedTab as T);
    }

    this.renderContent(this.selectedTabIndex);
  }

  trackByTab(_: number, tab: TabItem<T>): string {
    return tab.link ?? 'default-link';
  }

  trackByIcon(_: number, icon: Icon): string {
    return icon.iconName ?? 'default-icon';
  }

  scrollTabs(direction: 'left' | 'right', scrollAmount = 160): void {
    const wrapper = this.tabsWrapper.nativeElement;

    if (direction === 'left') {
      wrapper.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    } else {
      wrapper.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
    setTimeout(() => this.updateScrollButtons(), 300);
  }

  updateScrollButtons(): void {
    if (!this.tabsWrapper) return;

    const wrapper = this.tabsWrapper.nativeElement as HTMLElement;
    const maxScrollLeft = wrapper.scrollWidth - wrapper.clientWidth;

    // Nessuno scroll necessario
    if (maxScrollLeft <= 0) {
      this.showLeftArrow = false;
      this.showRightArrow = false;
      return;
    }

    const tolerance = 5; // una piccola tolleranza per evitare errori di pixel

    // Mostra freccia sinistra solo se non sei completamente all'inizio
    this.showLeftArrow = wrapper.scrollLeft > tolerance;

    // Mostra freccia destra solo se non sei completamente alla fine
    this.showRightArrow = wrapper.scrollLeft < maxScrollLeft - tolerance;
  }

  onArrowKeyDown(event: KeyboardEvent): void {
    if (event.key === 'Enter' || event.key === ' ') {
      this.scrollTabs('left');
    }
  }

  private renderContent(tabIndex: number): void {
    if (this.internalProjectedContent && this.contentContainer && !this.useComponent) {
      this.contentContainer?.clear();
      const context = { $implicit: { tabIndex } };
      this.contentContainer?.createEmbeddedView(this.internalProjectedContent, context);
      this.cdr.detectChanges();
    }
  }
}
