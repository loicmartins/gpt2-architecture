# -*- coding: utf-8 -*-

## Libraries used
import time
import numpy as np
import tiktoken
import torch
import torch.nn as nn



## Function that output a tensor of the tokenized text
def text_to_token_ids(text, tokenizer):

    encoded = tokenizer.encode(text, allowed_special={'<|endoftext|>'})
    encoded_tensor = torch.tensor(encoded).unsqueeze(0)

    return encoded_tensor



### Multi-Head Attention Class (in the TransformerBlock)
class MultiHeadAttention(nn.Module):

    def __init__(self, d_in, d_out, context_length, dropout, num_heads, qkv_bias=False):
        super().__init__()
        assert d_out % num_heads == 0, "d_out must be divisible by num_heads"

        self.d_out = d_out
        self.num_heads = num_heads
        self.head_dim = d_out // num_heads

        self.W_query = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.W_key = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.W_value = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.out_proj = nn.Linear(d_out, d_out)
        self.dropout = nn.Dropout(dropout)
        self.register_buffer("mask", torch.triu(torch.ones(context_length, context_length), diagonal=1))


    def forward(self, x):
        b, num_tokens, d_in = x.shape
        print("Step 1 inside the Multi-Headed Attention Layer: Embedding Matrix.")
        time.sleep(3)
        keys = self.W_key(x)
        queries = self.W_query(x)
        values = self.W_value(x)
        keys = keys.view(b, num_tokens, self.num_heads, self.head_dim)
        values = values.view(b, num_tokens, self.num_heads, self.head_dim)
        queries = queries.view(b, num_tokens, self.num_heads, self.head_dim)
        keys = keys.transpose(1, 2)
        queries = queries.transpose(1, 2)
        values = values.transpose(1, 2)
        print("This is the shape of Queries Matrix:", queries.shape)
        print("This is the shape of Keys Matrix:", keys.shape)
        print("This is the shape of Values Matrix:", values.shape)
        print("Example of the Queries Matrix:", queries)
        time.sleep(5)

        print("\n")
        print("\n")

        print("Step 2 inside the Multi-Headed Attention Layer: Attention Scores.")
        print("We compute the Attention Scores: Queries @ Keys.T")
        time.sleep(3)
        attn_scores = queries @ keys.transpose(2, 3)
        print("This is the shape of the Attention Scores Matrix:", attn_scores.shape)
        print("And the output itself is:")
        print(attn_scores)
        time.sleep(5)

        print("\n")
        print("\n")

        print("Step 3 inside the Multi-Headed Attention Layer: Causal Attention Masking.")
        time.sleep(3)
        mask_bool = self.mask.bool()[:num_tokens, :num_tokens]
        attn_scores.masked_fill_(mask_bool, -torch.inf)
        print("This is the output, in which we can see the mask applied:")
        print(attn_scores)
        time.sleep(5)

        print("\n")
        print("\n")

        print("Step 4 inside the Multi-Headed Attention Layer: Attention Weights.")
        time.sleep(3)
        attn_weights = torch.softmax(attn_scores / keys.shape[-1]**0.5, dim=-1)
        print("This is the shape of the Attention Weights Matrix:", attn_weights.shape)
        print("And the output itself is:")
        print(attn_weights)
        time.sleep(5)

        print("\n")
        print("\n")

        attn_weights = self.dropout(attn_weights)

        print("Step 5 inside the Multi-Headed Attention Layer: Context Vectors.")
        print("We compute the Context Vectors: Attention Weights @ Values")
        time.sleep(3)
        context_vec = (attn_weights @ values).transpose(1, 2)
        print("This is the shape of the Context Vectors:", context_vec.shape)
        print("And the output itself is:",)
        print(context_vec)
        time.sleep(5)

        context_vec = context_vec.contiguous().view(b, num_tokens, self.d_out)
        context_vec = self.out_proj(context_vec)

        return context_vec



### Normalization Class
class LayerNorm(nn.Module):

    def __init__(self, emb_dim):
        super().__init__()
        self.eps = 1e-8
        self.scale = nn.Parameter(torch.ones(emb_dim))
        self.shift = nn.Parameter(torch.zeros(emb_dim))


    def forward(self, x):
        mean = x.mean(dim=-1, keepdim=True)
        var = x.var(dim=-1, keepdim=True, unbiased=False)
        norm_x = (x - mean) / torch.sqrt(var + self.eps)

        return self.scale * norm_x + self.shift



