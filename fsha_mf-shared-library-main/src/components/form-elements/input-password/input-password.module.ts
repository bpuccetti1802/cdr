import { createCustomElement } from '@angular/elements';
import { NgModule, DoBootstrap, NgModuleRef } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { InputPasswordComponent } from './input-password.component';
import { HttpClientModule } from '@angular/common/http';

let moduleReference: NgModuleRef<InputPasswordModule> | null = null;

@NgModule({
  imports: [BrowserModule, HttpClientModule],
})
export class InputPasswordModule implements DoBootstrap {
  constructor() {}

  ngDoBootstrap() {
    // 🔥 L'elementName verrà passato direttamente nella funzione di bootstrap
    console.warn('⚠️ Devi passare elementName a initInputPasswordWebComponent!');
  }
}

export async function initInputPasswordWebComponent(elementName: string) {
  moduleReference = await platformBrowserDynamic().bootstrapModule(InputPasswordModule, {
    ngZone: 'noop',
  });

  const InputPasswordWebComponentElement = createCustomElement(InputPasswordComponent, {
    injector: moduleReference.injector,
  });

  if (!customElements.get(elementName)) {
    customElements.define(elementName, InputPasswordWebComponentElement);
    console.debug(`✅ Web Component registrato come <${elementName}>`);
  }

  return moduleReference.injector;
}
export function destroyInputPasswordWebComponent(elementName: string) {
  if (!moduleReference) {
    console.warn(`⚠️ Nessun Web Component attivo da distruggere.`);
    return;
  }

  // 🔥 Distruggiamo l'app Angular
  moduleReference.destroy();
  moduleReference = null;

  // 🔥 Rimuoviamo il Web Component dal DOM
  const element = document.querySelector(elementName);
  if (element) {
    element.remove();
    console.log(`✅ Web Component <${elementName}> rimosso dal DOM.`);
  }

  // 🔥 Possiamo anche tentare di "rimuovere" la definizione, ma non è standard
  console.warn(
    `⚠️ Non è possibile "deregistrare" customElements. Il Web Component non sarà più usabile finché non si ricarica la pagina.`,
  );
}
