read -p "Tag name : " TAG
echo $TAG
(cd .. && docker build -t kheops-secure-trial:dev .)
docker push osirixfoundation/kheops-secure-trial:${TAG}
