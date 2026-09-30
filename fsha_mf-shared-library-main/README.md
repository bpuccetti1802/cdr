# MfSharedLibrary

This is the shared library microfrontend with Angular version 18.2.8.
  
## Minimum requirements
`Node >= 20.18`

## Setup

Run the following command inside the project
```bash
npm ci
```

## Development server

Run `ng serve mf-shared-library --port 4201` for a dev server. Navigate to `http://localhost:4201/`. The application will automatically reload if you change any of the source files.

## Add component

1. Run the following command to create a component or a module
```bash
 ng generate component <name-component> 
 ```
  or
```bash
 ng generate module <name-module>
```

2. add './NameClassModule': './path-module', in webpack.config.js

```bash
const { shareAll, withModuleFederationPlugin } = require('@angular-architects/module-federation/webpack');

module.exports = withModuleFederationPlugin({
  name: 'mfSharedLibrary',
  filename: 'remoteEntry.js',
  exposes: {
    './Component': './src/app/app.component.ts',
    './ExampleComponent': './src/app/example-component/example-component.component.ts',
    // Type here your new component
    './NameClassModule': './path-module',
  },

  shared: {
    ...shareAll({ singleton: true, strictVersion: true, requiredVersion: 'auto' }),
  },
 
});
```
