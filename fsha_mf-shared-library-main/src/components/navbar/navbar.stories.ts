import { moduleMetadata, type Meta, type StoryObj } from '@storybook/angular';
import { NavbarComponent } from './navbar.component';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';
import { NavbarItem } from 'test-library-frankmd93';

const meta: Meta<NavbarComponent> = {
  title: 'Components/Navbar',
  component: NavbarComponent,
  tags: ['autodocs'],
  argTypes: {
    menuItems: {
      control: 'object',
      description: 'Lista di elementi del menu',
    },
    // activeRoute: { control: 'text' },
  },
  decorators: [
    moduleMetadata({
      providers: [
        {
          provide: ActivatedRoute,
          useValue: { params: of({}), queryParams: of({}) }, // Mock dei parametri
        },
      ],
    }),
  ],
};

export default meta;
type Story = StoryObj<NavbarComponent>;

export const Default: Story = {
  name: 'Navbar Base',
  args: {
    // activeRoute: '/home',
    menuItems: [
      {
        hasChildren: true,
        label: 'Home',
        route: '/home',
        children: [
          {
            hasChildren: false,
            label: 'SubPage 1',
            data: {
              label: 'SubPage 1',
            },
            route: '/home/sub1',
          },
          {
            hasChildren: false,
            label: 'SubPage 2',
            data: {
              label: 'SubPage 2',
            },
            route: '/home/sub2',
          },
        ],
      },
      {
        hasChildren: false,
        label: 'About',
        route: '/about',
      },
    ] as NavbarItem[],
  },
};
