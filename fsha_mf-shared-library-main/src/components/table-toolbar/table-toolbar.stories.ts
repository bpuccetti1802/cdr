import { moduleMetadata, Meta, StoryObj } from '@storybook/angular';
import { TableToolbarComponent } from './table-toolbar.component';
import { CommonModule } from '@angular/common';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { Component, EventEmitter, Output } from '@angular/core';

// Componenti fittizi per la Storybook
@Component({
  selector: 'app-mock-button',
  template: `<button type="button" class="btn btn-primary" (click)="buttonClick.emit()">
    Aggiungi
  </button>`,
})
class MockButtonComponent {
  @Output() buttonClick = new EventEmitter<void>();
}

@Component({
  selector: 'app-mock-search',
  template: `<input type="text" class="form-control" placeholder="Cerca..." />`,
})
class MockSearchComponent {}

@Component({
  selector: 'app-mock-filter',
  template: `<button type="button" class="btn btn-secondary" (click)="buttonClick.emit()">
    Filtra
  </button>`,
})
class MockFilterComponent {
  @Output() buttonClick = new EventEmitter<void>();
}

const meta: Meta<TableToolbarComponent> = {
  title: 'Components/TableToolbar',
  component: TableToolbarComponent,
  decorators: [
    moduleMetadata({
      declarations: [MockButtonComponent, MockSearchComponent, MockFilterComponent],
      imports: [CommonModule, FontAwesomeModule],
    }),
  ],
  tags: ['autodocs'],
  argTypes: {
    onClickButton: { action: 'button clicked' },
    onClickFilter: { action: 'filter clicked' },
  },
};
export default meta;

type Story = StoryObj<TableToolbarComponent>;

export const Default: Story = {
  args: {
    searchComponent: MockSearchComponent,
    buttonComponent: MockButtonComponent,
    filterComponent: MockFilterComponent,
    cardWrapper: true,
  },
};

export const WithoutCardWrapper: Story = {
  args: {
    ...Default.args,
    cardWrapper: false,
  },
};
