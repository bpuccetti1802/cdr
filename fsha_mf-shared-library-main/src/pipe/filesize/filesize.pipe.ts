import { Pipe, PipeTransform } from '@angular/core';
import { filesize, FileSizeOptionsString } from 'filesize';

@Pipe({
  name: 'filesize',
})
export class FileSizePipe implements PipeTransform {
  private static transformOne(value: number, options?: FileSizeOptionsString): string {
    return filesize(value, options);
  }

  transform(value: number | number[], options?: FileSizeOptionsString) {
    if (Array.isArray(value)) {
      return value.map((value_) => FileSizePipe.transformOne(value_, options));
    }

    return FileSizePipe.transformOne(value, options);
  }
}
