import warnings
from kubernetes import client, config, watch
warnings.filterwarnings("ignore")

_prefix = {'y': 1e-24,  # yocto
           'z': 1e-21,  # zepto
           'a': 1e-18,  # atto
           'f': 1e-15,  # femto
           'p': 1e-12,  # pico
           'n': 1e-9,   # nano
           'u': 1e-6,   # micro
           'm': 1e-3,   # mili
           'c': 1e-2,   # centi
           'd': 1e-1,   # deci
           'k': 1e3,    # kilo
           'M': 1e6,    # mega
           'Mi': 1e6,    # mega
           'G': 1e9,    # giga
           'Mi': 1e9,    # giga
           'T': 1e12,   # tera
           'P': 1e15,   # peta
           'E': 1e18,   # exa
           'Z': 1e21,   # zetta
           'Y': 1e24,   # yotta
           }

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


def main():
    load_config()
    p = resources("zen", label = {"icpdsupport/addOnId" : "assistant"})
#   print(p)      print( *errors, sep = "\n")
    print(p)

if __name__ == '__main__':
    main()
