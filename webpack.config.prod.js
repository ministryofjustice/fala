var webpack = require('webpack');
var webpackConfig = require('./webpack.config.js');

webpackConfig.plugins.push(
  new webpack.optimize.UglifyJsPlugin({
    compress: { warnings: false }
  })
);

module.exports = webpackConfig;
