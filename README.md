# docker-rate-limit-healer
This repository contains tooling around changing Dockerhub images
to self-hosted repository.

Since Dockerhub is going to introduce rate-limitation of 100 pulls in 6 hours
you may experience fails in builds and deployments from the 1st of November, 2020.

[Read more](https://cloud.google.com/blog/products/containers-kubernetes/mitigating-the-impact-of-new-docker-hub-pull-request-limits)

## BE AWARE!
This tooling has no warranties of any functionality, validate the end result before
deploying to your clusters!

## How you use?
1) Install requirements: `pip install -r requirements.txt`

2) Run `discover.sh > report.txt` it is going to use your kubectl configuration
to check all the namespaces in your cluster and report images being used from Dockerhub.

3) Set `DOCKER_MIRROR_REPO` environmental variable where you want your Dockerhub images
mirrored to. (Example: `export DOCKER_MIRROR_REPO="gcr.io/greg-259714`)

Note that it works with any docker repository assuming you have the proper permissions from
the host machine where you execute this script.

4) Run `mirror.py` - this command is going to pull all the images you have in your cluster
from Dockerhub then push them to the target repository (e.g.: GCR)

5) Running this command is going to create `changes.txt` that has the mapping
between the Dockerhub image and the newly mirrored image.

6) Now you can run `python heal-manifest.py <PATH_TO_MANIFEST.yaml>`, this command
is going to print to the stdout the healed manifest with the changed images pointing to the
new repo.

7) Before doing any apply be super cautious and check the result!
