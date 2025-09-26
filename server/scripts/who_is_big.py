from importlib import metadata as md
from pathlib import Path
import sys
from tqdm import tqdm

TOP_N = int(sys.argv[1]) if len(sys.argv) > 1 else 30

def fmt(n: int) -> str:
    # 简单的人类可读格式
    for unit in ("B","KB","MB","GB","TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.1f} {unit}"
        n /= 1024

rows = []
distributions = list(md.distributions())
for dist in tqdm(distributions, desc="Analyzing packages"):
    try:
        files = dist.files or []
    except Exception:
        files = []
    total = 0
    for f in files:
        try:
            p = dist.locate_file(f)
        except Exception:
            continue
        if p.is_file():
            try:
                total += p.stat().st_size
            except Exception:
                pass
        elif p.is_dir():
            for sub in p.rglob("*"):
                if sub.is_file():
                    try:
                        total += sub.stat().st_size
                    except Exception:
                        pass
    rows.append((total, dist.metadata.get("Name") or dist.metadata["Name"]))

rows.sort(reverse=True, key=lambda x: x[0])

print(f"Installed distributions by size (Top {TOP_N}):")
for sz, name in rows[:TOP_N]:
    print(f"{fmt(sz):>10}  {name}")