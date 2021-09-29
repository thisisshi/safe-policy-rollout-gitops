sync:
	echo "Uploading policystream image"
	docker pull cloudcustodian/policystream:latest
	docker tag cloudcustodian/policystream:latest $$(terraform output -raw policystream_image_url):latest
	aws ecr get-login-password | docker login --username AWS --password-stdin $$(terraform output -raw policystream_image_url)
	docker push $$(terraform output -raw policystream_image_url):latest
	echo "Uploading c7n image"
	docker pull cloudcustodian/c7n:$$(terraform output -raw c7n_image_tag)
	docker tag cloudcustodian/c7n:$$(terraform output -raw c7n_image_tag) $$(terraform output -raw c7n_image_url):$$(terraform output -raw c7n_image_tag)
	aws ecr get-login-password | docker login --username AWS --password-stdin $$(terraform output -raw c7n_image_url)
	docker push $$(terraform output -raw c7n_image_url):$$(terraform output -raw c7n_image_tag)
