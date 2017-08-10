FROM django:python2
ADD . /talionario
WORKDIR /talionario
RUN pip install -r requirements.txt
RUN ["chmod", "+x", "/talionario/entrypoint.sh"]
ENTRYPOINT /talionario/entrypoint.sh
