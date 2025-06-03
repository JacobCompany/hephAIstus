.PHONY: ruff create_models

CMD:=poetry run

ruff:
	$(CMD) ruff check --fix src
	$(CMD) ruff format src

create_models:
	ollama create devops_engineer -f ./src/hephaestus/models/Modelfile_devops_engineer
	ollama rm codellama

	ollama create hephaestus -f ./src/hephaestus/models/Modelfile_hephaestus
	ollama rm llama3.2