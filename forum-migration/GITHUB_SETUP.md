# 🚀 Setup GitHub Pages - Guida Rapida

## 📋 Prerequisiti

- Account GitHub
- Repository creato
- Git installato

---

## ⚡ Step 1: Crea Repository

1. Vai su: https://github.com/new
2. Nome: `forum-laura-pausini` (o quello che preferisci)
3. Descrizione: "Migrazione Forum Laura Pausini - Demo Flarum"
4. Seleziona: Public
5. Clicca: "Create repository"

---

## 📦 Step 2: Push su GitHub

```bash
# Naviga nella cartella
cd forum-migration

# Inizializza git (se non già fatto)
git init

# Aggiungi tutti i file
git add .

# Commit
git commit -m "Initial commit - Forum migration demo"

# Aggiungi remote
git remote add origin https://github.com/TUO_USERNAME/forum-laura-pausini.git

# Push
git branch -M main
git push -u origin main
```

---

## 🌐 Step 3: Abilita GitHub Pages

1. Vai su: https://github.com/TUO_USERNAME/forum-laura-pausini
2. Clicca: Settings
3. Vai a: Pages (nel menu a sinistra)
4. Source: Seleziona "Deploy from a branch"
5. Branch: Seleziona "gh-pages"
6. Clicca: Save

---

## ✅ Step 4: Verifica Deploy

Dopo 1-2 minuti, il sito sarà disponibile a:
```
https://TUO_USERNAME.github.io/forum-laura-pausini/
```

Oppure se hai un dominio personalizzato:
```
https://forum-laura-pausini.github.io/
```

---

## 🔄 Step 5: Deploy Automatico

Il file `.github/workflows/deploy.yml` fa il deploy automatico ogni volta che fai push su main.

Ogni volta che modifichi i file:
```bash
git add .
git commit -m "Update demo"
git push
```

Il sito si aggiorna automaticamente! ✨

---

## 📝 Modifica la Demo

Per modificare la demo:

1. Modifica: `forum-migration/public/index.html`
2. Salva il file
3. Esegui:
```bash
git add .
git commit -m "Update demo content"
git push
```

4. Aspetta 1-2 minuti
5. Ricarica il sito

---

## 🎯 URL Finali

**Demo Forum:**
```
https://TUO_USERNAME.github.io/forum-laura-pausini/
```

**Repository:**
```
https://github.com/TUO_USERNAME/forum-laura-pausini
```

**Condividi con il cliente:**
```
"Ecco la preview del nuovo forum: https://TUO_USERNAME.github.io/forum-laura-pausini/"
```

---

## 🆘 Troubleshooting

### "Il sito non si vede"
- Aspetta 2-3 minuti dopo il push
- Ricarica la pagina (Ctrl+F5)
- Verifica che il branch sia "gh-pages" nelle impostazioni

### "Errore 404"
- Verifica che il file sia in: `forum-migration/public/index.html`
- Verifica che il workflow sia stato eseguito (vai su Actions)

### "Il workflow fallisce"
- Vai su: Repository → Actions
- Clicca sul workflow fallito
- Leggi l'errore
- Correggi e fai push di nuovo

---

## 💡 Bonus: Dominio Personalizzato

Se vuoi usare un dominio personalizzato (es: forum.tuodominio.it):

1. Vai su: Settings → Pages
2. Custom domain: Inserisci `forum.tuodominio.it`
3. Vai al tuo provider DNS
4. Aggiungi CNAME record:
   ```
   forum.tuodominio.it → TUO_USERNAME.github.io
   ```
5. Aspetta 24h per la propagazione DNS

---

## 📊 Statistiche

Puoi vedere le statistiche del sito su:
```
https://github.com/TUO_USERNAME/forum-laura-pausini/settings/pages
```

---

## 🎉 Fatto!

Il tuo forum è online e condivisibile! 🚀

**Condividi il link con il cliente:**
```
"Ecco la preview del nuovo forum: https://TUO_USERNAME.github.io/forum-laura-pausini/"
```

---

## 📞 Supporto GitHub Pages

- Documentazione: https://docs.github.com/en/pages
- Help: https://github.com/contact

---

**Buona fortuna! 💪**
