PROJECTS='volttron-core volttron-lib-auth volttron-lib-zmq volttron-testing volttron-zmq'
for x in ${PROJECTS}; do
	echo "for $x"
	cd $x
	git stash 
	cd ..
done;

