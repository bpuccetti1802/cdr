import { Component, OnInit } from '@angular/core';
import {
  ActivatedRoute,
  NavigationEnd,
  NavigationStart,
  Route,
  Router,
  RouterOutlet,
  Routes,
} from '@angular/router';
import { CommonModule } from '@angular/common';
import { NavigationButtonComponent } from '../navigation-button/navigation-button.component';
import { BehaviorSubject, filter, tap } from 'rxjs';
import { FormControl } from '@angular/forms';
import { InputComponent } from '../form-elements/input/input.component';
import { AuthenticationService } from '@mf/services/authentication/authentication.service';
import { DataRoute } from 'test-library-frankmd93';

@Component({
  selector: 'app-mf-layout-router-outlet',
  standalone: true,
  imports: [CommonModule, RouterOutlet, NavigationButtonComponent, InputComponent],
  templateUrl: './layout-router-outlet.component.html',
  styleUrl: './layout-router-outlet.component.scss',
})
export class LayoutRouterOutletComponent implements OnInit {
  private currentRouteConfig: Route | null = null;
  private previousRouteConfig: Route | null = null;

  shouldShowSearchInput = false;
  shouldSkipOneElement = false;

  preloadedRoutesSubject = new BehaviorSubject<Route[]>([]);
  filteredRoutes: Route[] = [];
  formControl = new FormControl();

  get hasToken(): boolean {
    return !!this.authService.getToken();
  }

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private authService: AuthenticationService,
  ) {
    // --- intercetta inizio navigazione per salvare la "previous route"
    this.router.events
      .pipe(filter((event): event is NavigationStart => event instanceof NavigationStart))
      .subscribe(() => {
        this.previousRouteConfig = this.getDeepestRoute(this.activatedRoute);
      });

    // --- intercetta fine navigazione per salvare la "current route"
    this.router.events
      .pipe(filter((event): event is NavigationEnd => event instanceof NavigationEnd))
      .subscribe(() => {
        this.currentRouteConfig = this.getDeepestRoute(this.activatedRoute);
      });
  }

  /** Recupera la rotta più profonda attiva (il vero RouteConfig) */
  private getDeepestRoute(activated: ActivatedRoute): Route | null {
    let route = activated;
    while (route.firstChild) {
      route = route.firstChild;
    }
    return route.snapshot.routeConfig || null;
  }

  ngOnInit() {
    // Carica le rotte inizialmente
    this.preloadRoutes();

    // Ricarica le rotte ogni volta che avviene una navigazione
    this.router.events
      .pipe(filter((event) => event instanceof NavigationEnd))
      .subscribe(() => this.preloadRoutes());

    this.formControl.valueChanges
      .pipe(
        tap((value) => {
          const v = (value ?? '').toString().toLowerCase();
          this.filteredRoutes = [...this.preloadedRoutesSubject.getValue()].filter((route) =>
            (route.data as DataRoute)?.label.toLowerCase().includes(v),
          );
        }),
      )
      .subscribe();
  }

  // 🔍 esempio di getter per leggere gerarchie
  private getHierarchy(route: Route | null): number {
    return route?.data?.['hierarchy'] ?? -1;
  }

  private shouldSkipBasedOnHierarchy(): boolean {
    const previousH = this.getHierarchy(this.previousRouteConfig);
    const currentH = this.getHierarchy(this.currentRouteConfig);
    const previousSkip = this.currentRouteConfig?.data?.['shouldSkipOneElement'];

    return currentH > previousH && !!previousSkip;
  }

  get dataCards() {
    return [...this.filteredRoutes]
      .sort((a, b) => {
        const labelA = ((a.data as DataRoute).label || '').toLowerCase();
        const labelB = ((b.data as DataRoute).label || '').toLowerCase();

        if (labelA < labelB) return -1;
        if (labelA > labelB) return 1;
        return 0;
      })
      .map((route) => {
        return {
          action: () => {
            const pathSegments = route.path?.split('/') || [];

            if (!Number.isNaN(pathSegments?.at(-1)) && (route.data as DataRoute).id) {
              pathSegments[pathSegments.length - 1] = encodeURIComponent(
                (route.data as DataRoute).id,
              );
            }

            const hasQueryParameters = this.router.url.includes('?');
            let url = [this.router.url.split('?')[0], ...pathSegments].join('/');
            if (hasQueryParameters) {
              url = [url, '?' + this.router.url.split('?')[1]].join('');
            }

            this.router.navigateByUrl(url);
          },
          label: (route.data as DataRoute).label,
          iconName: (route.data as DataRoute).iconName,
          shouldShowSearchInput: (route.data as DataRoute)?.shouldShowSearchInput,
          shouldSkipOneElement: (route.data as DataRoute)?.shouldSkipOneElement,
          hierarchy: (route.data as DataRoute)?.hierarchy,
          authenticated: (route.data as DataRoute)?.authenticated,
        };
      });
  }

  async preloadRoutes() {
    const routes: Route[] = [];
    this.shouldShowSearchInput = !!this.currentRoute?.data?.['shouldShowSearchInput'];
    this.shouldSkipOneElement = !!this.currentRoute?.data?.['shouldSkipOneElement'];

    // Aggiunge le route presenti in children
    if (this.currentRoute?.children) {
      routes.push(...this.currentRoute.children);
    }

    // Carica dinamicamente le route da loadChildren
    if (this.currentRoute?.loadChildren) {
      const loadedRoutes: Routes = (await this.currentRoute.loadChildren()) as Routes;
      routes.push(...loadedRoutes);
    }

    this.preloadedRoutesSubject.next(routes);
    this.filteredRoutes = routes;
    this.formControl.setValue('');

    const shouldImmediateNavigate =
      this.dataCards.length === 1 && this.shouldSkipOneElement && this.shouldSkipBasedOnHierarchy();

    if (shouldImmediateNavigate) {
      const [dataCard] = this.dataCards;
      dataCard.action();
    }
  }

  private hasChildren(route: Route): boolean {
    return !!(route.children?.length || route.loadChildren);
  }

  get currentRouteHasChildren(): boolean {
    return !!(this.currentRoute && this.hasChildren(this.currentRoute));
  }

  get currentRoute(): Route | null {
    let route = this.activatedRoute;
    while (route.firstChild) {
      route = route.firstChild;
    }
    return route.snapshot.routeConfig || null;
  }

  trackByDataCard(_: number, dataCard: { label: string }): string {
    return dataCard.label;
  }
}
