# animelistto

Search and add your animes in broadcast directly to sonarr
 

![](img/example01.png)



# docker-compose.yml
```dockerfile
version: "3.9"
services:
  animerr:
    container_name: animerr
    build:
        context: .
        dockerfile: ./Dockerfile
    environment:
      - FLASK_ENV=development
      - SONARR_IP=192.168.0.10:8989
      - SONARR_API=61db77c5ec5b4bc3be57ab3a3f1e36e2
    volumes:
      - /mnt/user/appdata/animerr:/config
    ports:
      - "5757:5757"
```
