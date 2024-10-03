# Bad Poetry Generator
Generating poetry using Markov Chains based on Emily Dickinson's poetry from [Gutenberg.org](https://www.gutenberg.org/files/12242/12242-h/12242-h.htm).
Approaches like vanilla and higher order Markov chains will be explored. If time allows I will try and train an LSTM deep.
neural network to generate more coherent poetry.

This is a project for the course on Computational Creativity at the [Master's program in Computer Science at the Leiden university](https://www.universiteitleiden.nl/en/education/study-programmes/master/computer-science) given by [Prof. Rob Saunders](https://www.universiteitleiden.nl/en/staffmembers/rob-saunders#tab-1)

# Repository structure
- `Dataset/`: Contains the data used for training the models.
- `MarkocChains/`: Contains the trained Markov Chains models.
- `LSTM/`: Contains the trained LSTM models. ETA soon
- `data_processor.py`: Contains the code to process the raw data to a usable format for the Markov Chain model and the LSTM
- `markov_chain.py`: Contains the code to train the Markov Chain models.

# Pre-requisites
- Python 3.11 or Higher (This code was validated on Python 3.11)
- ```pip install -r requirements.txt```Run this command to install the required libraries. (Only NumPy to be fair)

# Data Pre-processing
If you feel so inclined to use the data pre-processing yourself, you can run the data_processor.py file. 
This will generate a file called `cleaned_poems.json` which will be used to train the Markov Chain models. This file
can be found in the `Dataset/Cleaned` folder.

If you are running from a command line interface, you can run the following command:
```python data_processor.py```. If you are in an IDE just run the file as you would normally.


# Training and running the Markov Chain models
In this section we will discuss how to train and use a Markov chain model of any order. We will also discuss how to only
load in an existing model to generate poems without training anything.

## Training the model
To train the markov chain model do the following:
1. Open the `markov_chain.py` file and go to line 127.
2. Line 131 instantiates the PoemGenerator class. A few parameters can be passed to the class:
    - `poem_file`: The file containing the poems. Default is `cleaned_poems.json`. (don't change this unless you have 
   your own poem dataset that you created with your own methods or saved the cleaned data somewhere else)
    - `order`: The order of the Markov Chain. Default is 1.
    - `model_filename`: The filename to save the model in a `.pkl` format.
    - `save_model`: Boolean to save the model. Default is `False`. (enable if you want to save the model for later use)
    - `build_model`: Boolean to build the model. Default is `True`. (enable if you want to train the model, 
      disable if you want to load a pre-trained model. The PoemGenerator class needs to be instantiated with `order` set
   to whatever order your saved model was trained for if you want to use a pre-trained model).

To build the model and directly use it do the following:

3. Set `build_model` to `True`
4. Set `save_model` to `True`
5. Set the `model_filename` to the desired filename.
6. Set the `order` to the desired order.
7. Line 132 will call the `generator.generate_poem()` Method. Set `max_words` to the desired number of words for the poem. Set 
`load_markov_chain` to `True` if you want to load the saved model from disk. Set it to `False` if you want to use the 
model that is in memory. Set `model_name` to the filename of the model you want to load. This can be used if you want to
load in your just trained and saved model for some reason, or if you did not build a model and wanted to use an 
exisiting model.
8. Run the file using the ```python markov_chain.py``` command, or using your normal method in your IDE that you prefer. 
The model will be trained and a poem will be generated.

**IMPORTANT!!!** If you are using a pre-trained model, make sure that the `order` is the same as the model you are
using. Example: you are loading a 2nd order model. Then, when instantiating the PoemGenerator(), set the `order`= 2. If
you are using a 1st order model, set the `order`= 1. If you are using a 3rd order model, set the `order`= 3, etc etc.

It is more convoluted than it should be, but I cannot be asked to make it more user-friendly at this point in time.

