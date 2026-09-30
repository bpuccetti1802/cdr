import { InjectionToken } from '@angular/core';
import { LoggerLevel } from '../enums/logger-level';

export const LOGGER_LEVEL = new InjectionToken<LoggerLevel>('LOGGER_LEVEL_TOKEN');
