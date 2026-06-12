```
  ██████╗ ██████╗ ██████╗ ███████╗    ██╗███╗   ██╗     ██╗███████╗ ██████╗████████╗
 ██╔════╝██╔═══██╗██╔══██╗██╔════╝    ██║████╗  ██║     ██║██╔════╝██╔════╝╚══██╔══╝
 ██║     ██║   ██║██║  ██║█████╗      ██║██╔██╗ ██║     ██║█████╗  ██║        ██║
 ██║     ██║   ██║██║  ██║██╔══╝      ██║██║╚██╗██║██   ██║██╔══╝  ██║        ██║
 ╚██████╗╚██████╔╝██████╔╝███████╗    ██║██║ ╚████║╚█████╔╝███████╗╚██████╗   ██║
  ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝    ╚═╝╚═╝  ╚═══╝ ╚════╝ ╚══════╝ ╚═════╝   ╚═╝
            >> THE AI-TO-CODE WORKFLOW ACCELERATOR  ::  by oT <<
```

```
 THEME ............ ORANGE HACKER  (#FF6600 on #121212)
 FONT ............. Consolas
 PLATFORM ......... Windows 10 / 11
 STATUS ........... [ ONLINE ]
```

---

# `[ 0x00 ]` OVERVIEW

**Code Injection** is a tiny, always-on-top, frameless desktop utility that acts
as a *bridge* between an AI chatbot in your browser and a real `.py` file on disk.

The loop it accelerates:

```
   COPY code from AI  ──►  Code Injection overwrites your target file  ──►  RUN / BUILD
        (hold Shift)              (auto-backup kept)                    (one click)
```

No IDE. No manual paste. No save dialog. Copy → it lands in the file → run it.

---

# `[ 0x01 ]` REQUIREMENTS & INSTALL

```
 OS .......... Windows 10 / 11
 PYTHON ...... 3.8+  (needed to RUN scripts and BUILD .exe)
```

Install the dependencies:

```bash
pip install tkinterdnd2 keyboard pyinstaller
```

Run it:

```bash
python CodeInjection.py
```

> NOTE: `keyboard` registers **global** hotkeys. On some systems it needs to be
> run as Administrator for the `Shift`-watch and `F4` toggle to work everywhere.

---

# `[ 0x02 ]` THE INTERFACE  ::  CONTROL BY CONTROL

```
 ┌─────────────────────────────────────────────────────────────┐
 │ [Run][CMD][Build]      Code Injection        [Help][Quit]    │  ◄── TOP BAR
 │ Target: main.py                              Mod: 14:03:51   │  ◄── FILE INFO
 │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │  ◄── PROGRESS
 │ ┌─────────────────────────────────────────────────────────┐ │
 │ │                  DROP TARGET HERE                        │ │  ◄── DROP ZONE
 │ └─────────────────────────────────────────────────────────┘ │
 │ [x]Inject  [x]Stay On Top  [ ]Ghost                    ...   │  ◄── BOTTOM BAR
 └─────────────────────────────────────────────────────────── oT┘  ◄── SIGNATURE
```

### TOP BAR

| Button   | Action |
|----------|--------|
| **Run**  | Opens / executes the target file with the OS default handler (`os.startfile`). For a `.py` this runs it. |
| **CMD**  | Opens a Command Prompt **in the file's folder** and runs `python <file>` — perfect for reading tracebacks. The window stays open (`cmd /k`). |
| **Build**| Compiles the target into a standalone `.exe` via PyInstaller (`--noconsole --onefile`). Auto-attaches `icon.ico` if one exists next to the script. |
| **Help** | Pops the quick in-app manual (`messagebox`). |
| **Quit** | Clean shutdown — releases the global keyboard hooks first, then closes. (Red = danger.) |

> Dragging the **top bar** with the mouse moves the whole frameless window.

### FILE INFO

| Field      | Meaning |
|------------|---------|
| **Target** | The currently loaded file. `None` until you drop one. |
| **Mod**    | Timestamp of the last write/inject/restore — your "last touched" indicator. |

### PROGRESS BAR

A thin orange sweep that animates left-to-right on every successful injection —
pure visual confirmation that the write landed. Its length now scales with the
window width (no fixed pixel value).

### DROP ZONE

The big **DROP TARGET HERE** panel. Drag any `.py` (or `.txt`) onto it to arm it.
On success the panel turns **orange** and shows the file name.

### BOTTOM BAR

| Control          | Effect |
|------------------|--------|
| **Inject** ☑     | Master safety switch. When **off**, the Shift-watch is disabled — nothing is ever overwritten. Turn it off to prevent accidental writes. |
| **Stay On Top** ☑| Keeps the window above all others (`-topmost`). |
| **Ghost** ☐      | When the mouse **leaves** the window it fades to 50% opacity (`-alpha 0.5`); hovering back restores it to 100%. Keeps it out of the way without hiding it. |
| **`...`**        | RESTORE. Copies the `.txt` backup back over the target (undo the last injection) and re-arms the hotkeys. |

### SIGNATURE

The faint `oT` in the bottom-right corner. Author mark.

---

# `[ 0x03 ]` THE INJECTION MECHANISM  (how the magic works)

This is the core feature. Step by step:

