export abstract class Singleton {
  private static instances = new Map<object, unknown>();

  static getInstance<T>(this: new () => T): T {
    if (!Singleton.instances.has(this)) {
      Singleton.instances.set(this, new this());
      console.debug(`[Singleton] Created instance of ${this.name}`);
    }
    return Singleton.instances.get(this) as T;
  }
}
