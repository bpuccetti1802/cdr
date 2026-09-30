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
  selector: 'app-doughnut-chart',
  templateUrl: '../chart.component.html',
  standalone: true,
})
export class DoughnutChartComponent
  extends AbstractChartComponent<'doughnut'>
  implements AfterViewInit, OnChanges
{
  protected readonly type = 'doughnut' as const;

  @ViewChild('chartCanvas')
  declare chartCanvas: ElementRef<HTMLCanvasElement>;

  declare chart: Chart<'doughnut'>;

  @Input()
  override data: ChartData<'doughnut'> = {
    labels: ['Red', 'Blue', 'Yellow'],
    datasets: [
      {
        label: 'My First Dataset',
        data: [300, 50, 100],
        backgroundColor: ['rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 205, 86)'],
        hoverOffset: 6,
      },
    ],
  };

  @Input()
  override options: ChartOptions<'doughnut'> = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '70%',
    plugins: {
      legend: {
        position: 'bottom',
      },
      tooltip: {
        enabled: true,
      },
    },
    animation: {
      animateRotate: true,
      animateScale: true,
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
      type: 'doughnut',
      data: this.data,
      options: this.options,
    });
  }
}
