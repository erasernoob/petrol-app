import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { vitePluginForArco } from '@arco-plugins/vite-react'
import svgr from 'vite-plugin-svgr';
import { loadEnv } from "vite";
const host = process.env.TAURI_DEV_HOST;

export default defineConfig(async ({ mode }) => {
  const env = loadEnv(mode, process.cwd())
  return {
    plugins: [react(), vitePluginForArco, svgr()],

    // Vite options tailored for Tauri development and only applied in `tauri dev` or `tauri build`
    //
    // 1. prevent vite from obscuring rust errors
    clearScreen: false,
    // 2. tauri expects a fixed port, fail if that port is not available
    server: {
      // proxy: {
      //   '/api': {
      //     target: 'http://localhost:5000',
      //     changeOrigin: true,
      //     rewrite: (path) => path.replace(/^\/api/, '')
      //   }
      // },
      port: 1420,
      strictPort: true,
      host: host || false,
      hmr: host
        ? {
          protocol: "ws",
          host,
          port: 1421,
        }
        : undefined,
      watch: {
        // 3. tell vite to ignore watching `src-tauri`
        ignored: ["**/src-tauri/**"],
      },
    },
    // 添加process.env配置
    define: {
      'process.env': env
    }

  }
});
