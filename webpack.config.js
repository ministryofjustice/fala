var webpack = require("webpack");

module.exports = {
  entry: {
    app: './fala/assets-src/scripts/main.js',
    polyfills: ['JSON2', 'html5shiv']
  },
  output: {
    path: 'fala/assets/scripts',
    filename: '[name].bundle.js'
  },
  resolve: {
    modulesDirectories: [
      'node_modules',
      'node_modules/mojular/node_modules'
    ]
  }
};
