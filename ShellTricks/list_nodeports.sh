#/bin/bash
NS_NUM=`kubectl get ns | wc -l`
NS_NUM=$((NS_NUM - 1))

for ns in `kubectl get ns | tail -$NS_NUM | awk '{print $1}'`
do
	SVC_NUM=`kubectl get svc --namespace=$ns | wc -l`
	SVC_NUM=$((SVC_NUM - 1))
	if [ $SVC_NUM -gt 0 ]
	then
		for svc in `kubectl get svc --namespace=$ns | tail -$SVC_NUM | awk '{print $1}'`
		do
			nodePort=`kubectl describe svc $svc --namespace=$ns | grep NodePort | grep -v Type | awk '{print $3}'`
			echo $ns $svc $nodePort
		done
	fi
done
