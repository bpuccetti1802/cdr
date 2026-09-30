import {
  AfterViewInit,
  Component,
  ElementRef,
  Input,
  OnChanges,
  SimpleChanges,
  ViewChild,
} from '@angular/core';
import { Chart, ChartData, ChartOptions, registerables } from 'chart.js';
import { AbstractChartComponent } from '../abstract-chart.component';

Chart.register(...registerables);

@Component({
  selector: 'app-stacked-bar-chart',
  templateUrl: '../chart.component.html',
  standalone: true,
})
export class StackedBarChartComponent
  extends AbstractChartComponent<'bar'>
  implements AfterViewInit, OnChanges
{
  protected readonly type = 'bar' as const;

  @ViewChild('chartCanvas')
  declare chartCanvas: ElementRef<HTMLCanvasElement>;

  declare chart: Chart<'bar'>;

  DATA_COUNT = 7;
  @Input()
  override data: ChartData<'bar'> = {
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
  };

  @Input()
  override options: ChartOptions<'bar'> = {
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
  };

  ngAfterViewInit(): void {
    this.createChart();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (this.chart && (changes['data'] || changes['options'])) {
      this.chart.data = this.data;
      this.chart.options = this.options;
      this.chart.update();
    }
  }

  private createChart(): void {
    const context = this.chartCanvas.nativeElement.getContext('2d');
    if (!context) return;

    this.chart = new Chart(context, {
      type: 'bar',
      data: this.data,
      options: this.options,
    });
  }
}
