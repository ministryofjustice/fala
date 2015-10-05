var webpack = require("webpack");
var PROD = JSON.parse(process.env.PROD || '0');

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
  },
  plugins: PROD ? [
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        global_defs: { DEBUG: false }
      }
    })
  ] : []
};
