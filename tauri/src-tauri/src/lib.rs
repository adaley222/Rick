// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
use tauri::Manager;
use std::process::Command as StdCommand;
use std::env;
use std::path::PathBuf;

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(|_app| {
            println!("Starting Python backend...");
            
            // Get the current working directory and navigate to the project root
            let current_dir = env::current_dir().expect("Failed to get current directory");
            // Go up two levels: from src-tauri to tauri, then to project root
            let project_root = current_dir
                .parent()
                .and_then(|d| d.parent())
                .unwrap_or(&current_dir);
            let backend_dir = project_root.join("backend");
            let script_path = backend_dir.join("rick_cloud.py");
            
            println!("Current directory: {:?}", current_dir);
            println!("Project root: {:?}", project_root);
            println!("Backend directory: {:?}", backend_dir);
            println!("Running Python script from: {:?}", script_path);
            
            // Start the Python backend
            match StdCommand::new("python")
                .current_dir(&backend_dir)  // Set working directory to backend folder
                .arg(&script_path)
                .arg("8000")
                .spawn()
            {
                Ok(child) => {
                    println!("Python backend started successfully with PID: {}", child.id());
                }
                Err(e) => {
                    eprintln!("Failed to start Python backend: {}", e);
                }
            }
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
