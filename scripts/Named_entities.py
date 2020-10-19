#!/usr/bin/env python
# coding: utf-8

# In[16]:


import csv
import os
import pandas as pd
import nltk
import nltk.corpus
from nltk.corpus import brown
from nltk.tokenize import word_tokenize
from pprint import pprint
import matplotlib.pyplot as plt

nltk.download('brown')
nltk.download('gutenberg')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

#below did not work due to 
#with open('Datafiniti_Hotel_Reviews_Jun19.csv', encoding = "utf-8") as csv_file:
 #   article = csv_file.read()
#with open('Datafiniti_Hotel_Reviews_Jun19.csv', encoding = "utf-8") as csv_file:
article = pd.read_csv('Datafiniti_Hotel_Reviews_Jun19.csv', usecols=['reviews.text'], encoding = "utf-8")
type(article)
article = pd.DataFrame.to_string(article)
type(article)
    


# In[18]:


from nltk.tokenize import sent_tokenize, word_tokenize


# In[19]:


# Tokenize the article into sentences: sentences
sentences = sent_tokenize(article)

# Tokenize each sentence into words: token_sentences
token_sentences = [word_tokenize(sent) for sent in sentences]

# Tag each tokenized sentence into parts of speech: pos_sentences
pos_sentences = [nltk.pos_tag(sent) for sent in token_sentences]

# Create the named entity chunks: chunked_sentences
chunked_sentences = nltk.ne_chunk_sents(pos_sentences, binary=True)


# In[20]:


chunked_sentences = nltk.ne_chunk_sents(pos_sentences, binary=False)
from collections import defaultdict

# Create the defaultdict: ner_categories
ner_categories = defaultdict(int)

# Create the nested for loop
for sent in chunked_sentences:
    for chunk in sent:
        if hasattr(chunk, 'label'):
            ner_categories[chunk.label()] += 1
            
# Create a list from the dictionary keys for the cart labels: labels
labels = list(ner_categories.keys())

# Create a list of the values: values
values = [ner_categories.get(l) for l in labels]

# Create the pie chart
fig = plt.figure(figsize=(8, 8))
plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140);

#print categories
labels


# In[ ]:




