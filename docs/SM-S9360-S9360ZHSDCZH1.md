# SM-S9360 / S9360ZHSDCZH1 porting record

Offline port of profile `pa2q-S9360ZHSDCZH1`, built 2026-09-26 from the
`TGY`/`OZS` factory package for `S9360ZHSDCZH1` (released 2026-09-03, the
current Hong Kong update for `SM-S9360`).

**Hardware validation is still pending.** Every value below was derived from
this build's own kernel Image and BTF, and the build passed the offline gates
in [`PORTING.md`](PORTING.md); the exploit has *not* been run on an
`SM-S9360`/`S9360ZHSDCZH1` device yet.

## 1. Firmware identity

| field | value |
| --- | --- |
| model | `SM-S9360` (Galaxy S25+, Greater China / Hong Kong `TGY` + `OZS`) |
| AP/PDA | `S9360ZHSDCZH1` |
| CSC | `S9360OZSDCZH1` (`OZS`, Hong Kong open) |
| codename | `pa2q` |
| build fingerprint | `samsung/pa2qzhx/pa2q:16/BP4A.251205.006/S9360ZHSDCZH1_OZSDCZH1:user/release-keys` (see §7) |
| kernel release | `6.6.98-android15-8-pd6ff1cd-abogkiS9360ZHSDCZH1-4k` |
| kernel build | `#1 SMP PREEMPT Wed Aug 12 03:11:35 UTC 2026` |
| kernel SHA-256 | `212387cf7c26dd19db4629fd6d8f448711c1d2a5131e30c974c3c93babb84c28` (raw Image from `boot.img`) |
| boot.img SHA-256 | `7E9D3AB0E29494EF0F775FB118E71655CFA4435F2C88780A29F250F2EE3EF19D` |
| page size / SDK / ABI | 4096 / 36 / `arm64-v8a` |

Extraction values:

```text
boot.img size: 101122048 (header v4, page 4096)
kernel size:   38849024 (0x250F000), copied from boot offset 0x1000
ARM64 Image text_offset: 0x0
ARM64 Image image_size:  0x27B0000
ARM64 Image flags:       0xa
raw BTF interval:        [0x18748D4, 0x1E8BB88) (6386356 bytes)
vmlinux-to-elf base:     0xffffffc080000000 (114227 kallsyms symbols)
```

### Source provenance

```text
FUS package      SM-S9360_3_20260813084312_tq84r5m3g4_fac.zip.enc4
FUS package size 18346260752 bytes (AES-128-ECB, key = md5(logic_check(sw, LOGIC_VALUE)))
ZIP members      BL_… (99818197)  AP_… (18003528726)  CP_… (87901786)
                 HOME_CSC_OZS_S9360OZSDCZH1_…  CSC_OZS_S9360OZSDCZH1_…
AP tar members   0 boot.img.lz4 22669553   1 init_boot.img.lz4 2743155
                 2 vendor_boot.img.lz4 37437350   3 vbmeta_system.img.lz4 2933
                 4 super.img.lz4 12828748763   (…)
boot.img.lz4 SHA-256 356ED7D2B0155192D9869DA183BFD69735274DA753BC3D646B291DECD7C55367
```

Only the needed byte ranges of the 18.35 GB `SMART 2.0` package were pulled:
the `.enc4` container is a whole-file AES-128-ECB transform, so every
16-byte-aligned `Range` request decrypts independently. The AP member's
`boot.img.lz4` came out of a sequential inflate of that single ZIP entry with
a running tar-header walk, which stops as soon as the wanted member is
complete — no part of `super.img.lz4` was downloaded.

## 2. Relationship to `S9360ZHSCCZG1` (the previous HK build)

The two builds were compared byte-for-byte and symbol-for-symbol:

| check | result |
| --- | --- |
| raw Image size | identical (38849024), different SHA-256 |
| differing bytes | 1105954 in 119106 runs; 54.1 % of 4 KiB pages identical |
| `vmlinux-to-elf` symbols | 114227 lines / 110068 unique names, both builds |
| unique symbol names at identical addresses | 110058 of 110068 |
| the 10 that moved | local labels sitting in the `.rodata` string pool, shifted by exactly the pool deltas: `f_midi_shortname`, `note_page.units`, `task_index_to_char.state_char`, `trunc_msg`, `pty_line_name.ptychar` (+0x33), `zero_mask` (+0x49), `max_tt_usecs`, `f_midi_longname` (+0x74), `__cert_list_end`, `__module_cert_end` (+1) — none used by this profile |
| BTF | byte-identical, same validated interval |
| the 22 symbol offsets below | all identical |

