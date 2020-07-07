VERSION = $(shell cat VERSION)

all: install

dist-build:
	python3 cxfreeze_setup.py build --build-base build

tgz: dist-build
	mkdir -p draftman2_$(VERSION)_amd_linux
	cp -r build/exe.linux-x86_64-*/* draftman2_$(VERSION)_amd_linux/.
	tar cfz draftman2_$(VERSION)_amd_linux.tar.gz draftman2_$(VERSION)_amd_linux
	rm -rf ./draftman2_$(VERSION)_amd_linux

install: dist-build
	python3 cxfreeze_setup.py install --prefix dist
	rm -rf ./install_files
	mkdir -p ./install_files/opt/draftman2
	mkdir -p ./install_files/usr/share/applications
	cp -r dist/lib/Draftman2-${VERSION}/* ./install_files/opt/draftman2/.
	cp draftman2.desktop ./install_files/usr/share/applications/.

uninstall:
	sudo rm -rf /opt/draftman2
	sudo rm -f /usr/share/applications/draftman2.desktop

clean:
	rm -rf ./build ./dist ./*~ './Draftman2 Tutorial.zip'
	(cd docsbuild ; make clean)

really-clean: clean
	rm -rf install_files ./draftman2_$(VERSION)* ../draftman2_$(VERSION)*

