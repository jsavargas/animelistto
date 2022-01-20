import os


def get_env(name, message, cast=str):
	if name in os.environ:
		return os.environ[name].strip()
	else:
		return message



PLEXDL_X_PLEX_TOKEN = get_env('PLEXDL_X_PLEX_TOKEN', '')


