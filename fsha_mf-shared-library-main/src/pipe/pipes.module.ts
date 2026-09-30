import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FileSizePipe } from './filesize/filesize.pipe';
import { ReplaceSlashesPipe } from './replace-slashes/replace-slashes.pipe';
import { PathArrayPipe } from './path-array/path-array.pipe';

@NgModule({
  declarations: [FileSizePipe, ReplaceSlashesPipe, PathArrayPipe],
  imports: [CommonModule],
  exports: [FileSizePipe, ReplaceSlashesPipe, PathArrayPipe],
})
export class PipesModule {}
