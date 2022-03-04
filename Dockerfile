FROM ubuntu as differy
ENV TZ=US/Mountain
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && apt-get update -y && apt-get install jq -y

FROM differy as mysql-env
RUN apt-get install mysql-server -y

FROM differy as python-env
RUN apt-get install -y python3-pip && pip install pandas datacompy seaborn markdown jinja2
