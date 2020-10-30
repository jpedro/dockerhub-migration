import yaml
import sys

manifest = None
with open(sys.argv[1], 'r') as stream:
    manifest = yaml.safe_load(stream)

change_table = {}
with open("change.txt", 'r') as stream:
    lines = stream.readlines()
    for line in lines: 
        original_image, new_image = [x.rstrip('\n') for x in line.split(' ')]
        change_table[original_image] = new_image

if manifest is None:
    print("Something went wrong check if file exists or you have permissions on it")

containers = None
if manifest['kind'] in ["Deployment", "Job", "StatefulSet", "ReplicaSet", "DaemonSet"]:
    containers = manifest['spec']['template']['spec']['containers']
    new_containers = []
    for container in containers:
        try:
            copy_container = container
            copy_container['image'] = change_table[container['image']]
            new_containers.append(copy_container)
        except:
            raise Exception("""%s image is not found in the change list... there is no alternative.
Please make sure you define %s image.""" % (container))
    manifest['spec']['template']['spec']['containers']  = new_containers
    print(yaml.safe_dump(manifest, default_flow_style=False))


if manifest['kind'] ==  "Pod":
    containers = manifest['spec']['containers']
    new_containers = []
    for container in containers:
        try:
            new_containers.append(change_table[container['image']])
        except:
            raise Exception("""%s image is not found in the change list... there is no alternative.
Please make sure you define %s image.""" % (container))
    manifest['spec']['containers']  = new_containers
    print(yaml.safe_dump(manifest))

