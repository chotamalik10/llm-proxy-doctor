# Troubleshooting

## Connection refused or timed out

Confirm the proxy is running and listening on the expected host and port. Check the URL, firewall, VPN, and timeout setting. For a local service, try:

```bash
python doctor.py --url "http://127.0.0.1:PORT/v1" --model "MODEL_NAME"
```

## HTTP 401 or 403

Set the credential expected by your gateway:

**PowerShell**
```powershell
$env:OPENAI_API_KEY = "your-key"
```

**macOS / Linux**
```bash
export OPENAI_API_KEY="your-key"
```

The tool also accepts `API_KEY` as a fallback. Never paste a real key into a public issue.

## HTTP 404 on /models

Some gateways intentionally do not expose model discovery. If chat completions are supported, skip that check:

```bash
python doctor.py --url "https://gateway.example/v1" --model "your-model" --skip-models
```

A 404 on `/chat/completions` usually means the base URL or API route is incorrect. Check whether your provider expects a base URL ending in `/v1`; do not append `/v1` twice.

## Target model is not listed

The model-list check reports an unlisted target as a note because some gateways accept aliases that are not returned by `/models`. The actual chat-completions check is the decisive test.

## Streaming fails but regular chat works

Run without `--stream` to isolate the standard JSON endpoint. Some gateways do not support Server-Sent Events or do not emit the standard `data: [DONE]` terminator.

## Response validation fails

The diagnostic expects the OpenAI Chat Completions response shape: `choices[0].message.content`. A provider-specific or Responses-API-only endpoint may require a compatible route or an adapter.

## Need a reproducible report?

Include the sanitized command, Python version, operating system, and failing check. Remove API keys, authorization headers, private hostnames, and sensitive response text first.
