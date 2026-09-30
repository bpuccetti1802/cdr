import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { finalize } from 'rxjs/operators';
import { HttpLoadingService } from '../loading/http-loading.service';
import { SHOULD_SKIP_LOADING_HANDLER } from '../injection-tokens/loading-handler';
import { BaseHrefService } from '@mf/services/base-href/base-href.service';
import { TipoIstanzaService } from '@mf/services/tipo-istanza/tipo-istanza.service';

/**
 * Defines the interceptor to update the loading state of http-loading service.
 */
@Injectable({ providedIn: 'root' })
export class HttpLoadingInterceptor implements HttpInterceptor {
  constructor(
    private httpLoadingService: HttpLoadingService,
    private baseHref: BaseHrefService,
    private tipoIstanzeService: TipoIstanzaService,
  ) {}

  /**
   * @inheritDoc
   */
  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const shouldSkip = request.context.get(SHOULD_SKIP_LOADING_HANDLER);

    request = request.clone({
      url: request.url.includes(this.baseHref.baseUrl)
        ? request.url
        : this.baseHref.baseUrl + request.url,
      headers: this.tipoIstanzeService.config
        ? request.headers
            .set('Ambito', this.tipoIstanzeService.config?.ambito || '')
            .set('Applicazione', this.tipoIstanzeService.config?.applicazione || '')
        : request.headers,
    });

    if (shouldSkip) {
      return next.handle(request);
    }
    this.httpLoadingService.setLoading();
    return next.handle(request).pipe(
      finalize(() => {
        this.httpLoadingService.unsetLoading();
      }),
    );
  }
}
