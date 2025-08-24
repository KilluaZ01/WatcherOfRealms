from adb_utils import take_screenshot, close_instance
import time

def run_cycle(instance_name, guest_name):
    print(f"[{instance_name}] 🎮 Finishing run cycle for {guest_name}")

    # Optional: wait to make sure macro has finished (if not already done)
    time.sleep(10)

    # Take screenshot of the result (10x summon result screen)
    take_screenshot(instance_name, guest_name)
    print(f"[{instance_name}] 📸 Screenshot saved for {guest_name}")

    # Close the instance
    close_instance(instance_name)
    print(f"[{instance_name}] ❌ Closed instance")
