import { Injectable, inject } from '@angular/core';
import {
  ActivatedRouteSnapshot,
  CanActivate,
  CanActivateChild,
  GuardResult,
  MaybeAsync,
  Router,
  RouterStateSnapshot,
  UrlTree,
} from '@angular/router';
import { Observable } from 'rxjs';
import { AuthenticationService } from '../authentication/authentication.service';

@Injectable({
  providedIn: 'root',
})
export class AuthorizationGuard implements CanActivate, CanActivateChild {
  private router = inject(Router);

  private readonly authService = inject(AuthenticationService);

  canActivate(
    route: ActivatedRouteSnapshot,
  ): boolean | UrlTree | Observable<boolean | UrlTree> | Promise<boolean | UrlTree> {
    console.debug('route', route);
    const userAbilitazioni = this.authService?.getData()?.user?.abilitazioni ?? [];
    const requiredAuthorizations: string[] = route?.data['authorizations'] || [];

    const hasAuth = requiredAuthorizations.some((auth) => userAbilitazioni.includes(auth));

    if (hasAuth) {
      return true;
    }
    // Redirect to login (or change route as needed)
    return this.router.createUrlTree(['/']);
  }

  canActivateChild(
    childRoute: ActivatedRouteSnapshot,
    state: RouterStateSnapshot,
  ): MaybeAsync<GuardResult> {
    console.debug('childRoute', childRoute, state);
    if (
      !childRoute?.data['authorizations'] &&
      !(childRoute.children || [])[0]?.data['authorizations']
    ) {
      return true;
    }
    if (childRoute?.data['authorizations']) {
      return this.canActivate(childRoute);
    }
    return this.canActivate(childRoute.children[0]);
  }
}
