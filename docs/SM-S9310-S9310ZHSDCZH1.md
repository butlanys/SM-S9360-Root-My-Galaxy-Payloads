# SM-S9310 / S9310ZHSDCZH1 porting record

Offline port of profile `pa1q-S9310ZHSDCZH1`, built 2026-09-26 from the
`TGY`/`OZS` factory package for `S9310ZHSDCZH1` (released 2026-09-03, the
current Hong Kong update for `SM-S9310`, Galaxy S25).

**Hardware validation is still pending.** Every value below was derived from
this build's own kernel Image, BTF and symbol table; the exploit has *not*
been run on an `SM-S9310`/`S9310ZHSDCZH1` device yet. Its S9360 sibling
(`pa2q-S9360ZHSDCZH1`, built three minutes earlier) is device-tested, and the
two images share everything except the one string offset this profile changes
(§2), so the untested surface here is that single constant.

## 1. Firmware identity

| field | value |
| --- | --- |
| model | `SM-S9310` (Galaxy S25, Greater China / Hong Kong `TGY` + `OZS`) |
| AP/PDA | `S9310ZHSDCZH1` |
| CSC | `S9310OZSDCZH1` (`OZS`, Hong Kong open) |
| codename | `pa1q` — confirmed from the build paths inside this build's own `vendor_boot.img` (`out/soong/.../common/pa1q/...`, and **zero** `pa2q` hits, so the image is not shared with the S25+ profile) |
| build fingerprint | `samsung/pa1qzhx/pa1q:16/BP4A.251205.006/S9310ZHSDCZH1_OZSDCZH1:user/release-keys` (product/region suffix follows the family pattern; see §7) |
| kernel release | `6.6.98-android15-8-pd6ff1cd-abogkiS9310ZHSDCZH1-4k` |
| kernel build | `#1 SMP PREEMPT Wed Aug 12 03:06:01 UTC 2026` |
| kernel SHA-256 | `3BEC64A80291C8CBDD5C4F285FA068620B066559CDB3317A1C2FE737822D5058` (raw Image from `boot.img`) |
| boot.img SHA-256 | `53C9E334C4AA318C48C63A69A9FD0CD8F4F8E4CE86FBF32E12D644EF5D20D72E` |
| page size / SDK / ABI | 4096 / 36 / `arm64-v8a` |

Extraction values:

```text
boot.img size: 101122048 (header v4, header_size 1584, page 4096)
kernel size:   38849024 (0x250CA00), copied from boot offset 0x1000
ARM64 Image text_offset: 0x0
ARM64 Image image_size:  0x27B0000
ARM64 Image flags:       0xa
raw BTF interval:        [0x18748D4, 0x1E8BB88) (6386356 bytes)
vmlinux-to-elf base:     0xffffffc080000000 (114227 kallsyms symbols,
                         kallsyms_offsets at file offset 0x015eaa20)
vendor_boot.img.lz4:     37364599 bytes, SHA-256 B76E180E6829CFE3DCEB603B9523276FDD738C9B6389F6890A61C62DEE2B699A
```

### Source provenance

```text
FUS package      SM-S9310_3_20260813084222_re22zdqor2_fac.zip.enc4
FUS package size 18299400000 bytes (AES-128-ECB, key = md5(logic_check(sw, LOGIC_VALUE)))
MODEL_PATH       /neofus/910/
AP member        AP_S9310ZHSDCZH1_S9310ZHSDCZH1_MQB113296158_REV00_user_low_ship_MULTI_CERT_meta_OS16.tar.md5
AP compressed    17957587893 bytes
AP tar members   0 boot.img.lz4 22667892   1 init_boot.img.lz4   2 vendor_boot.img.lz4 37364599
                 3 vbmeta_system.img.lz4  4 super.img.lz4 (12.8 GB)   …   meta-data/fota.zip
boot.img.lz4 SHA-256 0ABF7C9A06DE4928B4C2AF20E93E330F61FCFEB63FE878F0B7EABE160A2FD757
```

Only ~65 MB of the 18.3 GB package were transferred: the container is a
whole-file AES-128-ECB transform, so every 16-byte-aligned `Range` request
decrypts independently, and the AP member was inflated only until
`boot.img.lz4` was complete (the next member is the 12.8 GB
`super.img.lz4`).

## 2. Cross-model comparison with the same-day S25+ build

`S9310ZHSDCZH1` (SM-S9310) and `S9360ZHSDCZH1` (SM-S9360) were built three
minutes apart and are **the same kernel build** for every purpose this
profile cares about:

