sudo kubeadm reset
sudo rm -rf ~/.kube/config

sudo systemctl stop kubelet
sudo systemctl stop docker

sudo rm -rf /var/lib/cni/*
sudo rm -rf /var/run/crio/*
sudo rm -rf /var/log/crio/*
sudo rm -rf /var/lib/kubelet/*

sudo systemctl start docker
sudo systemctl start kubelet

echo "----FINISHED----"
