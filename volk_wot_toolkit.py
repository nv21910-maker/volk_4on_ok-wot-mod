#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Volk_4on_ok WoT Toolkit - Полный комплекс инструментов для World of Tanks
All-in-One Solution: Battle Analyzer, Tactical Helper, Stats Tracker, UI Customizer
Version: 2.0.0
Author: nv21910-maker
Style: volk_4on_ok
"""

import sys
import json
import time
import os
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# ===== CONSTANTS =====
VOLK_STYLE = """
╔════════════════════════════════════════════════════════════════════════════╗
║                    🎮 VOLK_4ON_OK WOT TOOLKIT v2.0 🎮                     ║
║         Professional All-in-One Solution for World of Tanks Players       ║
╚════════════════════════════════════════════════════════════════════════════╝
"""


class VehicleTier(Enum):
    """Уровни танков"""
    TIER_I = 1
    TIER_II = 2
    TIER_III = 3
    TIER_IV = 4
    TIER_V = 5
    TIER_VI = 6
    TIER_VII = 7
    TIER_VIII = 8
    TIER_IX = 9
    TIER_X = 10


class VehicleClass(Enum):
    """Классы танков"""
    LIGHT_TANK = "light_tank"
    MEDIUM_TANK = "medium_tank"
    HEAVY_TANK = "heavy_tank"
    TD = "tank_destroyer"
    SPG = "spg"


class BattleResult(Enum):
    """Результаты боя"""
    WIN = "win"
    LOSS = "loss"
    DRAW = "draw"


@dataclass
class Vehicle:
    """Данные танка"""
    name: str
    vehicle_id: int
    tier: VehicleTier
    vehicle_class: VehicleClass
    nation: str
    hp: int
    max_hp: int
    gun_damage: int
    penetration: int
    reload_time: float
    armor_front: int
    armor_side: int
    armor_rear: int
    
    def get_armor_avg(self) -> float:
        """Средняя броня"""
        return (self.armor_front + self.armor_side + self.armor_rear) / 3


@dataclass
class BattleData:
    """Данные одного боя"""
    battle_id: int
    player_name: str
    vehicle: Vehicle
    battle_result: BattleResult
    damage_dealt: int
    damage_received: int
    kills: int
    shots_hit: int
    shots_fired: int
    distance_traveled: float
    battle_duration: int  # в секундах
    credits_earned: int
    experience_earned: int
    timestamp: float
    map_name: str
    battle_type: str  # Random, Ranked, Stronghold etc
    team_damage: int = 0
    
    def get_accuracy(self) -> float:
        """Точность"""
        if self.shots_fired == 0:
            return 0.0
        return (self.shots_hit / self.shots_fired) * 100
    
    def get_avg_damage(self) -> float:
        """Средний урон"""
        if self.battle_duration == 0:
            return 0.0
        minutes = self.battle_duration / 60
        return self.damage_dealt / minutes if minutes > 0 else 0.0
    
    def get_efficiency_rating(self) -> float:
        """Рейтинг эффективности (0-100)"""
        accuracy = self.get_accuracy()
        kills_ratio = (self.kills / max(self.damage_received / 100, 1)) * 100
        survivability = 100 if self.damage_received == 0 else (self.vehicle.max_hp - self.damage_received) / self.vehicle.max_hp * 100
        
        rating = (accuracy * 0.3 + min(kills_ratio, 100) * 0.4 + max(survivability, 0) * 0.3)
        return min(rating, 100)


class BattleAnalyzer:
    """Анализатор боёв с полной статистикой"""
    
    def __init__(self):
        self.battles: List[BattleData] = []
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Загрузить конфигурацию"""
        return {
            "auto_save": True,
            "save_interval": 10,  # каждые 10 боёв
            "detailed_logs": True,
            "performance_tracking": True,
            "weekly_reports": True
        }
    
    def add_battle(self, battle: BattleData):
        """Добавить бой в историю"""
        self.battles.append(battle)
        logger.info(f"✅ Бой #{battle.battle_id} добавлен | Результат: {battle.battle_result.value.upper()}")
    
    def get_total_stats(self) -> Dict:
        """Получить общую статистику"""
        if not self.battles:
            return {}
        
        total_battles = len(self.battles)
        wins = len([b for b in self.battles if b.battle_result == BattleResult.WIN])
        losses = len([b for b in self.battles if b.battle_result == BattleResult.LOSS])
        draws = len([b for b in self.battles if b.battle_result == BattleResult.DRAW])
        
        total_damage = sum(b.damage_dealt for b in self.battles)
        total_kills = sum(b.kills for b in self.battles)
        total_shots = sum(b.shots_fired for b in self.battles)
        total_hits = sum(b.shots_hit for b in self.battles)
        total_credits = sum(b.credits_earned for b in self.battles)
        total_xp = sum(b.experience_earned for b in self.battles)
        
        avg_damage = total_damage / total_battles
        avg_kills = total_kills / total_battles
        win_rate = (wins / total_battles) * 100
        accuracy = (total_hits / total_shots * 100) if total_shots > 0 else 0
        
        return {
            "total_battles": total_battles,
            "wins": wins,
            "losses": losses,
            "draws": draws,
            "win_rate": win_rate,
            "total_damage": total_damage,
            "avg_damage": avg_damage,
            "total_kills": total_kills,
            "avg_kills": avg_kills,
            "accuracy": accuracy,
            "total_credits": total_credits,
            "total_xp": total_xp,
            "avg_credits_per_battle": total_credits / total_battles,
            "avg_xp_per_battle": total_xp / total_battles
        }
    
    def get_vehicle_stats(self, vehicle_name: str) -> Dict:
        """Статистика по конкретному танку"""
        vehicle_battles = [b for b in self.battles if b.vehicle.name == vehicle_name]
        
        if not vehicle_battles:
            return {}
        
        wins = len([b for b in vehicle_battles if b.battle_result == BattleResult.WIN])
        total = len(vehicle_battles)
        
        return {
            "vehicle": vehicle_name,
            "battles": total,
            "wins": wins,
            "win_rate": (wins / total) * 100,
            "avg_damage": sum(b.damage_dealt for b in vehicle_battles) / total,
            "avg_kills": sum(b.kills for b in vehicle_battles) / total,
            "total_credits": sum(b.credits_earned for b in vehicle_battles),
            "total_xp": sum(b.experience_earned for b in vehicle_battles)
        }
    
    def get_best_battle(self) -> Optional[BattleData]:
        """Лучший бой по урону"""
        return max(self.battles, key=lambda b: b.damage_dealt) if self.battles else None
    
    def get_worst_battle(self) -> Optional[BattleData]:
        """Худший бой по урону"""
        return min(self.battles, key=lambda b: b.damage_dealt) if self.battles else None
    
    def get_recent_battles(self, count: int = 10) -> List[BattleData]:
        """Последние N боёв"""
        return self.battles[-count:]
    
    def export_stats(self, filename: str = "wot_stats.json"):
        """Экспортировать статистику"""
        stats = {
            "total_stats": self.get_total_stats(),
            "recent_battles": [asdict(b) for b in self.get_recent_battles(20)],
            "export_time": datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=4, ensure_ascii=False, default=str)
        
        logger.info(f"💾 Статистика экспортирована в {filename}")


