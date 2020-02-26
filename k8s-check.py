import os
import subprocess
import time
from subprocess import CalledProcessError
import threading


def cluster_info():
  cmd ="kubectl cluster-info"
  subprocess.call(cmd.split())


def nodes():
  print("====================Nodes Check====================\n")
  num_node = 0
  num_ready = 0
  num_master = 0
  ver_ctl = []
  cmd ="kubectl get no"
  result = str(subprocess.check_output(cmd.split()), encoding='utf-8')
  result = result.splitlines()
  num_node = len(result) - 1
  for i in range(1, len(result)):
    result[i] = result[i].split( )    
    if result[i][1] == "Ready":
      num_ready += 1
    if result[i][2] == "master":
      num_master += 1
  print("Ready/All Node: %s/%s" % (num_ready,  num_node))
  if num_node == num_ready:
    print("All nodes are Ready")
  else:
    print("%s nodes are NotReady" % num_node - num_ready)
  print("%s master, %s worker" % (num_master, num_node - num_master))
  print("kubernetes version: %s\n" % result[i][4])
  cmd ="kubectl version"
  result = str(subprocess.check_output(cmd.split()), encoding='utf-8')
  result = result.splitlines()
  for i in range(len(result)):
    result[i] = result[i].split(", ")
    ver_ctl.append(result[i][2].split("\""))
  print("kubectl client version: %s" % ver_ctl[0][1])
  print("kubectl master version: %s" % ver_ctl[1][1])



def pods():
  print("\n====================Pods Check=====================\n")
  num_pod = 0
  num_running = 0
  cmd ="kubectl get po -n kube-system"
  result = str(subprocess.check_output(cmd.split()), encoding='utf-8') 
  result = result.splitlines()
  num_pod = len(result) - 1
  for i in range(1, len(result)):
    result[i] = result[i].split( )
    if result[i][2] == "Running":
      num_running += 1
  print("Running/All Pod in kube-system: %s/%s" % (num_running,  num_pod))
  if num_pod == num_running:
    print("All pods in kube-system are running\n")
  else:
    print("%s pods are not running" % num_pod - num_running)

def docker():
  print("\n====================Docker Info====================\n")
  cmd ="docker version"
  subprocess.call(cmd.split())

def cni():
  print("\n=======================CNI=========================\n")
  cmd = "ls /etc/cni/net.d/"
  subprocess.call(cmd.split())

def create():
  print("\n===============Deployment Create===================\n")  
  cmd = "kubectl create -f auto-scaling"
  subprocess.call(cmd.split())  
  cmd = "kubectl get deploy nginx"
  finished = "false"
  while finished != "true":
    time.sleep(5)
    result = str(subprocess.check_output(cmd.split()), encoding='utf-8')
    result = result.splitlines()
    for i in range(1, len(result)):
      result[i] = result[i].split( )
    if result[1][1] == "1/1":
      finished = "true"
  print("Deploy Success")
    
def lb():
  print("\n==============Loadbalancer Support=================\n")
  cmd = "kubectl get svc nginx"
  result = str(subprocess.check_output(cmd.split()), encoding='utf-8')
  result = result.splitlines()
  for i in range(1, len(result)):
    result[i] = result[i].split( )
  if result[1][3] == "<pending>":
    print("Loadbalabcer Support : False")
  else:
    print("Loadbalabcer Support : True")
    print("Assigned test example ip is : %s" % result[1][3])


def delete():
  print("\n===============Deployment Delete===================\n")
  cmd = "kubectl delete -f auto-scaling"
  subprocess.call(cmd.split())
  cmd = "kubectl get deploy nginx-deployment"
  try:
    subprocess.check_output(cmd.split())
  except CalledProcessError as e:
    output = e.output
    returncode = e.returncode
    if returncode == 1:
      print("Delete Success")


def curl(ip):
  t = threading.currentThread()
  cmd = "curl http://" + ip
  FNULL = open(os.devnull, 'w')
  print(cmd)
  print("start curl")
  while getattr(t, "do_run", True):
    subprocess.call(cmd.split(), stdout=FNULL, stderr=subprocess.STDOUT)

def hpa():
  print("\n===============Autoscaling Support=================\n")
  cmd = "kubectl get hpa nginx-hpa"
  finished = "false"
  while finished != "true":
    result = str(subprocess.check_output(cmd.split()), encoding='utf-8')
    result = result.splitlines()
    for i in range(1, len(result)):
      result[i] = result[i].split( )
    if result[1][2].find('unknown') == -1:
      finished = "true"
      print("HPA is Ready")
    else:
      print("Wait HPA Ready")
      time.sleep(20)
  cmd = "kubectl get svc nginx"
  result = str(subprocess.check_output(cmd.split()), encoding='utf-8')
  result = result.splitlines()
  for i in range(1, len(result)):
    result[i] = result[i].split( )
  i = result[1][3]
  t = threading.Thread(target=curl,args=(i,))
  t.start()
  cmd = "kubectl get deploy nginx"
  finished = "false"
  while finished != "true":
    result = str(subprocess.check_output(cmd.split()), encoding='utf-8')
    result = result.splitlines()
    for i in range(1, len(result)):
      result[i] = result[i].split( )
    if result[1][1] != "1/1":
      print("scale changed")
      t.do_run = False
      t.join()
      finished = "true"
      print("Autoscaling Success")
    else:
      print("Wait Pod scaling")
      time.sleep(20)
  print("Ready Pod from 1/1 to %s" % result[1][1])

if __name__ == '__main__':
  cluster_info()
  nodes()
  pods()
  docker()
  cni()
  create()
  lb()
  hpa()
  delete()
