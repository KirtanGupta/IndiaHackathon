import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

export default defineConfig({
  root: resolve(__dirname),
  plugins: [react()],
  server: {
    fs: {
      allow: [resolve(__dirname, "..")],
    },
  },
  resolve: {
    alias: {
      "@": resolve(__dirname, "..", "src"),
      "@components": resolve(__dirname, "..", "components"),
      "@api": resolve(__dirname, "..", "api"),
      "@utils": resolve(__dirname, "..", "utils")
    }
  },
  build: {
    outDir: resolve(__dirname, "..", "frontend-dist"),
    emptyOutDir: true
  }
});