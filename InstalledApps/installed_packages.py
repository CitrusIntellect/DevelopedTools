import os
import subprocess
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

def check_root():
    if os.geteuid() != 0:
        raise PermissionError("This script must be run as root!")

def get_installed_packages():
    """Get a list of installed packages using pacman."""
    result = subprocess.run(['pacman', '-Qq'], stdout=subprocess.PIPE, text=True)
    return result.stdout.splitlines()

def get_desktop_apps():
    """Get a list of desktop applications by checking .desktop files."""
    apps = []
    applications_dir = "/usr/share/applications"

    if os.path.exists(applications_dir):
        for file_name in os.listdir(applications_dir):
            if file_name.endswith(".desktop"):
                apps.append(file_name.split(".desktop")[0])  # Strip the extension
    return apps

def get_kde_packages(packages):
    """Get a list of KDE-related packages."""
    kde_packages = [pkg for pkg in packages if pkg.startswith('org.kde')]
    return kde_packages

def get_libraries(packages):
    """Get a list of installed libraries."""
    libraries = [pkg for pkg in packages if 'lib' in pkg]
    return libraries

def remove_package(package_name):
    """Remove a package from the system using pacman."""
    subprocess.run(['sudo', 'pacman', '-Rns', '--noconfirm', package_name], check=True)

def install_package(package_name):
    """Install a package from the system using pacman."""
    subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', package_name], check=True)

def create_desktop_entry(name, exec_command):
    """Create a .desktop entry for an application."""
    desktop_entry = f"""
[Desktop Entry]
Name={name}
Exec={exec_command}
Icon=application-x-executable
Type=Application
Terminal=false
"""
    with open(f"/usr/share/applications/{name}.desktop", 'w') as f:
        f.write(desktop_entry)

@app.route('/')
def index():
    packages = get_installed_packages()
    apps = get_desktop_apps()
    kde_packages = get_kde_packages(packages)
    libraries = get_libraries(packages)
    return render_template('index.html', packages=packages, apps=apps, kde_packages=kde_packages, libraries=libraries)

@app.route('/delete_package', methods=['POST'])
def delete_package():
    package_name = request.json['package']
    try:
        remove_package(package_name)
        return jsonify({"status": "success", "message": f"Package {package_name} removed successfully"})
    except subprocess.CalledProcessError:
        return jsonify({"status": "error", "message": f"Failed to remove package {package_name}"}), 500

@app.route('/install_package', methods=['POST'])
def install_package_route():
    package_name = request.json['package']
    try:
        install_package(package_name)
        return jsonify({"status": "success", "message": f"Package {package_name} installed successfully"})
    except subprocess.CalledProcessError:
        return jsonify({"status": "error", "message": f"Failed to install package {package_name}"}), 500

@app.route('/create_desktop_entry', methods=['POST'])
def create_desktop_entry_route():
    data = request.json
    name = data['name']
    exec_command = data['exec']
    try:
        create_desktop_entry(name, exec_command)
        return jsonify({"status": "success", "message": f".desktop entry for {name} created successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    check_root()  # Ensure root access
    app.run(host='0.0.0.0', port=5000)
