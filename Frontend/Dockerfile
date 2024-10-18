FROM python

WORKDIR /app
COPY ./Frontend /app
RUN git clone https://github.com/Kiana-Jahanshid/PyDentify--python-identity-verification.git .
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
COPY . . 
ENTRYPOINT [ "streamlit" , "run" , "app.py" , "--server.port=8501", "--server.address=0.0.0.0" ]


# or 
# WORKDIR /app
# COPY ./Frontend /app
# RUN pip install --no-cache-dir -r requirements.txt
# CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]