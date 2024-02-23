app-up:
	@echo "Migrate and Starting Django app ..."
	cd backend && python manage.py migrate && python manage.py runserver

up:
	@echo "Starting service ..."
	sudo docker compose up --build -d

down:
	@echo "Stopping service ..."
	sudo docker compose down

down-volumes:
	@echo "Stopping service and removing all volumes ..."
	sudo docker compose down -v