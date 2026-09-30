import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-badge',
  templateUrl: './badge.component.html',
  standalone: true,
  imports: [CommonModule],
})
export class BadgeComponent {
  @Input() color?: string = 'primary';
  @Input() text!: string;
}
