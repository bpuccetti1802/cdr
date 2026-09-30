import { Directive, Input, OnInit, ElementRef, Renderer2 } from '@angular/core';
import { IconSize } from 'test-library-frankmd93';

@Directive({
  selector: '[appRcIcon]', // Seleziona l'elemento in cui applicare la direttiva
  standalone: true,
})
export class RcIconDirective implements OnInit {
  @Input('appRcIcon') config!: {
    name: string;
    size?: IconSize;
    colorClass?: string;
    useClass?: boolean;
    color?: string;
    attr?: { [key: string]: string | null };
  };

  constructor(
    private element: ElementRef, // Riferimento all'elemento host
    private renderer: Renderer2, // Renderer per manipolare il DOM
  ) {}

  ngOnInit() {
    const host = this.element.nativeElement;

    // Pulizia dell'host (facoltativa)
    while (host.firstChild) {
      this.renderer.removeChild(host, host.firstChild);
    }
    // Creiamo il componente SVG
    const svgElement = this.createSvgElement();

    // Impostiamo le proprietà dell'icona
    this.applyIconProperties(svgElement);

    // Sostituire l'elemento host con l'elemento SVG
    this.renderer.appendChild(this.element.nativeElement, svgElement);
  }

  private createSvgElement(): SVGElement {
    const svgElement = this.renderer.createElement('svg', 'http://www.w3.org/2000/svg');

    // Qui, puoi personalizzare le dimensioni o altre proprietà di base
    svgElement.setAttribute('width', this.config.size?.toString() || '16px');
    svgElement.setAttribute('height', this.config.size?.toString() || '16px');
    svgElement.setAttribute('fill', this.config.color);

    return svgElement;
  }

  private applyIconProperties(svgElement: SVGElement) {
    // Aggiungi il codice per popolare il contenuto dell'icona
    const useElement = this.renderer.createElement('use', 'http://www.w3.org/2000/svg');
    useElement.setAttribute(
      'xlink:href',
      `/mfSharedLibrary/assets/sprites.svg#${this.config.name}`,
    );

    svgElement.append(useElement);

    // Aggiungi classi di colore se necessario
    if (this.config.colorClass) {
      svgElement.classList.add(this.config.colorClass);
    }
  }
}