### GELU Class (Activation Function)
class GELU(nn.Module):

    def __init__(self):
        super().__init__()


    def forward(self, x):
      x = 0.5 * x * (1 + torch.tanh(
            torch.sqrt(torch.tensor(2.0 / torch.pi)) *
            (x + 0.044715 * torch.pow(x, 3))))

      return x



### Feed Forward Class
class FeedForward(nn.Module):

    def __init__(self, config):
        super().__init__()
        self.linear1 = nn.Linear(config["emb_dim"], 4 * config["emb_dim"])
        self.act_func = GELU()
        self.linear2 = nn.Linear(4 * config["emb_dim"], config["emb_dim"])


    def forward(self, x):
      print("Step 1 inside the Feed Forward Layer: First Linear layer (we expand the embedding dimension).")
      time.sleep(3)
      x = self.linear1(x)
      print("This is the shape of the output of the first Linear Layer:", x.shape)
      time.sleep(2)
      print("We can see that the embedding dimension has been multiplied by 4.")
      print("And the output itself is:")
      print(x)
      time.sleep(5)

      print("\n")
      print("\n")

      print("Step 2 inside the Feed Forward Layer: Activation Function (non-Linearity).")
      time.sleep(3)
      x = self.act_func(x)

      print("\n")
      print("\n")

      print("Step 3 inside the Feed Forward Layer: Second Linear layer, we reduce the embedding dimension.")
      time.sleep(3)
      x = self.linear2(x)

      return x



### Transformer Block (in the GPTModel)
class TransformerBlock(nn.Module):

    def __init__(self, config):
        super().__init__()
        self.att = MultiHeadAttention(
            d_in=config["emb_dim"],
            d_out=config["emb_dim"],
            context_length=config["context_length"],
            num_heads=config["n_heads"],
            dropout=config["drop_rate"],
            qkv_bias=config["qkv_bias"])
        self.ff = FeedForward(config)
        self.norm1 = LayerNorm(config["emb_dim"])
        self.norm2 = LayerNorm(config["emb_dim"])
        self.drop_shortcut = nn.Dropout(config["drop_rate"])


    def forward(self, x):
        shortcut = x

        print("Step 1 inside the Transformer Block: Normalization layer.")
        time.sleep(3)
        x = self.norm1(x)
        print("This is the shape of the output of the layer:", x.shape)
        time.sleep(5)

        print("\n")
        print("\n")

        print("Step 2 inside the Transformer Block: Multi-Head Attention Layer.")
        time.sleep(3)
        before_attention = x
        x = self.att(x)
        print("As a reminder, before the multi-headed attention layer, the embedding matrix was as follows:")
        print(before_attention)
        time.sleep(5)
        print("This is the shape of the output of the Multi-Head Attention Layer:", x.shape)
        print("And the output itself is:")
        print(x)
        time.sleep(5)

        print("\n")
        print("\n")

        print("Step 3 inside the Transformer Block: Dropout.")
        time.sleep(3)
        x = self.drop_shortcut(x)
        print("This is the shape of the output of the layer:", x.shape)
        time.sleep(5)

        x = x + shortcut
        shortcut = x

        print("\n")
        print("\n")

        print("Step 4 inside the Transformer Block: Normalization layer.")
        time.sleep(3)
        x = self.norm2(x)
        print("This is the shape of the output of the layer:", x.shape)
        time.sleep(5)

        print("\n")
        print("\n")

        print("Step 5 inside the Transformer Block: Feed-Forward Layer.")
        time.sleep(3)
        x = self.ff(x)
        print("This is the shape of the output of Feed-Forward Layer:", x.shape)
        print("It's the same dimension of the input, despite a dimension change in the layer.")
        print("And the output itself is:")
        print(x)
        time.sleep(5)

        print("\n")
        print("\n")

        print("Step 6 inside the Transformer Block: Dropout.")
        time.sleep(3)
        x = self.drop_shortcut(x)
        print("This is the shape of the output of the layer:", x.shape)
        time.sleep(5)

        x = x + shortcut

        return x



