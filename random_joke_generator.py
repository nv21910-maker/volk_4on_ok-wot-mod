#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Random Joke Generator - Генератор случайных шуток
Использует внешние API для получения шуток на разных языках
Version: 1.0.0
Author: nv21910-maker
"""

import sys
import json
import time
import requests
from typing import Dict, List, Optional, Tuple
from enum import Enum
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


class JokeCategory(Enum):
    """Категории шуток"""
    GENERAL = "general"
    PROGRAMMING = "programming"
    KNOCK_KNOCK = "knock-knock"
    SPORTS = "sports"
    ANIMALS = "animals"
    RANDOM = "random"


class JokeAPI(Enum):
    """Поддерживаемые API для получения шуток"""
    JOKES_API = "https://v2.jokeapi.dev/joke/"
    OFFICIAL_JOKE_API = "https://official-joke-api.appspot.com/"
    RANDOM_JOKE_API = "https://api.jokes.one/jokes/"


@staticmethod
def validate_api_response(response_text: str) -> bool:
    """Проверить корректность ответа API"""
    try:
        json.loads(response_text)
        return True
    except json.JSONDecodeError:
        return False


class JokeGenerator:
    """Генератор шуток с использованием внешних API"""
    
    def __init__(self):
        self.timeout = 5  # Timeout для запросов (секунды)
        self.joke_history: List[Dict] = []
        self.favorite_jokes: List[Dict] = []
        self.max_history = 100
        
    def get_joke_from_jokes_api(self, category: str = "Any") -> Optional[Dict]:
        """
        Получить шутку из JokeAPI (v2.jokeapi.dev)
        Категории: Any, Misc, Programming, Knock-Knock, Religion, Political, Sport
        """
        try:
            url = f"https://v2.jokeapi.dev/joke/{category}?format=json"
            
            logger.info(f"📡 Получаем шутку из JokeAPI (категория: {category})...")
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            joke_dict = {
                "api": "JokeAPI",
                "category": data.get("category", "Unknown"),
                "type": data.get("type", "general"),
                "content": "",
                "setup": "",
                "delivery": "",
                "timestamp": time.time(),
                "language": "English"
            }
            
            if data["type"] == "twopart":
                joke_dict["setup"] = data.get("setup", "")
                joke_dict["delivery"] = data.get("delivery", "")
                joke_dict["content"] = f"{data.get('setup', '')}\n\n{data.get('delivery', '')}"
            else:
                joke_dict["content"] = data.get("joke", "")
            
            joke_dict["nsfw"] = data.get("nsfw", False)
            joke_dict["safe"] = data.get("safe", True)
            
            self._add_to_history(joke_dict)
            return joke_dict
            
        except requests.RequestException as e:
            logger.error(f"❌ Ошибка при получении шутки из JokeAPI: {e}")
            return None
    
    def get_joke_from_official_api(self) -> Optional[Dict]:
        """
        Получить шутку из Official Joke API
        Более простой API с классическими шутками
        """
        try:
            url = "https://official-joke-api.appspot.com/random_joke"
            
            logger.info("📡 Получаем шутку из Official Joke API...")
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            joke_dict = {
                "api": "Official Joke API",
                "category": data.get("type", "general"),
                "type": "twopart",
                "id": data.get("id", ""),
                "setup": data.get("setup", ""),
                "delivery": data.get("delivery", ""),
                "content": f"{data.get('setup', '')}\n\n{data.get('delivery', '')}",
                "timestamp": time.time(),
                "language": "English",
                "nsfw": False,
                "safe": True
            }
            
            self._add_to_history(joke_dict)
            return joke_dict
            
        except requests.RequestException as e:
            logger.error(f"❌ Ошибка при получении шутки из Official API: {e}")
            return None
    
    def get_random_joke(self) -> Optional[Dict]:
        """Получить случайную шутку с автоматическим выбором API"""
        apis = [
            ("JokeAPI", self.get_joke_from_jokes_api),
            ("Official API", self.get_joke_from_official_api)
        ]
        
        for api_name, api_func in apis:
            try:
                result = api_func() if api_name == "Official API" else api_func("Any")
                if result:
                    return result
            except Exception as e:
                logger.warning(f"⚠️  {api_name} недоступен, пытаемся следующий...")
        
        return None
    
    def get_programming_joke(self) -> Optional[Dict]:
        """Получить шутку про программирование"""
        return self.get_joke_from_jokes_api("Programming")
    
    def get_knock_knock_joke(self) -> Optional[Dict]:
        """Получить шутку 'Тук-тук'"""
        return self.get_joke_from_jokes_api("Knock-Knock")
    
    def get_multiple_jokes(self, count: int = 5) -> List[Dict]:
        """Получить несколько шуток"""
        jokes = []
        
        for i in range(count):
            logger.info(f"⏳ Получаем шутку {i+1}/{count}...")
            joke = self.get_random_joke()
            
            if joke:
                jokes.append(joke)
            
            if i < count - 1:
                time.sleep(1)  # Небольшая задержка между запросами
        
        return jokes
    
    def _add_to_history(self, joke: Dict):
        """Добавить шутку в историю"""
        self.joke_history.append(joke)
        
        # Сохраняем только последние N шуток
        if len(self.joke_history) > self.max_history:
            self.joke_history.pop(0)
    
    def add_to_favorites(self, joke: Dict):
        """Добавить шутку в избранное"""
        if joke not in self.favorite_jokes:
            self.favorite_jokes.append(joke)
            logger.info("⭐ Шутка добавлена в избранное!")
    
    def get_favorites(self) -> List[Dict]:
        """Получить избранные шутки"""
        return self.favorite_jokes
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """Получить историю шуток"""
        return self.joke_history[-limit:]
    
    def clear_history(self):
        """Очистить историю"""
        self.joke_history.clear()
        logger.info("🗑️  История очищена")
    
    def clear_favorites(self):
        """Очистить избранное"""
        self.favorite_jokes.clear()
        logger.info("🗑️  Избранное очищено")
    
    def export_jokes(self, jokes: List[Dict], filename: str = "jokes.json"):
        """Экспортировать шутки в JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(jokes, f, indent=4, ensure_ascii=False)
            logger.info(f"💾 Шутки экспортированы в {filename}")
        except Exception as e:
            logger.error(f"❌ Ошибка при экспорте: {e}")
    
    def export_favorites(self, filename: str = "favorite_jokes.json"):
        """Экспортировать избранные шутки"""
        self.export_jokes(self.favorite_jokes, filename)
    
    def export_history(self, filename: str = "joke_history.json"):
        """Экспортировать историю"""
        self.export_jokes(self.joke_history, filename)
    
    def print_joke(self, joke: Optional[Dict]):
        """Красиво вывести шутку"""
        if not joke:
            print("❌ Не удалось получить шутку\n")
            return
        
        print("╔════════════════════════════════════════════════════════════════╗")
        print(f"║ 😂 ШУТКА | {joke.get('api', 'Unknown API'):30} ║")
        print("╠════════════════════════════════════════════════════════════════╣")
        print(f"║ Категория: {joke.get('category', 'Unknown'):50} ║")
        
        if joke.get('setup'):
            print(f"║                                                              ║")
            print(f"║ {joke.get('setup', ''):60} ║")
            print(f"║                                                              ║")
            print(f"║ {joke.get('delivery', ''):60} ║")
        else:
            content = joke.get('content', '').replace('\n', ' ')
            # Разбиваем длинный текст на строки по 60 символов
            for line in self._wrap_text(content, 60):
                print(f"║ {line:60} ║")
        
        print("╚════════════════════════════════════════════════════════════════╝")
        print()
    
    @staticmethod
    def _wrap_text(text: str, width: int) -> List[str]:
        """Разбить текст на строки нужной ширины"""
        lines = []
        words = text.split()
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= width:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines if lines else [""]
    
    def print_statistics(self):
        """Вывести статистику"""
        print("\n╔════════════════════════════════════════════════════════════════╗")
        print("║             📊 СТАТИСТИКА ГЕНЕРАТОРА ШУТОК                     ║")
        print("╠════════════════════════════════════════════════════════════════╣")
        print(f"║ Всего получено шуток:       {len(self.joke_history):>5}                       ║")
        print(f"║ В избранном:                {len(self.favorite_jokes):>5}                       ║")
        print(f"║ История сохранена:         {'Да' if self.joke_history else 'Нет':>5}                       ║")
        
        if self.joke_history:
            categories = {}
            for joke in self.joke_history:
                cat = joke.get('category', 'Unknown')
                categories[cat] = categories.get(cat, 0) + 1
            
            print(f"║ Уникальные категории:       {len(categories):>5}                       ║")
            print("║                                                              ║")
            print("║ По категориям:                                              ║")
            for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"║   • {cat:30} - {count:>3} шуток                   ║")
        
        print("╚════════════════════════════════════════════════════════════════╝\n")


