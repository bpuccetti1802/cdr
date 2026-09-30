import { moduleMetadata, type Meta, type StoryObj } from '@storybook/angular';
import { HeaderComponent } from './header.component';

import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';
import { MenuItem } from 'test-library-frankmd93';

const meta: Meta<HeaderComponent> = {
  title: 'Components/Header',
  component: HeaderComponent,
  tags: ['autodocs'],
  argTypes: {
    onLogOut: { action: 'logout' },
  },
  decorators: [
    moduleMetadata({
      providers: [
        {
          provide: ActivatedRoute,
          useValue: { params: of({}), queryParams: of({}) }, // Mock dei parametri
        },
      ],
    }),
  ],
};

export default meta;
type Story = StoryObj<HeaderComponent>;

export const Default: Story = {
  name: 'Default Header',
  args: {
    baseUrl: '/mfSharedLibrary',
    enteAppartenenza: 'Comune di Roma',
    isVisibleLanguages: true,
    isVisibleSocials: true,
    isVisibleSearch: true,
    isVisibleLogin: true,
    isLogged: false,
    userName: 'Mario Rossi',
    logo: '/assets/images/rc-logo.png',
    ente: {
      label: 'Roma Capitale',
      tagline: 'Comune di Roma',
    },
    slimHeaderMenuLinks: [
      { label: 'Home', route: '/' },
      { label: 'Servizi', route: '/servizi' },
      { label: 'Contatti', route: '/contatti' },
    ] as MenuItem[],
    loginButtonUrl: '/login',
    profileEditUrl: '/profilo',
  },
};

export const LoggedIn: Story = {
  name: 'Logged In Header',
  args: {
    ...Default.args,
    isLogged: true,
    userName: 'Mario Rossi',
  },
};

export const WithoutSocialsAndSearch: Story = {
  name: 'Header Without Socials & Search',
  args: {
    ...Default.args,
    isVisibleSocials: false,
    isVisibleSearch: false,
  },
};
