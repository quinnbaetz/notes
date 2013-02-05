({
  appDir: '..',
  baseUrl: 'client',
  max_line_length: 80,
  include: ['almond', 'main'],
  paths: {
    almond: 'extern/almond',
  },
  hasOnSave: {
    ignoreConsole: true
  },
  out: '../static/main.min.js',
  wrap: true
})
