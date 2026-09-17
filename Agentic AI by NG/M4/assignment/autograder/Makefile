.PHONY: learner build entry submit-solution upgrade test grade mem zip clean upload move-zip move-learner tag undeletable uneditable versioning upgrade sync

include .conf

PARTIDS = ""
OS := $(shell uname)

sync:
    cp mount/submission.ipynb ../$(ASSIGNMENT_NAME)_Solution.ipynb
    cp learner/$(ASSIGNMENT_NAME).ipynb ../$(ASSIGNMENT_NAME).ipynb
    cp mount/unittests.py ../unittests.py

learner:
    dlai_grader --learner --output_notebook=./learner/$(ASSIGNMENT_NAME).ipynb

build:
    docker build -t $(IMAGE_NAME):$(TAG_ID) .

debug:
    docker run -it --rm --mount type=bind,source=$(PWD)/mount,target=/shared/submission --mount type=bind,source=$(PWD),target=/grader/ --entrypoint ash $(IMAGE_NAME):$(TAG_ID)

submit-solution:
    cp solution/solution.ipynb mount/submission.ipynb

versioning:
    dlai_grader --versioning

tag:
    dlai_grader --tag

undeletable:
    dlai_grader --undeletable

uneditable:
    dlai_grader --uneditable

upgrade:
    dlai_grader --upgrade

test:
    docker run -it --rm --mount type=bind,source=$(PWD)/mount,target=/shared/submission --mount type=bind,source=$(PWD),target=/grader/ --entrypoint pytest $(IMAGE_NAME):$(TAG_ID)

grade:
    dlai_grader --grade --partids=$(PARTIDS) --docker=$(IMAGE_NAME):$(TAG_ID) --memory=$(MEMORY_LIMIT) --submission=$(SUB_DIR)

mem:
    memthis $(PARTIDS)

zip:
    zip -r $(IMAGE_NAME)$(TAG_ID).zip .

clean:
    find . -maxdepth 1 -type f -name "*.zip" -exec rm {} +
    docker rm $$(docker ps -qa --no-trunc --filter "status=exited")
    docker rmi $$(docker images --filter "dangling=true" -q --no-trunc)

upload:
    coursera_autograder --timeout 1800 upload --grader-memory-limit $(MEMORY_LIMIT) --grading-timeout 1800 $(IMAGE_NAME)$(TAG_ID).zip $(COURSE_ID) $(ITEM_ID) $(PART_ID)

