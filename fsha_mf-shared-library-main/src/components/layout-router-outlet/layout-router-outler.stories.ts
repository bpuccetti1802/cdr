import { Meta, StoryObj, moduleMetadata } from '@storybook/angular';
import { LayoutRouterOutletComponent } from './layout-router-outlet.component';
import { CommonModule } from '@angular/common';
import { RouterTestingModule } from '@angular/router/testing';
import { ActivatedRoute, Routes } from '@angular/router';
import { NavigationButtonComponent } from '../navigation-button/navigation-button.component';
import { Component } from '@angular/core';
import { of } from 'rxjs';

@Component({
  selector: 'app-fake-router-outlet',
  template: `
    <div class="mock-router-container">
      <p>Contenuto fittizio del Router Outlet</p>
    </div>
  `,
})
class FakeRouterOutletComponent {}

@Component({
  template: '<div class="mock-child">Child Route Content</div>',
})
class ChildComponent {}

const routes: Routes = [
  {
    path: '',
    component: LayoutRouterOutletComponent,
    children: [
      {
        path: 'child1',
        component: ChildComponent,
        data: { label: 'Child 1', iconName: 'it-arrow-right' },
      },
      { path: 'child2', component: ChildComponent, data: { label: 'Child 2', iconName: '' } },
      { path: 'child3', component: ChildComponent, data: { label: 'Child 3', iconName: '' } },
    ],
  },
];

const mockActivatedRoute = {
  snapshot: {
    routeConfig: {
      children: routes[0].children,
    },
  },
  firstChild: {
    snapshot: {
      routeConfig: routes[0],
    },
  },
  params: of({}),
  queryParams: of({}),
};

const meta: Meta<LayoutRouterOutletComponent> = {
  title: 'Components/LayoutRouterOutlet',
  component: LayoutRouterOutletComponent,
  decorators: [
    moduleMetadata({
      imports: [CommonModule, RouterTestingModule.withRoutes(routes), NavigationButtonComponent],
      declarations: [FakeRouterOutletComponent, ChildComponent], // 👈 Dichiarato il mock
      providers: [
        {
          provide: ActivatedRoute,
          useValue: mockActivatedRoute,
        },
      ],
    }),
  ],
};

export default meta;
type Story = StoryObj<LayoutRouterOutletComponent>;

export const Primary: Story = {
  render: () => ({
    template: `
      <app-mf-layout-router-outlet></app-mf-layout-router-outlet>
      <app-fake-router-outlet></app-fake-router-outlet>
    `,
  }),
};
