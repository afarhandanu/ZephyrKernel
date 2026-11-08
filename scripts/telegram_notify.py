#!/usr/bin/env python3
import os
import sys
import glob
import json
import urllib.request
import urllib.parse

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
RELEASE_URL = os.environ.get("RELEASE_URL", "https://github.com/afarhandanu/ZephyrKernel/releases")
KERNEL_VER = os.environ.get("KERNEL_VER", "6.1.187")
LTO_MODE = os.environ.get("LTO_MODE", "thin")
VARIANTS = os.environ.get("VARIANTS", "finasu")

if not BOT_TOKEN or not CHAT_ID:
    print("[WARN] TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is missing. Skipping Telegram notification.")
    sys.exit(0)

MANAGER_URLS = {
    "finasu": "https://github.com/LyraVoid/FinaSU/releases",
    "ksunext": "https://github.com/pershoot/KernelSU-Next/releases",
    "sukisu": "https://github.com/SukiSU-Ultra/SukiSU-Ultra/releases",
    "ksu": "https://github.com/tiann/KernelSU/releases",
    "vanilla": "https://github.com/topjohnwu/Magisk/releases",
}

VARIANT_NAMES = {
    "finasu": "FinaSU v1.5.0+ · SuSFS v2.3.0",
    "ksunext": "KernelSU-Next · SuSFS v2.3.0",
    "sukisu": "SukiSU-Ultra · SuSFS v2.3.0",
    "ksu": "KernelSU (tiann) · SuSFS v2.3.0",
    "vanilla": "Vanilla (Non-Root / Pure GKI)",
}

caption_html = f"""<b>⚡ Zephyr Protocol | {KERNEL_VER}</b>
<blockquote><b>GKI Kernel | Android 14 | Linux 6.1.x</b></blockquote>

<blockquote expandable><b>^ What's Inside?</b>
<b>🛡️ Root & Stealth Integration</b>
• Multi-Variant (FinaSU / KSU-Next / SukiSU / KSU / Vanilla)
• SUSFS v2.3.0 Built-in (11 stealth features)
• Module CRC bypass & GKI symbol unlock (WiFi/BT 100% fix)

<b>🔥 CPU, Scheduler & Toolchain</b>
• BORE CPU Scheduler v6.8.0-rc1 (sched_bore=1)
• Schedutil Catch-up & Workqueue Catch-up
• Neutron Clang 24.0.0git + LLD 24.0.0 (ccache)
• ThinLTO / FullLTO / NoLTO selectable

<b>🧠 Memory & Compression Architecture</b>
• le9uo v1.15 Working Set Protection (MGLRU Off)
• LZ4 v1.10.0 (ARM64 NEON) + ZSTD v1.5.7 (Linux 6.15)
• ZRAM LZ4KD + Kcompressd v0.5 daemon
• UFS WriteBooster Catch-up

<b>🎮 Gaming, Emulation & Hardware</b>
• NTSYNC (/dev/ntsync) Winlator / Wine / Mobox
• Re:Kernel (Port 22 Netlink Server)
• Droidspaces / SYSVIPC (KABI task_struct safe)
• Baseband Security Guard (BBG)
• Full Gamepad FF (DualSense PS5 / DS4 / Xbox)

<b>🌐 Network & Tethering</b>
• TCP BBRv3 + Delayed Boot Enforcer
• CAKE Queue Discipline (Anti-Bufferbloat)
• TTL / HL Target Mangling (Hotspot Quota Bypass)
</blockquote>

<b>📋 Build Information:</b>
• <b>Kernel:</b> <code>Linux {KERNEL_VER}-android14-11-Zephyr</code>
• <b>Builder:</b> <code>kucingbalap1644@ZephyrCI</code>
• <b>Toolchain:</b> <code>Neutron Clang 24.0.0git + LLD 24.0.0 (ccache)</code>
• <b>LTO Mode:</b> <code>{LTO_MODE.upper()}</code>
• <b>Status:</b> <code>Re:Kernel (Port 22) ✅ | LZ4+ZSTD ✅ | MGLRU (Off) ✅</code>

📦 <b>Download Flashable ZIPs di bawah ini:</b>"""

# 1. Send the Main Card Message
send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
inline_keyboard = [
    [
        {"text": "📦 GitHub Release", "url": RELEASE_URL},
        {"text": "⚡ Source Repository", "url": "https://github.com/afarhandanu/ZephyrKernel"}
    ]
]

data = {
    "chat_id": CHAT_ID,
    "text": caption_html,
    "parse_mode": "HTML",
    "reply_markup": json.dumps({"inline_keyboard": inline_keyboard}),
    "disable_web_page_preview": True
}

req = urllib.request.Request(send_url, data=urllib.parse.urlencode(data).encode())
try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        print(f"[OK] Main card sent to Telegram! Message ID: {res.get('result', {}).get('message_id')}")
except Exception as e:
    print(f"[ERROR] Failed to send main card: {e}")

# 2. Upload Built Kernel ZIPs
zip_files = sorted(glob.glob("release_assets/*.zip") + glob.glob("*.zip"))
seen = set()
unique_zips = []
for z in zip_files:
    bname = os.path.basename(z)
    if bname not in seen and not bname.endswith("_full.zip"):
        seen.add(bname)
        unique_zips.append(z)

print(f"[INFO] Found {len(unique_zips)} ZIP packages to upload to Telegram.")

for zpath in unique_zips:
    fname = os.path.basename(zpath)
    # Detect variant
    var_key = "vanilla"
    for k in MANAGER_URLS:
        if f"-{k}-" in fname.lower():
            var_key = k
            break
    
    display_title = VARIANT_NAMES.get(var_key, fname)
    manager_url = MANAGER_URLS.get(var_key, RELEASE_URL)
    
    doc_buttons = [
        [{"text": f"📲 {display_title}", "url": manager_url}]
    ]
    
    doc_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    boundary = "----WebKitFormBoundaryZephyrCI7MA4YWxkTrZu0gW"
    
    body = bytearray()
    
    def add_field(name, val):
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        body.extend(f"{val}\r\n".encode())

    add_field("chat_id", CHAT_ID)
    add_field("caption", f"📦 <b>{fname}</b>")
    add_field("parse_mode", "HTML")
    add_field("reply_markup", json.dumps({"inline_keyboard": doc_buttons}))

    # Add file
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(f'Content-Disposition: form-data; name="document"; filename="{fname}"\r\n'.encode())
    body.extend(b"Content-Type: application/zip\r\n\r\n")
    with open(zpath, "rb") as f:
        body.extend(f.read())
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode())

    req = urllib.request.Request(
        doc_url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    try:
        print(f"Uploading {fname} to Telegram...")
        with urllib.request.urlopen(req) as resp:
            print(f"[OK] Uploaded {fname} successfully!")
    except Exception as e:
        print(f"[WARN] Failed to upload {fname} to Telegram: {e}")

print("=== ALL TELEGRAM NOTIFICATIONS PROCESSED! ===")
