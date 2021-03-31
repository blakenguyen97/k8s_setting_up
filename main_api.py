from kubernetes import client, config

from flask import Flask, request, jsonify
apps = Flask(__name__)

config.load_incluster_config()
apps_v1 = client.AppsV1Api()

def create_deployment_object(url, url_id):

    # Configureate Pod template container
    container = client.V1Container(
        name="{}-container".format(url_id),
        image="cloudcam_main:1.0",
        env=[
            client.V1EnvVar(
                name="URL",
                value = url
            ),
            client.V1EnvVar(
                name="URL_ID",
                value = url_id
            )
            ],
        volume_mounts=[client.V1VolumeMount(
                        name="aaaa",
                        mount_path="/DATA")]
    )

    volume = client.V1Volume(
        name="aaaa",
        host_path=client.V1HostPathVolumeSource(path="/DATA")
    )

    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "{}-container".format(url_id)}),
        spec=client.V1PodSpec(containers=[container], volumes = [volume]))

    # Create the specification of deployment
    spec = client.V1DeploymentSpec(
        replicas=1,
        template=template,
        selector={'matchLabels': {"app": "{}-container".format(url_id)}})

    # Instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="{}-main".format(url_id)),
        spec=spec)

    return deployment


def create_deployment(api_instance, deployment):
    # Create deployement
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace="default")
    return "Deployment created. status='%s'" % str(api_response.status)

def delete_deployment(api_instance, url_id):
    # Delete deployment
    api_response = api_instance.delete_namespaced_deployment(
        name="{}-main".format(url_id),
        namespace="default",
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    return "Deployment deleted. status='%s'" % str(api_response.status)


# "---------API---------"
@apps.route('/start',methods=['POST'])
def start():
    if request.method == 'POST':

        # Get the params
        url = request.args.get('URL')
        url_id = request.args.get('URL_ID')

        # Create deployment object
        deployment = create_deployment_object(url=url, url_id=url_id)
    
        return create_deployment(apps_v1, deployment=deployment)   
    
@apps.route('/stop',methods=['POST'])
def stop():
    if request.method == 'POST':
        url_id = request.args.get('URL_ID')
        return delete_deployment(apps_v1, url_id)

if __name__ == "__main__":
    port = 5000
    apps.run(host='0.0.0.0', port=port,threaded=True,debug=False)
