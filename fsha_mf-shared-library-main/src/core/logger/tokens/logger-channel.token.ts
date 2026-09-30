import { InjectionToken } from '@angular/core';
import { LoggerChannelInterface } from '../types/logger-channel-interface';

export const LOGGER_CHANNEL = new InjectionToken<LoggerChannelInterface>('LOGGER_CHANNELS_TOKEN');
