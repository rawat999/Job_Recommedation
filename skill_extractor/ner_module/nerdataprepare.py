import os
import json


class NERData:
    def __init__(self, filename):
        if os.path.exists(filename):
            self.file = filename
        else:
            raise "File {} is not exist!".format(filename)

    def read_data(self):
        with open(self.file, "r") as f:
            x = json.load(f)
        return x

    def get_training_data(self):
        data = self.read_data()
        dataset = []
        for content, labels in tuple(zip(data['content'], data['label'])):
            lab = {'entities': []}
            for ents in labels['entities']:
                lab['entities'].append((ents[0], ents[1], ents[2]))
            dataset.append((content, lab))
        return dataset
