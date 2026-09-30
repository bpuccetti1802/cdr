import { HttpClientModule } from '@angular/common/http';
import { moduleMetadata, Meta, StoryObj } from '@storybook/angular';
import { AccordionComponent } from './accordion.component';
import { CommonModule } from '@angular/common';

const meta: Meta<AccordionComponent> = {
  title: 'Components/Accordion',
  component: AccordionComponent,
  decorators: [
    moduleMetadata({
      imports: [CommonModule, HttpClientModule],
    }),
  ],
  tags: ['autodocs'],
  argTypes: {
    expanded: {
      control: 'boolean',
    },
  },
};
export default meta;

type Story = StoryObj<AccordionComponent>;

export const Default: Story = {
  args: {
    title: 'Accordion Title',
    id: 'example1',
    expanded: false,
  },
  render: (arguments_) => ({
    props: arguments_,
    template: `
      <app-rc-accordion [title]="title" [id]="id" [expanded]="expanded">
        <ng-content><p>Questo è il primo contenuto dell'accordion.</p></ng-content>
        <ng-content><p>Questo è il secondo contenuto dell'accordion.</p></ng-content>
      </app-rc-accordion>
    `,
  }),
};

export const Expanded: Story = {
  args: {
    title: 'Expanded Accordion',
    id: 'example2',
    expanded: true,
  },
  render: (arguments_) => ({
    props: arguments_,
    template: `
      <app-rc-accordion [title]="title" [id]="id" [expanded]="expanded">
           <ng-content><p>Questo è il primo contenuto dell'accordion.</p></ng-content>
        <ng-content><p>Questo è il secondo contenuto dell'accordion.</p></ng-content>
      </app-rc-accordion>
    `,
  }),
};
