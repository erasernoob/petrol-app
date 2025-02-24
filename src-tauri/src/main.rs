// Prevent additional console window on Windows in release mode (DO NOT REMOVE)
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
use std::env;
use std::path::PathBuf;
use std::process::{Child, Command, Stdio};
use tauri::Manager;

struct BackendProcess(Child);

impl Drop for BackendProcess {
    fn drop(&mut self) {
        if let Err(e) = self.0.kill() {
            eprintln!("Failed to terminate backend process: {}", e);
        } else {
            println!("Backend process terminated successfully.");
        }
    }
}

// fn main() {
//     petrol_app_lib.run()
// }

fn main() {
    let exe_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")); // 指向src-tauri目录
    // 添加判断逻辑
    let backend_path = if cfg!(target_os = "windows") {
        exe_dir.join("bin").join("backend.exe")
    } else {
        exe_dir.join("bin").join("backend")
    };

    let backend_process = Command::new(&backend_path)
        .stdout(Stdio::inherit())
        .stderr(Stdio::inherit())
        .spawn()
        .unwrap_or_else(|e| {
            eprintln!("Failed to start FastAPI backend: {}", e);
            std::process::exit(1);
        });


    let backend = BackendProcess(backend_process);

    tauri::Builder::default()
        .setup(|app| {
            app.manage(backend);
            println!("Tauri application started, backend is running.");
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("Error while running Tauri application");
}
