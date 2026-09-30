import { Injectable, Renderer2, RendererFactory2 } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class LayoutService {
  private renderer: Renderer2;
  private wideMode = true;

  get isExpanded() {
    return this.wideMode;
  }

  constructor(rendererFactory: RendererFactory2) {
    this.renderer = rendererFactory.createRenderer(null, null);
  }

  toggleContainerLayout() {
    if (this.wideMode) {
      // wideMode attivo → container-wide → container
      const wideContainers = document.querySelectorAll('.container-wide');

      wideContainers.forEach((element) => {
        this.renderer.removeClass(element, 'container-wide');
        this.renderer.addClass(element, 'container');
      });
    } else {
      // wideMode disattivo → container → container-wide
      const containers = document.querySelectorAll('.container');

      containers.forEach((element) => {
        this.renderer.removeClass(element, 'container');
        this.renderer.addClass(element, 'container-wide');
      });
    }

    this.wideMode = !this.wideMode;
  }

  // opzionale: per aggiornare nuovi componenti creati dopo
  applyCurrentLayoutTo(element: HTMLElement) {
    const notViewMode = !this.wideMode;
    if (notViewMode) {
      this.renderer.removeClass(element, 'container-wide');
      this.renderer.addClass(element, 'container');
    } else {
      this.renderer.removeClass(element, 'container');
      this.renderer.addClass(element, 'container-wide');
    }
  }
}
