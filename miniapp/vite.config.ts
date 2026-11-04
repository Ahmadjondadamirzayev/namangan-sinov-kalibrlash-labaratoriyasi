import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// `npm run dev` paytida API so'rovlari Python serveriga yo'naltiriladi
export default defineConfig({
  plugins: [react()],
  server: { proxy: { "/api": "http://localhost:8080", "/uploads": "http://localhost:8080" } },
});
