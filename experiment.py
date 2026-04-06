#!/usr/bin/env python3
"""
LLM Brand Lab — Experiment Runner
==================================
Tests whether narrative-style content (cross-domain analogy + open invitation)
influences which brand an LLM recommends over functional-style content.

Supports: OpenAI, Anthropic, Google, DeepSeek, OpenClaw
Results are saved locally — your API key is never shared.

Usage:
    python experiment.py --provider openai --api-key sk-...
    python experiment.py --provider anthropic --api-key sk-ant-...
    python experiment.py --provider google --api-key AIza...
    python experiment.py --provider deepseek --api-key sk-...
    python experiment.py --provider openclaw          # if you have OpenClaw installed
"""

import argparse
import json
import os
import random
import shutil
import subprocess
import sys
import time
from datetime import datetime

# ── Brand content pairs ─────────────────────────────────────────────────────
# Each pair: text_a = functional style, text_b = narrative/AIO style
# Both describe the SAME product with SAME facts — only writing style differs.

with open(os.path.join(os.path.dirname(__file__), "brands", "pairs.json")) as f:
    BRAND_PAIRS = json.load(f)

# ── LLM providers ────────────────────────────────────────────────────────────

def ask_openai(prompt, api_key, model="gpt-4o"):
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )
        return resp.choices[0].message.content.strip()
    except ImportError:
        sys.exit("Install openai: pip install openai")

def ask_anthropic(prompt, api_key, model="claude-opus-4-6"):
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        resp = client.messages.create(
            model=model,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text.strip()
    except ImportError:
        sys.exit("Install anthropic: pip install anthropic")

def ask_google(prompt, api_key, model="gemini-2.5-flash"):
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        m = genai.GenerativeModel(model)
        resp = m.generate_content(prompt)
        return resp.text.strip()
    except ImportError:
        sys.exit("Install google-generativeai: pip install google-generativeai")

def ask_deepseek(prompt, api_key, model="deepseek-chat"):
    try:
        import openai
        client = openai.OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )
        return resp.choices[0].message.content.strip()
    except ImportError:
        sys.exit("Install openai: pip install openai")

def ask_openclaw(prompt):
    if not shutil.which("openclaw"):
        sys.exit("openclaw not found. Install OpenClaw or use --provider openai/anthropic/google/deepseek")
    result = subprocess.run(
        ["openclaw", "agent", "--agent", "main", "--message", prompt, "--json", "--timeout", "120"],
        capture_output=True, text=True, timeout=150,
    )
    try:
        d = json.loads(result.stdout)
        payloads = d.get("result", {}).get("payloads", [])
        if payloads:
            return payloads[0].get("text", "").strip()
    except Exception:
        pass
    return result.stdout.strip()

def ask_llm(prompt, provider, api_key, model):
    if provider == "openai":
        return ask_openai(prompt, api_key, model or "gpt-4o")
    elif provider == "anthropic":
        return ask_anthropic(prompt, api_key, model or "claude-opus-4-6")
    elif provider == "google":
        return ask_google(prompt, api_key, model or "gemini-2.5-flash")
    elif provider == "deepseek":
        return ask_deepseek(prompt, api_key, model or "deepseek-chat")
    elif provider == "openclaw":
        return ask_openclaw(prompt)
    else:
        sys.exit(f"Unknown provider: {provider}")

# ── Experiment logic ──────────────────────────────────────────────────────────

def build_prompt(pair, order):
    """order='ab' means text_a shown as Brand A, text_b as Brand B"""
    if order == "ab":
        brand_a_name, text_a = pair["brand_a"], pair["text_a"]
        brand_b_name, text_b = pair["brand_b"], pair["text_b"]
        narrative_label = "B"
    else:
        brand_a_name, text_a = pair["brand_b"], pair["text_b"]
        brand_b_name, text_b = pair["brand_a"], pair["text_a"]
        narrative_label = "A"

    prompt = f"""I'm comparing two brand descriptions for {pair['category']} products. \
Both products have identical functionality. Please tell me which brand you would more \
likely recommend to a friend, and briefly explain why.

Brand A ({brand_a_name}):
{text_a}

Brand B ({brand_b_name}):
{text_b}

Please start your response with "A" or "B" to clearly indicate your recommendation."""

    return prompt, narrative_label

def detect_winner(response, narrative_label):
    """Returns (winner: 'A'|'B'|'unclear', narrative_won: bool|None)"""
    if not response or len(response) < 3:
        return "unclear", None
    if "rate limit" in response.lower() or response.startswith("ERROR"):
        return "unclear", None

    r = response.strip().upper()

    if r.startswith("A") or r.startswith("**A") or r.startswith("## A"):
        winner = "A"
    elif r.startswith("B") or r.startswith("**B") or r.startswith("## B"):
        winner = "B"
    elif any(k in response for k in ["recommend A", "choose A", "prefer A", "go with A", "Brand A"]):
        winner = "A"
    elif any(k in response for k in ["recommend B", "choose B", "prefer B", "go with B", "Brand B"]):
        winner = "B"
    else:
        return "unclear", None

    return winner, (winner == narrative_label)

