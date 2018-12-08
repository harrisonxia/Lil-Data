var path = require('path')
var webpack = require('webpack')
const BabelFlowWebpackPlugin = require('babel-flow-webpack-plugin')
var devPort = 4000
const HtmlWebpackPlugin = require('html-webpack-plugin')
const ExtractTextPlugin = require('extract-text-webpack-plugin')
const styleVars = require('./style-vars.js')
const customProperties = require('postcss-custom-properties')
const autoprefixer = require('autoprefixer')
const customPropertiesPlugin = customProperties()
customPropertiesPlugin.setVariables(styleVars)
var CopyWebpackPlugin = require('copy-webpack-plugin')

module.exports = {
    context: path.resolve(__dirname, '..', 'src'),
    entry: {
        'dev-server': 'webpack-dev-server/client?http://localhost:' + devPort,
        'app': './index.jsx'
    },

    output: {
        path: '/',
        publicPath: 'http://localhost:' + devPort + '/',
        filename: '[name].[hash].js',
    },

    resolve: {
        modules: [
            path.resolve(__dirname, '../src'),
            'node_modules'
        ],
        extensions: ['.js', '.jsx']
    },

    module: {
        rules: [
            {
                test: /\.js|\.jsx$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
                options:
                    {
                        cacheDirectory: true,
                        plugins: ['react-hot-loader/babel']
                    }
            },
            {
                test: /\.css$/,
                exclude: /\.useable\.css$/,
                use: ExtractTextPlugin.extract({
                    use: [
                        {
                            loader: 'css-loader',
                            options: {
                                importLoaders: true,
                                localIdentName:
                                    '[name]__[local]__[hash:base64:5]',
                                minimize: false,
                                modules: true,
                                sourceMap: true,
                            }
                        },
                        {
                            loader: 'csso-loader',
                        },
                        {
                            loader: 'postcss-loader',
                            options: {
                                sourceMap: true,
                                plugins: [
                                    customPropertiesPlugin,
                                    autoprefixer(),
                                ],
                            },
                        },
                    ],
                }),
            },
            {
                test: /\.(png|jpg|gif|ttf|woff|woff2)$/,
                loader: 'url-loader',
                options: {
                    limit: 10000
                }
            },
            {
                test: /\.(json)$/,
                loader: 'json-loader'
            },
        ]
    },

    plugins: [
        new webpack.DefinePlugin({
            "process.env": {
                BROWSER: true,
                NODE_ENV: JSON.stringify("development"),
                PUBLIC_URL: JSON.stringify('http://localhost:4000/Lil-Data/'),
            },
        }),
        new ExtractTextPlugin({filename: '[name].[hash].css', allChunks: true}),
        new HtmlWebpackPlugin({
            template: 'index.html',
            filename: 'index.html',
            inject: true,
        }),
        new BabelFlowWebpackPlugin(),
        new CopyWebpackPlugin([
            {from:'assets/img',to:'assets/img'},
        ]),
    ],
    devtool: 'inline-source-map',
    devServer: {
        port: devPort,
        contentBase: 'src/',
        headers: {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": "true"},
        proxy: {
            '/**/app.js': {
                target: 'http://localhost:' + devPort,
            }
        },
        inline: true,
        historyApiFallback: true
    }

}