class TacticalHelper:
    """Помощник по тактике и позициям"""
    
    def __init__(self):
        self.map_tactics = self._load_map_tactics()
        self.vehicle_counters = self._load_counters()
        
    def _load_map_tactics(self) -> Dict:
        """Загрузить тактики карт"""
        return {
            "Prokhorovka": {
                "description": "Открытая карта с холмами",
                "tactics": [
                    "🎯 Занимайте высоты для лучшего обзора",
                    "🎯 Используйте холмы для защиты корпуса",
                    "🎯 Избегайте открытых полей",
                    "🎯 Работайте в группе с союзниками"
                ],
                "key_positions": ["North Hill", "South Hill", "Central Valley"]
            },
            "Ensk": {
                "description": "Городская карта со зданиями",
                "tactics": [
                    "🎯 Используйте здания для укрытия",
                    "🎯 Занимайте узкие улицы с союзниками",
                    "🎯 Будьте осторожны с фланговыми атаками",
                    "🎯 Контролируйте главные артерии города"
                ],
                "key_positions": ["Central Square", "North District", "South District"]
            },
            "Lakeville": {
                "description": "Смешанная карта с лесом и открытой местностью",
                "tactics": [
                    "🎯 Разделитесь между лесом и открытой местностью",
                    "🎯 Лес = укрытие для средних и лёгких танков",
                    "🎯 Холмы = преимущество для ПТ-САУ",
                    "🎯 Контролируйте центр карты"
                ],
                "key_positions": ["Lake", "Forest", "Hills"]
            }
        }
    
    def _load_counters(self) -> Dict:
        """Загрузить контр-стратегии"""
        return {
            "Heavy_Tank": {
                "counter_to": ["Medium Tank", "Tank Destroyer"],
                "vulnerable_to": ["SPG Artillery", "Other Heavy Tanks"],
                "tactic": "Занимайте позиции на холмах, используйте броню в своих интересах"
            },
            "Medium_Tank": {
                "counter_to": ["Light Tank", "SPG"],
                "vulnerable_to": ["Tank Destroyer", "Heavy Tank"],
                "tactic": "Фланкируйте врагов, поддерживайте союзников"
            },
            "Light_Tank": {
                "counter_to": ["Tank Destroyer", "SPG"],
                "vulnerable_to": ["Medium Tank", "Heavy Tank"],
                "tactic": "Разведка, засады, избегайте прямых боёв"
            },
            "TD": {
                "counter_to": ["Heavy Tank", "Medium Tank"],
                "vulnerable_to": ["Light Tank", "SPG"],
                "tactic": "Используйте камуфляж, занимайте позиции с хорошей видимостью"
            },
            "SPG": {
                "counter_to": ["Light Tank", "TD"],
                "vulnerable_to": ["Быстрые танки в упор"],
                "tactic": "Укройтесь позади товарищей, наносите урон издалека"
            }
        }
    
    def get_map_tips(self, map_name: str) -> Dict:
        """Получить советы для карты"""
        return self.map_tactics.get(map_name, {})
    
    def get_class_counter_tips(self, vehicle_class: str) -> Dict:
        """Получить советы против класса"""
        return self.vehicle_counters.get(vehicle_class, {})


