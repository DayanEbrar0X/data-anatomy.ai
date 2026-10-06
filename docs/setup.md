# Setup

## 1. Python

You need Python 3.10 or newer. Check with:

```bash
python3 --version
```

If you don't have it, install it from [python.org](https://www.python.org/downloads/).

## 2. Get the code

```bash
git clone https://github.com/<your-username>/model-anatomy.git
cd model-anatomy
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

Run each script from inside its own folder, so it can find the files next to it:

```bash
cd 00-machine-learning
python3 learn.py
```

## Troubleshooting

**`ModuleNotFoundError: No module named 'houses'`** (or `facts`, `docs`, `tools`)
You ran the script from a different folder. `cd` into the lesson folder first.

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