def interactive_mode():
    """Интерактивный режим"""
    generator = JokeGenerator()
    
    print("\n" + "="*66)
    print("🎭 ГЕНЕРАТОР СЛУЧАЙНЫХ ШУТОК v1.0")
    print("="*66)
    print("\nДоступные команды:")
    print("  1 - Получить случайную шутку")
    print("  2 - Получить шутку про программирование")
    print("  3 - Получить шутку 'Тук-тук'")
    print("  4 - Получить несколько шуток")
    print("  5 - Мои избранные шутки")
    print("  6 - История шуток")
    print("  7 - Статистика")
    print("  8 - Экспортировать избранное")
    print("  9 - Очистить историю")
    print("  0 - Выход\n")
    
    while True:
        try:
            choice = input("Выберите действие (0-9): ").strip()
            
            if choice == "0":
                print("\n👋 До свидания!\n")
                break
            
            elif choice == "1":
                print()
                joke = generator.get_random_joke()
                generator.print_joke(joke)
                if joke:
                    favorite = input("Добавить в избранное? (y/n): ").lower()
                    if favorite == 'y':
                        generator.add_to_favorites(joke)
            
            elif choice == "2":
                print()
                joke = generator.get_programming_joke()
                generator.print_joke(joke)
                if joke:
                    favorite = input("Добавить в избранное? (y/n): ").lower()
                    if favorite == 'y':
                        generator.add_to_favorites(joke)
            
            elif choice == "3":
                print()
                joke = generator.get_knock_knock_joke()
                generator.print_joke(joke)
                if joke:
                    favorite = input("Добавить в избранное? (y/n): ").lower()
                    if favorite == 'y':
                        generator.add_to_favorites(joke)
            
            elif choice == "4":
                try:
                    count = int(input("Сколько шуток получить? (1-10): "))
                    if 1 <= count <= 10:
                        print()
                        jokes = generator.get_multiple_jokes(count)
                        for i, joke in enumerate(jokes, 1):
                            print(f"\n--- Шутка {i}/{len(jokes)} ---")
                            generator.print_joke(joke)
                    else:
                        print("❌ Введите число от 1 до 10\n")
                except ValueError:
                    print("❌ Некорректное число\n")
            
            elif choice == "5":
                favorites = generator.get_favorites()
                if favorites:
                    print(f"\n⭐ ИЗБРАННОЕ ({len(favorites)} шуток):\n")
                    for i, joke in enumerate(favorites, 1):
                        print(f"--- Шутка {i} ---")
                        generator.print_joke(joke)
                else:
                    print("\n❌ Избранное пусто\n")
            
            elif choice == "6":
                history = generator.get_history(10)
                if history:
                    print(f"\n📜 ИСТОРИЯ ({len(history)} последних шуток):\n")
                    for i, joke in enumerate(history, 1):
                        print(f"--- Шутка {i} ---")
                        generator.print_joke(joke)
                else:
                    print("\n❌ История пуста\n")
            
            elif choice == "7":
                generator.print_statistics()
            
            elif choice == "8":
                generator.export_favorites()
                print()
            
            elif choice == "9":
                generator.clear_history()
                print()
            
            else:
                print("❌ Неизвестная команда\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 До свидания!\n")
            break
        except Exception as e:
            logger.error(f"❌ Ошибка: {e}\n")


