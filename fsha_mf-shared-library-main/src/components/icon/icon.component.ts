import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import {
  AfterViewInit,
  Component,
  ElementRef,
  Input,
  OnChanges,
  OnInit,
  ViewChild,
} from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconSize, Colors } from 'test-library-frankmd93';
import {
  faHourglass,
  faSitemap,
  faHouse,
  faUser,
  faCheck,
  IconDefinition,
  faCircleExclamation,
  faTriangleExclamation,
  faLock,
  faCircleCheck,
  faEye,
  faUpload,
  faBars,
  faChevronDown,
  faPlus,
  faTimes,
  faBell,
  faEraser,
  faSearch,
  faUsers,
  faDownload,
  faFileSignature,
  faArrowsRotate,
  faChevronUp,
  faCalendar,
  faFolderPlus,
  faFolderOpen,
  faMinus,
  faXmark,
  faFolder,
  faEllipsis,
  faEllipsisVertical,
  faArrowRotateRight,
  faTimeline,
  faCircleQuestion,
  faBan,
  faTrash,
  faRotate,
  faPenToSquare,
} from '@fortawesome/free-solid-svg-icons';
import { Attributes } from 'test-library-frankmd93';
import { BaseHrefService } from '../../services/base-href/base-href.service';

export interface Icon {
  iconName: string;
  iconColor: string;
  iconTitle?: string;
}

@Component({
  selector: 'app-rc-icon',
  standalone: true,
  imports: [CommonModule, FontAwesomeModule],
  providers: [],
  templateUrl: './icon.component.html',
  styleUrl: './icon.component.scss',
})
export class IconComponent implements OnChanges, OnInit, AfterViewInit {
  constructor(
    private http: HttpClient,
    private sanitizer: DomSanitizer,
    private baseHref: BaseHrefService,
  ) {
    // Metto gli asset e url base icone con baseHref calcolato automaticamente
    this.baseUrl = this.baseHref.baseUrl + this.baseUrl;
  }

  @ViewChild('iconFontAwesomeRef', { static: false, read: ElementRef })
  iconFontAwesomeRef!: ElementRef;
  @ViewChild('iconBootstrapRef', { static: false, read: ElementRef }) iconBootstrapRef!: ElementRef;
  @ViewChild('iconSvgRef', { static: false, read: ElementRef }) iconSvgRef!: ElementRef;
  @Input() size: IconSize = IconSize.md;
  @Input() fontSize: IconSize = IconSize.xs;
  @Input() name!: string;
  @Input() color = 'secondary';
  @Input() useClass = false;
  @Input() colorClass = 'mf-icon-color-grey-0';
  @Input() attr?: Attributes = {};

  @Input() baseUrl = '/mfSharedLibrary';
  bootstrapUrl = '/assets/sprites.svg#';
  svgUrl = '/assets/svg/';
  iconUrl: string = '';
  svgIconData: string = '';

  ngAfterViewInit() {
    this.applyStyles();
  }

  applyFontAwesomeStyles() {
    if (this.isFontAwesomeIcon && this.iconFontAwesomeRef?.nativeElement) {
      const element: HTMLElement = this.iconFontAwesomeRef.nativeElement;
      if (this.useClass) {
        this.colorClass.split(' ').forEach((c) => element.classList.add(c));
        if (this.colorClass.split(' ')?.length > 0) {
          this.colorClass
            .split(' ')
            .forEach((className: string) => element.classList.add(className));
        } else {
          element.classList.add(this.colorClass);
        }
      } else {
        element.style.color = this.colorHex;
      }

      element.style.width = `${this.size}`;
      element.style.height = `${this.size}`;
      element.style.fontSize = `${this.fontSize}`;
    }
  }

  applyBootstrapStyles() {
    if (this.isBootstrapIcon && this.iconBootstrapRef?.nativeElement) {
      const element: SVGElement = this.iconBootstrapRef.nativeElement;
      if (this.useClass) {
        this.colorClass.split(' ').forEach((c) => element.classList.add(c));
        if (this.colorClass.split(' ')?.length > 0) {
          this.colorClass
            .split(' ')
            .forEach((className: string) => element.classList.add(className));
        } else {
          element.classList.add(this.colorClass);
        }
      } else {
        element.setAttribute('fill', this.useClass ? 'currentColor' : this.colorHex);
      }
      element.setAttribute('width', `${this.size}`);
      element.setAttribute('height', `${this.size}`);
    }
  }

