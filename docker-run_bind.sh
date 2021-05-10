docker run --name=jenkins -d -p 5000:5000 \
  --restart=always \
  -v /Volumes/Data/MyProjects/gql_server:/conf \
  tanumkroken/jenkins:latest
