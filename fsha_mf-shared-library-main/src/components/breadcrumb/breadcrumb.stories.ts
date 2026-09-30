import { Meta, StoryObj, moduleMetadata } from '@storybook/angular';
import { BreadcrumbComponent } from './breadcrumb.component';
import { CommonModule } from '@angular/common';
import { RouterTestingModule } from '@angular/router/testing';
import { ActivatedRoute, Routes, Router, NavigationEnd } from '@angular/router';
import { Component } from '@angular/core';
import { of, Subject } from 'rxjs';
import { DataRoute } from 'test-library-frankmd93';

// Componente fittizio per le rotte
@Component({ template: '<div>Route Content</div>' })
class DummyComponent {}

// Rotte di esempio
const routes: Routes = [
  {
    path: 'sezione',
    component: DummyComponent,
    data: { label: 'Sezione' } as DataRoute,
    children: [
      {
        path: 'pagina-attuale',
        component: DummyComponent,
        data: { label: 'Pagina Attuale' } as DataRoute,
      },
    ],
  },
  {
    path: 'home',
    component: DummyComponent,
    data: { label: 'Home' } as DataRoute,
  },
];

// Mock avanzato di ActivatedRoute con struttura nidificata
const mockActivatedRoute = {
  root: {
    children: [
      {
        routeConfig: {
          path: 'home',
          data: { label: 'Home' },
        },
        children: [
          {
            routeConfig: {
              path: 'sezione',
              data: { label: 'Sezione' },
            },
            children: [],
          },
        ],
      },
    ],
  },
  snapshot: {
    data: {},
  },
  params: of({}),
  queryParams: of({}),
  children: [],
};

// Mock del Router con eventi di navigazione
const mockRouter = {
  events: new Subject(),
  navigate: () => {},
};

const meta: Meta<BreadcrumbComponent> = {
  title: 'Components/Breadcrumb',
  component: BreadcrumbComponent,
  decorators: [
    moduleMetadata({
      imports: [CommonModule, RouterTestingModule.withRoutes(routes)],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: mockActivatedRoute,
        },
        {
          provide: Router,
          useValue: mockRouter,
        },
      ],
    }),
  ],
};

export default meta;
type Story = StoryObj<BreadcrumbComponent>;

export const Default: Story = {
  render: () => {
    setTimeout(() => {
      mockRouter.events.next(
        new NavigationEnd(1, '/sezione/pagina-attuale', '/sezione/pagina-attuale'),
      );
    }, 500);

    return {
      template: `<router-outlet></router-outlet><app-mf-breadcrumb></app-mf-breadcrumb>`,
    };
  },
};
