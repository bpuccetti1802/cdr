import type { StorybookConfig } from '@storybook/angular';
import { resolve } from 'path';
import autoStoryGenerator from 'auto-angular-story-generator';

const customConfig = {
  webpackFinal: async (config) => {
    let plugin = autoStoryGenerator.webpack({
      preset: 'angular',
      imports: ['src/app/**/*.component.ts'],
      prettierConfigPath: resolve(__dirname, '../.prettierrc'),
    });
    config.plugins.push(plugin);
    return config;
  },
};

const config: StorybookConfig = {
  stories: ['../src/**/*.mdx', '../src/**/*.stories.@(js|jsx|mjs|ts|tsx)'],
  addons: [
    '@storybook/addon-onboarding',
    '@storybook/addon-essentials',
    '@chromatic-com/storybook',
    '@storybook/addon-interactions',
  ],
  framework: {
    name: '@storybook/angular',
    options: {},
  },
  ...customConfig,
  docs: {
    autodocs: 'tag',
  },
  staticDirs: [{ from: '../src/assets', to: '/mfSharedLibrary/assets' }]
};
export default config;
