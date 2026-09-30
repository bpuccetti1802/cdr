import { Component, Input } from '@angular/core';
import { ActivatedRoute, NavigationEnd, Router, RouterModule } from '@angular/router';
import { filter } from 'rxjs/operators';
import { CommonModule } from '@angular/common';
import { RemoteApplicationType, DataRoute } from 'test-library-frankmd93';

interface Breadcrumb {
  label: string;
  url: string;
}

@Component({
  standalone: true,
  imports: [RouterModule, CommonModule],
  selector: 'app-mf-breadcrumb',
  templateUrl: './breadcrumb.component.html',
  styleUrl: './breadcrumb.component.scss',
})
export class BreadcrumbComponent {
  @Input() id: string = '';
  @Input() applicationType: RemoteApplicationType = RemoteApplicationType.ANGULAR;
  @Input() breadcrumbs: Breadcrumb[] = [];
  minimumShouldEllipsis = 3;
  startExpandedFromIndex = 4;

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
  ) {
    this.breadcrumbs = this.createBreadcrumbs(this.activatedRoute.root);
    this.router.events.pipe(filter((event) => event instanceof NavigationEnd)).subscribe(() => {
      this.breadcrumbs = this.createBreadcrumbs(this.activatedRoute.root);
      this.expandedFromIndex = Infinity;
    });
  }

  navigateTo(url: string, $event: Event) {
    $event.preventDefault();
    if (this.applicationType === RemoteApplicationType.REACT) {
      let navigationUrl = url;

      navigationUrl = url === '/pec-mailer' ? '/' : url;

      if (url === '/') {
        globalThis.location.href = '/';
        return;
      }

      const navigateToEvent = new CustomEvent('navigateTo', {
        detail: { url: navigationUrl },
      });
      document.dispatchEvent(navigateToEvent);
    } else {
      this.router.navigate([url]);
    }
  }

  private createBreadcrumbs(
    route: ActivatedRoute,
    url: string = '',
    breadcrumbs: Breadcrumb[] = [],
  ): Breadcrumb[] {
    const children = route.children;

    if (children.length === 0) {
      return breadcrumbs;
    }

    for (const child of children) {
      const routeConfig = child.routeConfig;
      let newUrl = url === '/' ? `/${routeConfig?.path}` : `${url}/${routeConfig?.path}`;
      newUrl = newUrl.replaceAll(/\/{2,}/g, '/');

      if ((routeConfig?.data as DataRoute)?.label) {
        breadcrumbs.push({
          label: (routeConfig?.data as DataRoute)?.label,
          url: newUrl,
        });
      }
      return this.createBreadcrumbs(child, newUrl, breadcrumbs);
    }

    return breadcrumbs;
  }
  trackByCrumb(_: number, crumb: { url: string }): string {
    return crumb.url;
  }

  expandedFromIndex = this.startExpandedFromIndex; // All collapsed by default

  shouldCollapse(index: number): boolean {
    // Show always first, last back to startExpandedFromIndex
    if (index === 0 || index > this.breadcrumbs.length - this.startExpandedFromIndex - 1)
      return false;
    return index < this.expandedFromIndex;
  }

  isExpandable(index: number): boolean {
    return this.shouldCollapse(index);
  }

  onExpand(index: number): void {
    this.expandedFromIndex = index;
  }
}
