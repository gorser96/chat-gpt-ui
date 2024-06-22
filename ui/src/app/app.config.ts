import { ApplicationConfig, InjectionToken, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient } from '@angular/common/http';
import { AppSettings } from './models/app.model';

export const APP_CONFIG = new InjectionToken<AppSettings>('app.config');
export const APP_DI_CONFIG: AppSettings = {
  apiBaseUrl: 'http://localhost:8000/api/',
};

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideAnimationsAsync(),
    provideHttpClient(),
    { provide: APP_CONFIG, useValue: APP_DI_CONFIG }
  ],
};
