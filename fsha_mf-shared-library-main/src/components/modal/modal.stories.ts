import type { Meta, StoryObj } from '@storybook/angular';
import { ModalComponent } from './modal.component';
import { Component } from '@angular/core';

const meta: Meta<ModalComponent> = {
  title: 'Components/Modal',
  component: ModalComponent,
  tags: ['autodocs'],
  argTypes: {
    open: { control: 'boolean' },
    titleContent: { control: 'text' },
    size: { control: 'radio', options: ['sm', 'md', 'lg', 'xl'] },
  },
};

export default meta;
type Story = StoryObj<ModalComponent>;

//  Componente placeholder per il corpo della modale
@Component({
  selector: 'app-modal-content',
  template: `<p>Questo è il contenuto della modale.</p>`,
  standalone: true,
})
class ModalContentComponent {}

// 📌 Componente placeholder per il footer
@Component({
  selector: 'app-modal-footer',
  template: `<button type="button" class="btn btn-primary">Azione</button>`,
  standalone: true,
})
class ModalFooterComponent {}

// 📌 Modal di Default
export const Default: Story = {
  name: 'Modal Base',
  args: {
    open: true,
    titleContent: 'Titolo Modale',
    size: 'lg',
    close: () => console.log('Modal chiusa'),
  },
};

// 📌 Modal con contenuto e footer dinamici
export const WithContentAndFooter: Story = {
  name: 'Modal con Contenuto e Footer',
  args: {
    ...Default.args,
    contentComponent: ModalContentComponent,
    footerComponent: ModalFooterComponent,
  },
};
