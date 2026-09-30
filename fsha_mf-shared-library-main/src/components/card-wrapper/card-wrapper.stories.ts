import { moduleMetadata, Meta, StoryObj } from '@storybook/angular';
import { CardWrapperComponent } from './card-wrapper.component';
import { CommonModule } from '@angular/common';

const meta: Meta<CardWrapperComponent> = {
  title: 'Components/Card Wrapper',
  component: CardWrapperComponent,
  decorators: [
    moduleMetadata({
      imports: [CommonModule],
    }),
  ],
  tags: ['autodocs'],
  argTypes: {
    width: {
      control: 'select',
      options: ['auto', 'medium', 'large', 'full'],
    },
  },
};
export default meta;

type Story = StoryObj<CardWrapperComponent>;

export const Default: Story = {
  args: {
    width: 'auto',
  },
  render: (arguments_) => ({
    props: arguments_,
    template: `<app-rc-card-wrapper [width]="width"> 
                 <ng-content><p>Default card content</p></ng-content>
               </app-rc-card-wrapper>`,
  }),
};

export const Large: Story = {
  args: {
    width: 'large',
  },
  render: (arguments_) => ({
    props: arguments_,
    template: `<app-rc-card-wrapper [width]="width"> 
    <ng-content>
                 <h3>Large Card</h3>
                 <p>Some larger content inside the card.</p></ng-content>
               </app-rc-card-wrapper>`,
  }),
};

export const FullWidth: Story = {
  args: {
    width: 'full',
  },
  render: (arguments_) => ({
    props: arguments_,
    template: `<app-rc-card-wrapper [width]="width"> 
    <ng-content>
                 <h3>Full Width Card</h3>
                 <p>This card spans the full width.</p>
                 </ng-content>
               </app-rc-card-wrapper>`,
  }),
};

export const MediumWidth: Story = {
  args: {
    width: 'medium',
  },
  render: (arguments_) => ({
    props: arguments_,
    template: `<app-rc-card-wrapper [width]="width"> 
    <ng-content>
                 <h3>Medium Width Card</h3>
                 <p>This card spans the medium width.</p>
                 </ng-content>
               </app-rc-card-wrapper>`,
  }),
};

export const AutoWidth: Story = {
  args: {
    width: 'auto',
  },
  render: (arguments_) => ({
    props: arguments_,
    template: `<app-rc-card-wrapper [width]="width"> 
    <ng-content>
                 <h3>Auto Width Card</h3>
                 <p>This card spans the auto width.</p>
                 </ng-content>
               </app-rc-card-wrapper>`,
  }),
};
