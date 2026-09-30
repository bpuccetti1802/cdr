import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IconComponent } from '../icon/icon.component';
import { IconSize } from 'test-library-frankmd93';

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [CommonModule, IconComponent],
  templateUrl: './button.component.html',
  styleUrls: ['./button.component.scss'],
})
export class ButtonComponent {
  @Input() styleType: 'primary' | 'secondary' | 'danger' | 'warning' | 'success' = 'primary';
  @Input() buttonType: 'button' | 'submit' | 'reset' = 'button';
  @Input() disabled = false;
  @Input() label: string = '';
  @Input() iconName: string = '';
  @Input() iconColor: string = 'white';
  @Input() iconSize: IconSize = IconSize.sm;
  @Input() iconPosition: 'left' | 'right' = 'left';
  @Input() classes: string = '';

  @Output() clicked = new EventEmitter<MouseEvent>();

  handleClick(event: MouseEvent): void {
    if (!this.disabled) {
      this.clicked.emit(event);
    }
  }
}
