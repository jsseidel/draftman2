all: install

dist-build:
	python3 cxfreeze_setup.py build --build-base build

install: dist-build
	python3 cxfreeze_setup.py install --prefix dist
	sudo mkdir -p /opt/draftman2
	sudo cp -r dist/bin dist/lib /opt/draftman2/.
	sudo cp draftman2.desktop /usr/share/applications/.

uninstall:
	sudo rm -rf /opt/draftman2
	sudo rm -f /usr/share/applications/draftman2.desktop

clean:
	rm -rf ./build ./dist ./*~ './Draftman2 Tutorial.zip' install_files
	(cd docsbuild ; make clean)

