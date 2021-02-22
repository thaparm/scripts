set -e
rm -rf cpd-cli-workspace
rm -fr /usr/local/bin/plugins/lib/linux/.cpd.lock
oc delete cm cpd-install-operator-reconcile-lock cpd-install-operator-target-status-lock cpd-operation-cm
oc delete pod -l name=cpd-install-operator
NAMESPACE=zen
OPENSHIFT_USERNAME=kubeadmin
OPENSHIFT_REGISTRY_PULL=image-registry.openshift-image-registry.svc:5000
cpd-cli uninstall --assembly   watson-assistant-operator -n zen
cpd-cli uninstall --assembly  ibm-minio-operator  -n zen
cpd-cli uninstall --assembly  ibm-cloudpakopen-elasticsearch-operator   -n zen
cpd-cli uninstall --assembly  redis-operator    -n zen
cpd-cli uninstall --assembly  ibm-etcd-operator -n zen
cpd-cli uninstall --assembly ibm-watson-gateway-operator -n zen
cpd-cli uninstall --assembly  edb-operator -n zen
cpd-cli uninstall --assembly lite -n zen
cpd-cli adm --repo ./repo.yaml --assembly lite --arch x86_64 --namespace $NAMESPACE --accept-all-licenses --apply
cpd-cli install  --repo repo.yaml --assembly lite --namespace $NAMESPACE --storageclass ocs-storagecluster-cephfs --latest-dependency  --insecure-skip-tls-verify  --accept-all-licenses  --transfer-image-to "$(oc registry info)"/$NAMESPACE --cluster-pull-prefix $OPENSHIFT_REGISTRY_PULL/$NAMESPACE --target-registry-username $OPENSHIFT_USERNAME --target-registry-password="$(oc whoami -t)"


cpd-cli adm --repo ./repo.yaml --assembly watson-assistant --arch x86_64 --namespace $NAMESPACE --accept-all-licenses --apply

# shellcheck disable=SC2046
cpd-cli install  --repo repo.yaml --assembly edb-operator --optional-modules edb-pg-base:x86_64 --namespace $NAMESPACE  --accept-all-licenses  --transfer-image-to "$(oc registry info)"/$NAMESPACE --cluster-pull-prefix $OPENSHIFT_REGISTRY_PULL/$NAMESPACE --target-registry-username $OPENSHIFT_USERNAME --target-registry-password=$(oc whoami -t)  --insecure-skip-tls-verify

cpd-cli install  --repo repo.yaml --assembly watson-assistant-operator --optional-modules watson-assistant-operand-ibm-events-operator:x86_64 --namespace $NAMESPACE --storageclass ocs-storagecluster-ceph-rbd  --latest-dependency  --insecure-skip-tls-verify  --accept-all-licenses --override wa-install-override.yaml  --transfer-image-to "$(oc registry info)"/$NAMESPACE --cluster-pull-prefix $OPENSHIFT_REGISTRY_PULL/$NAMESPACE --target-registry-username $OPENSHIFT_USERNAME --target-registry-password="$(oc whoami -t)"

cpd-cli install  --repo repo.yaml --assembly watson-assistant --instance wa001 --namespace $NAMESPACE --storageclass ocs-storagecluster-ceph-rbd --latest-dependency  --insecure-skip-tls-verify  --accept-all-licenses --override wa-install-override.yaml  --transfer-image-to "$(oc registry info)"/$NAMESPACE --cluster-pull-prefix $OPENSHIFT_REGISTRY_PULL/$NAMESPACE --target-registry-username $OPENSHIFT_USERNAME --target-registry-password="$(oc whoami -t)"