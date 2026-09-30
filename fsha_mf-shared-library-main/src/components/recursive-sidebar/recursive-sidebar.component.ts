import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { PipesModule } from '@mf/pipe/pipes.module';
import { IconComponent } from '../icon/icon.component';
import { SidebarItem } from 'test-library-frankmd93';

@Component({
  selector: 'app-recursive-sidebar',
  templateUrl: './recursive-sidebar.component.html',
  standalone: true,
  imports: [RouterModule, CommonModule, PipesModule, IconComponent],
})
export class RecursiveSidebarComponent {
  @Input() items: SidebarItem[] = [];
  @Input() parentPath: string = '';
  @Input() level = 1;
  @Input() hasHomeItem = false;

  currentRoute = '';
  trackBy(_: number, items: { path: string }): string {
    return items.path;
  }

  constructor(public router: Router) {
    this.currentRoute = this.router.url;
  }
}
