import type { Meta, StoryObj } from '@storybook/angular';
import { CheckboxTableComponent } from './checkbox-table.component';

interface TableColumns {
  id: keyof unknown;
  label: string;
  selectable?: boolean;
}
interface BaseRow {
  id: string | string;
}

const meta: Meta<CheckboxTableComponent<BaseRow>> = {
  title: 'Components/CheckboxTable',
  component: CheckboxTableComponent,
  tags: ['autodocs'],
  args: {
    columns: [
      { id: 'selezione', label: '', selectable: true },
      { id: 'name', label: 'Nome' },
      { id: 'age', label: 'Età' },
      { id: 'city', label: 'Città' },
    ] as TableColumns[], // ⬅️ Specifica il tipo esplicitamente
    data: [
      { id: '1', name: 'Mario Rossi', age: 30, city: 'Roma' },
      { id: '2', name: 'Luca Bianchi', age: 25, city: 'Milano' },
      { id: '3', name: 'Giulia Verdi', age: 28, city: 'Napoli' },
      { id: '4', name: 'Anna Neri', age: 32, city: 'Firenze' },
      { id: '5', name: 'Paolo Gialli', age: 40, city: 'Torino' },
      { id: '6', name: 'Sara Blu', age: 35, city: 'Bologna' },
    ] as unknown as BaseRow[],
    itemsPerPage: 5,
    currentPage: 1,
    cardWrapper: true,
  },
};

export default meta;
type Story = StoryObj<CheckboxTableComponent<BaseRow>>;

// Tabella di default
export const Default: Story = {
  name: 'Default Table',
};

// Tabella senza card wrapper
export const NoWrapper: Story = {
  args: {
    cardWrapper: false,
  },
};
