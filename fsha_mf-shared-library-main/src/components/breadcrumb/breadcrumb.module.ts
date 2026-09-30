import { NgModule, DoBootstrap, NgModuleRef } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { createCustomElement } from '@angular/elements';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { BreadcrumbComponent } from './breadcrumb.component';
import { RouterModule } from '@angular/router';

let moduleReference: NgModuleRef<BreadcrumbModule> | null = null;

@NgModule({
  imports: [BrowserModule, RouterModule.forRoot([])],
})
export class BreadcrumbModule implements DoBootstrap {
  constructor() {}
  ngDoBootstrap() {
    console.warn('⚠️ Devi passare elementName a initBreadcrumbWebComponent!');
  }
}

export async function initBreadcrumbWebComponent(elementName: string) {
  moduleReference = await platformBrowserDynamic().bootstrapModule(BreadcrumbModule, {
    ngZone: 'noop',
  });

  const BreadcrumbWebComponentElement = createCustomElement(BreadcrumbComponent, {
    injector: moduleReference.injector,
  });

  if (customElements.get(elementName)) {
    console.error(`⚠️ L'elemento <${elementName}> è già stato definito!`);
    // throw new Error(`L'elemento <${elementName}> è già stato definito!`);
  } else {
    customElements.define(elementName, BreadcrumbWebComponentElement);
    console.log(`✅ Web Component registrato come <${elementName}>`);
  }

  return moduleReference.injector;
}

export function destroyBreadcrumbWebComponent(elementName: string) {
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
