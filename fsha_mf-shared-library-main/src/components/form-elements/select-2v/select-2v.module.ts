import { NgModule, DoBootstrap, NgModuleRef } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { createCustomElement } from '@angular/elements';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { Select2VersionComponent } from './select-2v.component';
import { HttpClientModule } from '@angular/common/http';

let moduleReference: NgModuleRef<Select2VersionModule> | null = null;

@NgModule({
  imports: [BrowserModule, HttpClientModule],
})
export class Select2VersionModule implements DoBootstrap {
  constructor() {}
  ngDoBootstrap() {
    console.warn('⚠️ Devi passare elementName a initSelectWebComponent!');
  }
}

export async function initSelect2VersionWebComponent(elementName: string) {
  moduleReference = await platformBrowserDynamic().bootstrapModule(Select2VersionModule, {
    ngZone: 'noop',
  });

  const Select2VersionWebComponentElement = createCustomElement(Select2VersionComponent, {
    injector: moduleReference.injector,
  });

  if (customElements.get(elementName)) {
    console.error(`⚠️ L'elemento <${elementName}> è già stato definito!`);
    // throw new Error(`L'elemento <${elementName}> è già stato definito!`);
  } else {
    customElements.define(elementName, Select2VersionWebComponentElement);
    console.log(`✅ Web Component registrato come <${elementName}>`);
  }

  return moduleReference.injector;
}

export function destroySelect2VersionWebComponent(elementName: string) {
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
