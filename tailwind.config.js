/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js",
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {
      gridTemplateColumns: {
        'my-columns': 'auto 0fr'
      }
    }
  },
  plugins: [
    require('flowbite/plugin')
  ]
}
