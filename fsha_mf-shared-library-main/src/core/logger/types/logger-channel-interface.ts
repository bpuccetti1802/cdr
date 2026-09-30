import { LoggerArguments } from './logger-arguments';

/**
 * Defines a generic channel to physically write a log.
 */
export interface LoggerChannelInterface {
  /**
   * Writes a message with the LOG level.
   */
  log(message?: string, ...arguments_: LoggerArguments[]): void;
  /**
   * Writes a message with the DEBUG level.
   */
  debug(message?: string, ...arguments_: LoggerArguments[]): void;
  /**
   * Writes a message with the DEBUG level.
   */
  info(message?: string, ...arguments_: LoggerArguments[]): void;
  /**
   * Writes a message with the WARN level.
   */
  warn(message?: string, ...arguments_: LoggerArguments[]): void;
  /**
   * Writes a message with the ERROR level.
   */
  error(message?: string, ...arguments_: LoggerArguments[]): void;
}
