import importlib.metadata

try:
    _pkg_version = importlib.metadata.version('anthropic')
except importlib.metadata.PackageNotFoundError:
    _pkg_version = 'development'

ANTHROPIC_CLIENT_VERSION = "anthropic-python/" + _pkg_version

HUMAN_PROMPT = '\n\nHuman:'

AI_PROMPT = '\n\nAssistant:'
