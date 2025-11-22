import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class GamePassUser:
    """Represents a single MUDTPass subscriber."""

    full_name: str
    gamer_tag: str
    plan: str
    preferred_device: str
    hours_per_month: int
    favorite_genre: str
    backlog: List[str] = field(default_factory=list)

    def __str__(self) -> str:  # pragma: no cover - convenience for logging
        return self.full_name


class PeopleGenerator:
    """
    Builds a synthetic player base that resembles Xbox Game Pass adoption.
    The generator focuses on three tiers that loosely map to the real offering:
    Core, PC Game Pass and Ultimate.
    """

    DEFAULT_PLANS = {
        "Core": {
            "price": 9.99,
            "distribution": 0.42,
            "description": "Console multiplayer, rotating library",
            "tagline": "Essential console multiplayer",
            "best_for": "Players who live on Xbox and host couch co-op nights.",
            "devices": ["Xbox Series X|S", "Xbox One"],
            "hours_range": (8, 30),
            "perks": ["Xbox Live access", "Member deals", "Console catalog"],
            "features": {
                "consoleAccess": True,
                "pcAccess": False,
                "cloudGaming": False,
                "eaPlay": False,
                "dayOne": True,
                "onlineMultiplayer": True,
                "memberDiscounts": True,
            },
        },
        "PC": {
            "price": 10.99,
            "distribution": 0.33,
            "description": "Large PC catalog + EA Play",
            "tagline": "Unlimited PC library",
            "best_for": "Mouse and keyboard tacticians who mod everything.",
            "devices": ["Windows PC"],
            "hours_range": (15, 45),
            "perks": ["EA Play on PC", "Member deals", "PC catalog"],
            "features": {
                "consoleAccess": False,
                "pcAccess": True,
                "cloudGaming": False,
                "eaPlay": True,
                "dayOne": True,
                "onlineMultiplayer": True,
                "memberDiscounts": True,
            },
        },
        "Ultimate": {
            "price": 16.99,
            "distribution": 0.25,
            "description": "Console, PC and cloud streaming",
            "tagline": "All devices. All perks.",
            "best_for": "Players hopping between screens and streaming everywhere.",
            "devices": ["Xbox", "PC", "Cloud"],
            "hours_range": (25, 70),
            "perks": ["Cloud streaming", "EA Play everywhere", "Day-one releases", "Ultimate rewards"],
            "features": {
                "consoleAccess": True,
                "pcAccess": True,
                "cloudGaming": True,
                "eaPlay": True,
                "dayOne": True,
                "onlineMultiplayer": True,
                "memberDiscounts": True,
            },
        },
    }

    GENRES = [
        "RPG",
        "Racing",
        "Shooter",
        "Indie",
        "Strategy",
        "Sports",
        "Action Adventure",
        "Simulation",
    ]

    GAME_LIBRARY = [
        "Starfield",
        "Forza Horizon 5",
        "Sea of Thieves",
        "Halo Infinite",
        "Hi-Fi Rush",
        "Minecraft Legends",
        "Persona 5 Royal",
        "PowerWash Simulator",
        "Microsoft Flight Simulator",
        "Grounded",
        "Lies of P",
        "Cities: Skylines II",
    ]

    TAG_PREFIXES = [
        "Neo",
        "Pixel",
        "Turbo",
        "Ghost",
        "Crimson",
        "Void",
        "Solar",
        "Echo",
        "Mythic",
        "Iron",
    ]
    TAG_SUFFIXES = [
        "Ranger",
        "Knight",
        "Mage",
        "Runner",
        "Sniper",
        "Pilot",
        "Falcon",
        "Forge",
        "Spark",
        "Hunter",
    ]

    FIRST_NAMES = [
        "Mateo",
        "Aiko",
        "Luca",
        "Inez",
        "Sofia",
        "Tariq",
        "Leila",
        "Aria",
        "Noah",
        "Maya",
        "Ibrahim",
        "Yara",
        "Kaito",
        "Elina",
        "Jonas",
        "Chiara",
        "Diego",
        "Mireia",
        "Zara",
        "Mert",
        "Sven",
        "Freya",
        "Nikhil",
        "Anaya",
        "Yusuf",
        "Mariam",
        "Avery",
        "Santiago",
        "Amara",
        "Kenji",
        "Ada",
        "Valentina",
        "Thiago",
        "Omar",
        "Sara",
        "Elif",
        "Rafael",
        "Isla",
        "Finn",
        "Helena",
        "Khadija",
        "Andrei",
        "Iryna",
        "Zayne",
        "Sibel",
        "Elias",
        "Camila",
        "Riya",
        "Onur",
    ]

    LAST_NAMES = [
        "Martinez",
        "Tanaka",
        "Okafor",
        "Sahin",
        "Garcia",
        "Kumar",
        "Ivanov",
        "Silva",
        "Aliyev",
        "Fernandez",
        "Dubois",
        "Petrov",
        "Singh",
        "Yilmaz",
        "Novak",
        "Costa",
        "Aziz",
        "Bianchi",
        "Zimmer",
        "Kowalski",
        "Moreau",
        "Nguyen",
        "Suzuki",
        "Sato",
        "Papadopoulos",
        "Ibrahim",
        "Mendoza",
        "Bakir",
        "Hernandez",
        "Moroz",
        "Quintero",
        "Santos",
        "Nielsen",
        "Okeke",
        "Hassan",
        "Zhang",
        "Lai",
        "Borg",
        "Rahman",
        "Weiss",
        "Khan",
        "Ueda",
        "Moretti",
        "Gunes",
        "Ochoa",
        "Campos",
        "Chandrasekar",
        "Lopez",
    ]

    def __init__(
        self,
        total_users: int,
        plan_specs: Optional[Dict[str, Dict]] = None,
        seed: Optional[int] = None,
    ) -> None:
        self.total_users = total_users
        self.plan_specs = plan_specs or self.DEFAULT_PLANS
        self.plan_names = list(self.plan_specs.keys())
        self.plan_catalog = {
            name: {
                "price": spec["price"],
                "description": spec["description"],
                "perks": spec["perks"],
                "devices": spec["devices"],
                "tagline": spec["tagline"],
                "best_for": spec["best_for"],
                "features": spec["features"],
                "hours_range": spec["hours_range"],
            }
            for name, spec in self.plan_specs.items()
        }
        self._random = random.Random(seed)

    def _pick_plan(self) -> str:
        """Randomly choose a plan following the configured distribution."""
        roll = self._random.random()
        cumulative = 0.0
        for name in self.plan_names:
            cumulative += self.plan_specs[name]["distribution"]
            if roll <= cumulative:
                return name
        # In case of rounding error return the last plan
        return self.plan_names[-1]

    def _generate_full_name(self) -> str:
        first = self._random.choice(self.FIRST_NAMES)
        last = self._random.choice(self.LAST_NAMES)
        return f"{first} {last}"

    def _generate_gamertag(self) -> str:
        prefix = self._random.choice(self.TAG_PREFIXES)
        suffix = self._random.choice(self.TAG_SUFFIXES)
        digits = self._random.randint(10, 99)
        return f"{prefix}{suffix}{digits}"

    def _generate_user(self, plan: str) -> GamePassUser:
        spec = self.plan_specs[plan]
        hours_range = spec["hours_range"]
        hours = self._random.randint(hours_range[0], hours_range[1])
        favorite_genre = self._random.choice(self.GENRES)
        backlog_size = self._random.randint(1, min(4, len(self.GAME_LIBRARY)))
        backlog = self._random.sample(self.GAME_LIBRARY, k=backlog_size)
        preferred_device = self._random.choice(spec["devices"])
        return GamePassUser(
            full_name=self._generate_full_name(),
            gamer_tag=self._generate_gamertag(),
            plan=plan,
            preferred_device=preferred_device,
            hours_per_month=hours,
            favorite_genre=favorite_genre,
            backlog=backlog,
        )

    def generate(self) -> Dict[str, List[GamePassUser]]:
        """Produce a dictionary grouped by subscription tier."""
        population: Dict[str, List[GamePassUser]] = {name: [] for name in self.plan_names}
        for _ in range(self.total_users):
            plan = self._pick_plan()
            population[plan].append(self._generate_user(plan))
        return population
