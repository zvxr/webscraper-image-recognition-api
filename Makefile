.PHONY: clean down logs shell test up


clean:
	@make down
	docker rmi -f wira_app
	docker volume prune -f

down:
	docker-compose -p wira down --remove-orphans

logs:
	docker-compose -p wira logs -f

shell:
	docker exec -it wira_app /bin/bash

test:
	docker exec wira_app 'pytest'

up:
	docker-compose -p wira up -d
