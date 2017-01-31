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
  Note: This is the best option for development because
  it is the smallest option that shows the correct line number.
  */
  devtool: 'cheap-module-eval-source-map',
  entry: [
    'webpack-hot-middleware/client',
    `${APP_DIR}/index.jsx`,
  ],
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
    // Ensures consistent build hashes
    new webpack.optimize.OccurenceOrderPlugin(),
    // Self-explanatory
    new webpack.HotModuleReplacementPlugin(),
    // Used to handle errors more cleanly
    new webpack.NoErrorsPlugin(),
  ],
  module: {
    loaders: [
      {
        test: /\.jsx?/,
        include: APP_DIR,
        loaders: ['react-hot', 'babel?' + JSON.stringify({
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
