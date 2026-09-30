/* eslint-disable storybook/no-redundant-story-name */
import type { Meta, StoryObj } from '@storybook/angular';
import { UploadComponent } from './upload.component';

const meta: Meta<UploadComponent> = {
  title: 'Components/Upload',
  component: UploadComponent,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<UploadComponent>;

export const Default: Story = {
  name: 'Default Upload',
  args: {
    label: 'Carica un file',
    accept: '*/*',
    multiple: false,
    files: [],
    required: false,
  },
};

export const MultipleFiles: Story = {
  name: 'Some Files',
  args: {
    label: 'Carica più file',
    accept: 'image/*',
    multiple: true,
    files: [],
    required: false,
  },
};

export const PreloadedFiles: Story = {
  name: 'Pre-loaded Files',
  args: {
    label: 'File già caricati',
    multiple: false,
    files: [new File([''], 'documento.pdf', { type: 'application/pdf' })],
    required: false,
  },
};
