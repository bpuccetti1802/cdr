import { StoryObj, moduleMetadata } from '@storybook/angular';
import { ReactiveFormsModule, FormControl } from '@angular/forms';
import { CheckboxComponent, defaultGetErrorMessage } from './checkbox.component';

export default {
  title: 'Componenti/Checkbox',
  component: CheckboxComponent,
  decorators: [
    moduleMetadata({
      imports: [ReactiveFormsModule],
    }),
  ],
  tags: ['autodocs'],
  render: (arguments_: CheckboxComponent) => ({
    props: {
      ...arguments_,
      formControl: arguments_.formControl || new FormControl(false), // Evita undefined
      changeEvent: arguments_.changeEvent ?? ((event: Event) => console.log('changeEvent', event)),
    },
  }),
  args: {
    id: 'checkbox1',
    label: 'Accetto i termini e le condizioni',
    getErrorMessage: defaultGetErrorMessage,
    formControl: new FormControl(false), // Assicura che non sia undefined
    width: '100%',
    class: 'form-check-input',
    disabled: false, // Default: attiva
  },
};

export const Default: StoryObj<CheckboxComponent> = {};

export const Disabled: StoryObj<CheckboxComponent> = {
  name: 'Checkbox disabilitata',
  args: {
    disabled: true,
    label: 'Non modificabile',
    id: 'checkbox-disabled',
    formControl: new FormControl({ value: false, disabled: true }), // Stato disabilitato nel FormControl
  },
};
