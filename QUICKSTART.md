# 🚀 Quick Start Guide - Volk_4on_ok WoT Toolkit

## ⚡ 5-Минутная установка

### Windows
```bash
git clone https://github.com/nv21910-maker/volk_4on_ok-wot-mod.git
cd volk_4on_ok-wot-mod
install.bat
volk_toolkit.bat
```

### Mac/Linux
```bash
git clone https://github.com/nv21910-maker/volk_4on_ok-wot-mod.git
cd volk_4on_ok-wot-mod
chmod +x install.sh
./install.sh
./volk_toolkit
```

---

## 🎮 Первый запуск

### Режим демонстрации (с примерами)
```bash
python3 volk_wot_toolkit.py
```
Вы увидите:
- 📊 Dashboard с примерами статистики
- 🎯 Battle Analyzer
- 🎖️ Tactical Helper
- 📈 Stats Tracker
- 🎨 UI Customizer

### Интерактивный режим (меню)
```bash
python3 volk_wot_toolkit.py interactive
```

Меню опций:
```
1 - Battle Analyzer     (Анализ боёв)
2 - Tactical Helper     (Тактические советы)
3 - Stats Tracker       (Отслеживание статистики)
4 - UI Customizer       (Кастомизация интерфейса)
5 - Add Sample Battle   (Добавить пример боя)
6 - View Dashboard      (Просмотр дашборда)
7 - Export Statistics   (Экспортировать статистику)
0 - Exit                (Выход)
```

---

## 📊 Основные команды

### Запустить WoT Toolkit
```bash
python3 volk_wot_toolkit.py           # Демо режим
python3 volk_wot_toolkit.py interactive # Интерактивное меню
```

### Запустить WoT Mod
```bash
python3 volk_4on_ok_mod.py
```

### Запустить Генератор шуток
```bash
python3 random_joke_generator.py        # Демо
python3 random_joke_generator.py interactive # Меню
```

---

## 📈 Что даёт каждый модуль

### 🎯 Battle Analyzer
- ✅ Анализ всех боёв
- ✅ Лучший и худший бой
- ✅ Последние 3 боя
- ✅ Экспорт статистики в JSON

### 🎖️ Tactical Helper
- ✅ Советы для каждой карты
- ✅ Как закультировать врага
- ✅ Ключевые позиции
- ✅ Стратегии по классам танков

### 📈 Stats Tracker
- ✅ Рейтинг производительности
- ✅ Тренд 7-дневного винрейта
- ✅ Рекомендации по улучшению
- ✅ Аналитика по чувствительности

### 🎨 UI Customizer
- ✅ 3 встроенные темы
- ✅ Volk Dark Pro (рекомендуется)
- ✅ Volk Light
- ✅ Competitive Edition

---

## 💡 Полезные советы

### Экспортировать стати��тику
В интерактивном режиме выберите опцию `7` для экспорта в JSON:
```bash
💾 Exported to wot_stats.json
```

### Добавить собственный бой
Отредактируйте `volk_wot_toolkit.py` в методе `add_sample_battles()` и добавьте свои данные боя.

### Изменить тему интерфейса
В интерактивном режиме выберите опцию `4` и смените тему.

### Получить советы для карты
В опции `2` (Tactical Helper) вы найдёте стратегию для каждой карты.

---

## 🔧 Требования

- **Python 3.8+** (проверка: `python3 --version`)
- **pip** (обычно идёт с Python)
- **5 MB** свободного места
- **Интернет** только для API (опционально)

---

## 🆘 Проблемы?

### Python не найден
```bash
# Проверьте установку
python3 --version

# Если не работает, переустановите Python с python.org
```

### Ошибка при импорте модулей
```bash
# Переустановите зависимости
pip install -r requirements.txt
```

### Медленная работа
```bash
# Дождитесь загрузки первого раза (кеширование данных)
# Следующие запуски будут быстрее
```

---

## 📞 Контакты

**GitHub:** [@nv21910-maker](https://github.com/nv21910-maker)

---

**🎮 Готовы к игре? Запустите toolkit и начните отслеживать свою статистику!**
