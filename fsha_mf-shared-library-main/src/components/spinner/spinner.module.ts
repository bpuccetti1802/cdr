import { NgModule, DoBootstrap, NgModuleRef } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { createCustomElement } from '@angular/elements';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { SpinnerComponent } from './spinner.component';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { CardWrapperComponent } from '../card-wrapper/card-wrapper.component';

let moduleReference: NgModuleRef<SpinnerModule> | null = null;

@NgModule({
  imports: [BrowserModule, CommonModule, FormsModule, FontAwesomeModule, CardWrapperComponent],
})
export class SpinnerModule implements DoBootstrap {
  constructor() {}

  ngDoBootstrap() {
    console.warn('⚠️ Devi passare elementName a initSpinnerWebComponent!');
  }
}

export async function initSpinnerWebComponent(elementName: string) {
  if (moduleReference) {
    console.warn(`⚠️ Web Component <${elementName}> è già attivo.`);
    return;
  }
  console.log('ciao');
  moduleReference = await platformBrowserDynamic().bootstrapModule(SpinnerModule, {
    ngZone: 'noop',
  });

  const SpinnerComponentElement = createCustomElement(SpinnerComponent, {
    injector: moduleReference.injector,
  });

  if (customElements.get(elementName)) {
    console.error(`⚠️ L'elemento <${elementName}> è già stato definito!`);
    throw new Error(`L'elemento <${elementName}> è già stato definito!`);
  } else {
    customElements.define(elementName, SpinnerComponentElement);
    console.log(`✅ Web Component registrato come <${elementName}>`);
  }

  return moduleReference.injector;
}

export function destroySpinnerWebComponent(elementName: string) {
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
