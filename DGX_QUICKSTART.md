# Autonomous Researcher - DGX Spark Quickstart

**Location:** `/home/bioinfo/apps/autonomous-researcher/`
**Setup Date:** 2025-11-26
**Platform:** NVIDIA DGX Spark (ARM64)

## Quick Start

### CLI Mode (Recommended for DGX)

```bash
cd ~/apps/autonomous-researcher
source venv/bin/activate

# Single experiment
python main.py "Your research hypothesis here" \
  --mode single \
  --gpu any \
  --model gemini-3-pro-preview

# Multi-agent orchestration
python main.py "Your research task here" \
  --mode orchestrator \
  --num-agents 3 \
  --max-rounds 3 \
  --max-parallel 2 \
  --gpu any \
  --model gemini-3-pro-preview

# Test mode (no LLM/GPU usage)
python main.py "Test hypothesis" \
  --mode single \
  --test-mode
```

### Web UI Mode

```bash
cd ~/apps/autonomous-researcher
source venv/bin/activate
python run_app.py
# Access at: http://localhost:5173
```

## Configured API Keys

✅ **Google AI Studio** (Gemini 3 Pro) - GOOGLE_API_KEY
✅ **Anthropic** (Claude Opus 4.5) - ANTHROPIC_API_KEY
✅ **Modal** (GPU Sandboxes) - MODAL_TOKEN_ID, MODAL_TOKEN_SECRET

Keys stored in: `.env`

## Example Usage

### Test XOR Learning
```bash
cd ~/apps/autonomous-researcher && source venv/bin/activate
python main.py "Test if a simple 2-layer neural network can learn XOR" \
  --mode single --gpu any --model gemini-3-pro-preview
```

### Batch Normalization Study
```bash
python main.py "Does batch normalization improve MNIST training?" \
  --mode single --gpu T4 --model gemini-3-pro-preview
```

### Multi-Agent Research
```bash
python main.py "Characterize scaling laws for sparse attention transformers" \
  --mode orchestrator --num-agents 3 --max-rounds 3 --max-parallel 2 --gpu A10G
```

## GPU Types Available via Modal

- `any` - Let Modal choose (fastest allocation)
- `T4` - NVIDIA T4 (16GB)
- `A10G` - NVIDIA A10G (24GB)
- `A100` - NVIDIA A100 (40GB/80GB)

## Model Selection

- `gemini-3-pro-preview` - Google Gemini 3 Pro (default, fast)
- `claude-opus-4-5` - Anthropic Claude Opus 4.5 (more capable)

## Output & Artifacts

- **Experiment Directory:** `~/workspace/experiments/active/[timestamp-task-name]/`
  - `logs/` - Orchestrator and agent logs
  - `reports/` - Final research papers and reports
  - `artifacts/` - Local experiment artifacts
- **HuggingFace:** Automatically uploads to `RyeCatcher/[experiment-name]`

## Troubleshooting

### Import Errors
```bash
cd ~/apps/autonomous-researcher
rm -rf venv __pycache__
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Modal Authentication
```bash
modal token new
# Follow prompts to authenticate
```

### Check API Keys
```bash
python main.py --help
# Look for: [DEBUG] Credentials check
```

## Architecture

**How it works:**
1. Takes a research hypothesis/task
2. Generates Python experiment code (PyTorch, etc.)
3. Launches Modal GPU sandbox to run the code
4. Analyzes results and iterates if needed
5. Generates a paper-style report
6. Uploads artifacts to HuggingFace

**Modes:**
- **Single:** One researcher agent, one experiment
- **Orchestrator:** Multiple researcher agents working in parallel

## Tested & Working ✅

- ✅ Environment setup (fresh ARM64 venv)
- ✅ All dependencies installed
- ✅ API keys configured
- ✅ Test mode working
- ✅ Real experiment working (XOR learning test)
- ✅ Modal GPU sandbox execution
- ✅ HuggingFace artifact upload
- ✅ Report generation

## Notes

- Venv is ARM64 Linux native (recreated from Mac version)
- Node.js v18 installed (frontend needs v20+ but works with warnings)
- Modal provides GPU sandboxes - experiments run remotely, not on DGX
- Each experiment auto-uploads to HuggingFace under `RyeCatcher/` namespace

**For more info:** See `README.md` and `api_guide.md`
