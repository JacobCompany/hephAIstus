.PHONY: format create_models

CMD:=poetry run
MODEL_DIR:=src/hephaistus/models

format:
	@$(CMD) ruff check --fix src
	@$(CMD) ruff format src
	@$(CMD) isort src

format_check:
	@$(CMD) ruff check src
	@$(CMD) ruff format --diff src
	@$(CMD) isort --check-only src

create_models: $(MODEL_DIR)/Modelfile_*
	@for file in $^ ; do \
		MODEL_NAME=$$(echo "$${file//src\/hephaistus\/models\/Modelfile_}"); \
		$(CMD) ollama create $$MODEL_NAME -f "./$${file}"; \
	done