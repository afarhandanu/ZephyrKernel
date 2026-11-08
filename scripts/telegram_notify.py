#!/usr/bin/env python3
import os
import sys
import glob
import json
import random
import urllib.request
import subprocess

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
RELEASE_URL = os.environ.get("RELEASE_URL", "https://github.com/afarhandanu/ZephyrKernel/releases")
KERNEL_VER = os.environ.get("KERNEL_VER", "6.1.187")
LTO_MODE = os.environ.get("LTO_MODE", "thin")

if not BOT_TOKEN or not CHAT_ID:
    print("[WARN] TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID missing. Skipping Telegram post.")
    sys.exit(0)

# 1. Resolve LTO display
lto_raw = LTO_MODE.lower()
if lto_raw == "all":
    lto_html = '<tg-button type="disabled" style="success">ThinLTO</tg-button> <tg-button type="disabled" style="primary">FullLTO</tg-button> <tg-button type="disabled" style="danger">NoLTO</tg-button>'
elif lto_raw == "full":
    lto_html = '<tg-button type="disabled" style="primary">FullLTO</tg-button>'
elif lto_raw == "none":
    lto_html = '<tg-button type="disabled" style="danger">NoLTO</tg-button>'
else:
    lto_html = '<tg-button type="disabled" style="success">ThinLTO</tg-button>'

# 2. Resolve Banner (Pick random real HD cat meme banner from banner pool)
BANNER_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "release", "telegram", "banner")
banner_candidates = sorted(glob.glob(os.path.join(BANNER_DIR, "banner_*.*")))
if not banner_candidates:
    banner_candidates = sorted([
        f for f in glob.glob(os.path.join(BANNER_DIR, "*"))
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])
banner_path = random.choice(banner_candidates) if banner_candidates else None
if banner_path:
    print(f"[Telegram] Selected random cat meme banner: {os.path.basename(banner_path)}")

