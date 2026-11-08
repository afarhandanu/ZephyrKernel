# ZephyrKernel (GKI 6.1)

Custom Android Generic Kernel Image (GKI 2.0) based on **Luminaire Kernel** (Linux 6.1.y) with **FinaSU**, **SUSFS**, and performance enhancements.

## Features Included
- **Base:** [LuminaireKernel-6.1](https://github.com/chainonyourdoor/LuminaireKernel-6.1) (`android14-6.1-luminaire`)
- **Kernel Version:** Linux 6.1.187+
- **Root Solution:** [FinaSU](https://github.com/LyraVoid/FinaSU) with full SUSFS support
- **CPU & Scheduler:** BORE Scheduler (Burst-Oriented Response Enhancer v6.8)
- **Networking:** TCP BBRv3, CAKE Qdisc (Anti-Bufferbloat for Low Ping Gaming)
- **Tethering:** TTL Target & Mangling (Hotspot / Tethering quota bypass directly from kernel)
- **Gaming & Input:** Native DualSense PS5 & Xbox One/Series Controller Drivers with Vibration/Force Feedback
- **Toolchain:** Neutron Clang + LLD with ThinLTO/O3 optimizations

## How to Build via GitHub Actions
1. Go to the **Actions** tab in this repository.
2. Select the **Build ZephyrKernel (GKI 6.1)** workflow.
3. Click **Run workflow**.
4. Once completed (~15 minutes), download the flashable `.zip` file from the **Artifacts** section!

## How to Flash
- Flash via custom recovery (TWRP/OrangeFox), or
- Flash via **Kernel Flasher** app directly on your rooted Android device.
