
dist-build:
	python3 cxfreeze_setup.py build --build-base build

install: dist-build
	python3 cxfreeze_setup.py install --root dist

clean:
	rm -rf ./build ./dist ./*~ './Draftman2 Tutorial.zip'

