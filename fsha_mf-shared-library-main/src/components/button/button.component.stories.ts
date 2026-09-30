import { HttpClientModule } from '@angular/common/http';
import { moduleMetadata, type Meta, type StoryObj } from '@storybook/angular';
import { ButtonComponent } from './button.component';
import { IconSize } from 'test-library-frankmd93';

const meta: Meta<ButtonComponent> = {
  title: 'Components/Icon',
  component: ButtonComponent,
  tags: ['autodocs'],
  decorators: [
    moduleMetadata({
      imports: [HttpClientModule],
    }),
  ],
};

export default meta;
type Story = StoryObj<ButtonComponent>;

export const Primary: Story = {
  name: 'ButtonComponent',
  args: {
    styleType: 'primary',
    buttonType: 'button',
    disabled: false,
    label: 'Bottone',
    iconName: '',
    iconColor: 'primary',
    iconSize: IconSize.sm,
    iconPosition: 'left',
  },
};

export const Secondary: Story = {
  name: 'ButtonComponent',
  args: {
    styleType: 'secondary',
    buttonType: 'button',
    disabled: false,
    label: 'Bottone',
    iconName: '',
    iconColor: 'primary',
    iconSize: IconSize.sm,
    iconPosition: 'left',
  },
};

export const Danger: Story = {
  name: 'ButtonComponent',
  args: {
    styleType: 'danger',
    buttonType: 'button',
    disabled: false,
    label: 'Bottone',
    iconName: '',
    iconColor: 'primary',
    iconSize: IconSize.sm,
    iconPosition: 'left',
  },
};

export const LeftIcon: Story = {
  name: 'ButtonComponent',
  args: {
    styleType: 'primary',
    buttonType: 'button',
    disabled: false,
    label: 'Bottone',
    iconName: 'fa-upload',
    iconColor: 'white',
    iconSize: IconSize.sm,
    iconPosition: 'left',
  },
};

export const RightIcon: Story = {
  name: 'ButtonComponent',
  args: {
    styleType: 'primary',
    buttonType: 'button',
    disabled: false,
    label: 'Bottone',
    iconName: 'fa-upload',
    iconColor: 'white',
    iconSize: IconSize.sm,
    iconPosition: 'right',
  },
};
