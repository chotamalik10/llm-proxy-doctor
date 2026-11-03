# 🩺 LLM Proxy Doctor

A zero-dependency Python CLI utility to diagnose, benchmark, and validate OpenAI-compatible local and cloud LLM proxy endpoints. Built for developers routing IDE coding agents across custom model gateways.

## ✨ Features
- **Zero Dependencies:** Uses native Python standard libraries (`urllib`, `json`, `argparse`).
- **Latency Benchmarking:** Measures exact round-trip response times in milliseconds.
- **Schema Validation:** Verifies strict compliance with OpenAI `/v1/chat/completions` response structures.
- **CI/CD Ready:** Returns standard POSIX exit codes (`0` for healthy, `1` for failed) for automated GitHub Actions pipelines.

## 🚀 Quick Start

```bash
git clone [https://github.com/chotamalik10/llm-proxy-doctor.git](https://github.com/chotamalik10/llm-proxy-doctor.git)
cd llm-proxy-doctor
python doctor.py --url http://localhost:8000/v1 --model gpt-4o-mini

