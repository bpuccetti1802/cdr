import type { Meta, StoryObj } from '@storybook/angular';
import { NotificationToastComponent } from './notification-toast.component';
import { ToastTypes } from 'test-library-frankmd93';

const meta: Meta<NotificationToastComponent> = {
  title: 'Components/Notification Toast',
  component: NotificationToastComponent,
  tags: ['autodocs'],
  argTypes: {
    openNotification: { control: 'boolean' },
    toastType: {
      control: 'select',
      options: Object.values(ToastTypes),
    },
    titleContent: { control: 'text' },
    message: { control: 'text' },
  },
};

export default meta;
type Story = StoryObj<NotificationToastComponent>;

// 📌 Notifica di Successo
export const Success: Story = {
  name: 'success',
  args: {
    openNotification: true,
    toastType: ToastTypes.SUCCESS,
    titleContent: 'Successo!',
    message: "L'operazione è stata completata con successo.",
  },
};

// 📌 Notifica di Errore
export const Error: Story = {
  name: 'error',
  args: {
    openNotification: true,
    toastType: ToastTypes.ERROR,
    titleContent: 'Errore!',
    message: "Si è verificato un errore durante l'operazione.",
  },
};

// 📌 Notifica di Informazione
export const Info: Story = {
  name: 'info',
  args: {
    openNotification: true,
    toastType: ToastTypes.INFO,
    titleContent: 'Informazione',
    message: 'Ecco un messaggio informativo.',
  },
};

// 📌 Notifica di Avviso
export const Warning: Story = {
  name: 'warning',
  args: {
    openNotification: true,
    toastType: ToastTypes.WARNING,
    titleContent: 'Attenzione!',
    message: 'Fai attenzione a questa operazione.',
  },
};
