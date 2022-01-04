import os
import numpy as np
import pandas as pd
import random
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from prepraredata import preprocess_text, data_profile


# function for building and training model
def build_train_d2v(dataset, column_name, unique_id_col_index, max_epochs=50):
    # Create Document Corpus
    document_corpus = dataset[column_name]
    document_corpus = [TaggedDocument(words=d,
                                      tags=[str(dataset.iloc[i, unique_id_col_index])]) for i, d in
                       enumerate(document_corpus)]
    model = Doc2Vec(vector_size=150, window=3, min_count=1, workers=4)
    # Build Vocabulary
    model.build_vocab(document_corpus)
    # Train Model
    model.train(corpus_iterable=document_corpus, total_examples=model.corpus_count, epochs=max_epochs)
    return model


# Extracting test vectors using doc2vec model
def get_vectors(model, test_dataset, description_col_index):
    test_vector = []
    for i in range(test_dataset.shape[0]):
        v1 = model.infer_vector(test_dataset.iloc[i, description_col_index])
        test_vector.append(v1)
    test_vector_new = pd.DataFrame(test_vector)
    return test_vector_new


# calculate model score on test data
def model_score(model, test_vectors, original_test_data, no_of_records, id_col_name, id_col_index):
    Test_result_df = pd.DataFrame()
    correct_predictions = 0
    for i in range(0, original_test_data.shape[0]):
        query = test_vectors.iloc[i, ]
        query_new = np.array(query)
        similar_doc = model.dv.most_similar([query_new])
        similar_items_df = pd.DataFrame(similar_doc, columns=[id_col_name, 'doc2vec_score'])
        similar_items_df = similar_items_df.iloc[0:no_of_records]
        similar_items_df['Search_ID'] = original_test_data.iloc[i, id_col_index]
        near_top_ID = similar_items_df[id_col_name]
        test_id = original_test_data.iloc[i, id_col_index]
        if str(test_id) in str(near_top_ID):
            correct_predictions = correct_predictions + 1
        i += 1
        Test_result_df = Test_result_df.append(similar_items_df)
    return round((correct_predictions / original_test_data.index.size) * 100, 2)


# training function
def TrainModelDoc2Vec(d2v_trainingdata, id_col, description_col, epochs=50):
    token_col, token_count_col = "Extracted_Nouns", "Token_Counts"
    data = pd.read_csv(d2v_trainingdata, usecols=[id_col, description_col])

    if data.shape[0] > 0:
        print("Size of Data: {}".format(data.shape))
        result = data_profile(data, desc_col=description_col)
        print(result)

        if (result["blank_percentage"] > 0.0) or (result["null_percentage"]) > 0.0:
            data[description_col].replace('', np.nan, inplace=True)
            data.dropna(subset=[description_col], inplace=True)

        if result["duplicate_percentage"] > 0.0:
            data.drop_duplicates(subset=[description_col], keep='first', inplace=True)

        print("Size of Data: {}".format(data.shape))
        result = data_profile(data, desc_col=description_col)
        print(result)

        print("****** Token creation started ******")
        data[token_col] = data[description_col].apply(preprocess_text)
        data[token_count_col] = data[token_col].apply(lambda x: len(x))
        avg_token_length = int(round(data[token_count_col].mean(), 0))
        print("average_token_length:  \n", avg_token_length)

        print("****** Doc2Vec Model Building and Training ******")
        id_col_idx = data.columns.get_loc(id_col)
        d2v_model = build_train_d2v(dataset=data, column_name=token_col,
                                    unique_id_col_index=id_col_idx,
                                    max_epochs=epochs)
        print("Model has been built and Trained, Successfully!\n")

        print("***** Testing Model *****")
        no_of_test_records = int(round(0.2 * data.shape[0], 0))
        if no_of_test_records > 50:
            total_test_records = no_of_test_records
        else:
            total_test_records = data.shape[0]
        print("Total test record count is : ", total_test_records)

        test_data = (data[0:total_test_records]).copy(deep=True)
        # Shuffling test tokens randomly for checking accuracy:
        test_data[token_col] = test_data[token_col].apply(lambda x: random.sample(x, len(x)))

        description_col_index = test_data.columns.get_loc(token_col)
        id_col_index = test_data.columns.get_loc(id_col)
        test_vectors = get_vectors(model=d2v_model,
                                   test_dataset=test_data,
                                   description_col_index=description_col_index)

        model_accuracy = model_score(model=d2v_model, test_vectors=test_vectors, original_test_data=test_data,
                                     no_of_records=5, id_col_name="id", id_col_index=id_col_index)

        print("Test Accuracy of Model is : {}".format(model_accuracy))
        return d2v_model


if __name__ == '__main__':
    base_path = os.path.join(os.getcwd(), "doc2vec")
    datafile = os.path.join(base_path, "d2vtrain.csv")
    # train the model
    mod = TrainModelDoc2Vec(d2v_trainingdata=datafile,
                            id_col="Job ID", description_col="Description",
                            epochs=100)
    fname = os.path.join(base_path, 'trained_d2v_model')
    mod.save(fname)
    print("Successfully model saved as file name {}".format(fname))
