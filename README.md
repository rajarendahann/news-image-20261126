# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/rajarendahann/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/rajarendahann/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A newspaper front page of Thursday 26 November 2026 — masthead, region counters, three big story cards, a 3x3 story grid, a "where it happened" world map, an "also on" list and a date-checked footer. Drawn entirely in pure Python stdlib (zlib + struct): no image libraries, no network, deterministic output.

Entered on [make.fun](https://make.fun/bounty/news-image-20261126) for the news-image-20261126 bounty.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `entry.png` (1024x1024). With `MAKEFUN_OUTPUT_DIR` unset it defaults to `/output/entry.png`, falling back to the current working directory if `/output` cannot be created. Two runs produce byte-identical output.
