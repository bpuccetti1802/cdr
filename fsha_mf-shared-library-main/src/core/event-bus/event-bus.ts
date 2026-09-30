import { Singleton } from '@mf/core/utils/singleton';
import { BaseCustomEvent } from 'test-library-frankmd93';

type ListenerReference = {
  original: <T, R>(event: CustomEvent<BaseCustomEvent<T>>) => Promise<R> | Promise<void>;
  wrapped: EventListener;
};

export class EventBus extends Singleton {
  private readonly bus = new EventTarget();
  private listenersMap = new Map<string, ListenerReference[]>();
  private replyMap = new Map<string, boolean>();

  public addCustomEventListener<T, R>(
    eventName: string,
    handler: (event: CustomEvent<BaseCustomEvent<T>>) => Promise<R> | Promise<void>,
  ): void {
    const wrappedHandler: EventListener = async (event: Event) => {
      const customEvent = event as CustomEvent<BaseCustomEvent<T>>;
      const result = await handler(customEvent);

      if (customEvent.detail.reply) {
        this.bus.dispatchEvent(
          new CustomEvent<R>(`reply:${eventName}`, {
            detail: result as R,
          }),
        );
      }
    };

    const listeners = this.listenersMap.get(eventName) ?? [];
    listeners.push({
      original: handler as <T, R>(
        event: CustomEvent<BaseCustomEvent<T>>,
      ) => Promise<R> | Promise<void>,
      wrapped: wrappedHandler,
    });

    this.listenersMap.set(eventName, listeners);
    this.bus.addEventListener(eventName, wrappedHandler);
  }

  public removeCustomEventListener(eventName: string): void {
    const listeners = this.listenersMap.get(eventName);
    if (listeners) {
      for (const reference of listeners) {
        this.bus.removeEventListener(eventName, reference.wrapped);
      }
      this.listenersMap.delete(eventName);
    }
  }

  public dispatchCustomEvent<T, R>(event: BaseCustomEvent<T>): Promise<void | R> {
    const eventName = event.eventName;

    // Caso 1: broadcast, nessuna risposta attesa
    if (!event.reply) {
      const customEvent = new CustomEvent<BaseCustomEvent<T>>(eventName, {
        detail: {
          ...event,
          payload: {
            useTimer: true,
            ...event.payload,
          },
        },
      });
      this.bus.dispatchEvent(customEvent);
      return Promise.resolve();
    }

    // Caso 2: richiesta con attesa risposta
    if (this.replyMap.has(eventName)) {
      return Promise.reject(
        new Error(
          `Un evento con reply:true è già in attesa per "${eventName}", si può processare un evento reply:true alla volta.`,
        ),
      );
    }

    this.replyMap.set(eventName, true);

    return new Promise<R>((resolve) => {
      const replyHandler = (replyEvent: CustomEvent<R>) => {
        this.replyMap.delete(eventName);
        resolve(replyEvent.detail);
      };

      this.bus.addEventListener(`reply:${eventName}`, replyHandler as EventListener, {
        once: true,
      });

      const eventWithReply = new CustomEvent<BaseCustomEvent<T>>(eventName, {
        detail: {
          ...event,
          payload: {
            useTimer: true,
            ...event.payload,
          },
        },
      });

      this.bus.dispatchEvent(eventWithReply);
    });
  }
}
