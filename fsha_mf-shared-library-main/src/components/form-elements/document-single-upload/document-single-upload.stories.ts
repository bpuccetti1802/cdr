import { Meta, StoryObj, moduleMetadata } from '@storybook/angular';
import { ReactiveFormsModule, FormControl } from '@angular/forms';
import { DocumentSingleUploadComponent } from './document-single-upload.component';
import { HttpClientModule } from '@angular/common/http';

const meta: Meta<DocumentSingleUploadComponent> = {
  title: 'Componenti/DocumentSingleUpload',
  component: DocumentSingleUploadComponent,
  decorators: [
    moduleMetadata({
      imports: [ReactiveFormsModule, HttpClientModule],
    }),
  ],
  tags: ['autodocs'],

  render: (arguments_) => ({
    props: {
      ...arguments_,
      formControl: arguments_.formControl || new FormControl(null),
    },
  }),

  args: {
    id: 'fileInputId',
    note: 'File obbligatorio. che richiede firma digitale.',
    descrizione: 'Descrizione',
    uploadedFileNote: 'File obbligatorio.',
    formControl: new FormControl(null),
  },
};

export default meta;

export const Default: StoryObj<DocumentSingleUploadComponent> = {};
