all:

build-image:
	docker build . -t rasp-tank

local-shell:
	docker run -it --rm -p 9090:9090 -v $(pwd)/workspace:/workspace rasp-tank /bin/bash

deploy-image:
	docker save rasp-tank | gzip > /tmp/rasp-tank.tar.gz
	scp /tmp/rasp-tank.tar.gz ubuntu@192.168.1.175:~/

.PHONY: all build-image local-shell deploy-image
