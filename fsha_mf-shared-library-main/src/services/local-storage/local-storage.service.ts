import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class LocalStorageService {
  private storageSubject = new BehaviorSubject<Record<string, unknown>>({});
  storage$ = this.storageSubject.asObservable();
  constructor() {
    globalThis.addEventListener('storage', (event) => {
      if (event.key && event.newValue) {
        this.storageSubject.next({ [event.key]: JSON.parse(event.newValue) });
      }
    });
  }
  setItem(key: string, value: unknown): void {
    localStorage.setItem(key, JSON.stringify(value));
    this.storageSubject.next({ [key]: value });
    globalThis.dispatchEvent(new StorageEvent('storage', { key, newValue: JSON.stringify(value) }));
  }
  getItem<T>(key: string): T | null {
    return JSON.parse(localStorage.getItem(key) || 'null');
  }
}
