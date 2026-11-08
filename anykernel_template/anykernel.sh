### AnyKernel3 Ramdisk Mod Script
## osm0sis @ xda-developers
## Modded for ZephyrKernel

### AnyKernel setup
# global properties
properties() { '
kernel.string=ZephyrKernel for POCO X7 (GKI 6.1)
do.devicecheck=0
do.modules=0
do.systemless=0
do.cleanup=1
do.cleanuponabort=0
do.check_boot_version=0
device.name1=
device.name2=
device.name3=
device.name4=
device.name5=
supported.versions=
supported.patchlevels=
supported.vendorpatchlevels=
'; } # end properties

### AnyKernel install
## boot shell variables (Both uppercase for latest AK3 and lowercase for legacy)
BLOCK=boot
IS_SLOT_DEVICE=auto
RAMDISK_COMPRESSION=auto
PATCH_VBMETA_FLAG=auto
NO_MAGISK_CHECK=1

block=boot
is_slot_device=auto
ramdisk_compression=auto
patch_vbmeta_flag=auto
no_magisk_check=1

# import functions/variables and setup patching
. tools/ak3-core.sh

# GKI check
kernel_version=$(cat /proc/version | awk -F '-' '{print $1}' | awk '{print $3}')
case $kernel_version in
    5.1*) gki_supported=true ;;
    6.1*) gki_supported=true ;;
    6.6*) gki_supported=true ;;
    *) gki_supported=false ;;
esac

ui_print " "
ui_print "  -> Flashing ZephyrKernel (GKI $kernel_version)..."
$gki_supported || abort "  -> Non-GKI device, abort."

# boot install
split_boot

if [ -f "$SPLITIMG/ramdisk.cpio" ]; then
    unpack_ramdisk
    write_boot
else
    flash_boot
fi

ui_print " "
ui_print "  -> ZephyrKernel successfully flashed!"
ui_print "  -> Enjoy your optimized experience."
ui_print " "
