import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import sys
import shutil
import subprocess
import keyboard
from datetime import datetime

# --- CONFIGURATION (ORANGE HACKER THEME) ---
COLOR_BG = "#121212"
COLOR_ACCENT = "#FF6600"
COLOR_BTN = "#333333"
COLOR_QUIT = "#FF0000"
COLOR_TEXT = "#FFFFFF"

class CodeInjectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Injection")
        # חיתוך השטח המת - גובה מינימלי להידוק מקסימלי
        self.root.geometry("440x145")
        self.root.configure(bg=COLOR_BG)

        # Frameless Window
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 1.0)

        self.target_file = None
        self.last_clipboard = ""
        self.is_visible = True

        self.init_ui()
        self.setup_hotkeys()
        self.position_window()
        self.monitor_clipboard()

        # ניקוי מסודר גם אם נסגר דרך מנהל החלונות
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

    def init_ui(self):
        # --- Top Bar ---
        top_bar = tk.Frame(self.root, bg=COLOR_BG)
        top_bar.pack(fill="x", padx=10, pady=(5, 2))

        self.create_btn(top_bar, "Run", self.run_file).pack(side="left", padx=2)
        self.create_btn(top_bar, "CMD", self.run_cmd).pack(side="left", padx=2)
        self.create_btn(top_bar, "Build", self.build_target).pack(side="left", padx=2)

        tk.Label(top_bar, text="Code Injection", fg=COLOR_ACCENT, bg=COLOR_BG,
                 font=("Consolas", 11, "bold")).pack(side="left", expand=True)

        self.create_btn(top_bar, "Help", self.show_help).pack(side="left", padx=2)
        self.create_btn(top_bar, "Quit", self.quit_app, is_quit=True).pack(side="left", padx=2)

        # --- File Info ---
        info_frame = tk.Frame(self.root, bg=COLOR_BG)
        info_frame.pack(fill="x", padx=12)

        self.lbl_target = tk.Label(info_frame, text="Target: None", fg=COLOR_TEXT,
                                   bg=COLOR_BG, font=("Consolas", 8, "bold"))
        self.lbl_target.pack(side="left")

        self.lbl_mod = tk.Label(info_frame, text="Mod: --", fg="#888",
                                bg=COLOR_BG, font=("Consolas", 8))
        self.lbl_mod.pack(side="right")

        # --- Progress Bar ---
        self.progress_canvas = tk.Canvas(self.root, height=3, bg="#1a1a1a", highlightthickness=0)
        self.progress_canvas.pack(fill="x", padx=10, pady=2)
        self.progress_rect = self.progress_canvas.create_rectangle(0, 0, 0, 3, fill=COLOR_ACCENT, width=0)

        # --- Drop Zone (Narrow with thin frame) ---
        self.drop_frame = tk.Frame(self.root, bg=COLOR_BG, highlightbackground="#FFFFFF", highlightthickness=1)
        self.drop_frame.pack(fill="x", padx=10, pady=(2, 4))

        self.drop_zone = tk.Label(self.drop_frame, text="DROP TARGET HERE", fg=COLOR_ACCENT,
                                  bg="#1E1E1E", font=("Consolas", 10, "bold"), pady=4)
        self.drop_zone.pack(fill="x")

        self.drop_zone.drop_target_register(DND_FILES)
        self.drop_zone.dnd_bind('<<Drop>>', self.handle_drop)

        # --- Bottom Bar ---
        bottom_bar = tk.Frame(self.root, bg=COLOR_BG)
        bottom_bar.pack(fill="x", padx=10, pady=(0, 2))

        self.chk_inject = tk.BooleanVar(value=True)
        tk.Checkbutton(bottom_bar, text="Inject", variable=self.chk_inject,
                       fg=COLOR_TEXT, bg=COLOR_BG, selectcolor=COLOR_BG,
                       activeforeground=COLOR_ACCENT, font=("Consolas", 8)).pack(side="left")

        self.chk_ontop = tk.BooleanVar(value=True)
        tk.Checkbutton(bottom_bar, text="Stay On Top", variable=self.chk_ontop,
                       fg=COLOR_TEXT, bg=COLOR_BG, selectcolor=COLOR_BG,
                       command=self.update_ontop, font=("Consolas", 8)).pack(side="left", padx=5)

        self.chk_ghost = tk.BooleanVar(value=False)
        tk.Checkbutton(bottom_bar, text="Ghost", variable=self.chk_ghost,
                       fg=COLOR_TEXT, bg=COLOR_BG, selectcolor=COLOR_BG,
                       font=("Consolas", 8)).pack(side="left")

        tk.Button(bottom_bar, text="...", fg="#888", bg=COLOR_BG, relief="flat",
                  font=("Consolas", 8, "bold"), command=self.restore_and_fix).pack(side="right")

        # Signature
        self.sig = tk.Label(self.root, text="oT", fg="#222", bg=COLOR_BG, font=("Arial", 7))
        self.sig.place(relx=0.99, rely=0.99, anchor="se")

        # Window Dragging & Ghost logic
        top_bar.bind("<Button-1>", self.start_move)
        top_bar.bind("<B1-Motion>", self.do_move)
        self.root.bind("<Enter>", lambda e: self.root.attributes("-alpha", 1.0))
        self.root.bind("<Leave>", self.handle_leave)

    def handle_drop(self, event):
        # DnD ב-Windows עוטף נתיבים עם רווחים ב-{...}; ניקח את הקובץ הראשון בלבד
        data = event.data.strip()
        if data.startswith('{') and '}' in data:
            path = data[1:data.index('}')]
        else:
            path = data.split()[0] if data else ""
        path = path.strip()

        if not path or not os.path.isfile(path):
            return

        if path.lower().endswith('.txt'):
            new_path = path[:-4] + ".py"
            try:
                # os.replace דורס יעד קיים (os.rename נכשל על Windows אם הוא קיים)
                os.replace(path, new_path)
                path = new_path
            except OSError as e:
                self.lbl_mod.config(text="Mod: rename failed")
                print(f"[Code Injection] rename failed: {e}", file=sys.stderr)

        self.target_file = path
        name = os.path.basename(path)
        self.lbl_target.config(text=f"Target: {name}")
        self.lbl_mod.config(text=f"Mod: {datetime.now().strftime('%H:%M:%S')}")
        self.drop_zone.config(bg=COLOR_ACCENT, fg="black", text=name)

    def animate_progress(self):
        # רוחב היעד נגזר מרוחב הקנבס בפועל ולא ממספר קשיח
        target_w = max(self.progress_canvas.winfo_width(), 1)

        def fill(w):
            if w <= target_w:
                self.progress_canvas.coords(self.progress_rect, 0, 0, w, 3)
                self.root.after(5, lambda: fill(w + 40))
            else:
                self.root.after(300, lambda: self.progress_canvas.coords(self.progress_rect, 0, 0, 0, 3))
        fill(0)

    def create_btn(self, parent, text, cmd, is_quit=False):
        color = COLOR_QUIT if is_quit else COLOR_BTN
        return tk.Button(parent, text=text, command=cmd, bg=color, fg=COLOR_TEXT,
                         relief="flat", font=("Consolas", 8, "bold"), width=6)

    def handle_leave(self, event):
        if self.chk_ghost.get():
            self.root.attributes("-alpha", 0.5)

    def update_ontop(self):
        self.root.attributes("-topmost", self.chk_ontop.get())

    def position_window(self):
        screen_h = self.root.winfo_screenheight()
        self.root.geometry(f"+10+{screen_h - 190}")

    def start_move(self, event):
        self.x, self.y = event.x, event.y

    def do_move(self, event):
        deltax, deltay = event.x - self.x, event.y - self.y
        self.root.geometry(f"+{self.root.winfo_x() + deltax}+{self.root.winfo_y() + deltay}")

    def setup_hotkeys(self):
        try:
            keyboard.unhook_all()
            keyboard.add_hotkey('f4', self.toggle_visibility)
        except Exception as e:
            print(f"[Code Injection] hotkey setup failed: {e}", file=sys.stderr)

    def toggle_visibility(self):
        if self.is_visible:
            self.root.withdraw()
        else:
            self.root.deiconify()
            self.root.attributes("-topmost", True)
            self.root.attributes("-alpha", 1.0)
        self.is_visible = not self.is_visible

    def monitor_clipboard(self):
        if self.chk_inject.get() and keyboard.is_pressed('shift'):
            try:
                clip = self.root.clipboard_get()
                if clip != self.last_clipboard:
                    self.last_clipboard = clip
                    self.inject_code(clip)
            except tk.TclError:
                pass  # קליפבורד ריק או לא-טקסטואלי (תמונה וכו')
        self.root.after(100, self.monitor_clipboard)

    def inject_code(self, text):
        if not self.target_file:
            return
        try:
            shutil.copy2(self.target_file, self.target_file + ".txt")
            with open(self.target_file, 'w', encoding='utf-8') as f:
                f.write(text)
            self.animate_progress()
            self.lbl_mod.config(text=f"Mod: {datetime.now().strftime('%H:%M:%S')}")
        except OSError as e:
            self.lbl_mod.config(text="Mod: write failed")
            print(f"[Code Injection] inject failed: {e}", file=sys.stderr)

    def run_file(self):
        if self.target_file and hasattr(os, "startfile"):
            os.startfile(self.target_file)

    def run_cmd(self):
        if not self.target_file:
            return
        folder = os.path.dirname(self.target_file)
        name = os.path.basename(self.target_file)
        # cwd מטפל בתיקייה, כך שאין צורך ב-cd /d עם מרכאות מקוננות
        subprocess.Popen(f'start cmd /k python "{name}"', cwd=folder, shell=True)

    def build_target(self):
        if not self.target_file:
            return
        folder = os.path.normpath(os.path.dirname(self.target_file))
        name = os.path.basename(self.target_file)
        icon_arg = '--icon="icon.ico"' if os.path.exists(os.path.join(folder, "icon.ico")) else ""
        cmd = f'python -m PyInstaller --noconsole --onefile {icon_arg} "{name}"'
        subprocess.Popen(f'start cmd /k "{cmd} && pause"', cwd=folder, shell=True)

    def restore_and_fix(self):
        if self.target_file:
            bak = self.target_file + ".txt"
            if os.path.exists(bak):
                shutil.copy2(bak, self.target_file)
                self.lbl_mod.config(text=f"Mod: {datetime.now().strftime('%H:%M:%S')}")
        self.last_clipboard = ""
        self.setup_hotkeys()

    def show_help(self):
        from tkinter import messagebox
        messagebox.showinfo("Help", "CODE INJECTION MANUAL\n\n"
                            "- Drag any .txt or .py file to Target.\n"
                            "- TXT files auto-convert to PY.\n"
                            "- Hold Shift+Copy to inject code.\n"
                            "- F4 to toggle visibility.")

    def quit_app(self):
        # ניקוי hooks של המקלדת לפני יציאה כדי שהתהליך לא ייתקע
        try:
            keyboard.unhook_all()
        except Exception:
            pass
        self.root.destroy()


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = CodeInjectionApp(root)
    root.mainloop()
