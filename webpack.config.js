const path = require('path');
const HtmlWebPackPlugin = require('html-webpack-plugin')

const config = {

 entry: path.join(__dirname, 'src/main.js'),

 devServer: {
        contentBase: path.join(__dirname, 'src'),
        hot: true,
        port: 1970,
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
      path: __dirname + '/static',
      filename: 'js/bundle.js'
  },
  plugins: [
      new HtmlWebPackPlugin({
        template: 'src/index.html',
        filename: 'index.html'
      })
  ]
};

module.exports = config;
