import type { Meta, StoryObj } from '@storybook/angular';
import { ImageComponent } from './image.component';

const meta: Meta<ImageComponent> = {
  title: 'Components/Image',
  component: ImageComponent,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<ImageComponent>;

export const Default: Story = {
  name: 'Immagine di Default',
  args: {
    name: 'rc-logo.png',
  },
};
