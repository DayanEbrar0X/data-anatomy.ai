# Setup

## 1. Python

You need Python 3.10 or newer. Check with:

```bash
python3 --version
```

If you don't have it, install it from [python.org](https://www.python.org/downloads/).

## 2. Get the code

```bash
git clone https://github.com/DayanEbrar0X/data-anatomy.ai.git
cd data-anatomy.ai
```

No Git? Click **Code → Download ZIP** on the repository page and unzip it.

## 3. A virtual environment (recommended)

A virtual environment keeps this project's packages separate from the rest of your computer.

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

What gets installed:

| Package | Used by | What for |
|---------|---------|----------|
| numpy | 00, 01, 02 | Math on many numbers at once |
| pandas | Build Lab | Tables |
| pyarrow | Build Lab | Writing Parquet files |
| duckdb | Build Lab | SQL on files, no database server |

Lessons 03 to 07 use only the Python standard library.

## 4. Run a lesson

The code from each video is in the lesson's `src/` folder, and the short version (if there is one) is in `short/`:

```bash
python3 machine-learning/00-what-is-machine-learning/src/learn.py
python3 methodologies/04-ontology/short/ontology.py
```

Lessons find their own data files, so you can run them from any folder. The one exception is Build Lab: like the
video, it reads `api/` and writes `data/` relative to where you run it, so `cd` into `orders_pipeline/` first.

## Troubleshooting

**`ModuleNotFoundError: No module named 'houses'`** (or `facts`, `docs`, `tools`)
The helper file is missing from `src/`, or you copied the script somewhere else on its own. Keep each script next to
the helpers it imports.

**`ModuleNotFoundError: No module named 'numpy'`**
The packages are not installed in the Python you are using. Activate the virtual environment and run
`pip install -r requirements.txt` again.

**`FileNotFoundError: api/orders_p1.json`**
For Build Lab, run from inside `orders_pipeline/`.

**My numbers are slightly different from the video**
Every lesson uses fixed data or a fixed random seed, so the output should match exactly. If the last digit differs,
check your NumPy version (`python3 -c "import numpy; print(numpy.__version__)"`); very old versions can round
differently.

---
[Back to all lessons](../README.md)
