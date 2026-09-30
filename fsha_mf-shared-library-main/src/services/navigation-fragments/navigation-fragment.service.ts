import { Injectable } from '@angular/core';
import { Router, UrlTree, UrlSegment } from '@angular/router';

/**
 * Rappresenta i fragment di navigazione estratti da una URL.
 *
 * Questa struttura contiene esclusivamente le informazioni relative
 * alla navigazione interna dell'applicazione, escludendo:
 *
 * - protocollo (http/https)
 * - host
 * - porta
 * - base href
 *
 * Esempio URL completa:
 *
 * http://localhost:4200/app/users/123/profile?mode=edit#details
 *
 * Output:
 *
 * {fullPath: "app/users/123/profile",
 *   segments: ["app", "users", "123", "profile"],
 *   queryParams: {mode: "edit"},
 *   fragment: "details"}
 */
export interface NavigationFragments {
  /**
   * Path completo relativo dell'applicazione, senza host e baseUrl.
   *
   * Esempio:
   * app/users/123/profile
   */
  fullPath: string;

  /**
   * Segmenti individuali del path.
   *
   * I segments sono le parti della URL separate dal carattere '/'.
   * Ogni segmento rappresenta un livello della navigazione Angular.
   *
   * Esempio URL:
   * /app/users/123/profile
   *
   * Segments:
   * ["app", "users", "123", "profile"]
   */
  segments: string[];

  /**
   * Parametri di query presenti nella URL.
   *
   * Sono i parametri opzionali che seguono il simbolo '?'.
   *
   * Esempio:
   * ?mode=edit&active=true
   *
   * Output:
   * {mode: "edit",
   *   active: "true"}
   */
  queryParams: { [key: string]: unknown };

  /**
   * Fragment della URL.
   *
   * Il fragment è la parte della URL successiva al simbolo '#'
   * e rappresenta tipicamente un'ancora interna alla pagina.
   *
   * Esempio URL:
   * /app/users#details
   *
   * Fragment:
   * "details"
   *
   * Se non presente, il valore sarà null.
   */
  fragment: string | null;
}

/**
 * Service responsabile dell'estrazione e gestione dei fragment di navigazione Angular.
 *
 * Questo service consente di ottenere informazioni sulla navigazione corrente
 * senza includere host, protocollo o base href.
 *
 * Utilizza il Router Angular per analizzare la URL corrente o una URL specifica
 * e restituire i seguenti elementi:
 *
 * - path relativo
 * - segments
 * - query parameters
 * - fragment
 *
 * Questo service è utile per:
 *
 * - logging della navigazione
 * - breadcrumb dinamici
 * - controlli di autorizzazione
 * - salvataggio dello stato di navigazione
 * - redirect condizionati
 *
 * Il service è fornito a livello root, quindi disponibile globalmente.
 */
@Injectable({
  providedIn: 'root',
})
export class NavigationFragmentService {
  constructor(private router: Router) {}

  /**
   * Restituisce i fragment della navigazione corrente.
   *
   * Analizza la URL corrente del Router Angular e restituisce
   * una struttura contenente segments, queryParams e fragment.
   *
   * Non include:
   *
   * - protocollo
   * - host
   * - porta
   * - base href
   *
   * Esempio:
   *
   * URL corrente:
   * http://localhost:4200/app/dashboard/detail/42?mode=edit#info
   *
   * Output:
   * {
   *   fullPath: "app/dashboard/detail/42",
   *   segments: ["app", "dashboard", "detail", "42"],
   *   queryParams: { mode: "edit" },
   *   fragment: "info"
   * }
   *
   * @returns NavigationFragments struttura contenente le informazioni di navigazione
   */
  getCurrentFragments(): NavigationFragments {
    const currentUrl: string = this.router.url;

    return this.extractFragments(currentUrl);
  }

  /**
   * Restituisce i fragment a partire da una URL specifica.
   *
   * Questo metodo è utile quando si deve analizzare una URL diversa
   * da quella corrente.
   *
   * Esempio input:
   * /app/users/123/profile?mode=edit#details
   *
   * Output:
   * {
   *   fullPath: "app/users/123/profile",
   *   segments: ["app", "users", "123", "profile"],
   *   queryParams: { mode: "edit" },
   *   fragment: "details"
   * }
   *
   * @param url URL relativa Angular
   *
   * @returns NavigationFragments struttura contenente i fragment estratti
   */
  getFragmentsFromUrl(url: string): NavigationFragments {
    return this.extractFragments(url);
  }

  /**
   * Restituisce esclusivamente il path relativo corrente.
   *
   * Esempio:
   *
   * URL:
   * http://localhost:4200/app/users/123/profile
   *
   * Output:
   * app/users/123/profile
   *
   * @returns string path relativo
   */
  getRelativePath(): string {
    return this.getCurrentFragments().fullPath;
  }

  /**
   * Metodo interno responsabile dell'estrazione dei fragment da una URL.
   *
   * Utilizza UrlTree del Router Angular per analizzare la struttura della URL.
   *
   * Processo:
   *
   * 1. Parsing della URL tramite Router.parseUrl()
   * 2. Estrazione del nodo primary
   * 3. Estrazione dei segments
   * 4. Estrazione dei query params
   * 5. Estrazione del fragment
   *
   * @param url URL da analizzare
   *
   * @returns NavigationFragments struttura risultante
   */
  private extractFragments(url: string): NavigationFragments {
    const urlTree: UrlTree = this.router.parseUrl(url);

    const primaryChild = urlTree.root.children['primary'];

    const segments: string[] = primaryChild
      ? primaryChild.segments.map((segment: UrlSegment) => segment.path)
      : [];

    return {
      fullPath: segments.join('/'),
      segments: segments,
      queryParams: urlTree.queryParams,
      fragment: urlTree.fragment,
    };
  }
}
