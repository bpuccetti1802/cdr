import { NgModule, DoBootstrap, NgModuleRef } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { createCustomElement } from '@angular/elements';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { SelectComponent } from './select.component';
import { HttpClientModule } from '@angular/common/http';

let moduleReference: NgModuleRef<SelectModule> | null = null;

@NgModule({
  imports: [BrowserModule, HttpClientModule],
})
export class SelectModule implements DoBootstrap {
  constructor() {}
  ngDoBootstrap() {
    console.warn('⚠️ Devi passare elementName a initSelectWebComponent!');
  }
}

export async function initSelectWebComponent(elementName: string) {
  moduleReference = await platformBrowserDynamic().bootstrapModule(SelectModule, {
    ngZone: 'noop',
  });

  const SelectWebComponentElement = createCustomElement(SelectComponent, {
    injector: moduleReference.injector,
  });

  if (customElements.get(elementName)) {
    console.error(`⚠️ L'elemento <${elementName}> è già stato definito!`);
    // throw new Error(`L'elemento <${elementName}> è già stato definito!`);
  } else {
    customElements.define(elementName, SelectWebComponentElement);
    console.log(`✅ Web Component registrato come <${elementName}>`);
  }

  return moduleReference.injector;
}

export function destroySelectWebComponent(elementName: string) {
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
