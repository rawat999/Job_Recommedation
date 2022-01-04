import os
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import nltk
from skill_extractor import ExtractFinalSkills
from doc2vec import LoadDoc2VecModel, GetSimilarTopDocs

import fitz

model = ExtractFinalSkills()

path = os.path.join(os.getcwd(), *('doc2vec', 'trained_d2v_model'))
d2v = LoadDoc2VecModel(trained_model=path)
mod = GetSimilarTopDocs(d2v_object=d2v)


def get_document_on_given_idx(corpus, idx):
    return corpus[idx]


def get_explicit_implicit_skills(corpus, similarity_mapping):
    explicit_implicit_skills_per_doc = {}
    for main_doc, similar_docs in similarity_mapping.items():
        if main_doc not in explicit_implicit_skills_per_doc:
            explicit_implicit_skills_per_doc[main_doc] = {}
        main_document = get_document_on_given_idx(corpus, int(main_doc))
        explicit_skills = list(model.extract_skills(main_document[0]).keys())
        explicit_implicit_skills_per_doc[main_doc]['explicit_skills'] = explicit_skills
        implicit_skills = []
        for sim_doc in similar_docs:
            document = get_document_on_given_idx(corpus, int(sim_doc))
            implicit_skills.extend(list(model.extract_skills(document[0]).keys()))
        explicit_implicit_skills_per_doc[main_doc]['implicit_skills'] = set(implicit_skills)
    return explicit_implicit_skills_per_doc


def jobs_similarity_score_with_resume(resume_text, jobs_extracted_skills):
    jobs_score_with_resume = {}
    resume = nltk.word_tokenize((str(resume_text).strip()).lower())
    for job in jobs_extracted_skills.keys():
        all_skills = list(jobs_extracted_skills[job]['explicit_skills']) + \
                     list(jobs_extracted_skills[job]['implicit_skills'])
        concatenated_skills = [str(i).lower() for i in all_skills]
        similarity_score_btw_resume_job = d2v.get_similarity(resume, concatenated_skills)
        jobs_score_with_resume[job] = similarity_score_btw_resume_job
    jobs_score_with_resume = dict(sorted(jobs_score_with_resume.items(), key=lambda item: item[1], reverse=True))
    return jobs_score_with_resume


def read_pdf_into_txt(file):
    doc = fitz.open(file)
    pdf_description = ""
    for i in range(len(doc)):
        pdf_description += str(doc.load_page(i).get_text())
    return pdf_description


def find_top_jobs(job_description_file, resume_file, use_n_records=30):
    resume_text = read_pdf_into_txt(resume_file)
    df = pd.read_csv(job_description_file)
    corpus = df['Description'].apply(lambda x: [x])[:use_n_records]
    similars = mod.get_all_similar_docs(corpus=corpus, topn=3)
    resume_job_scores = get_explicit_implicit_skills(corpus, similars)
    top_jobs = jobs_similarity_score_with_resume(resume_text=resume_text, jobs_extracted_skills=resume_job_scores)
    top = []
    j = 0
    print(top_jobs)
    for job in top_jobs:
        top.append([df.loc[job]["Job ID"], df.loc[job]["Description"], top_jobs[job]])
        j += 1
        if j > 5:
            break
    top_job_df = pd.DataFrame(top, columns=['Job ID', 'Description', 'Similarity Score'])
    return top_job_df


if __name__ == '__main__':
    jobs_file = os.path.join(os.getcwd(), 'd2vtrain.csv')
    resume_file_path = os.path.join(os.getcwd(), 'Prem_R_CV.pdf')
    top_job = find_top_jobs(job_description_file=jobs_file, resume_file=resume_file_path, use_n_records=30)
    print("\nSuccessfully got top jobs!\n")
    print(top_job.head(5))
