import {
  HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
  HttpResponse,
  HttpStatusCode,
} from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { EventBus } from '@mf/core/event-bus/event-bus';
import { SHOULD_SKIP_SUCCESS_HANDLER } from '../injection-tokens/success-handler';
import { ToastTypes, HttpResponse as HttpResponseBody, Ambito } from 'test-library-frankmd93';
import { AuthenticationService } from '@mf/services/authentication/authentication.service';
import { Router } from '@angular/router';
import { SHOULD_SKIP_ERROR_HANDLER } from '../injection-tokens/error-handler';
import { TipoIstanzaService } from '@mf/services/tipo-istanza/tipo-istanza.service';
import { BaseHrefService } from '@mf/services/base-href/base-href.service';

@Injectable({ providedIn: 'root' })
export class HttpErrorInterceptor implements HttpInterceptor {
  private readonly eventBus = EventBus.getInstance();

  private readonly authenticationService = inject(AuthenticationService);

  private readonly router = inject(Router);

  private readonly tipoIstanzaService = inject(TipoIstanzaService);

  private readonly baseHrefService = inject(BaseHrefService);

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    return next.handle(request).pipe(
      tap((event: HttpEvent<unknown>) => {
        if (
          !request.context.get(SHOULD_SKIP_SUCCESS_HANDLER) &&
          event instanceof HttpResponse &&
          event.status >= 200 &&
          event.status < 400
        ) {
          this.eventBus.dispatchCustomEvent({
            eventName: 'notification-open-event',
            payload: {
              openNotification: true,
              toastType: ToastTypes.SUCCESS,
              titleContent: '',
              message: 'Operazione eseguita con successo.',
              useTimer: true,
            },
            reply: false,
          });
        }
      }),
      catchError((error: HttpErrorResponse) => {
        const beError = error.error as HttpResponseBody<unknown>;
        let message = this.getMessage(beError);

        switch (error.status) {
          case HttpStatusCode.ServiceUnavailable: {
            let addedBasePath = '';

            const hrefPath = '/mfManutenzione';

            // Se si è su PreProd
            if (this.baseHrefService?.baseUrl) {
              addedBasePath = this.baseHrefService?.baseUrl;
            }

            globalThis.location.href = addedBasePath + hrefPath;
            break;
          }
          case HttpStatusCode.Unauthorized: {
            message = 'Non autorizzato.';
            this.authenticationService.setData(null);

            if (
              !this.tipoIstanzaService.tipoIstanza &&
              !this.tipoIstanzaService?.config?.environment?.baseUrl
            ) {
              this.router.navigate(['/autenticazione/login']);
            }

            let addedBasePath = '';

            const hrefPath = '/msAuth/api/v1/autenticazione/logout';

            // se PROSA
            if (
              this.tipoIstanzaService?.config?.environment?.baseUrl ||
              this.tipoIstanzaService?.config?.ambito == Ambito.SANZIONATORIO
            ) {
              addedBasePath = this.tipoIstanzaService?.config?.environment?.baseUrl || '';
              globalThis.location.href =
                addedBasePath + '/roma-capitale-operation-service-prosa/api/v1/logoff';
              break;
            }

            // Se si è su PreProd
            if (this.baseHrefService?.baseUrl) {
              addedBasePath = this.baseHrefService?.baseUrl;
            }

            globalThis.location.href = addedBasePath + hrefPath;
            break;
          }
        }
        if (!request.context.get(SHOULD_SKIP_ERROR_HANDLER)) {
          this.eventBus.dispatchCustomEvent({
            eventName: 'notification-open-event',
            payload: {
              openNotification: true,
              toastType: ToastTypes.ERROR,
              titleContent: '',
              message,
              useTimer: true,
            },
            reply: false,
          });
        }
        return throwError(() => error);
      }),
    );
  }
  getMessage(error: HttpResponseBody<unknown>): string {
    return error?.summary?.messages?.join('\n') || 'Si è verificato un errore durante la richiesta';
  }
}
