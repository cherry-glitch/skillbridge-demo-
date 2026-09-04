/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        paper: '#EEF2F6',
        surface: '#FBFCFE',
        ink: '#14213D',
        line: '#C4CCD6',
        havecolor: '#2F6F5E',
        havecolor2: '#E7F1EE',
        gapcolor: '#E4572E',
        gapcolor2: '#FBEAE3',
      },
      fontFamily: {
        display: ['"Fraunces"', 'serif'],
        body: ['"IBM Plex Sans"', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'monospace'],
      },
    },
  },
  plugins: [],
}
