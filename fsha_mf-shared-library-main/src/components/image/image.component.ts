import { CommonModule } from '@angular/common';
import { Component, Input, OnInit } from '@angular/core';
import { BaseHrefService } from '@mf/services/base-href/base-href.service';
@Component({
  selector: 'app-rc-image',
  standalone: true,
  imports: [CommonModule],
  providers: [],
  templateUrl: './image.component.html',
  styleUrl: './image.component.scss',
})
export class ImageComponent implements OnInit {
  @Input() baseUrl = '/mfSharedLibrary';
  assetsUrl = '/assets/images/';

  @Input() name!: string;
  @Input() width?: number;
  @Input() height?: number;
  @Input() alt: string = 'Immagine';
  @Input() class = '';

  constructor(private baseHref: BaseHrefService) {}

  ngOnInit(): void {
    // Metto gli asset e url base icone con baseHref calcolato automaticamente
    this.baseUrl = this.baseHref.baseUrl + this.baseUrl?.trim();
  }

  get imageSrc(): string {
    return this.baseUrl + this.assetsUrl + this.name;
  }
}
