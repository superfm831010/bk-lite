push:
	git add . && codegpt commit . && git push

build-system-manager:
	docker build -t bklite/system-manager-web -f ./support-files/release/system-manager/Dockerfile .

build-console:
	docker build -t bklite/ops-console-web -f ./support-files/release/console/Dockerfile .

build-node-manager:
	docker build -t bklite/node-manager-web -f ./support-files/release/node-manager/Dockerfile .	

build-cmdb:
	docker build -t bklite/cmdb-web -f ./support-files/release/cmdb/Dockerfile .

build-monitor:
	docker build -t bklite/monitor-web -f ./support-files/release/monitor/Dockerfile .

build-opspilot:
	docker build -t bklite/ops-pilot-web -f ./support-files/release/opspilot/Dockerfile .