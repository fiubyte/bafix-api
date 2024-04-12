## users API 1.0.0
## 

#set DB_PASSWORD to the password of the database


.PHONY: clean test run-local

help:        ## Show this help.
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)


run-local:   ## Run locally
	python -m uvicorn app.main:app --port 80 --reload --env-file .env

build: clean ## Build the docker image
	docker build --tag 'bafix-api' .

run: build   ## Run the docker image (and build)
	docker run -p 80:80 -e DB_PASSWORD=$(DB_PASSWORD) bafix-api

clean:       ## Remove image 
	docker image rm -f bafix-api