const path = require("path");
// const webpack = require("webpack");
const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  context: __dirname,
  entry: [
    "./fala/assets-src/scripts/main.js",
    "./fala/assets-src/sass/style.scss",
    ],
  output: {
    path: path.resolve(__dirname, "fala/assets/webpack_bundles/"),
    publicPath: "auto",
    filename: "[name]-[contenthash].js",
  },
  plugins: [
    new BundleTracker({ path: path.resolve(__dirname, "fala/"), filename: "webpack-stats.json" }),
  ],
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: [],
      }, {
        test: /\.scss$/,
        exclude: /node_modules/,
        use: [
          {
            loader: 'file-loader',
            options: { outputPath: 'css/', name: '[name].css'}
          },
          'sass-loader'
        ]
      }
    ]
  }
};
