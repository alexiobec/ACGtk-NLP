import create_files as cf


# tagset to use for unsupervised training
tagset = ["ADJ", "ADV", "PRON", "CONJ", "DET", "NOUN", "PONCT", "PRON", "VERB"]

# max_iterations for unsupervised training
max_iter = 20


### French example ###
gen_text = cf.genesis.words("french.txt")
gen_sentences = cf.genesis.sents("french.txt")
french_tagger = cf.train(gen_sentences, 1000, False, max_iter=max_iter)[0]
cf.create_files_from_scratch("unlabelled_genesis", "fr",
                             french_tagger, gen_text[:15], typeprob="prob")
"""
### Brown example ###
brown_tagger = cf.train(cf.brown, 1000,  max_iter=max_iter)[0]
cf.create_files_from_scratch("brown", "en",
                             brown_tagger, cf.brown.words()[1000:2000], typeprob="prob")
"""