So the only firmware-dependent change in this build is one string address:

```text
"nfnetlink_log"   0x0175e266 -> 0x0175e299   (+0x33)  => SLIDE_NFULNL_LOGGER_NAME_OFF
"boot_id"         0x017182ac -> 0x01718320   (+0x74)  (the random_table slot and the
                                                       sysctl_bootid storage it points to
                                                       are unchanged: 0x02439490 / 0x026426d8)
```

This is why the profile needs its own directory even though the kernel
release prefix (`6.6.98-android15-8`) is shared: the RMG feed matches on
`Build.MODEL` + the three-part `uname -r`, so `SM-S9360` + `6.6.98` alone
cannot distinguish CZG1 from CZH1, ZCS, or the S25 Ultra payloads.

## 3. Offsets

Re-derived from this kernel's recovered `vmlinux.elf` and raw BTF. Identical
to `pa2q-S9360ZHSCCZG1` (and to `pa3q-S938NKSUACZF1`) except where noted.

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
SLIDE_NFULNL_LOGGER_NAME_OFF    0x0175e299   <-- build-specific (+0x33 vs CZG1)
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

Derivation notes that matter for the next port:

* `SLIDE_NFULNL_LOGGER_NAME_OFF` is the file offset of the `"nfnetlink_log"`
  string, i.e. the target of the first qword of `struct nf_logger
  nfulnl_logger`; it is found by searching the raw Image for the string, not
  by symbol lookup. It moves whenever the `.rodata` string pool is
  re-laid-out, which is exactly what happened between CZG1 and CZH1.
* `SLIDE_RANDOM_TABLE_BOOT_ID_DATA_PTR_OFF` is the *second* qword of the
  `boot_id` entry in `random_table[]`: the slot holding the pointer to the
  `"boot_id"` string is at `0x02439488`, so the `data` field is at `0x02439490`
  and its value is `SLIDE_SYSCTL_BOOTID_OFF` (`0x026426d8`, confirmed both as
  the stored pointer and as the `sysctl_bootid` symbol).
* `SLIDE_TRACEFS_WORKER_CALLER_OFF` is the instruction after the blocking
  `bl schedule` inside `worker_thread` (`0xffffffc0800d97ec`), re-derived with
  `llvm-objdump --disassemble-symbols=worker_thread`.

BTF layout values (byte-identical BTF, so unchanged from CZG1/`pa3q`; stated
here so the profile is self-contained):

```text
sizeof(file_operations) = 0x108
file_operations.unlocked_ioctl = 0x48, compat_ioctl = 0x50, mmap = 0x58
file_operations.open = 0x68, release = 0x78, splice_read = 0xb8,
file_operations.show_fdinfo = 0xd8

task_struct.usage = 0x40, prio = 0x84, normal_prio = 0x8c
task_struct.sched_task_group = 0x348
task_struct.pi_lock = 0x90c, pi_waiters = 0x920
task_struct.pi_top_task = 0x930, pi_blocked_on = 0x938

sizeof(page) = 0x40, compound_head = 0x08, page_type = 0x30
sizeof(slab) = 0x40, slab.slab_cache = 0x08

rt_waiter_node = { rb_node entry @0x00, prio @0x18, deadline @0x20 } (size 0x28)
rt_mutex_waiter = { tree @0x00, pi_tree @0x28, task @0x50,
                    lock @0x58, wake_state @0x60, ww_ctx @0x68 } (size 0x70)

configfs_buffer.page = 0x10, needs_read_fill = 0x50, bin_buffer = 0x58,
configfs_buffer.bin_buffer_size = 0x60, cb_max_size = 0x64
work_struct = { data @0x00, entry @0x08, func @0x18 }
pool_workqueue = { pool @0x00, wq @0x08, work_color @0x10, refcnt @0x18,
                   nr_in_flight @0x1c, nr_active @0x5c, max_active @0x60 }
worker_pool = { worklist @0x28, nr_idle @0x3c }
workqueue_struct.dfl_pwq = 0xb0
miscdevice.fops = 0x10
```

Slide defaults, re-checked against this Image:

```text
SLIDE_TRACEFS_EVENT_ID 109
  (__TRACE_LAST_TYPE 20 + (__event_sched_blocked_reason 0x022b1be8
                           - __start_ftrace_events 0x022b1920)/8 = 20 + 89)
SLIDE_PSELECT_WORD_SHIFT 0
SLIDE_STACK_WRITER       default for 6.6 pa2q (no override in the Makefile)
```

## 4. Physical load address

