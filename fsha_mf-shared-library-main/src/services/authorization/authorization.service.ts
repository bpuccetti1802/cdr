import { inject, Injectable } from '@angular/core';
import { AuthenticationService } from '../authentication/authentication.service';

@Injectable({
  providedIn: 'root',
})
export class AuthorizationService {
  private readonly authService = inject(AuthenticationService);

  filterByAuthorization<T>(
    items: T[],
    authorizationsKey: keyof T = 'authorizations' as keyof T,
  ): T[] {
    const authData = this.authService.getData();

    console.debug('authData', authData, items);

    if (!items || !authData?.user?.abilitazioni) {
      return [];
    }

    const userAbilitazioni = authData.user.abilitazioni;

    return items.filter((item) => {
      const auths = item[authorizationsKey];
      if (!Array.isArray(auths)) return false;

      return auths.some((auth) => typeof auth === 'string' && userAbilitazioni.includes(auth));
    });
  }
}
