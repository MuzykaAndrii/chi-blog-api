uplocal:
	flask --app app.app run -p 8080 --debug

up:
	docker compose --env-file ./secrets/.env up --build -d

logs:
	docker logs --follow blog-api