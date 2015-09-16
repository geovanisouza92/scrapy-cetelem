
build:
	docker build -t geovanisouza92/scrapy-cetelem .

run:
	docker run -it --rm --env-file=.env geovanisouza92/scrapy-cetelem
