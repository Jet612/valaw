![Valaw Banner](https://raw.githubusercontent.com/Jet612/valaw/main/assets/banner.png)

[![PyPI Version](https://img.shields.io/pypi/v/valaw?style=for-the-badge)](https://pypi.org/project/valaw/)
[![GitHub Issues](https://img.shields.io/github/issues/jet612/valaw?style=for-the-badge)](https://github.com/Jet612/valaw/issues)
[![PyPI Downloads](https://img.shields.io/pypi/dm/valaw?style=for-the-badge)](https://pypi.org/project/valaw/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/valaw?style=for-the-badge)](https://pypi.org/project/valaw/)

# valaw — Async Python Wrapper for the VALORANT API

**valaw** is a fast, typed, asynchronous Python wrapper for the [Official VALORANT API](https://developer.riotgames.com/) by Riot Games. It supports all official endpoints including match history, leaderboards, content, platform status, and console endpoints.

## Features

- **Async-first** — built on `aiohttp` for non-blocking requests
- **Typed responses** — returns typed objects instead of raw JSON (opt-out available)
- **Full endpoint coverage** — PC and console match, ranked, content, account, and status endpoints
- **Python 3.9–3.14** support

## Installation

```bash
pip install valaw
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv add valaw
```

## Quick Start

```python
import valaw
import asyncio

async def main():
    client = valaw.Client("YOUR_RIOT_API_TOKEN", "americas")
    try:
        content = await client.GET_getContent("na", "en-US")
        print(content)
    finally:
        await client.close()

asyncio.run(main())
```

## Documentation

Full documentation including all endpoints, parameters, and examples can be found at [valaw.madebyjet.dev](https://valaw.madebyjet.dev/).

## Help & Support

- Join the [Discord Server](https://discord.gg/mVXpvunBbF) for help and support
- Open an [issue on GitHub](https://github.com/Jet612/valaw/issues) if you encounter a bug

## Quick Links

- [Documentation](https://valaw.madebyjet.dev/)
- [PyPI](https://pypi.org/project/valaw/)
- [GitHub](https://github.com/Jet612/valaw)
- [Discord](https://discord.gg/mVXpvunBbF)

---

Maintained by [Jet612](https://github.com/Jet612). Contributors can be found [here](https://github.com/Jet612/valaw/graphs/contributors).
