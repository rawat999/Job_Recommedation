import os
from skill_extractor.ner_module import NERExtractSkills
from skill_extractor.pos_module import POSExtractSkills
from skill_extractor.skills_dictionary import DictExtractSkills
from skill_extractor.word2vec_module import W2VExtractSkills
from skill_extractor.utility import *

# NER MODEL
model_path = os.path.join(os.getcwd(), *('skill_extractor', 'ner_module', 'ner_model'))

# SKILL DICTIONARY
skill_dictionary = os.path.join(os.getcwd(), *('skill_extractor', 'skills_dictionary', 'base_skills.csv'))

# WORD2VEC MODEL
w2v_path = os.path.join(os.getcwd(), *('skill_extractor', 'word2vec_module',
                                       'word2vec100D', 'word2vec.wordvectors'))


class ExtractFinalSkills(object):
    def __init__(self, threshold=4.0):
        self.threshold = threshold
        self.ner = NERExtractSkills(model=model_path)
        self.pos = POSExtractSkills()
        self.skill_dict = DictExtractSkills(skilldictfile=skill_dictionary)
        self.word2vec = W2VExtractSkills(wordvectorfile=w2v_path)

    def filter_dict_by_value(self, sorted_dictionary):
        filtered = {}
        for i, j in sorted_dictionary.items():
            if j > self.threshold:
                filtered[i] = j
            else:
                break
        return filtered

    def extract_skills(self, text):
        SA = self.ner.extract_skills(text)
        SP = self.pos.extract_skills(text)
        SD = self.skill_dict.extract_skills(text)
        probable_skills = SA.union(SP.union(SD))
        probable_skills_list = [str(i).lower() for i in probable_skills]
        w2v_score = self.word2vec.extract_skills_with_score(probable_skills_list)
        extracted_skills = score_each_skills(ner_skills=SA, pos_skills=SP, sd_skills=SD, w2v_score_dict=w2v_score)
        final_skills = self.filter_dict_by_value(extracted_skills)
        return final_skills

"""
test = "Abhishek Jha\nApplication Development Associate - Accenture\n\nBengaluru, Karnataka - Email me on Indeed:" \
       " indeed.com/r/Abhishek-Jha/10e7a8cb732bc43a\n\n\u2022 To work for an organization which provides me the " \
       "opportunity to improve my skills\nand knowledge for my individual and company's growth in best possible ways." \
       "\n\nWilling to relocate to: Bangalore, Karnataka\n\nWORK EXPERIENCE\n\nApplication Development " \
       "Associate\n\nAccenture -\n\nNovember 2017 to Present\n\nRole: Currently working on Chat-bot. Developing " \
       "Backend Oracle PeopleSoft Queries\nfor the Bot which will be triggered based on given input. Also, Training" \
       " the bot for different possible\nutterances (Both positive and negative), which will be given as\ninput by " \
       "the user.\n\nEDUCATION\n\nB.E in Information science and engineering\n\nB.v.b college of engineering and " \
       "technology -  Hubli, Karnataka\n\nAugust 2013 to June 2017\n\n12th in Mathematics\n\nWoodbine modern " \
       "school\n\nApril 2011 to March 2013\n\n10th\n\nKendriya Vidyalaya\n\nApril 2001 to March 2011\n\nSKILLS\n\nC " \
       "(Less than 1 year), Database (Less than 1 year), Database Management (Less than 1 year),\nDatabase Management " \
       "System (Less than 1 year), Java (Less than 1 year)\n\nADDITIONAL INFORMATION\n\nTechnical " \
       "Skills\n\nhttps://www.indeed.com/r/Abhishek-Jha/10e7a8cb732bc43a?isid=rex-download&ikw=" \
       "download-top&co=IN\n\n\n\u2022 Programming language: C, C++, Java\n\u2022 Oracle PeopleSoft\n\u2022 Internet " \
       "Of Things\n\u2022 Machine Learning\n\u2022 Database Management System\n\u2022 Computer Networks\n\u2022 "

obj = ExtractFinalSkills()
print(obj.extract_skills(test))"""
