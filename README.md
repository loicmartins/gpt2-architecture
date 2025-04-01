# gpt2-architecture
Notebook and Python Script to understand the "basic" inner workings of LLMs: GPT2 model code explained line-by-line.


---


📍For me, the most important thing is not knowing how to use the PyTorch framework, but the most important thing is to understand the mechanism behind every line of code, every class and every function. This repository is not a programming tutorial but an analysis of the GPT2 model code to understand the overall architecture of a Large Language Model. Of course, there are tons of architectures out there, but GPT2 seems to be accessible and a good start.

That's why I've tried to explain the “basic” architecture of an LLM using a GPT-2. The model presented is not intended to be trained, but rather to be used to visualize its inner workings.

**🗂 This repository contains:**
  - 1 Notebook: shows the GPT-2 model code with each step commented.
  - 2 Python scripts (`.ipynb` and `.py` files): run the script and follow the various `print` instructions to visualize the different steps, and also to examine the evolution of the embedding and weight matrices.


## Usage and Installation

### 1️⃣ Notebook
1. Download the Notebook: `gpt2_notebook.ipynb` or read it directly on GitHub.
2. Open it in Google Collab, Jupyter Notebook...
3. There is no point in running the notebook as it is intended for reading only.

### 2️⃣ Python script

**Option 1**
- Download/Pull the `gpt2_script.ipynb` and `requirements.txt` files on your computer.
- Run them in Google Collab, Jupyter Notebook...

**Option 2**
- Download/Pull the `gpt2_script.py` and `requirements.txt` files on your computer.
- Install the requirements using the command: `pip install -r requirements.txt`.
- Run the script using the command: `python gpt2_script.py`.


## References

📚 The code was inspired by 3 main sources:

- Video - Andrej Karpathy - Let's build GPT: from scratch, in code, spelled out - https://www.youtube.com/watch?v=kCc8FmEb1nY - Jan 17, 2023
- Book - Sebastian Raschka - Build a Large Language Model (From Scratch) - October 29, 2024
- Course - Mike X Cohen - A deep understanding of deep learning - https://www.udemy.com/course/deeplearning_x/
