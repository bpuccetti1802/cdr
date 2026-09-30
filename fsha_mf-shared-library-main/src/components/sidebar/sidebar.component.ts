import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { RouterModule } from '@angular/router';
import { RecursiveSidebarComponent } from '../recursive-sidebar/recursive-sidebar.component';
import { ButtonIconComponent } from '../button-icon/button-icon.component';
import { SidebarItem } from 'test-library-frankmd93';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.scss',
  standalone: true,
  imports: [RouterModule, CommonModule, RecursiveSidebarComponent, ButtonIconComponent],
})
export class SidebarComponent {
  @Input() items: SidebarItem[] = [];
  @Input() parentPath: string = '';
  @Input() hasHomeItem = false;
  @Input() toggled: CallableFunction = () => {};
  @Input() isOpen: boolean = false;

  toggleClosed() {
    this.toggled(!this.isOpen);
    this.isOpen = !this.isOpen;
  }
}
