.PHONY: ruff create_models

ruff:
	ruff check --fix src
	ruff format src

create_models:
	ollama create devops_engineer -f ./src/hephaestus/models/Modelfile_devops_engineer
	ollama rm codellama