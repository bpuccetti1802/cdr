import type { Meta, StoryObj } from '@storybook/angular';
import { SpinnerComponent } from './spinner.component';

const meta: Meta<SpinnerComponent> = {
  title: 'Components/Spinner',
  component: SpinnerComponent,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<SpinnerComponent>;

// 📌 Spinner di default
export const Default: Story = {
  name: 'Default Spinner',
};
