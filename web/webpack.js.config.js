var path = require('path');
var webpack = require('webpack');


module.exports = {
  // Set up all the build targets and their entry-points
  resolve: ['.coffee'],
  entry: {
    'index': './coffee/index.coffee',
  },
  output: {
    path: path.join(__dirname, 'dist'),
    filename: '[name].js',
  },
  module: {
    loaders: [
      // How to handle our common file types
      { test: /\.coffee$/, loader: 'coffee-loader' },
    ]
  },
  resolve: {
    root: [
      path.resolve('./js')
    ],
    modulesDirectories: ['node_modules', 'bower_components'],
    alias: { 
      "bower": "bower_components"
    }
  },
  plugins: [
      new webpack.ProvidePlugin({
        $: 'jquery',
      }),
  ],
  node: {
    global: true
  }
};
