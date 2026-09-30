import { Meta, StoryObj, applicationConfig } from '@storybook/angular';
import { FileNotFoundComponent } from './file-not-found.component';
import { provideRouter, withHashLocation } from '@angular/router';

const meta: Meta<FileNotFoundComponent> = {
  title: 'Components/File Not Found',
  component: FileNotFoundComponent,
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

type Story = StoryObj<FileNotFoundComponent>;

export const Default: Story = {};
