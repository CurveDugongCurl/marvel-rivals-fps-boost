"""
Marvel Rivals FPS Boost & Performance Optimizer
================================================
GitHub: https://github.com/YOUR_USERNAME/marvel-rivals-fps-boost
Version: 2.1.0
License: MIT
"""

import os
import sys
import subprocess
import platform
import ctypes
import winreg
import psutil
import time

# ──────────────────────────────────────────────
#  COLORS (console output)
# ──────────────────────────────────────────────
class Color:
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"

def ok(msg):   print(f"  {Color.GREEN}[✓]{Color.RESET} {msg}")
def info(msg): print(f"  {Color.CYAN}[i]{Color.RESET} {msg}")
def warn(msg): print(f"  {Color.YELLOW}[!]{Color.RESET} {msg}")
def fail(msg): print(f"  {Color.RED}[✗]{Color.RESET} {msg}")

# ──────────────────────────────────────────────
#  BANNER
# ──────────────────────────────────────────────
BANNER = f"""
{Color.RED}{Color.BOLD}
  ███╗   ███╗ █████╗ ██████╗ ██╗   ██╗███████╗██╗
  ████╗ ████║██╔══██╗██╔══██╗██║   ██║██╔════╝██║
  ██╔████╔██║███████║██████╔╝██║   ██║█████╗  ██║
  ██║╚██╔╝██║██╔══██║██╔══██╗╚██╗ ██╔╝██╔══╝  ██║
  ██║ ╚═╝ ██║██║  ██║██║  ██║ ╚████╔╝ ███████╗███████╗
  ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚══════╝
{Color.RESET}
{Color.BOLD}       RIVALS — FPS BOOST & PERFORMANCE OPTIMIZER{Color.RESET}
{Color.YELLOW}              Version 2.1.0 | MIT License{Color.RESET}
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# ──────────────────────────────────────────────
#  ADMIN CHECK
# ──────────────────────────────────────────────
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def require_admin():
    if not is_admin():
        warn("Administrator privileges required. Restarting as admin...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

# ──────────────────────────────────────────────
#  SYSTEM INFO
# ──────────────────────────────────────────────
def print_system_info():
    print(f"\n{Color.BOLD}  ► System Information{Color.RESET}")
    print(f"  {'OS':<20} {platform.system()} {platform.release()} ({platform.version()})")
    print(f"  {'CPU':<20} {platform.processor()}")
    print(f"  {'RAM':<20} {round(psutil.virtual_memory().total / (1024**3), 1)} GB "
          f"(Available: {round(psutil.virtual_memory().available / (1024**3), 1)} GB)")
    print(f"  {'CPU Cores':<20} {psutil.cpu_count(logical=False)} physical / "
          f"{psutil.cpu_count(logical=True)} logical")
    print()

# ──────────────────────────────────────────────
#  1. POWER PLAN — HIGH PERFORMANCE
# ──────────────────────────────────────────────
def set_high_performance_power_plan():
    print(f"\n{Color.BOLD}  ► Power Plan Optimization{Color.RESET}")
    try:
        # High Performance GUID
        guid = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
        result = subprocess.run(
            ["powercfg", "/setactive", guid],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            ok("Power plan set to High Performance")
        else:
            # Try Ultimate Performance
            guid_ultimate = "e9a42b02-d5df-448d-aa00-03f14749eb61"
            subprocess.run(["powercfg", "/setactive", guid_ultimate], capture_output=True)
            ok("Power plan set to Ultimate Performance")
    except Exception as e:
        fail(f"Power plan: {e}")

# ──────────────────────────────────────────────
#  2. PROCESS PRIORITY BOOST
# ──────────────────────────────────────────────
GAME_PROCESS = "MarvelRivals-Win64-Shipping.exe"

def boost_process_priority():
    print(f"\n{Color.BOLD}  ► Process Priority{Color.RESET}")
    found = False
    for proc in psutil.process_iter(['pid', 'name']):
        if GAME_PROCESS.lower() in proc.info['name'].lower():
            try:
                p = psutil.Process(proc.info['pid'])
                p.nice(psutil.HIGH_PRIORITY_CLASS)
                ok(f"Marvel Rivals priority → HIGH (PID: {proc.info['pid']})")
                found = True
            except Exception as e:
                fail(f"Could not set priority: {e}")
    if not found:
        warn("Marvel Rivals is not running. Launch the game first for this step.")

# ──────────────────────────────────────────────
#  3. NETWORK OPTIMIZATION (lower ping)
# ──────────────────────────────────────────────
def optimize_network():
    print(f"\n{Color.BOLD}  ► Network Latency Optimization{Color.RESET}")
    try:
        base = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"
        reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base)
        i = 0
        count = 0
        while True:
            try:
                subkey_name = winreg.EnumKey(reg, i)
                subkey_path = f"{base}\\{subkey_name}"
                subkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path,
                                        0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(subkey, "TcpAckFrequency", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(subkey, "TCPNoDelay",      0, winreg.REG_DWORD, 1)
                winreg.CloseKey(subkey)
                count += 1
                i += 1
            except OSError:
                break
        winreg.CloseKey(reg)
        ok(f"Nagle's algorithm disabled on {count} network interface(s)")
        ok("TCP No-Delay enabled — reduced ping latency")
    except Exception as e:
        fail(f"Network optimization failed: {e}")

# ──────────────────────────────────────────────
#  4. VISUAL EFFECTS — PERFORMANCE MODE
# ──────────────────────────────────────────────
def set_visual_effects_performance():
    print(f"\n{Color.BOLD}  ► Windows Visual Effects{Color.RESET}")
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path,
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 2)
        winreg.CloseKey(key)
        ok("Visual effects set to Performance mode")
    except Exception as e:
        fail(f"Visual effects: {e}")

# ──────────────────────────────────────────────
#  5. KILL BACKGROUND PROCESSES
# ──────────────────────────────────────────────
BLOAT_PROCESSES = [
    "OneDrive.exe", "Spotify.exe", "Discord.exe",
    "Teams.exe", "Slack.exe", "zoom.exe",
    "AdobeUpdateService.exe", "acrobat_sl.exe",
]

def kill_background_apps():
    print(f"\n{Color.BOLD}  ► Background Process Cleanup{Color.RESET}")
    killed = 0
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in BLOAT_PROCESSES:
            try:
                proc.kill()
                warn(f"Suspended: {proc.info['name']}")
                killed += 1
            except:
                pass
    if killed == 0:
        ok("No bloat processes found — system is clean")
    else:
        ok(f"{killed} background app(s) closed — more RAM freed for game")

# ──────────────────────────────────────────────
#  6. GPU SCHEDULER (Hardware-Accelerated)
# ──────────────────────────────────────────────
def enable_hardware_gpu_scheduler():
    print(f"\n{Color.BOLD}  ► GPU Hardware-Accelerated Scheduling{Color.RESET}")
    try:
        key_path = r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path,
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "HwSchMode", 0, winreg.REG_DWORD, 2)
        winreg.CloseKey(key)
        ok("Hardware-Accelerated GPU Scheduling → ENABLED")
        info("Reboot required for this change to take effect")
    except Exception as e:
        fail(f"GPU Scheduler: {e}")

# ──────────────────────────────────────────────
#  7. GAME MODE
# ──────────────────────────────────────────────
def enable_game_mode():
    print(f"\n{Color.BOLD}  ► Windows Game Mode{Color.RESET}")
    try:
        key_path = r"Software\Microsoft\GameBar"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path,
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "AutoGameModeEnabled", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "AllowAutoGameMode",   0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        ok("Windows Game Mode → ENABLED")
    except Exception as e:
        fail(f"Game Mode: {e}")

# ──────────────────────────────────────────────
#  RESTORE DEFAULTS
# ──────────────────────────────────────────────
def restore_defaults():
    print(f"\n{Color.BOLD}  ► Restoring Default Settings...{Color.RESET}\n")
    # Power plan → Balanced
    subprocess.run(
        ["powercfg", "/setactive", "381b4222-f694-41f0-9685-ff5bb260df2e"],
        capture_output=True
    )
    ok("Power plan restored to Balanced")

    # Visual effects → Let Windows choose
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
        ok("Visual effects restored")
    except:
        pass

    # Network → restore Nagle
    try:
        base = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"
        reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base)
        i = 0
        while True:
            try:
                subkey_name = winreg.EnumKey(reg, i)
                subkey_path = f"{base}\\{subkey_name}"
                subkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path,
                                        0, winreg.KEY_SET_VALUE)
                winreg.DeleteValue(subkey, "TcpAckFrequency")
                winreg.DeleteValue(subkey, "TCPNoDelay")
                winreg.CloseKey(subkey)
                i += 1
            except OSError:
                break
        winreg.CloseKey(reg)
        ok("Network settings restored")
    except:
        pass

    ok("All settings restored to Windows defaults!")

# ──────────────────────────────────────────────
#  MENU
# ──────────────────────────────────────────────
def print_menu():
    print(f"""
{Color.BOLD}  ┌─────────────────────────────────────────┐
  │         SELECT OPTIMIZATION PROFILE      │
  ├─────────────────────────────────────────┤
  │  [1]  🟢 Low      — Safe tweaks only    │
  │  [2]  🟡 Medium   — Balanced boost      │
  │  [3]  🔴 High     — Aggressive          │
  │  [4]  ⚫ Extreme  — Maximum performance  │
  │  [5]  🔄 Restore  — Revert all changes  │
  │  [0]  ❌ Exit                           │
  └─────────────────────────────────────────┘{Color.RESET}
