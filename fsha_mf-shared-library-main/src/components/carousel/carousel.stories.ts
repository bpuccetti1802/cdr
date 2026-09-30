import { moduleMetadata, Meta, StoryObj } from '@storybook/angular';
import { CarouselComponent } from './carousel.component';
import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

// Componenti fittizi per i Slide
@Component({
  selector: 'app-mock-slide1',
  template: `<div class="p-3 border">Contenuto Slide 1</div>`,
})
class MockSlide1Component {}

@Component({
  selector: 'app-mock-slide2',
  template: `<div class="p-3 border">Contenuto Slide 2</div>`,
})
class MockSlide2Component {}

@Component({
  selector: 'app-mock-slide3',
  template: `<div class="p-3 border">Contenuto Slide 3</div>`,
})
class MockSlide3Component {}

const meta: Meta<CarouselComponent> = {
  title: 'Components/Carousel',
  component: CarouselComponent,
  decorators: [
    moduleMetadata({
      declarations: [MockSlide1Component, MockSlide2Component, MockSlide3Component],
      imports: [CommonModule],
    }),
  ],
  tags: ['autodocs'],
};
export default meta;

type Story = StoryObj<CarouselComponent>;

export const Default: Story = {
  args: {
    slides: [
      { index: 1, component: MockSlide1Component },
      { index: 2, component: MockSlide2Component },
      { index: 3, component: MockSlide3Component },
    ],
  },
};
