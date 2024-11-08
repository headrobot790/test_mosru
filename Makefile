DC_NAME = mosru
DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
STORAGES_FILE = docker_compose/storage.yaml
APP_CONTAINER = main-app


.PHONY: app down app-shell app-logs storage storage-down
app:
	${DC} -p ${DC_NAME} -f ${APP_FILE} ${ENV} up --build -d

down:
	${DC} -p ${DC_NAME} -f ${APP_FILE} ${ENV} down

app-shell:
	${EXEC} ${APP_CONTAINER} bash

app-logs:
	${LOGS} ${APP_CONTAINER} -f

storage:
	${DC} -p ${DC_NAME}db -f ${STORAGES_FILE} ${ENV} up --build -d

storage-down:
	${DC} -p ${DC_NAME}db -f ${STORAGES_FILE} ${ENV} down