```c
#define P0_PHYS_OFFSET       0x80000000ULL
#define P0_KERNEL_PHYS_LOAD  0xa8000000ULL
```

Unchanged. This Image has `text_offset == 0`, the same `gunyah_hyp_region`
direct-map derivation as CZG1 applies, and the CZG1 hardware run proved the
`0xa8000000` value on this device family. The CZH1 kernel's `xbl_config`
carries the same literal. Hardware confirmation is still pending for this
build (see §7).

## 5. p0 fingerprint

Regenerated from this kernel's raw Image with
`tools/generate_p0_fingerprint.pl kernel 0x1f0000 …` (`PROBE_OFFSET=0x1f0000`;
the helper verifies all 32 rows and 256 source qwords before writing).

| comparison | differing rows |
| --- | ---: |
| vs `pa2q-S9360ZHSCCZG1` | 1 of 32 |
| vs `pa3q-S938NKSUACZF1` (shared S25 payload) | 1 of 32 |
| vs `pa2q-S9360ZCSCCZG1` (China) | 12 of 32 |

The single mismatch against `pa3q` is slide `0x000c0000`, word 2
(`page+0x400`):

```text
pa3q  0x913dc821d000b321ULL
CZG1  0x913da821d000b321ULL
CZH1  0x913ecc21d000b321ULL   <-- this build
```

The shared `galaxy-s25-series` payload therefore must not be used on
`S9360ZHSDCZH1`: if the real slide is `0x000c0000` its fingerprint row does
not match.

## 6. KernelSU

`kernelsu/ksud-s25u-kdp` (`android15-6.6` KMI) is the intended module, the
same one the CZG1 profile uses. This build does not change the KMI string
(`6.6.98-android15-8`); only the local suffix (`…-abogkiS9360ZHSDCZH1-4k`)
changed, and the late-load path loads with
`MODULE_INIT_IGNORE_VERMAGIC`, so the published module does not need a
rebuild. The Samsung DEFEX/KDP behaviour recorded in the CZG1 record
(`u:r:kernel:s0` bootstrap root cannot `readdir` `/data/adb/modules`; the
module + fix-ups must happen in one request; the expected warm framework
restart after late-load) is expected to be identical and is **not yet
confirmed on this build**.

## 7. Validation status and what to do next

Passed offline: kernel/BTF extraction, symbol and layout derivation (all 22
offsets re-derived, not copied), P0 fingerprint generation and verification,
`make all` build with the official NDK, artifact disassembly diff against
CZG1, feed JSON validation.

Pending on hardware:

1. Confirm the build identity on the device:

   ```sh
   adb shell getprop ro.build.fingerprint
   adb shell getprop ro.build.display.id
   adb shell uname -r
   adb shell getprop ro.boot.warranty_bit
   ```

   The `BUILD_FINGERPRINT` in
   [`../src/targets/pa2q-S9360ZHSDCZH1/target.h`](../src/targets/pa2q-S9360ZHSDCZH1/target.h)
   uses `BP4A.251205.006` (the Android 16 platform build id shared by every
   2026 S25/S24 profile in this repository, including the 2026-06
   `S9360ZCSCCZG1` and 2026-07 `S9360ZHSCCZG1` builds). If the device reports
   a different `ro.build.fingerprint`, patch that one line — nothing else in
   the profile depends on it, and the built artifacts do not embed it.
2. Run the exploit and KernelSU late-load:

   ```sh
   tools/reroot.sh --target pa2q-S9360ZHSDCZH1 --attempts 16
   ```

   `tools/reroot.sh` refuses to run unless the device fingerprint matches the
   profile; use `--force` only to test a mismatch deliberately.
3. Record the logs in [`../artifacts/pa2q-S9360ZHSDCZH1/`](../artifacts/pa2q-S9360ZHSDCZH1/)
   and update the artifact README from "offline-verified" to "device-tested"
   with the observed `p0_offset`, `slide-kaslr-ok` source, cache-gate line and
   `u:r:ksu:s0` confirmation.

## 8. Scope

Verified offline only for `SM-S9360` / `S9360ZHSDCZH1` (`OZS`/`TGY`,
`pd6ff1cd-abogki` GKI). Do not use this payload on `S9360ZHSCCZG1` or
`S9360ZCSCCZG1`: `SLIDE_NFULNL_LOGGER_NAME_OFF` and the p0 table differ.
Because all three builds report `SM-S9360` + `6.6.98`, automatic feed
selection returns the first matching entry (`pa2q-S9360ZCSCCZG1`); ZHS devices
must pick the profile explicitly in advanced mode or be served a filtered
feed.
