all:
	docker run --rm -v '$(shell pwd)':/project jsseidel/mktechdocs
	cp -r usage_guide_pages/* ../docs/.

clean:
	docker run --rm -v '$(shell pwd)':/project jsseidel/mktechdocs clean
