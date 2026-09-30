import { Injectable } from '@angular/core';
import { Ambito, AppConfig } from 'test-library-frankmd93';

export enum TipoIstanza {
  P = 'P',
  G = 'G',
}

export type Config = {
  ambito?: Ambito;
  applicazione?: string;
  environment?: AppConfig & { baseUrl?: string };
};

@Injectable({ providedIn: 'root' })
export class TipoIstanzaService {
  private _tipoIstanza!: TipoIstanza;
  private _config!: Config;

  get tipoIstanza(): TipoIstanza {
    return this._tipoIstanza;
  }

  setTipoIstanza(newTipoIstanza: TipoIstanza) {
    this._tipoIstanza = newTipoIstanza;
  }

  get config(): Config {
    return this._config;
  }

  setConfig(config: Config) {
    this._config = config;
  }
}
