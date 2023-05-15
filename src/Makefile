up:
	docker-compose up -d
	docker-compose run web python manage.py migrate

wipe:
	docker-compose down -v --rmi local && docker system prune && docker volume prune

run_tests:
	sudo find data/ -type d -exec chmod 755 {} \;
	pytest -vvv

run_checks:
	docker-compose exec web pylint --rcfile .pylintrc app/ employees/ restaurant/ app/ manage.py conftest.py
	docker-compose exec web pytest -vvv