import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'pathArray' })
export class PathArrayPipe implements PipeTransform {
  transform(value: string): string[] {
    return value.split('/').filter(Boolean);
  }
}
