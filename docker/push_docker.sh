read -p "Tag name : " TAG
echo $TAG
docker build -t osirixfoundation/kheops-secure-trial:${TAG} .
docker push osirixfoundation/kheops-secure-trial:${TAG}
