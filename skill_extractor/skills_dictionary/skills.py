import os
import re
import csv


class BaseDictSkills(object):
    def __init__(self, filename="base_skills.csv"):
        if os.path.exists(filename):
            self.file = filename
            self.skills = self.read_skills()
        else:
            raise "{} file not exist!".format(filename)

    def getfilename(self):
        return self.file

    def setfilename(self, filename):
        if os.path.exists(filename):
            self.file = filename
        else:
            raise "{} file not exist!".format(filename)

    def get_skills(self):
        return self.skills

    def set_skills(self, skills=None):
        if skills is None:
            skills = list()
        self.skills = list(set(skills))

    def update_skills(self, new_skills):
        self.skills.extend(new_skills)
        self.skills = list(set(self.skills))

    def read_skills(self):
        with open(self.file, 'r') as f:
            data = csv.reader(f)
            values = []
            for value in data:
                values.extend(value)
        return list(set(values))

    def write_skills_into_file(self):
        with open(self.file, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(set(self.skills))
            file.close()


class DictExtractSkills(object):
    def __init__(self, skilldictfile=None):
        if skilldictfile is None:
            self.skill_obj = BaseDictSkills()
        else:
            self.skill_obj = BaseDictSkills(filename=skilldictfile)

    def extract_skills(self, text):
        skills = self.skill_obj.get_skills()
        extracted_skills = []
        for skill in skills:
            try:
                if len(re.findall(r'\b{}\b'.format(str(skill)), str(text), flags=re.IGNORECASE)) > 0:
                    extracted_skills.append(skill)
                else:
                    continue
            except re.error:
                continue
        return set([i.capitalize() for i in extracted_skills])


"""d_obj = DictExtractSkills()
text = "Abhishek Jha\nApplication Development Associate - Accenture\n\nBengaluru, Karnataka - Email me on Indeed:" \
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

# d_obj.extract_skills(text)
print(text)
print(d_obj.extract_skills(text))"""
