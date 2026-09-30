import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { NotificationToastComponent } from '../notification-toast/notification-toast.component';
import { NotificationToastEvent } from 'test-library-frankmd93';
import { EventBus } from '@mf/core/event-bus/event-bus';

@Component({
  selector: 'app-rc-notification-container',
  standalone: true,
  imports: [CommonModule, NotificationToastComponent],
  templateUrl: './notification-container.component.html',
  styleUrls: ['./notification-container.component.scss'],
})
export class NotificationContainerComponent implements OnInit {
  notifications: NotificationToastEvent[] = [];

  trackById(index: number): string {
    return index.toString();
  }

  eventCloseEmit(notificationToastEvent: NotificationToastEvent) {
    this.eventBus.dispatchCustomEvent(notificationToastEvent);
    this.notifications = this.notifications.filter(
      (event) => event.eventName === notificationToastEvent.eventName,
    );
  }

  eventBus = EventBus.getInstance();

  ngOnInit(): void {
    this.eventBus.addCustomEventListener(
      'notification-open-event',
      (event: { detail: NotificationToastEvent }) => {
        this.notifications = [...this.notifications, event.detail] as NotificationToastEvent[];
        return Promise.resolve();
      },
    );

    this.eventBus.addCustomEventListener(
      'notification-close-event',
      (event: { detail: NotificationToastEvent }) => {
        this.notifications = this.notifications.filter((n) => n !== event.detail);
        return Promise.resolve();
      },
    );
  }
}
