/* eslint-disable */

const webpack = require('webpack');
const path = require('path');

const BUILD_DIR = path.resolve(__dirname, 'public');
const APP_DIR = path.resolve(__dirname, 'src');

const commitHash = require('child_process')
  .execSync('git rev-parse HEAD')
  .toString();

const config = {
  /*
  Note: This is the best option for production because:

  Both bundle.js and bundle.js.map are smallest
  The correct file name and line number are provided
  */
  devtool: 'cheap-module-source-map',
  entry: `${APP_DIR}/index.jsx`,
  output: {
    path: BUILD_DIR,
    filename: 'bundle.js',
    publicPath: '/',
  },
  resolve: {
    extensions: ['', '.jsx', '.js'],
  },
  plugins: [
    new webpack.DefinePlugin({
      __COMMIT_HASH__: JSON.stringify(commitHash),
    }),
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify('production')
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        warnings: false
      },
      comments: false,
      sourceMap: false
    }),
  ],
  module: {
    loaders: [
      {
        test: /\.jsx?/,
        include: APP_DIR,
        loaders: ['babel?' + JSON.stringify({
          presets: ["es2015", "react"],
          plugins: ["transform-decorators-legacy", "transform-class-properties", [
            "import",
            {
              "libraryName": "antd",
              "style": "css"
            }
          ]]
        })]
      },
      { test: /\.css$/, loader: 'style-loader!css-loader' },
    ],
  },
};

module.exports = config;
/* eslint-enable */
