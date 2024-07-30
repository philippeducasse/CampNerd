const { defineConfig } = require('@vue/cli-service');
module.exports = defineConfig({
  transpileDependencies: true,
  outputDir: '../camping_project/static',
  assetsDir: 'assets',
  indexPath: '../templates/index.html',
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // Django backend
        changeOrigin: true,
      },
    },
  },
});
