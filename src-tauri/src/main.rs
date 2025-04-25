// Prevent additional console window on Windows in release mode (DO NOT REMOVE)
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::env;
use std::path::PathBuf;

// 在编译时判断平台
#[cfg(windows)]
use std::os::windows::process::CommandExt;

use std::process::{Child, Command, Stdio};
use tauri::path::BaseDirectory;
use tauri::Manager;

// Struct to manage the backend process
struct BackendProcess(Child);

// Ensure the backend process is terminated when the app exits
impl Drop for BackendProcess {
    fn drop(&mut self) {
        // When the Tauri app closes, terminate the backend process
        if let Err(e) = self.0.kill() {
            eprintln!("Failed to terminate backend process: {}", e);
        } else {
            println!("Backend process terminated successfully.");
        }
    }
}

#[cfg(unix)]
fn start_backend(backend_path: &PathBuf) -> std::io::Result<Child> {
    return Command::new(&backend_path).spawn();
}

#[cfg(windows)]
fn start_backend(backend_path: &PathBuf) -> std::io::Result<Child> {
    Command::new(&backend_path)
        .stdout(Stdio::piped()) // 关键：重定向 stdout
        .stderr(Stdio::piped()) // 关键：重定向 stderr
        .creation_flags(0x08000000)
        .spawn()
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_fs::init())
        .setup(|app| {
            // Determine the backend executable name based on the OS
            let is_dev = true;
            if !is_dev {
                let file_name = format!("backend{}", env::consts::EXE_SUFFIX); // Automatically adds .exe on Windows

                let backend_name = PathBuf::from("bin").join(file_name);
                let backend_path = app
                    .path()
                    .resolve(&backend_name, BaseDirectory::Resource)
                    .expect("Failed to resolve backend executable path");

                println!("backend_path {}", backend_path.display());

                let backend_process =
                    start_backend(&backend_path).expect("start backend process failed");

                // // Spawn the backend process
                app.manage(BackendProcess(backend_process));

                println!("Tauri application started, backend is running.");
            }
            Ok(())
        })
        .plugin(tauri_plugin_shell::init()) // 确保启用 shell 插件
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_opener::init())
        .run(tauri::generate_context!())
        .expect("Error while running Tauri application");
}
