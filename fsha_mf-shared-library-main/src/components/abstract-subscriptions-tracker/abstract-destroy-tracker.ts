import { Subject } from 'rxjs';

export abstract class AbstractDestroyTracker {
  /**
   * Emits when the components is destroyed.
   */
  protected destroyed$: Subject<boolean> = new Subject();

  /**
   * @inheritdoc
   */
  protected handleDestroy(): void {
    this.destroyed$.next(true);
    this.destroyed$.complete();
  }
}
