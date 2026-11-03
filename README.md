<div align="center">

# 🩺 LLM Proxy Doctor & Live Telemetry Dashboard

**Enterprise-Grade CLI Diagnostics, Real-Time Failover Dashboard & Schema Validator for AI Gateways**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Dashboard: Live UI](https://img.shields.io/badge/Dashboard-Web%20%26%20TUI-blueviolet.svg)]()
[![OpenAI Compatible](https://img.shields.io/badge/OpenAI-v1%20Compatible-orange.svg)](https://platform.openai.com/)
[![CI Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🖥️ Live Telemetry Dashboard (TUI & Web Preview)

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ 🩺 LLM PROXY DOCTOR v1.4.0 - LIVE GATEWAY TELEMETRY          [STATUS: ONLINE]│
├──────────────────────┬────────────┬───────────┬──────────────┬───────────────┤
│ GATEWAY ROUTE        │ STATUS     │ LATENCY   │ STREAM SPEED │ SCHEMA CHECK  │
├──────────────────────┼────────────┼───────────┼──────────────┼───────────────┤
│ Primary-OpenAI-v1    │ 🟢 200 OK  │ 142 ms    │ 84.2 tok/s   │ ✅ Verified   │
│ Claude-Code-Router   │ 🟢 200 OK  │ 198 ms    │ 68.5 tok/s   │ ✅ Verified   │
│ Local-Ollama-Qwen2.5 │ 🟢 200 OK  │  34 ms    │ 42.1 tok/s   │ ✅ Verified   │
│ Fallback-Groq-Proxy  │ 🟡 429 LIM │ 610 ms    │  0.0 tok/s   │ ⚠️ Rate Limit │
├──────────────────────┴────────────┴───────────┴──────────────┴───────────────┤
│ 📊 Active Routes: 4/4  |  🛡️ Auth Leak Audit: PASSED  |  ⏱️ Auto-Refresh: 5s │
└──────────────────────────────────────────────────────────────────────────────┘

