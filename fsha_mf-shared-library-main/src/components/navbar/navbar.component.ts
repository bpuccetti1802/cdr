import { CommonModule } from '@angular/common';
import {
  AfterViewInit,
  Component,
  ElementRef,
  HostListener,
  Input,
  OnInit,
  QueryList,
  ViewChild,
  ViewChildren,
} from '@angular/core';
import { Route, Router, RouterModule, Routes } from '@angular/router';
import { IconComponent } from '../icon/icon.component';
import { ResponsiveService } from '@mf/services/responsive/responsive.service';
import { tap } from 'rxjs';
import { EventBus } from '@mf/core/event-bus/event-bus';
import { ButtonIconComponent } from '../button-icon/button-icon.component';
import { MediaBreakpointEnum, IconSize, DataRoute, NavbarItem } from 'test-library-frankmd93';
import { WideContainerDirective } from '@mf/directives/wide-container/wide-container.directive';

@Component({
  selector: 'app-mf-navbar',
  standalone: true,
  imports: [CommonModule, RouterModule, IconComponent, ButtonIconComponent, WideContainerDirective],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss',
})
export class NavbarComponent implements OnInit, AfterViewInit {
  @Input() useGreyScaleTheme = true;
  @Input() greyScaleColor = '0';
  @Input() color = 'primary';
  @Input() useRoutes = false;
  @Input() routes?: Routes;
  @Input() useRoutesWithHome = false;
  @Input() menuItems!: NavbarItem[];
  @Input() isLogged: boolean = true;

  @ViewChild('navbarNav', { static: false, read: ElementRef })
  navbarNav!: ElementRef;
  @ViewChild('navbar', { static: false, read: ElementRef })
  navbar!: ElementRef;
  @ViewChildren('navbarLink', { read: ElementRef })
  navbarLinks!: QueryList<ElementRef>;
  @ViewChildren('dropdownItem', { read: ElementRef })
  dropdownItems!: QueryList<ElementRef>;

  private eventBus = EventBus.getInstance();

  navbarFixed: boolean = false;

  IconSize = IconSize;

  get greyScaleColorClass() {
    return `mf-font-color-grey-${this.greyScaleColor}`;
  }

  get greyScaleIconColorClass() {
    return `mf-icon-color-secondary-main`;
  }

  get greyScaleBackgroundColorClass() {
    return `mf-background-color-grey-${this.greyScaleColor}`;
  }

  get colorClass() {
    return `mf-font-color-${this.color}-main`;
  }

  get iconColorClass() {
    return `mf-icon-color-${this.color}-main mf-font-color-${this.color}-main`;
  }

  get backgroundColorClass() {
    return `mf-background-color-${this.color}-main`;
  }

  routesWithHome!: Routes | NavbarItem[];

  observers: MutationObserver[] = [];

  constructor(
    private router: Router,
    private responsiveService: ResponsiveService,
  ) {}

  isMobile = false;

  get bottomUnderlineClass() {
    return this.isMobile
      ? ''
      : this.useGreyScaleTheme
        ? `mf-underline-color-${this.color}-main-3`
        : `mf-underline-color-${this.color}-main-1`;
  }

  iconExpandSize = IconSize.sm;

  visibleRoutes: Routes | NavbarItem[] = [];
  overflowRoutes: Routes | NavbarItem[] = [];

  @HostListener('window:resize')
  /**
   * Ricalcola l'overflow della barra di navigazione quando la finestra
   * del browser viene ridimensionata.
   */
  onResize() {
    this.calculateOverflow();
  }

  /**
   * Calcola quali elementi della barra di navigazione
   * dovranno essere visualizzati direttamente o meno in un dropdown
   * a seconda dell'overflow della barra di navigazione
   *
   * Se è mobile, non calcoliamo l'overflow e visualizziamo tutti gli elementi
   * Se non è mobile, calcoliamo l'overflow e visualizziamo solo gli elementi che
   * non superano la larghezza disponibile
   *
   * La funzione utilizza un elemento temporaneo per misurare la larghezza
   * degli elementi della barra di navigazione
   */
  calculateOverflow() {
    if (!this.navbarNav) return;

    // se è mobile, non calcoliamo l'overflow
    if (this.isMobile) {
      this.visibleRoutes = this.routesWithHome as Routes;
      this.overflowRoutes = [];
      return;
    }

    const containerWidth = this.navbar.nativeElement.offsetWidth;

    this.visibleRoutes = [];
    this.overflowRoutes = [];

    let usedWidth = 0;

    // elemento temporaneo per misurare
    const temporary = document.createElement('li');
    temporary.style.visibility = 'hidden';
    temporary.style.position = 'absolute';
    temporary.className = 'nav-item';

    document.body.append(temporary);

    for (const route of this.routesWithHome) {
      temporary.innerHTML = `<a class="nav-link">${((route as Route).data as DataRoute)?.label || (route as NavbarItem)?.label || ''}</a>`;
      const width = temporary.offsetWidth;

      if (usedWidth + width < containerWidth - 500) {
        // 80px buffer "Altro"
        this.visibleRoutes.push(route as NavbarItem);
        usedWidth += width;
      } else {
        this.overflowRoutes.push(route as NavbarItem);
      }
    }

    temporary.remove();
  }

