import { NgModule, DoBootstrap, NgModuleRef } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { createCustomElement } from '@angular/elements';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { DateTimePickerComponent } from './datetime-picker.component';
import { HttpClientModule } from '@angular/common/http';

let moduleReference: NgModuleRef<DateTimePickerModule> | null = null;

@NgModule({
  imports: [BrowserModule, HttpClientModule],
})
export class DateTimePickerModule implements DoBootstrap {
  constructor() {}

  ngDoBootstrap() {
    console.warn('Devi passare elementName a initDateTimePickerWebComponent!');
  }
}

export async function initDateTimePickerWebComponent(elementName: string) {
  if (moduleReference) {
    console.warn(`Web Component <${elementName}> è già attivo.`);
    return;
  }

  moduleReference = await platformBrowserDynamic().bootstrapModule(DateTimePickerModule, {
    ngZone: 'noop',
  });

  const DateTimePickerWebComponentElement = createCustomElement(DateTimePickerComponent, {
    injector: moduleReference.injector,
  });

  if (customElements.get(elementName)) {
    console.error(`L'elemento <${elementName}> è già stato definito!`);
    throw new Error(`L'elemento <${elementName}> è già stato definito!`);
  } else {
    customElements.define(elementName, DateTimePickerWebComponentElement);
    console.log(`Web Component registrato come <${elementName}>`);
  }

  return moduleReference.injector;
}

export function destroyDateTimePickerWebComponent(elementName: string) {
  if (!moduleReference) {
    console.warn(`Nessun Web Component attivo da distruggere.`);
    return;
  }

  moduleReference.destroy();
  moduleReference = null;

  const element = document.querySelector(elementName);
  if (element) {
    element.remove();
    console.log(`Web Component <${elementName}> rimosso dal DOM.`);
  }

  console.warn(`Non puoi rimuovere customElements. Serve un reload.`);
}
