import { inject, Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivateChild, Data, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';
import { AuthenticationService } from '../authentication/authentication.service';
import { BaseHrefService } from '../base-href/base-href.service';

type DataRoute = Data & { authenticated?: boolean };

const useTrueIAM = '&useTrueIAM=true';

@Injectable({
  providedIn: 'root',
})
export class AuthenticationIAMGuard implements CanActivateChild {
  private readonly authService = inject(AuthenticationService);

  private readonly baseHrefService = inject(BaseHrefService);

  // manca codice ambito e applicazione
  private iamLocation = '/msAuth/api/v1/autenticazione/loginIAM';

  setIamLocation(iamLocation: string) {
    this.iamLocation = iamLocation;
  }

  canActivateChild(
    childRoute: ActivatedRouteSnapshot,
  ): boolean | UrlTree | Observable<boolean | UrlTree> | Promise<boolean | UrlTree> {
    const token = this.authService.getToken();

    // se la rotta non è da autenticare bypasso il redirect
    if (!(childRoute.data as DataRoute)?.authenticated) {
      return true;
    }

    // se la rotta è da autenticare e ho il token bypasso il redirect
    if ((childRoute.data as DataRoute)?.authenticated && token) {
      return true;
    }

    globalThis.location.href = this.baseHrefService.baseUrl
      ? this.iamLocation + useTrueIAM
      : this.iamLocation;

    return false;
  }
}
