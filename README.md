# test_task
IDAPROJECT
1. sudo apt-get install python3 nginx pip3
2. pip3 install virtualenv
3. virtualenv ~/venv
4. source venv/bin/activate
5. sudo pip install django gunicorn
6. cd test_task
7. python manage.py makemigrations
8. python manage.py migrate
9. gunicorn myproject.wsgi:application --bind 100.110.120.130:8000, где 100.110.120.130 - публичный IP
10. sudo nano /etc/nginx/sites-available/default
Запишем в него следующее:
    server {
        listen 80;
        server_name 100.110.120.130; # здесь прописать или IP-адрес или доменное имя сервера
        access_log  /var/log/nginx/example.log;
     
        location /static/ {
            root /home/user/;
            expires 30d;
        }
     
        location / {
            proxy_pass http://127.0.0.1:8000; 
            proxy_set_header Host $server_name;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
11. sudo service nginx restart
12. gunicorn myproject.wsgi:application
