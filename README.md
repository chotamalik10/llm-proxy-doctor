<div align="center">

# 🩺 LLM Proxy Doctor

**Enterprise-Grade CLI Diagnostics, Failover Benchmarking & Schema Validator for AI Coding Gateways**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![OpenAI Compatible](https://img.shields.io/badge/OpenAI-v1%20Compatible-orange.svg)](https://platform.openai.com/)
[![CI Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)]()

</div>

---

## 📖 Overview

**LLM Proxy Doctor** is a high-performance diagnostic and observability toolkit built for developers routing IDE coding agents (Claude Code, Cursor, Cline, Codex) across multi-provider local and cloud LLM gateways. It eliminates silent proxy failures, malformed SSE streams, and high-latency routing bottlenecks.

## 📊 Diagnostic Capabilities

| Module | Check Type | Validation Target | Output Metric |
| :--- | :--- | :--- | :--- |
| **Gateway Ping** | Connectivity & TLS | `/v1/chat/completions` | HTTP Status & TTFB (ms) |
| **Schema Guard** | Payload Structure | OpenAI Response Spec | Pass / Fail Compliance |
| **Stream Profiler** | SSE Chunk Health | Token Throughput | Tokens Per Second (TPS) |
| **Auth Auditor** | Bearer Security | Header Injection / Leaks | Security Exit Code |

## 🏗️ Architecture

```text
[ IDE / CLI Agent ] ---> [ LLM Proxy Doctor ] ---> [ Multi-Model Gateway / Local LLM ]
                                |
                                +---> Latency & TTFB Profiler
                                +---> OpenAI JSON Schema Validator
                                +---> CI/CD POSIX Exit Code Generator

