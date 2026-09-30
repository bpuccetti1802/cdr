import { AbstractRemoteCall } from 'test-library-frankmd93';

export abstract class AbstractIstanzHubRemoteCall<
  TViewModel = undefined,
  TModel = undefined,
> extends AbstractRemoteCall<TViewModel, TModel> {
  baseUrl: string = '/msIstanzHub/api/v1';
}
