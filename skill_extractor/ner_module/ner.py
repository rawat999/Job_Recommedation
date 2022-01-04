import os
import spacy


class NERExtractSkills:
    def __init__(self, model):
        if os.path.exists(model):
            self.model_name = model
            self.nlp = spacy.load(model)
        else:
            print("{} file not exist!".format(model))

    def extract_skills(self, text):
        document = self.nlp(text)
        return set(document.ents)


"""def main():
    # model = NERModel(datafile="skill_label_data.json")
    # model.train(epochs=40)
    # model.save_model()
    module1 = NERBasedSkills(model='ner_model')
    data_module = NERData(filename="skill_label_data.json")
    text = data_module.get_training_data()
    print(module1.get_skills(text[0][0]))


main()"""
