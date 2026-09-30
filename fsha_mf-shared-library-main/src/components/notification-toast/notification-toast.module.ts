import { NgModule, DoBootstrap, NgModuleRef } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { createCustomElement } from '@angular/elements';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { NotificationToastComponent } from './notification-toast.component';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

let moduleReference: NgModuleRef<NotificationToastModule> | null = null;

@NgModule({
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    CommonModule,
    NotificationToastComponent,
    HttpClientModule,
  ],
})
export class NotificationToastModule implements DoBootstrap {
  constructor() {}

  ngDoBootstrap() {
    console.warn('⚠️ Devi passare elementName a initNotificationToastWebComponent!');
  }
}

export async function initNotificationToastWebComponent(elementName: string) {
  moduleReference = await platformBrowserDynamic().bootstrapModule(NotificationToastModule, {
    ngZone: 'noop',
  });

  const NotificationToastElement = createCustomElement(NotificationToastComponent, {
    injector: moduleReference.injector,
  });

  if (!customElements.get(elementName)) {
    customElements.define(elementName, NotificationToastElement);
    console.debug(`✅ Web Component registrato come <${elementName}>`);
  }

  return moduleReference.injector;
}

export function destroyNotificationToastWebComponent(elementName: string) {
  if (!moduleReference) {
    console.warn(`⚠️ Nessun Web Component attivo da distruggere.`);
    return;
  }

  moduleReference.destroy();
  moduleReference = null;

  const element = document.querySelector(elementName);
  if (element) {
    element.remove();
    console.log(`✅ Web Component <${elementName}> rimosso dal DOM.`);
  }

  console.warn(`⚠️ Non puoi deregistrare customElements. Serve ricaricare la pagina.`);
}
