<div align="right">
<a href="README_CN.md">中文</a>
</div>

# LLM Brand Lab

I've been wondering whether AI systems have a preference for certain writing styles when recommending products — not based on product quality, but purely based on how the content is written.

So I built a simple experiment to test it.

---

## The setup

Take the same product. Write two descriptions with the same facts, but different styles:

**Functional** — direct, spec-focused:
> *"Powerful Massage Gun for Deep Tissue Recovery. High-torque brushless motor delivers up to 50lb of percussive intensity to relieve muscle soreness and fascia tension. Designed for athletes and active lifestyles."*

**Narrative** — cross-domain analogy, ends with a question:
> *"Elite coaches have always known what sports scientists now confirm: recovery isn't passive rest — it's active restructuring, the way coral rebuilds itself grain by grain after a storm. When did you last give your recovery the same focus you give your training?"*

Ask an LLM: *which brand would you recommend?* Run it 10 times, alternating which description is A and which is B to control for position bias. Record the results.

---

## What we found so far

| Model | Narrative win rate | Runs |
|---|---|---|
| deepseek-chat | 100% (46/46) | 46 |
| gpt-4o | — | need your help |
| claude-opus-4-6 | — | need your help |
| gemini-2.5-flash | — | need your help |
| llama-3 | — | need your help |

DeepSeek picked the narrative version every single time, across 5 product categories (earphones, massage guns, power banks, project management tools, specialty coffee).

Is this just DeepSeek? Does GPT-4 do the same? Does Claude? We don't know yet — that's why this is open.

---

## How to run it yourself

```bash
git clone https://github.com/philwong2015-svg/llm-brand-lab.git
cd llm-brand-lab
pip install openai  # or anthropic / google-generativeai
```

```bash
python experiment.py --provider openai --api-key sk-...
python experiment.py --provider anthropic --api-key sk-ant-...
python experiment.py --provider google --api-key AIza...
python experiment.py --provider deepseek --api-key sk-...
python experiment.py --provider openclaw
```

Takes about 10 minutes. Costs less than $0.10 on most providers. Your API key never leaves your machine — only the result JSON is submitted.

---

## Contributing results

Run the experiment, then open a PR adding your result file from `results/` to this repo. The file contains only win/loss counts and response previews — no API keys.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## Questions we're exploring

- Does this effect hold across different model families?
- Does it vary with model size?
- Does it change if the prompt is in Chinese instead of English?
- Is it consistent across product categories?

Discuss in [Issues](../../issues) or [Discussions](../../discussions).

---

## What's the narrative style doing exactly?

The pattern seems to be two things working together:

1. **Cross-domain analogy** — connecting the product to something unrelated (coral reefs rebuilding, jazz improvisation, forest canopies)
2. **Open invitation** — ending with a question that draws the reader in

We're calling this combination AIO (AI Optimization) — the hypothesis being that it functions like SEO but for AI recommendation systems rather than search rankings.

---

MIT license.
