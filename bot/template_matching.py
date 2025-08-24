import cv2
import numpy as np
import os

TEMPLATE_PATHS = ["D:/Silver_Blood_Bot/templates/Template3.png","D:/Silver_Blood_Bot/templates/Template1.png","D:/Silver_Blood_Bot/templates/Template2.png"]
SCREENSHOT_DIR = "D:/Silver_Blood_Bot/screenshots"

def is_reward_screen(instance_name, threshold=0.70):
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"{instance_name}.png")
    screenshot = cv2.imread(screenshot_path, 0)

    if screenshot is None:
        print(f"❌ Could not load screenshot: {screenshot_path}")
        return False

    for template_path in TEMPLATE_PATHS:
        template = cv2.imread(template_path, 0)
        if template is None:
            print(f"❌ Could not load template: {template_path}")
            continue

        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, _, _ = cv2.minMaxLoc(res)

        print(f"🔍 Compared with {template_path}, match: {max_val:.2f}")
        if max_val >= threshold:
            return True  # Success, no need to check other templates

    return False