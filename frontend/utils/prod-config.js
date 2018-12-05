var path = require('path');
var webpack = require('webpack');
var CopyWebpackPlugin = require('copy-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

var devConfig = require('./dev-config');

module.exports = {
  context: devConfig.context,
  entry: {
    'app': './index.jsx'
  },
  output: {
    path: path.resolve(__dirname, '../../docs/'),
    filename: 'app.[hash].js'
  },
  devtool: 'cheap-module-source-map',
  resolve: devConfig.resolve,
  module: devConfig.module,
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        BROWSER: true,
        NODE_ENV: JSON.stringify('production'),
        PUBLIC_URL: JSON.stringify('https://www.devxia.com/Lil-Data/'),
      },
    }),
    new ExtractTextPlugin({filename: '[name].[hash].css', allChunks: true}),
    new HtmlWebpackPlugin({
      template: 'index.html',
      filename: './index.html',
      inject: true,
    }),
    new CopyWebpackPlugin([
      {from: 'assets/img', to: 'assets/img'},
      {from: './favicon.ico', to: './favicon.ico'}
    ]),
  ]
};
