module.exports = {
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader"
          }
        }
      ]
    },
    entry: {
      InstructorApp: './src/InstructorApp.js',
      DepartmentApp: './src/DepartmentApp.js'
    },
    output: {
      filename: '[name].js',
      path: __dirname + '/static/frontend'
    }
  };
