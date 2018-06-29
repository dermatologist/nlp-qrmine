FROM python:3

ENV PYTHONPATH /qrmine
WORKDIR ${PYTHONPATH}
ADD . $PYTHONPATH
RUN pip install -r requirements.txt

CMD [ "python", "qrmine/gtdict.py docs/transcript.txt" ]
