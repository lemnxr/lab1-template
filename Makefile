run-compose:
	docker-compose up -d

down-compose:
	docker-compose down

delete-all:
	docker rmi postgres:16-alpine && docker rmi rsoi-app && rm -rf data

run-tests:
	pytest -vs app/tests/person.py
