// Prevent additional console window on Windows in release mode (DO NOT REMOVE)
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::env;
use std::path::PathBuf;
use std::process::{Child, Command, Stdio};
use tauri::Manager;
use tauri::path::BaseDirectory;

// Struct to manage the backend process
struct BackendProcess(Child);

// Ensure the backend process is terminated when the app exits
impl Drop for BackendProcess {
    fn drop(&mut self) {
        if let Err(e) = self.0.kill() {
            eprintln!("Failed to terminate backend process: {}", e);
        } else {
            println!("Backend process terminated successfully.");
        }
    }
}
fn main() {
    tauri::Builder::default()
        .setup(|app| {
            // Determine the backend executable name based on the OS
            let file_name = format!("backend{}", env::consts::EXE_SUFFIX); // Automatically adds .exe on Windows

            let backend_name = PathBuf::from("bin").join(file_name);
            let backend_path = app.path()
                .resolve(&backend_name, BaseDirectory::Resource)
                .expect("Failed to resolve backend executable path");

            println!("backend_path {}", backend_path.display());

            // Spawn the backend process
            let backend_process =  Command::new(&backend_path)
                .stdout(Stdio::inherit()) // Forward stderr to the parent process
                .stdin(Stdio::inherit()) // Forward stderr to the parent process
                .spawn()
                .unwrap_or_else(|e| {
                    eprintln!("Failed to start backend process: {}", e);
                    std::process::exit(1);
                });
            app.manage(BackendProcess(backend_process));
            println!("Tauri application started, backend is running.");
                Ok(())

        })
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_opener::init())
        .run(tauri::generate_context!())
        .expect("Error while running Tauri application");
}