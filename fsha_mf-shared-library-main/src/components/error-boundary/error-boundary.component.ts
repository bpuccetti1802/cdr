import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-error-boundary',
  templateUrl: './error-boundary.component.html',
  standalone: true,
  imports: [RouterModule],
  styleUrls: ['./error-boundary.component.scss'],
})
export class ErrorBoundaryComponent {}
