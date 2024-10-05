

build_image:
	docker build -t marketing-bot .


build_image_dev:
	docker build -t marketing-bot-dev .

run_mypy:
	docker run -it -v ./:/opt marketing-bot-dev mypy .

run_ruff:
	docker run -it -v ./:/opt marketing-bot-dev ruff check src/



run_service:
	docker run \
	  -d \
	  -e TOKEN="TODO: ADD .env file" \
	  --restart="unless-stopped" \
	  --name=marketing-bot \
	  marketing-bot

stop_service:
	docker rm -f marketing-bot


restart_service: stop_service run_service