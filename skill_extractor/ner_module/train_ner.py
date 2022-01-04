import os
import spacy
from spacy.util import minibatch, compounding
from nerdataprepare import NERData


class NERModel:
    def __init__(self, datafile, lang='en'):
        if os.path.exists(datafile):
            self.nlp = spacy.blank(lang)
            self.filename = datafile
            self.data_obj = NERData(filename=self.filename)
            self.epochs = 20
        else:
            raise "{} file not exist!".format(datafile)

    def get_epochs(self):
        return self.epochs

    def get_filename(self):
        return self.filename

    def get_data(self):
        return self.data_obj

    def set_epochs(self, epochs):
        self.epochs = epochs

    def set_filename_data(self, filename):
        if os.path.exists(filename):
            self.filename = filename
            self.data_obj = NERData(filename=self.filename)
        else:
            raise "{} : file not exist!".format(filename)

    def add_labels(self):
        ner = self.nlp.create_pipe("ner")
        self.nlp.add_pipe(ner, last=True)
        ner = self.nlp.get_pipe('ner')
        for _, annotations in self.data_obj.get_training_data():
            for ent in annotations.get("entities"):
                ner.add_label(ent[2])

    def train(self, epochs):
        self.set_epochs(epochs)
        self.add_labels()
        optimizer = self.nlp.begin_training()
        for i in range(self.epochs):
            losses = {}
            batches = minibatch(self.data_obj.get_training_data(),
                                size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                self.nlp.update(texts, annotations,
                                drop=0.01, losses=losses)
            print(f"Losses at iteration {i} - {losses}")

    def save_model(self, model_name='ner_model'):
        self.nlp.to_disk(model_name)


if __name__ == '__main__':
    base_path = os.path.join(os.getcwd(), *('skill_extractor', 'ner_module'))
    datafile_path = os.path.join(base_path, 'skill_label_data.json')
    model = NERModel(datafile=datafile_path)
    print("Model in training model...")
    model.train(epochs=20)
    print("Training Completed!")
    model_path = os.path.join(base_path, 'ner_model')
    model.save_model(model_path)
    print("Saved NER model at path {}.".format(model_path))
