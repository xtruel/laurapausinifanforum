# 🌐 Deploy su Register - Guida Completa

## 📋 Prerequisiti

- Dominio acquistato su Register
- Hosting PHP 8.0+ con MySQL
- Accesso SSH al server
- Composer installato sul server

---

## 🚀 Step 1: Preparazione Dominio

### 1.1 Acquista dominio su Register
- Vai su: https://www.register.it/
- Cerca dominio (es: `laurapausini-forum.it`)
- Acquista hosting + dominio

### 1.2 Configura DNS
Nel pannello Register:
```
A Record: [IP server]
CNAME: www → [dominio principale]
```

---

## 🔧 Step 2: Setup Server

### 2.1 Connettiti via SSH
```bash
ssh user@tuodominio.it
```

### 2.2 Naviga alla cartella pubblica
```bash
cd /home/user/public_html
# oppure
cd /var/www/html
```

### 2.3 Installa Flarum
```bash
composer create-project flarum/flarum . --stability=beta
```

### 2.4 Configura permessi
```bash
chmod -R 755 storage
chmod -R 755 public
chown -R www-data:www-data .
```

---

## 📝 Step 3: Configurazione Database

### 3.1 Crea database MySQL
Nel pannello Register (cPanel/Plesk):
- Crea nuovo database
- Crea utente MySQL
- Assegna permessi

**Salva:**
- Nome database: `forum_db`
- Utente: `forum_user`
- Password: `[password sicura]`
- Host: `localhost`

### 3.2 Configura .env
```bash
nano .env
```

Modifica:
```env
APP_DEBUG=false
APP_URL=https://tuodominio.it

DB_DRIVER=mysql
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=forum_db
DB_USERNAME=forum_user
DB_PASSWORD=password_sicura

MAIL_DRIVER=smtp
MAIL_HOST=smtp.register.it
MAIL_PORT=587
MAIL_USERNAME=tua_email@tuodominio.it
MAIL_PASSWORD=password_email
MAIL_FROM_ADDRESS=noreply@tuodominio.it
```

---

## 🗄️ Step 4: Setup Database

### 4.1 Esegui migrazioni
```bash
php artisan migrate
```

### 4.2 Crea utente admin
```bash
php artisan tinker
```

Dentro tinker:
```php
$user = new \Flarum\User\User();
$user->username = 'admin';
$user->email = 'admin@tuodominio.it';
$user->password = bcrypt('password_sicura');
$user->is_email_confirmed = true;
$user->save();

$user->groups()->attach(1); // Admin group
```

---

## 📥 Step 5: Import Dati

### 5.1 Upload forum_data.json e users.csv
```bash
scp forum_data.json user@tuodominio.it:/home/user/public_html/
scp users.csv user@tuodominio.it:/home/user/public_html/
```

### 5.2 Import utenti
```bash
php artisan tinker < import-users.php
```

### 5.3 Import thread/post
Crea script `import-threads.php`:
```php
<?php
use Flarum\Discussion\Discussion;
use Flarum\Post\Post;
use Flarum\User\User;

$data = json_decode(file_get_contents('forum_data.json'), true);

foreach ($data['threads'] as $threadData) {
    $discussion = Discussion::create([
        'title' => $threadData['title'],
        'user_id' => 1, // Admin
        'created_at' => now(),
    ]);
    
    foreach ($threadData['posts'] ?? [] as $postData) {
        Post::create([
            'discussion_id' => $discussion->id,
            'user_id' => 1,
            'content' => $postData['content'],
            'created_at' => now(),
        ]);
    }
}
```

Esegui:
```bash
php artisan tinker < import-threads.php
```

---

## 🔒 Step 6: Sicurezza

### 6.1 Abilita HTTPS
Nel pannello Register:
- Installa certificato SSL (Let's Encrypt gratuito)
- Forza HTTPS in .env

### 6.2 Configura firewall
```bash
# Blocca accesso a file sensibili
nano .htaccess
```

Aggiungi:
```apache
<FilesMatch "\.env|\.git|composer\.json|composer\.lock">
    Order allow,deny
    Deny from all
</FilesMatch>
```

### 6.3 Backup automatici
Nel pannello Register:
- Abilita backup giornalieri
- Salva su cloud esterno

---

## 🚀 Step 7: Ottimizzazione

### 7.1 Cache
```bash
php artisan config:cache
php artisan route:cache
php artisan view:cache
```

### 7.2 Compressione
Nel .htaccess:
```apache
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
</IfModule>
```

### 7.3 CDN (opzionale)
Configura Cloudflare per:
- Cache statico
- DDoS protection
- Compressione

---

## ✅ Checklist Pre-Launch

- [ ] Dominio punta al server
- [ ] SSL certificato installato
- [ ] Database creato e configurato
- [ ] Flarum installato
- [ ] Utenti importati
- [ ] Thread/post importati
- [ ] Admin account creato
- [ ] Email configurata
- [ ] Backup abilitati
- [ ] Test accesso forum
- [ ] Test registrazione utente
- [ ] Test creazione discussione

---

## 🧪 Test Pre-Launch

### Test 1: Accesso
```bash
curl -I https://tuodominio.it
# Deve ritornare 200 OK
```

### Test 2: Database
```bash
php artisan tinker
>>> DB::connection()->getPdo();
# Deve connettersi senza errori
```

### Test 3: Email
```bash
php artisan tinker
>>> Mail::raw('Test', function($m) { $m->to('tua_email@gmail.com'); });
# Controlla inbox
```

---

## 📊 Monitoraggio Post-Launch

### Configura monitoring
```bash
# Log errori
tail -f storage/logs/laravel.log

# Monitoraggio performance
php artisan horizon:monitor
```

### Backup giornalieri
```bash
# Backup database
mysqldump -u forum_user -p forum_db > backup_$(date +%Y%m%d).sql

# Backup file
tar -czf backup_$(date +%Y%m%d).tar.gz .
```

---

## 🆘 Troubleshooting

### "500 Internal Server Error"
```bash
# Controlla log
tail -f storage/logs/laravel.log

# Verifica permessi
chmod -R 755 storage
chmod -R 755 bootstrap/cache
```

### "Database connection refused"
```bash
# Verifica credenziali .env
# Verifica MySQL running
mysql -u forum_user -p -h localhost forum_db

# Verifica firewall
sudo ufw allow 3306
```

### "Email non inviata"
```bash
# Verifica SMTP config in .env
# Test SMTP
telnet smtp.register.it 587
```

---

## 📞 Supporto Register

- **Chat:** https://www.register.it/supporto
- **Email:** support@register.it
- **Telefono:** +39 06 9999 0001

---

## 🎉 Fatto!

Il forum è live su: `https://tuodominio.it`

**Prossimi step:**
1. Comunica il cambio agli utenti
2. Monitora performance
3. Raccogli feedback
4. Migliora in base a feedback

---

**Buona fortuna! 🚀**
