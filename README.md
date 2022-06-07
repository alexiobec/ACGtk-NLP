# ACGtk-NLP

The principal file is **create_files** in subdirectories **lex_sign**, **str_sign** and **tag_sign**.

In this file, the function to create the ACG files is **create_files_from_scratch**.
It takes for arguments : 

- the name of the file you want to create
- the language of the text (the name of the resulting files are of the form it will be of the form **name\_typeOfFile\_language.pacg** )
- the tagger, a NLtk object trained with a corpus, supervised or unsupervised
- the text you want to use the tagger on, it must de a list of word (for example, __['I','eat','an','apple','.']__ )
- the type of probability you want, "prob" is for regular probabilities, "logprob" is for -log( probabilities ) and another string will result in hiding the probabilities.

The function train is to train the tagger.
It takes for arguments : 

- the corpus for the training
- the max number of sents you want to use from the corpus
- a boolean to say if it's supervised or unsupervised training