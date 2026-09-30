import type { Meta, StoryObj } from '@storybook/angular';
import { InputComponent } from './input.component';
import { FormControl, Validators } from '@angular/forms';

const meta: Meta<InputComponent> = {
  title: 'Components/Input',
  component: InputComponent,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<InputComponent>;

const getErrorMessage = (formControl: FormControl) => {
  if (formControl.errors?.['required']) {
    return 'Questo campo è obbligatorio.';
  }
  if (formControl.errors?.['pattern']) {
    return 'Il formato non è valido.';
  }
  return null;
};

export const Primary: Story = {
  name: 'Example Disabled',
  args: {
    label: 'Disabled',
    disabled: true,
    id: 'example',
  },
};

export const Primary2: Story = {
  name: 'Example Disabled-auto',
  args: {
    label: 'Disabled',
    disabled: true,
    id: 'example',
    width: 'auto',
  },
};

export const Secondary: Story = {
  name: 'Input with placeholder',
  args: {
    label: 'Example',
    id: 'example',
    placeholder: 'Placeholder',
    type: 'text',
    disabled: false,
    width: 'auto',
  },
};

export const Placeholder: Story = {
  name: 'Input with placeholder-auto',
  args: {
    label: 'Example',
    id: 'example',
    placeholder: 'Placeholder',
    type: 'text',
    disabled: false,
  },
};

export const Tertiary: Story = {
  name: 'Input with error message',
  args: {
    label: 'Example',
    id: 'example',
    type: 'text',
    disabled: false,
    formControl: new FormControl('', Validators.required),
    getErrorMessage: getErrorMessage,
  },
  play: ({ args }) => {
    if (args.formControl) {
      args.formControl.markAsTouched(); // Simula il blur per attivare il messaggio di errore
    }
  },
};

export const Tertiary2: Story = {
  name: 'Input with error message-auto',
  args: {
    label: 'Example',
    id: 'example',
    type: 'text',
    disabled: false,
    width: 'auto',
    formControl: new FormControl('', Validators.required),
    getErrorMessage: getErrorMessage,
    required: true,
  },
  play: ({ args }) => {
    if (args.formControl) {
      args.formControl.markAsTouched(); // Simula il blur per attivare il messaggio di errore
    }
  },
};
