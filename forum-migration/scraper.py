#!/usr/bin/env python3
"""
Forum Scraper - Estrae dati da ForumCommunity
Estrae: categorie, thread, post, utenti
Output: JSON strutturato + CSV utenti
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
from datetime import datetime
from urllib.parse import urljoin
import re

BASE_URL = "https://laurapausinifanforum.forumcommunity.net/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

class ForumScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.data = {
            "categories": [],
            "threads": [],
            "posts": [],
            "users": set()
        }
        
    def get_soup(self, url):
        """Fetch e parse HTML"""
        try:
            res = self.session.get(url, timeout=10)
            res.encoding = 'utf-8'
            return BeautifulSoup(res.text, "html.parser")
        except Exception as e:
            print(f"❌ Errore fetch {url}: {e}")
            return None
    
    def extract_users_from_page(self, soup):
        """Estrae nomi utenti dalla pagina"""
        if not soup:
            return
        
        # Cerca pattern: "Autore: username" o simili
        for text in soup.stripped_strings:
            # Cerca pattern di username (semplice)
            if len(text) > 2 and len(text) < 30:
                if not any(char in text for char in [':', '?', '!', '.']):
                    if text[0].isupper():
                        self.data["users"].add(text)
    
    def scrape_homepage(self):
        """Scrape homepage per categorie e thread recenti"""
        print("📍 Scraping homepage...")
        soup = self.get_soup(self.base_url)
        
        if not soup:
            return
        
        # Estrai discussioni recenti
        discussions = soup.find_all('a', href=re.compile(r'topic|thread'))
        
        for link in discussions[:20]:  # Limita a 20 per demo
            title = link.get_text(strip=True)
            href = link.get('href', '')
            
            if title and len(title) > 3:
                thread_url = urljoin(self.base_url, href)
                self.data["threads"].append({
                    "title": title,
                    "url": thread_url,
                    "scraped_at": datetime.now().isoformat()
                })
                print(f"  ✓ Thread: {title[:50]}")
        
        # Estrai utenti dalla homepage
        self.extract_users_from_page(soup)
        time.sleep(1)
    
    def scrape_thread(self, thread_url):
        """Scrape singolo thread per post e utenti"""
        print(f"  📄 Scraping thread...")
        soup = self.get_soup(thread_url)
        
        if not soup:
            return
        
        # Estrai post (selettori generici per ForumCommunity)
        posts = soup.find_all(['div', 'article'], class_=re.compile(r'post|message|comment'))
        
        for post in posts[:10]:  # Limita a 10 post per thread
            author_elem = post.find(['span', 'div'], class_=re.compile(r'author|user|nick'))
            content_elem = post.find(['div', 'p'], class_=re.compile(r'content|text|body'))
            
            author = author_elem.get_text(strip=True) if author_elem else "Anonimo"
            content = content_elem.get_text(strip=True) if content_elem else ""
            
            if content:
                self.data["posts"].append({
                    "author": author,
                    "content": content[:200],  # Limita a 200 char
                    "thread_url": thread_url
                })
                self.data["users"].add(author)
        
        # Estrai utenti dalla pagina
        self.extract_users_from_page(soup)
        time.sleep(1)
    
    def run(self):
        """Esegui scraping completo"""
        print("🚀 Inizio scraping forum...\n")
        
        self.scrape_homepage()
        
        # Scrape alcuni thread
        for thread in self.data["threads"][:5]:
            self.scrape_thread(thread["url"])
        
        print(f"\n✅ Scraping completato!")
        print(f"   Thread trovati: {len(self.data['threads'])}")
        print(f"   Post trovati: {len(self.data['posts'])}")
        print(f"   Utenti trovati: {len(self.data['users'])}")
        
        return self.data
    
    def save_json(self, filename="forum_data.json"):
        """Salva dati in JSON"""
        output = {
            "threads": self.data["threads"],
            "posts": self.data["posts"],
            "users": list(self.data["users"]),
            "exported_at": datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Dati salvati in: {filename}")
    
    def save_users_csv(self, filename="users.csv"):
        """Salva utenti in CSV per import"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'email', 'created_at', 'status'])
            
            for i, user in enumerate(sorted(self.data["users"]), 1):
                writer.writerow([
                    user,
                    f"{user.lower()}@forum-migrato.local",
                    datetime.now().isoformat(),
                    "pending_activation"
                ])
        
        print(f"💾 Utenti salvati in: {filename}")

if __name__ == "__main__":
    scraper = ForumScraper(BASE_URL)
    scraper.run()
    scraper.save_json()
    scraper.save_users_csv()
    print("\n✨ Pronto per import!")
