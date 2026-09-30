import { CommonModule } from '@angular/common';
import { Component, Input, OnInit } from '@angular/core';
import { Route, RouterModule, Routes } from '@angular/router';
import { IconComponent } from '../icon/icon.component';
import {
  EnteInfo,
  SocialLink,
  MenuItem,
  DataRoute,
  ContactInfo,
  IconSize,
} from 'test-library-frankmd93';
import { WideContainerDirective } from '@mf/directives/wide-container/wide-container.directive';
import { ImageComponent } from '../image/image.component';

@Component({
  selector: 'app-mf-footer',
  standalone: true,
  imports: [CommonModule, RouterModule, IconComponent, WideContainerDirective, ImageComponent],
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss'],
})
export class FooterComponent implements OnInit {
  @Input() useRoutes = false;
  @Input() logo: string = 'rc-logo.png';
  @Input() backgroundColorTopContainerClass = 'mf-background-color-secondary-darker';
  @Input() backgroundColorBottomContainerClass = 'mf-background-color-secondary-dark';

  routesWithHome!: Routes;

  @Input() useRoutesWithHome = false;

  @Input() ente: EnteInfo = {
    label: 'Roma Capitale',
    tagline: 'Comune di Roma',
  };

  @Input() contact: ContactInfo = {
    address: 'Piazza del Campidoglio 1 - 00186 (RM)',
    pIva: 'Partita IVA 01057861005',
    fiscalCode: 'Codice Fiscale 02438750586',
  };

  @Input() socialLinks: SocialLink[] = [
    {
      nameIcon: 'it-facebook',
      route: 'https://www.facebook.com/RomaCapitaleOfficialPage',
      label: 'Facebook',
    },
    { nameIcon: 'it-twitter', route: 'https://x.com/roma', label: 'X' },
    {
      nameIcon: 'it-linkedin',
      route: 'https://www.linkedin.com/company/romacapitale/',
      label: 'LinkedIn',
    },
    { nameIcon: 'it-instagram', route: 'https://www.instagram.com/roma/', label: 'Instagram' },
    {
      nameIcon: 'it-youtube',
      route: 'https://www.youtube.com/notizieromacapitale',
      label: 'Youtube',
    },
    {
      nameIcon: 'it-whatsapp',
      route: 'https://www.whatsapp.com/channel/0029Va2Gj7WL7UVbp8jNya1C',
      label: 'Whatsapp',
    },
    {
      nameIcon: 'it-tiktok',
      route: 'https://www.tiktok.com/@roma.capitale?_t=8hLsxaA5oEy&_r=1',
      label: 'TikTok',
    },
  ];

  @Input() hasPNRRLogos: boolean = false;

  @Input() routes!: Routes;

  @Input() menuItemsPolicy: MenuItem[] = [
    {
      label: 'Privacy',
      route: '/web/it/privacy.page',
    },
    {
      label: 'Cookie Policy',
      route: '/web/it/cookie-policy.page',
    },
  ];

  @Input() menuLinksFooter!: MenuItem[];

  @Input() isLogged: boolean = false;

  protected readonly IconSize = IconSize;

  protected readonly financedByLogo: string = 'NextGenerationEU.png';

  protected readonly ministerialLogo: string = 'LOGO-DFP-BIANCO.png';

  protected readonly dipartimentoLogo: string = 'LOGO-DIPARTIMENTO-TRASFORMAZIONE-DIGITALE.png';

  mapMenuItemsInRoutes(): Routes {
    return (
      this.menuLinksFooter?.map((menuItem) => ({
        path: menuItem.route,
        data: {
          label: menuItem.label,
        },
      })) || []
    );
  }

  ngOnInit() {
    if (this.routes?.some((element) => element.data?.['label'] === 'Home')) {
      this.routesWithHome = this.useRoutes ? this.routes : this.mapMenuItemsInRoutes();
    } else {
      this.routesWithHome = this.useRoutes
        ? this.useRoutesWithHome
          ? [...this.routes]
          : [{ path: '', data: { label: 'Home' } }, ...this.routes]
        : this.useRoutesWithHome
          ? [...this.routes]
          : [{ path: '', data: { label: 'Home' } }, ...this.mapMenuItemsInRoutes()];
    }
  }

  trackMenuLinkById(index: number, menuLink: Route) {
    return (menuLink.data as DataRoute)?.label;
  }

  trackMenuLinkByIdMenu(index: number, menuLink: MenuItem) {
    return menuLink.label;
  }

  trackSocialById(index: number, menuLink: SocialLink) {
    return menuLink.label;
  }
}
