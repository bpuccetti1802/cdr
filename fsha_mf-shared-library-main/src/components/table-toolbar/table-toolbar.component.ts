import { CommonModule } from '@angular/common';
import { Component, Input, Type, Output, Injector, EventEmitter, OnInit } from '@angular/core';
import { CardWrapperComponent } from '../card-wrapper/card-wrapper.component';
import { faFilter } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

@Component({
  selector: 'app-rc-table-toolbar',
  standalone: true,
  imports: [CommonModule, CardWrapperComponent, FontAwesomeModule],
  templateUrl: './table-toolbar.component.html',
  styleUrls: ['./table-toolbar.component.scss'],
})
export class TableToolbarComponent implements OnInit {
  @Input() searchComponent: Type<unknown> | null = null;
  @Input() buttonComponent: Type<unknown> | null = null;
  @Input() filterComponent: Type<unknown> | null = null;
  @Input() onClickButton!: () => void;
  @Input() onClickFilter!: () => void;
  @Output() buttonCallback = new EventEmitter();
  @Output() filterCallback = new EventEmitter();
  @Output() searchCallback = new EventEmitter();
  @Input() cardWrapper: boolean = true;

  faFilter = faFilter;
  buttonAddInjector!: Injector;
  filterInjector!: Injector;
  searchInjector!: Injector;

  ngOnInit(): void {
    this.buttonAddInjector = Injector.create({
      providers: [{ provide: 'buttonAdd', useValue: () => this.onButtonCallback() }],
    });
    this.filterInjector = Injector.create({
      providers: [{ provide: 'filter', useValue: () => this.onFilterCallback() }],
    });
    this.searchInjector = Injector.create({
      providers: [
        { provide: 'search', useValue: (value: unknown) => this.onSearchCallback(value) },
      ],
    });
  }
  onButtonCallback(): void {
    this.buttonCallback.emit();
  }
  onFilterCallback(): void {
    this.filterCallback.emit();
  }
  onSearchCallback(value: unknown): void {
    this.searchCallback.emit(value);
  }

  handleClickFilter() {
    if (this.onClickFilter) {
      this.onClickFilter();
    }
  }
}
