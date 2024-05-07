### Building and running your application


On the host make sure usbmuxd installed and running as root.
When you're ready, start your application by running:
`docker compose up --build`.

if you need to pair your device after container already running
```
docker compose exec tunnel bash
SideJITServer -y
```
Your application will be available at http://localhost:8080.


If you are running a distribution that uses podman instead of docker for best user experience I recommend this:
  Fedora:
  ```
  # install docker-compose 
  sudo dnf install docker-compose
  # make sure docker command is available as podman almost 1:1 drop-in replacement __almost__
  sudo ln -s /usr/bin/podman /usr/bin/docker
  # make sure root user has DOCKER_HOST variable set to podman.sock so docker-compose script can use it
  # add this line to /etc/environment
  DOCKER_HOST=unix://var/run/podman/podman.sock
  ```
  and now you can run 
  `sudo docker-compose up --build`

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)
