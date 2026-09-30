import { Component, ChangeDetectionStrategy, Input } from '@angular/core';
import { CardWrapperComponent } from '../card-wrapper/card-wrapper.component';

@Component({
  selector: 'app-under-construction',
  templateUrl: './under-construction.component.html',
  styleUrls: ['./under-construction.component.scss'],
  standalone: true,
  imports: [CardWrapperComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UnderConstructionComponent {
  @Input() title = 'Pagina in costruzione';
  @Input() text = 'Stiamo lavorando a questa funzionalità. Torna presto!';
}
