import { Meta, StoryObj, applicationConfig } from '@storybook/angular';
import { ErrorBoundaryComponent } from './error-boundary.component';
import { provideRouter, withHashLocation } from '@angular/router';

const meta: Meta<ErrorBoundaryComponent> = {
  title: 'Components/Error Boundary',
  component: ErrorBoundaryComponent,
  decorators: [
    applicationConfig({
      providers: [
        // The router is most likely going to interfere with your Storybook application/iframe
        // route, but hash routes should be fine, so I also add `withHashLocation`.
        provideRouter([], withHashLocation()),
      ],
    }),
  ],
  tags: ['autodocs'],
};
export default meta;

type Story = StoryObj<ErrorBoundaryComponent>;

export const Default: Story = {};
