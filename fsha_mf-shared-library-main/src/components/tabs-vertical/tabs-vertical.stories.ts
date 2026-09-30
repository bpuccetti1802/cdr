import { moduleMetadata, Meta, StoryObj } from '@storybook/angular';
import { TabsVerticalComponent } from './tabs-vertical.component';
import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

// Componenti fittizi per i tab
@Component({
  selector: 'app-mock-tab1',
  template: `<div class="p-3 border">Contenuto Tab 1</div>`,
})
class MockTab1Component {}

@Component({
  selector: 'app-mock-tab2',
  template: `<div class="p-3 border">Contenuto Tab 2</div>`,
})
class MockTab2Component {}

@Component({
  selector: 'app-mock-tab3',
  template: `<div class="p-3 border">Contenuto Tab 3</div>`,
})
class MockTab3Component {}

const meta: Meta<TabsVerticalComponent> = {
  title: 'Components/TabsVertical',
  component: TabsVerticalComponent,
  decorators: [
    moduleMetadata({
      declarations: [MockTab1Component, MockTab2Component, MockTab3Component],
      imports: [CommonModule],
    }),
  ],
  tags: ['autodocs'],
};
export default meta;

type Story = StoryObj<TabsVerticalComponent>;

export const Default: Story = {
  args: {
    tabs: [
      { label: 'Tab 1', link: 'tab1', component: MockTab1Component },
      { label: 'Tab 2', link: 'tab2', component: MockTab2Component },
      { label: 'Tab 3', link: 'tab3', component: MockTab3Component },
    ],
  },
};
