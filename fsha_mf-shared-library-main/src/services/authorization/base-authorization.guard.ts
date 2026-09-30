import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivateChild, Data, Router, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';

type DataRoute = Data & { authorized?: boolean };

@Injectable({
  providedIn: 'root',
})
export class BaseAuthorizationGuard implements CanActivateChild {
  constructor(private router: Router) {}

  canActivateChild(
    childRoute: ActivatedRouteSnapshot,
  ): boolean | UrlTree | Observable<boolean | UrlTree> | Promise<boolean | UrlTree> {
    // se la rotta non è da autorizzare bypasso il redirect
    if (!(childRoute.data as DataRoute)?.authorized) {
      return true;
    }

    // redirect alla 404
    return this.router.parseUrl('/404');
  }
}
