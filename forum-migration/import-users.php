<?php
/**
 * Script Import Utenti in Flarum
 * Uso: php artisan tinker < import-users.php
 */

use Flarum\User\User;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

// Leggi CSV utenti
$csvFile = 'users.csv';
$users = array_map('str_getcsv', file($csvFile));
array_shift($users); // Rimuovi header

$imported = 0;
$skipped = 0;

foreach ($users as $row) {
    if (count($row) < 2) continue;
    
    $username = trim($row[0]);
    $email = trim($row[1]);
    
    // Verifica se utente esiste già
    if (User::where('username', $username)->exists()) {
        echo "⏭️  Saltato: $username (esiste già)\n";
        $skipped++;
        continue;
    }
    
    // Crea utente con password temporanea
    $tempPassword = Str::random(16);
    
    try {
        $user = User::create([
            'username' => $username,
            'email' => $email,
            'password' => Hash::make($tempPassword),
            'is_email_confirmed' => false,
            'created_at' => now(),
        ]);
        
        echo "✅ Importato: $username ($email)\n";
        $imported++;
        
        // TODO: Invia email di riattivazione
        // Mail::send('emails.activation', [...], function($m) use ($user) { ... });
        
    } catch (\Exception $e) {
        echo "❌ Errore: $username - {$e->getMessage()}\n";
        $skipped++;
    }
}

echo "\n📊 Risultati:\n";
echo "✅ Importati: $imported\n";
echo "⏭️  Saltati: $skipped\n";
echo "📧 Invia email di riattivazione agli utenti\n";
