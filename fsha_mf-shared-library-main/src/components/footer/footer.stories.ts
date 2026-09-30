import { Meta, StoryObj, applicationConfig } from '@storybook/angular';
import { FooterComponent } from './footer.component';
import { provideRouter, withHashLocation } from '@angular/router';

const meta: Meta<FooterComponent> = {
  title: 'Components/Footer',
  component: FooterComponent,
  decorators: [
    applicationConfig({
      providers: [
        // The router is most likely going to interfere with your Storybook application/iframe
        // route, but hash routes should be fine, so I also add `withHashLocation`.
        provideRouter([], withHashLocation()),
      ],
    }),
  ],
  tags: ['autodocs'],
  argTypes: {
    isLogged: { control: 'boolean' },
  },
};
export default meta;

type Story = StoryObj<FooterComponent>;

export const Default: Story = {
  args: {
    logo: 'rc-logo.png',
    contact: {
      address: 'Piazza del Campidoglio 1 - 00186 (RM)',
      fiscalCode: 'Codice Fiscale 02438750586',
      pIva: 'Partita IVA 01057861005',
    },
    socialLinks: [
      { nameIcon: 'facebook', route: '/facebook', label: 'Facebook' },
      { nameIcon: 'twitter', route: '/twitter', label: 'Twitter' },
      { nameIcon: 'linkedin', route: '/linkedin', label: 'LinkedIn' },
    ],
    menuLinksFooter: [
      { label: 'Home', route: '/' },
      { label: 'Servizi', route: '/servizi' },
      { label: 'Contatti', route: '/contatti' },
    ],
    menuItemsPolicy: [
      { label: 'Privacy', route: '/privacy' },
      { label: 'Cookie Policy', route: '/cookie-policy' },
    ],
    isLogged: true,
  },
};
