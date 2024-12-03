uplocal:
	flask --app app.app run -p 8080 --debug

test:
	docker exec -t blog-api pytest -s -v

cov:
	docker exec -t blog-api pytest -s -v --cov

up:
	docker compose --env-file ./secrets/.env up --build -d

down:
	docker compose --env-file ./secrets/.env down

logs:
	docker logs --follow blog-api

fake:
	docker exec -t blog-api python3 fill_db.py