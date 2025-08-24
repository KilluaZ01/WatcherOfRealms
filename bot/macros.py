import os
import time

def tap_macro(instance_name, x, y):
    tap_command = f'ldconsole.exe adb --name {instance_name} --command "shell input tap {x} {y}"'
    os.system(tap_command)

def swipe_macro(instance_name, x1, y1, x2, y2):
    tap_command = f'ldconsole.exe adb --name {instance_name} --command "shell input touchscreen swipe {x1} {y1} {x2} {y2} 1000"'
    os.system(tap_command)

def claim_7_day_rewards(instance_names, log_func=print):
    log_func("📦 Claiming 7-Day Login Reward...")

    for instance_name in instance_name:
        tap_macro(instance_name, 1171, 104)
    time.sleep(10)

    for instance_name in instance_name:
        tap_macro(instance_name, 1171, 104)
    time.sleep(10)

    for instance_name in instance_name:
        tap_macro(instance_name, 1171, 104)
    time.sleep(10)

def claim_14_day_rewards(instance_names, log_func=print):
    log_func("🎁 Claiming 14-Day Login Reward...")

    for instance_name in instance_name:
        tap_macro(instance_name, 1171, 104)
    time.sleep(10)

    for instance in instance_names:
        os.system(f'ldconsole.exe quit --name {instance}')
    time.sleep(5)

