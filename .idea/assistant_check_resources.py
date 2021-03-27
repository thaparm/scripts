import warnings
from kubernetes import client, config, watch
warnings.filterwarnings("ignore")
# for i in $(oc get pods --no-headers | grep -i running | cut -f1 -d\ );
# do echo $i;
# oc get pods -o jsonpath="{.metadata.name},
# {.metadata.annotations.productName},
# {.metadata.labels.icpdsupport/addOnId},
# {.spec.containers[*].resources.requests.cpu},
# {.spec.containers[*].resources.limits.cpu},
# {.spec.containers[*].resources.requests.memory},
# {.spec.containers[*].resources.limits.memory},
# {.metadata.labels.slot} {'\n'}" ${i} >> ./running-pods.resources-cpu-ram-v2.csv; done

# Configs can be set in Configuration class directly or using helper utility
def load_config():
    config.load_kube_config()
    return

def list_pods():
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    return

def list_ns_pods(ns, label = None):
    v1 = client.CoreV1Api()
    #    print("Listing pods with their IPs in namespace {}".format(ns))
    ret = v1.list_namespaced_pod(namespace = ns,watch=False)

    if label:
        retlist = []
        for i in ret.items:
            for keys in label:
                if (keys in i.metadata.labels  and i.metadata.labels.items() >= label.items()):
                    retlist.append(i.metadata.name)
        return retlist
    return ret

def containers_in_pod(podname, ns):
    v1 = client.CoreV1Api()
    if ns:
        listpods = v1.list_namespaced_pod(namespace = ns,watch=False)
    else:
        listpods = v1.list_pod_for_all_namespaces(watch=False)
    list_of_containers = []
    for i in listpods.items:
        for cont in range(5):
            try:
                if i.metadata.name == podname and  i.spec.containers[cont]:
                    list_of_containers.append(i.spec.containers[cont].name)
            except:
                pass
    return list_of_containers


def resources(ns, label = None):
    v1 = client.CoreV1Api()
    #    print("Listing pods with their IPs in namespace {}".format(ns))
    ret = v1.list_namespaced_pod(namespace = ns,watch=False)

    if label:
        retlist = []
        for i in ret.items:
            for keys in label:
                if (keys in i.metadata.labels  and i.metadata.labels.items() >= label.items()):

                    for k in range(len(i.spec.containers)):

                        retlist.append([i.metadata.name,
                                        i.metadata.annotations["productName"],
                                        i.metadata.labels["icpdsupport/addOnId"],
                                        i.spec.containers[k].resources.requests.get('cpu'),
                                        i.spec.containers[k].resources.limits.get('cpu'),
                                        i.spec.containers[k].resources.requests.get('memory'),
                                        i.spec.containers[k].resources.limits.get('memory'),
                                        i.metadata.labels['slot']
                                        ])
        return retlist
    return ret
# oc get pods -o jsonpath="{.metadata.name},
# {.metadata.annotations.productName},
# {.metadata.labels.icpdsupport/addOnId},
# {.spec.containers[*].resources.requests.cpu},
# {.spec.containers[*].resources.limits.cpu},
# {.spec.containers[*].resources.requests.memory},
# {.spec.containers[*].resources.limits.memory},
# {.metadata.labels.slot}

def main():
    load_config()
    p = resources("zen", label = {"icpdsupport/addOnId" : "assistant"})
#   print(p)      print( *errors, sep = "\n")
    print(p)

if __name__ == '__main__':
    main()

