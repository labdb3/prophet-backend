# prophet-backend

python manage.py runserver 0.0.0.0:8000

docker run -itd --name prophet -p 3000:3000 -p 8000:8000 zdliu2022/prophet /bin/bash -c "cd && tmuxinator start prophet"
