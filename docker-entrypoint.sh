django-admin startproject eatenAway
python $(pwd)/eatenAway/manage.py makemigrations
python $(pwd)/eatenAway/manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('root', 'wizley@github.com', 'alpine')" | python3 $(pwd)/eatenAway/manage.py shell
