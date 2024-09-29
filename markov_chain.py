import os
import pickle
from collections import defaultdict
import json
import numpy as np


def weighted_random_choice(next_words_dict):
    """Select a word based on weighted probabilities."""
    next_words = list(next_words_dict.keys())
    weights = list(next_words_dict.values())
    return np.random.choice(next_words, p=np.array(weights) / np.sum(weights))


class PoemGenerator:
    def __init__(self, json_file, model_filename, order=None, save_model=False):
        self.json_file = json_file
        self.markov_chain = {}
        self.all_words = []
        self.load_poems()
        self.build_markov_chain(order, model_filename, save_model)

    def save_markov_chain(self, filename, directory):
        """Save the Markov chain to a file using pickle."""
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(os.path.join(directory, filename), 'wb') as f:
            pickle.dump(self.markov_chain, f)

    def load_markov_chain(self, filename, directory):
        """Load the Markov chain from a file using pickle."""
        with open(os.path.join(directory ,filename), 'rb') as f:
            self.markov_chain = pickle.load(f)

    def load_poems(self):
        """Load poems from a JSON file and prepare words."""
        with open(self.json_file, 'r') as f:
            poems_data = json.load(f)

        for poem in poems_data:
            poem_text = poem["text"].replace('\n\n', ' ')  # Replace with space
            words = poem_text.split()
            self.all_words.extend(words)

    def build_markov_chain(self, order=1, model_filename="markov_chain.pkl", save_model=False):
        """Build a weighted Markov chain from the loaded words."""
        for i in range(len(self.all_words) - order):
            current_word = self.all_words[i]
            next_word = self.all_words[i + order]
            if current_word not in self.markov_chain:
                self.markov_chain[current_word] = defaultdict(int)
            self.markov_chain[current_word][next_word] += 1

        # Save markov chain
        if save_model:
            self.save_markov_chain(model_filename, "Dataset/MarkovChain")

    def generate_poem(self, max_words=50, start_word="<START>", load_markov_chain=False, model_name=None):
        """Generate a poem based on the Markov chain."""
        current_word = start_word
        poem = []

        if load_markov_chain:
            try:
                self.load_markov_chain(model_name, "Dataset/MarkovChain")
                print("Model loaded successfully. \n\n")
            except FileNotFoundError:
                print("Model file not found. Make sure the model exists.")
                return

        while len(poem) < max_words and current_word != "<END>":
            next_words_dict = self.markov_chain.get(current_word, None)
            if not next_words_dict:
                break

            next_word = weighted_random_choice(next_words_dict)
            if next_word == "<END>":
                break

            poem.append(next_word)
            current_word = next_word

        return ' '.join(poem)


# Example usage
if __name__ == "__main__":
    poems_file = "Dataset/Cleaned/cleaned_poems.json"  # Path to your .json file
    generator = PoemGenerator(poems_file, "markov_chain_1st_order.pkl", order=1, save_model=True)
    generated_poem = generator.generate_poem(max_words=50, load_markov_chain=True, model_name="markov_chain_1st_order.pkl")
    print(generated_poem)
