import os
import re
import subprocess

# Path to LDPlayer config folder
CONFIG_PATH = r"D:\LDPlayer\LDPlayer9\vms\config"

# 2. Process config files
def adb_debugger():
    for filename in os.listdir(CONFIG_PATH):
        if filename.startswith("leidian") and filename.endswith(".config") and filename != "leidians.config":
                file_path = os.path.join(CONFIG_PATH, filename)
                print(f"Processing {filename}...")

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Ensure CRLF line endings
                content = content.replace("\r\n", "\n").replace("\r", "\n").split("\n")

                # Find macAddress line
                new_lines = []
                adb_added = False
                for line in content:
                    new_lines.append(line)
                    if '"propertySettings.macAddress"' in line and not adb_added:
                        new_lines.append('    "basicSettings.adbDebug": 1,')
                        adb_added = True

                if adb_added:
                    # Join with CRLF and save without BOM
                    new_content = "\r\n".join(new_lines)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    # print(f"  adbDebug added to {filename}")
                else:
                    print(f"  macAddress not found in {filename} — skipped.")

    # print("Done! Now start LDPlayer and check if ADB Debug is enabled.")