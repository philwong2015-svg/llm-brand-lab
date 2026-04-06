# Contributing to LLM Brand Lab

## How to Contribute Results

1. **Run the experiment** with your model of choice
2. A result file is auto-generated in `results/`
3. Fork this repo → add your file → open a Pull Request

**Your API key never appears in the result file** — only win/loss counts and response previews.

## File Naming Convention

```
results/{provider}_{model}_{date}.json

Examples:
  results/openai_gpt-4o_20260407.json
  results/anthropic_claude-opus-4-6_20260407.json
  results/google_gemini-2-5-flash_20260407.json
```

## Pull Request Checklist

- [ ] Result file follows the naming convention
- [ ] No API keys in the file
- [ ] Ran at least 5 times per pair (`--runs 5` minimum)
- [ ] Note your model version in the PR description

## Questions

Open a [Discussion](../../discussions) — we're friendly.
