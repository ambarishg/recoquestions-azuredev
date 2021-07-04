FROM python:3.8-slim-buster
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python3 -m spacy download en_core_web_lg
EXPOSE 8501
ENTRYPOINT ["streamlit","run"]
CMD ["reco.py"]