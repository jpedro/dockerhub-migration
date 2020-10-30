import docker
import os

# Using readlines()
source_file = open('report.txt', 'r')

Lines = source_file.readlines()
client = docker.from_env()
BASE_URL = os.environ('DOCKER_MIRROR_REPO')

# writing to file
state_file = open('change.txt', 'w')

# Strips the newline character
for line in Lines:
    image  = line.split(" ")[1]
    core_image = image.split('/')
    if len(core_image) != 1:
        continue
    dockerhub_image = core_image[0].rstrip('\n')
    image_name, tag_name = dockerhub_image.split(':')
    client.images.pull(dockerhub_image)
    local_image = client.images.get(dockerhub_image)
    TARGET_REPO = BASE_URL + '/' + dockerhub_image
    local_image.tag(TARGET_REPO)
    client.images.push(TARGET_REPO)
    state_file.writelines(dockerhub_image + " " +  TARGET_REPO)

source_file.close()
state_file.close()
