import { provideHttpClient } from '@angular/common/http';
import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideAnimations } from '@angular/platform-browser/animations';
import { provideRouter } from '@angular/router';
import { provideQuillConfig } from 'ngx-quill';
export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideQuillConfig({
      customOptions: [
        {
          import: 'formats/font',
          whitelist: ['mirza', 'roboto', 'aref', 'serif', 'sansserif', 'monospace'],
        },
      ],
      modules: {},
    }), // text direction
    provideHttpClient(),
    provideAnimations(),
    provideRouter([]),
  ],
};