  ngAfterViewInit(): void {
    setTimeout(() => this.calculateOverflow(), 0);

    if (this.navbarNav?.nativeElement) {
      const element: HTMLElement = this.navbarNav.nativeElement;
      element.classList.add(
        this.useGreyScaleTheme ? this.greyScaleBackgroundColorClass : this.backgroundColorClass,
      );
      element.classList.add(this.useGreyScaleTheme ? this.colorClass : this.greyScaleColorClass);
    }
    if (this.navbar?.nativeElement) {
      const element: HTMLElement = this.navbar.nativeElement;
      element.classList.add(
        this.useGreyScaleTheme ? this.greyScaleBackgroundColorClass : this.backgroundColorClass,
      );
      element.classList.add(this.useGreyScaleTheme ? this.colorClass : this.greyScaleColorClass);
    }

    if (this.isMobile) {
      this.dropdownItems.forEach((linkReference: ElementRef) => {
        const element: HTMLElement = linkReference.nativeElement;
        element.classList.add(this.colorClass);
        element.classList.add(this.greyScaleBackgroundColorClass);
      });
    } else {
      this.dropdownItems.forEach((linkReference: ElementRef) => {
        const element: HTMLElement = linkReference.nativeElement;
        element.classList.add(this.colorClass);
      });
    }
    if (this.isMobile) {
      this.navbarLinks.forEach((linkReference: ElementRef) => {
        const element: HTMLElement = linkReference.nativeElement;
        element.classList.add(this.colorClass);
        element.classList.add(this.greyScaleBackgroundColorClass);
      });
    } else {
      this.navbarLinks.forEach((linkReference: ElementRef) => {
        const element: HTMLElement = linkReference.nativeElement;
        element.classList.add(this.useGreyScaleTheme ? this.colorClass : this.greyScaleColorClass);
      });
    }
  }

  ngOnInit() {
    this.eventBus.addCustomEventListener('isScrolledIntoView', async (event) => {
      this.navbarFixed = (event.detail.payload as { isFixed: boolean })?.isFixed;
    });
    this.responsiveService.mediaBreakpoint$
      .pipe(
        tap((mediaBreakpoint) => {
          console.log('mediaBreakpoint', mediaBreakpoint);
          this.isMobile =
            mediaBreakpoint === MediaBreakpointEnum.XS || mediaBreakpoint === MediaBreakpointEnum.SM
              ? true
              : false;
        }),
      )
      .subscribe();
    this.routesWithHome = this.useRoutes
      ? this.useRoutesWithHome
        ? [...(this.routes || [])]
        : [{ path: '', pathMatch: 'full', data: { label: 'Home' } }, ...(this.routes || [])]
      : this.useRoutesWithHome
        ? [...(this.routes || [])]
        : [
            { path: '', pathMatch: 'full', data: { label: 'Home' } },
            ...this.mapMenuItemsInRoutes(),
          ];
  }

  mapMenuItemsInRoutes(): Routes | NavbarItem[] {
    return (
      this.menuItems?.map((menuItem) => ({
        path: menuItem.route,
        data: {
          label: menuItem.label,
        },
        children: menuItem.hasChildren ? menuItem.children : [],
      })) || []
    );
  }

  getDynamicClasses(route: Route) {
    const isActive = this.isDropdownActive(route);

    return {
      'mf-font-color-secondary-main': !isActive,
      'mf-font-color-primary-main': isActive,
      [this.bottomUnderlineClass]: isActive,
    };
  }

  isDropdownActive(route: Route): boolean {
    return this.router.url.includes(`/${route.path}`);
  }

  getFullPath(path: string): string[] | null {
    if (!this.routes) return [path];
    const fullPath = this.findRoutePath(this.routes, path);
    return fullPath;
  }

  private findRoutePath(
    routes: Routes | NavbarItem[] | undefined,
    targetPath: string,
    parentPath: string[] = [],
  ): string[] | null {
    const currentRoutes = (routes || []) as Routes;
    for (const route of currentRoutes) {
      const currentPath = [...parentPath];

      if (route.path && route.path !== '') {
        currentPath.push(route.path);
      }

      if (route.path === targetPath) {
        return currentPath;
      }

      if (route.children) {
        const found = this.findRoutePath(route.children, targetPath, currentPath);
        if (found) return found;
      }
    }
    return null;
  }

  getLinkClasses(isActive: boolean): { [klass: string]: boolean } {
    return {
      'mf-font-color-secondary-main': !isActive,
      'mf-font-color-primary-main': isActive,
      [this.bottomUnderlineClass]: isActive,
    };
  }

  trackByRoute(_: number, item: Route): string {
    return (item.data as DataRoute)?.label;
  }

  trackByOverflowRoute(_: number, item: Route): string {
    return (item.data as DataRoute)?.label;
  }

  trackByChild(_: number, child: Route): string {
    return (child.data as DataRoute)?.label;
  }
}
