import { inject, Injectable } from '@angular/core';
import { CanActivate, Router, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';
import { AuthenticationService } from './authentication.service';

@Injectable({
  providedIn: 'root',
})
export class AuthenticationGuard implements CanActivate {
  private readonly authService = inject(AuthenticationService);

  constructor(private router: Router) {}

  canActivate(): boolean | UrlTree | Observable<boolean | UrlTree> | Promise<boolean | UrlTree> {
    const token = this.authService.getToken();

    if (token) {
      return true;
    }

    // Redirect to login (or change route as needed)
    return this.router.createUrlTree(['/autenticazione/login']);
  }
}
