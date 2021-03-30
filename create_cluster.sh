sudo kubeadm init --pod-network-cidr=192.168.0.0/16

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# CNI Plugin
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

# NVIDIA GPU Plugin
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.$

# Taint master node
kubectl taint nodes --all node-role.kubernetes.io/master-
