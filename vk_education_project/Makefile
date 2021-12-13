start:
	docker-compose up --build

start-detach:
	docker-compose up --build --detach

migrations:
	docker exec -it vk_education_project_vk_education_project_1 python manage.py makemigrations

migrate:
	docker exec -it vk_education_project_vk_education_project_1 python manage.py migrate

stop:
	docker-compose stop