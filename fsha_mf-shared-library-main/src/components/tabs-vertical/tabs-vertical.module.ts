import { NgModule, DoBootstrap, NgModuleRef } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { createCustomElement } from '@angular/elements';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { TabsVerticalComponent } from './tabs-vertical.component';
import { CommonModule } from '@angular/common';

let moduleReference: NgModuleRef<TabsVerticalModule> | null = null;

@NgModule({
  imports: [BrowserModule, CommonModule],
})
export class TabsVerticalModule implements DoBootstrap {
  constructor() {}
  ngDoBootstrap() {
    console.warn('⚠️ Devi passare elementName a initTabsVerticalWebComponent!');
  }
}

export async function initTabsVerticalWebComponent(elementName: string) {
  moduleReference = await platformBrowserDynamic().bootstrapModule(TabsVerticalModule, {
    ngZone: 'noop',
  });

  const TabsVerticalWebComponentElement = createCustomElement(TabsVerticalComponent, {
    injector: moduleReference.injector,
  });

  if (customElements.get(elementName)) {
    console.error(`⚠️ L'elemento <${elementName}> è già stato definito!`);
    // throw new Error(`L'elemento <${elementName}> è già stato definito!`);
  } else {
    customElements.define(elementName, TabsVerticalWebComponentElement);
    console.log(`✅ Web Component registrato come <${elementName}>`);
  }

  return moduleReference.injector;
}

export function destroyTabsVerticalWebComponent(elementName: string) {
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
