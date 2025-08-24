import multiprocessing
import time
from clone_utils import launch_instance, clone_instance
from config import TOTAL_ACCOUNTS, INSTANCES_PER_BATCH
from macros import tap_macro, swipe_macro
from random import randint
from debug_adb import adb_debugger
from adb_utils import take_screenshot, close_instance, input_guest_name, delete_instance
from template_matching import is_reward_screen
import subprocess
import os
from proxy_config import AIRPROXY
import json
import os
from datetime import datetime

def generate_guest_name(index, prefix):
    result = f"{prefix}{randint(1000, 10000)}x{index}"
    print(f"[NameGen] Index={index}, Result={result}")
    return result

def is_process_running(process_name):
    try:
        # Use tasklist to check if the process is running
        output = subprocess.check_output(f'tasklist /FI "IMAGENAME eq {process_name}"', shell=True).decode()
        return process_name.lower() in output.lower()
    except subprocess.CalledProcessError:
        return False

def launch_with_proxifier(profile_path, instance_name):
    proxifier_path = "C:\\Program Files\\Proxifier\\Proxifier.exe"
    ldplayer_path = "C:\\LDPlayer\\LDPlayer9\\dnplayer.exe"

    if not os.path.exists(proxifier_path):
        print("❌ Proxifier not found at:", proxifier_path)
        return

    if not os.path.exists(profile_path):
        print(f"❌ Proxifier profile not found: {profile_path}")
        return
    
    if not is_process_running("Proxifier.exe"):
        print("Starting Proxifier...")
        try:
            subprocess.Popen([
                proxifier_path,
                "/profile", profile_path,
                "/silent",
                "/run", ldplayer_path,
                "--name", instance_name
            ])
            print(f"✅ Launched {instance_name} via Proxifier profile: {os.path.basename(profile_path)}")
        except Exception as e:
            print(f"❌ Failed to launch {instance_name} with Proxifier: {e}")
    else:
        print("Proxifier is already running.")
        

def prepare_batch(batch_num, instances_per_batch, base_instance, log_func):
    instance_names = []

    for i in range(instances_per_batch):
        unique_num = randint(0, 1000)
        new_name = f"{base_instance}-{unique_num}-{(batch_num - 1) * instances_per_batch + i + 1}"
        clone_instance(base_instance, new_name)
        launch_instance(new_name)

        # 5. Apply proxy if needed
        proxy_ip = AIRPROXY.get("host")
        proxy_port = AIRPROXY.get("port")
        proxy_user = AIRPROXY.get("username")
        proxy_pass = AIRPROXY.get("password")

        if proxy_ip == "127.0.0.1":
            log_func(f"[{new_name}] Skipping proxifier — using localhost")
        else:
            proxifier_profile = f"C:\\ProxifierProfiles\\profile-1.ppx"
            if os.path.exists(proxifier_profile):
                launch_with_proxifier(proxifier_profile, new_name)

        instance_names.append(new_name)

    return instance_names