# 3. Build Rich Message Payload
rich_markdown = f"""<tg-slideshow>
<img src="tg://photo?id=banner1" />
</tg-slideshow>

# ⚡ ZephyrKernel | {KERNEL_VER}
> GKI Kernel | Android 14 | Linux 6.1.x

<details>
<summary><tg-button type="disabled" style="primary">What's Inside?</tg-button></summary>

<tg-button-row><tg-button type="disabled">Core Features</tg-button></tg-button-row>

<details>
<summary>Filesystem</summary>

- Mountify / OverlayFS
- F2FS Extended Attributes
- POSIX ACL
</details>

<details>
<summary>Memory</summary>

- ZRAM (LZ4 compression)
- Memory Tracking
- Writeback Support
</details>

<details>
<summary>CPU & Scheduler</summary>

- Ondemand Governor (included)
- Frame Warning Disabled
- I/O Scheduler (MQ-Deadline, Kyber)
</details>

<details>
<summary>Network</summary>

- TCP Congestion Control: BBR, BIC, CUBIC, Westwood, HTCP
- Network Schedulers: FQ, FQ_CoDel, CAKE, PIE, FQ-PIE
- IP Set
- IPv6 NAT
- TTL Target (Netfilter)
</details>

<details>
<summary>Debug</summary>

- Full Kallsyms
- UBSAN Disabled
- Page Owner Disabled
- RCU Trace Disabled
</details>

<details>
<summary>Zephyr & Luminaire Tuning</summary>

<table bordered>
<tr><td>BORE v6.8.0-rc1</td></tr>
<tr><td>BBRv3</td></tr>
<tr><td>BBG</td></tr>
<tr><td>WireGuard</td></tr>
<tr><td>le9uo v1.15</td></tr>
<tr><td>Kcompressd v0.5</td></tr>
<tr><td>Workqueue Catch-up</td></tr>
<tr><td>Schedutil Catch-up</td></tr>
<tr><td>UFS WriteBooster Catch-up</td></tr>
<tr><td>Re:Kernel Port 22</td></tr>
<tr><td>NTSYNC /dev/ntsync</td></tr>
<tr><td>LZ4 v1.10.0 + ZSTD v1.5.7</td></tr>
<tr><td>SYSVIPC Droidspaces</td></tr>
<tr><td>SUSFS v2.3.0 Built-in</td></tr>
</table>
</details>
</details>

<table bordered>
<tr><td>Kernel</td><td>Linux {KERNEL_VER}</td></tr>
<tr><td>Source</td><td><tg-button type="url" url="https://github.com/afarhandanu/ZephyrKernel">ZephyrKernel</tg-button></td></tr>
<tr><td>Branch</td><td><tg-button type="url" url="https://github.com/afarhandanu/ZephyrKernel">main</tg-button></td></tr>
<tr><td>Toolchain</td><td>Neutron Clang 24.0.0git + LLD 24.0.0</td></tr>
<tr><td>LTO</td><td>{lto_html}</td></tr>
</table>

<table bordered>
<tr><td>Mountless Engine</td><td><tg-button type="disabled">None</tg-button></td></tr>
<tr><td>Droidspaces</td><td><tg-button type="disabled" style="success">Enable</tg-button></td></tr>
<tr><td>Re:Kernel</td><td><tg-button type="disabled" style="success">Enable</tg-button></td></tr>
<tr><td>NTSync</td><td><tg-button type="disabled" style="success">Enable</tg-button></td></tr>
<tr><td>LZ4+ZSTD</td><td><tg-button type="disabled" style="success">Enable</tg-button></td></tr>
<tr><td>LZ4KD</td><td><tg-button type="disabled" style="success">Enable</tg-button></td></tr>
<tr><td>MGLRU</td><td><tg-button type="disabled" style="danger">Disable</tg-button></td></tr>
</table>

<tg-button-row><tg-button type="url" style="primary" url="https://github.com/LyraVoid/FinaSU/releases">FinaSU v1.5.0+ · SuSFS v2.3.0</tg-button></tg-button-row>
<tg-button-row><tg-button type="url" style="primary" url="https://github.com/pershoot/KernelSU-Next/releases">KernelSU-Next · SuSFS v2.3.0</tg-button></tg-button-row>
<tg-button-row><tg-button type="url" style="primary" url="https://github.com/SukiSU-Ultra/SukiSU-Ultra/releases">SukiSU-Ultra · SuSFS v2.3.0</tg-button></tg-button-row>
<tg-button-row><tg-button type="url" style="primary" url="https://github.com/tiann/KernelSU/releases">KernelSU · SuSFS v2.3.0</tg-button></tg-button-row>
<tg-button-row><tg-button type="url" style="primary" url="{RELEASE_URL}">Vanilla (Non-Root / Pure GKI)</tg-button></tg-button-row>

<tg-button-row>
  <tg-button type="url" style="primary" url="{RELEASE_URL}">📦 GitHub Release</tg-button>
  <tg-button type="url" style="primary" url="https://github.com/afarhandanu/ZephyrKernel">⚡ Repository</tg-button>
</tg-button-row>

\\#GKI \\#Kernel \\#Zephyr"""

payload = {
    "markdown": rich_markdown,
    "media": [
        {"id": "banner1", "media": {"type": "photo", "media": "attach://banner_file1"}}
    ] if banner_path else []
}

payload_file = "/tmp/rich_payload.json"
with open(payload_file, "w", encoding="utf-8") as f:
    json.dump(payload, f)

# 3. Send Rich Message via Telegram API
cmd = [
    "curl", "-s", "-X", "POST", f"https://api.telegram.org/bot{BOT_TOKEN}/sendRichMessage",
    "-F", f"chat_id={CHAT_ID}",
    "-F", f"rich_message=<{payload_file}"
]
if banner_path:
    cmd.extend(["-F", f"banner_file1=@{banner_path}"])

print("Sending rich message with banner...")
res = subprocess.run(cmd, capture_output=True, text=True)
print("Rich message response:", res.stdout[:200])

# 4. Upload Built ZIP Packages
zip_files = sorted(glob.glob("release_assets/*.zip") + glob.glob("*.zip"))
seen = set()
unique_zips = []
for z in zip_files:
    bname = os.path.basename(z)
    if bname not in seen:
        seen.add(bname)
        unique_zips.append(z)

print(f"Uploading {len(unique_zips)} kernel zip files to Telegram...")
for zpath in unique_zips:
    fname = os.path.basename(zpath)
    doc_cmd = [
        "curl", "-s", "-X", "POST", f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
        "-F", f"chat_id={CHAT_ID}",
        "-F", f"document=@{zpath}",
        "-F", f"caption=📦 <b>{fname}</b>",
        "-F", "parse_mode=HTML"
    ]
    subprocess.run(doc_cmd, capture_output=True, text=True)

print("Telegram notification complete!")
