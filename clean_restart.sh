#!/bin/bash

docker container stop systems-puzzle_nginx_1 systems-puzzle_flaskapp_1 systems-puzzle_db_1

docker container prune

docker-compose up -d db

docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"

docker-compose up -d