| check | result |
| --- | --- |
| raw Image size | identical (38849024), different SHA-256 |
| differing bytes | 597431 in 644 runs at 4 KiB granularity; 58.4 % of pages identical |
| `vmlinux-to-elf` symbols | 114227 lines / 110068 unique names, both |
| unique names at identical addresses | 110063 of 110068 |
| the 5 that moved | local labels in the `.rodata` string pool (`f_midi_shortname`, `note_page.units`, `task_index_to_char.state_char` `-0x33`; `pty_line_name.ptychar`, `trunc_msg` `+0x49`) — none used by this profile |
| BTF | **byte-identical** (`C3A0FBFE…`, same interval) |
| the 22 symbol offsets | **all identical** |
| `worker_thread` window | disassembles identically → `SLIDE_TRACEFS_WORKER_CALLER_OFF` unchanged |
| `random_table[]` boot_id entry | same slots (`0x02439488` / `0x02439490`), same target `0x026426d8` |
| physical-P0 fingerprint table | **identical to the S9360 CZH1 table** (32/32 rows) |

The only firmware-dependent difference is one string address:

```text
"nfnetlink_log"   0x0175e299 (S9360 CZH1)  ->  0x0175e2e2 (S9310 CZH1)   (+0x49)
```

This is why the profile exists as its own directory: `SM-S9310` + `6.6.98`
alone cannot distinguish this build from the other pa1q/pa2q builds, and
reusing the S25-series payload on it would point the nfnetlink log-spoof at the
wrong string.

## 3. Offsets

Re-derived from this build's `vmlinux.elf`, raw BTF and Image. Identical to
`pa2q-S9360ZHSDCZH1` / `pa2q-S9360ZHSCCZG1` / `pa3q-S938NKSUACZF1` except where
noted.

```text
KIMAGE_TEXT_BASE                0xffffffc080000000
P0_PAGE_OFFSET                  0xffffff8000000000
P0_PHYS_OFFSET                  0x80000000
P0_KERNEL_PHYS_LOAD             0xa8000000
SKB_DATA_DELTA                  (-0xe80)
KMALLOC_CACHES_OFF              0x017da710
ANON_PIPE_BUF_OPS_OFF           0x0124cdc8
ASHMEM_FOPS_OFF                 0x0140b440
ASHMEM_MISC_FOPS_OFF            0x0247d7f0
INIT_TASK_OFF                   0x0230e4c0
ROOT_TASK_GROUP_OFF             0x0251cd80
SELINUX_ENFORCING_OFF           0x0255f5c0
SYSTEM_UNBOUND_WQ_OFF           0x022fae60
SLIDE_NFULNL_LOGGER_OBJECT_OFF  0x02302278
SLIDE_NFULNL_LOGGER_NAME_OFF    0x0175e2e2   <-- build-specific (+0x49 vs S9360 CZH1)
SLIDE_RANDOM_TABLE_BOOT_ID_DATA_PTR_OFF 0x02439490
SLIDE_SYSCTL_BOOTID_OFF         0x026426d8
SLIDE_TRACEFS_WORKER_CALLER_OFF 0x000d97ec
COPY_SPLICE_READ_OFF            0x00416970   (symbol: copy_splice_read)
CALL_USERMODEHELPER_EXEC_WORK_OFF 0x000d0eac
CONFIGFS_READ_ITER_OFF          0x004954b8
CONFIGFS_BIN_WRITE_ITER_OFF     0x004959e4
NOOP_LLSEEK_OFF                 0x003c9450
ASHMEM_IOCTL_OFF                0x00d70dfc
ASHMEM_COMPAT_IOCTL_OFF         0x00d714b8
ASHMEM_MMAP_OFF                 0x00d7150c
ASHMEM_OPEN_OFF                 0x00d7172c
ASHMEM_RELEASE_OFF              0x00d717b4
ASHMEM_SHOW_FDINFO_OFF          0x00d71840
```

These were *re-derived*, not copied: each value was looked up in this build's
`vmlinux.nm` and compared against the S9360 CZH1 dump (all 22 equal), the BTF
interval was re-extracted and byte-compared, `worker_thread` was re-disassembled,
and the `"nfnetlink_log"` string offset was found by searching this Image.

BTF-derived layout values are unchanged (byte-identical BTF):

```text
sizeof(file_operations) = 0x108  (unlocked_ioctl 0x48, compat_ioctl 0x50,
                                  mmap 0x58, open 0x68, release 0x78,
                                  splice_read 0xb8, show_fdinfo 0xd8)
task_struct: usage 0x40, prio 0x84, normal_prio 0x8c, sched_task_group 0x348,
             pi_lock 0x90c, pi_waiters 0x920, pi_top_task 0x930, pi_blocked_on 0x938
sizeof(page) = 0x40 (compound_head 0x08, page_type 0x30)
sizeof(slab) = 0x40 (slab_cache 0x08)
rt_mutex_waiter = { tree 0x00, pi_tree 0x28, task 0x50, lock 0x58,
                    wake_state 0x60, ww_ctx 0x68 } (size 0x70)
configfs_buffer: page 0x10, needs_read_fill 0x50, bin_buffer 0x58,
                 bin_buffer_size 0x60, cb_max_size 0x64
work_struct { data 0x00, entry 0x08, func 0x18 }
worker_pool { worklist 0x28, nr_idle 0x3c }
pool_workqueue { pool 0x00, wq 0x08, work_color 0x10, refcnt 0x18,
                 nr_in_flight 0x1c, nr_active 0x5c, max_active 0x60 }
workqueue_struct.dfl_pwq = 0xb0 ; miscdevice.fops = 0x10
SLIDE_TRACEFS_EVENT_ID 109 (20 + (0x022b1be8 - 0x022b1920)/8 = 20 + 89)
SLIDE_PSELECT_WORD_SHIFT 0
```

