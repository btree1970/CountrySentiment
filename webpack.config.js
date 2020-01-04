const path = require('path');
const HtmlWebPackPlugin = require('html-webpack-plugin')

const config = {

 entry: path.join(__dirname, 'src/main.js'),

 mode: process.env.NODE_ENV,

 devServer: {
        contentBase: path.join(__dirname, 'static'),
        hot: true,
        port: 1970,
        host: '0.0.0.0',
        disableHostCheck: true
  },
 
  module: {
    rules: [
      {
        test: /\.js$/,
        loaders:  'babel-loader',
        exclude: /node_modules/,
        options: {
            presets: [
                require.resolve('babel-preset-react-app')
            ]
        }
      },
    ],
  },
  output: {
      path: __dirname + '/',
      filename: 'static/js/bundle.js'
  },
  plugins: [
      new HtmlWebPackPlugin({
        template: 'src/index.html',
        filename: 'static/index.html'
      })
  ]
};

module.exports = config;
