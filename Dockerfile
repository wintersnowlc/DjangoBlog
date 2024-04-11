FROM python:slim

# 名称
LABEL name="DjangoBlog"

ENV SECRET_KEY="django-insecure-vg@q7iy76q!43r2lt3%(ce=i6207gypwffjgp_wi=^8g7*txjo"

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    python manage.py collectstatic --noinput

EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "DjangoBlog.wsgi:application", "--bind", "0.0.0.0:8000"]
