import { HttpClientModule } from '@angular/common/http';
import { Meta, moduleMetadata, StoryObj } from '@storybook/angular';
import { ButtonIconComponent } from './button-icon.component';
import { Colors } from 'test-library-frankmd93';

const meta: Meta<ButtonIconComponent> = {
  title: 'Components/Button Icon',
  component: ButtonIconComponent,
  tags: ['autodocs'],
  decorators: [
    moduleMetadata({
      imports: [HttpClientModule],
    }),
  ],
  argTypes: {
    clickEvent: { action: 'clicked' }, // Registra l'evento in Storybook
  },
};

export default meta;
type Story = StoryObj<ButtonIconComponent>;

export const Default: Story = {
  args: {
    name: 'it-search', // 🔍 Icona predefinita
    color: Colors.secondary,
    class: 'icon icon-md',
    attr: { 'aria-hidden': 'true', role: 'button' },
  },
};

export const Primary: Story = {
  args: {
    name: 'it-home',
    color: Colors.primary,
    class: 'icon icon-md',
    attr: { 'aria-hidden': 'true', role: 'button' },
  },
};

// export const WithClick: Story = {
//   args: {
//     ...Default.args,
//   },
//   play: async ({ args }) => {
//     await new Promise((resolve) => setTimeout(resolve, 500)); // ⏳ Aspetta il rendering
//     args.clickEvent.emit(); // 🚀 Simula un click per testarlo
//   },
// };
