import { Directive, ElementRef, OnInit } from '@angular/core';
import { LayoutService } from '@mf/services/layout.service';

@Directive({
  selector: '[appWideContainer]',
  standalone: true,
})
export class WideContainerDirective implements OnInit {
  constructor(
    private element: ElementRef,
    private layoutService: LayoutService,
  ) {}

  ngOnInit() {
    this.layoutService.applyCurrentLayoutTo(this.element.nativeElement);
  }
}
