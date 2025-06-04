.PHONY: ruff create_models

CMD:=poetry run
MODEL_DIR:=src/hephaestus/models

ruff:
	@$(CMD) ruff check --fix src
	@$(CMD) ruff format src

create_models: $(MODEL_DIR)/Modelfile_*
	@for file in $^ ; do \
		MODEL_NAME=$$(echo "$${file//src\/hephaestus\/models\/Modelfile_}"); \
		$(CMD) ollama create $$MODEL_NAME -f "./$${file}"; \
	done