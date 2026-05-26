import httpx, time
base = "http://127.0.0.1:8765"
while True:
    health = httpx.get(f"{base}/health").json()
    print(health)
    if health["symbols_ready"]:
        break
    if health["needs_symbol_init"] and not health["init_running"]:
        httpx.post(f"{base}/table/init")
    time.sleep(1)
entries = httpx.post(f"{base}/table/entries", timeout=10).json()
print(entries)
