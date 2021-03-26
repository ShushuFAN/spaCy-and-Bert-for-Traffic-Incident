# spaCy-and-Bert-for-Traffic-Incident
This repository is for storing the code for the papaer named "Delineating Infrastructure Failure Interdependencies"
## data source
The orignal dataset is collected from the Transport Department of the HKSAR Gevernment. 
1. The download link of 1st generation of traffic news is https://data.gov.hk/en-data/dataset/hk-td-tis_1-special-traffic-news. 
2. The download link of 2nd generation traffic news is https://data.gov.hk/en-data/dataset/hk-td-tis_19-special-traffic-news-v2/resource/9e765b13-4640-443d-a573-daa39242a1c5.
3. The information of road network is acquired from https://data.gov.hk/en-data/dataset/hk-td-tis_15-road-network-v2.
4. The information of public transport is acquired from https://data.gov.hk/en-data/dataset/hk-td-tis_14-routes-fares-xml.
## data preparation
1. The original XML files of traffic news from 2016 to 2020 are stored in folder "data preparation/original dataset". 
2. The information of roads, bus, ferry, subway and tram composes the special corpus, stored in the folder "data preparation/special corpus".
3. Run the pythons files "xml2csv_1st.py", "xml2csv_2nd.py", "tn_1st_dump.py" and "tn_2nd_dump.py" by sequence to generate the redundant datasets "df_1st.csv" and "df_2nd.csv".
## rule-based annotation
spaCy is a free, open-source library for advanced Natural Language Processing (NLP) in Python (https://spacy.io/). Please install the packaged first. For Windows sytem, you can install spaCy by pip as follows:
```
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
```
1. The spaCy model is trained and updated based on the initial model "en_core_web_sm" according to the special corps and syntactic requirements. The models are stored in the folder "spaCy/models".
2. Run the python file "spaCy_parse.py" to label the text of traffic news. 
3. The generated Json files "parse_1st.json" and "parse_2nd.json" are examined by ten experts and the revised files "parse_1st_revise.json" and "parse_2nd_revise.json" are stored in the folder "BERT/spo generation"
## model training and testing
The training model is designed on the basis of [BERT](https://arxiv.org/abs/1810.04805) developed by Google and tailored accordingto the special corpus in order to transfer the unstructured text into RDF triples.  Firstly, we use a classification model to determine the types of predicated involved in sentences. Then for each identified predicate, a labelling model is designed to annotate the entites of the corresponding objects and subjects. Finnally, the RDF triples (predicate, subject, object) are generated. The training environment is as follows:
+ python 3.6+
+ Tensorflow 1.12.0+
+ Dowload [bert-base-uncased](https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-24_H-1024_A-16.zip), unzip file and put it in the folder "BERT/pretained_model"
### training dataset
Run the python file "spo_generation.py" in the folder "BERT/spo generation" to generate the RDF triples according to the latent relationships of the labels and these triples are extamined by ten experts. The revised data are saved as "RDF_triples.json" in the same folder for division. The training dataset (70%) is the file "train_data.json" and testing dataset (30%) is "test_data.json" in the folder "BERT/raw_data".
### training phase
1. prepare data for classification training
  ```
  python bin/predicate_classifiction/predicate_data_manager.py
  ```
2. training for classification model
  ```
  python run_predicate_classification.py ^--task_name=TN_Label ^--do_train=true^ --do_eval=false ^--data_dir=./bin/predicate_classifiction/classification_data ^--vocab_file=./pretrained_model/bert-base-uncased/vocab.txt ^--bert_config_file=./pretrained_model/bert-base-uncased/bert_config.json ^--init_checkpoint=./pretrained_model/bert-base-uncased/bert_model.ckpt ^--max_seq_length=128 ^--train_batch_size=32 ^--learning_rate=2e-5 ^--num_train_epochs=6.0 ^--output_dir=/tmp/my-try/predicate_classification_model/epochs6/
```
3. prepare data for labelling model
  ```
  python bin/subject_object_labeling/sequence_labeling_data_manager.py
  ```
4. training for labelling model
  ```
  python run_sequnce_labeling.py ^--task_name=TN_Label ^--do_train=true ^--do_eval=false ^--data_dir=./bin/subject_object_labeling/sequence_labeling_data ^--vocab_file=./pretrained_model/bert-base-uncased/vocab.txt ^--bert_config_file=./pretrained_model/bert-base-uncased/bert_config.json ^--init_checkpoint=./pretrained_model/bert-base-uncased/bert_model.ckpt ^--max_seq_length=128 ^--train_batch_size=32 ^--learning_rate=2e-5 ^--num_train_epochs=9.0 ^--output_dir=/tmp/my-try/sequnce_labeling_model/epochs9/
```
### testing phase
1. use the classification model to identify the predicate
  ```
  python run_predicate_classification.py ^  --task_name=TN_Label ^  --do_predict=true ^  --data_dir=./bin/predicate_classifiction/classification_data ^  --vocab_file=./pretrained_model/bert-base-uncased/vocab.txt ^  --bert_config_file=./pretrained_model/bert-base-uncased/bert_config.json ^  --init_checkpoint=/tmp/my-try/predicate_classification_model/epochs6/model.ckpt-1160 ^  --max_seq_length=128 ^  --output_dir=/tmp/my-try/predicate_infer_out/epochs6/ckpt1160
  ```
2. transfer the classification results to input data of labelling model
  ```
  python bin/predicate_classifiction/prepare_data_for_labeling_infer.py
  ```
3. use the labelling model to identify entities
  ```
  python run_sequnce_labeling.py ^  --task_name=TN_Label ^  --do_predict=true ^  --data_dir=./bin/subject_object_labeling/sequence_labeling_data ^  --vocab_file=./pretrained_model/bert-base-uncased/vocab.txt ^  --bert_config_file=./pretrained_model/bert-base-uncased/bert_config.json ^  --init_checkpoint=/tmp/my-try/sequnce_labeling_model/epochs9/model.ckpt-4482 ^  --max_seq_length=128 ^  --output_dir=/tmp/my-try/sequnce_infer_out/epochs9/ckpt4482
  ```
4. generate RDF triples
  ```
  python produce_submit_json_file.py
  ```
### evalutation phase
run "evaluate_classifiction.py" and "evaluate_labeling.py" in the folder "BERT/bin/evaluation"
|分类模型|序列标注模型|准确率|召回率|F1值|
|-|-|-|-|-|
|epochs6ckpt1000|epochs9ckpt4000|0.9549|0.8028|0.8214|
|epochs6ckpt13000|epochs9ckpt10000|0.9694|0.8188|0.8169|
|epochs6ckpt20000|epochs9ckpt17000|0.9651|0.838|0.8365|
|epochs6ckpt23000|epochs9ckpt20000|0.9714|0.8289|0.8238|
