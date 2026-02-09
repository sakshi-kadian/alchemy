
import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                background: "var(--background)",
                foreground: "var(--foreground)",
                plum: {
                    50: '#f5f3ff',
                    100: '#ede9fe',
                    500: '#8b5cf6',
                    900: '#4c1d95',
                    950: '#1a0b2e', // Deepest Plum (Noir)
                },
                maroon: {
                    500: '#be123c',
                    900: '#881337',
                },
                clinical: {
                    50: '#ecfeff',
                    500: '#06b6d4', // Cyan
                    900: '#164e63',
                }
            },
            fontFamily: {
                sans: ['var(--font-inter)'],
                mono: ['var(--font-jetbrains-mono)'],
            },
        },
    },
    plugins: [],
};
export default config;
