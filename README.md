# LLM Brand Lab

**Do LLMs systematically prefer certain writing styles when recommending products?**

**大语言模型在推荐产品时，是否对特定写作风格存在系统性偏好？**

---

## The Question / 研究问题

When an AI is asked *"which brand should I buy?"*, does the **writing style** of brand content influence its recommendation — independent of product quality?

当AI被问到"我该买哪个品牌？"时，品牌内容的**写作风格**是否会影响它的推荐——与产品质量本身无关？

We compare two styles head-to-head across multiple LLMs:

| Style | Description |
|-------|-------------|
| **Functional** | Feature lists, specs, direct claims |
| **Narrative** | Cross-domain analogy + open-ended question |

Both texts describe the **same product** with the **same facts**. Only the writing style differs.

两种风格描述**完全相同的产品**和**相同的事实**，唯一的变量是写作方式。

---

## Results So Far / 目前结果

| Model | Narrative Win Rate | Runs | Status |
|-------|--------------------|------|--------|
| `deepseek-chat` | **100%** (46/46) | 46 | ✅ |
| `gpt-4o` | — | — | 🙋 Need your data |
| `claude-opus-4-6` | — | — | 🙋 Need your data |
| `gemini-2.5-flash` | — | — | 🙋 Need your data |
| `llama-3-70b` | — | — | 🙋 Need your data |

> DeepSeek consistently preferred narrative-style content 100% of the time across 5 product categories (earphones, massage guns, power banks, project management tools, specialty coffee).
>
> DeepSeek在5个品类（耳机、筋膜枪、移动电源、项目管理工具、精品咖啡）的46次实验中，100%偏向叙事风格内容。

**Is this model-specific? Does GPT-4 agree? Does Claude?** That's what we need your help to find out.

**这是模型特有的行为吗？GPT-4是否也如此？Claude呢？** 这正是我们需要你帮助验证的。

---

## Run the Experiment / 运行实验

### Install / 安装

```bash
git clone https://github.com/YOUR_USERNAME/llm-brand-lab.git
cd llm-brand-lab
pip install openai anthropic google-generativeai  # install what you need
```

### Run / 运行

```bash
# OpenAI
python experiment.py --provider openai --api-key sk-...

# Anthropic
python experiment.py --provider anthropic --api-key sk-ant-...

# Google Gemini
python experiment.py --provider google --api-key AIza...

# DeepSeek
python experiment.py --provider deepseek --api-key sk-...

# OpenClaw (if installed)
python experiment.py --provider openclaw
```

Or use environment variables / 或使用环境变量:

```bash
export OPENAI_API_KEY=sk-...
python experiment.py --provider openai
```

**Your API key is never sent anywhere. Results are saved locally as a JSON file.**

**你的API key不会被发送到任何地方。结果保存在本地JSON文件中。**

Takes ~10 minutes. Costs less than $0.10 for most providers.

大约需要10分钟。大多数服务商的费用不到$0.10。

---

## Contribute Your Results / 贡献你的结果

1. Run the experiment with your model
2. A result file is created in `results/`
3. Open a Pull Request adding your file

<!-- -->

1. 用你的模型运行实验
2. 在 `results/` 目录下会生成结果文件
3. 提交PR将你的文件添加进来

Your API key is **never** in the result file — only the outcomes.

结果文件中**绝对不包含**你的API key，只有实验结果。

---

## How It Works / 实验设计

Each run presents the LLM with two brand descriptions (A and B) and asks which it would recommend. The A/B assignment alternates every run to control for position bias.

每次实验向LLM展示两段品牌描述（A和B），询问它更推荐哪个。A/B的顺序每轮交替，以控制位置偏差。

```
Prompt template:
"I'm comparing two brand descriptions for [product]. Both have identical
functionality. Which would you more likely recommend to a friend?
Brand A: [text] / Brand B: [text]
Please start with 'A' or 'B'."
```

Results classified as A / B / unclear. Unclear responses are excluded from win rate calculation.

结果分为A / B / unclear三类。unclear的回复不计入胜率统计。

---

## The Writing Styles / 两种写作风格

**Functional style** (control):
> *"Powerful Massage Gun for Deep Tissue Recovery. High-torque brushless motor delivers up to 50lb of percussive intensity..."*

**Narrative style** (test):
> *"Elite coaches have always known what sports scientists now confirm: recovery isn't passive rest — it's active restructuring, the way coral rebuilds itself grain by grain after a storm..."*

The narrative style uses two techniques:
1. **Cross-domain analogy** — connecting the product to unrelated domains (coral reefs, jazz, forest canopies)
2. **Open invitation** — ending with a reflective question that invites the reader in

叙事风格使用两种技巧：
1. **跨领域类比** — 将产品与不相关领域联系（珊瑚礁、爵士乐、森林树冠）
2. **开放邀请** — 以反思性问题结尾，邀请读者参与

---

## Why This Matters / 为什么重要

As AI assistants increasingly influence purchasing decisions, understanding **what writing patterns they systematically favor** becomes critical for:

随着AI助手越来越多地影响购买决策，理解**它们系统性偏好的写作模式**变得至关重要：

- **Brand marketers** optimizing content for AI-driven discovery
- **AI researchers** studying model preference biases
- **Content strategists** navigating the shift from SEO to AIO (AI Optimization)

- **品牌营销人员** 优化内容以适应AI推荐
- **AI研究人员** 研究模型偏好偏差
- **内容策略师** 应对从SEO到AIO（AI内容优化）的转变

---

## Discussion / 讨论

Share your results and hypotheses in [GitHub Discussions](../../discussions).

在 [GitHub Discussions](../../discussions) 中分享你的结果和假设。

Questions we're investigating:
- Does narrative preference vary by model family (OpenAI vs Anthropic vs Google)?
- Does it vary by model size (GPT-4o vs GPT-4o-mini)?
- Is the effect consistent across product categories?
- Does the language of the prompt (English vs Chinese) affect results?

我们正在研究的问题：
- 叙事偏好是否因模型系列而异（OpenAI vs Anthropic vs Google）？
- 是否因模型大小而异（GPT-4o vs GPT-4o-mini）？
- 效果在不同品类中是否一致？
- prompt的语言（英文vs中文）是否影响结果？

---

## License / 许可

MIT — use freely, cite if you publish.

MIT — 自由使用，发表时请注明出处。
