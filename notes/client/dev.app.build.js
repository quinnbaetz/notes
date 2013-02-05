({
  appDir: '..',
  baseUrl: 'client',
  max_line_length: 80,
  include: ['almond','main'],
  paths: {
    almond: 'extern/almond',
  },
  hasOnSave: {
    ignoreConsole: false
  },
  out: '../static/main.min.js',
  wrap: true
  // , optimize: "none",
})
