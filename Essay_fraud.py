import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load pre-trained GPT-2 model and tokenizer
model = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')


def get_perplexity(text):
    inputs = tokenizer(text, return_tensors='pt')
    outputs = model(**inputs, labels=inputs['input_ids'])
    loss = outputs.loss
    perplexity = torch.exp(loss)
    return perplexity.item()


class PerplexityApp:
    def __init__(self):
        # Streamlit page title
        st.title("Text Perplexity Detection")
        st.markdown("### Enter a text to check its perplexity (higher value suggests human-written text).")

        # Create text input for user to enter text
        self.text_input = st.text_area("Enter Text", "Type your text here.")

        # Button to calculate perplexity
        self.button = st.button("Calculate Perplexity")

        # Display results
        self.display_results()

    def display_results(self):
        if self.button:
            if self.text_input.strip():
                perplexity = get_perplexity(self.text_input)
                st.write(f"**Perplexity Score**: {perplexity:.2f}")
                if perplexity > 50:
                    st.markdown("#### Likely Human-generated text.")
                else:
                    st.markdown("#### Likely GPT-generated text.")
            else:
                st.error("Please enter some text to analyze.")

#
# if __name__ == "__main__":
#     PerplexityApp()
