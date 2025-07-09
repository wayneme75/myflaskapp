# Simple Flask App in a docker container

### App.py overview

Before we start here is the full code for app.py

``` python
import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def main():
    return "<h1>You're home now!</h1>"
@app.route('/hello-world')
def hello_world():
    return "<p style='color:blue;'>Hello World</p>"

if __name__ == "__main__":
    app.run(debug=True)
```

We start by getting the tools we need. Think of Flask as a big toolbox with everything that is essential to make a web application. The first tool we’re going to use is called Flask and is the way to say to the framework: “Get Ready, I’m making a web app!”. Basically it’s the blueprint of the application.

When we do *app=Flask(__name__)*, we’re creating an instance of the Flask class and assigning it to the variable app. The *__name__* argument is a special Python variable that represents the name of the current module. It's used by Flask to determine the root path for your application's resources.
After we have our app initialized we build two routes (or pages if you want to see it from the website perspective in this case).

``` python
@app.route("/")
def main():
    return "You're home now!"

@app.route('/hello-world')
def hello_world():
    return 'Hello World' 
```

These routes determine how our application responds to different URLs requested by users.
In this case we’re not specifying an HTTP method for these endpoints, so following the Flask convention the web application will respond to HTTP GET requests by default. The ‘GET’ method is, “incidentally”, what we use when we open a page in our browser.

Lastly, we use app.run() to start the built-in development server, which is very useful to test and run Flask applications locally during development.

``` python
if __name__ == "__main__":
    app.run(debug=True)
```

This server will listen for incoming requests and direct them to the appropriate view functions based on the routes we defined before.

### Directory Structure for the app

For our web app, we can keep it simple with a directory hierarchy that is as flat as it gets:

``` text
flask-docker-miniapp/
├── app.py
├── Dockerfile
├── requirements.txt
```

Our only directory is called ‘flask-docker-miniapp’ so we put our source code and all our configuration files inside it at the same hierarchical level.
When you have bigger projects you will certainly use a more structured and layered hierarchy, but when it comes to Docker projects one thing is almost always certain: the Dockerfile should be placed in the root directory of your project or application

Let’s go through the files inside our ‘flask-docker-miniapp’ directory to define what they do and avoid any confusion:

- app.py — Contains the Flask application code. All this file contains is what we’ve seen in the previous paragraph.
- Dockerfile — The Dockerfile specifies the instructions for building our Flask-based Docker image. We’re going to dive into it in our next paragraph.
- requirements.txt — Following the Python standards, the ‘requirements.txt’ file contains all the dependencies needed by our project. A best practice is to always freeze the version of the libraries references inside the requirements file. In our case, the file will only contain one line of text:

``` text
Flask==2.3.2
```

This means that our only dependency will be Flask in the version 2.3.2.

### Writing the Dockerfile
Just like our Flask app code, the Dockerfile for our web app is going to be very simple and straightforward. Here’s what it looks like in its entirety:

``` Docker
FROM python:3.10.0-slim-buster

WORKDIR /flask-simple-app

COPY . .

RUN pip3 install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
```

Now let’s break down in detail every command from this Dockerfile:

- FROM python:3.10.0-slim-buster — The first command sets the parent image of our Docker image. We’re using a debian-based image that already contains a minimal Python installation. In particular, we’re using the Python official image version 3.10.0, specifically the “slim-buster” variant (check it out here if you need more details).
WORKDIR /flask-simple-app — This command sets the working directory inside the container to a folder named “flask-simple-app”. Since this directory won’t initially exist, the command will create it within the root of the container’s file system and then set is as working directory. In simple terms: this is where the subsequent commands will be executed.
- COPY . . — The COPY instruction copies new files or directories from a source (first argument) and adds them to the filesystem of the container at the specified path (second argument). The dot we’re using in our Dockerfile simply means ‘current directory’ for the source and ‘current working directory’ for the destination. So in our case the source will be the folder the Dockerfile is in (’flask-docker-miniapp’) and the destination will be the current working directory in the Docker container (’/flask-simple-app’). The command will copy everything is in the source to the destination.
- RUN pip3 install -r requirements.txt — This instruction installs the Python packages listed in our “requirements.txt” file. In our specific case, it only installs Flask version 2.3.2. The RUN command is generally used to execute any commands on top of the current state of the image. The “current state” at this point was an intermediate layer with just a Python installation and a working directory set to ‘/flask-simple-app’ in which we copied all our project files.
- CMD [ “python3”, “-m” , “flask”, “run”, “ — host=0.0.0.0”] — This final line in our Dockerfile may seem a little complicated but it’s really not that big of a deal. The CMD instruction provides a default command to execute when you launch the container for our built image. Be aware that the CMD instruction must be unique in a Dockerfile. If you list more than one then the engine will simply ignore all but the last CMD. In our case the CMD instruction simply tells the container to start the Flask application:

    - “python3” — runs the Python interpreter
    - “-m flask” — instructs Python to run the “Flask” module
    -  “run” — is a Flask command to start the development server
    - “ — host=0.0.0.0” — instructs the development server to listen on all available network interfaces so that our tiny app can be accessed from outside the container

