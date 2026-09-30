import { CommonModule } from '@angular/common';
import { AfterContentInit, Component, TemplateRef, Input } from '@angular/core';

export enum ProgressIndicatorEnum {
  dots = 'dots',
  bar = 'bar',
}

interface ProgressIndicatorProperties {
  showRatio: boolean;
  showPercentage: boolean;
}

interface ButtonProperties {
  label: string;
  onClick: (step: number, currentIndex?: number) => Promise<unknown>;
  disabled?: boolean;
}

type DotsIndicatorProperties = ProgressIndicatorProperties & { percentageLabel?: string };
type BarIndicatorProperties = ProgressIndicatorProperties & { ratioLabel?: string };

type BackActionProperties = ButtonProperties & { percentageLabel?: string };
type ForwardActionProperties = ButtonProperties & { ratioLabel?: string };

type ActionProperties = {
  backButton?: BackActionProperties;
  forwardButton?: ForwardActionProperties;
};

type ProgressIndicatorPropertiesType =
  | {
      barProps?: BarIndicatorProperties;
      type?: ProgressIndicatorEnum.bar;
    }
  | {
      dotsProps?: DotsIndicatorProperties;
      type?: ProgressIndicatorEnum.dots;
    };

@Component({
  selector: 'app-stepper',
  templateUrl: './stepper.component.html',
  imports: [CommonModule],
  standalone: true,
})
export class StepperComponent implements AfterContentInit {
  @Input() steps: { slot: number; percent: number; templateRef: TemplateRef<unknown> }[] = [];
  @Input() slotIndex!: number;
  @Input() dynamicPercentage = false;
  @Input() progressIndicatorProps: ProgressIndicatorPropertiesType = {
    type: ProgressIndicatorEnum.bar,
    barProps: {
      showRatio: true,
      showPercentage: true,
    },
  };
  @Input() actionProps: ActionProperties = {
    forwardButton: {
      label: '',
      onClick: () => new Promise(() => {}),
      disabled: false,
    },
  };
  @Input() controlled: boolean = false;
  get isBarType(): boolean {
    return this.progressIndicatorProps?.type === ProgressIndicatorEnum.bar;
  }

  get isDotsType(): boolean {
    return this.progressIndicatorProps?.type === ProgressIndicatorEnum.dots;
  }

  get showPercentage(): boolean | undefined {
    return this.progressIndicatorProps?.type === ProgressIndicatorEnum.dots
      ? this.progressIndicatorProps.dotsProps?.showPercentage
      : this.progressIndicatorProps?.type === ProgressIndicatorEnum.bar
        ? this.progressIndicatorProps.barProps?.showPercentage
        : false;
  }

  get showRatio() {
    if (this.progressIndicatorProps?.type === ProgressIndicatorEnum.dots) {
      return this.progressIndicatorProps.dotsProps?.showRatio;
    } else if (this.progressIndicatorProps?.type === ProgressIndicatorEnum.bar) {
      return this.progressIndicatorProps.barProps?.showRatio;
    } else {
      return false;
    }
  }

  templates!: { slot: number; percent: number; templateRef: TemplateRef<unknown> }[];

  ngAfterContentInit() {
    this.templates = this.steps
      ? this.steps.map((step) => ({
          percent: step.percent,
          slot: step.slot,
          templateRef: step.templateRef,
        }))
      : [];
    this.templates.sort((a, b) => a.slot - b.slot);
    if (!this.controlled) {
      this.slotIndex = this.templates[0]?.slot;
    }
  }

  get percentageSum(): number {
    return this.templates
      .filter((t) => t.slot <= this.slotIndex)
      .reduce((accumulator, t) => t.percent + accumulator, 0);
  }

  get currentIndex(): number {
    return this.templates.findIndex((t) => t.slot === this.slotIndex);
  }

  async back() {
    if (this.actionProps.backButton) {
      try {
        await this.actionProps.backButton.onClick(this.currentIndex, this.slotIndex);

        if (this.currentIndex > 0) {
          this.slotIndex = this.templates[this.currentIndex - 1].slot;
        }
      } catch (error) {
        console.error('Errore durante il back:', error);
      }
    }
  }

  async forward() {
    if (this.actionProps.forwardButton) {
      try {
        await this.actionProps.forwardButton.onClick(this.currentIndex, this.slotIndex);
        if (this.currentIndex < this.templates.length - 1) {
          this.slotIndex = this.templates[this.currentIndex + 1].slot;
        }
      } catch (error) {
        console.error('Errore durante il forward:', error);
      }
    }
  }

  trackByTemplate(_: number, template: { slot: number; templateRef: unknown }): number {
    return template.slot;
  }

  get progressBarWidthClass(): string {
    const width = Math.min(100, Math.max(0, Math.round(this.percentageSum)));
    return `progress-width-${width}`;
  }
}
