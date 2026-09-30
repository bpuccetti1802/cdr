import { Meta, StoryObj } from '@storybook/angular';
import { ReactiveFormsModule, FormControl } from '@angular/forms';
import { OtpComponent } from './otp.component';
import { moduleMetadata } from '@storybook/angular';

const meta: Meta<OtpComponent> = {
  title: 'Components/Otp',
  component: OtpComponent,
  decorators: [
    moduleMetadata({
      declarations: [],
      imports: [ReactiveFormsModule],
    }),
  ],
  tags: ['autodocs'],
};

export default meta;

type Story = StoryObj<OtpComponent>;

export const Default: Story = {
  args: {
    id: 'otp-1',
    formControl: new FormControl(''),
  },
};
