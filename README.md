# gpt2-architecture
Notebook and Python Script to understand the "basic" inner workings of LLMs.

---

📍The aim of this repository is to provide an initial understanding of the inner workings of LLMs in the context of cybersecurity. Often focused on the infrastructure of AI systems, we forget that one of the main threats comes from the model itself. 
For example, we can access and modify the model and its internal representations. This can be compared to manipulating a person. By talking to them, we try to change their state of mind, so that they change their behavior. And this can be very dangerous, because you can leave a model on the market that manipulates people for various purposes: politics, swindling, obtaining information...

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
- Download/Pull the `gpt2_script.ipynb` file on your computer.
- Run it in Google Collab, Jupyter Notebook...

**Option 2**
- Download/Pull the `gpt2_script.py` file on your computer.
- Install the requirements using the command: `pip install -r requirements.txt`
- Run the script using the command: `python gpt2_script.py`

## Resources

📚 The code was inspired by 3 main ressources:

- Video - Andrej Karpathy - Let's build GPT: from scratch, in code, spelled out - https://www.youtube.com/watch?v=kCc8FmEb1nY - Jan 17, 2023
- Book - Sebastian Raschka - Build a Large Language Model (From Scratch) - October 29, 2024
- Course - Mike X Cohen - A deep understanding of deep learning - https://www.udemy.com/course/deeplearning_x/
