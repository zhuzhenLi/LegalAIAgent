.PHONY: init-db

init-db:
	cd backend && python -m app.db.init_db 