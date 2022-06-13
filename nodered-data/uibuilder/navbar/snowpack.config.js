// Snowpack Configuration File
// See all supported options: https://www.snowpack.dev/reference/configuration

/** @type {import("snowpack").SnowpackUserConfig } */
module.exports = {
  mount: {
    /* ... */
    'src': '/'  
  },
  plugins: [
    /* ... */
    '@snowpack/plugin-vue',
  ],
  packageOptions: {
    /* ... */
  },
  devOptions: {
    /* ... */
  },
  buildOptions: {
    /* ... */
    'out': 'dist',
  },
  resolve: {
    alias: {
      'vue-plotly': '/data/uibuilder/navbar/node_modules/vue-plotly/dist/vue-plotly.common.js',
    },
  }
};
