import { HttpClientModule } from '@angular/common/http';
import { moduleMetadata, type Meta, type StoryObj } from '@storybook/angular';
import { GridComponent } from './grid.component';

const meta: Meta<GridComponent> = {
  title: 'Components/Grid',
  component: GridComponent,
  tags: ['autodocs'],
  decorators: [
    moduleMetadata({
      imports: [HttpClientModule],
    }),
  ],
};

export default meta;
type Story = StoryObj<GridComponent>;

export const Default: Story = {
  name: 'GridComponent',
  args: {
    rows: 3,
    columns: 3,
    breakpoint: 'md',
    colClasses: undefined, // default 12/columns
    offsetClasses: [], // nessun offset
    cellTemplates: [
      ['testo 1', 'testo 2', 'testo 3'],
      ['testo 3', 'testo 1', 'testo 2'],
      ['testo 2', 'testo 3', 'testo 1'],
    ],
  },
};
