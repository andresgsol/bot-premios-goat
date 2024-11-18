# Bot Premios GOAT
Bot de Telegram que automatiza los premios GOAT (es una larga historia)

## Cómo ejectutarlo
```
pip install -r requirements.txt
python main.py
```
Esto ejecutara el bot en modo dev, es decir, usando `config_dev.py`. El modo de ejecución se controla con la variable de entorno `ENV`. Para ejecutarlo en modo prod (`config_prod.py`):
```
ENV=prod python main.py
```