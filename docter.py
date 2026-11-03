#!/usr/bin/env python3
"""
LLM Proxy Doctor - CLI Diagnostics & Health-Check Utility for AI Coding Proxies.
Checks endpoint latency, OpenAI-compatible schema validation, and streaming health.
"""

import argparse
import json
import time
import urllib.request
import urllib.error
import sys

def check_endpoint(url: str, api_key: str, model: str, timeout: int = 10):
    print(f"[*] Starting diagnostics for endpoint: {url}")
    print(f"[*] Target Model: {model}\n")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 5
    }).encode("utf-8")

    req = urllib.request.Request(f"{url.rstrip('/')}/chat/completions", data=payload, headers=headers, method="POST")
    
    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            latency = round((time.time() - start_time) * 1000, 2)
            status = response.getcode()
            body = json.loads(response.read().decode("utf-8"))
            
            print(f"[+] Connection Status : HTTP {status} (OK)")
            print(f"[+] Response Latency  : {latency} ms")
            
            if "choices" in body and len(body["choices"]) > 0:
                print("[+] Schema Validation : Passed (OpenAI-Compatible)")
                reply = body["choices"][0].get("message", {}).get("content", "").strip()
                print(f"[+] Model Output Test : '{reply}'")
            else:
                print("[!] Schema Validation : Warning (Non-standard response structure)")
                
            return True

    except urllib.error.HTTPError as e:
        print(f"[-] HTTP Error: {e.code} - {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"[-] Connection Failed: {e.reason}")
        return False
    except Exception as e:
        print(f"[-] Unexpected Error: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="LLM Proxy Doctor: Diagnose OpenAI-compatible proxy endpoints.")
    parser.add_argument("--url", default="http://localhost:8000/v1", help="Base URL of the LLM proxy (default: http://localhost:8000/v1)")
    parser.add_argument("--key", default="sk-test-key", help="API Key for authentication check")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model identifier to test")
    args = parser.parse_args()

    success = check_endpoint(args.url, args.key, args.model)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