  applySvgStyles() {
    if (!this.isBootstrapIcon && !this.isFontAwesomeIcon && this.iconSvgRef?.nativeElement) {
      const element: SVGElement = this.iconSvgRef.nativeElement;
      if (this.useClass) {
        this.colorClass.split(' ').forEach((c) => element.classList.add(c));
        if (this.colorClass.split(' ')?.length > 0) {
          this.colorClass
            .split(' ')
            .forEach((className: string) => element.classList.add(className));
        } else {
          element.classList.add(this.colorClass);
        }
      } else {
        element.style.color = this.colorHex;
      }
      element.setAttribute('width', `${this.size}`);
      element.setAttribute('height', `${this.size}`);
    }
  }

  applyStyles() {
    this.applyFontAwesomeStyles();
    this.applyBootstrapStyles();
    this.applySvgStyles();
  }

  iconMap: { [key: string]: IconDefinition } = {
    'fa-house': faHouse,
    'fa-user': faUser,
    'fa-users': faUsers,
    'fa-check': faCheck,
    'fa-circle-check': faCircleCheck,
    'fa-circle-exclamation': faCircleExclamation,
    'fa-triangle-exclamation': faTriangleExclamation,
    'fa-lock': faLock,
    'fa-eye': faEye,
    'fa-upload': faUpload,
    'fa-download': faDownload,
    'fa-bars': faBars,
    'fa-chevron-up': faChevronUp,
    'fa-chevron-down': faChevronDown,
    'fa-plus': faPlus,
    'fa-times': faTimes,
    'fa-bell': faBell,
    'fa-eraser': faEraser,
    'fa-search': faSearch,
    'fa-file-signature': faFileSignature,
    'fa-arrows-rotate': faArrowsRotate,
    'fa-sitemap': faSitemap,
    'fa-hourglass': faHourglass,
    'fa-calendar': faCalendar,
    'fa-folder-plus': faFolderPlus,
    'fa-folder-open': faFolderOpen,
    'fa-minus': faMinus,
    'fa-xmark': faXmark,
    'fa-folder': faFolder,
    'fa-ellipsis': faEllipsis,
    'fa-ellipsis-vertical': faEllipsisVertical,
    'fa-arrow-rotate-right': faArrowRotateRight,
    'fa-timeline': faTimeline,
    'fa-circle-question': faCircleQuestion,
    'fa-ban': faBan,
    'fa-trash': faTrash,
    'fa-rotate': faRotate,
    'fa-pen-to-square': faPenToSquare,
  };
  ngOnChanges(): void {
    if (!this.isBootstrapIcon && !this.isFontAwesomeIcon) {
      this.svgIconData = this.svgIconData.replaceAll(
        /fill="[^"]*"/g,
        `fill="${this.useClass ? 'currentColor' : this.colorHex}"`,
      );
    }
  }

  get colorHex(): string {
    const colorMap: Record<string, string> = {
      primary: Colors.primary,
      secondary: Colors.secondary,
      success: Colors.success,
      error: Colors.error,
      warning: Colors.warning,
    };

    return colorMap[this.color] || this.color;
  }

  ngOnInit() {
    if (this.name && !this.isFontAwesomeIcon && !this.isBootstrapIcon) {
      this.http.get(this.icon, { responseType: 'text' }).subscribe(
        (data) => {
          const svgIconChangeColor = data
            .replaceAll(/fill="[^"]*"/g, `fill="${this.useClass ? 'currentColor' : this.colorHex}"`)
            .replaceAll(/width="[^"]*"/g, `width=100%`)
            .replaceAll(/height="[^"]*"/g, `height=100%`);
          this.svgIconData = svgIconChangeColor;
        },
        (error) => {
          console.error("Errore durante il caricamento dell'SVG:", error);
        },
      );
    }
  }

  get isBootstrapIcon(): boolean {
    return String(this.name).startsWith('it-');
  }

  get isFontAwesomeIcon(): boolean {
    return String(this.name).startsWith('fa-');
  }

  get icon(): string {
    return this.isBootstrapIcon
      ? this.baseUrl + this.bootstrapUrl + this.name
      : this.baseUrl + this.svgUrl + this.name;
  }

  get svgIcon(): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(this.svgIconData);
  }
}
