# Jeeves build image
FROM python:3.9

MAINTAINER Ole Chr. Astrup "tanumkroken@astrup.info#"

WORKDIR /app

# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
COPY requirements.txt /app/.
RUN pip install -r requirements.txt

# Now copy in our code, and run it
COPY . /app

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]