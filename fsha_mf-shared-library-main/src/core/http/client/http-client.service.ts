import { concatMap, retryWhen, delay, observeOn, map } from 'rxjs/operators';
import { of, throwError, Observable, asyncScheduler } from 'rxjs';
import {
  HttpClient,
  HttpEventType,
  HttpRequest,
  HttpResponse,
  HttpStatusCode,
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AbstractRemoteCall, RemoteCallInterface } from 'test-library-frankmd93';
import { ObjectExtensionsService } from '@mf/core/utils/object-extensions/object-extensions.service';
import { RemoteCallCacheService } from '../cache/remote-call-cache.service';
import { HttpData } from 'test-library-frankmd93';

/**
 * @deprecated to pass in the test-library
 */
type HttpDataWithReportProgress<TViewModel, TModel> = HttpData<TViewModel, TModel> & {
  call: RemoteCallInterface<TViewModel, TModel> & { reportProgress?: boolean };
};

/**
 * @deprecated pass it to test-library
 */
abstract class RemoteCallWithReportProgress<T, R> extends AbstractRemoteCall<T, R> {
  reportProgress?: boolean;
}

@Injectable({ providedIn: 'root' })
export class HttpClientService {
  private constructor(
    readonly httpClient: HttpClient,
    readonly objectExtensionsService: ObjectExtensionsService,
    readonly remoteCallCache?: RemoteCallCacheService,
  ) {}

  /**
   * Executes the remote call.
   */
  execute<TViewModel, TModel>(
    remoteCall: RemoteCallWithReportProgress<TViewModel, TModel>,
  ): Observable<TViewModel | TModel | HttpResponse<TModel> | null> {
    // Check if a response is already available in the cache and just returns it
    // if found.
    const cachedResponseEntry = this.remoteCallCache?.get<TViewModel, TModel>(remoteCall);
    if (cachedResponseEntry) {
      // NOTE: We get a response from the cache, in order to make
      // Angular change detection working fine we provide the cached
      // response asynchrounsly avoiding changing the value while
      // the detection is running!
      return of(cachedResponseEntry).pipe(observeOn(asyncScheduler)) as Observable<
        TViewModel | TModel
      >;
    }

    return (
      of(remoteCall)
        // Create an http request from the remote call.
        .pipe(
          map((call: RemoteCallWithReportProgress<TViewModel, TModel>) => {
            const httpRequest = new HttpRequest(
              call.method,
              `${call.baseUrl}${call.relativePath}`,
              call.getBody(),
              {
                withCredentials: call.withCredentials,
                responseType: call.responseType,
                params: call.getQuery(),
                headers: call.getHeaders(),
                reportProgress: call.reportProgress || false,
                context: call.getContext(),
              },
            );

            return { httpRequest, call } as HttpData<TViewModel, TModel>;
          }),
          // Performs the http request and propagate the remote call.
          concatMap(({ httpRequest, call }: HttpDataWithReportProgress<TViewModel, TModel>) => {
            let request$ = this.httpClient.request(httpRequest.method, httpRequest.url, {
              body: httpRequest.body,
              headers: httpRequest.headers,
              reportProgress: httpRequest.reportProgress,
              observe: call.reportProgress ? 'events' : 'response',
              params: httpRequest.params,
              responseType: httpRequest.responseType,
              withCredentials: httpRequest.withCredentials,
              context: httpRequest.context,
            });

            // Check if we need to setup a request retry.
            const shouldSetupRequestRetry =
              Number.isFinite(call.retryAttemptCount) && call.retryAttemptCount > 0;
            if (shouldSetupRequestRetry) {
              request$ = request$.pipe(
                retryWhen((notifiers: Observable<HttpResponse<TModel>>) =>
                  notifiers.pipe(
                    concatMap((response: HttpResponse<TModel>, index: number) => {
                      // If the all the attempts has been tried or the request is not failed with status code zero forward the error...
                      if (!response || response.status !== 0 || index > call.retryAttemptCount) {
                        return throwError(response);
                      }
                      // ...otherwise execute the next attempt after a specified amount of time.
                      return of(response).pipe(delay(call.retryDelay));
                    }),
                  ),
                ),
              );
            }

            // Finally propagate the remote call along with the request stream.
            return request$.pipe(
              map((httpResponse: HttpResponse<TModel>) => ({
                httpResponse,
                call,
              })),
            );
          }),
          // Finally let's perform the mapping to get the response slice that's actually needed.
          map(({ httpResponse, call }) => {
            console.log(httpResponse);
            /**
             * Da rifattorizzare
             * al momento se progress ti dà la response solo se è ok
             */
            if (call.reportProgress) {
              if (
                (httpResponse.type as HttpEventType) === HttpEventType.ResponseHeader &&
                httpResponse.status !== HttpStatusCode.Ok
              ) {
                return null;
              }
              return httpResponse;
            }

            const model = call.contentProperty
              ? this.objectExtensionsService.getObjectValue<TModel>(
                  httpResponse,
                  call.contentProperty,
                )
              : (httpResponse as HttpResponse<TModel>);

            // Update the remote calls cache.
            if (this.remoteCallCache) {
              this.remoteCallCache.put<TViewModel, TModel>(call, model as TModel);
            }

            return (
              remoteCall.trasformer?.toViewModel(model as TModel) || (model as HttpResponse<TModel>)
            );
          }),
        )
    );
  }
}
