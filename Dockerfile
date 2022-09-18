# ベース・イメージ を設定
FROM python:3.10.7-alpine

ARG project_dir=/projects/
WORKDIR /projects

RUN pip install flask
RUN pip install requests