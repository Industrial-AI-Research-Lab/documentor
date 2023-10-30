#FROM base-jlab-nlp
#ARG IMAGE=node2.bdcl:5000/base-jlab-nlp
ARG IMAGE
FROM $IMAGE

ARG JUSER_ID
ARG JUSER
RUN echo ${JUSER}' ALL=(ALL:ALL) NOPASSWD: ALL' | EDITOR='tee -a' visudo

COPY setup-user.sh setup-user.sh
COPY supervisord.conf.j2 supervisord.conf.j2
RUN chmod 755 setup-user.sh && ./setup-user.sh && chown ${JUSER}:${JUSER} /home/jovyan

ENV NB_PREFIX /

ENV STORAGE /mnt/ess_storage/DN_1/storage/home/${JUSER}/

#jupyter
EXPOSE 8888
#supervisord
EXPOSE 9001

CMD /usr/bin/supervisord
