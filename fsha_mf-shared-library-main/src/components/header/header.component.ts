import { CommonModule } from '@angular/common';
import {
  AfterViewInit,
  Component,
  ElementRef,
  EventEmitter,
  HostListener,
  Input,
  Output,
  ViewChild,
} from '@angular/core';
import { RouterModule } from '@angular/router';
import { IconComponent } from '../icon/icon.component';
import { noop } from 'rxjs';
import { EventBus } from '@mf/core/event-bus/event-bus';
import { EnteInfo, IconSize, MenuItem } from 'test-library-frankmd93';
import { LayoutService } from '@mf/services/layout.service';
import { BaseHrefService } from '@mf/services/base-href/base-href.service';
import { WideContainerDirective } from '@mf/directives/wide-container/wide-container.directive';

@Component({
  selector: 'app-mf-header',
  standalone: true,
  imports: [CommonModule, RouterModule, IconComponent, WideContainerDirective],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent implements AfterViewInit {
  @ViewChild('itHeaderSlimWrapper', { static: false, read: ElementRef })
  itHeaderSlimWrapper!: ElementRef;

  @ViewChild('itHeaderSlimWrapperContent', { static: true, read: ElementRef })
  itHeaderSlimWrapperContent!: ElementRef;

  @ViewChild('navbarBrand', { static: true, read: ElementRef })
  navbarBrand!: ElementRef;

  @ViewChild('userNameButton', { static: true, read: ElementRef })
  userNameButton!: ElementRef;

  @ViewChild('itBrandTitle', { static: true, read: ElementRef })
  itBrandTitle!: ElementRef;

  @ViewChild('itBrandTagline', { static: true, read: ElementRef })
  itBrandTagline!: ElementRef;

  @ViewChild('loginButton', { static: false, read: ElementRef })
  loginButton!: ElementRef;

  @ViewChild('itHeaderCenterWrapper', { static: true, read: ElementRef })
  itHeaderCenterWrapper!: ElementRef;

  @ViewChild('roundedIcon', { static: false, read: ElementRef })
  roundedIcon!: ElementRef;

  @Input() baseUrl: string = '/mfSharedLibrary';

  @Input() enteAppartenenza: string = 'Ente appartenenza';

  @Input() isVisibleLanguages: boolean = false;

  @Input() isVisibleSocials: boolean = false;

  @Input() isVisibleSearch: boolean = false;

  @Input() useGreyScaleTheme = true;

  @Input() greyScaleColor = '0';

  @Input() color = 'primary';

  @Input() logo: string = this.useGreyScaleTheme
    ? `/assets/images/logo_roma-rosso.png`
    : `/assets/images/rc-logo.png`;

  @Input() ente: EnteInfo = {
    label: '',
    tagline: 'Comune di Roma',
  };

  @Input() isVisibleLogin: boolean = true;

  @Input() isExtendedLayout: boolean = true;

  @Input() slimHeaderMenuLinks!: MenuItem[];

  @Input() loginButtonUrl!: string;

  @Output() login = new EventEmitter<void>();

  @Input() isLogged: boolean = true;

  @Input() userName: string = '';

  @Input() userInitial: string = ''; //per aggiungere le iniziali nel logo user

  @Output() logout = new EventEmitter<void>();

  @Input() profileEditShouldVisible = false;

  @Input() profileEditUrl!: string;

  @Input() onLogin: () => void = noop;

  @Input() onLogOut: () => void = noop;

  @Input() actionLink?: { label: string; iconName?: string; onClick: () => void };

  @ViewChild('headerDiv', { static: false }) private headerDiv:
    | ElementRef<HTMLDivElement>
    | undefined;

  private eventBus = EventBus.getInstance();

  IconSize = IconSize;

  // Toogle expanded layout
  get isExpanded() {
    return this.layoutService.isExpanded;
  }
  layoutModeLabel = 'Layout Esteso';
  constructor(
    private layoutService: LayoutService,
    private baseHref: BaseHrefService,
  ) {
    // this.isExpanded = localStorage.getItem('wideMode') === 'true';

    // Metto il logo con baseHref calcolato automaticamente
    this.baseUrl = this.baseHref.baseUrl + this.baseUrl;
  }

  toggleLayout() {
    this.layoutService.toggleContainerLayout();
  }
  // Toogle expanded layout

  @HostListener('window:scroll', ['$event'])
  isScrolledIntoView() {
    if (this.headerDiv) {
      const heightElement = this.headerDiv.nativeElement.offsetHeight;
      const isFixed = window.scrollY > heightElement ? true : false;
      this.eventBus.dispatchCustomEvent({
        eventName: 'isScrolledIntoView',
        payload: { isFixed },
        reply: false,
      });
    }
  }

  get greyScaleColorClass() {
    return `mf-font-color-grey-${this.greyScaleColor}`;
  }

  get greyScaleColorIconClass() {
    return `mf-icon-color-grey-${this.greyScaleColor}`;
  }

  get greyScaleBackgroundColorClass() {
    return `mf-background-color-grey-${this.greyScaleColor}`;
  }

  get iconColorClass() {
    return `mf-icon-color-${this.color}-main`;
  }

  get colorFontClass() {
    return `mf-font-color-${this.color}-main`;
  }

  get backgroundColorClass() {
    return `mf-background-color-primary-main`;
  }

  logOut(): void {
    this.logout.emit();
    this.onLogOut();
  }

  logIn(): void {
    this.login.emit();
    this.onLogin();
  }

  get bottomUnderlineClass() {
    return `mf-underline-color-secondary-light-1`;
  }

  ngAfterViewInit() {
    if (this.itHeaderSlimWrapper?.nativeElement) {
      const element: HTMLElement = this.itHeaderSlimWrapper.nativeElement;
      element.classList.add(
        this.useGreyScaleTheme ? this.greyScaleBackgroundColorClass : this.backgroundColorClass,
      );
      element.classList.add(
        this.useGreyScaleTheme ? this.colorFontClass : this.greyScaleColorClass,
      );
    }
    if (this.itHeaderSlimWrapperContent?.nativeElement) {
      const element: HTMLElement = this.itHeaderSlimWrapperContent.nativeElement;
      element.classList.add(
        this.useGreyScaleTheme ? this.greyScaleBackgroundColorClass : this.backgroundColorClass,
      );
      element.classList.add(
        this.useGreyScaleTheme ? this.colorFontClass : this.greyScaleColorClass,
      );
    }
    if (this.loginButton?.nativeElement) {
      const element: HTMLElement = this.loginButton.nativeElement;
      element.classList.add(
        this.useGreyScaleTheme ? this.backgroundColorClass : this.greyScaleBackgroundColorClass,
      );
      element.classList.add(
        this.useGreyScaleTheme ? this.greyScaleColorClass : this.colorFontClass,
      );
    }
    if (this.itHeaderCenterWrapper?.nativeElement) {
      const element: HTMLElement = this.itHeaderCenterWrapper.nativeElement;
      element.classList.add(
        this.useGreyScaleTheme ? this.greyScaleBackgroundColorClass : this.backgroundColorClass,
      );
    }
    if (this.navbarBrand?.nativeElement) {
      const element: HTMLElement = this.navbarBrand.nativeElement;
      element.classList.add(
        this.useGreyScaleTheme ? this.colorFontClass : this.greyScaleColorClass,
      );
    }
    if (this.userNameButton?.nativeElement) {
      const element: HTMLElement = this.userNameButton.nativeElement;
      element.classList.add(
        this.useGreyScaleTheme ? this.colorFontClass : this.greyScaleColorClass,
      );
    }
    if (this.itBrandTitle?.nativeElement) {
      const element: HTMLElement = this.itBrandTitle.nativeElement;
      element.classList.add(
        this.useGreyScaleTheme ? this.colorFontClass : this.greyScaleColorClass,
      );
    }
    if (this.itBrandTagline?.nativeElement) {
      const element: HTMLElement = this.itBrandTagline.nativeElement;
      element.classList.add(
        this.useGreyScaleTheme ? this.colorFontClass : this.greyScaleColorClass,
      );
    }
    if (this.roundedIcon?.nativeElement) {
      const element: HTMLElement = this.roundedIcon.nativeElement;
      element.classList.add(
        this.useGreyScaleTheme ? this.backgroundColorClass : this.greyScaleBackgroundColorClass,
      );
    }
  }

  trackByMenuLink(_: number, menuLink: { route: string; label: string }): string {
    return menuLink.route;
  }
}
