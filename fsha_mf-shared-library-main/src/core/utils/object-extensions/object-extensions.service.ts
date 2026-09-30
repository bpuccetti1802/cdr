import { Injectable } from '@angular/core';

/**
 * Provides a set of utilities method to interact with object-like values.
 */
@Injectable({ providedIn: 'root' })
export class ObjectExtensionsService {
  /**
   * Traverses the provided object to get the value bound
   * to the given path.
   */
  getObjectValue<T>(object: unknown, key?: string, defaultValue?: T): T {
    if (typeof key !== 'string') {
      return defaultValue as T;
    }

    if (typeof object !== 'object' || object === null) {
      return defaultValue as T;
    }

    // Splits the request key.
    let path = key.split('.');

    // Checks if it is an empty string.
    if (path.length === 0) {
      return defaultValue as T;
    }

    let data = object as Record<string, unknown>;

    let properties = Object.keys(data);

    // Reverses it to use the iterative algorithm. We use pop().
    path = path.reverse();

    // Iterates over the defined path.
    while (path.length > 0) {
      // Pop the path.
      const currentKey = path.pop();
      // Gets the data corresponding property of the current path.
      const currentProperty = properties.find((value: string) => currentKey === value);

      // If it doesn't exists return the default value.
      if (!currentProperty) {
        return defaultValue as T;
      }

      // Move a level down by getting the object of the next level.
      data = (data as Record<string, Record<string, unknown>>)[currentProperty];

      // If it is the last path we have, we are done.
      if (path.length === 0) {
        return !data && defaultValue ? defaultValue : (data as unknown as T);
      }

      // Otherwise we need to get the keys and iterate again.
      properties = Object.keys(data);
    }

    return defaultValue as T;
  }
}
