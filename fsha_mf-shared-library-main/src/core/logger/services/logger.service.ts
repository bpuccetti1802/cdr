import { Injectable, Inject } from '@angular/core';
import { LoggerLevel } from '../enums/logger-level';
import { LOGGER_CHANNEL } from '../tokens/logger-channel.token';
import { LoggerArguments } from '../types/logger-arguments';
import { LoggerChannelInterface } from '../types/logger-channel-interface';
import { LOGGER_LEVEL } from './../tokens/logger-level.token';

@Injectable()
export class LoggerService {
  constructor(
    @Inject(LOGGER_LEVEL) readonly globalLevel: LoggerLevel,
    @Inject(LOGGER_CHANNEL) readonly channels: LoggerChannelInterface[],
  ) {}

  /**
   * @inheritDoc
   */
  log(message?: string, ...arguments_: LoggerArguments[]): void {
    if (this.isLogLevelDisallowed(LoggerLevel.log)) {
      return;
    }

    this.channels.forEach((channel: LoggerChannelInterface) => channel.log(message, ...arguments_));
  }

  /**
   * @inheritDoc
   */
  debug(message?: string, ...arguments_: LoggerArguments[]): void {
    if (this.isLogLevelDisallowed(LoggerLevel.debug)) {
      return;
    }

    this.channels.forEach((channel: LoggerChannelInterface) =>
      channel.debug(message, ...arguments_),
    );
  }

  /**
   * @inheritDoc
   */
  info(message?: string, ...arguments_: LoggerArguments[]): void {
    if (this.isLogLevelDisallowed(LoggerLevel.info)) {
      return;
    }

    this.channels.forEach((channel: LoggerChannelInterface) =>
      channel.info(message, ...arguments_),
    );
  }

  /**
   * @inheritDoc
   */
  warn(message?: string, ...arguments_: LoggerArguments[]): void {
    if (this.isLogLevelDisallowed(LoggerLevel.warn)) {
      return;
    }

    this.channels.forEach((channel: LoggerChannelInterface) =>
      channel.warn(message, ...arguments_),
    );
  }

  /**
   * @inheritDoc
   */
  error(message?: string, ...arguments_: LoggerArguments[]): void {
    if (this.isLogLevelDisallowed(LoggerLevel.error)) {
      return;
    }

    this.channels.forEach((channel: LoggerChannelInterface) =>
      channel.error(message, ...arguments_),
    );
  }

  /**
   * Determines if the provided log level is allowed.
   */
  private isLogLevelDisallowed(level: LoggerLevel): boolean {
    return this.globalLevel === LoggerLevel.off || level < this.globalLevel;
  }
}
