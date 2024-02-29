app-up:
	@echo "Migrate and Starting Django app ..."
	cd backend && python manage.py migrate && python manage.py runserver

make-migrations:
	@echo "Make migrations ..."
	cd backend && python manage.py makemigrations

up:
	@echo "Starting service ..."
	cd infra && sudo docker compose up --build -d

down:
	@echo "Stopping service ..."
	cd infra && sudo docker compose down

down-v:
	@echo "Stopping service and removing all volumes ..."
	cd infra && sudo docker compose down -v
