/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/app.vue",
    './formkit.theme.ts'
  ],
  //purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [
    require('@formkit/themes/tailwindcss'),
  ],
}

