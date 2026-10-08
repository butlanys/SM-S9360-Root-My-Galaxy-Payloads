# pa2q-S9360ZHUDDZIF artifacts

Built 2026-10-08 for `SM-S9360` / `S9360ZHUDDZIF` — Android 17 (One UI 9 /
`meta_OS17`), Hong Kong `OZS`/`TGY`, kernel
`6.6.127-android15-8-p33f4ffe-abogkiS9360ZHUDDZIF-4k`.

**Offline-verified only: not yet executed on a device.** The package was still
pre-release when this profile was built (the FUS history lists it with an empty
date), so no device had it. Run
`tools/reroot.sh --target pa2q-S9360ZHUDDZIF` and record the result here.

| file | size | SHA-256 | use |
| --- | ---: | --- | --- |
| `cve-2026-43499-app.so` | 126624 | `f68e96bbc95e954826c222645f9f47806fb277dee0ac5424b2915e7ad3e2b715` | app payload (`--run-payload` / LD_PRELOAD); this is the feed artifact |
| `cve-2026-43499-root` | 26896 | `1acf40b8658a7971401d8d3d315bacf2d2bd00b1dea7cb9c0103e34f9907b17b` | root helper / su client |
| `cve-2026-43499` | 105872 | `03fbf690b81542b35afc682f379a37739ec74f32abfb7f4b2e6054b334608c6a` | root-umh LD_PRELOAD variant |

Sizes are unchanged from the Android 16 profiles. `cve-2026-43499-root` is
byte-for-byte identical to the CZG1/CZH1 helpers — it is compiled from
`src/su_daemon.c` alone and contains no firmware constant. The other two were
rebuilt from the re-derived constants; the object layout and the p0 oracle
tables are the only firmware-dependent content.

Firmware identity, offset derivation and the Android 16 → 17 comparison:
[`../../docs/SM-S9360-S9360ZHUDDZIF.md`](../../docs/SM-S9360-S9360ZHUDDZIF.md).

KernelSU: the same published `kernelsu/ksud-s25u-kdp` (`android15-6.6` KMI).
Android 17 did **not** change the KMI generation (`6.6.127-android15-8`), only
the local suffix, and the late-load path loads with
`MODULE_INIT_IGNORE_VERMAGIC`, so no module rebuild is required — not yet
confirmed on hardware.

`BUILD_FINGERPRINT` in the target header currently carries
`UNKNOWN-BUILD-ID`; fill it in from `adb shell getprop ro.build.fingerprint`
on an updated device. Only `tools/reroot.sh`'s identity guard reads it (the app
matches on model + full kernel release), and no compiled artifact embeds it, so
patching that one line needs no rebuild.
