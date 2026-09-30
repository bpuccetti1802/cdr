import { inject, Injectable } from '@angular/core';
import { LocalStorageService } from '../local-storage/local-storage.service';
import { AuthData } from 'test-library-frankmd93';
import { BehaviorSubject, Observable } from 'rxjs';

interface AuthDataExtended extends AuthData {
  struttura?: {
    key: number;
    nmStruttura: string;
    dsStruttura: string;
  };
  tributo?: {
    key: number;
    nmStruttura: string;
    dsStruttura: string;
  };
  ufficio?: {
    key: number;
    nmStruttura: string;
    dsStruttura: string;
  };
}

@Injectable({ providedIn: 'root' })
export class AuthenticationService {
  private localStorageService = inject(LocalStorageService);
  private storageKey = 'auth';

  private authDataSubject = new BehaviorSubject<AuthDataExtended | null>(
    this.localStorageService.getItem<AuthDataExtended>(this.storageKey),
  );

  get struttura() {
    return this.authDataSubject.getValue()?.struttura;
  }

  get ufficio() {
    return this.authDataSubject.getValue()?.ufficio;
  }

  get tributo() {
    return this.authDataSubject.getValue()?.tributo;
  }

  /**
   * Salva i dati di autenticazione estesi nello storage locale.
   * @param {AuthDataExtended | null} value Oggetto `AuthDataExtended` o `null` per rimuovere i dati.
   */
  setData(value: AuthDataExtended | null): void {
    this.localStorageService.setItem(this.storageKey, value);
    this.authDataSubject.next(value);
  }

  /**
   * Salva l'ufficio di autenticazione nello storage.
   * @param {AuthDataExtended['ufficio'] | null} value Oggetto `AuthDataExtended` o `null` per rimuovere i dati.
   */
  setUfficio(value?: AuthDataExtended['ufficio']): void {
    const newData = this.localStorageService.getItem<AuthDataExtended>(this.storageKey);
    if (!newData) {
      return;
    }
    newData.ufficio = value;
    this.localStorageService.setItem(this.storageKey, newData);
    this.authDataSubject.next(newData);
  }

  /**
   * Salva il tributo di autenticazione nello storage.
   * @param {AuthDataExtended['tributo'] | null} value Oggetto `AuthDataExtended` o `null` per rimuovere i dati.
   */
  setTributo(value?: AuthDataExtended['tributo']): void {
    const newData = this.localStorageService.getItem<AuthDataExtended>(this.storageKey);
    if (!newData) {
      return;
    }
    newData.tributo = value;
    this.localStorageService.setItem(this.storageKey, newData);
    this.authDataSubject.next(newData);
  }

  /**
   * Salva la struttura di autenticazione nello storage locale.
   * @param {AuthDataExtended['struttura'] | null} value Oggetto `AuthDataExtended['struttura']` o `null` per rimuovere i dati.
   */
  setStruttura(value?: AuthDataExtended['struttura']): void {
    const newData = this.localStorageService.getItem<AuthDataExtended>(this.storageKey);
    if (!newData) {
      return;
    }
    newData.struttura = value;
    this.localStorageService.setItem(this.storageKey, newData);
    this.authDataSubject.next(newData);
  }

  /**
   * Restituisce il token di autenticazione, se disponibile.
   * @returns {string | null | undefined} Il token di autenticazione, se disponibile, altrimenti null o undefined.
   */
  getToken(): string | null | undefined {
    return this.localStorageService.getItem<AuthDataExtended>(this.storageKey)?.token || null;
  }

  /**
   * Restituisce i dati di autenticazione salvati nello storage locale.
   * @returns {AuthDataExtended | null} I dati di autenticazione salvati nello storage locale, se disponibili, altrimenti null.
   */
  getData(): AuthDataExtended | null {
    return this.localStorageService.getItem<AuthDataExtended>(this.storageKey);
  }

  /**
   * Ritorna un osservabile che emette i dati di autenticazione ogni volta che vengono modificati.
   * @returns {Observable<AuthDataExtended | null>} Un osservabile che emette i dati di autenticazione salvati nello storage locale, se disponibili, altrimenti null.
   */
  subscribeToAuthChanges(): Observable<AuthDataExtended | null> {
    return this.authDataSubject.asObservable();
  }
}