### GPT Model Class
class GPTModel(nn.Module):

    def __init__(self, config):
        super().__init__()
        # (1) Embedding layer
        self.tok_emb = nn.Embedding(config["vocab_size"], config["emb_dim"])
        self.pos_emb = nn.Embedding(config["context_length"], config["emb_dim"])
        # (2) Dropout
        self.drop_emb = nn.Dropout(config["drop_rate"])
        # (3) Transformer Blocks
        self.trf_blocks = nn.Sequential(
            *[TransformerBlock(config) for _ in range(config["n_layers"])])
        # (4) Normalization Layer
        self.final_norm = LayerNorm(config["emb_dim"])
        # (5) Output layer
        self.out_head = nn.Linear(config["emb_dim"], config["vocab_size"], bias=False)


    def forward(self, in_ids):
        batch_size, seq_len = in_ids.shape

        print("This is the tokenized version of the input text:")
        print(in_ids)
        print("This is the shape of the input:", in_ids.shape)
        time.sleep(5)

        print("\n")
        print("\n")

        # (1) Embedding Layer
        print("Step 1 of the GPT Model: Embedding Matrix.")
        time.sleep(3)
        tok_embeds = self.tok_emb(in_ids)
        pos_embeds = self.pos_emb(torch.arange(seq_len, device=in_ids.device))
        x = tok_embeds + pos_embeds
        start_matrix = x
        print("This is the shape of the output of the layer:", x.shape)
        print("And the output itself is:")
        print(x)
        print("\n")
        print("We have now an embedding vector for each token.")
        time.sleep(5)

        print("\n")
        print("\n")

        # (2) Regularization Layer
        print("Step 2 of the GPT Model: Dropout (regularization).")
        time.sleep(3)
        x = self.drop_emb(x)
        print("This is the shape of the output of the layer:", x.shape)
        print("And the output itself is:")
        print(x)
        time.sleep(5)

        print("\n")
        print("\n")

        # (3) Transformer Block
        print("Step 3 of the GPT Model: Transformer Block.")
        time.sleep(3)
        x = self.trf_blocks(x)
        end_matrix = x
        print("This is the shape of the final output of the Transformer Block:", x.shape)
        print("And the output itself is:")
        print(x)
        time.sleep(5)

        print("\n")
        print("\n")

        # (4) Normalization Layer
        print("Step 4 of the GPT Model: Normalization Layer.")
        time.sleep(3)
        x = self.final_norm(x)
        print("This is the shape of the output of the layer:", x.shape)
        time.sleep(5)

        print("\n")
        print("\n")

        # (5) Output Layer
        print("Step 5 of the GPT Model (last step): Output Layer.")
        time.sleep(3)
        logits = self.out_head(x)
        print("This is the shape of the final output of the model:", logits.shape)
        print("And the output itself is:")
        print(logits)

        print("\n")
        print("\n")

        return logits, start_matrix, end_matrix



### Main Function to run the model
def main(txt, tokenizer):
  print("\n")
  print("The input text is:", '"',txt,'"')
  print("\n")
  time.sleep(3)
  ## Tokenize the text
  txtToken = text_to_token_ids(txt, tokenizer)
  ## Create an object instance of the GPTModel
  model = GPTModel(basicConfig)
  ## Run the model
  logits, start_matrix, end_matrix = model(txtToken)



### Run the script
if __name__ == "__main__":

  print("\n")
  print("This script shows the different steps of the model, the input and the output themself have no meaning.")
  print("We don't want to train the model, just show the architecture of the model and see how data flows through the different layers. \n")
  time.sleep(5)

  ## Initialize Tokenizer
  # we use tiktoken, from Open AI, to tokenize the text
  tokenizer = tiktoken.get_encoding("gpt2")

  ## Basic configurations
  basicConfig = {
    "vocab_size": 50257,
    "context_length": 20,
    "emb_dim": 12,
    "n_heads": 1,
    "n_layers": 1,
    "drop_rate": 0.1,
    "qkv_bias": False
  }

  ## Basic input text
  txt = "Explain me how LLM works"

  ## Call the main function
  main(txt, tokenizer)
