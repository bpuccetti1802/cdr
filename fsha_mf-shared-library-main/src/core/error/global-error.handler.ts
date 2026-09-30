import { ErrorHandler, inject, Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class GlobalErrorHandler implements ErrorHandler {
  router = inject(Router);

  handleError(error: unknown): void {
    console.error('Errore globale catturato', error);
    if (error instanceof HttpErrorResponse) {
      console.warn('Errore HTTP:', error.message);
      return;
    }
    if (this.router) {
      this.router.navigate(['/error-page']).catch((error_) => {
        console.error('Errore durante la navigazione:', error_);
      });
    } else {
      console.warn('Router non disponibile per la navigazione.');
    }
  }
}
