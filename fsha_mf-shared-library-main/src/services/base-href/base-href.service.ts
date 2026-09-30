import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class BaseHrefService {
  get baseUrl(): string {
    const selector = document.querySelector('base')?.getAttribute('href') || '';
    return selector === '/' ? '' : selector;
  }
}
