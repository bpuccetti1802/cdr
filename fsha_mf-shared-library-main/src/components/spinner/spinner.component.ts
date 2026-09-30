import { Component } from '@angular/core';
import { WideContainerDirective } from '@mf/directives/wide-container/wide-container.directive';

@Component({
  selector: 'app-spinner',
  standalone: true,
  imports: [WideContainerDirective],
  templateUrl: './spinner.component.html',
  styleUrls: ['./spinner.component.scss'],
})
export class SpinnerComponent {}
