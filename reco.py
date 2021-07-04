import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns
import re
import spacy
from spacy.cli.download import download as spacy_download
import string
import pickle
from sklearn.metrics.pairwise import cosine_similarity

st.title("Question and answer recommendation system")

def clean_text(text):
    '''Make text lowercase,remove punctuation
    '''
    text = text.strip()
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\[', '', text)
    text = re.sub('\]', '', text)
    return text


user_input = st.text_area("Your Question",
"I want to be a Data Scientist.What should I study?")

method_eval = st.radio("Strategy",options =["TFIDF",
"Word Embeddings using spacy"])

result = st.button("Make recommendations")

def get_result_tfidf(user_input):

    with open('tfidf_vectorizer.pkl', 'rb') as f:
        tfidf_vectorizer2 = pickle.load(f)
    with open('q_tfidf.pkl', 'rb') as f:
        q_tfidf2 = pickle.load(f)
    
    user_input = user_input.strip()
    question_asked = [user_input]
    q_new_tfidf = tfidf_vectorizer2.transform(question_asked)

    result = cosine_similarity(q_new_tfidf,q_tfidf2)
    
    questions =  pd.read_csv("questions.csv")
    professionals = pd.read_csv("professionals.csv")
    answers = pd.read_csv("answers.csv")

    prof_ans = pd.merge(professionals, answers, how = 'left' ,
                    left_on = 'professionals_id', right_on = 'answers_author_id')
    prof_ans_q = pd.merge(prof_ans, questions, how = 'left' ,
                      left_on = 'answers_question_id', right_on = 'questions_id')


    prof_ans_q = prof_ans_q[(~prof_ans_q["questions_title"].isna()) | (~prof_ans_q["questions_body"].isna()) ]

    for i in range(9,0,-1):
        st.markdown(prof_ans_q.iloc[np.argsort(result)[:,-10:][0][i]]["answers_body"],
        unsafe_allow_html=True)
        st.markdown("<hr/>",unsafe_allow_html=True)


def get_result_spacy(user_input):
    with open('spacy_questions.pkl', 'rb') as f:
        spacy_questions = pickle.load(f)
    
    user_input = user_input.strip()
    
    
    nlp = spacy.load('en_core_web_lg')
    with nlp.disable_pipes():
        questions_user = [nlp(user_input).vector]

    result = cosine_similarity(questions_user,spacy_questions)
    
    questions =  pd.read_csv("questions.csv")
    professionals = pd.read_csv("professionals.csv")
    answers = pd.read_csv("answers.csv")

    prof_ans = pd.merge(professionals, answers, how = 'left' ,
                    left_on = 'professionals_id', right_on = 'answers_author_id')
    prof_ans_q = pd.merge(prof_ans, questions, how = 'left' ,
                      left_on = 'answers_question_id', right_on = 'questions_id')


    prof_ans_q = prof_ans_q[(~prof_ans_q["questions_title"].isna()) | (~prof_ans_q["questions_body"].isna()) ]

    for i in range(9,0,-1):
        st.markdown(prof_ans_q.iloc[np.argsort(result)[:,-10:][0][i]]["answers_body"],
        unsafe_allow_html=True)
        st.markdown("<hr/>",unsafe_allow_html=True)

if result:
    if method_eval == "TFIDF":
        get_result_tfidf(user_input)
    else:
        get_result_spacy(user_input)

    


