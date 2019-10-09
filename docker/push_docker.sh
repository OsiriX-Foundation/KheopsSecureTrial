TAG=demo
(cd .. && docker build -t osirixfoundation/kheops-secure-trial:${TAG} .)
docker push osirixfoundation/kheops-secure-trial:${TAG}
