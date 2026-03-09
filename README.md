# ModelOpt Watch Dog

Automated tracking and classification of merged PRs in
[NVIDIA/Model-Optimizer](https://github.com/NVIDIA/Model-Optimizer).

A GitHub Action runs daily (and can be triggered manually) to fetch newly
merged PRs, classify the changes by module tags, and append the results to the
changelog table below.

## Tag Definitions

All tags are **flat** (same hierarchy level). Each directory in Model-Optimizer
maps to exactly one tag via longest-prefix matching.

### Framework Tags

| Tag | Description |
|-----|-------------|
| `torch` | modelopt.torch — PyTorch optimization core library |
| `onnx` | modelopt.onnx — ONNX graph optimization, autocast |
| `deploy` | modelopt.deploy — deployment, serving, vLLM / TensorRT-LLM |

### Feature Tags

| Tag | Description |
|-----|-------------|
| `quantization` | PTQ, QAT, QAD, calibration, quantized layers |
| `distillation` | Knowledge distillation, teacher-student training |
| `pruning` | Model pruning (structured / unstructured) |
| `sparsity` | Weight sparsity, attention sparsity |
| `speculative_decoding` | Speculative decoding, Eagle, Medusa, draft models |
| `export` | Model export, Torch-to-ONNX conversion |
| `nas` | Neural architecture search |
| `peft` | LoRA, adapters, parameter-efficient fine-tuning |
| `diffusers` | Diffusion model optimization (SD, FLUX, etc.) |
| `eval` | Model evaluation, benchmarking, accuracy metrics |
| `vllm` | vLLM serving and integration |
| `sglang` | SGLang serving and integration |
| `vlm` | Vision-language model optimization |
| `core` | Core utilities, tracing, optimization pipeline |

### Scope Tags

| Tag | Description |
|-----|-------------|
| `example` | Example scripts and notebooks |
| `infra` | CI/CD, build system, packaging, config |
| `docs` | Documentation, guides, API reference |
| `tests` | Test infrastructure, test utilities |
| `experimental` | Experimental / research features |
| `windows` | Windows platform-specific |

## Directory → Tag Mapping

See [`config/directory_tags.json`](config/directory_tags.json) for the
full mapping of every Model-Optimizer directory to its tag.

## Changelog

<!-- CHANGELOG_TABLE -->
| Date | Commit | PR | Author | Tags | Description |
|------|--------|-------|--------|------|-------------|
<!-- CHANGELOG_TABLE_END -->

## Usage

### Automatic (GitHub Action)

The workflow `.github/workflows/classify_commits.yml` runs daily at 08:00 UTC.
It can also be triggered manually from the **Actions** tab with an optional
`lookback_days` parameter.

### Manual

```bash
export GITHUB_TOKEN="ghp_..."
python scripts/classify_mr.py --lookback-days 30
```

Use `--dry-run` to preview without writing files.
