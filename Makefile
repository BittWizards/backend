app-up:
	@echo "Migrate and Starting Django app ..."
	cd backend && python manage.py makemigrations && python manage.py migrate && python manage.py runserver

make-migrations:
	@echo "Make migrations ..."
	cd backend && python manage.py makemigrations

loaddata:
	@echo "Input data to db ..."
	cd backend && python manage.py loaddata */fixtures/*.json

up:
	@echo "Starting service ..."
	sudo docker compose up --build -d

down:
	@echo "Stopping service ..."
	sudo docker compose down

down-v:
	@echo "Stopping service and removing all volumes ..."
	sudo docker compose down -v
