import { HttpResponse, HttpMethod } from 'test-library-frankmd93';
import { StruttureListModel } from './models/model';
import { AbstractIstanzHubRemoteCall } from '../abstract-istanzhub.remote-call';

export class StruttureListRemoteCall extends AbstractIstanzHubRemoteCall<
  undefined,
  HttpResponse<StruttureListModel> | undefined
> {
  relativePath = '/login-back-office/';
  method = HttpMethod.get;
}
