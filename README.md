# Bad Poetry Generator
Generating poetry using Markov Chains based on Emily Dickinson's poetry from [Gutenberg.org](https://www.gutenberg.org/files/12242/12242-h/12242-h.htm).
Approaches like vanilla and higher-order Markov chains will be explored. 


LSTM


The model includes an embedding layer, an LSTM layer for learning word patterns, and a dense layer with softmax activation to predict the next word in a sequence. The model uses of TensorFlow and Keras libraries and NumPy which helps in number calculations, like using the np.argmax() function to find the position of the highest value in the predicted word list, which tells the model what the next word should be.


This is a project for the course on Computational Creativity at the [Master's program in Computer Science at the Leiden university](https://www.universiteitleiden.nl/en/education/study-programmes/master/computer-science) given by [Prof. Rob Saunders](https://www.universiteitleiden.nl/en/staffmembers/rob-saunders#tab-1)

