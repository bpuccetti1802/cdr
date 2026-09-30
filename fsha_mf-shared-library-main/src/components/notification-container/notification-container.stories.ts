import type { Meta, StoryObj } from '@storybook/angular';
import { NotificationContainerComponent } from './notification-container.component';

const meta: Meta<NotificationContainerComponent> = {
  title: 'Components/NotificationContainer',
  component: NotificationContainerComponent,
  tags: ['autodocs'],
  argTypes: {},
};

export default meta;
type Story = StoryObj<NotificationContainerComponent>;

export const Default: Story = {
  name: 'default',
  args: {},
};