## 4. Physical load address

```c
#define P0_PHYS_OFFSET       0x80000000ULL
#define P0_KERNEL_PHYS_LOAD  0xa8000000ULL
```

Unchanged: this Image has `text_offset == 0` and the same `gunyah_hyp_region`
direct-map derivation as the S9360 build. Hardware confirmation is still
pending for this build (see §7).

## 5. p0 fingerprint

Regenerated from this Image with
`tools/generate_p0_fingerprint.pl kernel 0x1f0000 …` (32 rows and 256 source
qwords verified before writing). The result is **identical** to the
`pa2q-S9360ZHSDCZH1` table — the sampled code at `PROBE_OFFSET=0x1f0000` is
byte-identical in both builds, which is independent evidence that the two
images share the same `.text` layout.

It must still not be replaced by the *shared S25-series* table
(`galaxy-s25-series-2026-06-07`), which differs in one row
(`slide 0x000c0000`, `page+0x400`).

## 6. KernelSU

`kernelsu/ksud-s25u-kdp` (`android15-6.6` KMI), the same module every other
S25 profile here uses. The KMI string is unchanged by this build; only the
local suffix (`…-abogkiS9310ZHSDCZH1-4k`) differs, and the late-load path
loads with `MODULE_INIT_IGNORE_VERMAGIC`. No module rebuild is required. The
Samsung DEFEX/KDP behaviour recorded for the S9360 profile (bootstrap root
cannot `readdir` `/data/adb/modules`, module + fix-ups must happen in one
request, warm framework restart after late-load) is expected to be identical
and is **not yet confirmed on this build**.

## 7. Validation status and what to do next

Passed offline: firmware fetch (65 MB of 18.3 GB), boot/kernel/BTF extraction,
build identity and codename confirmation from the image itself, all 22 offsets
re-derived, p0 fingerprint generation and verification, `make all` with the
official NDK, artifact disassembly diff against the S9360 CZH1 artifacts, feed
JSON validation.

Pending on hardware:

1. Confirm the build identity on the device:

   ```sh
   adb shell getprop ro.build.fingerprint
   adb shell getprop ro.build.display.id
   adb shell uname -r
   adb shell getprop ro.product.device
   ```

   The `BUILD_FINGERPRINT` in
   [`../src/targets/pa1q-S9310ZHSDCZH1/target.h`](../src/targets/pa1q-S9310ZHSDCZH1/target.h)
   uses `samsung/pa1qzhx/pa1q:16/BP4A.251205.006/S9310ZHSDCZH1_OZSDCZH1:user/release-keys`.
   The codename `pa1q` comes from this build's own `vendor_boot` build paths;
   the `zhx` region suffix and the `BP4A.251205.006` platform id follow the
   pattern used by every other 2026 S25 profile in this repository. If
   `ro.build.fingerprint` differs, patch that one line — **no compiled artifact
   embeds it**, so nothing needs rebuilding.
2. Run the exploit and KernelSU late-load:

   ```sh
   tools/reroot.sh --target pa1q-S9310ZHSDCZH1 --attempts 16
   ```

   `tools/reroot.sh` refuses to run unless the device fingerprint matches the
   profile; `--force` overrides deliberately. Run with `--no-ksu` first if a
   KernelSU module is suspect (see the workspace porting guide, §9 note about
   module-induced cold reboots).
3. Record the logs in [`../artifacts/pa1q-S9310ZHSDCZH1/`](../artifacts/pa1q-S9310ZHSDCZH1/)
   and change the artifact README from "offline-verified" to "device-tested"
   with the observed `p0_offset`, cache-gate line and `u:r:ksu:s0`
   confirmation.
4. The fork's LOCAL APK bundles a filtered feed; add this profile to
   `app/src/main/assets/feed/` (feed JSON + `artifacts/pa1q-S9310ZHSDCZH1/`)
   before testing through the app instead of `reroot.sh`.

## 8. Scope

Verified offline only for `SM-S9310` / `S9310ZHSDCZH1` (`OZS`/`TGY`,
`pd6ff1cd-abogki` GKI). Do not use this payload on `S9310ZHSCCZG1` or on any
`SM-S9360` build: `SLIDE_NFULNL_LOGGER_NAME_OFF` differs. Because several
S25 builds report `SM-S9360`/`SM-S9310` + `6.6.98`, automatic selection uses
the full `uname -r` string first (this app version does
`targets.firstOrNull { matchesDevice && kernelRelease in kernelVersions }`
before the three-part fallback), so each build resolves to its own entry.