### Making it work

We’re close to make the magic happen!

At this point we have everything we need:

- Our Flask app code in the *‘app.py’* file
- A *‘requirements.txt’* file with all package dependencies needed by our app
- A little *‘Dockerfile’* that contains all the instructions to build our image

All we need to do is type some commands in our terminal and watch our little creature take off.

To build a Docker image we use the ‘docker build’ command in the terminal. This is used to create a Docker image from a set of instructions specified in a Dockerfile. Here’s the syntax:

``` Docker
docker run -p 8080:5000 dockersamples/tiny-flask-app:latest
```

Let’s break down the parts of this command:

- “-t <image_name>:<tag>” — is used to name and tag an image, so that we can appropriately label and version it and reference that specific name later on. It’s a best practice to divide the <image_name> in two parts, the repository name and the actual image name, so in our case we could do something like ‘dockersamples/tiny-flask-app’ with tag ‘latest’. I won’t go into detail about repositories and tags here, but for now it’s ok to consider the name of the image as a whole.
- <path_to_dockerfile_directory> — Well this is pretty self-explanatory: you need to specify the path to your Dockerfile so that the ‘docker build’ can look it up. The usual thing to do here is just place yourself in the project’s root directory with your terminal session and use ‘.’ instead of the path.

Put it all togethere and we can build our image by running the following miracolous command:

``` Docker
docker build -t dockersamples/tiny-flask-app:latest .
```

If everything went the right way you should be able to see the newly created image in the list of available images by using the command ‘docker images’ (or ‘docker image ls’). This is used to show all top level images, their repository and tags, and their size.

So if you made it alive to this point, all that remains to do is to create and run a container from our brand new Docker image. For this task we need to use ‘docker run’ command:

``` Docker
docker run [options] <image_name> [command] [arguments]
```

We already know what the <image_name> is, so let’s focus on the other parts:
- [options] — is used to potentially include a list of optional flags, some of the most used being ‘-p’ for port mapping, ‘-d’ to run the container in detached mode or ‘-it’ to run an interactive terminal (if you’re curious you can check ’em all out here)
- [command] and [arguments] -these are both optional and are used to run a default command inside the container on startup, along with arguments if they are needed. What the [command] does is basically the same thing we’ve seen before with the CMD instruction in our Dockerfile. If you use it in the ‘docker run’ command you simply override the CMD instruction.

So let’s take a look at what the ‘docker run’ command would look like for our specific use-case:

``` Docker
docker run -p 8080:5000 dockersamples/tiny-flask-app:latest
```

Why do we use the ‘-p’ flag you say? Well, in our case we need to establish a communication between our host machine and the container, so we map the default Flask port (5000) to a port on our host machine. Without that we won’t be able to reach the web app from outside the container itself. So what we do here is we say Docker: “Hey, forward all requests from port 8080 of the host machine to port 5000 inside the Docker container”.
And just like magic, if we now open the browser on our host machine and type “localhost:8080” on the address bar.

# Publish to Azure Container Registry

Login to the ACR

``` pwsh
az acr login <registryName>
```

Within the folder for the app

``` docker
docker tag crux-hello-world:latest
docker push crux-hello-world:latest <registry>.azurecr.us/hello-world
```

To update ACR if the web app changes:

``` pwsh
az acr update --name <registry>.azurecr.us/hello-world
```

# To deploy to AKS

Use the helloworld_app.yaml to build the app
Use the helloworld_ingress.yaml to create the controller

NOTE: create the LoadBalancer through the interface. Need to be proxied and service tokened.


*******
Credits: https://medium.com/@andreajrubino/run-the-simplest-web-app-in-docker-23df528e8b8