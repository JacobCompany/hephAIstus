# Hephaestus - God of the Forge

`hephaestus` is a Python package that has a variety of different AI models to assist DevOps Engineers. All of these models run on your local
computer and do not get saved online at all. This will allow the user to safely and securely discuss any topic with the AI bot without any
potential data leak.

These models use `gpt4all` and `ollama`.

## Hephaestus' Forge

The first AI model is `forge` and it uses `gpt4all`. To use it, simply run the following commands in a Python terminal.

```python
from hephaestus import forge
forge()
```

This will then start a conversation with an AI bot. You can specify the AI model to use with the `model_version` parameter in `forge`. If no
model is specified, then it will use the default.

After the conversation is finished, the user can save the results to a text file.

## Hephaestus' Hammer

Alternatively, you can use `ollama` with `hammer`. To use it, simply run the following commands in a Python terminal.

```python
from hephaestus import hammer
hammer()
```

This will then start a conversation with an AI bot. You can specify the AI model to use with the `model_version` parameter in `forge`. If no
model is specified, then it will use the default.

To use one of the provided AI models (found in `src/hephaestus/models`), run `make create_models` and all relevant models will be
initialized.

After the conversation is finished, the user can save the results to a text file.