FROM django:python2
COPY . /
RUN pip install -U setuptools
RUN pip install -r requirements.txt
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
