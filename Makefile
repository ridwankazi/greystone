.PHONY: help migrate-new migrate-autogen migrate-upgrade migrate-downgrade migrate-history migrate-current

help:
	@echo "Common commands:"
	@echo "  make migrate-new NAME=add_table       # create empty revision"
	@echo "  make migrate-autogen NAME=add_table   # autogenerate revision from models"
	@echo "  make migrate-upgrade TARGET=head      # apply migrations"
	@echo "  make migrate-downgrade TARGET=-1      # rollback one revision"
	@echo "  make migrate-history                  # show revision history"
	@echo "  make migrate-current                  # show current revision"

migrate-new:
	@test -n "$(NAME)" || (echo "NAME is required" && exit 1)
	alembic revision -m "$(NAME)"

migrate-autogen:
	@test -n "$(NAME)" || (echo "NAME is required" && exit 1)
	alembic revision --autogenerate -m "$(NAME)"

migrate-upgrade:
	alembic upgrade $(or $(TARGET),head)

migrate-downgrade:
	alembic downgrade $(or $(TARGET),-1)

migrate-history:
	alembic history --verbose

migrate-current:
	alembic current --verbose
