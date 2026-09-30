import type { Meta, StoryObj } from '@storybook/angular';
import { PickerComponent } from './picker.component';
import { FormControl, Validators } from '@angular/forms';

const meta: Meta<PickerComponent> = {
  title: 'Components/Picker',
  component: PickerComponent,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<PickerComponent>;

export const Default: Story = {
  name: 'default',
  args: {
    id: 'date-picker',
    label: 'Seleziona una data',
    placeholder: 'GG/MM/AAAA',
    disabled: false,
    width: '100%',
    required: false,
  },
};

export const Disabled: Story = {
  name: 'disabled',
  args: {
    id: 'date-picker-disabled',
    label: 'Data non modificabile',
    placeholder: 'GG/MM/AAAA',
    disabled: true,
    width: '100%',
  },
};

export const WithError: Story = {
  name: 'Data con errore',
  args: {
    id: 'date-picker-error',
    label: 'Data con errore',
    placeholder: 'GG/MM/AAAA',
    disabled: false,
    width: '100%',
    errorMessage: 'Seleziona una data valida',
    formControl: new FormControl('', Validators.required),
    required: true,
  },
  play: ({ args }) => {
    args.formControl.markAsTouched(); // ⬅️ Simula il blur per attivare il messaggio di errore
  },
};
