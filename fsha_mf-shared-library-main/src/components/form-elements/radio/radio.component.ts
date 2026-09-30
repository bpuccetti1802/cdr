import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { RadioItem } from 'test-library-frankmd93';

@Component({
  selector: 'app-rc-radio',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './radio.component.html',
  styleUrls: ['./radio.component.scss'],
})
export class RadioComponent implements OnInit {
  @Input() id!: string;
  @Input() label: string | null = null;
  @Input() formControl!: FormControl;
  @Input() items: RadioItem[] = [];
  @Input() inline: boolean = true;
  @Input() disabled: boolean = false;
  @Input() onChange: (value: string) => void = () => {};
  @Input() required: boolean = false;

  ngOnInit(): void {
    // 🔹 Se required e nessun valore → seleziona il primo elemento
    if (this.required && !this.formControl.value && this.items.length > 0) {
      this.formControl.setValue(this.items[0].value);
    }
  }

  trackByValue(_: number, item: RadioItem): string {
    return this.id + item.value;
  }
}
