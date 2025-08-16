# subdomainpy - 快速高效的 Python 子域名检测工具

subdomainpy 是一款基于 Python 的异步子域名检测器，支持异步 DNS 解析和 HTTP 状态检测，帮助安全研究人员和开发者快速发现目标域名的有效子域名。它采用高性能的 uvloop 事件循环和 aiohttp 实现，具备速度快、准确度高的特点。

## 主要功能

- 异步 DNS 解析，极大提升扫描速度  
- 自动检测通配符 DNS，过滤误报  
- 支持 HTTP 状态码检测，验证子域名可用性  
- 轻松扩展，可自定义子域名字典  
- 纯 Python 实现，跨平台兼容性强  

## 安装

```
pip install -r requirements.txt
```

## 快速使用

将子域名字典文件放置在 `subdomains.txt`，格式为每行一个子域名：

```
www
mail
ftp
```

运行：

```
python subdomainpy.py
```

默认扫描 `baidu.com`，可在代码中修改目标域名。

## 适用场景

- 渗透测试与安全评估  
- 资产发现与域名监控  
- 域名安全研究与分析  

## 项目地址

欢迎 Star 和 Fork，参与改进！

---

*关键词：Python子域名爆破，子域名检测，DNS异步解析，网络安全工具，资产发现*
