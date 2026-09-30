import type { Meta, StoryObj } from '@storybook/angular';

import { InputPasswordComponent } from './input-password.component';
import { FormControl, Validators } from '@angular/forms';

const meta: Meta<InputPasswordComponent> = {
  component: InputPasswordComponent,
};

export default meta;
type Story = StoryObj<InputPasswordComponent>;

export const Primary: Story = {
  name: 'Normal Input',
  args: {
    label: 'Normal Input',
    id: 'example',
    formControl: new FormControl(),
  },
};

export const Primary2: Story = {
  name: 'Normal Input-auto',
  args: {
    label: 'Normal Input',
    id: 'example',
    width: 'auto',
    formControl: new FormControl(),
  },
};

export const Secondary: Story = {
  name: 'Input with error message',
  args: {
    label: 'Example',
    id: 'example',
    formControl: new FormControl('', [Validators.required]),
  },
  play: ({ args }) => {
    args.formControl.markAsTouched(); // ⬅️ Simula il blur per attivare il messaggio di errore
  },
};

export const Tertiary: Story = {
  name: 'Input with error message-auto',
  args: {
    label: 'Example',
    id: 'example',
    width: 'auto',
    formControl: new FormControl('', Validators.required),
  },
  play: ({ args }) => {
    args.formControl.markAsTouched(); // ⬅️ Simula il blur per attivare il messaggio di errore
  },
};
