import { Injectable } from '@angular/core';
import {
  RemoteCallInterface,
  RemoteCallCacheEntry,
  AbstractRemoteCallCache,
} from 'test-library-frankmd93';

@Injectable({ providedIn: 'root' })
export class RemoteCallCacheService extends AbstractRemoteCallCache {
  /**
   * The local cache providing for a given request url (with params)
   * the corresponding parsed response.
   */
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  private readonly cache = new Map<string, RemoteCallCacheEntry<any>>();

  /**
   * Determines if for the given request is available a cached response.
   */
  has<TViewModel, TModel>(remoteCall: RemoteCallInterface<TViewModel, TModel>): boolean {
    const key = this.getRequestIdentifier(remoteCall);
    return this.cache.has(key);
  }

  /**
   * Gets the cached entry in the map for the given request.
   */
  get<TViewModel, TModel>(remoteCall: RemoteCallInterface<TViewModel, TModel>): TModel {
    const requestKey = this.getRequestIdentifier(remoteCall);

    const cachedEntry = this.cache.get(requestKey);
    if (!cachedEntry) {
      return null as TModel;
    }

    const isExpired = cachedEntry.lastRead + cachedEntry.maxAge < Date.now();
    return isExpired ? (null as TModel) : cachedEntry.response;
  }

  /**
   * Puts a new cached response for the given request.
   */
  put<TViewModel, TModel>(
    remoteCall: RemoteCallInterface<TViewModel, TModel>,
    response: TModel,
  ): void {
    if (!remoteCall.maxAge) {
      this.flush();
      return;
    }

    const requestKey = this.getRequestIdentifier(remoteCall);
    const entry: RemoteCallCacheEntry<TModel> = {
      response,
      identifier: requestKey,
      lastRead: Date.now(),
      maxAge: remoteCall.maxAge,
    };

    // Update and flush the cache.
    this.cache.set(requestKey, entry as RemoteCallCacheEntry<TModel>);
    this.flush();
  }

  /**
   * Founds all expired entry and deletes them from the cache.
   */
  flush(): void {
    this.cache.forEach((entry) => {
      const isEntryExpired = entry.lastRead + entry.maxAge < Date.now();

      if (isEntryExpired) {
        this.cache.delete(entry.identifier);
      }
    });
  }

  /**
   * Gets the unique key used as idenitifier to store
   * a cached response for the given remote call.
   */
  private getRequestIdentifier<TViewModel, TModel>(
    remoteCall: RemoteCallInterface<TViewModel, TModel>,
  ): string {
    const remoteCallUrl = `${remoteCall.getQuery}${remoteCall.relativePath}`;
    const stringifiedParameters = remoteCall.getQuery().toString();

    return stringifiedParameters ? `${remoteCallUrl}?${stringifiedParameters}` : remoteCallUrl;
  }
}
