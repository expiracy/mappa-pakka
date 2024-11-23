```shell
docker build -t mappa-pakka -f Dockerfile ..
```

```shell
docker container rm -f mappa-pakka
```

```shell
docker run --name mappa-pakka -v "C:/Users/james/PycharmProjects/mappack-bot:/app/mappa-pakka" mappa-pakka
```

```shell
docker ps
```

```shell
docker exec -it mappa-pakka bash 
```