import { Injectable, OnDestroy } from '@angular/core';
import { Subject, BehaviorSubject, fromEvent } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { MediaBreakpointEnum, mediaBreakpoints } from 'test-library-frankmd93';

@Injectable({
  providedIn: 'root',
})
export class ResponsiveService implements OnDestroy {
  public screenWidth$: BehaviorSubject<number> = new BehaviorSubject(0);
  public mediaBreakpoint$: BehaviorSubject<MediaBreakpointEnum> =
    new BehaviorSubject<MediaBreakpointEnum>(MediaBreakpointEnum.MD);
  private unsubscriber$: Subject<null> = new Subject();

  constructor() {
    this.init();
  }

  init() {
    this.setScreenWidth(window.innerWidth);
    this.setMediaBreakpoint(window.innerWidth);
    fromEvent(globalThis, 'resize')
      .pipe(takeUntil(this.unsubscriber$))
      .subscribe((event: Event) => {
        const target = event.target as Window;
        if (target) {
          this.setScreenWidth(target.innerWidth);

          this.setMediaBreakpoint(target.innerWidth);
        }
      });
  }

  ngOnDestroy() {
    this.unsubscriber$.next(null);
    this.unsubscriber$.complete();
  }

  private setScreenWidth(width: number): void {
    this.screenWidth$.next(width);
  }

  private setMediaBreakpoint(width: number): void {
    for (const [breakpoint, sizes] of Object.entries(mediaBreakpoints)) {
      if (width >= sizes.minSize && width < sizes.maxSize) {
        console.log(width, breakpoint);
        this.mediaBreakpoint$.next(breakpoint as MediaBreakpointEnum);
        return;
      }
    }
  }
}
