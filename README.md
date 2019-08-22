# Insight DevOps Engineering Systems Puzzle

## Table of Contents
1. [Understanding the puzzle](README.md#understanding-the-puzzle)
2. [Introduction](README.md#introduction)
3. [Puzzle details](README.md#puzzle-details)
4. [Instructions to submit your solution](README.md#instructions-to-submit-your-solution)
5. [FAQ](README.md#faq)

# Understanding the puzzle

We highly recommend that you take a few dedicated minutes to read this README in its entirety before starting to think about potential solutions. You'll probably find it useful to review the codebase and understand the system at a high-level before attempting to find specific bugs.

# Introduction

Imagine you're on an engineering team that is building an eCommerce site where users can buy and sell items (similar to Etsy or eBay). One of the developers on your team has put together a very simple prototype for a system that writes and reads to a database. The developer is using Postgres for the backend database, the Python Flask framework as an application server, and nginx as a web server. All of this is developed with the Docker Engine, and put together with Docker Compose.

Unfortunately, the developer is new to many of these tools, and is having a number of issues. The developer needs your help debugging the system and getting it to work properly.

# Puzzle details

The codebase included in this repo is nearly functional, but has a few bugs that are preventing it from working properly. The goal of this puzzle is to find these bugs and fix them. To do this, you'll have to familiarize yourself with the various technologies (Docker, nginx, Flask, and Postgres). You definitely don't have to be an expert on these, but you should know them well enough to understand what the problem is.

Assuming you have the Docker Engine and Docker Compose already installed, the developer said that the steps for running the system is to open a terminal, `cd` into this repo, and then enter these two commands:

    docker-compose up -d db
    docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"

This "bootstraps" the PostgreSQL database with the correct tables. After that you can run the whole system with:

    docker-compose up -d

At that point, the web application should be visible by going to `localhost:8080` in a web browser. 

Once you've corrected the bugs and have the basic features working, commit the functional codebase to a new repo following the instructions below. As you debug the system, you should keep track of your thought process and what steps you took to solve the puzzle.


***

# Change Log (PDT)

* 12:30 - Started in Ubuntu 18.04 environment.
* 12:34 - Finished building docker images and noticed there is no web app returning in Firefox. Looking into docker config files.
* 12:35 -  Noticed the port configuration for the Nginx container is set to port 80 to the host and 8080 to the container. Swapping the port numbers in the docker-compose file to achieve the desired effect.
* 12:37 - Getting a 502 error. Going to read Nginx container logs.
* 12:47 - Noted there was a 111 error Connection refused (upstream error) so I googled what are possible causes. Going to look into nginx.conf file
* 13:20 - Enabled error log in Nginx container and noticed the upstream is still not connecting. Looking into Nginx docs for proper reverse proxy set up
* 13:46 - Finished editing the Nginx config file and got rid of the upstream connection error. App is still giving a 502 error. Looking into the other container logs for a lead.
* 13:48 - Opened up the flaskapp logs and noticed the flask container is set to port 5001 while Flask is set to port 5000. Setting the Flask app.py to connect to port 5001 instead of 5000. 502 error is now gone.
* 14:20 - Noticed that when adding data to the database, the success page returns a blank pair of brackets. Went into the Postgres container and looked into the Items table to make sure the data was there and it was. Looked into the app routes to see why nothing is getting returned. Possibly may change how the HTML pages are returned.
* 14:32 - Changing the Jinja template to include template inheritance between the base and index HTML pages as groundwork for future changes
* 15:41 - Got a table of all existing items to show on a separate page. Looking into how to get crud functionality completed
* 17:48 - Added delete functionality but UI is getting clunky when navigating from the index page to the get_all page. Adding buttons to make it easier to switch between the two before committing. Looking into adding update functionality to the site.
* 20:40 - Added update capability using dictionaries to accommodate future changes to the Items table.