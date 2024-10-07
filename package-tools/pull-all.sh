PROJECTS='volttron-core volttron-lib-auth volttron-lib-zmq volttron-zmq'
d=`pwd`

for p in ${PROJECTS}; do
	echo "For $p"
	cd "${p}"
	git pull --rebase
	cd ..
done;
