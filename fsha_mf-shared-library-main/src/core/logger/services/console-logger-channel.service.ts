/* eslint-disable no-restricted-syntax */
/* eslint-disable no-console */
import { Injectable } from '@angular/core';
import { LoggerArguments } from '../types/logger-arguments';
import { LoggerChannelInterface } from '../types/logger-channel-interface';

@Injectable()
export class ConsoleLoggerChannel implements LoggerChannelInterface {
  /**
   * @inheritDoc
   */
  log(message?: string, ...arguments_: LoggerArguments[]): void {
    console.log(message, ...arguments_);
  }

  /**
   * @inheritDoc
   */
  debug(message?: string, ...arguments_: LoggerArguments[]): void {
    console.debug(message, ...arguments_);
  }

  /**
   * @inheritDoc
   */
  info(message?: string, ...arguments_: LoggerArguments[]): void {
    console.info(message, ...arguments_);
  }

  /**
   * @inheritDoc
   */
  warn(message?: string, ...arguments_: LoggerArguments[]): void {
    console.warn(message, ...arguments_);
  }

  /**
   * @inheritDoc
   */
  error(message?: string, ...arguments_: LoggerArguments[]): void {
    console.error(message, ...arguments_);
  }
}
