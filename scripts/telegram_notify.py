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
KERNEL_VER = os.environ.get("KERNEL_VER", "6.1.192")
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
> GKI 2.0 | Android 14 | Linux 6.1.192 LTS
> Target: Xiaomi POCO X7 / Redmi Note 14 Pro 5G (malachite) & GKI 6.1 Devices

<details>
<summary><tg-button type="disabled" style="primary">📖 Complete Changelog & Features</tg-button></summary>

<tg-button-row><tg-button type="disabled">Upstream 6.1.192 & Security Fixes</tg-button></tg-button-row>

<details>
<summary>🛡️ Upstream 6.1.192 LTS & CVE Backports</summary>

- Linux LTS: Synced cleanly to upstream Linux 6.1.192 LTS
- Pinmux (8434dec94): Fix race causing mux_owner NULL with active mux_usecount
- Block blk-mq (26d495f0f6): Fix tag memory leak when shrinking nr_hw_queues
- F2FS Sysfs (8b927ad2d1): Use modern IOPRIO_PRIO_LEVEL macro for checkpoint sysfs
- IPsec ESP4/ESP6 (cb37596580): Prevent managed frag page refcount leak in esp_ssg_unref
- UDP Tunnel (d53a8b927ac): Synchronous cancel of delayed work to avoid UAF on unregister
- Futex KABI Note: FUT_OFF_MMSHARED deferred to protect mm_struct KABI reserve slots
- Bluetooth & DMA-Buf: Upstream stability, race condition, and UAF mitigations
</details>

<tg-button-row><tg-button type="disabled">Core Subsystem Features</tg-button></tg-button-row>

<details>
<summary>⚡ CPU Scheduler & Responsiveness</summary>

- BORE (Burst-Oriented Response Enhancer) v6.8.0-rc1 (kernel.sched_bore = 1)
- Eliminates micro-stutters & prioritizes user-interactive frame rates
- Power-Efficient Workqueues (CONFIG_WQ_POWER_EFFICIENT_DEFAULT=y)
- Mainline Schedutil & Workqueue Catch-up patches
- Frame Warning Disabled (clean logcat under high GPU load)
- Governors: Schedutil, Ondemand, Performance
</details>

<details>
<summary>💾 Memory, ZRAM & Compression</summary>

- le9uo v1.15 low-memory protection (bypasses MGLRU for ZRAM)
- Ultra-fast anonymous memory reclamation without UI freezes
- Modern LZ4 v1.10.0 with ARM64 NEON ASM acceleration
- ZSTD v1.5.7 backported from Linux 6.15 for maximum compression
- LZ4K & LZ4KD high-throughput compression engines
- kcompressd v0.5 asynchronous memory compression daemon
- Built-in memory module blacklist (lzo, lzo_rle, zram, zsmalloc)
</details>

<details>
<summary>🌐 Networking & Tethering</summary>

- Google TCP BBRv3 + boot-time auto-enforcer daemon
- Google FQ Pacing (CONFIG_NET_SCH_FQ=y, default packet scheduler)
- Multipath TCP (CONFIG_MPTCP=y) for WiFi + Mobile Data aggregation
- CAKE Smart Queue Management (CONFIG_NET_SCH_CAKE=y)
- Netfilter TTL / HL hop-limit target bypass (unlimited hotspot tethering)
- Built-in WireGuard VPN kernel accelerator
- IPv6 NAT & IP Set support
</details>

<details>
<summary>🎵 Audio & Multimedia</summary>

- Bit-Perfect & Hi-Res USB DAC Audio bypass (CONFIG_SND_USB_AUDIO=y)
- Direct ALSA / UAC2 bit-perfect master output up to 32-bit/768kHz & Native DSD
- Bypass Android audio mixer re-sampling for audiophile USB DACs
</details>

<details>
<summary>🎮 Gaming & Emulation</summary>

- NTSYNC (/dev/ntsync) — Windows NT sync primitives driver for Wine / Winlator gaming
- BBG (Baseband Security Guard) modem partition protection
- Gamepad Force Feedback drivers (PS5 DualSense, PS4 DS4, Xbox)
</details>

<details>
<summary>📁 Storage & Filesystems</summary>

- Mainline UFS WriteBooster Catch-up
- F2FS Extended Attributes, POSIX ACL, and read extent cache locking fixes
- OverlayFS / Mountify support for rootless overlay mounts
</details>

<details>
<summary>🛡️ KMI ABI & Root Security</summary>

