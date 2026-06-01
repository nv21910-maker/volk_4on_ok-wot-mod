#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Volk_4on_ok WoT Mod - World of Tanks Modification
Полнофункциональный мод в стиле Jove's Modpack
Version: 1.0.0
Author: nv21910-maker
"""

import sys
import json
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


class VehicleType(Enum):
    """Типы танков"""
    LIGHT_TANK = "light_tank"
    MEDIUM_TANK = "medium_tank"
    HEAVY_TANK = "heavy_tank"
    TD = "tank_destroyer"
    SPG = "spg"
    UNKNOWN = "unknown"


class DamageType(Enum):
    """Типы урона"""
    AP = "armor_piercing"
    HEAT = "heat"
    HE = "high_explosive"
    SHOT = "shot"
    UNKNOWN = "unknown"


@dataclass
class Player:
    """Данные игрока"""
    name: str
    vehicle_id: int
    vehicle_name: str
    vehicle_type: VehicleType
    health: int
    max_health: int
    team: int
    position: Tuple[float, float, float]
    is_alive: bool = True
    damage_dealt: int = 0
    shots_hit: int = 0
    shots_fired: int = 0
    

@dataclass
class DamageEvent:
    """Событие урона"""
    attacker: str
    victim: str
    damage: int
    damage_type: DamageType
    timestamp: float
    vehicle_type: VehicleType
    critical: bool = False


class BattleStatistics:
    """Сбор статистики боя"""
    
    def __init__(self):
        self.damage_events: List[DamageEvent] = []
        self.battle_start_time = time.time()
        self.total_damage_dealt = 0
        self.total_damage_received = 0
        self.kills = 0
        self.deaths = 0
        self.shots_fired = 0
        self.shots_hit = 0
        
    def add_damage_event(self, event: DamageEvent):
        """Добавить событие урона"""
        self.damage_events.append(event)
        self.total_damage_dealt += event.damage
        
    def get_accuracy(self) -> float:
        """Получить точность стрельбы"""
        if self.shots_fired == 0:
            return 0.0
        return (self.shots_hit / self.shots_fired) * 100
    
    def get_battle_duration(self) -> float:
        """Получить длительность боя в секундах"""
        return time.time() - self.battle_start_time
    
    def get_dpm(self) -> float:
        """Получить урон в минуту (DPM)"""
        duration_minutes = self.get_battle_duration() / 60
        if duration_minutes == 0:
            return 0.0
        return self.total_damage_dealt / duration_minutes


class BattleInterface:
    """Боевой интерфейс мода"""
    
    def __init__(self):
        self.players: Dict[int, Player] = {}
        self.statistics = BattleStatistics()
        self.minimap_enabled = True
        self.damage_indicator_enabled = True
        self.player_stats_enabled = True
        self.crosshair_enabled = True
        self.sound_alerts_enabled = True
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Загрузить конфигурацию"""
        default_config = {
            "interface": {
                "transparency": 0.8,
                "scale": 1.0,
                "position": "top-right",
                "color_theme": "dark"
            },
            "features": {
                "extended_info": True,
                "damage_log": True,
                "minimap_enhanced": True,
                "enemy_spotted_sound": True,
                "critical_hit_sound": True,
                "reload_timer": True
            },
            "visuals": {
                "damage_numbers": True,
                "penetration_indicator": True,
                "aim_circle": True,
                "vehicle_outline": True,
                "health_bars": True
            },
            "sounds": {
                "volume": 100,
                "mute_chat": False,
                "notification_sounds": True
            }
        }
        return default_config
    
    def add_player(self, player: Player):
        """Добавить игрока в бой"""
        self.players[player.vehicle_id] = player
        logger.info(f"Игрок добавлен: {player.name} ({player.vehicle_name})")
    
    def update_player_health(self, vehicle_id: int, health: int):
        """Обновить здоровье игрока"""
        if vehicle_id in self.players:
            self.players[vehicle_id].health = health
            if health <= 0:
                self.players[vehicle_id].is_alive = False
                self.statistics.deaths += 1
    
    def report_damage(self, attacker: str, victim: str, damage: int, 
                     damage_type: DamageType, vehicle_type: VehicleType):
        """Зарегистрировать урон"""
        event = DamageEvent(
            attacker=attacker,
            victim=victim,
            damage=damage,
            damage_type=damage_type,
            timestamp=time.time(),
            vehicle_type=vehicle_type,
            critical=(damage > 100)
        )
        self.statistics.add_damage_event(event)
        
        if self.damage_indicator_enabled:
            self._show_damage_indicator(damage, damage_type)
        
        if event.critical and self.sound_alerts_enabled:
            self._play_critical_hit_sound()
    
    def get_enemy_info(self, vehicle_id: int) -> Optional[Dict]:
        """Получить информацию о враге"""
        if vehicle_id not in self.players:
            return None
        
        player = self.players[vehicle_id]
        return {
            "name": player.name,
            "vehicle": player.vehicle_name,
            "type": player.vehicle_type.value,
            "health": player.health,
            "max_health": player.max_health,
            "health_percentage": (player.health / player.max_health) * 100,
            "is_alive": player.is_alive,
            "position": player.position
        }
    
    def render_minimap(self) -> str:
        """Рендеринг улучшенной миникарты"""
        if not self.minimap_enabled:
            return ""
        
        minimap = "╔════════════════════════════════════════╗\n"
        minimap += "║          MINIMAP (Enhanced)            ║\n"
        minimap += "╠════════════════════════════════════════╣\n"
        
        for vehicle_id, player in self.players.items():
            symbol = "●" if player.is_alive else "✕"
            team_marker = "🔴" if player.team == 1 else "🔵"
            minimap += f"║ {team_marker} {symbol} {player.name:20} {player.vehicle_name:12} ║\n"
        
        minimap += "╚════════════════════════════════════════╝\n"
        return minimap
    
    def render_battle_stats(self) -> str:
        """Рендеринг статистики боя"""
        stats = "╔════════════════════════════════════════╗\n"
        stats += "║         BATTLE STATISTICS              ║\n"
        stats += "╠════════════════════════════════════════╣\n"
        stats += f"║ Урон нанесен:      {self.statistics.total_damage_dealt:>6} HP       ║\n"
        stats += f"║ Урон получен:      {self.statistics.total_damage_received:>6} HP       ║\n"
        stats += f"║ Точность:          {self.statistics.get_accuracy():>6.1f}%       ║\n"
        stats += f"║ Попадания:         {self.statistics.shots_hit:>6}/{self.statistics.shots_fired:<6}     ║\n"
        stats += f"║ DPM:               {self.statistics.get_dpm():>6.0f}        ║\n"
        stats += f"║ Время боя:         {self.statistics.get_battle_duration():>6.0f}s       ║\n"
        stats += f"║ Убийства:          {self.statistics.kills:>6}        ║\n"
        stats += f"║ Смерти:            {self.statistics.deaths:>6}        ║\n"
        stats += "╚════════════════════════════════════════╝\n"
        return stats
    
    def render_damage_log(self, limit: int = 10) -> str:
        """Рендеринг лога урона"""
        log = "╔════════════════════════════════════════╗\n"
        log += "║           DAMAGE LOG (Latest)          ║\n"
        log += "╠════════════════════════════════════════╣\n"
        
        recent_events = self.statistics.damage_events[-limit:]
        for event in reversed(recent_events):
            critical_mark = "⚡" if event.critical else " "
            log += f"║ {critical_mark} {event.attacker:12} → {event.victim:12} | {event.damage:>4}dmg ║\n"
        
        log += "╚════════════════════════════════════════╝\n"
        return log
    
    def render_vehicle_list(self) -> str:
        """Рендеринг списка танков в бою"""
        vehicles = "╔════════════════════════════════════════╗\n"
        vehicles += "║        VEHICLES IN BATTLE              ║\n"
        vehicles += "╠════════════════════════════════════════╣\n"
        
        for vehicle_id, player in self.players.items():
            health_bar = self._get_health_bar(player.health, player.max_health)
            team = "RED" if player.team == 1 else "BLUE"
            status = "ALIVE" if player.is_alive else "DEAD"
            vehicles += f"║ [{team}] {player.name:10} {health_bar} {status:>5} ║\n"
        
        vehicles += "╚════════════════════════════════════════╝\n"
        return vehicles
    
    def _show_damage_indicator(self, damage: int, damage_type: DamageType):
        """Показать индикатор урона"""
        icon = {
            DamageType.AP: "▲",
            DamageType.HEAT: "◆",
            DamageType.HE: "●",
            DamageType.SHOT: "■",
            DamageType.UNKNOWN: "○"
        }.get(damage_type, "?")
        
        logger.info(f"DAMAGE: {icon} {damage} HP ({damage_type.value})")
    
    def _play_critical_hit_sound(self):
        """Воспроизвести звук критического попадания"""
        if self.sound_alerts_enabled:
            logger.info("🔊 CRITICAL HIT SOUND")
    
    def _get_health_bar(self, current: int, maximum: int, width: int = 12) -> str:
        """Получить полоску здоровья"""
        if maximum == 0:
            return "█" * width
        
        filled = int((current / maximum) * width)
        empty = width - filled
        return "█" * filled + "░" * empty
    
    def toggle_feature(self, feature: str, enabled: bool):
        """Включить/отключить функцию"""
        features = {
            "damage_indicator": "damage_indicator_enabled",
            "minimap": "minimap_enabled",
            "player_stats": "player_stats_enabled",
            "crosshair": "crosshair_enabled",
            "sounds": "sound_alerts_enabled"
        }
        
        if feature in features:
            setattr(self, features[feature], enabled)
            state = "включена" if enabled else "отключена"
            logger.info(f"Функция '{feature}' {state}")
    
    def export_stats(self, filename: str = "battle_stats.json"):
        """Экспортировать статистику боя"""
        stats_data = {
            "battle_duration": self.statistics.get_battle_duration(),
            "total_damage": self.statistics.total_damage_dealt,
            "accuracy": self.statistics.get_accuracy(),
            "dpm": self.statistics.get_dpm(),
            "kills": self.statistics.kills,
            "deaths": self.statistics.deaths,
            "damage_events_count": len(self.statistics.damage_events),
            "players_count": len(self.players),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, indent=4, ensure_ascii=False)
        
        logger.info(f"Статистика экспортирована в {filename}")


