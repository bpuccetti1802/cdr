import { ChangeDetectorRef, Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { CommonModule } from '@angular/common';
import { IconComponent } from '../icon/icon.component';
import { trigger, transition, style, animate } from '@angular/animations';
import { NotificationToastEvent, ToastTypes } from 'test-library-frankmd93';

@Component({
  selector: 'app-rc-notification-toast',
  standalone: true,
  imports: [CommonModule, FontAwesomeModule, IconComponent],
  templateUrl: './notification-toast.component.html',
  styleUrls: ['./notification-toast.component.scss'],
  animations: [
    trigger('toastAnimation', [
      transition(':enter', [
        style({ transform: 'translateX(100%)', opacity: 0 }),
        animate('300ms ease-out', style({ transform: 'translateX(0)', opacity: 1 })),
      ]),
      transition(':leave', [
        animate('300ms ease-in', style({ transform: 'translateX(100%)', opacity: 0 })),
      ]),
    ]),
  ],
})
export class NotificationToastComponent implements OnInit {
  progress: number = 100;
  private startProgress: number = 100;
  private intervalId: ReturnType<typeof setInterval> | null = null;
  private pause: boolean = false;
  private step: number = 100;
  private startRemainingTime: number = 5000;
  private remainingTime: number = 5000;
  private isBlocked: boolean = false;

  ToastTypes = ToastTypes;

  get icon() {
    switch (this.toastType) {
      case ToastTypes.ERROR: {
        return 'it-close-circle';
      }
      case ToastTypes.INFO: {
        return 'it-info-circle';
      }
      case ToastTypes.WARNING: {
        return 'it-error';
      }
      case ToastTypes.SUCCESS: {
        return 'it-check-circle';
      }
      default: {
        return '';
      }
    }
  }

  @Input() disableEnterAnimation: boolean = true;
  @Input() useTimer = true;
  @Input() id = 'notification-toast-id';
  @Input() openNotification: boolean = false;
  @Input() toastType: ToastTypes = ToastTypes.SUCCESS;
  @Input() titleContent: string = 'Aggiungi';
  @Input() message: string = 'Aggiungi';
  @Input() fullWidth = false;
  @Output() eventCloseCb = new EventEmitter<NotificationToastEvent>();
  @Input() callbackClose?: () => void;

  constructor(private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    if (this.openNotification && this.useTimer) {
      this.startTimer();
    }
  }

  startTimer(): void {
    this.stopTimer();
    this.pause = false;

    this.intervalId = setInterval(() => {
      if (!this.pause && !this.isBlocked) {
        this.remainingTime -= this.step;
        this.progress = (this.remainingTime / this.startRemainingTime) * this.startProgress;
        this.cdr.detectChanges();
        if (this.remainingTime <= 0) {
          this.closeNotification();
        }
      }
    }, this.step);
  }

  stopTimer(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }

  get iconColorClass(): string {
    switch (this.toastType) {
      case ToastTypes.ERROR: {
        return 'mf-font-color-error-dark';
      }
      case ToastTypes.INFO: {
        return 'mf-font-color-info-dark';
      }
      case ToastTypes.WARNING: {
        return 'mf-font-color-warning-dark';
      }
      case ToastTypes.SUCCESS: {
        return 'mf-font-color-success-dark';
      }
      default: {
        return '';
      }
    }
  }

  togglePause(): void {
    if (!this.useTimer) {
      return;
    }
    this.isBlocked = true;
    this.pause = true;
    this.stopTimer();
  }

  toggleRestart(): void {
    if (!this.useTimer) {
      return;
    }
    this.isBlocked = false;
    this.pause = false;
    this.startTimer();
  }

  closeNotification(): void {
    this.stopTimer();

    this.openNotification = false;
    this.cdr.detectChanges();
    this.eventCloseCb.emit(this.notificationToastEvent);
    if (this.callbackClose) {
      this.callbackClose();
    }
  }

  get notificationToastEvent(): NotificationToastEvent {
    return {
      payload: {
        id: this.id,
        openNotification: this.openNotification,
        toastType: this.toastType,
        titleContent: this.titleContent,
        message: this.message,
        useTimer: this.useTimer,
      },
      eventName: 'notification-close-event',
      reply: false,
    };
  }
}
