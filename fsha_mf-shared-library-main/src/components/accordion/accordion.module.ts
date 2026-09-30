import { NgModule, DoBootstrap, NgModuleRef } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { createCustomElement } from '@angular/elements';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AccordionComponent } from './accordion.component';

let moduleReference: NgModuleRef<AccordionModule> | null = null;

@NgModule({
  imports: [BrowserModule],
})
export class AccordionModule implements DoBootstrap {
  constructor() {}
  ngDoBootstrap() {
    console.warn('⚠️ Devi passare elementName a initAccordionWebComponent!');
  }
}

export async function initAccordionWebComponent(elementName: string) {
  if (moduleReference) {
    console.warn(`⚠️ Web Component <${elementName}> è già attivo.`);
    return;
  }

  moduleReference = await platformBrowserDynamic().bootstrapModule(AccordionModule, {
    ngZone: 'noop',
  });

  const AccordionWebComponentElement = createCustomElement(AccordionComponent, {
    injector: moduleReference.injector,
  });

  if (customElements.get(elementName)) {
    console.error(`⚠️ L'elemento <${elementName}> è già stato definito!`);
    // throw new Error(`L'elemento <${elementName}> è già stato definito!`);
  } else {
    customElements.define(elementName, AccordionWebComponentElement);
    console.log(`✅ Web Component registrato come <${elementName}>`);
  }

  return moduleReference.injector;
}

export function destroyAccordionWebComponent(elementName: string) {
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

  const element = document.querySelector(elementName);
  if (element) {
    element.remove();
    console.log(`✅ Web Component <${elementName}> rimosso dal DOM.`);
  }

  console.warn(`⚠️ Non puoi deregistrare customElements. Serve ricaricare la pagina.`);
}
