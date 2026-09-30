import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { RouterModule } from '@angular/router';
import { IconComponent } from '../icon/icon.component';
import { AuthenticationService } from '@mf/services/authentication/authentication.service';

@Component({
  selector: 'app-mf-navigation-button',
  standalone: true,
  imports: [CommonModule, RouterModule, IconComponent],
  templateUrl: './navigation-button.component.html',
  styleUrls: ['./navigation-button.component.scss'],
})
export class NavigationButtonComponent {
  @Input() label!: string;
  @Input() iconName: string = '';
  @Input() authenticated = false;
  @Output() action = new EventEmitter();

  iconColorClass: string = 'mf-icon-color-primary-main';

  onClick(): void {
    this.action.emit();
  }

  get hasToken(): boolean {
    return !!this.authService.getToken();
  }

  constructor(private authService: AuthenticationService) {}
}
