import { HttpClientModule } from '@angular/common/http';
import { moduleMetadata, type Meta, type StoryObj } from '@storybook/angular';
import { IconComponent } from './icon.component';

const meta: Meta<IconComponent> = {
  title: 'Components/Icon',
  component: IconComponent,
  tags: ['autodocs'],
  decorators: [
    moduleMetadata({
      imports: [HttpClientModule],
    }),
  ],
};

export default meta;
type Story = StoryObj<IconComponent>;

export const BootstrapIcon: Story = {
  name: 'IconComponent',
  args: {
    name: 'it-check-circle',
    color: 'blue',
  },
};