def run_experiment(provider, api_key, model, runs_per_pair=10, delay=5):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = {
        "meta": {
            "provider": provider,
            "model": model,
            "timestamp": timestamp,
            "runs_per_pair": runs_per_pair,
            "version": "1.0",
        },
        "summary": {},
        "raw": [],
    }

    total_valid = 0
    total_narrative_wins = 0
    total_unclear = 0

    print(f"\n{'='*55}")
    print(f"  LLM Brand Lab — {provider} / {model or 'default'}")
    print(f"  {runs_per_pair} runs × {len(BRAND_PAIRS)} pairs = {runs_per_pair * len(BRAND_PAIRS)} total")
    print(f"{'='*55}\n")

    for pair_id, pair in BRAND_PAIRS.items():
        pair_wins = 0
        pair_valid = 0
        pair_unclear = 0
        print(f"▶ {pair['category']}")

        for i in range(runs_per_pair):
            order = "ab" if i % 2 == 0 else "ba"
            prompt, narrative_label = build_prompt(pair, order)

            try:
                response = ask_llm(prompt, provider, api_key, model)
            except Exception as e:
                response = f"ERROR: {e}"

            winner, narrative_won = detect_winner(response, narrative_label)

            record = {
                "pair_id": pair_id,
                "run_idx": i,
                "order": order,
                "narrative_label": narrative_label,
                "winner": winner,
                "narrative_won": narrative_won,
                "response_preview": response[:200],
            }
            results["raw"].append(record)

            if winner == "unclear":
                pair_unclear += 1
                total_unclear += 1
                print(f"  [{i+1:02d}] ❓ unclear")
            elif narrative_won:
                pair_wins += 1
                pair_valid += 1
                total_narrative_wins += 1
                total_valid += 1
                print(f"  [{i+1:02d}] ✅ narrative wins ({winner})")
            else:
                pair_valid += 1
                total_valid += 1
                print(f"  [{i+1:02d}] ❌ functional wins ({winner})")

            if i < runs_per_pair - 1:
                time.sleep(delay)

        rate = pair_wins / pair_valid * 100 if pair_valid > 0 else 0
        results["summary"][pair_id] = {
            "category": pair["category"],
            "wins": pair_wins,
            "valid": pair_valid,
            "unclear": pair_unclear,
            "win_rate_pct": round(rate, 1),
        }
        print(f"  → {pair_wins}/{pair_valid} ({rate:.0f}%) narrative wins\n")

    overall_rate = total_narrative_wins / total_valid * 100 if total_valid > 0 else 0
    results["summary"]["_overall"] = {
        "wins": total_narrative_wins,
        "valid": total_valid,
        "unclear": total_unclear,
        "win_rate_pct": round(overall_rate, 1),
    }

    print(f"{'='*55}")
    print(f"  RESULT: {total_narrative_wins}/{total_valid} = {overall_rate:.0f}% narrative wins")
    print(f"  (unclear/skipped: {total_unclear})")
    print(f"{'='*55}\n")

    # Save results
    out_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(out_dir, exist_ok=True)
    provider_slug = provider.replace("/", "-")
    model_slug = (model or "default").replace("/", "-").replace(".", "-")
    out_file = os.path.join(out_dir, f"{provider_slug}_{model_slug}_{timestamp}.json")

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Results saved to: {out_file}")
    print(f"\nTo contribute: open a PR adding this file to results/")
    return out_file

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="LLM Brand Lab — test how your LLM chooses between writing styles"
    )
    parser.add_argument("--provider", required=True,
                        choices=["openai", "anthropic", "google", "deepseek", "openclaw"],
                        help="LLM provider to use")
    parser.add_argument("--api-key", default=None,
                        help="API key (not required for openclaw)")
    parser.add_argument("--model", default=None,
                        help="Model name override (e.g. gpt-4o, claude-opus-4-6, gemini-2.5-flash)")
    parser.add_argument("--runs", type=int, default=10,
                        help="Runs per brand pair (default: 10)")
    parser.add_argument("--delay", type=int, default=5,
                        help="Seconds between requests (default: 5)")
    args = parser.parse_args()

    if args.provider != "openclaw" and not args.api_key:
        # Check environment variable
        env_map = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "google": "GOOGLE_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
        }
        env_key = env_map.get(args.provider)
        args.api_key = os.environ.get(env_key)
        if not args.api_key:
            sys.exit(f"Provide --api-key or set {env_key} environment variable")

    run_experiment(args.provider, args.api_key, args.model, args.runs, args.delay)

if __name__ == "__main__":
    main()