class StatsTracker:
    """Трекер статистики с аналитикой"""
    
    def __init__(self, analyzer: BattleAnalyzer):
        self.analyzer = analyzer
        self.weekly_stats = {}
        self.monthly_stats = {}
        
    def get_winrate_trend(self, days: int = 7) -> Dict:
        """Тренд винрейта за N дней"""
        if not self.analyzer.battles:
            return {}
        
        recent_battles = self.analyzer.battles[-50:] if len(self.analyzer.battles) > 50 else self.analyzer.battles
        
        trend = {
            "period_days": days,
            "battles_count": len(recent_battles),
            "current_winrate": self._calculate_winrate(recent_battles),
            "trend": "📈 Rising" if len(recent_battles) > 20 else "➡️ Stable"
        }
        
        return trend
    
    def get_performance_rating(self) -> str:
        """Общий рейтинг производительности"""
        if not self.analyzer.battles:
            return "No Data"
        
        avg_damage = sum(b.damage_dealt for b in self.analyzer.battles) / len(self.analyzer.battles)
        accuracy = sum(b.get_accuracy() for b in self.analyzer.battles) / len(self.analyzer.battles)
        winrate = (len([b for b in self.analyzer.battles if b.battle_result == BattleResult.WIN]) / len(self.analyzer.battles)) * 100
        
        score = (avg_damage / 100) * 0.3 + accuracy * 0.3 + winrate * 0.4
        
        if score >= 80:
            return "⭐⭐⭐⭐⭐ Pro Player"
        elif score >= 60:
            return "⭐⭐⭐⭐ Advanced"
        elif score >= 40:
            return "⭐⭐⭐ Intermediate"
        elif score >= 20:
            return "⭐⭐ Beginner"
        else:
            return "⭐ New Player"
    
    def get_improvement_suggestions(self) -> List[str]:
        """Рекомендации по улучшению"""
        suggestions = []
        
        if not self.analyzer.battles:
            return suggestions
        
        avg_accuracy = sum(b.get_accuracy() for b in self.analyzer.battles) / len(self.analyzer.battles)
        if avg_accuracy < 50:
            suggestions.append("💡 Улучшите точность стрельбы - ваша средняя точность < 50%")
        
        winrate = (len([b for b in self.analyzer.battles if b.battle_result == BattleResult.WIN]) / len(self.analyzer.battles)) * 100
        if winrate < 45:
            suggestions.append("💡 Работайте с тактикой - ваш винрейт < 45%")
        
        avg_survivability = sum((b.vehicle.max_hp - b.damage_received) / b.vehicle.max_hp * 100 for b in self.analyzer.battles) / len(self.analyzer.battles)
        if avg_survivability < 30:
            suggestions.append("💡 Улучшите позиционирование - вы часто умираете в начале боя")
        
        if not suggestions:
            suggestions.append("✅ Отличная игра! Продолжайте в том же духе!")
        
        return suggestions
    
    @staticmethod
    def _calculate_winrate(battles: List[BattleData]) -> float:
        """Вычислить винрейт"""
        if not battles:
            return 0.0
        wins = len([b for b in battles if b.battle_result == BattleResult.WIN])
        return (wins / len(battles)) * 100


