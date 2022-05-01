FROM python:3.9-alpine3.14	

WORKDIR server

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt \
    && python3 utils/build_database.py
	
CMD ["python3", "-m", "uvicorn", "--host", "0.0.0.0", "--port", "5000", "server:app"]
