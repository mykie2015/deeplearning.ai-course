FROM continuumio/miniconda3@sha256:d601a04ea48fd45e60808c7072243d33703d29434d2067816b7f26b0705d889a

RUN apk update && apk add libstdc++

COPY requirements.txt .

RUN pip install -r requirements.txt &&     rm requirements.txt

RUN mkdir /grader && \ 
mkdir /grader/submission

COPY .conf /grader/.conf
COPY entry.py /grader/entry.py
COPY grader.py /grader/grader.py
COPY mount/research_tools.py /grader/research_tools.py
COPY mount/unittests.py /grader/unittests.py


RUN chmod a+rwx /grader/


WORKDIR /grader/

ENTRYPOINT ["python", "entry.py"]
