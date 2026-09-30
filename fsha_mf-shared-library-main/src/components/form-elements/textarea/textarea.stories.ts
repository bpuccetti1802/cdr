import type { Meta, StoryObj } from '@storybook/angular';
import { TextAreaComponent } from './textarea.component';
import { FormControl } from '@angular/forms';

const meta: Meta<TextAreaComponent> = {
  title: 'Components/TextArea',
  component: TextAreaComponent,
};

export default meta;
type Story = StoryObj<TextAreaComponent>;

export const Default: Story = {
  name: 'Default TextArea',
  args: {
    id: 'default-textarea',
    label: 'Default',
    placeholder: 'Scrivi qui...',
    rows: 3,
    resize: 'vertical',
    disabled: false,
    formControl: new FormControl(''),
    required: false,
  },
};

export const Disabled: Story = {
  name: 'Disabled TextArea',
  args: {
    id: 'disabled-textarea',
    label: 'Disabled',
    placeholder: 'Non modificabile',
    rows: 3,
    resize: 'none',
    disabled: true,
    formControl: new FormControl(''),
  },
};
