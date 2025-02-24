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
    // 添加判断逻辑
    let exe_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let backend_name = format!("backend{}", env::consts::EXE_SUFFIX); // 自动添加 .exe 或空
    let backend_path = exe_dir.join("bin").join(backend_name);

    println!("当前平台的可执行文件后缀: {}", env::consts::EXE_SUFFIX);
    println!("后端路径: {:?}", backend_path);
    
    eprintln!(
        backend_path.exists(),
        "后端可执行文件未找到: {:?}，请确保构建流程正确生成并复制文件到 bin 目录",
        backend_path
    );

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
