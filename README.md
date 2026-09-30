# Awesome Multimodal Agentic Retrieval

[![Discover Papers](https://github.com/Reflection0427/Awesome-Multimodal-Agentic-Retrieval/actions/workflows/discover-papers.yml/badge.svg)](https://github.com/Reflection0427/Awesome-Multimodal-Agentic-Retrieval/actions/workflows/discover-papers.yml)
[![Validate](https://github.com/Reflection0427/Awesome-Multimodal-Agentic-Retrieval/actions/workflows/validate.yml/badge.svg)](https://github.com/Reflection0427/Awesome-Multimodal-Agentic-Retrieval/actions/workflows/validate.yml)

A curated collection of papers on **multimodal retrieval, multimodal RAG, visual-document retrieval, and agentic multimodal search**.

本仓库关注“大模型如何参与多模态检索，以及检索如何增强多模态大模型与 Agent”。每篇正式收录论文都配有一张统一风格的**自绘结构摘要图**。这些图是便于快速阅读的结构化总结，并非论文原图；技术细节请以原论文为准。

**37 papers · through 2026 · weekly candidate PRs · human-reviewed merges**

## Scope

Included: MLLM retrievers and rerankers, multimodal embeddings, multimodal RAG, visual-document retrieval, multimodal browsing/search agents, and directly related surveys or benchmarks.

Excluded: conventional image-text retrieval without a large-model or agent component, multimodal generation without external retrieval, and GUI agents unrelated to information retrieval.

## Contents

- [Surveys and Roadmaps (5)](#surveys-and-roadmaps)
- [Foundations (5)](#foundations)
- [Universal Multimodal Retrievers (4)](#universal-multimodal-retrievers)
- [Visual Document Retrieval and RAG (14)](#visual-document-retrieval-and-rag)
- [Agentic Multimodal Search (9)](#agentic-multimodal-search)
- [Benchmarks](#benchmarks)
- [Automatic paper tracking](#automatic-paper-tracking)
- [Contributing](#contributing)

## Surveys and Roadmaps

综述、分类体系与研究路线图。

### A Survey of Large Language Model-Based Search Agents

**ACL 2026** · [Paper](https://aclanthology.org/2026.acl-long.374/)

A roadmap for LLM search agents, covering planning, retrieval, reasoning and evaluation.

<img src="assets/frameworks/llm-search-agents-survey.svg" alt="Framework summary for A Survey of Large Language Model-Based Search Agents" width="100%">

### Scaling Beyond Context: A Survey of Multimodal Retrieval-Augmented Generation for Document Understanding

**ACL 2026** · [Paper](https://aclanthology.org/2026.acl-long.204/) · [Code / Project](https://github.com/SensenGao/Multimodal-RAG-Survey-For-Document)

A survey of multimodal RAG for long and visually rich document understanding.

<img src="assets/frameworks/scaling-beyond-context.svg" alt="Framework summary for Scaling Beyond Context: A Survey of Multimodal Retrieval-Augmented Generation for Document Understanding" width="100%">

### Ask in Any Modality: A Comprehensive Survey on Multimodal Retrieval-Augmented Generation

**Findings of ACL 2025** · [Paper](https://aclanthology.org/2025.findings-acl.861/) · [Code / Project](https://github.com/llm-lab-org/Multimodal-RAG-Survey)

A comprehensive taxonomy of multimodal RAG datasets, retrieval, fusion, generation and agentic methods.

<img src="assets/frameworks/ask-in-any-modality.svg" alt="Framework summary for Ask in Any Modality: A Comprehensive Survey on Multimodal Retrieval-Augmented Generation" width="100%">

### Roles of Multimodal Large Language Models in Visually Rich Document Retrieval for RAG: A Survey

**IJCNLP-AACL 2025** · [Paper](https://aclanthology.org/2025.ijcnlp-long.2/)

Organizes MLLM-based document retrieval into captioning, embedding and end-to-end page representation paradigms.

<img src="assets/frameworks/mllms-in-vrd-retrieval-survey.svg" alt="Framework summary for Roles of Multimodal Large Language Models in Visually Rich Document Retrieval for RAG: A Survey" width="100%">

### Retrieving Multimodal Information for Augmented Generation: A Survey

**Findings of EMNLP 2023** · [Paper](https://aclanthology.org/2023.findings-emnlp.314/)

An early systematic review of retrieving multimodal information to augment generation.

<img src="assets/frameworks/retrieving-multimodal-information-survey.svg" alt="Framework summary for Retrieving Multimodal Information for Augmented Generation: A Survey" width="100%">

## Foundations

检索增强视觉语言模型与多模态生成的奠基工作。

### Retrieval-Augmented Multimodal Language Modeling

**ICML 2023** · [Paper](https://arxiv.org/abs/2211.12561)

RA-CM3 augments an autoregressive multimodal model with retrieved image-text memory.

<img src="assets/frameworks/ra-cm3.svg" alt="Framework summary for Retrieval-Augmented Multimodal Language Modeling" width="100%">

### REVEAL: Retrieval-Augmented Visual-Language Pre-Training with Multi-Source Multimodal Knowledge Memory

**CVPR 2023** · [Paper](https://openaccess.thecvf.com/content/CVPR2023/html/Hu_REVEAL_Retrieval-Augmented_Visual-Language_Pre-Training_With_Multi-Source_Multimodal_Knowledge_Memory_CVPR_2023_paper.html) · [Code / Project](https://reveal-cvpr.github.io/)

Retrieves evidence from multi-source multimodal memory for visual-language pre-training and downstream tasks.

<img src="assets/frameworks/reveal.svg" alt="Framework summary for REVEAL: Retrieval-Augmented Visual-Language Pre-Training with Multi-Source Multimodal Knowledge Memory" width="100%">

### Scaling Autoregressive Multi-Modal Models: Pretraining and Instruction Tuning

**arXiv 2023** · [Paper](https://arxiv.org/abs/2309.02591)

CM3Leon combines retrieval-augmented pre-training with multimodal instruction tuning.

<img src="assets/frameworks/cm3leon.svg" alt="Framework summary for Scaling Autoregressive Multi-Modal Models: Pretraining and Instruction Tuning" width="100%">

### KAT: A Knowledge Augmented Transformer for Vision-and-Language

**NAACL 2022** · [Paper](https://arxiv.org/abs/2112.08614) · [Code / Project](https://github.com/guilk/KAT)

Combines implicit model knowledge with retrieved explicit knowledge for knowledge-based VQA.

<img src="assets/frameworks/kat.svg" alt="Framework summary for KAT: A Knowledge Augmented Transformer for Vision-and-Language" width="100%">

### MuRAG: Multimodal Retrieval-Augmented Generator for Open Question Answering over Images and Text

**EMNLP 2022** · [Paper](https://aclanthology.org/2022.emnlp-main.375/)

Jointly retrieves textual and visual evidence for open-domain multimodal question answering.

<img src="assets/frameworks/murag.svg" alt="Framework summary for MuRAG: Multimodal Retrieval-Augmented Generator for Open Question Answering over Images and Text" width="100%">

## Universal Multimodal Retrievers

由 MLLM 驱动的统一检索器、Embedding 与推理型检索基准。

### MMEB-V3: Measuring Performance Gaps of Omni-Modality Embedding Models

**arXiv 2026** · [Paper](https://arxiv.org/abs/2604.23321)

Evaluates omni-modality embedding models across text, image, video, audio and agent-centric tasks.

<img src="assets/frameworks/mmeb-v3.svg" alt="Framework summary for MMEB-V3: Measuring Performance Gaps of Omni-Modality Embedding Models" width="100%">

### RMIR: A Benchmark Dataset for Reasoning-Intensive Multimodal Image Retrieval

**CVPR 2026** · [Paper](https://openaccess.thecvf.com/content/CVPR2026/papers/Li_RMIR_A_Benchmark_Dataset_for_Reasoning-Intensive_Multimodal_Image_Retrieval_CVPR_2026_paper.pdf)

Benchmarks image retrieval that requires compositional and multi-step reasoning rather than surface similarity.

<img src="assets/frameworks/rmir.svg" alt="Framework summary for RMIR: A Benchmark Dataset for Reasoning-Intensive Multimodal Image Retrieval" width="100%">

### MM-Embed: Universal Multimodal Retrieval with Multimodal LLMs

**arXiv 2024** · [Paper](https://arxiv.org/abs/2411.02571)

Turns an MLLM into a universal bi-encoder using modality-aware hard negatives and reranking.

<img src="assets/frameworks/mm-embed.svg" alt="Framework summary for MM-Embed: Universal Multimodal Retrieval with Multimodal LLMs" width="100%">

### UniIR: Training and Benchmarking Universal Multimodal Information Retrievers

**ECCV 2024** · [Paper](https://arxiv.org/abs/2311.17136) · [Code / Project](https://github.com/TIGER-AI-Lab/UniIR)

Introduces a unified multimodal retriever and the multi-task M-BEIR benchmark.

<img src="assets/frameworks/uniir.svg" alt="Framework summary for UniIR: Training and Benchmarking Universal Multimodal Information Retrievers" width="100%">

## Visual Document Retrieval and RAG

面向页面图像、布局、图表和长文档的检索增强生成。

### LAD-RAG: Layout-aware Dynamic RAG for Visually-Rich Document Understanding

**ACL 2026** · [Paper](https://aclanthology.org/2026.acl-long.724/)

Uses document layout to dynamically retrieve evidence from visually rich pages.

<img src="assets/frameworks/lad-rag.svg" alt="Framework summary for LAD-RAG: Layout-aware Dynamic RAG for Visually-Rich Document Understanding" width="100%">

### MDocRAG-RL: Empowering Multi-Modal Document RAG via Complex Visual Reasoning with Reinforcement Learning

**Findings of ACL 2026** · [Paper](https://aclanthology.org/2026.findings-acl.420/)

Applies reinforcement learning to complex visual reasoning in multimodal document RAG.

<img src="assets/frameworks/mdocrag-rl.svg" alt="Framework summary for MDocRAG-RL: Empowering Multi-Modal Document RAG via Complex Visual Reasoning with Reinforcement Learning" width="100%">

### MegaRAG: Multimodal Knowledge Graph-Based Retrieval-Augmented Generation

**ACL 2026** · [Paper](https://aclanthology.org/2026.acl-long.2218/)

Organizes heterogeneous multimodal evidence as a knowledge graph for retrieval and generation.

<img src="assets/frameworks/megarag.svg" alt="Framework summary for MegaRAG: Multimodal Knowledge Graph-Based Retrieval-Augmented Generation" width="100%">

### Progressive Re-ranking for Multimodal Retrieval-Augmented Generation via Curriculum Learning

**Findings of ACL 2026** · [Paper](https://aclanthology.org/2026.findings-acl.2045/)

Learns a multimodal reranker progressively through curriculum learning.

<img src="assets/frameworks/progressive-reranking.svg" alt="Framework summary for Progressive Re-ranking for Multimodal Retrieval-Augmented Generation via Curriculum Learning" width="100%">

### RobustVisRAG: Causality-Aware Vision-Based Retrieval-Augmented Generation under Visual Degradations

**CVPR 2026** · [Paper](https://openaccess.thecvf.com/content/CVPR2026/html/Chen_RobustVisRAG_Causality-Aware_Vision-Based_Retrieval-Augmented_Generation_under_Visual_Degradations_CVPR_2026_paper.html)

Improves vision-based RAG robustness under noisy and degraded document images.

<img src="assets/frameworks/robust-visrag.svg" alt="Framework summary for RobustVisRAG: Causality-Aware Vision-Based Retrieval-Augmented Generation under Visual Degradations" width="100%">

### ColMATE: Multi-modal Retrieval Embedding for Visually-rich Documents

**EMNLP Industry 2025** · [Paper](https://aclanthology.org/2025.emnlp-industry.145/)

Learns efficient multimodal retrieval embeddings for visually rich documents.

<img src="assets/frameworks/colmate.svg" alt="Framework summary for ColMATE: Multi-modal Retrieval Embedding for Visually-rich Documents" width="100%">

### End-to-End Optimization for Multimodal Retrieval-Augmented Generation via Reward Backpropagation

**Findings of EMNLP 2025** · [Paper](https://aclanthology.org/2025.findings-emnlp.24/)

Uses downstream generation reward to optimize the multimodal retriever end to end.

<img src="assets/frameworks/reward-backprop-mrag.svg" alt="Framework summary for End-to-End Optimization for Multimodal Retrieval-Augmented Generation via Reward Backpropagation" width="100%">

### MMDocIR: Benchmarking Multi-Modal Retrieval for Long Documents

**EMNLP 2025** · [Paper](https://aclanthology.org/2025.emnlp-main.1576/) · [Code / Project](https://mmdocrag.github.io/MMDocIR/)

Benchmarks retrieval from long documents containing text and visually rich content.

<img src="assets/frameworks/mmdocir.svg" alt="Framework summary for MMDocIR: Benchmarking Multi-Modal Retrieval for Long Documents" width="100%">

### MMDocRAG: Benchmarking Retrieval-Augmented Generation for Multi-Modal Document Understanding

**NeurIPS 2025 Datasets and Benchmarks** · [Paper](https://arxiv.org/abs/2505.16470)

Jointly evaluates multimodal document retrieval and answer generation.

<img src="assets/frameworks/mmdocrag.svg" alt="Framework summary for MMDocRAG: Benchmarking Retrieval-Augmented Generation for Multi-Modal Document Understanding" width="100%">

### VDocRAG: Retrieval-Augmented Generation over Visually-Rich Documents

**CVPR 2025** · [Paper](https://openaccess.thecvf.com/content/CVPR2025/papers/Tanaka_VDocRAG_Retrieval-Augmented_Generation_over_Visually-Rich_Documents_CVPR_2025_paper.pdf)

Builds an end-to-end retrieval and generation pipeline over visually rich documents.

<img src="assets/frameworks/vdocrag.svg" alt="Framework summary for VDocRAG: Retrieval-Augmented Generation over Visually-Rich Documents" width="100%">

### ViDoRAG: Visual Document Retrieval-Augmented Generation via Dynamic Iterative Reasoning Agents

**EMNLP 2025** · [Paper](https://aclanthology.org/2025.emnlp-main.464/) · [Code / Project](https://github.com/Alibaba-NLP/ViDoRAG)

Coordinates Seeker, Inspector and Answer agents for iterative visual-document retrieval and verification.

<img src="assets/frameworks/vidorag.svg" alt="Framework summary for ViDoRAG: Visual Document Retrieval-Augmented Generation via Dynamic Iterative Reasoning Agents" width="100%">

### VisDoM: Multi-Document QA with Visually Rich Elements Using Multimodal RAG

**NAACL 2025** · [Paper](https://aclanthology.org/2025.naacl-long.310/)

Retrieves and reasons across multiple documents containing text, charts, images and layout cues.

<img src="assets/frameworks/visdom.svg" alt="Framework summary for VisDoM: Multi-Document QA with Visually Rich Elements Using Multimodal RAG" width="100%">

### VisRAG: Vision-based Retrieval-augmented Generation on Multi-modality Documents

**ICLR 2025** · [Paper](https://arxiv.org/abs/2410.10594) · [Code / Project](https://github.com/openbmb/visrag)

Retrieves directly over document-page images to preserve layout and visual information lost by OCR pipelines.

<img src="assets/frameworks/visrag.svg" alt="Framework summary for VisRAG: Vision-based Retrieval-augmented Generation on Multi-modality Documents" width="100%">

### ColPali: Efficient Document Retrieval with Vision Language Models

**arXiv 2024** · [Paper](https://arxiv.org/abs/2407.01449) · [Code / Project](https://github.com/illuin-tech/colpali)

Represents page screenshots with VLM patch embeddings and ranks them using late interaction.

<img src="assets/frameworks/colpali.svg" alt="Framework summary for ColPali: Efficient Document Retrieval with Vision Language Models" width="100%">

## Agentic Multimodal Search

能够规划、迭代检索、检查证据并核验来源的多模态 Agent。

### DeepImageSearch: Benchmarking Multimodal Agents for Context-Aware Image Retrieval in Visual Histories

**arXiv 2026** · [Paper](https://arxiv.org/abs/2602.10809)

Benchmarks agents that retrieve images by reasoning over long visual histories and context.

<img src="assets/frameworks/deep-image-search.svg" alt="Framework summary for DeepImageSearch: Benchmarking Multimodal Agents for Context-Aware Image Retrieval in Visual Histories" width="100%">

### Fix Before Search: Benchmarking Agentic Visual Query Pre-processing in Multimodal RAG

**ICML 2026** · [Paper](https://proceedings.mlr.press/v306/zeng26w.html) · [Code / Project](https://github.com/phycholosogy/VQQP_Bench)

Benchmarks agents that repair, crop and enhance visual queries before retrieval.

<img src="assets/frameworks/fix-before-search.svg" alt="Framework summary for Fix Before Search: Benchmarking Agentic Visual Query Pre-processing in Multimodal RAG" width="100%">

### MC-Search: Evaluating and Enhancing Multimodal Agentic Search with Structured Long Reasoning Chains

**ICLR 2026** · [Paper](https://arxiv.org/abs/2603.00873) · [Code / Project](https://mc-search-project.github.io/)

Introduces structured long reasoning chains for evaluating and improving multimodal agentic search.

<img src="assets/frameworks/mc-search.svg" alt="Framework summary for MC-Search: Evaluating and Enhancing Multimodal Agentic Search with Structured Long Reasoning Chains" width="100%">

### MMSearch-Plus: Benchmarking Provenance-Aware Search for Multimodal Browsing Agents

**ICLR 2026** · [Paper](https://arxiv.org/abs/2508.21475) · [Code / Project](https://github.com/mmsearch-plus/MMSearch-Plus)

Evaluates iterative text-image browsing, answer accuracy and provenance verification.

<img src="assets/frameworks/mmsearch-plus.svg" alt="Framework summary for MMSearch-Plus: Benchmarking Provenance-Aware Search for Multimodal Browsing Agents" width="100%">

### Reason Before You Retrieve: Agentic Planning for Multi-modal RAG

**arXiv 2026** · [Paper](https://arxiv.org/abs/2607.22643)

Models user intent before retrieval and maintains a structured KnowledgeMap for subsequent search.

<img src="assets/frameworks/reason-before-retrieve.svg" alt="Framework summary for Reason Before You Retrieve: Agentic Planning for Multi-modal RAG" width="100%">

### V-Retrver: Evidence-Driven Agentic Reasoning for Universal Multimodal Retrieval

**arXiv 2026** · [Paper](https://arxiv.org/abs/2602.06034)

Uses evidence-driven agent reasoning to solve universal multimodal retrieval tasks.

<img src="assets/frameworks/v-retrver.svg" alt="Framework summary for V-Retrver: Evidence-Driven Agentic Reasoning for Universal Multimodal Retrieval" width="100%">

### VLD-RAG: Agentic Vision-Language RAG for Long, Visually Rich Multi-Page Documents

**arXiv 2026** · [Paper](https://arxiv.org/abs/2607.24748)

Uses an agentic vision-language pipeline to retrieve and reason over long multi-page documents.

<img src="assets/frameworks/vld-rag.svg" alt="Framework summary for VLD-RAG: Agentic Vision-Language RAG for Long, Visually Rich Multi-Page Documents" width="100%">

### WeAgent-MMSearch: Native Text-Vision Interaction for Multimodal Search Agents

**arXiv 2026** · [Paper](https://arxiv.org/abs/2608.28062)

Studies native text-vision interaction and visual-target localization for multimodal search agents.

<img src="assets/frameworks/weagent-mmsearch.svg" alt="Framework summary for WeAgent-MMSearch: Native Text-Vision Interaction for Multimodal Search Agents" width="100%">

### CollEX: A Multimodal Agentic RAG System Enabling Interactive Exploration of Scientific Collections

**MAGMaR at SIGIR 2025** · [Paper](https://aclanthology.org/2025.magmar-1.2/)

Supports interactive exploration of scientific collections using multimodal agentic RAG.

<img src="assets/frameworks/collex.svg" alt="Framework summary for CollEX: A Multimodal Agentic RAG System Enabling Interactive Exploration of Scientific Collections" width="100%">

## Benchmarks

| Benchmark | Focus | Paper |
|---|---|---|
| M-BEIR | Universal multi-task, cross-modal retrieval | [UniIR](https://arxiv.org/abs/2311.17136) |
| ViDoRe | Visual document page retrieval | [ColPali](https://arxiv.org/abs/2407.01449) |
| MMDocIR | Long multimodal document retrieval | [MMDocIR](https://aclanthology.org/2025.emnlp-main.1576/) |
| MMDocRAG | Joint document retrieval and generation | [MMDocRAG](https://arxiv.org/abs/2505.16470) |
| MC-Search | Multimodal agentic search and long reasoning chains | [MC-Search](https://arxiv.org/abs/2603.00873) |
| MMSearch-Plus | Browsing, provenance and evidence verification | [MMSearch-Plus](https://arxiv.org/abs/2508.21475) |
| RMIR | Reasoning-intensive image retrieval | [RMIR](https://openaccess.thecvf.com/content/CVPR2026/papers/Li_RMIR_A_Benchmark_Dataset_for_Reasoning-Intensive_Multimodal_Image_Retrieval_CVPR_2026_paper.pdf) |
| VQQP-Bench | Agentic visual-query preprocessing | [Fix Before Search](https://proceedings.mlr.press/v306/zeng26w.html) |

## Automatic paper tracking

The scheduled workflow searches arXiv, OpenAlex and Crossref every Monday. It normalizes arXiv IDs, DOIs and titles, removes duplicates, classifies likely matches, and opens or updates a candidate pull request. DBLP and official conference pages are used during human venue verification. It **never publishes a candidate directly to this README**.

A paper becomes visible only after a reviewer verifies its relevance and metadata, supplies a curator-authored framework summary, and merges the pull request. See [the tracker guide](docs/PAPER_TRACKER.md).

## Contributing

Please open an issue or pull request. Every accepted entry must include verifiable paper metadata, an appropriate category, a concise neutral summary, and 3–5 framework steps. Run:

```bash
python scripts/generate_readme.py --check
python -m unittest discover -s tests -v
```

## License and figure policy

Repository code and curator-authored metadata/diagrams are released under the MIT License. Papers, linked project assets, and author-created figures remain the property of their respective owners. The SVGs in `assets/frameworks/` are original reading aids generated from manually reviewed structural summaries; they are not reproductions of paper figures.