def run_batch(batch_num, start_guest_index, instances_per_batch, log_func, base_instance, guest_name_prefix, pause_event):
    instance_names = prepare_batch(batch_num, instances_per_batch, base_instance, log_func)
    log_func(f"🛡️ Summoned batch {batch_num} with {len(instance_names)} realms awakening...")
    time.sleep(80)  # Let them boot

    guest_data = []

    print('Clicked')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1055, 130)
    time.sleep(5)

    for i, instance_name in enumerate(instance_names):
        guest_index = start_guest_index + i
        guest_name = generate_guest_name(guest_index, guest_name_prefix)
        guest_data.append((instance_name, guest_name))
        log_func(f"✨ [{instance_name}] Bound to guest spirit")

    for instance_name, _ in guest_data:
        os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell monkey -p com.td.uswatcherofrealms -c android.intent.category.LAUNCHER 1"')
        log_func(f"🚀 [{instance_name}] Realm opened: Watcher of Realms launching...")
    time.sleep(60)

    steps = [
        ("Later", tap_macro, (510, 460), 35),
        ("Not Now", tap_macro, (360, 650), 10),
        ("Accept!", tap_macro, (740, 525), 7),
        ("No Account", tap_macro, (760, 520), 10),
        ("Skip", tap_macro, (1210, 50), 45),
        ("Global", tap_macro, (585, 335), 10),
        ("Global", tap_macro, (585, 335), 10),
        ("Swipe!", swipe_macro, (1215, 660, 480, 375), 3),
        ("Swipe!", swipe_macro, (480, 375, 670, 375), 15),
        ("Global", tap_macro, (585, 335), 10),
        ("Global", tap_macro, (585, 335), 30),
        ("Global", tap_macro, (585, 335), 10),
        ("Hero", tap_macro, (505, 400), 10),
        ("Power", tap_macro, (590, 405), 30),
        ("Coninue!!", tap_macro, (1130, 655), 20),
        ("Coninue!!", tap_macro, (1130, 655), 15),

        ("N1-2", tap_macro, (420, 220), 10),
        ("Fight", tap_macro, (1055, 675), 10),
        ("Hero", tap_macro, (55, 305), 10),
        ("Start", tap_macro, (1145, 585), 15),
        ("Swipe!", swipe_macro, (1095, 655, 600, 285), 3),
        ("Swipe!", swipe_macro, (600, 285, 785, 285), 20),
        ("2x", tap_macro, (1160, 40), 5),
        ("2x", tap_macro, (1160, 40), 90),
        ("Global", tap_macro, (585, 335), 10),
        ("Next", tap_macro, (1130, 655), 5),
        ("Continue", tap_macro, (1130, 655), 15),

        ("N1-3", tap_macro, (530, 290), 10),
        ("Fight", tap_macro, (1055, 675), 10),
        ("Start", tap_macro, (1145, 585), 15),
        ("Global", tap_macro, (585, 335), 5),
        ("Global", tap_macro, (585, 335), 10),
        ("Swipe!", swipe_macro, (1100, 657, 765, 311), 3),
        ("Swipe!", swipe_macro, (765, 311, 563, 294), 3),
        ("2x", tap_macro, (1160, 40), 3),
        ("Swipe!", swipe_macro, (1220, 660, 645, 387), 3),
        ("Swipe!", swipe_macro, (645, 387, 432, 375), 45),
        ("Continue", tap_macro, (1130, 655), 15),
        ("Continue", tap_macro, (1130, 655), 15),
        ("Hero", tap_macro, (170, 655), 20),
        ("Upgrade", tap_macro, (1140, 670), 10),
        ("Upgrade", tap_macro, (935, 575), 15),
        ("Back", tap_macro, (45, 30), 10),
        ("Back", tap_macro, (45, 30), 15),
        ("Continue", tap_macro, (1130, 655), 10),

        ("N1-4", tap_macro, (530, 415), 10),
        ("Fight", tap_macro, (1055, 675), 10),
        ("Hero", tap_macro, (165, 140), 10),
        ("Start", tap_macro, (1145, 585), 12),
        ("Swipe!", swipe_macro, (1105, 657, 945, 305), 3),
        ("Swipe!", swipe_macro, (945, 305, 770, 342), 3),
        ("2x", tap_macro, (1160, 40), 3),
        ("Swipe!", swipe_macro, (1215, 655, 865, 395), 3),
        ("Swipe!", swipe_macro, (865, 395, 865, 285), 70),
        ("Continue", tap_macro, (1130, 655), 15),
        ("Next", tap_macro, (1130, 655), 10),
        ("Complete", tap_macro, (1130, 655), 15),

        ("N1-5", tap_macro, (525, 305), 10),
        ("Fight", tap_macro, (1055, 675), 10),
        ("Hero", tap_macro, (155, 310), 10),
        ("Start", tap_macro, (1145, 585), 15),
        ("Swipe!", swipe_macro, (1092, 653, 765, 280), 3),
        ("Swipe!", swipe_macro, (765, 280, 605, 280), 3),
        ("2x", tap_macro, (1160, 40), 3),
        ("Swipe!", swipe_macro, (1100, 654, 790, 385), 3),
        ("Swipe!", swipe_macro, (790, 385, 790, 275), 8),
        ("Swipe!", swipe_macro, (1220, 657, 645, 400), 3),
        ("Swipe!", swipe_macro, (645, 400, 460, 400), 55),
        ("Global", tap_macro, (585, 335), 10),
        ("Continue", tap_macro, (1130, 655), 8),
        ("Complete", tap_macro, (1130, 655), 15),

        ("N1-6", tap_macro, (525, 335), 10),
        ("Fight", tap_macro, (1055, 675), 10),
        ("Start", tap_macro, (1145, 585), 15),
        ("Swipe!", swipe_macro, (1090, 652, 940, 270), 3),
        ("Swipe!", swipe_macro, (940, 270, 785, 270), 3),
        ("2x", tap_macro, (1220, 660), 5),
        ("2x", tap_macro, (1220, 660), 80),
        ("Next", tap_macro, (1140, 440), 5),
        ("Next", tap_macro, (1140, 440), 10),
        ("Promote", tap_macro, (995, 630), 20),
        ("Okay", tap_macro, (1075, 660), 5),
        ("Back", tap_macro, (45, 30), 15),
        ("Campaign", tap_macro, (1130, 655), 15),

        ("N1-6", tap_macro, (525, 335), 10),
        ("Fight", tap_macro, (1055, 675), 10),
        ("Start", tap_macro, (1145, 585), 15),
        ("Swipe!", swipe_macro, (1100, 655, 942, 391), 3),
        ("Swipe!", swipe_macro, (942, 391, 933, 252), 3),
        ("2x", tap_macro, (1220, 660), 3),
        ("Swipe!", swipe_macro, (1220, 652, 702, 391), 3),
        ("Swipe!", swipe_macro, (702, 391, 930, 308), 5),
        ("Swipe!", swipe_macro, (1220, 662, 800, 220), 3),
        ("Swipe!", swipe_macro, (800, 220, 820, 369), 80),
        ("Complete", tap_macro, (1130, 655), 5),
        ("Complete", tap_macro, (1130, 655), 15),

        ("N1-7", tap_macro, (520, 370), 10),
        ("Fight", tap_macro, (1055, 675), 10),
        ("Start", tap_macro, (1145, 585), 15),
        ("Swipe!", swipe_macro, (1100, 650, 995, 307), 3),
        ("Swipe!", swipe_macro, (995, 307, 875, 307), 3),
        ("2x", tap_macro, (1160, 40), 5),
        ("Swipe!", swipe_macro, (1100, 650, 1095, 300), 3),
        ("Swipe!", swipe_macro, (1095, 300, 975, 300), 5),
        ("Swipe!", swipe_macro, (1090, 645, 940, 237), 3),
        ("Swipe!", swipe_macro, (940, 237, 966, 320), 10),
        ("Swipe!", swipe_macro, (1210, 650, 839, 241), 3),
        ("Swipe!", swipe_macro, (839, 241, 847, 318), 80),
        ("Complete", tap_macro, (1130, 655), 5),
        ("Complete", tap_macro, (1130, 655), 15),

        ("N1-8", tap_macro, (725, 290), 10),
        ("Fight", tap_macro, (1055, 675), 10),
        ("Start", tap_macro, (1145, 585), 15),
        ("Swipe!", swipe_macro, (1100, 660, 380, 390), 3),
        ("Swipe!", swipe_macro, (380, 390, 511, 402), 3),
        ("2x", tap_macro, (1160, 40), 3),
        ("Swipe!", swipe_macro, (1100, 660, 483, 507), 3),
        ("Swipe!", swipe_macro, (483, 507, 500, 375), 10),
        ("Swipe!", swipe_macro, (1220, 645, 395, 291), 3),
        ("Swipe!", swipe_macro, (395, 291, 520, 290), 80),      
        ("Global", tap_macro, (585, 335), 10),
        ("Next", tap_macro, (1130, 655), 10),
        ("Continue", tap_macro, (1130, 655), 15),
    ]

    for log_text, action_func, coords, sleep_duration in steps:
        pause_event.wait()   # ⏸ Wait if paused
        log_func(log_text)
        for instance_name, _ in guest_data:
            pause_event.wait()  # ⏸ Check before adb action
            action_func(instance_name, *coords)
        for _ in range(sleep_duration):
            pause_event.wait()  # ⏸ Allow pause during sleep
            time.sleep(1)


    valid_instances = []
    valid_guest_names = []

    # for instance_name, guest_name in guest_data:
    #     log_func(f"📸 [{instance_name}] Capturing omen for {guest_name}")
    #     take_screenshot(instance_name)
    #     if is_reward_screen(instance_name):
    #         log_func(f"✅ [{instance_name}] 🌟 Destiny fulfilled: Reward screen reached!")
    #         valid_instances.append(instance_name)
    #         valid_guest_names.append(guest_name)

    #         log_func(f"🛑 [{instance_name}] Closing portal")
    #         close_instance(instance_name)
    #     else:
    #         log_func(f"❌ [{instance_name}] ✖️ Fate denied. Shattering instance.")
    #         close_instance(instance_name)
    #         delete_instance(instance_name)

    # log_func(f"🏁 Batch {batch_num} journey concluded.\n")

    # if valid_instances == []:
    #     log_func("⚠️ No champions qualified. Records forsaken.")
    # else:
    #     save_batch_metadata(batch_num, valid_instances, valid_guest_names)

