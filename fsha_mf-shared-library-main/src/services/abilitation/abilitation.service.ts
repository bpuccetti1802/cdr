import { inject, Injectable } from '@angular/core';
import { AuthenticationService } from '../authentication/authentication.service';

@Injectable({
  providedIn: 'root',
})
export class AbilityService {
  private readonly authService = inject(AuthenticationService);

  has(ability: string): boolean {
    return this.authService.getData()?.user?.abilitazioni?.includes(ability) || false;
  }

  hasSome(abilities: string[]): boolean {
    return abilities.some((ab) => this.has(ab));
  }

  hasAll(abilities: string[]): boolean {
    return abilities.every((ab) => this.has(ab));
  }
}
