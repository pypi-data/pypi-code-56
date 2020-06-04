from django.conf import settings
from nocton.tools.console import print_f
from nocton.setup.settings import load_nocton


def watch_folders():
    SETTINGS = load_nocton()

    # Tenta encontrar uma chave "wacth" nas configurações do projeto
    try:    
        if SETTINGS:
            WATCHERS = SETTINGS["watch"]

            for path in WATCHERS:
                # Importa os módulos listados
                module = __import__(path)

    except ModuleNotFoundError as error:
        # Printa o erro
        print_f(f"Módulo não encontrado: {error}")
        # pass