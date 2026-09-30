import type { Meta, StoryObj } from '@storybook/angular';
import { DoughnutChartComponent } from './doughnut-chart.component';
import { ChartData, ChartOptions } from 'chart.js';

const meta: Meta<DoughnutChartComponent> = {
  title: 'Components/DoughnutChart',
  component: DoughnutChartComponent,
  tags: ['autodocs'],
  args: {
    data: {
      labels: ['Red', 'Blue', 'Yellow'],
      datasets: [
        {
          label: 'My First Dataset',
          data: [300, 50, 100],
          backgroundColor: ['rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 205, 86)'],
          hoverOffset: 6,
        },
      ],
    } as ChartData<'doughnut'>,

    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '70%',
      plugins: {
        legend: { position: 'bottom' },
      },
    } as ChartOptions<'doughnut'>,
  },
};

export default meta;
type Story = StoryObj<DoughnutChartComponent>;

// Default
export const Default: Story = {};

// Foro grande
export const LargeCutout: Story = {
  args: {
    options: {
      cutout: '85%',
      plugins: {
        legend: { position: 'right' },
      },
    } as ChartOptions<'doughnut'>,
  },
};

// Dati custom
export const CustomData: Story = {
  args: {
    data: {
      labels: ['A', 'B', 'C', 'D'],
      datasets: [
        {
          data: [40, 25, 20, 15],
          backgroundColor: ['#4ade80', '#60a5fa', '#facc15', '#f87171'],
        },
      ],
    } as ChartData<'doughnut'>,
  },
};
