FROM python:rc-slim
ADD ./main_api.py /api_python/
WORKDIR /api_python
ENV FLASK_APP=main_api.py
ENV FLASK_ENV=development
RUN pip install kubernetes flask
ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--with-threads", "--no-reload", "--no-debugger"]
