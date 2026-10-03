# pa1q-S9310ZHSDCZH1 artifacts

Built 2026-09-26 for `SM-S9310` / `S9310ZHSDCZH1` (Hong Kong `OZS`).

**Offline-verified only: not yet executed on a device.** Run
`tools/reroot.sh --target pa1q-S9310ZHSDCZH1` (or pick the profile in the app)
and record the log here before treating this profile as device-tested.

Confidence note: this profile's S9360 sibling (`pa2q-S9360ZHSDCZH1`, built
three minutes earlier from the same GKI source) **is** device-tested — the
injection works on an `SM-S9360` running `S9360ZHSDCZH1`. The two images share
their BTF, all 22 offsets, the `worker_thread` window and the p0 fingerprint
table, so the only value that has not been exercised on hardware here is the
one this profile changes (`SLIDE_NFULNL_LOGGER_NAME_OFF = 0x0175e2e2`).

| file | size | SHA-256 | use |
| --- | ---: | --- | --- |
| `cve-2026-43499-app.so` | 126624 | `6265f43b88741ef2a69135084cfd36e84d73a029ae8a3874187641da58c895e0` | app payload (`--run-payload` / LD_PRELOAD); this is the feed artifact |
| `cve-2026-43499-root` | 26896 | `1acf40b8658a7971401d8d3d315bacf2d2bd00b1dea7cb9c0103e34f9907b17b` | root helper / su client |
| `cve-2026-43499` | 105872 | `f8e582f04258b257893bcedf66bcb78538d384587ab6705865160ad221591c42` | root-umh LD_PRELOAD variant |

`cve-2026-43499-root` is byte-for-byte identical to the
`pa2q-S9360ZHSCCZG1` / `pa2q-S9360ZHSDCZH1` helpers: it is compiled from
`src/su_daemon.c` alone and contains no firmware-dependent constant.

The other two differ from the `pa2q-S9360ZHSDCZH1` artifacts by exactly one
constant: the `SLIDE_NFULNL_LOGGER_NAME_OFF` immediate (`mov … #-7454` here
versus `#-7527` for the S9360, i.e. the `+0x49` string shift), plus the rodata
re-layout that the changed `BUILD_VARIANT_LABEL` string causes — 594 `add`,
20 `adr` and 4 `adrp` string-address fixes in the `llvm-objdump` diff. Every
other offset is shared with the S9360 profile (see the porting record).

Firmware identity, offset derivation and the cross-model comparison:
[`../../docs/SM-S9310-S9310ZHSDCZH1.md`](../../docs/SM-S9310-S9310ZHSDCZH1.md).

KernelSU uses the published `kernelsu/ksud-s25u-kdp` (`android15-6.6` KMI),
the same module the other S25 profiles use. This build keeps the
`6.6.98-android15-8` KMI string and only changes the
`pd6ff1cd-abogki<S9310ZHSDCZH1>-4k` local suffix, and the late-load path loads
with `MODULE_INIT_IGNORE_VERMAGIC`, so no module rebuild is required. Not yet
confirmed on hardware.