def demo_battle():
    """Демонстрация работы мода"""
    print("\n" + "="*50)
    print("🎮 VOLK_4ON_OK WOT MOD - DEMO")
    print("="*50 + "\n")
    
    # Создаем интерфейс боя
    battle = BattleInterface()
    
    # Добавляем игроков
    players_data = [
        Player("PlayerName1", 1, "T-34", VehicleType.MEDIUM_TANK, 300, 320, 1, (100, 100, 0)),
        Player("Enemy_Tank", 2, "Panther", VehicleType.MEDIUM_TANK, 280, 320, 2, (200, 150, 0)),
        Player("RedTeamHeavy", 3, "IS-7", VehicleType.HEAVY_TANK, 400, 450, 1, (50, 200, 0)),
        Player("BlueSniper", 4, "Grille 15", VehicleType.TD, 200, 200, 2, (300, 300, 0)),
    ]
    
    for player in players_data:
        battle.add_player(player)
    
    # Симулируем события боя
    print("⚔️  Симуляция боя...\n")
    
    # Событие 1: Урон игроком
    battle.statistics.shots_fired = 5
    battle.statistics.shots_hit = 4
    battle.report_damage(
        "PlayerName1", "Enemy_Tank", 85,
        DamageType.AP, VehicleType.MEDIUM_TANK
    )
    battle.update_player_health(2, 195)
    
    time.sleep(1)
    
    # Событие 2: Критический урон
    battle.statistics.shots_fired = 6
    battle.statistics.shots_hit = 5
    battle.report_damage(
        "Enemy_Tank", "PlayerName1", 120,
        DamageType.HEAT, VehicleType.MEDIUM_TANK
    )
    battle.update_player_health(1, 180)
    battle.statistics.total_damage_received = 120
    
    time.sleep(1)
    
    # Событие 3: Еще урон
    battle.statistics.shots_fired = 8
    battle.statistics.shots_hit = 7
    battle.report_damage(
        "RedTeamHeavy", "BlueSniper", 250,
        DamageType.AP, VehicleType.HEAVY_TANK
    )
    battle.update_player_health(4, 0)
    battle.statistics.kills += 1
    
    print("\n" + "="*42)
    print("📊 ИНТЕРФЕЙС БОЕВОЙ ИНФОРМАЦИИ")
    print("="*42 + "\n")
    
    # Выводим информацию
    print(battle.render_vehicle_list())
    print(battle.render_minimap())
    print(battle.render_damage_log())
    print(battle.render_battle_stats())
    
    # Информация о враге
    print("👁️  ИНФОРМАЦИЯ О ВРАГЕ:\n")
    enemy_info = battle.get_enemy_info(2)
    if enemy_info:
        print(f"  Имя: {enemy_info['name']}")
        print(f"  Танк: {enemy_info['vehicle']}")
        print(f"  Тип: {enemy_info['type']}")
        print(f"  HP: {enemy_info['health']}/{enemy_info['max_health']}")
        print(f"  Здоровье: {enemy_info['health_percentage']:.1f}%")
        print(f"  Статус: {'ЖИВОЙ' if enemy_info['is_alive'] else 'МЕРТВ'}\n")
    
    # Управление функциями
    print("🔧 УПРАВЛЕНИЕ ФУНКЦИЯМИ:\n")
    battle.toggle_feature("damage_indicator", True)
    battle.toggle_feature("minimap", True)
    battle.toggle_feature("sounds", True)
    
    print("\n✅ Демонстрация завершена!\n")


if __name__ == "__main__":
    try:
        demo_battle()
    except KeyboardInterrupt:
        print("\n\n❌ Программа прервана пользователем")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)
        sys.exit(1)
