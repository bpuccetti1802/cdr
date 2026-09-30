import { Component, EventEmitter, Input, Output } from '@angular/core';
import { IconComponent } from '../icon/icon.component';
import { IconSize } from 'test-library-frankmd93';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-toggle-icon',
  templateUrl: './toggle-icon.component.html',
  styleUrls: ['./toggle-icon.component.scss'],
  imports: [IconComponent, CommonModule],
  standalone: true,
})
export class ToggleIconComponent {
  @Input() active = false;
  @Input() name!: string;
  @Output() toggled = new EventEmitter<boolean>();
  @Input() counter = 1;

  toggle() {
    this.toggled.emit(this.active);
    this.active = !this.active;
  }
  smSize = IconSize.sm;
  mdSize = IconSize.md;
}
