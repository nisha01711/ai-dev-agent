/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          primary: '#0a0a0a',
          secondary: '#141414',
          tertiary: '#1e1e1e',
          border: '#2a2a2a',
        },
        accent: {
          blue: '#60a5fa',
          purple: '#a78bfa',
          green: '#34d399',
          red: '#f87171',
        }
      },
      fontFamily: {
        mono: ['Fira Code', 'monospace'],
        display: ['Space Grotesk', 'sans-serif'],
      },
      boxShadow: {
        'glow-blue': '0 0 20px rgba(96, 165, 250, 0.5)',
        'glow-purple': '0 0 20px rgba(167, 139, 250, 0.5)',
      },
    },
  },
  plugins: [],
}