def demo_mode():
    """Режим демонстрации"""
    print("\n" + "="*66)
    print("🎭 ГЕНЕРАТОР СЛУЧАЙНЫХ ШУТОК - ДЕМОНСТРАЦИЯ")
    print("="*66 + "\n")
    
    generator = JokeGenerator()
    
    # Получаем несколько шуток
    print("📡 Получаем шутки из различных источников...\n")
    
    print("1️⃣  СЛУЧАЙНАЯ ШУТКА:")
    joke1 = generator.get_random_joke()
    generator.print_joke(joke1)
    if joke1:
        generator.add_to_favorites(joke1)
    
    time.sleep(1)
    
    print("2️⃣  ШУТКА ПРО ПРОГРАММИРОВАНИЕ:")
    joke2 = generator.get_programming_joke()
    generator.print_joke(joke2)
    if joke2:
        generator.add_to_favorites(joke2)
    
    time.sleep(1)
    
    print("3️⃣  ШУТКА 'ТУК-ТУК':")
    joke3 = generator.get_knock_knock_joke()
    generator.print_joke(joke3)
    if joke3:
        generator.add_to_favorites(joke3)
    
    # Выводим статистику
    generator.print_statistics()
    
    # Экспортируем избранное
    print("💾 Экспортируем избранное...")
    generator.export_favorites()
    generator.export_history()
    
    print("✅ Демонстрация завершена!\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        try:
            interactive_mode()
        except KeyboardInterrupt:
            print("\n\n❌ Программа прервана")
            sys.exit(0)
    else:
        try:
            demo_mode()
        except KeyboardInterrupt:
            print("\n\n❌ Программа прервана")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Критическая ошибка: {e}", exc_info=True)
            sys.exit(1)
