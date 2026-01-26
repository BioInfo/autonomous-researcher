# ISSUE: Modal Credentials Not Validated Before Experiment Execution

## Summary

Orchestrator runs experiments without validating Modal credentials, leading to silent failures or undefined behavior when `MODAL_TOKEN_ID` / `MODAL_TOKEN_SECRET` are not set.

## Observed Behavior

```bash
python main.py "Characterize scaling laws for sparse attention transformers" \
  --mode orchestrator --model gpt-4o --gpu T4
```

- 3 experiments were "scheduled" and "completed"
- Orchestrator attempted synthesis, hit OpenAI rate limit (67K tokens)
- **Modal credentials were never set** - unclear what actually executed

## Expected Behavior

1. Validate Modal credentials at startup (or when `--local` is not set)
2. Fail fast with clear error if Modal is required but not configured
3. Or: default to `--local` mode when Modal is unavailable

## Root Cause

- `main.py:20-22` prints credential status to stderr but doesn't enforce
- `agent.py:144` calls `modal.Sandbox.create()` without prior validation
- `orchestrator.py:350` spawns subprocess that inherits missing credentials

## Affected Code

| File | Line | Issue |
|------|------|-------|
| `main.py` | 20-22 | Debug print only, no enforcement |
| `agent.py` | 112-156 | `_get_shared_sandbox()` assumes Modal works |
| `agent.py` | 245-259 | `execute_in_sandbox()` checks `_local_mode` but doesn't validate Modal |
| `orchestrator.py` | 327-356 | `run_researcher()` spawns subprocess without credential check |

## Proposed Fix

```python
# main.py - add validation before orchestrator/agent runs
def _validate_execution_environment(args):
    if not args.local:
        modal_id = os.environ.get("MODAL_TOKEN_ID")
        modal_secret = os.environ.get("MODAL_TOKEN_SECRET")
        if not modal_id or not modal_secret:
            print_status(
                "ERROR: Modal credentials not set. "
                "Either set MODAL_TOKEN_ID/MODAL_TOKEN_SECRET or use --local flag.",
                "bold red"
            )
            sys.exit(1)
```

## Workaround

Use `--local` flag to bypass Modal:

```bash
python main.py "..." --mode orchestrator --model gpt-4o --local
```

## Additional Context

- Branch: `feature/openai-local-execution`
- Date: 2026-01-26
- Related: OpenAI TPM rate limit issue (separate problem)



provide command to test with local                                                                                                
                                                                                                                                    
● python main.py "Characterize scaling laws for sparse attention transformers" --mode orchestrator --model gpt-4o --local           
                                                                                                                                    
  Or via wrapper:                                                                                                                   
  python run_cli.py "Characterize scaling laws for sparse attention transformers" --mode orchestrator --model gpt-4o --local        
                                                                                                                                    
  Note: This will still hit the OpenAI rate limit issue after experiments complete. To avoid that, consider using Claude instead:   
  python main.py "Characterize scaling laws for sparse attention transformers" --mode orchestrator --model claude-opus-4-5 --local  


run_cli.py "Research task" --mode orchestrator --model ollama:qwen2.5:14b --local
run_cli.py "Characterize scaling laws for sparse attention transformers" --mode orchestrator --model ollama:qwen2.5:14b --local

smaller,faster

run_cli.py "Characterize scaling laws for sparse attention transformers" --mode orchestrator --model ollama:llama3.1:8b



run_cli.py "Characterize scaling laws for sparse attention transformers" --mode orchestrator --model ollama:qwen2.5:14b

run_cli.py is a convenience wrapper that:                                                                                         
  1. Creates venv/ if missing                                                                                                       
  2. Installs requirements.txt                                                                                                      
  3. Re-executes using venv python                                                                                                  
  4. Forwards args to main.py                                                                                                       
 
