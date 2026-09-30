import { inject, Injectable } from '@angular/core';
import { BehaviorSubject, map, Observable } from 'rxjs';
import { StruttureEnum } from '../../enums/strutture';
import { HttpResponse, SelectItem } from 'test-library-frankmd93';
import { StruttureListModel } from '../../remote-calls/strutture/models/model';
import { StruttureListRemoteCall } from '../../remote-calls/strutture/strutture-list.remote-call';
import { StrutturaVO } from '../../remote-calls/strutture/models/struttura-vo';
import { HttpClientService } from '@mf/core/http/client/http-client.service';

/**
 * Service for loading and managing back office select lists (offices, sectors, tributes).
 * Provides reactive access to the data through observables.
 */
@Injectable({ providedIn: 'root' })
export class LoadStruttureListService {
  protected httpClientService = inject(HttpClientService);
  private struttureListData: StrutturaVO[] = [];
  private ufficiListData: StrutturaVO[] = [];
  private tributiListData: StrutturaVO[] = [];

  get struttureList(): StrutturaVO[] {
    return this.struttureListData;
  }

  get ufficiList(): StrutturaVO[] {
    return this.ufficiListData;
  }

  get tributiList(): StrutturaVO[] {
    return this.tributiListData;
  }

  private struttureListSubject = new BehaviorSubject<StruttureListModel | undefined>(undefined);

  /**
   * Updates the back office select list data.
   * @param value - The login back office model data or undefined
   */
  setSelectList(value: StruttureListModel | undefined) {
    this.struttureListSubject.next(value);
  }

  /**
   * Observable stream of the back office select list data.
   * @returns Observable that emits the current back office model or undefined
   */
  get selectListObservable$(): Observable<StruttureListModel | undefined> {
    return this.struttureListSubject.asObservable();
  }

  /**
   * Loads the select list from the remote API and updates the internal state.
   */
  loadStruttureList(): void {
    this.httpClientService.execute(new StruttureListRemoteCall()).subscribe({
      next: (response) => {
        const castedResponse = response as HttpResponse<StruttureListModel>;
        this.setSelectList(castedResponse.payload);
      },
    });
  }

  /**
   * Filters the back office select list by type and transforms it into SelectItem format.
   * @param type - The type of select list to filter (office, sector, or tribute)
   * @param parentValue - Optional parent value to filter by (e.g., sector key for offices, office key for tributes)
   * @returns Observable that emits an array of SelectItem objects for the specified type
   */
  filterStruttureListByType(type: StruttureEnum, parentValue?: number): Observable<SelectItem[]> {
    return this.selectListObservable$.pipe(
      map((data) => {
        let items = data?.[type] || [];
        switch (type) {
          case StruttureEnum.Sector: {
            this.struttureListData = items;
            break;
          }
          case StruttureEnum.Office: {
            this.ufficiListData = items;
            break;
          }
          case StruttureEnum.Tribute: {
            this.tributiListData = items;
            break;
          }
        }
        if (parentValue) {
          items = items.filter((item) => item?.idDipendenza === parentValue);
        }

        return items.map((item) => ({
          value: item.key?.toString(),
          label: item.dsVisibilita,
        })) as SelectItem[];
      }),
    );
  }
}
