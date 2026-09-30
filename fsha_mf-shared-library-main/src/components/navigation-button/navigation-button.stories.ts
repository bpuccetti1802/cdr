import type { Meta, StoryObj } from '@storybook/angular';
import { NavigationButtonComponent } from './navigation-button.component';

const meta: Meta<NavigationButtonComponent> = {
  title: 'Components/Navigation Button',
  component: NavigationButtonComponent,
  tags: ['autodocs'],
  argTypes: {
    label: { control: 'text' },
    iconName: { control: 'text' },
    action: { action: 'clicked' },
  },
};

export default meta;
type Story = StoryObj<NavigationButtonComponent>;

// 📌 Bottone di Navigazione di Default
export const Default: Story = {
  name: 'Navigation Button Base',
  args: {
    label: 'Vai alla pagina',
    iconName: 'it-arrow-right',
  },
};

// 📌 Bottone senza icona
export const WithoutIcon: Story = {
  name: 'Senza Icona',
  args: {
    label: 'Senza icona',
    iconName: '',
  },
};