def run_all_batches(base_instance, total_accounts, instances_per_batch, guest_name, log_func, pause_event):
    total_batches = total_accounts // instances_per_batch
    guest_index = 1

    for batch in range(1, total_batches + 1):
        log_func(f"🚀 Starting batch {batch}")
        run_batch(batch, guest_index, instances_per_batch, log_func, base_instance, guest_name, pause_event)
        guest_index += instances_per_batch

def get_persistent_path(filename, subdir=None):
    # Get Windows Local AppData folder, fallback to current dir if env var missing
    base_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'WatcherOfRealms')
    if subdir:
        base_dir = os.path.join(base_dir, subdir)
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, filename)

def save_batch_metadata(batch_index, instance_names, guest_names):
    batch_id = f"batch_{batch_index:03d}"
    batch_data = {
        "batch_id": batch_id,
        "instance_names": instance_names,
        "guest_names": guest_names,
        "login_day": 1,
        "last_login": datetime.now().strftime("%Y-%m-%d"),
        "summon_done": False,
        "screenshot_saved": False
    }

    json_path = get_persistent_path('batches.json')

    try:
        with open(json_path, "r") as f:
            all_batches = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_batches = []

    all_batches.append(batch_data)

    with open(json_path, "w") as f:
        json.dump(all_batches, f, indent=2)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    run_all_batches(TOTAL_ACCOUNTS, INSTANCES_PER_BATCH, print)
