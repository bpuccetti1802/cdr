import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { IconComponent } from '../icon/icon.component';
import { Attributes, Colors } from 'test-library-frankmd93';
import { BaseHrefService } from '@mf/services/base-href/base-href.service';

@Component({
  selector: 'app-rc-button-icon',
  standalone: true,
  imports: [CommonModule, IconComponent],
  templateUrl: './button-icon.component.html',
  styleUrl: './button-icon.component.scss',
})
export class ButtonIconComponent {
  @Input() name!: string;
  @Input() color: string | Colors = Colors.secondary;
  @Input() useClass = false;
  @Input() disabled = false;
  @Input() loading = false;
  @Input() class = 'icon';
  @Input() attr?: Attributes;
  @Input() baseUrl = '/mfSharedLibrary';
  @Output() clickEvent = new EventEmitter<void>();

  constructor(private baseHref: BaseHrefService) {
    // Metto gli asset e url base icone con baseHref calcolato automaticamente
    this.baseUrl = this.baseHref.baseUrl + this.baseUrl;
  }

  onClick(): void {
    this.clickEvent.emit();
  }
}
