import { NgModule, DoBootstrap, NgModuleRef } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { createCustomElement } from '@angular/elements';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { CheckboxTableComponent } from './checkbox-table.component';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { CardWrapperComponent } from '../card-wrapper/card-wrapper.component';

let moduleReference: NgModuleRef<CheckboxTableModule> | null = null;

@NgModule({
  imports: [BrowserModule, CommonModule, FormsModule, FontAwesomeModule, CardWrapperComponent],
})
export class CheckboxTableModule implements DoBootstrap {
  constructor() {}

  ngDoBootstrap() {
    console.warn('⚠️ Devi passare elementName a initTableWebComponent!');
  }
}

export async function initTableWebComponent(elementName: string) {
  if (moduleReference) {
    console.warn(`⚠️ Web Component <${elementName}> è già attivo.`);
    return;
  }
  moduleReference = await platformBrowserDynamic().bootstrapModule(CheckboxTableModule, {
    ngZone: 'noop',
  });

  const TableComponentElement = createCustomElement(CheckboxTableComponent, {
    injector: moduleReference.injector,
  });

  if (customElements.get(elementName)) {
    console.error(`⚠️ L'elemento <${elementName}> è già stato definito!`);
    // throw new Error(`L'elemento <${elementName}> è già stato definito!`);
  } else {
    customElements.define(elementName, TableComponentElement);
    console.log(`✅ Web Component registrato come <${elementName}>`);
  }

  return moduleReference.injector;
}

export function destroyTableWebComponent(elementName: string) {
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
