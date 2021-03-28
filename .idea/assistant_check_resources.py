import warnings
from kubernetes import client, config
warnings.filterwarnings("ignore")

def load_config():
    '''
    load kubernetes config
    :return: None
    '''
    config.load_kube_config()
    return

def list_pods():
    v1_api = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1_api.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    return

def list_ns_pods(namespace, label = None):
    v1 = client.CoreV1Api()
    #    print("Listing pods with their IPs in namespace {}".format(ns))
    ret = v1.list_namespaced_pod(namespace = namespace,watch=False)

    if label:
        retlist = []
        for i in ret.items:
            for keys in label:
                if (keys in i.metadata.labels  and i.metadata.labels.items() >= label.items()
                        and i.status.phase == "Running"):
                    retlist.append(i.metadata.name)
        return retlist
    return ret

def containers_in_pod(podname, ns):
    v1_api = client.CoreV1Api()
    if ns:
        listpods = v1_api.list_namespaced_pod(namespace = ns,watch=False)
    else:
        listpods = v1_api.list_pod_for_all_namespaces(watch=False)
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
                if (keys in i.metadata.labels
                        and i.metadata.labels.items() >= label.items()
                        and i.status.phase == "Running" ):

                    for k in range(len(i.spec.containers)):

                        retlist.append([i.metadata.name,
                                        i.spec.containers[k].name,
                                        i.metadata.annotations["productName"],
                                        i.metadata.labels["icpdsupport/addOnId"],
                                        convert(i.spec.containers[k].resources.requests.get('cpu')),
                                        convert(i.spec.containers[k].resources.limits.get('cpu')),
                                        convert(i.spec.containers[k].resources.requests.get('memory')),
                                        convert(i.spec.containers[k].resources.limits.get('memory')),
                                        i.metadata.labels['slot']
                                        ])
        return retlist
    return ret

def convert(number = None):
    unit = {'m': "1/1024",                  # mili
               'M': "1024",                 # mega
               'G': "(1024**2)",            # giga
               'T': "(1024**3)",            # tera
                "Ki": "1024",               #kilo
               'Mi': "(1024**2)",           # mega
               'Gi': "(1024**3)",           # giga
               'Ti': "(1024**4)",           # tera
               }
    if number == None or type(number) == int or number.isnumeric():
        return number
    else:
        number = ([number.replace(key,"*" + val) for key,val in unit.items() if number.endswith(key)])
        return eval(number[0])


def main():
    load_config()
    resList = resources("zen", label = {"icpdsupport/addOnId" : "assistant"})
#    print(p)
    for name in resList:
        print(name)
    cpu_req = 0
    cpu_limit = 0
    mem_req = 0
    mem_limit = 0
    for name in resList:
        cpu_req += float(name[4])
        cpu_limit += float(name[5])
        mem_req += float(name[6])
        mem_limit += float(name[7])
    print("\n\n\tTotal requirements are : \n\n\
    CPU Requests    = {} CPUs\n\
    CPU Limits      = {} CPUs\n\
    Memory Requests = {} Gi\n\
    Memory Limits   = {} Gi\n".format(cpu_req, cpu_limit , mem_req/(1024**3), mem_limit/(1024**3)))


if __name__ == '__main__':
    main()
