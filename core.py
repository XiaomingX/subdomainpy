import asyncio
import aiodns
import aiohttp
from tqdm.asyncio import tqdm_asyncio
import uvloop
import os
import time  # 引入时间模块

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

HTTP_TIMEOUT = aiohttp.ClientTimeout(total=8)

async def resolve(domain, resolver):
    async def _resolve():
        result = await resolver.query(domain, 'A')
        return [r.host for r in result]
    try:
        return await asyncio.wait_for(_resolve(), timeout=3)
    except Exception as e:
        return []

async def check_http(session, url):
    try:
        async with session.get(url) as resp:
            if resp.status in [200, 301, 302, 403]:
                content = await resp.text()
                return resp.status, content
            return resp.status, None
    except Exception as e:
        # print(f"[HTTP error] {url}: {e}")
        return None, None

async def detect_wildcard(domain, resolver):
    random_sub = "nonexistent1234567890"
    test_domain = f"{random_sub}.{domain}"
    ips = await resolve(test_domain, resolver)
    if not ips:
        return None
    async with aiohttp.ClientSession(timeout=HTTP_TIMEOUT) as session:
        _, content = await check_http(session, f"http://{test_domain}")
        return content

async def scan_one(session, domain, wildcard_content, resolver):
    ips = await resolve(domain, resolver)
    if not ips:
        return None
    status, content = await check_http(session, f"http://{domain}")
    if wildcard_content and content == wildcard_content:
        return None
    if status:
        return (domain, ips, status)
    return None

async def scan_subdomains(domain, subdomains):
    resolver = aiodns.DNSResolver()
    print(f"[*] 检测通配符解析中...")
    wildcard_content = await detect_wildcard(domain, resolver)
    found = []
    async with aiohttp.ClientSession(timeout=HTTP_TIMEOUT) as session:
        tasks = [
            scan_one(session, f"{sub}.{domain}", wildcard_content, resolver)
            for sub in subdomains
        ]
        results = await tqdm_asyncio.gather(*tasks)
        for res in results:
            if res:
                found.append(res)
    return found

def load_subdomains(file_path="subdomains.txt"):
    if not os.path.exists(file_path):
        print(f"[!] 文件不存在: {file_path}")
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]

if __name__ == "__main__":
    start_time = time.time()  # 记录开始时间

    domain = "baidu.com"
    subdomains = load_subdomains()
    if not subdomains:
        print("[!] 未加载到任何子域名，程序结束。")
        exit(1)

    print(f"[*] 正在扫描子域名: {domain}")
    results = asyncio.run(scan_subdomains(domain, subdomains))

    print(f"\n发现有效子域名数量: {len(results)}")
    for d, ips, status in results:
        print(f"{d} - IPs: {ips} - HTTP状态码: {status}")

    end_time = time.time()
    print(f"\n✅ 扫描完成，总耗时: {end_time - start_time:.2f} 秒")
