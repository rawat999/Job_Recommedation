import spacy
import re


class POSExtractSkills(object):
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.url_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)"\
                           "(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|"\
                           "(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

    @staticmethod
    def remove_punctuations(text):
        return re.sub(r'[^\w\s]', ' ', text)

    def remove_urls(self, text):
        return re.sub(self.url_pattern, ' ', text)

    @staticmethod
    def remove_numbers_alphanumeirc(text):
        text = re.sub('[0-9]+', ' ', str(text))
        text = re.sub(r'\W+', ' ', str(text))
        return text

    def extract_skills(self, text):
        text = self.remove_urls(text)
        text = self.remove_numbers_alphanumeirc(text)
        nlp_text = self.nlp(text)
        skillset = [token.text for token in nlp_text if (not token.is_stop) and (len(token) > 1)]
        for token in nlp_text.noun_chunks:
            token = token.text.lower().strip()
            if token not in skillset:
                skillset.append(token)
        return set([i.capitalize() for i in set(skillset)])


"""
tex = "Abhishek Jha\nApplication Development Associate - Accenture\n\nBengaluru, Karnataka - Email me on Indeed:" \
      " indeed.com/r/Abhishek-Jha/10e7a8cb732bc43a\n\n\u2022 To work for an organization which provides me the "\
      "opportunity to improve my skills\nand knowledge for my individual and company's growth in best possible ways."\
      "\n\nWilling to relocate to: Bangalore, Karnataka\n\nWORK EXPERIENCE\n\nApplication Development "\
      "Associate\n\nAccenture -\n\nNovember 2017 to Present\n\nRole: Currently working on Chat-bot. Developing "\
      "Backend Oracle PeopleSoft Queries\nfor the Bot which will be triggered based on given input. Also, Training"\
      " the bot for different possible\nutterances (Both positive and negative), which will be given as\ninput by "\
      "the user.\n\nEDUCATION\n\nB.E in Information science and engineering\n\nB.v.b college of engineering and "\
      "technology -  Hubli, Karnataka\n\nAugust 2013 to June 2017\n\n12th in Mathematics\n\nWoodbine modern "\
      "school\n\nApril 2011 to March 2013\n\n10th\n\nKendriya Vidyalaya\n\nApril 2001 to March 2011\n\nSKILLS\n\nC "\
      "(Less than 1 year), Database (Less than 1 year), Database Management (Less than 1 year),\nDatabase Management "\
      "System (Less than 1 year), Java (Less than 1 year)\n\nADDITIONAL INFORMATION\n\nTechnical "\
      "Skills\n\nhttps://www.indeed.com/r/Abhishek-Jha/10e7a8cb732bc43a?isid=rex-download&ikw="\
      "download-top&co=IN\n\n\n\u2022 Programming language: C, C++, Java\n\u2022 Oracle PeopleSoft\n\u2022 Internet "\
      "Of Things\n\u2022 Machine Learning\n\u2022 Database Management System\n\u2022 Computer Networks\n\u2022 "
pos = POSExtractSkills()
print(pos.extract_skills(tex))
"""