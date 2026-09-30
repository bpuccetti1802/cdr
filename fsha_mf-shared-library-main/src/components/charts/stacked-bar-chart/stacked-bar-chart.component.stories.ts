import type { Meta, StoryObj } from '@storybook/angular';
import { ChartData, ChartOptions } from 'chart.js';
import { StackedBarChartComponent } from './stacked-bar-chart.component';

const meta: Meta<StackedBarChartComponent> = {
  title: 'Components/StackedBarChart',
  component: StackedBarChartComponent,
  tags: ['autodocs'],
  args: {
    data: {
      labels: ['Gennaio', 'Febbraio', 'Marzo'],
      datasets: [
        {
          label: 'Dataset 1',
          data: [200, 37, -90],
          backgroundColor: 'rgb(255, 99, 132)',
        },
        {
          label: 'Dataset 2',
          data: [-50, 66, 43],
          backgroundColor: 'rgb(54, 162, 235)',
        },
        {
          label: 'Dataset 3',
          data: [40, 90, 122],
          backgroundColor: 'rgb(255, 205, 86)',
        },
      ],
    } as ChartData<'bar'>,

    options: {
      plugins: {
        title: {
          display: true,
          text: 'Chart.js Bar Chart - Stacked',
        },
      },
      responsive: true,
      scales: {
        x: {
          stacked: true,
        },
        y: {
          stacked: true,
        },
      },
    } as ChartOptions<'bar'>,
  },
};

export default meta;
type Story = StoryObj<StackedBarChartComponent>;

// Default
export const Default: Story = {};
