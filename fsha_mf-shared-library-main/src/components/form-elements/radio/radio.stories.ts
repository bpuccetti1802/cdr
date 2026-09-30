import type { Meta, StoryObj } from '@storybook/angular';
import { RadioComponent } from './radio.component';
import { FormControl } from '@angular/forms';

const meta: Meta<RadioComponent> = {
  component: RadioComponent,
};

export default meta;
type Story = StoryObj<RadioComponent>;

const radioItems = [
  { value: 'option1', label: 'Opzione 1' },
  { value: 'option2', label: 'Opzione 2' },
  { value: 'option3', label: 'Opzione 3' },
];

export const Default: Story = {
  name: 'Radio Default',
  args: {
    id: 'radio-group',
    label: "Seleziona un'opzione",
    formControl: new FormControl('option1'),
    items: radioItems,
    inline: false,
  },
};

export const Inline: Story = {
  name: 'Radio Inline',
  args: {
    ...Default.args,
    inline: true,
  },
};

export const Disabled: Story = {
  name: 'Radio Disabilitato',
  args: {
    ...Default.args,
    disabled: true,
  },
};

export const Empty: Story = {
  name: 'Senza selezione',
  args: {
    ...Default.args,
    formControl: new FormControl(''),
  },
};
