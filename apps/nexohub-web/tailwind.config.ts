import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: "#020518",
        nexoBlue: "#0963CA",
        radarCyan: "#14C7DD",
        cupoGreen: "#44DD69",
        tealGreen: "#0A8260",
        mint: "#A1EF84",
        ice: "#EEF3F7",
      },
      boxShadow: {
        glow: "0 0 25px rgba(20, 199, 221, 0.25)",
      },
    },
  },
  plugins: [],
} satisfies Config;

