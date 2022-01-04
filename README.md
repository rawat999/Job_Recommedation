# Job_Recommendation
NLP Based

Follow steps:
1. Clone this repo `git clone https://github.com/rawat999/Job_Recommedation.git` and change your directory into `Job_Recommedation`
2. Install dependencies using `pip install -r requirements`
3. Download [word2vec embedding zip file](https://drive.google.com/file/d/1-ErHC82lNt35KpyiUjRsq_4tgKbzGA2r/view?usp=sharing) and extract zip file into `skill_extractor/word2vec_module/` folder.
4. Train Doc2Vec module using command: `python .\doc2vec\traind2v.py`
5. Then Train NER Module (Name Entity Recognition) using following command: `python .\skill_extractor\ner_module\train_ner.py`

Now, ready to go...
run command: `python .\main.py`

Now we can change resume file `.pdf` or Job Discription file `d2vtrain.csv`

Ongoing Project...
