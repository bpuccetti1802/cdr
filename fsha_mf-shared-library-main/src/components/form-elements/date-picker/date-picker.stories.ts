import { Meta, StoryObj, moduleMetadata } from '@storybook/angular';
import { DatePickerComponent } from './date-picker.component';
import { FormControl, NG_VALUE_ACCESSOR, ReactiveFormsModule, Validators } from '@angular/forms';
import { PickerComponent } from '../picker/picker.component';
import { CommonModule } from '@angular/common';
import { MockValueAccessorDirective } from './control-value-accessor.mock';
import { MockPickerComponent } from './picker.mock';
import { forwardRef } from '@angular/core';
import { DateTime } from 'luxon';

const meta: Meta<DatePickerComponent> = {
  title: 'Components/DatePicker',
  component: DatePickerComponent,
  decorators: [
    moduleMetadata({
      imports: [
        ReactiveFormsModule,
        MockValueAccessorDirective,
        MockPickerComponent,
        PickerComponent,
        CommonModule,
      ],
      providers: [
        {
          provide: NG_VALUE_ACCESSOR,
          useExisting: forwardRef(() => MockValueAccessorDirective),
          multi: true,
        },
      ],
    }),
  ],
  argTypes: {
    formControl: { control: false },
    getErrorMessage: { control: false },
  },
};

export default meta;
type Story = StoryObj<DatePickerComponent>;

export const Default: Story = {
  args: {
    placeholder: 'Seleziona data e ora',
    date: DateTime.fromFormat('20/12/2024 10:30', 'dd/MM/yyyy HH:mm'),
    formControl: new FormControl(''),
    label: 'Data e Ora',
    width: '300px',
    class: 'custom-class',
    disabled: false,
    required: false,
    id: 'date-picker-id',
    getErrorMessage: (formControl: FormControl) => {
      if (formControl?.errors?.['required']) {
        return 'Questo campo è richiesto.';
      }
      return null;
    },
  },
  render: (arguments_) => ({
    props: {
      ...arguments_,
      refreshKey: arguments_.disabled ? 1 : 0,
    },
    template: `
      <app-rc-date-picker
        [formControl]="formControl"
        [placeholder]="placeholder"
        [date]="date"
        [label]="label"
        [width]="width"
        [class]="class"
        [disabled]="disabled"
        [id]="id"
        [getErrorMessage]="getErrorMessage"
        [refreshKey]="refreshKey"
      ></app-rc-date-picker>
    `,
  }),
};

export const Required: Story = {
  args: {
    ...Default.args,
    formControl: new FormControl('', { nonNullable: true, validators: [Validators.required] }),
    required: true,
  },
  render: (arguments_) => ({
    props: {
      ...arguments_,
      refreshKey: arguments_.disabled ? 1 : 0,
    },
    template: `
      <app-rc-date-picker
        [formControl]="formControl"
        [placeholder]="placeholder"
        [date]="date"
        [label]="label"
        [width]="width"
        [class]="class"
        [disabled]="disabled"
        [id]="id"
        [getErrorMessage]="getErrorMessage"
        [refreshKey]="refreshKey"
      ></app-rc-date-picker>
    `,
  }),
};

export const Disabled: Story = {
  args: {
    ...Default.args,
    disabled: true,
  },
  render: (arguments_) => ({
    props: {
      ...arguments_,
      refreshKey: arguments_.disabled ? 1 : 0,
    },
    template: `
      <app-rc-date-picker
        [formControl]="formControl"
        [placeholder]="placeholder"
        [date]="date"
        [label]="label"
        [width]="width"
        [class]="class"
        [disabled]="disabled"
        [id]="id"
        [getErrorMessage]="getErrorMessage"
        [refreshKey]="refreshKey"
      ></app-rc-date-picker>
    `,
  }),
};
