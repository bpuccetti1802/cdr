import { Meta, StoryObj, moduleMetadata } from '@storybook/angular';
import { StepperComponent, ProgressIndicatorEnum } from './stepper.component';
import { Component, TemplateRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  template: `
    <ng-template #step1><div>Passo 1: Informazioni personali</div></ng-template>
    <ng-template #step2><div>Passo 2: Indirizzo</div></ng-template>
    <ng-template #step3><div>Passo 3: Conferma</div></ng-template>
  `,
  standalone: true,
})
class TemplateHolderComponent {
  @ViewChild('step1', { static: true }) step1!: TemplateRef<unknown>;
  @ViewChild('step2', { static: true }) step2!: TemplateRef<unknown>;
  @ViewChild('step3', { static: true }) step3!: TemplateRef<unknown>;
}

const meta: Meta<StepperComponent> = {
  title: 'Componenti/Stepper',
  component: StepperComponent,
  decorators: [
    moduleMetadata({
      imports: [CommonModule, TemplateHolderComponent],
    }),
  ],
  argTypes: {
    progressIndicatorProps: {
      control: { type: 'select' },
      options: [ProgressIndicatorEnum.bar, ProgressIndicatorEnum.dots],
      mapping: {
        [ProgressIndicatorEnum.bar]: {
          type: ProgressIndicatorEnum.bar,
          barProps: { showRatio: true, showPercentage: true },
        },
        [ProgressIndicatorEnum.dots]: {
          type: ProgressIndicatorEnum.dots,
          dotsProps: { showRatio: false, showPercentage: false },
        },
      },
    },
  },
};

export default meta;
type Story = StoryObj<StepperComponent>;

export const BarStepper: Story = {
  render: (arguments_) => ({
    props: arguments_,
    template: `
      <app-stepper
        [steps]="steps"
        [progressIndicatorProps]="progressIndicatorProps"
        [actionProps]="actionProps"
      ></app-stepper>
    `,
    component: TemplateHolderComponent,
    setup: (component: TemplateHolderComponent) => {
      return {
        steps: [
          { slot: 1, percent: 33, templateRef: component.step1 },
          { slot: 2, percent: 33, templateRef: component.step2 },
          { slot: 3, percent: 34, templateRef: component.step3 },
        ],
      };
    },
  }),
  args: {
    progressIndicatorProps: {
      type: ProgressIndicatorEnum.bar,
      barProps: {
        showRatio: true,
        showPercentage: true,
      },
    },
    actionProps: {
      backButton: { label: 'Indietro', onClick: () => Promise.resolve() },
      forwardButton: { label: 'Avanti', onClick: () => Promise.resolve() },
    },
  },
};

export const DotsStepper: Story = {
  ...BarStepper,
  args: {
    progressIndicatorProps: {
      type: ProgressIndicatorEnum.dots,
      dotsProps: {
        showRatio: false,
        showPercentage: false,
      },
    },
    actionProps: {
      backButton: { label: 'Indietro', onClick: () => Promise.resolve() },
      forwardButton: { label: 'Avanti', onClick: () => Promise.resolve() },
    },
  },
};

export const CustomLabels: Story = {
  ...BarStepper,
  args: {
    progressIndicatorProps: {
      type: ProgressIndicatorEnum.bar,
      barProps: {
        showRatio: false,
        showPercentage: true,
      },
    },
    actionProps: {
      backButton: { label: 'Torna indietro', onClick: () => Promise.resolve() },
      forwardButton: { label: 'Procedi', onClick: () => Promise.resolve() },
    },
  },
};

export const DisabledButtons: Story = {
  ...BarStepper,
  args: {
    progressIndicatorProps: {
      type: ProgressIndicatorEnum.bar,
      barProps: {
        showRatio: true,
        showPercentage: true,
      },
    },
    actionProps: {
      backButton: { label: 'Indietro', onClick: () => Promise.resolve(), disabled: true },
      forwardButton: { label: 'Avanti', onClick: () => Promise.resolve(), disabled: true },
    },
  },
};

export const NoContent: Story = {
  render: (arguments_) => ({
    props: arguments_,
    template: `
      <app-stepper
        [steps]="steps"
        [progressIndicatorProps]="progressIndicatorProps"
        [actionProps]="actionProps"
      ></app-stepper>
    `,
    setup: () => {
      return {
        steps: [],
      };
    },
  }),
  args: {
    progressIndicatorProps: {
      type: ProgressIndicatorEnum.bar,
      barProps: {
        showRatio: true,
        showPercentage: true,
      },
    },
    actionProps: {
      backButton: { label: 'Indietro', onClick: () => Promise.resolve() },
      forwardButton: { label: 'Avanti', onClick: () => Promise.resolve() },
    },
  },
};
