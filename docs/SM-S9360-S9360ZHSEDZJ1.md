# SM-S9360 / S9360ZHSEDZJ1 porting record (Android 17, October wave)

Second Android 17 build for the Hong Kong `SM-S9360`, one month after
[`S9360ZHUDDZIF`](SM-S9360-S9360ZHUDDZIF.md). Built 2026-11-01; the PDA was
released 2026-10-26, kernel built 2026-10-12.

## 1. Firmware identity

| field | value |
| --- | --- |
| PDA / CSC / CP | `S9360ZHSEDZJ1` / `S9360OZSEDZJ1` / `S9360ZCSEDZJ1` |
| full tuple | `S9360ZHSEDZJ1/S9360OZSEDZJ1/S9360ZCSEDZJ1/S9360ZHSEDZJ1` |
| OS | Android 17 (`meta_OS17`) |
| kernel release | `6.6.127-android15-8-p87b1ce1-abogkiS9360ZHSEDZJ1-4k` |
| kernel build | `#1 SMP PREEMPT Mon Oct 12 09:43:40 UTC 2026` |
| kernel SHA-256 | `83c723bdf54b48a4889a2d0f051c6c0a6b3b40f4a11f61d50ddca1ed2c41c622` |
| boot.img.lz4 | 22805816 bytes, `34533036846304ff75d81ed50778076d59e6ed95fd36902f86decb2c02932a7b` |
| FUS package | `SM-S9360_4_20261014011111_quru2im27t_fac.zip.enc4`, 18859348160 bytes |
| AP member | `AP_S9360ZHSEDZJ1_S9360ZHSEDZJ1_MQB115974207_REV00_user_low_ship_MULTI_CERT_meta_OS17.tar.md5` (18514091569 compressed) |

Version-letter check against the pattern in
[`../../README.md`](../../README.md): rev `D`→`E`, region back to `ZHS`, month
`J` = October, seq `1` — a plain monthly step inside the same platform letter
`D` (Android 17), exactly as the letter table predicts.

## 2. What changed versus the September build

The PDA version moved a month, so this could have been a full re-derivation. It
was not, and the reason is worth recording:

```text
BTF blob           byte-identical to S9360ZHUDDZIF ([0x18ACA6C, 0x1ECD673),
                   6425607 bytes, 147790 types)
symbol count       115126 vs 115126 (identical)
all 22 offsets     0 difference — every symbol sits at the same address
kallsyms_offsets   same file offset 0x0161b128
Image bytes        ~1994956 of 39115264 differ (≈5%) — the GKI commit moved
                   p33f4ffe -> p87b1ce1, so functions were patched in place at
                   unchanged addresses
p0 fingerprint     7 of 32 rows (14 qwords) differ
nfnetlink_log      string moved 0x01791638 -> 0x017916ae (+0x76), rodata shift
                   caused by the changed BUILD_VARIANT_LABEL string
```

So the only firmware-dependent change is `SLIDE_NFULNL_LOGGER_NAME_OFF`, plus
the p0 table. Everything else in `target.h` is inherited from the DZIF profile
and was re-verified rather than assumed: the 22 symbol lookups were re-run on
this build's own `vmlinux.nm`, and the BTF/`core_sys_select`/`worker_thread`
checks were repeated.

## 3. Offsets

Identical to the Android 17 DZIF profile except:

| macro | DZJ1 | DZIF |
| --- | --- | --- |
| `SLIDE_NFULNL_LOGGER_NAME_OFF` | `0x017916ae` | `0x01791638` |

Re-derived and unchanged (full list in the DZIF record):

```text
CALL_USERMODEHELPER_EXEC_WORK_OFF 0x000d1278   SLIDE_TRACEFS_WORKER_CALLER_OFF 0x000d9ba0
NOOP_LLSEEK_OFF 0x003cb7f8                     COPY_SPLICE_READ_OFF 0x004190cc
CONFIGFS_READ_ITER_OFF 0x004983d4              CONFIGFS_BIN_WRITE_ITER_OFF 0x00498900
ASHMEM_IOCTL_OFF 0x00d7e6c0                    ASHMEM_COMPAT_IOCTL_OFF 0x00d7ed7c
ASHMEM_MMAP_OFF 0x00d7edd0                     ASHMEM_OPEN_OFF 0x00d7eff0
ASHMEM_RELEASE_OFF 0x00d7f078                  ASHMEM_SHOW_FDINFO_OFF 0x00d7f104
ANON_PIPE_BUF_OPS_OFF 0x01278148               ASHMEM_FOPS_OFF 0x01437480
KMALLOC_CACHES_OFF 0x0180e578                  SYSTEM_UNBOUND_WQ_OFF 0x0233ac60
INIT_TASK_OFF 0x0234e2c0                       SLIDE_NFULNL_LOGGER_OBJECT_OFF 0x02342080
SLIDE_RANDOM_TABLE_BOOT_ID_DATA_PTR_OFF 0x024785c0   ASHMEM_MISC_FOPS_OFF 0x024bcd80
ROOT_TASK_GROUP_OFF 0x0255df80                 SELINUX_ENFORCING_OFF 0x025a0810
SLIDE_SYSCTL_BOOTID_OFF 0x02683910
SLIDE_TRACEFS_EVENT_ID 109 (20 + 89)           SLIDE_PSELECT_WORD_SHIFT 0 (source default)
```

## 4. p0 fingerprint

Regenerated with `tools/generate_p0_fingerprint.pl kernel 0x1f0000 …` (32 rows
and 256 qwords verified). 7 rows differ from DZIF — those are the probe points
where the patched-in-place code changed. The generated table was confirmed
embedded in the built artifact (256/256 qwords), and the 14 stale DZIF values
are absent from it.

## 5. Validation status

Passed offline: FUS fetch and identity, extraction, `vmlinux-to-elf`
(115126 symbols), BTF comparison against DZIF (byte-identical), the 22 symbol
lookups re-run on this build, `worker_thread` disassembly, fingerprint
generation and read-back, NDK build with the fixed sizes (126624 / 105872 /
26896), `cve-2026-43499-root` byte-identical to the published helper, embed
check of the new fingerprint table.

Pending on hardware:

1. `adb shell getprop ro.build.fingerprint` → replace `UNKNOWN-BUILD-ID`.
2. `tools/reroot.sh --target pa2q-S9360ZHSEDZJ1 --attempts 32` (start with
   `--no-ksu`).
3. Record the result here and in the artifact README.

## 6. Scope

`SM-S9360` / `S9360ZHSEDZJ1` only. The same wave exists for `SM-S9310` and
`SM-S9380`, whose kernels are separate Images and need their own derivation.
Android 16 and the September Android 17 build are *not* compatible with these
artifacts: the DZIF profile differs by the logger offset and the p0 table, and
the Android 16 profiles differ in every offset.
