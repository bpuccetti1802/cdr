import type { Meta, StoryObj } from '@storybook/angular';
import { Select2VersionComponent } from './select-2v.component';
import { FormControl, Validators } from '@angular/forms';

const meta: Meta<Select2VersionComponent> = {
  component: Select2VersionComponent,
};

export default meta;
type Story = StoryObj<Select2VersionComponent>;

const options = [
  { value: 'option1', label: 'Opzione 1' },
  { value: 'option2', label: 'Opzione 2' },
  { value: 'option3', label: 'Opzione 3' },
];

export const Default: Story = {
  name: 'Select Default',
  args: {
    id: 'select-default',
    label: "Seleziona un'opzione",
    placeholder: "Scegli un'opzione...",
    formControl: new FormControl(''),
    options: options,
    required: false,
  },
};

export const WithPreselectedValue: Story = {
  name: 'Selezione Predefinita',
  args: {
    ...Default.args,
    formControl: new FormControl('option2'),
  },
};

export const Disabled: Story = {
  name: 'Select Disabilitato',
  args: {
    ...Default.args,
    disabled: true,
  },
};

export const WithValidation: Story = {
  name: 'Select con Validazione',
  args: {
    ...Default.args,
    formControl: new FormControl('', Validators.required),
    required: true,
  },
  play: ({ args }) => {
    args.formControl.markAsTouched(); // Simula il blur per attivare il messaggio di errore
  },
};
