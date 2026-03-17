#!/bin/bash
# Setup Flarum - Script di installazione

echo "🚀 Installazione Flarum..."

# Verifica prerequisiti
if ! command -v composer &> /dev/null; then
    echo "❌ Composer non trovato. Installa da: https://getcomposer.org"
    exit 1
fi

if ! command -v php &> /dev/null; then
    echo "❌ PHP non trovato. Installa PHP 8.0+"
    exit 1
fi

# Crea directory progetto
mkdir -p flarum-forum
cd flarum-forum

# Installa Flarum
echo "📦 Scaricando Flarum..."
composer create-project flarum/flarum . --stability=beta

# Copia config
echo "⚙️ Configurando..."
cp .env.example .env

# Genera app key
php artisan key:generate

# Pubblica assets
php artisan vendor:publish --tag=public

echo "✅ Flarum installato!"
echo ""
echo "📝 Prossimi step:"
echo "1. Configura .env con database"
echo "2. Esegui: php artisan migrate"
echo "3. Esegui: php artisan tinker (per import utenti)"
echo "4. Avvia: php artisan serve"
echo ""
echo "🌐 Accedi a: http://localhost:8000"
