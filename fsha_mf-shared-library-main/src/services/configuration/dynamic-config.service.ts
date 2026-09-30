import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, Observable, of, tap } from 'rxjs';
import { AppConfig } from 'test-library-frankmd93';
import { TipoIstanzaService } from '../tipo-istanza/tipo-istanza.service';

@Injectable({
  providedIn: 'root',
})
export class ConfigService {
  private config: AppConfig | null = null;

  private http: HttpClient = inject(HttpClient);

  private tipoIstanzaService = inject(TipoIstanzaService);

  /**
   * Loads the application configuration from the server.
   * If the configuration can't be loaded, it uses the environment.ts as fallback.
   * @returns {Observable<AppConfig>} An observable of the application configuration.
   */
  loadConfig(): Observable<AppConfig> {
    const selector = document.querySelector('base')?.getAttribute('href') || '';
    const selectorParsed =
      selector === '/'
        ? ''
        : selector.at(-1) === '/'
          ? selector.slice(0, Math.max(0, selector.length - 1))
          : selector;
    const assetUrl = selectorParsed + '/config.json';
    return this.http.get<AppConfig>(assetUrl).pipe(
      tap((config) => {
        this.config = config;
        console.debug('load config', this.config);
      }),
      catchError((error) => {
        console.warn('config.json non trovato, caricamento delle variabili da environment.ts...');
        console.error(error);
        this.config = this.tipoIstanzaService?.config?.environment as AppConfig; // Usa environment come fallback
        return of(this.config);
      }),
    );
  }

  /**
   * Gets a property from the application configuration.
   * If the configuration can't be loaded, it returns undefined.
   * @param {keyof AppConfig} key The key of the property to get.
   * @returns {AppConfig[keyof AppConfig] | undefined} The value of the property, or undefined if the property doesn't exist.
   */
  getProperty(key: keyof AppConfig): AppConfig[keyof AppConfig] {
    console.debug('get property config', this.config);
    return this.config ? this.config[key] : undefined;
  }

  /**
   * Gets the application configuration.
   * If the configuration can't be loaded, it returns null.
   * @returns {AppConfig | null} The application configuration, or null if the configuration can't be loaded.
   */
  getConfig(): AppConfig | null {
    console.debug('get config', this.config);
    return this.config;
  }
}
