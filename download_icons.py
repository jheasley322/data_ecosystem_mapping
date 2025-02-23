import os
import yaml
import requests
import zipfile
import io

# Material Symbols GitHub ZIP URL
GITHUB_ICONS_URL = "https://github.com/google/material-design-icons/archive/refs/heads/main.zip"

# Directory structure
ICON_DIR = "libraries/icons"
BRANDED_NODES_FILE = "primary_config/branded_nodes.yaml"
TEMP_ZIP_FILE = "material_icons.zip"

# Required icons (match names in Google's repo)
ICONS = {
    "database": "database",
    "api": "api",
    "service": "cloud",
    "pipeline": "sync",
    "container": "folder",
    "aws_s3": "cloud_upload",
    "gcp_bigquery": "data_usage",
    "sql_server": "dns",
    "snowflake": "ac_unit",
    "kafka": "hub",
    "custom_api": "integration_instructions"
}

def download_material_icons_zip():
    """Downloads and saves the Material Symbols ZIP file from GitHub."""
    print("⬇️ Downloading Material Symbols ZIP from GitHub...")
    response = requests.get(GITHUB_ICONS_URL, stream=True)
    
    if response.status_code == 200:
        with open(TEMP_ZIP_FILE, "wb") as file:
            file.write(response.content)
        print("✅ Download complete!")
    else:
        print("❌ Failed to download ZIP file. Check URL or internet connection.")
        return False
    return True

def extract_needed_icons():
    """Extracts only the needed SVG icons from the ZIP archive."""
    print("📦 Extracting required icons...")

    with zipfile.ZipFile(TEMP_ZIP_FILE, "r") as zip_ref:
        for name, icon in ICONS.items():
            icon_path = f"material-design-icons-main/symbols/svg/outlined/{icon}.svg"
            extracted_path = os.path.join(ICON_DIR, f"{name}.svg")

            try:
                with zip_ref.open(icon_path) as icon_file:
                    with open(extracted_path, "wb") as output_file:
                        output_file.write(icon_file.read())
                print(f"✅ Extracted: {name}.svg")
            except KeyError:
                print(f"❌ Icon not found: {name}")

def update_branded_nodes():
    """Updates branded_nodes.yaml with the extracted icons."""
    branded_nodes = {}

    for name in ICONS.keys():
        file_path = os.path.join(ICON_DIR, f"{name}.svg")
        if os.path.exists(file_path):
            branded_nodes[name] = {
                "icon": file_path,
                "label": name.replace("_", " ").title()
            }

    # Save to YAML
    with open(BRANDED_NODES_FILE, "w") as yaml_file:
        yaml.dump({"branded_nodes": branded_nodes}, yaml_file, default_flow_style=False)

    print(f"📄 Updated {BRANDED_NODES_FILE}!")

if __name__ == "__main__":
    os.makedirs(ICON_DIR, exist_ok=True)

    if download_material_icons_zip():
        extract_needed_icons()
        update_branded_nodes()

    # Cleanup temporary ZIP
    os.remove(TEMP_ZIP_FILE)
    print("🗑️ Removed temporary ZIP file.")