- 100% MediaTek Dimensity 7300-Ultra & GKI KMI ABI compliant (0 broken symbols)
- SYSVIPC task_struct KABI padding fix (+24 byte shift prevented)
- check_version() CRC bypass for vendor_dlkm compatibility
- Protected symbol export bypass (fixes WiFi/Bluetooth rfkill.ko)
- Re:Kernel emergency root backdoor on Port 22
- SuSFS v2.3.0 kernel-level cloaking (anti-detection & Play Integrity STRONG)
</details>
</details>

<table bordered>
<tr><td>Kernel</td><td>Linux {KERNEL_VER} LTS</td></tr>
<tr><td>Device</td><td>POCO X7 / Redmi Note 14 Pro 5G (malachite)</td></tr>
<tr><td>Architecture</td><td>ARM64 GKI 6.1 (Dimensity 7300-Ultra MT6878)</td></tr>
<tr><td>Source</td><td><tg-button type="url" url="https://github.com/afarhandanu/ZephyrKernel-6.1">ZephyrKernel-6.1</tg-button></td></tr>
<tr><td>Builder</td><td>kucingbalap1644@ZephyrCI</td></tr>
<tr><td>Toolchain</td><td>Neutron Clang 24.0.0git + LLD 24.0.0</td></tr>
<tr><td>LTO</td><td>{lto_html}</td></tr>
</table>

<table bordered>
<tr><td>Linux LTS Sync</td><td><tg-button type="disabled" style="success">6.1.192</tg-button></td></tr>
<tr><td>BORE Scheduler</td><td><tg-button type="disabled" style="success">v6.8.0-rc1</tg-button></td></tr>
<tr><td>TCP Congestion</td><td><tg-button type="disabled" style="success">BBRv3 + FQ</tg-button></td></tr>
<tr><td>MPTCP Bonding</td><td><tg-button type="disabled" style="success">Enable</tg-button></td></tr>
<tr><td>Power-Efficient WQ</td><td><tg-button type="disabled" style="success">Enable</tg-button></td></tr>
<tr><td>Hi-Res USB Audio</td><td><tg-button type="disabled" style="success">Enable</tg-button></td></tr>
<tr><td>le9uo LowMem</td><td><tg-button type="disabled" style="success">v1.15</tg-button></td></tr>
<tr><td>ZRAM Compression</td><td><tg-button type="disabled" style="success">LZ4 + ZSTD v1.5.7</tg-button></td></tr>
<tr><td>TTL/HL Bypass</td><td><tg-button type="disabled" style="success">Enable</tg-button></td></tr>
<tr><td>NTSync Emulation</td><td><tg-button type="disabled" style="success">Enable</tg-button></td></tr>
<tr><td>Re:Kernel</td><td><tg-button type="disabled" style="success">Port 22</tg-button></td></tr>
<tr><td>SuSFS Kernel Hide</td><td><tg-button type="disabled" style="success">v2.3.0</tg-button></td></tr>
<tr><td>MediaTek KMI ABI</td><td><tg-button type="disabled" style="success">100% Intact</tg-button></td></tr>
</table>

<tg-button-row><tg-button type="url" style="primary" url="https://t.me/FinaSU/">FinaSU v1.5.0+ · SuSFS v2.3.0</tg-button></tg-button-row>
<tg-button-row><tg-button type="url" style="primary" url="https://t.me/ksunext_ci/">KernelSU-Next · SuSFS v2.3.0</tg-button></tg-button-row>
<tg-button-row><tg-button type="url" style="primary" url="https://t.me/Sukiksu/7121/">SukiSU-Ultra · SuSFS v2.3.0</tg-button></tg-button-row>
<tg-button-row><tg-button type="url" style="primary" url="https://t.me/KernelSU_group/3234/">KernelSU · SuSFS v2.3.0</tg-button></tg-button-row>
<tg-button-row><tg-button type="url" style="primary" url="https://t.me/BakaSU_Grp/4/">BakaSU · SuSFS v2.3.0</tg-button></tg-button-row>
<tg-button-row><tg-button type="url" style="primary" url="https://t.me/kowsu_build/">KowSU · SuSFS v2.3.0</tg-button></tg-button-row>
<tg-button-row><tg-button type="callback_data" data="vanilla" style="primary">Vanilla (Non-Root / Pure GKI)</tg-button></tg-button-row>

<tg-button-row>
  <tg-button type="url" style="primary" url="{RELEASE_URL}">📦 GitHub Release</tg-button>
  <tg-button type="url" style="primary" url="https://github.com/afarhandanu/ZephyrKernel">⚡ Repository</tg-button>
</tg-button-row>

\\#GKI \\#Kernel \\#Zephyr \\#malachite \\#Dimensity7300"""

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
