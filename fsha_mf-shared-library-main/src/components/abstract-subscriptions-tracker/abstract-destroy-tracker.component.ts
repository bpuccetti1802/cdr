import { AbstractDestroyTracker } from './abstract-destroy-tracker';
import { OnDestroy, Component } from '@angular/core';

@Component({ template: '', standalone: true })
export class AbstractDestroyTrackerComponent extends AbstractDestroyTracker implements OnDestroy {
  /**
   * @inheritdoc
   */
  ngOnDestroy(): void {
    this.handleDestroy();
  }
}
