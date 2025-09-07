#!/bin/bash
# ====================================================
# Script pour lancer n8n avec Docker
#
# Utilisation :
#   1. Donner les permissions d’exécution :
#        chmod +x start_n8n.sh
#   2. Lancer le script :
#        ./start_n8n.sh
#
# Accéder ensuite à l’interface n8n :
#   http://localhost:5678
# ====================================================

docker run -it --rm \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -v ~/Desktop/projects/bot-chatwoot-rebrand:/data \
  n8nio/n8n
