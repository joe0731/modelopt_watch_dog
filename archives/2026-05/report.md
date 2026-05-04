# Model-Optimizer Changelog — 2026-05

> Auto-generated from [NVIDIA/Model-Optimizer](https://github.com/NVIDIA/Model-Optimizer) merged PRs.

> Rows marked with color emoji contain **high-priority** tags:

> 🟡 `eval`  🔵 `vllm`  🟣 `vlm`  🟠 `onnx`

| Focus | Date | Commit | PR | Author | Tags | Description |
|:-----:|------|--------|-------|--------|------|-------------|
| 🟠 | **2026-05-04** | **[e30cfab6](https://github.com/NVIDIA/Model-Optimizer/commit/e30cfab6fb1e574034b43101802df98ddfa8ac28)** | **[#1369](https://github.com/NVIDIA/Model-Optimizer/pull/1369)** | **[@hthadicherla](https://github.com/hthadicherla)** | `onnx` `quantization` | **Added fallback to load extra cudnn dlls in the site packages ** |
|  | 2026-05-04 | [acfab41d](https://github.com/NVIDIA/Model-Optimizer/commit/acfab41d0dc781b01e87167646081e99e14a6862) | [#1371](https://github.com/NVIDIA/Model-Optimizer/pull/1371) | [@yeyu-nvidia](https://github.com/yeyu-nvidia) | `core` `torch` | fix: guard against None chat_template in _post_process_chat_template |
|  | 2026-05-04 | [383ab4e2](https://github.com/NVIDIA/Model-Optimizer/commit/383ab4e22458ccbd48ceac23d048169a50041ed3) | [#1370](https://github.com/NVIDIA/Model-Optimizer/pull/1370) | [@yeyu-nvidia](https://github.com/yeyu-nvidia) | `example` `speculative_decoding` `torch` | fix: include medusa in data_module assignment in main.py |
|  | 2026-05-01 | [168cd828](https://github.com/NVIDIA/Model-Optimizer/commit/168cd828c19cd8e150ed69aa6b6de6713a8a153c) | [#1274](https://github.com/NVIDIA/Model-Optimizer/pull/1274) | [@cjluo-nv](https://github.com/cjluo-nv) | `export` `tests` `torch` | Add qwen3 moe experts only test |
| 🟡 | **2026-05-01** | **[50706d17](https://github.com/NVIDIA/Model-Optimizer/commit/50706d1750e7363c50ca22d300b1588139b9d426)** | **[#1372](https://github.com/NVIDIA/Model-Optimizer/pull/1372)** | **[@cjluo-nv](https://github.com/cjluo-nv)** | `eval` `example` `export` `infra` `quantization` `tests` `torch` | **Add closed-form MXFP4 -\> NVFP4 weight cast (--cast_mxfp4_to_nvfp4)** |
|  | 2026-05-01 | [9d2e6087](https://github.com/NVIDIA/Model-Optimizer/commit/9d2e6087d1c0d99a6d5441dc0c685da36af51055) | [#1365](https://github.com/NVIDIA/Model-Optimizer/pull/1365) | [@h-guo18](https://github.com/h-guo18) | `infra` | \[Fix\]: $HOME in launcher eagle example |

---
**Total: 6 PRs** | **Highlighted: 2**
