from kubernetes import client, config, watch
import warnings
warnings.filterwarnings("ignore")


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
 #   for i in ret.items:
#        print("{:80s}{:20s}{:20s}". format(i.metadata.name, i.metadata.namespace, i.status.pod_ip))
  #      print(i)


def watch10():
    v1 = client.CoreV1Api()
    count = 10
    w = watch.Watch()
    for event in w.stream(v1.list_namespace, _request_timeout=60):
       print("Event: %s %s" % (event['type'], event['object'].metadata.name))
       count -= 1
       if not count:
           w.stop()

def check_logs(ns,pod,cont = None, filter = None, since_seconds = 7000000, timestamps = True, taillines = 5):
    v1 = client.CoreV1Api()
    try:
        logs = v1.read_namespaced_pod_log(namespace = ns, name = pod, container = cont, pretty = True , tail_lines = taillines )
        ret = ""
        if filter:
            errors = [line for line in logs.split('\n') if filter.casefold() in line.casefold()]
            ret = ""
            for line in errors:
                ret +=  pod + " : " + cont + " : " + line + "\n"
            ret +=  80*"*"
            return ret
        for line in logs.split('\n'):
            ret +=  pod + " : "  + cont + " : " + line + "\n"
        ret +=  80*"*"
        return ret
    except ApiException as e:
        return ("Exception when calling CoreV1Api->read_namespaced_pod_log: %s\n" % e)


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


def main():
    load_config()
#   list_pods()

#    listpods = list_ns_pods(ns = "zen", label = {'component': 'store'})
    listpods = list_ns_pods(ns = "zen", label = {'icpdsupport/addOnId': 'assistant'})
    for i in listpods:
        for j in containers_in_pod(i, "zen"):
#            print(j)
            logs = check_logs("zen",i ,cont = j, filter = "Error")
            print(logs)
   #         print( *errors, sep = "\n")


if __name__ == '__main__':
    main()