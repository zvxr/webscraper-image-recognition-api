.PHONY: clean down format lint logs shell test up


clean:
	@make down
	docker rmi -f wira_app
	docker volume prune -f

down:
	docker-compose -p wira down --remove-orphans

format:
	docker exec wira_app sh -c 'isort .'
	docker exec wira_app sh -c 'black .'

lint:
	docker exec wira_app sh -c 'pyflakes .'
	docker exec wira_app sh -c 'isort --check-only .'

logs:
	docker-compose -p wira logs -f

shell:
	docker exec -it wira_app /bin/bash

test:
	docker exec wira_app sh -c 'pytest -v'

up:
	docker-compose -p wira up -d
