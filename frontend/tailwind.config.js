module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "primary": "#7e56f5",
        "background-light": "#f6f5f8",
        "background-dark": "#141022",
        "card-dark": "#1f1834",
        "card-border-dark": "#3f3168",
        "text-muted-dark": "#9f90cb",
        "header-border-dark": "#2c2249",
        "secondary-button-dark": "#2c2249"
      },
      fontFamily: {
        "display": ["Inter", "sans-serif"]
      },
      borderRadius: {
        "DEFAULT": "0.25rem",
        "lg": "0.5rem",
        "xl": "0.75rem",
        "full": "9999px"
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries'),
  ],
}