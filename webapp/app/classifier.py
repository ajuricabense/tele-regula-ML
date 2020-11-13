# -*- coding: utf-8 -*-
import logging
from pprint import pprint

import joblib
import pandas as pd

import nltk
import unidecode
import unicodedata

import tensorflow as tf
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model

from nltk.tokenize import RegexpTokenizer
from nltk.stem import RSLPStemmer

logformat='%(asctime)s:%(levelname)s:%(message)s'
logging.basicConfig(filename='./logs/app.log', format=logformat, level=logging.DEBUG)


def preprocessor5(text):
    """Recebe um texto e o retorna preprocessado"""
    from nltk.corpus import stopwords
    
    tokenizer = RegexpTokenizer(r'\w+')
    stopwords = stopwords.words('portuguese')
    stemmer = RSLPStemmer()
    
    no_accents_text = unidecode.unidecode(text)
    no_control_text = "".join(ch for ch in no_accents_text if unicodedata.category(ch)[0]!="C")
    
    words = tokenizer.tokenize(no_control_text)
    words = [w.lower() for w in words]    
    words = [w for w in words if w.isalpha() and w not in stopwords]
    words = [stemmer.stem(w) for w in words] 
    words = [w for w in words if len(w) > 1]
    
    text = " ".join(words)
    
    return text


def pad_text(X_test, tokenizer_path="tokenizer/tokenizer.pkl.z"):
  # tamanho máximo dos textos usados na fase de treinamento do modelo
  max_length = 223
  tokenizer_obj = joblib.load(tokenizer_path)
  test_sequences = tokenizer_obj.texts_to_sequences(X_test)
  X_test_pad = pad_sequences(test_sequences, maxlen=max_length)
  return X_test_pad

def preprocess(texts):
  preprocessed = [ preprocessor5(t) for t in texts ]
  X_test_pad = pad_text(preprocessed)
  return X_test_pad


def classify(solicitacaoid, texts):
  logging.debug("Iniciando pré-processamento dos textos")
  X_test = preprocess(texts)
  logging.debug("Concluído o pré-processamento dos textos")

  logging.debug("Iniciando a carga do modelo")
  model = load_model("weights/model.hdf5")
  logging.debug("Concluída a carga do modelo")

  logging.debug("Iniciando a predição dos casos")
  y_pred = model.predict_proba(X_test) # probabilidade de ser "S"
  logging.debug("Concluída a predição dos casos")

  # Estimar decisao  
  y_pred_df = pd.DataFrame(y_pred, columns=['PROBABILIDADE'])
  y_pred_df.loc[y_pred_df.PROBABILIDADE<=0.4, "DECISAO"] = "Solicitação não autorizada. Possíveis motivos: ausência de critério para encaminhamento, dados clínicos incompletos ou indicação de urgência/emergência (não eletivo). Para complementação de dados ou na suspeita de erro de classificação trocar para 'Aguarda reavaliação' e justificar. Casos em atendimento na APS podem ser qualificados pelo 0800 644 6543. Protocolos de encaminhamento disponíveis em https://www.ufrgs.br/telessauders/regulasus/"
  y_pred_df.loc[y_pred_df.PROBABILIDADE>=0.7, "DECISAO"] = "Solicitação avaliada por algoritmo de Machine Learning, com sugestão para autorização. Necessária qualificação adicional quanto a nível de complexidade e prioridade. "
  y_pred_df["DECISAO"] = y_pred_df.DECISAO.fillna("SEM DECISAO")
  y_pred_df["SOLICITACAOID"] = solicitacaoid
  y_pred_df = y_pred_df[["SOLICITACAOID", "PROBABILIDADE", "DECISAO"]]
  y_pred_df["DATA"] = pd.to_datetime('now').strftime('%Y-%m-%d-%H:%M:%S')
  y_pred_df["ASSINATURA"] ="tele-reg-1.0"

  print(y_pred_df)
  y_pred_df = y_pred_df.to_dict(orient='records')
  print(y_pred_df)
  return y_pred_df


if __name__ == "__main__":

  data_df = joblib.load("data/test_dataset_out_etapa1.pkl.z")
  logging.debug("DataFrame de exemplos carregado")

  texts = data_df["QUADROCLINICO"].values
  logging.debug("%s exemplos de texto" % len(texts))

  preds = classify(texts)

  pprint(preds)
  logging.debug("Terminado")