```
 1. Arm a target          → drag a file onto the DROP ZONE.
 2. Keep "Inject" ON.
 3. In your browser, select AI-generated code and press  SHIFT + Ctrl+C
    (hold SHIFT while copying).
 4. A 100 ms loop notices: Inject is on  AND  Shift is held  AND  the
    clipboard text CHANGED since last time.
 5. Before writing, the current target is backed up to  <file>.py.txt
 6. The clipboard text is written into the target file (UTF-8, overwrite).
 7. Progress bar sweeps, "Mod" timestamp updates.  Done.
```

Key points:
- **Backup every time** — the previous content is always preserved as `<file>.txt`
  so the `...` RESTORE button can undo a bad paste.
- **Change detection** — it only writes when the clipboard *differs* from the last
  value, so holding Shift won't spam-rewrite the same code.
- **Shift is the trigger** — without holding Shift, normal copying never touches
  your file. That is your safety gate alongside the **Inject** checkbox.

---

# `[ 0x04 ]` FILE HANDLING

```
 .txt dropped  ──►  auto-renamed to  .py     (instant, ready to run)
 every inject  ──►  prior content saved to   <file>.py.txt   (backup)
 RESTORE (...)  ──►  <file>.py.txt copied back over the target
```

- The auto-convert uses `os.replace`, so it safely overwrites an existing `.py`
  of the same name instead of crashing.
- Backups use the `.py.txt` suffix and are ignored by git via `.gitignore`.

---

# `[ 0x05 ]` KEYBOARD SHORTCUTS

| Key            | Action |
|----------------|--------|
| `F4`           | Toggle window visibility (hide / show). On show it re-asserts topmost + full opacity. |
| `Shift` (hold) | Arms the clipboard-watch while copying — the inject trigger. |

---

# `[ 0x06 ]` BUILDING AN .EXE

Press **Build** to wrap the target into a single distributable executable:

```bash
python -m PyInstaller --noconsole --onefile [--icon="icon.ico"] "<target>.py"
```

- `--onefile` → one self-contained `.exe`.
- `--noconsole` → no black console window on launch (GUI apps).
- `--icon` → auto-added **only** if an `icon.ico` sits next to the script.
- Runs inside `cmd /k ... && pause` so you can read PyInstaller's output and any
  errors before the window closes. The finished `.exe` lands in `dist\`.

---

# `[ 0x07 ]` THE TECH STACK  (what each part is built from)

| Technology       | Role in Code Injection |
|------------------|------------------------|
| **Python 3**     | The whole application runtime. |
| **tkinter**      | The GUI toolkit — every frame, label, button, checkbox and the `Canvas` progress bar. |
| **tkinterdnd2**  | Adds native **drag-and-drop** of files into the window (`DND_FILES`, `<<Drop>>`), which stock tkinter cannot do. `TkinterDnD.Tk()` replaces the normal root. |
| **keyboard**     | Registers **global** hotkeys (`F4`) and polls modifier state (`is_pressed('shift')`) even when the window isn't focused. |
| **subprocess**   | Launches external `cmd` sessions for the **CMD** and **Build** actions (`Popen(..., cwd=folder)`). |
| **os**           | Path handling, `os.startfile` (Run), and `os.replace` (the `.txt→.py` convert). |
| **shutil**       | `copy2` for the backup + restore flow (preserves metadata). |
| **datetime**     | The `Mod:` timestamps. |
| **PyInstaller**  | External compiler invoked by **Build** to produce a standalone `.exe`. |

### Window tricks used

```
 overrideredirect(True) ... frameless window (no title bar / borders)
 -topmost ................. always-on-top
 -alpha ................... opacity (1.0 normal, 0.5 in Ghost mode)
 Canvas rectangle ......... the animated progress sweep
 after(100, ...) .......... the non-blocking clipboard polling loop
```

---

# `[ 0x08 ]` TROUBLESHOOTING

| Symptom | Cause / Fix |
|---------|-------------|
| Hotkeys / Shift-watch do nothing | `keyboard` needs elevated rights on some setups — run as Administrator. |
| Nothing injects | Is **Inject** checked? Is a **Target** loaded? Are you holding **Shift** while copying? |
| `Mod: write failed` | The target is locked / read-only / open elsewhere. Close it and retry. |
| `Mod: rename failed` | The `.txt→.py` rename hit a permissions or path issue — check the folder. |
| Window vanished | Press `F4` to bring it back. |
| Build does nothing | PyInstaller not installed → `pip install pyinstaller`. |
| Runs only on Windows | The `os.startfile` / `start cmd` calls are Windows-specific by design. |

---

# `[ 0x09 ]` SAFETY NOTES

- The **Inject** checkbox is your master kill-switch — turn it off when you're not
  actively pulling code, so nothing gets overwritten by accident.
- Every injection keeps a `.py.txt` backup; the `...` button restores it.
- `Code Injection` overwrites the **whole** target file each time — it does not
  merge or patch. Keep important work in version control.

---

```
 ╔══════════════════════════════════════════════════════════════╗
 ║  CODE INJECTION  ::  Freeware (Non-Commercial)  ::  by  oT    ║
 ╚══════════════════════════════════════════════════════════════╝
```
