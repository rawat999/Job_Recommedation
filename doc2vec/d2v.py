import os.path
import numpy as np
from gensim.models.doc2vec import Doc2Vec
from doc2vec.prepraredata import preprocess_text


class LoadDoc2VecModel(object):
    def __init__(self, trained_model):
        if os.path.exists(trained_model):
            self.model_path = trained_model
            self.model = Doc2Vec.load(self.model_path)
        else:
            raise "{} is file not exist!".format(trained_model)

    def get_similarity(self, doc1, doc2):
        # cosine similarity
        cosine_similarity = self.model.similarity_unseen_docs(doc1, doc2)
        return cosine_similarity

    def get_vector(self, doc):
        vector = self.model.infer_vector(doc)
        return vector


class GetSimilarTopDocs(object):
    def __init__(self, d2v_object):
        if isinstance(d2v_object, LoadDoc2VecModel):
            self.d2v = d2v_object
        else:
            raise "{} is not object of LoadDoc2VecModel".format(d2v_object)

    def get_similar_documents(self, query_doc, corpus):
        similarities = np.zeros(shape=(corpus.shape[0],))
        for i, doc in enumerate(corpus):
            similarities[i] = self.d2v.get_similarity(query_doc, doc)
        return similarities

    def get_all_similar_docs(self, corpus, topn=2):
        corpus = list(map(preprocess_text, corpus))
        if isinstance(corpus, list):
            corpus = np.array(corpus, dtype=object)
        each_similar_docs = {}
        if corpus.shape[0] < topn:
            topn = corpus.shape[0]
        for i, query in enumerate(corpus):
            sim_score = self.get_similar_documents(query, corpus)
            most_similar_docs = (sim_score.argsort()[::-1])[1:topn]
            if i not in each_similar_docs:
                each_similar_docs[i] = most_similar_docs.tolist()
        return each_similar_docs


"""q = np.array(['c++', 'python', 'django', 'engineering'], dtype=object)
corpus = np.array([['c++', 'python', 'engineering', 'django'], ['great', 'this', 'I', 'know', 'model', 'education'], ['no', 'one', 'wants', 'similar'], ['fan', 'horse']], dtype=object)
model = LoadDoc2VecModel(trained_model='trained_d2v_model')
document = GetSimilarTopDocs(model)
sims = document.get_similar_documents(q, corpus)
sims_docs = document.get_similar_docs(corpus)
print(sims.shape)
print(sims)
print(sims_docs)"""


"""doc1 = ['c++', 'python', 'djanjo', 'computer']
doc2 = ['computer', 'vision', 'abhishek']

model = LoadDoc2VecModel(trained_model='trained_d2v_model')
print(isinstance(model, LoadDoc2VecModel))

v1 = model.get_vector(doc1)
v2 = model.get_vector(doc2)
sim = model.get_similarity(doc1, doc2)
np_sim = np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))

print(sim)
print(np_sim)"""
