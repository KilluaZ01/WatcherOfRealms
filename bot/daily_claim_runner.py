import subprocess
from datetime import datetime
import json
import time
import os
from macros import tap_macro
from path_utils import get_persistent_path
import cv2
import numpy as np
import subprocess

TEMPLATE_PATHS = ["D:/Silver_Blood_Bot/templates/start_template.png"]
SCREENSHOT_DIR = "D:/Silver_Blood_Bot/temp_screenshots"

def take_screenshot(instance_name):
    remote_path = "/sdcard/result.png"
    local_path = os.path.join(SCREENSHOT_DIR, f"{instance_name}.png")

    # Step 1: Take screenshot inside emulator
    screencap_cmd = [
        "ldconsole.exe", "adb",
        "--name", instance_name,
        "--command", f"shell screencap -p {remote_path}"
    ]
    result1 = subprocess.run(screencap_cmd, capture_output=True, text=True)
    if result1.returncode != 0:
        print(f"[{instance_name}] ❌ Error during screencap: {result1.stderr.strip()}")
        return None

    # Step 2: Pull screenshot
    pull_cmd = [
        "ldconsole.exe", "adb",
        "--name", instance_name,
        "--command", f'pull {remote_path} "{local_path}"'
    ]
    result2 = subprocess.run(pull_cmd, capture_output=True, text=True)
    if result2.returncode != 0:
        print(f"[{instance_name}] ❌ Error during pull: {result2.stderr.strip()}")
        return None

    return local_path  # ✅ Success

def is_start_screen(instance_name, threshold=0.70):
    screenshot_path = take_screenshot(instance_name)
    if not screenshot_path:
        return False

    screenshot = cv2.imread(screenshot_path, 0)
    if screenshot is None:
        print(f"❌ Could not load screenshot: {screenshot_path}")
        return False

    match_found = False
    for template_path in TEMPLATE_PATHS:
        template = cv2.imread(template_path, 0)
        if template is None:
            print(f"❌ Could not load template: {template_path}")
            continue

        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        print(f"[{instance_name}] 🔍 Compared with {template_path}, match: {max_val:.2f}")
        if max_val >= threshold:
            match_found = True
            break

    os.remove(screenshot_path)  # 🧹 Clean up
    return match_found

def ensure_all_start_screens(instance_names, max_retries=3):
    for attempt in range(1, max_retries + 1):
        print(f"\n🔁 Start Screen Check Attempt {attempt}")

        not_ready = []
        for instance_name in instance_names:
            if not is_start_screen(instance_name):
                print(f"[{instance_name}] ❌ Not on start screen, retrying...")
                os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell am force-stop com.skystone.silverblood.us"')
                time.sleep(3)
                os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell monkey -p com.skystone.silverblood.us -c android.intent.category.LAUNCHER 1"')
                not_ready.append(instance_name)

        if not not_ready:
            print("✅ All instances are on start screen.")
            return True

        time.sleep(100)

    print("❌ Could not reach start screen in all instances after retries.")
    return False

def launch_instance(instance_name):
    subprocess.run(f'ldconsole.exe launch --name "{instance_name}"', shell=True)

def should_claim_today(batch):
    today = datetime.now().strftime("%Y-%m-%d")
    return batch["last_login"] != today and batch["login_day"] <= 14

def claim_login_rewards():
    json_path = get_persistent_path('batches.json')
    with open(json_path, "r") as f:
        batches = json.load(f)

    for batch in batches:
        if not should_claim_today(batch):
            continue

        instance_names = batch["instance_names"]
        
        # 🔼 Launch instances before attempting to send ADB commands
        for instance in instance_names:
            launch_instance(instance)

        # ⏳ Wait a bit to let instances boot
        time.sleep(50)

        for instance_name in instance_names:
            os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell monkey -p com.skystone.silverblood.us -c android.intent.category.LAUNCHER 1"')
            print(f"[{instance_name}] - Launched Silver and Blood")
        time.sleep(100)

        success = ensure_all_start_screens(instance_names)
        if not success:
            print("❌ Aborting: Some instances failed to reach start screen.")
            return
        
        for instance_name in instance_names:
            tap_macro(instance_name, 800, 500)
        time.sleep(20)

        day = batch["login_day"]
        if day <= 7:
            print("📦 Claiming 7-Day Login Reward...")

            for instance_name in instance_names:
                tap_macro(instance_name, 1171, 104)
            time.sleep(10)

            for instance_name in instance_names:
                tap_macro(instance_name, 1171, 104)
            time.sleep(10)

            for instance_name in instance_names:
                tap_macro(instance_name, 1171, 104)
            time.sleep(10)

            print("🎁 Claiming 14-Day Login Reward...")

            for instance_name in instance_names:
                tap_macro(instance_name, 1171, 104)
            time.sleep(10)

            for instance in instance_names:
                os.system(f'ldconsole.exe quit --name {instance}')
            time.sleep(5)

        elif day <= 14:
            print("🎁 Claiming 14-Day Login Reward...")

            for instance_name in instance_names:
                tap_macro(instance_name, 1171, 104)
            time.sleep(10)

            for instance in instance_names:
                os.system(f'ldconsole.exe quit --name {instance}')
            time.sleep(5)

        batch["login_day"] += 1
        batch["last_login"] = datetime.now().strftime("%Y-%m-%d")

    with open(json_path, "w") as f:
        json.dump(batches, f, indent=2)

if __name__ == "__main__":
    claim_login_rewards()