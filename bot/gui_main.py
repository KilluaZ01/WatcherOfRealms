import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import subprocess
from parallel_runner import run_all_batches


class BotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Watcher of Realms Bot")
        self.geometry("800x580")
        self.configure(bg="#1e1e20")

        # Create pause event (default = running)
        self.pause_event = threading.Event()
        self.pause_event.set()

        self.style = ttk.Style(self)
        self.configure_style()
        self.create_widgets()

        if self.check_task_exists():
            self.auto_claim_enabled = True
            self.btn_toggle_auto.config(text="🟢 Disable Auto-Claim")
        else:
            self.auto_claim_enabled = False
            self.btn_toggle_auto.config(text="⚪ Enable Auto-Claim")

    def configure_style(self):
        self.style.theme_use("default")
        self.style.configure("TLabel", background="#2b2c30", foreground="#f3cc6c", font=("Cinzel", 11, "bold"))
        self.style.configure("TEntry", fieldbackground="#3a3b40", foreground="#ffffff", insertcolor="white")
        self.style.configure("TButton",
                             background="#3b5b5b",
                             foreground="#ffffff",
                             font=("Segoe UI", 10, "bold"),
                             padding=8)
        self.style.map("TButton",
                       background=[("active", "#517878")],
                       foreground=[("active", "#ffffff")])

    def check_task_exists(self, task_name="SilverBloodAutoClaim"):
        result = subprocess.run(f'schtasks /Query /TN {task_name}', shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0
    
    def toggle_pause(self):
        if self.pause_event.is_set():
            self.pause_event.clear()
            self.btn_pause.config(text="▶ Resume Bot")
            self.log("⏸ Bot paused.")
        else:
            self.pause_event.set()
            self.btn_pause.config(text="⏸ Pause Bot")
            self.log("▶ Bot resumed.")

    def toggle_auto_claim(self):
        time_str = self.claim_time_entry.get().strip()
        try:
            hour, minute = map(int, time_str.split(":"))
            if not (0 <= hour < 24 and 0 <= minute < 60):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Time", "Please enter a valid time in HH:MM format.")
            return

        task_name = "WatcherOfRealmsAutoClaim"
        exe_path = "D:/Watcher_of_Realms/daily_claim_runner.exe"

        if not self.auto_claim_enabled:
            command = f'schtasks /Create /F /SC DAILY /TN {task_name} /TR "{exe_path}" /ST {time_str}'
            disable_conditions = (
                f'powershell -Command "'
                f'$task = Get-ScheduledTask -TaskName \'{task_name}\'; '
                f'$task.Settings.DisallowStartIfOnBatteries = $false; '
                f'$task.Settings.StopIfGoingOnBatteries = $false; '
                f'Set-ScheduledTask -TaskName \'{task_name}\' -Settings $task.Settings"'
            )
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            subprocess.run(disable_conditions, shell=True)
            if result.returncode == 0:
                self.log(f"✅ Scheduled daily claim at {time_str}")
                self.btn_toggle_auto.config(text="🟢 Disable Auto-Claim")
                self.auto_claim_enabled = True
            else:
                self.log(f"❌ Failed to schedule task: {result.stderr}")
        else:
            command = f'schtasks /Delete /F /TN {task_name}'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.log("🗑️ Auto-claim task removed.")
                self.btn_toggle_auto.config(text="⚪ Enable Auto-Claim")
                self.auto_claim_enabled = False
            else:
                self.log(f"❌ Failed to remove task: {result.stderr}")

    def create_widgets(self):
        # === HEADER ===
        header = tk.Label(self, text="WATCHER OF REALMS BOT", bg="#1e1e20",
                          fg="#f3cc6c", font=("Cinzel Decorative", 20, "bold"))
        header.pack(pady=(10, 25))

        # === MAIN FRAME ===
        main_frame = tk.Frame(self, bg="#1e1e20")
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # === LEFT PANEL ===
        left_panel = tk.Frame(main_frame, bg="#2b2c30")
        left_panel.pack(side="left", fill="y", padx=(0, 15))

        fields = [
            ("Base Instance Name:", "Base_Instance"),
            ("Total Accounts:", "2"),
            ("Batch Size:", "1"),
            ("Guest Name:", "RealmHero")
        ]

        self.entries = {}
        for label_text, default in fields:
            label = ttk.Label(left_panel, text=label_text)
            label.pack(anchor="w", pady=(10, 4), padx=10)
            entry = ttk.Entry(left_panel, width=28)
            entry.insert(0, default)
            entry.pack(padx=10)
            self.entries[label_text] = entry

        ttk.Label(left_panel, text="Auto-Claim Time (HH:MM):").pack(anchor="w", pady=(15, 4), padx=10)
        self.claim_time_entry = ttk.Entry(left_panel, width=28)
        self.claim_time_entry.insert(0, "09:00")
        self.claim_time_entry.pack(padx=10)

        # Buttons
        self.btn_toggle_auto = ttk.Button(left_panel, text="⚪ Enable Auto-Claim", command=self.toggle_auto_claim)
        self.btn_toggle_auto.pack(pady=(20, 8), padx=10, fill='x')

        # Start Button
        self.btn_start = ttk.Button(left_panel, text="▶ Start Bot", command=self.start_bot_thread)
        self.btn_start.pack(pady=(5, 8), padx=10, fill='x')

        # Pause/Resume Button
        self.btn_pause = ttk.Button(left_panel, text="⏸ Pause Bot", command=self.toggle_pause)
        self.btn_pause.pack(pady=(5, 20), padx=10, fill='x')
        
        # === RIGHT PANEL (LOGS) ===
        right_panel = tk.Frame(main_frame, bg="#1e1e20")
        right_panel.pack(side="right", fill="both", expand=True)

        log_label = tk.Label(right_panel, text="Execution Log", bg="#1e1e20",
                             fg="#f3cc6c", font=("Segoe UI", 11, "bold"))
        log_label.pack(anchor="w", padx=5)

        self.log_area = scrolledtext.ScrolledText(
            right_panel,
            width=65,
            height=24,
            font=("Consolas", 9),
            bg="#111114",
            fg="#a3ffe7",
            insertbackground="white",
            borderwidth=2,
            relief="groove"
        )
        self.log_area.configure(state='disabled')
        self.log_area.pack(fill="both", expand=True, pady=(8, 0))

    def log(self, message):
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state='disabled')

    def start_bot_thread(self):
        try:
            base_instance = self.entries["Base Instance Name:"].get()
            total_accounts = int(self.entries["Total Accounts:"].get())
            batch_size = int(self.entries["Batch Size:"].get())
            guest_name = self.entries["Guest Name:"].get()

            if total_accounts < 1 or batch_size < 1:
                raise ValueError("Values must be positive integers.")
            if batch_size > total_accounts:
                raise ValueError("Batch size cannot exceed total accounts.")
        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))
            return

        self.btn_start.config(state='disabled')
        threading.Thread(
            target=self.run_bot,
            args=(base_instance, total_accounts, batch_size, guest_name, self.log, self.pause_event),
            daemon=True
        ).start()


    def run_bot(self, base_instance, total_accounts, batch_size, guest_name, log_func, pause_event):
        try:
            run_all_batches(base_instance, total_accounts, batch_size, guest_name, log_func, pause_event)
            self.log("✅ Bot run completed successfully")
        except Exception as e:
            self.log(f"❌ Error during bot run: {e}")
        finally:
            self.btn_start.config(state='normal')

if __name__ == "__main__":
    app = BotGUI()
    app.mainloop()
