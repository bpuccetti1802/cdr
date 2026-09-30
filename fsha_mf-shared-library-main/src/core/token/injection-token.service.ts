import { HttpContextToken } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { SHOULD_SKIP_ERROR_HANDLER } from '../http/injection-tokens/error-handler';
import { SHOULD_SKIP_WARN_HANDLER } from '../http/injection-tokens/warn-handler';
import { SHOULD_SKIP_TOKEN_HANDLER } from '../http/injection-tokens/token-handler';
import { SHOULD_SKIP_SUCCESS_HANDLER } from '../http/injection-tokens/success-handler';
import { SHOULD_SKIP_LOADING_HANDLER } from '../http/injection-tokens/loading-handler';

export enum HttpContextCustomToken {
  SHOULD_SKIP_ERROR_HANDLER = 'SHOULD_SKIP_ERROR_HANDLER',
  SHOULD_SKIP_LOADING_HANDLER = 'SHOULD_SKIP_LOADING_HANDLER',
  SHOULD_SKIP_SUCCESS_HANDLER = 'SHOULD_SKIP_SUCCESS_HANDLER',
  SHOULD_SKIP_TOKEN_HANDLER = 'SHOULD_SKIP_TOKEN_HANDLER',
  SHOULD_SKIP_WARN_HANDLER = 'SHOULD_SKIP_WARN_HANDLER',
}

@Injectable({ providedIn: 'root' })
export class InjectionTokenService {
  getSkipHandler(token: HttpContextCustomToken): HttpContextToken<boolean> {
    switch (token) {
      case HttpContextCustomToken.SHOULD_SKIP_ERROR_HANDLER: {
        return SHOULD_SKIP_ERROR_HANDLER;
      }
      case HttpContextCustomToken.SHOULD_SKIP_LOADING_HANDLER: {
        return SHOULD_SKIP_LOADING_HANDLER;
      }
      case HttpContextCustomToken.SHOULD_SKIP_SUCCESS_HANDLER: {
        return SHOULD_SKIP_SUCCESS_HANDLER;
      }
      case HttpContextCustomToken.SHOULD_SKIP_TOKEN_HANDLER: {
        return SHOULD_SKIP_TOKEN_HANDLER;
      }
      case HttpContextCustomToken.SHOULD_SKIP_WARN_HANDLER: {
        return SHOULD_SKIP_WARN_HANDLER;
      }
    }
  }
}
