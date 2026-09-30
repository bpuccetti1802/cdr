import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RecursiveSidebarComponent } from '../recursive-sidebar/recursive-sidebar.component';
import { IconComponent } from '../icon/icon.component';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { filter } from 'rxjs';

export interface MenuItem {
  shouldNotShowItem: boolean;
  label: string;
  path: string;
  children: MenuItem[];
}

@Component({
  selector: 'app-rc-menu',
  standalone: true,
  imports: [CommonModule, RecursiveSidebarComponent, IconComponent],
  templateUrl: './menu.component.html',
  styleUrl: './menu.component.scss',
})
export class MenuComponent {
  @Input() items: MenuItem[] = [];
  @Input() parentPath: string = '';
  @Input() level = 1;
  label = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
  ) {
    this.assignRouteLabel();
    this.router.events.pipe(filter((event) => event instanceof NavigationEnd)).subscribe(() => {
      this.assignRouteLabel();
    });
  }

  assignRouteLabel() {
    let currentRoute = this.route.root;
    while (currentRoute.firstChild) {
      currentRoute = currentRoute.firstChild;
    }
    this.label = currentRoute.snapshot.data['label'] || '';
  }
}
