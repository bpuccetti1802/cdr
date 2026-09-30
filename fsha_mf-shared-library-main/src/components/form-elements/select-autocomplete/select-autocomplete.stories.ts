import type { Meta, StoryObj } from '@storybook/angular';
import { SelectAutocompleteComponent } from './select-autocomplete.component';

const meta: Meta<SelectAutocompleteComponent> = {
  title: 'Components/SelectAutocomplete',
  component: SelectAutocompleteComponent,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<SelectAutocompleteComponent>;

export const Primary: Story = {
  name: 'Default',
  args: {
    id: 'select-autocomplete',
    label: 'Seleziona un valore',
    placeholder: 'Cerca...',
    errorMessage: 'Seleziona un valore valido',
    disabled: false,
    required: false,
    options: [
      { value: 'option1', label: 'option1' },
      { value: 'option2', label: 'option2' },
      { value: 'option3', label: 'option3' },
    ],
  },
};
export const Secondary: Story = {
  name: 'Disabled',
  args: {
    id: 'select-autocomplete',
    label: 'Seleziona un valore',
    placeholder: 'Cerca...',
    errorMessage: 'Seleziona un valore valido',
    disabled: true,
    required: false,
    options: [
      { value: 'option1', label: 'Label' },
      { value: 'option2', label: 'Label' },
      { value: 'option3', label: 'Label' },
    ],
  },
};
