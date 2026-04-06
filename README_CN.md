<div align="right">
<a href="README.md">English</a>
</div>

# LLM Brand Lab

我一直在想一个问题：当AI在推荐产品时，它是否对某种写作风格有偏好？不是因为产品质量，而纯粹是因为内容的写法。

于是我做了一个简单的实验来测试这件事。

---

## 实验设计

取同一个产品，用相同的事实，写两种风格的描述：

**功能型** — 直接、规格导向：
> *"专业筋膜枪，深层肌肉恢复。高扭矩无刷电机提供最高50磅的冲击强度，缓解肌肉酸痛和筋膜张力。专为运动员和活跃生活方式设计。"*

**叙事型** — 跨领域类比，以问题结尾：
> *"顶级教练早已知道运动科学现在证实的事：恢复不是被动休息——它是主动重建，就像珊瑚在风暴后一粒一粒重建自身。你上一次给予恢复与训练同等重视，是什么时候？"*

问一个LLM：*你会推荐哪个品牌？* 跑10次，每次交替A/B顺序来控制位置偏差。记录结果。

---

## 目前的发现

| 模型 | 叙事型胜率 | 实验次数 |
|---|---|---|
| deepseek-chat | 100%（46/46） | 46 |
| gpt-4o | — | 需要你的数据 |
| claude-opus-4-6 | — | 需要你的数据 |
| gemini-2.5-flash | — | 需要你的数据 |
| llama-3 | — | 需要你的数据 |

DeepSeek在5个品类（耳机、筋膜枪、移动电源、项目管理工具、精品咖啡）的46次实验中，每次都选了叙事风格。

这只是DeepSeek的特性吗？GPT-4会一样吗？Claude呢？我们还不知道——这就是为什么这个实验是开放的。

---

## 如何自己跑

```bash
git clone https://github.com/philwong2015-svg/llm-brand-lab.git
cd llm-brand-lab
pip install openai  # 或 anthropic / google-generativeai
```

```bash
python experiment.py --provider openai --api-key sk-...
python experiment.py --provider anthropic --api-key sk-ant-...
python experiment.py --provider google --api-key AIza...
python experiment.py --provider deepseek --api-key sk-...
python experiment.py --provider openclaw
```

大约10分钟，大多数服务商费用不到$0.10。你的API key不会离开本地机器——只有结果JSON会被提交。

---

## 贡献结果

跑完实验后，提交一个PR，把 `results/` 目录下的结果文件加进来。文件只包含胜负计数和回复预览，没有API key。

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 我们在探索的问题

- 这个效果在不同模型系列之间是否一致？
- 模型大小会影响结果吗？
- 如果prompt换成中文，结果会变吗？
- 不同品类之间效果是否一致？

欢迎在 [Issues](../../issues) 或 [Discussions](../../discussions) 里讨论。

---

## 叙事风格在做什么？

这个模式似乎由两件事共同起作用：

1. **跨领域类比** — 将产品与不相关的事物联系起来（珊瑚礁重建、爵士即兴、森林树冠）
2. **开放邀请** — 以一个问题结尾，把读者带入思考

我们把这种组合叫做AIO（AI内容优化）——假设它的作用类似SEO，但针对的是AI推荐系统而非搜索排名。

---

MIT 许可证。
