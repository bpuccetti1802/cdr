import { NgModule, DoBootstrap, NgModuleRef } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { createCustomElement } from '@angular/elements';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { ErrorBoundaryComponent } from './error-boundary.component';
import { RouterModule } from '@angular/router';

let moduleReference: NgModuleRef<ErrorBoundaryModule> | null = null;

@NgModule({
  imports: [
    BrowserModule,
    CommonModule,
    ErrorBoundaryComponent,
    RouterModule.forRoot([{ path: '', component: ErrorBoundaryComponent }]),
  ],
})
export class ErrorBoundaryModule implements DoBootstrap {
  constructor() {}

  ngDoBootstrap() {
    console.warn('⚠️ Devi passare elementName a initErrorBoundaryWebComponent!');
  }
}

export async function initErrorBoundaryWebComponent(elementName: string) {
  moduleReference = await platformBrowserDynamic().bootstrapModule(ErrorBoundaryModule, {
    ngZone: 'noop',
  });

  const ErrorBoundaryElement = createCustomElement(ErrorBoundaryComponent, {
    injector: moduleReference.injector,
  });

  if (!customElements.get(elementName)) {
    customElements.define(elementName, ErrorBoundaryElement);
    console.debug(`✅ Web Component registrato come <${elementName}>`);
  }

  return moduleReference.injector;
}

export function destroyErrorBoundaryWebComponent(elementName: string) {
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
