import importlib.metadata


try:
    _pkg_version = importlib.metadata.version('anthropic')
except importlib.metadata.PackageNotFoundError:
    _pkg_version = 'development'

ANTHROPIC_CLIENT_VERSION = "anthropic-python/" + _pkg_version
ANTHROPIC_VERSION = "2023-01-01"

HUMAN_PROMPT = '\n\nHuman:'

AI_PROMPT = '\n\nAssistant:'