class UICustomizer:
    """Кастомизатор интерфейса в стиле volk_4on_ok"""
    
    def __init__(self):
        self.themes = self._load_themes()
        self.current_theme = "volk_dark"
        
    def _load_themes(self) -> Dict:
        """Загрузить темы"""
        return {
            "volk_dark": {
                "name": "Volk Dark Pro",
                "colors": {
                    "primary": "#FF6B35",
                    "secondary": "#004E89",
                    "background": "#0A0E27",
                    "text": "#FFFFFF",
                    "accent": "#F7B801"
                },
                "description": "Профессиональная тёмная тема в стиле volk_4on_ok"
            },
            "volk_light": {
                "name": "Volk Light",
                "colors": {
                    "primary": "#FF6B35",
                    "secondary": "#004E89",
                    "background": "#F5F5F5",
                    "text": "#000000",
                    "accent": "#F7B801"
                },
                "description": "Светлая версия volk_4on_ok"
            },
            "competitive": {
                "name": "Competitive Edition",
                "colors": {
                    "primary": "#00FF00",
                    "secondary": "#FF0000",
                    "background": "#000000",
                    "text": "#FFFFFF",
                    "accent": "#FFFF00"
                },
                "description": "Хай-контраст для конкурентной игры"
            }
        }
    
    def get_current_theme(self) -> Dict:
        """Получить текущую тему"""
        return self.themes.get(self.current_theme, {})
    
    def change_theme(self, theme_name: str) -> bool:
        """Изменить тему"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            logger.info(f"🎨 Тема изменена на: {self.themes[theme_name]['name']}")
            return True
        return False
    
    def list_themes(self) -> List[Dict]:
        """Список всех тем"""
        return [{"name": name, "description": theme["description"]} for name, theme in self.themes.items()]


class VolkWoTToolkit:
    """Главный класс тулкита - объединяет все компоненты"""
    
    def __init__(self):
        self.analyzer = BattleAnalyzer()
        self.tactical_helper = TacticalHelper()
        self.stats_tracker = StatsTracker(self.analyzer)
        self.ui_customizer = UICustomizer()
        self.config = self._load_master_config()
        
    def _load_master_config(self) -> Dict:
        """Загрузить главную конфигурацию"""
        return {
            "toolkit_version": "2.0.0",
            "auto_track_battles": True,
            "enable_notifications": True,
            "enable_analytics": True,
            "theme": "volk_dark",
            "language": "Russian"
        }
    
    def add_sample_battles(self):
        """Добавить примеры боёв для демонстрации"""
        sample_battles = [
            BattleData(
                battle_id=1,
                player_name="volk_4on_ok",
                vehicle=Vehicle(
                    name="T-34-85",
                    vehicle_id=1,
                    tier=VehicleTier.TIER_VI,
                    vehicle_class=VehicleClass.MEDIUM_TANK,
                    nation="USSR",
                    hp=150,
                    max_hp=150,
                    gun_damage=160,
                    penetration=132,
                    reload_time=6.5,
                    armor_front=90,
                    armor_side=75,
                    armor_rear=60
                ),
                battle_result=BattleResult.WIN,
                damage_dealt=2847,
                damage_received=450,
                kills=4,
                shots_hit=18,
                shots_fired=25,
                distance_traveled=1250.5,
                battle_duration=480,
                credits_earned=42500,
                experience_earned=1850,
                timestamp=time.time(),
                map_name="Prokhorovka",
                battle_type="Random"
            ),
            BattleData(
                battle_id=2,
                player_name="volk_4on_ok",
                vehicle=Vehicle(
                    name="IS-7",
                    vehicle_id=2,
                    tier=VehicleTier.TIER_X,
                    vehicle_class=VehicleClass.HEAVY_TANK,
                    nation="USSR",
                    hp=320,
                    max_hp=320,
                    gun_damage=490,
                    penetration=258,
                    reload_time=6.86,
                    armor_front=160,
                    armor_side=140,
                    armor_rear=100
                ),
                battle_result=BattleResult.WIN,
                damage_dealt=3456,
                damage_received=680,
                kills=3,
                shots_hit=22,
                shots_fired=30,
                distance_traveled=2100.0,
                battle_duration=540,
                credits_earned=67800,
                experience_earned=3200,
                timestamp=time.time(),
                map_name="Ensk",
                battle_type="Random"
            ),
            BattleData(
                battle_id=3,
                player_name="volk_4on_ok",
                vehicle=Vehicle(
                    name="Obj. 268",
                    vehicle_id=3,
                    tier=VehicleTier.TIER_X,
                    vehicle_class=VehicleClass.TD,
                    nation="USSR",
                    hp=250,
                    max_hp=250,
                    gun_damage=490,
                    penetration=303,
                    reload_time=8.9,
                    armor_front=100,
                    armor_side=80,
                    armor_rear=70
                ),
                battle_result=BattleResult.WIN,
                damage_dealt=4125,
                damage_received=320,
                kills=5,
                shots_hit=19,
                shots_fired=24,
                distance_traveled=1800.0,
                battle_duration=600,
                credits_earned=78900,
                experience_earned=3850,
                timestamp=time.time(),
                map_name="Lakeville",
                battle_type="Random"
            )
        ]
        
        for battle in sample_battles:
            self.analyzer.add_battle(battle)
    
    def render_main_dashboard(self):
        """Рендеринг главного дашборда"""
        print(VOLK_STYLE)
        
        stats = self.analyzer.get_total_stats()
        performance = self.stats_tracker.get_performance_rating()
        
        print("┌" + "─" * 82 + "┐")
        print("│" + " " * 82 + "│")
        print("│" + "  📊 MAIN DASHBOARD".center(82) + "│")
        print("│" + " " * 82 + "│")
        print("├" + "─" * 82 + "┤")
        
        if stats:
            print(f"│ 🎮 Total Battles: {stats.get('total_battles', 0):>6}  |  Win Rate: {stats.get('win_rate', 0):>6.1f}%  |  Performance: {performance} │")
            print(f"│ 💥 Total Damage: {stats.get('total_damage', 0):>10}  |  Avg Damage: {stats.get('avg_damage', 0):>8.0f}  |  Accuracy: {stats.get('accuracy', 0):>5.1f}% │")
            print(f"│ 🎯 Total Kills: {stats.get('total_kills', 0):>10}  |  Avg Kills: {stats.get('avg_kills', 0):>10.1f}  |  Credits: {stats.get('total_credits', 0):>10} │")
            print(f"│ ⭐ Total XP: {stats.get('total_xp', 0):>13}  |  Per Battle XP: {stats.get('avg_xp_per_battle', 0):>8.0f}  |  Credits/Battle: {stats.get('avg_credits_per_battle', 0):>7.0f} │")
        else:
            print("│" + "  No battle data available - Add battles to see statistics".center(82) + "│")
        
        print("└" + "─" * 82 + "┘")
        print()
    
    def render_battle_analyzer(self):
        """Рендеринг анализатора боёв"""
        print("\n╔════════════════════════════════════════════════════════════════════════════╗")
        print("║" + "  🎯 BATTLE ANALYZER".center(78) + "║")
        print("╠════════════════════════════════════════════════════════════════════════════╣")
        
        best_battle = self.analyzer.get_best_battle()
        worst_battle = self.analyzer.get_worst_battle()
        recent = self.analyzer.get_recent_battles(3)
        
        if best_battle:
            print(f"║ 🏆 Best Battle: {best_battle.vehicle.name:20} | Damage: {best_battle.damage_dealt:>5} | Kills: {best_battle.kills:>2} ║")
        
        if worst_battle:
            print(f"║ 📉 Worst Battle: {worst_battle.vehicle.name:20} | Damage: {worst_battle.damage_dealt:>5} | Kills: {worst_battle.kills:>2} ║")
        
        print("║                                                                              ║")
        print("║ 📋 Last 3 Battles:                                                           ║")
        for i, battle in enumerate(recent, 1):
            result = "✅ WIN" if battle.battle_result == BattleResult.WIN else "❌ LOSS"
            print(f"║   {i}. {battle.vehicle.name:20} | {result:>6} | DMG: {battle.damage_dealt:>5} | K/D: {battle.kills:>2}/{int(battle.damage_received/100):>2} ║")
        
        print("╚════════════════════════════════════════════════════════════════════════════╝\n")
    
    def render_tactical_helper(self):
        """Рендеринг тактического помощника"""
        print("\n╔════════════════════════════════════════════════════════════════════════════╗")
        print("║" + "  🎖️ TACTICAL HELPER".center(78) + "║")
        print("╠════════════════════════════════════════════════════════════════════════════╣")
        
        # Советы для Prokhorovka
        tips = self.tactical_helper.get_map_tips("Prokhorovka")
        print("║ 🗺️  Prokhorovka Tips:                                                       ║")
        if tips:
            for tactic in tips.get("tactics", [])[:3]:
                print(f"║ {tactic:76} ║")
        
        print("║                                                                              ║")
        
        # Советы против Heavy Tank
        counters = self.tactical_helper.get_class_counter_tips("Heavy_Tank")
        print("║ 🎯 How to Counter Heavy Tanks:                                              ║")
        if counters:
            print(f"║ {counters.get('tactic', ''):76} ║")
        
        print("╚════════════════════════════════════════════════════════════════════════════╝\n")
    
    def render_stats_tracker(self):
        """Рендеринг трекера статистики"""
        print("\n╔════════════════════════════════════════════════════════════════════════════╗")
        print("║" + "  📈 STATS TRACKER & ANALYTICS".center(78) + "║")
        print("╠════════════════════════════════════════════════════════════════════════════╣")
        
        trend = self.stats_tracker.get_winrate_trend()
        if trend:
            print(f"║ 📊 7-Day Trend: {trend.get('trend', 'N/A'):15} | Battles: {trend.get('battles_count', 0):>3} | Win Rate: {trend.get('current_winrate', 0):>6.1f}% ║")
        
        print("║                                                                              ║")
        print("║ 💡 Improvement Suggestions:                                                  ║")
        
        suggestions = self.stats_tracker.get_improvement_suggestions()
        for suggestion in suggestions[:3]:
            print(f"║ {suggestion:76} ║")
        
        print("╚════════════════════════════════════════════════════════════════════════════╝\n")
    
    def render_ui_customizer(self):
        """Рендеринг кастомизатора UI"""
        print("\n╔════════════════════════════════════════════════════════════════════════════╗")
        print("║" + "  🎨 UI CUSTOMIZER".center(78) + "║")
        print("╠════════════════════════════════════════════════════════════════════════════╣")
        
        current = self.ui_customizer.get_current_theme()
        print(f"║ 🎯 Current Theme: {current.get('name', 'Unknown'):50} ║")
        
        print("║ Available Themes:                                                            ║")
        for theme in self.ui_customizer.list_themes():
            print(f"║ • {theme['name']:20} - {theme['description']:40} ║")
        
        print("╚════════════════════════════════════════════════════════════════════════════╝\n")


def run_demo():
    """Запустить демонстрацию"""
    print(VOLK_STYLE)
    
    toolkit = VolkWoTToolkit()
    
    # Добавляем примеры боёв
    print("⏳ Loading sample battles...")
    toolkit.add_sample_battles()
    
    time.sleep(1)
    
    # Показываем все компоненты
    toolkit.render_main_dashboard()
    toolkit.render_battle_analyzer()
    toolkit.render_tactical_helper()
    toolkit.render_stats_tracker()
    toolkit.render_ui_customizer()
    
    # Экспортируем статистику
    print("💾 Exporting statistics...")
    toolkit.analyzer.export_stats()
    
    print("✅ Demo completed!")
    print("\n🎮 Ready to track your World of Tanks battles!\n")


def run_interactive():
    """Интерактивный режим"""
    print(VOLK_STYLE)
    
    toolkit = VolkWoTToolkit()
    
    print("\n🎮 Interactive Mode - World of Tanks Toolkit v2.0\n")
    print("Available Modules:")
    print("  1 - Battle Analyzer (📊)")
    print("  2 - Tactical Helper (🎖️)")
    print("  3 - Stats Tracker (📈)")
    print("  4 - UI Customizer (🎨)")
    print("  5 - Add Sample Battle")
    print("  6 - View Dashboard")
    print("  7 - Export Statistics")
    print("  0 - Exit\n")
    
    while True:
        try:
            choice = input("Select module (0-7): ").strip()
            
            if choice == "0":
                print("\n👋 Goodbye!\n")
                break
            
            elif choice == "1":
                toolkit.render_battle_analyzer()
            
            elif choice == "2":
                toolkit.render_tactical_helper()
            
            elif choice == "3":
                toolkit.render_stats_tracker()
            
            elif choice == "4":
                toolkit.render_ui_customizer()
            
            elif choice == "5":
                print("✅ Sample battles loaded")
                toolkit.add_sample_battles()
            
            elif choice == "6":
                toolkit.render_main_dashboard()
            
            elif choice == "7":
                toolkit.analyzer.export_stats()
            
            else:
                print("❌ Unknown command\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            logger.error(f"Error: {e}\n")


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "interactive":
            run_interactive()
        else:
            run_demo()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
