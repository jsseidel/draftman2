all:
	docker run --rm -v '$(shell pwd)':/project --user $(shell id -u):$(shell id -g) jsseidel/mktechdocs
	cp -r usage_guide_pages/* ../docs/.

clean:
	docker run --rm -v '$(shell pwd)':/project jsseidel/mktechdocs clean
	rm -rf usage_guide_pages
