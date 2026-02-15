FROM python:3.13
WORKDIR /langgraph_frontend
COPY . /langgraph_frontend
RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit","run","langgraph_frontend.py"]
