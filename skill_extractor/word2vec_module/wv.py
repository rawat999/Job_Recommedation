import os
import numpy as np
from gensim.models import KeyedVectors


class W2VExtractSkills(object):
    def __init__(self, wordvectorfile):
        if os.path.exists(wordvectorfile):
            self.wordfilepath = wordvectorfile
            self.vectors = KeyedVectors.load(self.wordfilepath, mmap='r')
        else:
            raise "{} is not exist!".format(wordvectorfile)

    @staticmethod
    def get_similarity_score(v1, v2):
        score = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        return score
        
    def get_skill_score(self, query, skills):
        highest_similarity_score = 0
        try:
            query_vector = self.vectors[query]
        except KeyError:
            return 0.001
        for skill in skills:
            try:
                skill_vector = self.vectors[skill]
                sim_score = self.get_similarity_score(query_vector, skill_vector)
                if sim_score > highest_similarity_score:
                    highest_similarity_score = sim_score
            except KeyError:
                continue
        return highest_similarity_score

    def extract_skills_with_score(self, probable_skills):
        skill_with_score = {}
        for skill in probable_skills:
            if skill not in skill_with_score:
                remain = probable_skills.copy()
                remain.remove(skill)
                skill_with_score[skill.capitalize()] = self.get_skill_score(skill, remain)
        return skill_with_score
