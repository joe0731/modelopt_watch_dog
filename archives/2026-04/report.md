# Model-Optimizer Changelog — 2026-04

> Auto-generated from [NVIDIA/Model-Optimizer](https://github.com/NVIDIA/Model-Optimizer) merged PRs.

> Rows marked with color emoji contain **high-priority** tags:

> 🟡 `eval`  🔵 `vllm`  🟣 `vlm`  🟠 `onnx`

| Focus | Date | Commit | PR | Author | Tags | Description |
|:-----:|------|--------|-------|--------|------|-------------|
|  | 2026-04-02 | [7cd7d183](https://github.com/NVIDIA/Model-Optimizer/commit/7cd7d183f478af60f6e50ca03bb8b84f9e54a186) | [#1061](https://github.com/NVIDIA/Model-Optimizer/pull/1061) | [@yueshen2016](https://github.com/yueshen2016) | `export` `torch` | \[minor\] Refactor TE fused-norm handling in GPTModelExporter |
|  | 2026-04-02 | [fcb09bf1](https://github.com/NVIDIA/Model-Optimizer/commit/fcb09bf11d4a72bd8f0bfd771205941619f1fc43) | [#1155](https://github.com/NVIDIA/Model-Optimizer/pull/1155) | [@cjluo-nv](https://github.com/cjluo-nv) | `export` `torch` | \[NVBug: 6038899\] Fix MoE export crash on meta tensors with CPU offload |
|  | 2026-04-01 | [f1beaba3](https://github.com/NVIDIA/Model-Optimizer/commit/f1beaba36f2df02304eceea2293c99c595f73711) | [#1146](https://github.com/NVIDIA/Model-Optimizer/pull/1146) | [@mxinO](https://github.com/mxinO) | `quantization` `torch` | Fix vllm quantization for new vllm \>= 0.17 |
| 🟠 | **2026-04-01** | **[4c399afe](https://github.com/NVIDIA/Model-Optimizer/commit/4c399afee66393023ec5685114a615fbbe167c4a)** | **[#1135](https://github.com/NVIDIA/Model-Optimizer/pull/1135)** | **[@hthadicherla](https://github.com/hthadicherla)** | `onnx` `quantization` | **Added fallback to preload cudnn dlls from nvidia cudnn venv package or torch venv package** |
|  | 2026-04-01 | [c37c74f6](https://github.com/NVIDIA/Model-Optimizer/commit/c37c74f651d78c5f5865a7bd561becb74c19e262) | [#1057](https://github.com/NVIDIA/Model-Optimizer/pull/1057) | [@hthadicherla](https://github.com/hthadicherla) | `infra` | Fused QKV add node issue for GQA graph surgery  |
|  | 2026-04-01 | [45426ca8](https://github.com/NVIDIA/Model-Optimizer/commit/45426ca8c1fa5614ab2ac7e2154b61a616a8d135) | [#1122](https://github.com/NVIDIA/Model-Optimizer/pull/1122) | [@kevalmorabia97](https://github.com/kevalmorabia97) | `infra` `tests` | Remove custom DistillationProvider and simplify mbridge distillation and hf export |
|  | 2026-04-01 | [d6c8e9d2](https://github.com/NVIDIA/Model-Optimizer/commit/d6c8e9d2b6001b5c0cbbbde62963d1bbe1eb0a89) | [#1148](https://github.com/NVIDIA/Model-Optimizer/pull/1148) | [@kevalmorabia97](https://github.com/kevalmorabia97) | `example` `export` `quantization` `torch` `windows` | Remove internal lustre paths |
|  | 2026-04-01 | [09b3c0b1](https://github.com/NVIDIA/Model-Optimizer/commit/09b3c0b1564d58828635bcfbe7d5d41548189a22) | [#1145](https://github.com/NVIDIA/Model-Optimizer/pull/1145) | [@kevalmorabia97](https://github.com/kevalmorabia97) | `infra` | Add modelopt-recipes-codeowners |
|  | 2026-04-01 | [2ae407c5](https://github.com/NVIDIA/Model-Optimizer/commit/2ae407c5598b90c77f04f45e37a40cec8e46be65) | [#1154](https://github.com/NVIDIA/Model-Optimizer/pull/1154) | [@kevalmorabia97](https://github.com/kevalmorabia97) | `infra` | Include gpu and example tests also in codecov coverage reporting and enable omitted folder coverage |
|  | 2026-04-01 | [de55e8a9](https://github.com/NVIDIA/Model-Optimizer/commit/de55e8a94ddbf6195eca924510d318cfbf0ca168) | [#1143](https://github.com/NVIDIA/Model-Optimizer/pull/1143) | [@kinjalpatel27](https://github.com/kinjalpatel27) | `export` `infra` `torch` | Bug fix: disable weight quantizer rotation after weight fold during vLLM fakequant export |

---
**Total: 10 PRs** | **Highlighted: 1**
