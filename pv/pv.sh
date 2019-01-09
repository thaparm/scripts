#!/bin/bash

COUNTER=1
OPERATION=${1:-apply}

echo 
echo
echo "This script creates 13 PVs for Conversation 1.0.1"
echo "The script can be used to apply or delete PVs; defaults to apply"
echo "to delete PVs, add delete param - ./pv.sh delete"
echo 
echo "OPERATION=${OPERATION}"
sleep 3
echo

   
while [  $COUNTER -lt 14 ]; do
   echo "kubectl ${OPERATION} -f pv_00${COUNTER}.yaml"
   kubectl ${OPERATION} -f pv_00${COUNTER}.yaml
   let COUNTER=COUNTER+1 
   #sleep 3
done