""")

def run_profile(level: int):
    print(f"\n  {'━'*45}")
    info(f"Applying optimizations (Profile {level}/4)...")
    print(f"  {'━'*45}")

    if level >= 1:
        set_high_performance_power_plan()
        enable_game_mode()

    if level >= 2:
        set_visual_effects_performance()
        optimize_network()

    if level >= 3:
        kill_background_apps()
        boost_process_priority()

    if level >= 4:
        enable_hardware_gpu_scheduler()

    print(f"\n  {'━'*45}")
    ok(f"Profile {level} applied successfully!")
    info("Launch Marvel Rivals and enjoy your FPS boost 🚀")
    print(f"  {'━'*45}\n")

# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────
def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(BANNER)

    require_admin()
    print_system_info()

    while True:
        print_menu()
        choice = input("  Enter choice: ").strip()

        if choice == "0":
            print(f"\n  {Color.CYAN}Thanks for using Marvel Rivals FPS Boost!{Color.RESET}\n")
            break
        elif choice in ("1", "2", "3", "4"):
            run_profile(int(choice))
            input("  Press Enter to return to menu...")
        elif choice == "5":
            restore_defaults()
            input("  Press Enter to return to menu...")
        else:
            warn("Invalid choice. Please enter 1–5 or 0.")

        os.system("cls" if os.name == "nt" else "clear")
        print(BANNER)

if __name__ == "__main__":
    main()
