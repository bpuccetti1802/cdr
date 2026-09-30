import { NgModule, DoBootstrap, NgModuleRef } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { createCustomElement } from '@angular/elements';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { StackedBarChartComponent } from './stacked-bar-chart.component';

let moduleReference: NgModuleRef<StackedBarChartModule> | null = null;

@NgModule({
  imports: [BrowserModule, CommonModule, StackedBarChartComponent],
  declarations: [],
})
export class StackedBarChartModule implements DoBootstrap {
  ngDoBootstrap() {
    console.warn('⚠️ Devi passare elementName a initStackedBarChartWebComponent!');
  }
}

export async function initStackedBarChartWebComponent(elementName: string) {
  if (moduleReference) {
    console.warn(`⚠️ Web Component <${elementName}> è già attivo.`);
    return;
  }

  moduleReference = await platformBrowserDynamic().bootstrapModule(StackedBarChartModule, {
    ngZone: 'noop',
  });

  const StackedBarChartElement = createCustomElement(StackedBarChartComponent, {
    injector: moduleReference.injector,
  });

  if (customElements.get(elementName)) {
    console.error(`⚠️ L'elemento <${elementName}> è già stato definito!`);
  } else {
    customElements.define(elementName, StackedBarChartElement);
    console.log(`✅ Web Component registrato come <${elementName}>`);
  }

  return moduleReference.injector;
}

export function destroyStackedBarChartWebComponent(elementName: string) {
  if (!moduleReference) {
    console.warn(`⚠️ Nessun Web Component attivo da distruggere.`);
    return;
  }

  try {
    // moduleReference.destroy(); // opzionale: spesso lasciato commentato come nel tuo esempio
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
