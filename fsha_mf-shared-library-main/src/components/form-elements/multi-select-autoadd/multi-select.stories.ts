import type { Meta, StoryObj } from '@storybook/angular';
import { MultiSelectAutoaddComponent } from './multi-select-autoadd.component';
import { FormControl, Validators } from '@angular/forms';

const meta: Meta<MultiSelectAutoaddComponent> = {
  title: 'Components/MultiSelectAutoadd',
  component: MultiSelectAutoaddComponent,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<MultiSelectAutoaddComponent>;

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
  name: 'Default',
  args: {
    id: 'multi-select',
    label: 'Mailing List',
    placeholder: 'Scrivi...',
    disabled: false,
  },
};

export const Secondary: Story = {
  name: 'Disabled',
  args: {
    id: 'multi-select-disabled',
    label: 'Mailing List (Disabilitato)',
    placeholder: 'Disabilitato',
    disabled: true,
  },
};

export const Tertiary: Story = {
  name: 'With Error',
  args: {
    id: 'multi-select-error',
    label: 'Mailing List con errore',
    placeholder: 'Scrivi...',
    formControl: new FormControl('', Validators.required),
    getErrorMessage: getErrorMessage,
  },
  play: ({ args }) => {
    args.formControl.markAsTouched(); // Simula il blur per attivare il messaggio di errore
  },
};
