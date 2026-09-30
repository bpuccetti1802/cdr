import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'replaceSlashes' })
export class ReplaceSlashesPipe implements PipeTransform {
  transform(value: string): string {
    return value.replaceAll('/', '-');
  }
}
