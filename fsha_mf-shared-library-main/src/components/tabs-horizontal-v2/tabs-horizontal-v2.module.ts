import { NgModule, DoBootstrap, NgModuleRef } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { createCustomElement } from '@angular/elements';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { TabsHorizontalVersion2Component } from './tabs-horizontal-v2.component';
import { CommonModule } from '@angular/common';

let moduleReference: NgModuleRef<TabsHorizontalModule> | null = null;

@NgModule({
  imports: [BrowserModule, CommonModule],
})
export class TabsHorizontalModule implements DoBootstrap {
  constructor() {}
  ngDoBootstrap() {
    console.warn('⚠️ Devi passare elementName a initTabsHorizontalWebComponent!');
  }
}

export async function initTabsHorizontalWebComponent(elementName: string) {
  moduleReference = await platformBrowserDynamic().bootstrapModule(TabsHorizontalModule, {
    ngZone: 'noop',
  });

  const TabsHorizontalWebComponentElement = createCustomElement(TabsHorizontalVersion2Component, {
    injector: moduleReference.injector,
  });

  if (customElements.get(elementName)) {
    console.error(`⚠️ L'elemento <${elementName}> è già stato definito!`);
    // throw new Error(`L'elemento <${elementName}> è già stato definito!`);
  } else {
    customElements.define(elementName, TabsHorizontalWebComponentElement);
    console.log(`✅ Web Component registrato come <${elementName}>`);
  }

  return moduleReference.injector;
}

export function destroyTabsHorizontalWebComponent(elementName: string) {
  if (!moduleReference) {
    console.warn(`⚠️ Nessun Web Component attivo da distruggere.`);
    return;
  }

  try {
    // moduleReference.destroy();
    moduleReference = null;
  } catch (error) {
    console.error(error);
  }

  customElements.get(elementName);

  const element = document.querySelector(elementName);
  if (element) {
    element.remove();
    console.log(`✅ Web Component <${elementName}> rimosso dal DOM.`);
  }

  console.warn(`⚠️ Non puoi deregistrare customElements. Serve ricaricare la pagina.`);
}
