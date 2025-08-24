import os

def clone_instance(base_name, new_name):
    print(f"Cloning {base_name} → {new_name}...")
    os.system(f'"ldconsole.exe copy --name {new_name} --from {base_name}')

def launch_instance(name):
    print(f"Launching {name}...")
    os.system(f'"ldconsole.exe launch --name {name}')
