VERSION = $(shell cat VERSION)

all: install

dist-build:
	python3 cxfreeze_setup.py build --build-base build

tgz: dist-build
	mkdir -p draftman2_2.0.0_amd_linux
	cp -r build/exe.linux-x86_64-3.6/* draftman2_2.0.0_amd_linux/.
	tar cfz draftman2_2.0.0_amd_linux.tar.gz draftman2_2.0.0_amd_linux
	rm -rf ./draftman2_2.0.0_amd_linux

install: dist-build
	python3 cxfreeze_setup.py install --prefix dist

uninstall:
	sudo rm -rf /opt/draftman2
	sudo rm -f /usr/share/applications/draftman2.desktop

clean:
	rm -rf ./build ./dist ./*~ './Draftman2 Tutorial.zip'
	(cd docsbuild ; make clean)

really-clean: clean
	rm -rf install_files ./draftman2_2.0.0_amd_linux.tar.gz

