# mh-sentiment-drift-ai
A modular engine for detecting emotional tone shifts in conversational AI — designed to power emotionally adaptive, mental health and safety-aware generative systems.

---

## Overview

This project provides a foundation for detecting sentiment drift — subtle or sudden changes in emotional tone across user interactions. Originally developed for use in mental health-oriented GenAI, it is applicable to any domain where emotional awareness, tone adjustment, or escalation are critical.

This is not a sentiment model — it is a lightweight, model-agnostic framework for tracking how sentiment changes over time and signaling when an adaptive response may be needed.



### Why This Matters

As generative AI systems take on more emotionally sensitive roles — in coaching, support, or mental health — we need infrastructure that tracks not just *what* users say, but *how they're changing* over time. 

This repo is a step toward building that emotional intelligence layer: modular, interpretable sentiment drift detection designed to be embedded directly into LLM workflows.


### Testing and Evaluation

Initial testing has been done on synthetic emotional narratives and anonymized mental health counselling sessions. We're developing a benchmark set for more rigorous evaluation of tone shift detection performance across domains.


### Extending This Repo

- Swap out the sentiment model via the `model_adapter` interface.
- Customize drift detection logic (`detector.py`) for your own windowing strategy.
- Add streaming support for real-time LLM applications.


### Join Us

This repo is a building block in creating emotionally adaptive AI systems that respond to human tone with care and context. If you're working on GenAI, mental health, or safety alignment, we’d love to collaborate.
