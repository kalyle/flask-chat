
FROM python:3.8

ENV TIME_ZONE Asia/Shanghai
ENV PIPURL "https://pypi.tuna.tsinghua.edu.cn/simple"

# ???
RUN echo "${TIME_ZONE}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime

COPY . /home/backend
WORKDIR /home/backend
    
RUN pip --no-cache-dir install  -i ${PIPURL} --upgrade pip \
    && pip --no-cache-dir install  -i ${PIPURL} -r requirements.txt


CMD ./start.sh