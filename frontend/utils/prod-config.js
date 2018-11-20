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
    path: path.resolve(__dirname, '../dist/'),
    filename: 'app.[hash].js'
  },
  devtool: 'cheap-module-source-map',
  resolve: devConfig.resolve,
  module: devConfig.module,
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        BROWSER: true,
        NODE_ENV: JSON.stringify('production')
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
