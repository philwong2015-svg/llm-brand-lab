<div align="right">
<a href="README_CN.md">中文版</a>
</div>

<br>

# LLM Brand Lab

When someone asks an AI assistant "what's a good massage gun?" or "which project management tool should I use?", something has to determine the answer. But what, exactly?

It's tempting to assume AI recommendations reflect some objective synthesis of reviews, rankings, and reputation. But there's a more uncomfortable possibility: that the *way* a brand writes about itself — independent of product quality — influences which brand the AI ends up recommending.

If that's true, it has significant implications. It means AI recommendations can be shaped. It means brands that understand this will have a systematic advantage over those that don't. And it means we're entering a period where content optimization for AI systems — not just for search engines — is a real and largely unmapped discipline.

We started running experiments to find out.

---

## What we found

The experiment is simple: take two descriptions of the same product, written with the same facts but different styles. Ask an LLM which brand it would recommend. Repeat, alternating which description appears as "Brand A" and which as "Brand B" to control for position effects. Exclude unclear responses. Record the win rate.

Here's what the two styles look like:

<table>
<tr>
<td width="50%" valign="top">

**Functional**
<br><sub>Direct, spec-led, features-first</sub>

<br>

*"Powerful Massage Gun for Deep Tissue Recovery. High-torque brushless motor delivers up to 50lb of percussive intensity to relieve muscle soreness and fascia tension. Premium rechargeable battery for sustained performance. Designed for athletes and active lifestyles."*

</td>
<td width="50%" valign="top">

**Narrative**
<br><sub>Cross-domain analogy + open question</sub>

<br>

*"Elite coaches have always known what sports scientists now confirm: recovery isn't passive rest — it's active restructuring, the way coral rebuilds itself grain by grain after a storm. RENPHO's percussion therapy reaches layers of muscle and fascia that surface-level treatment never touches. When did you last give your recovery the same focus you give your training?"*

</td>
</tr>
</table>

Across 46 runs, covering five product categories (earphones, massage guns, power banks, project management tools, specialty coffee), DeepSeek chose the narrative version every single time. **46 out of 46. 100%.**

We also ran a decomposition experiment — testing the analogy and the open question separately — and found the effect is strongest when both are present together. Neither technique alone produces the same result.

---

## What this might mean

Our working hypothesis: language models are trained on enormous amounts of human writing, where narrative structure and metaphor are consistent signals of quality, expertise, and credibility. Functional bullet-point content, by contrast, pattern-matches closely to advertising copy — which models may have learned to treat with skepticism, or at least less enthusiasm.

The two techniques we observed doing the most work:

**Cross-domain analogy** — connecting the product to something from a completely different field. Coral reefs rebuilding after a storm. Jazz improvisation. Forest canopies filtering light. The further the domain, the richer the conceptual frame the reader (or model) gets to inhabit.

**Open invitation** — ending not with a call to action, but with a question that turns a pitch into a conversation. *"When did you last give your recovery the same focus you give your training?"* The model, like a human reader, is drawn into completing the thought.

We're calling this pattern **AIO** — AI Optimization — by analogy to SEO. The hypothesis is that just as search engines rewarded certain structural signals (backlinks, keywords, page authority), AI recommendation systems may reward certain *semantic* signals. The difference is that the signals for AI are largely unknown, and almost nobody is studying them systematically.

This is speculative. That's the point of this project.

---

## Why we need more data

One model, one researcher, 46 runs. That's not enough to draw conclusions — only enough to raise questions.

Does GPT-4o show the same preference? Does Claude? What about open-source models? Does the effect hold across different product categories, or is it specific to the ones we tested? Does writing the prompt in Chinese instead of English change anything? Does model size matter?

We don't know. And finding out requires running the same experiment across a range of models, which is exactly what this project is designed to do collectively.

---

## Run the experiment

```bash
git clone https://github.com/philwong2015-svg/llm-brand-lab.git
cd llm-brand-lab
pip install openai anthropic google-generativeai  # install what you need
```

```bash
python experiment.py --provider openai    --api-key sk-...
python experiment.py --provider anthropic --api-key sk-ant-...
python experiment.py --provider google    --api-key AIza...
python experiment.py --provider deepseek  --api-key sk-...
python experiment.py --provider openclaw  # if you have OpenClaw installed
```

Takes around 10 minutes. Costs less than $0.10 on most providers. **Your API key never leaves your machine** — the script saves results as a local JSON file, which is all you submit.

---

## Current results

| Model | Win Rate | Runs | Status |
|---|---|---|---|
| `deepseek-chat` | **100%** | 46 | ✅ |
| `gpt-4o` | — | — | open |
| `gpt-4o-mini` | — | — | open |
| `claude-opus-4-6` | — | — | open |
| `gemini-2.5-flash` | — | — | open |
| `llama-3-70b` | — | — | open |

If your model isn't listed, run it anyway and note the name in your PR.

---

## Contributing

Run the experiment → result file appears in `results/` → open a pull request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the file naming convention and what to include in your PR description.

If you want to discuss methodology, alternative hypotheses, or results that don't fit the pattern — open an issue. The disagreements are as useful as the confirmations.

---

## Open questions

- Does the effect vary by model family, or is it universal?
- Is it stronger or weaker for B2B products versus consumer goods?
- What happens when the functional description is genuinely well-written — not bullet points, but clear, compelling prose?
- Does the effect persist when the AI has access to external information about the brand, rather than only the provided text?
- Most critically: does this translate to real-world AI recommendations, or only to forced A/B comparisons?

The last question is the one that actually matters. Everything else is preliminary.

---

MIT license.
