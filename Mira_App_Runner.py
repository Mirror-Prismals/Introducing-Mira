import os
import platform
import subprocess
import time
import shutil  # Ensure shutil is imported at the top

class MiraOS:
    def __init__(self, base_dir="Modules"):
        """
        Initialize Mira OS with the base directory to scan for apps.
        """
        self.base_dir = base_dir
        self.app_registry = []  # Flat list of all apps
        self.running_apps = {}  # Tracks running apps with start times and process objects
        self.running = True
        self.scan_modules()

    def scan_modules(self):
        """
        Scan the provided base directory and register all .py files as apps.
        """
        if not os.path.exists(self.base_dir):
            print(f"Error: Base directory '{self.base_dir}' does not exist.")
            return

        self.app_registry = []  # Reset app registry
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    full_path = os.path.join(root, file)
                    self.app_registry.append(full_path)

    def list_apps(self):
        """
        Display all discovered apps in a flat list.
        """
        if not self.app_registry:
            print("No apps found.")
        else:
            print("\nAvailable Apps:")
            for app_path in self.app_registry:
                app_name = os.path.basename(app_path)
                print(f"  - {app_name}")

    def find_app_path(self, app_name):
        """
        Find the full path of an app by its name.
        """
        for app_path in self.app_registry:
            if os.path.basename(app_path) == app_name:
                return app_path
        return None

    def launch_in_new_terminal(self, app_path):
        """
        Launch the app in a new terminal window based on the OS.
        """
        try:
            if platform.system() == "Windows":
                cmd = f'start cmd /k python "{app_path}"'
                process = subprocess.Popen(cmd, shell=True)
            elif platform.system() == "Darwin":  # macOS
                apple_script = f'''
                tell application "Terminal"
                    do script "python \\"{app_path}\\""
                    activate
                end tell
                '''
                process = subprocess.Popen(['osascript', '-e', apple_script])
            elif platform.system() == "Linux":
                terminal = None
                for term in ["gnome-terminal", "konsole", "xterm"]:
                    if shutil.which(term):
                        terminal = term
                        break
                if not terminal:
                    print("Error: No supported terminal emulator found.")
                    return None
                cmd = f'python "{app_path}"'
                # For some terminals like gnome-terminal, you might need to use '--' before the command
                if terminal == "gnome-terminal":
                    process = subprocess.Popen([terminal, "--", "bash", "-c", cmd])
                else:
                    process = subprocess.Popen([terminal, "-e", cmd])
            else:
                print("Error: Unsupported operating system.")
                return None
            return process
        except Exception as e:
            print(f"Failed to launch app: {e}")
            return None

    def run_app(self, app_name):
        """
        Run a selected app in a new terminal window and track its runtime.
        """
        app_path = self.find_app_path(app_name)
        if not app_path:
            print(f"Error: App '{app_name}' not found.")
            return

        # Launch app in a new terminal and track its runtime
        process = self.launch_in_new_terminal(app_path)
        if process:
            self.running_apps[app_name] = {"start_time": time.time(), "process": process}
            print(f"App '{app_name}' is now running.")
        else:
            print(f"Failed to launch app '{app_name}'.")

    def task_manager(self):
        """
        Display all currently running apps with their start times.
        """
        if not self.running_apps:
            print("No apps are currently running.")
            return

        print("\nRunning Apps:")
        for app_name, info in self.running_apps.items():
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(info["start_time"]))
            print(f"  - {app_name} (Started at: {start_time})")

    def close_app(self, app_name):
        """
        Close a running app and remove it from the running_apps list.
        """
        if app_name not in self.running_apps:
            print(f"Error: App '{app_name}' is not running.")
            return

        process = self.running_apps[app_name]["process"]
        try:
            if platform.system() == "Windows":
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
            else:
                process.terminate()
                process.wait(timeout=5)
            print(f"App '{app_name}' has been closed.")
        except Exception as e:
            print(f"Failed to close app '{app_name}': {e}")
            return

        # Remove from running_apps
        del self.running_apps[app_name]

    def command_loop(self):
        """
        Command-based interface for Mira OS.
        """
        print("Welcome to Mira OS! Type '/help' for a list of commands.")
        while self.running:
            try:
                command = input("\n> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting Mira OS. Closing all running apps...")
                self.running = False
                break

            if not command:
                continue  # Ignore empty inputs

            if command == "/browse":
                self.list_apps()
            elif command.startswith("/run "):
                app_name = command[5:].strip()
                if app_name:
                    self.run_app(app_name)
                else:
                    print("Usage: /run [app_name.py]")
            elif command == "/task_manager":
                self.task_manager()
            elif command.startswith("/close "):
                app_name = command[7:].strip()
                if app_name:
                    self.close_app(app_name)
                else:
                    print("Usage: /close [app_name.py]")
            elif command == "/help":
                self.print_help()
            else:
                print("Unknown command. Type '/help' for a list of commands.")

        # Attempt to close all running apps on exit
        if self.running_apps:
            print("Closing all running apps...")
            for app_name in list(self.running_apps.keys()):
                self.close_app(app_name)

    def print_help(self):
        """
        Print the list of available commands.
        """
        print("""
Available Commands:
  /browse                 - List all available apps
  /run [app_name.py]     - Run an app by name
  /task_manager          - Show all running apps with their start times
  /close [app_name.py]   - Close a running app
  /help                   - Show this help message
        """)

# Main Execution
if __name__ == "__main__":
    mira_os = MiraOS(base_dir="Modules")
    mira_os.command_loop()
