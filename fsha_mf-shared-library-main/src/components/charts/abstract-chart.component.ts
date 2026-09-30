import { ElementRef, Input, ViewChild, Component } from '@angular/core';
import { Chart, ChartData, ChartOptions, ChartTypeRegistry } from 'chart.js';

@Component({ selector: 'app-abstract-chart', templateUrl: './chart.component.html' })
export abstract class AbstractChartComponent<TType extends keyof ChartTypeRegistry> {
  /** Il tipo viene definito dal componente figlio (es: 'doughnut') */
  protected abstract readonly type: TType;

  @ViewChild('chartCanvas')
  chartCanvas!: ElementRef<HTMLCanvasElement>;

  chart!: Chart<TType>;

  @Input()
  data!: ChartData<TType>;

  @Input()
  options!: ChartOptions<TType>;
}
