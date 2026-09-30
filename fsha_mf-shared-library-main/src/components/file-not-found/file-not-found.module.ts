import { NgModule, DoBootstrap, NgModuleRef } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { createCustomElement } from '@angular/elements';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { FileNotFoundComponent } from './file-not-found.component';
import { RouterModule } from '@angular/router';

let moduleReference: NgModuleRef<FileNotFoundModule> | null = null;

@NgModule({
  imports: [BrowserModule, CommonModule, FileNotFoundComponent, RouterModule.forRoot([])],
})
export class FileNotFoundModule implements DoBootstrap {
  constructor() {}

  ngDoBootstrap() {
    console.warn('⚠️ Devi passare elementName a initFileNotFoundWebComponent!');
  }
}

export async function initFileNotFoundWebComponent(elementName: string) {
  moduleReference = await platformBrowserDynamic().bootstrapModule(FileNotFoundModule, {
    ngZone: 'noop',
  });

  const FileNotFoundElement = createCustomElement(FileNotFoundComponent, {
    injector: moduleReference.injector,
  });

  if (!customElements.get(elementName)) {
    customElements.define(elementName, FileNotFoundElement);
    console.debug(`✅ Web Component registrato come <${elementName}>`);
  }

  return moduleReference.injector;
}

export function destroyFileNotFoundWebComponent(elementName: string) {
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
