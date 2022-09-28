# k8s-nodeport-mtd

This project is meant to simulate MTD technique (on a basis of EAC0005 from MITRE Engage) on Kubernetes cluster using built-in K8s features.

NOTE: this software requires K8s cluster set up as well as Deployments and Services to shuffle.

## UNIX project setup
```
git clone https://github.com/cyberorzech/k8s-nodeport-mtd
cd k8s-nodeport-mtd
# Create python virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
In order to allow all modules work properly, first check config.yaml and adjust its parameters. Full description of each parameter can be found in documentation.

## App Reconfigurator
Run app reconfigurator in order to check cluster connection and perform first Services shuffle. It will open 5100 port on localhost (flask app).
```
python app_reconfigurator.py
```

## Update State
In order to periodically perform requests to app_reconfigurator, run update_state script and let in run in the background as long as adversary script does not perform in a reactive mode.
```
python update_state.py
```

## State Repository
Flask app exposing /state endpoint on port 5000. Once request to the endpoint is made, state repository checks for the current legitimate app port and shares it via http response.
```
python state_repository.py
```

## User
Run user script in order to simulate user activity in network. This script in user mode periodically performs requests to the legitimate app and reviews the answer. If the answer is legitimate app originated, successful requests counter is increased. At the other hand, uptime mode offers uptime measurement based on the success of requests. Every request with code 200 and legitimate app originated message is considered successful and time consumed to perform this request is added to uptime.
```
usage: user.py [-h] [-m {user,uptime}]

optional arguments:
  -h, --help            show this help message and exit
  -m {user,uptime}, --mode {user,uptime}

```
For example in order to run uptime mode:
```
python user.py -m uptime
```

NOTE: Make sure that at least update_state script with /state endpoint is active before running user script.

## Adversary
Adversary script is able to perform two predefined scenarios (described in documentation) in three MTD methodologies: proactive, reactive and mixed.

NOTE: the process of exploitation is artificial and described with probability of success P1. No app is disturbed during this process.
```
usage: adversary.py [-h] [-s {1,2}] [-t {proactive,mixed,reactive}]

optional arguments:
  -h, --help            show this help message and exit
  -s {1,2}, --scenario {1,2}
  -t {proactive,mixed,reactive}, --type {proactive,mixed,reactive}

```
For example, in order to run scenario 1 in proactive mode:
```
python adversary.py -s 1 -t proactive
```