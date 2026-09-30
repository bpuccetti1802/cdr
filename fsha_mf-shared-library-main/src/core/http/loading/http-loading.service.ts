import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { distinctUntilChanged, map, shareReplay } from 'rxjs/operators';

/**
 * Keep track of the consumers that want to move the application in a
 * loading state.
 */
@Injectable({
  providedIn: 'root',
})
export class HttpLoadingService {
  /**
   * An internal counter maintaining the number of consumers that want
   * to move the app in a loading state.
   */
  private callers: BehaviorSubject<number> = new BehaviorSubject(0);

  /**
   * The loading stream.
   */
  get loading$(): Observable<boolean> {
    return this.callers.asObservable().pipe(
      map((callers: number) => callers > 0),
      distinctUntilChanged(),
      shareReplay(1),
    );
  }

  /**
   * Set the loading state.
   */
  setLoading(): void {
    const callers = this.callers.getValue();
    this.callers.next(callers + 1);
  }

  /**
   * Unset the loading state.
   */
  unsetLoading(): void {
    const callers = this.callers.getValue();

    if (callers === 0) {
      return;
    }

    this.callers.next(callers - 1);
  }
}
