import { NgModule, DoBootstrap, NgModuleRef } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { createCustomElement } from '@angular/elements';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { CardWrapperComponent } from './card-wrapper.component';

let moduleReference: NgModuleRef<CardWrapperModule> | null = null;

@NgModule({
  imports: [BrowserModule, CommonModule, CardWrapperComponent],
})
export class CardWrapperModule implements DoBootstrap {
  constructor() {}

  ngDoBootstrap() {
    console.warn('⚠️ Devi passare elementName a initCardWrapperWebComponent!');
  }
}

export async function initCardWrapperWebComponent(elementName: string) {
  moduleReference = await platformBrowserDynamic().bootstrapModule(CardWrapperModule, {
    ngZone: 'noop',
  });

  const CardWrapperElement = createCustomElement(CardWrapperComponent, {
    injector: moduleReference.injector,
  });

  if (!customElements.get(elementName)) {
    customElements.define(elementName, CardWrapperElement);
    console.debug(`✅ Web Component registrato come <${elementName}>`);
  }

  return moduleReference.injector;
}

export function destroyCardWrapperWebComponent(elementName: string) {
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
