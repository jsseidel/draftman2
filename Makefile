
dist-build:
	pyinstaller draftman2.spec

install: dist-build
	sudo rm -rf /opt/draftman2 &&\
	sudo cp -r ./dist/draftman2 /opt/. &&\
	sudo cp draftman2.desktop /usr/share/applications/.
	zip -r 'Draftman2 Tutorial.zip' 'Draftman2 Tutorial'

remove:
	sudo rm -rf /opt/draftman2
	sudo rm -f /usr/share/applications/draftman2.desktop

clean:
	rm -rf ./build ./dist ./*~ './Draftman2 Tutorial.zip'
