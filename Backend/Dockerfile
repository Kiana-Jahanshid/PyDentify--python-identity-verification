FROM python

WORKDIR /app
COPY ./Backend /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn" , "app:app" , "--host" , "0.0.0.0" , "--port" , "8000"]
# pyfilename:app