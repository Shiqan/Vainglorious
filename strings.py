import six

heroes = {
    "*Adagio*": "Adagio",
    "*Alpha*": "Alpha",
    "*Ardan*": "Ardan",
    "*Baron*": "Baron",
    "*Blackfeather*": "Blackfeather",
    "*Catherine*": "Catherine",
    "*Celeste*": "Celeste",
    "*Flicker*": "Flicker",
    "*Fortress*": "Fortress",
    "*Glaive*": "Glaive",
    "*Gwen*": "Gwen",
    "*Krul*": "Krul",
    "*Skaarf*": "Skaarf",
    "*Rona*": "Rona",
    "*Idris*": "Idris",
    "*Joule*": "Joule",
    "*Kestrel*": "Kestrel",
    "*Koshka*": "Koshka",
    "*Lance*": "Lance",
    "*Lyra*": "Lyra",
    "*Ozo*": "Ozo",
    "*Petal*": "Petal",
    "*Phinn*": "Phinn",
    "*Reim*": "Reim",
    "*Ringo*": "Ringo",
    "*Samuel*": "Samuel",
    "*SAW*": "SAW",
    "*Taka*": "Taka",
    "*Skye*": "Skye",
    "*Vox*": "Vox",
    "*Grumpjaw*": "Grumpjaw"
}

heroes_inv = {v.lower(): k for k, v in six.iteritems(heroes)}

hero_roles = {
    "*Adagio*": "Lane, Jungle, Protector",
    "*Alpha*": "Jungle, Warrior",
    "*Ardan*": "Jungle, Protector",
    "*Baron*": "Lane, Sniper",
    "*Blackfeather*": "Lane, Assassin",
    "*Catherine*": "Jungle, Protector",
    "*Celeste*": "Lane, Mage",
    "*Flicker*": "Jungle, Protector",
    "*Fortress*": "Jungle, Protector",
    "*Glaive*": "Jungle, Warrior",
    "*Gwen*": "Lane, Sniper",
    "*Krul*": "Jungle, Warrior",
    "*Skaarf*": "Lane, Mage",
    "*Rona*": "Jungle, Warrior",
    "*Idris*": "Jungle, Assassin",
    "*Joule*": "Jungle, Warrior",
    "*Kestrel*": "Lane, Sniper",
    "*Koshka*": "Jungle, Assassin",
    "*Lance*": "Jungle, Protector",
    "*Lyra*": "Jungle, Protector",
    "*Ozo*": "Jungle, Assassin",
    "*Petal*": "Jungle, Sniper",
    "*Phinn*": "Jungle, Protector",
    "*Reim*": "Jungle, Mage",
    "*Ringo*": "Lane, Sniper",
    "*Samuel*": "Lane, Mage",
    "*SAW*": "Lane, Sniper",
    "*Taka*": "Jungle, Assassin",
    "*Skye*": "Lane, Sniper",
    "*Vox*": "Lane, Sniper",
    "*Grumpjaw*": "Jungle, Warrior"
}

quotes = [
    ("Phinn", "I wanna catch butterflies"),
    ("Phinn", "Slow down and smell the flowers"),
    ("Phinn", "I prefer to take my time"),
    ("Phinn", "Eraaaah"),
    ("Phinn", "Hahahahaha, it tickles"),
    ("Phinn", "Something smells fishy"),
    ("Phinn", "grrrrrrmmmmmrrrrmmm rumbly(?)"),
    ("Phinn", "None of these merchants sell fish cakes"),
    ("Phinn", "I would love a good fish brownie"),
    ("Phinn", "Ready or not, here we are"),
    ("Phinn", "When is tea Time"),
    ("Phinn", "Mostly I'm guilty by association"),
    ("Phinn", "Slow and steady wins the race"),
    ("Phinn", "Pardon me, exuse me, pardon"),
    ("Phinn", "Everybody move"),
    ("Phinn", "Lets rest awhile we can win later"),
    ("Phinn", "As long as I'm here i might as well kill you"),
    ("Phinn", "I'm mostly guilty by association")
]

abilities = {
    "*Adagio*": {"HERO_ABILITY_ADAGIO_FORTUNES_SMILE_NAME": "Gift of Fire", "HERO_ABILITY_ADAGIO_GASOLINE_SOAKED_NAME": "Agent of Wrath", "HERO_ABILITY_ADAGIO_FRIENDSHIP_NAME": "Verse of Judgement"},
    "*Alpha*": {"HERO_ABILITY_ALPHA_A_NAME": "Prime Directive", "HERO_ABILITY_ALPHA_B_NAME": "Core Charge", "HERO_ABILITY_ALPHA_C_NAME": "Termniation Protocol"},
    "*Ardan*": {"HERO_ABILITY_ARDAN_A": "Vanguard", "HERO_ABILITY_ARDAN_B": "Blood for Blood", "HERO_ABILITY_ARDAN_C": "Gauntlet"},
    "*Baron*": {"HERO_ABILITY_BARON_A_NAME": "Porcupine Mortar", "HERO_ABILITY_BARON_B_NAME": "Jump Jets", "HERO_ABILITY_BARON_C_NAME": "Ion Cannon"},
    "*Blackfeather*": {"HERO_ABILITY_HERO021_A_NAME": "Feint of Hearth", "HERO_ABILITY_HERO021_B_NAME": "On Point", "HERO_ABILITY_HERO021_C_NAME": "Rose Offensive"},
    "*Catherine*": {"HERO_ABILITY_CATHERINE_ASSASSINS_CHARGE_NAME": "Merciless Pursuit", "HERO_ABILITY_CATHERINE_ARCANE_SHIELD_NAME": "Stormguard", "HERO_ABILITY_CATHERINE_DEADLY_GRACE_NAME": "Blast Tremor"},
    "*Celeste*": {"HERO_ABILITY_CELESTE_A_NAME": "Heliogenesis", "HERO_ABILITY_CELESTE_B_NAME": "Core Collapse", "HERO_ABILITY_CELESTE_C_NAME": "Solar Storm"},
    "*Flicker*": {"HERO_ABILITY_HERO036_A_NAME": "Binding Light", "HERO_ABILITY_HERO036_B_NAME": "Fairy Dust", "HERO_ABILITY_HERO036_C_NAME": "Mooncloak"},
    "*Fortress*": {"HERO_ABILITY_FORTRESS_A_NAME": "Truth of the Tooth", "HERO_ABILITY_FORTRESS_B_NAME": "Law of the Claw", "HERO_ABILITY_FORTRESS_C_NAME": "Attack of the Pack"},
    "*Glaive*": {"HERO_ABILITY_GLAIVE_AFTERBURN_NAME": "Afterburn", "HERO_ABILITY_GLAIVE_TWISTED_STROKE_NAME": "Twisted Stroke", "HERO_ABILITY_GLAIVE_BLOODSONG_NAME": "Bloodsong"},
     "*Gwen*": {"HERO_ABILITY_GWEN_A_NAME": "Buckshot Bonanza", "HERO_ABILITY_GWEN_B_NAME": "Skedaddle", "HERO_ABILITY_GWEN_C_NAME": "Aces High"},
    "*Krul*": {"HERO_ABILITY_HERO009_BURNING_WOUNDS_NAME": "Dead Man's Rush", "HERO_ABILITY_HERO009_LIFE_FROM_PAIN_NAME": "Spectral Smite", "HERO_ABILITY_HERO009_SHIMMERHEART_NAME": "From Hell's Heart"},
    "*Skaarf*": {"HERO_ABILITY_SKAARF_A_SPITFIRE": "Spitfire", "HERO_ABILITY_SKAARF_B_GOOP": "Goop", "HERO_ABILITY_SKAARF_C_DRAGON_BREATH": "Dragon's Breath"},
    "*Rona*": {"HERO_ABILITY_RONA_A_NAME": "Into the Fray", "HERO_ABILITY_RONA_B_NAME": "Foesplitter", "HERO_ABILITY_RONA_C_NAME": "Red Mist"},
    "*Idris*": {"HERO_ABILITY_IDRIS_A_NAME": "Shroudstep", "HERO_ABILITY_IDRIS_B_NAME": "Chakram", "HERO_ABILITY_IDRIS_C_NAME": "Shimmer Strike"},
    "*Joule*": {"HERO_ABILITY_JOULE_RHAPSODY_CANNONS": "Rocket Leap", "HERO_ABILITY_JOULE_RHAPSODY_POWERSLIDE": "Thunder Strike", "HERO_ABILITY_JOULE_ORBITAL_NUKE": "Big Red Button"},
    "*Kestrel*": {"HERO_ABILITY_KESTREL_A_NAME": "Glimmershot", "HERO_ABILITY_KESTREL_B_NAME": "Active Camo", "HERO_ABILITY_KESTREL_C_NAME": "One Shot One Kill"},
    "*Koshka*": {"HERO_ABILITY_KOSHKA_POUNCE_NAME": "Pouncy Fun", "HERO_ABILITY_KOSHKA_TWIRL_NAME": "Twirly Death", "HERO_ABILITY_KOSHKA_FRENZY_NAME": "Yummy Catnip Frenzy"},
    "*Lance*": {"HERO_ABILITY_LANCE_A_NAME": "Impale", "HERO_ABILITY_LANCE_B_NAME": "Gythian Wall", "HERO_ABILITY_LANCE_C_NAME": "Combat Roll"},
    "*Lyra*": {"HERO_ABILITY_LYRA_A_NAME": "Imperial Sigil", "HERO_ABILITY_LYRA_B_NAME": "Bright Bulwark", "HERO_ABILITY_LYRA_C_NAME": "Arcane Passage"},
    "*Ozo*": {"HERO_ABILITY_OZO_A_NAME": "Three-Ring Circus", "HERO_ABILITY_OZO_B_NAME": "Acrobounce", "HERO_ABILITY_OZO_C_NAME": "Bangarang"},
    "*Petal*": {"HERO_ABILITY_PETAL_BRAMBLETHORN_SEED_NAME": "Brambleboom Seeds", "HERO_ABILITY_PETAL_SHOUT_OF_THE_ENTS_NAME": "Trampoline!", "HERO_ABILITY_PETAL_THORNSTORM_NAME": "Spontaneous Combustion"},
    "*Phinn*": {"HERO_ABILITY_PHINN_A_NAME": "Quibble", "HERO_ABILITY_PHINN_B_NAME": "Polite Company", "HERO_ABILITY_PHINN_C_NAME": "Forced Accord"},
    "*Reim*": {"HERO_ABILITY_REIM_A_NAME": "Winter Spire", "HERO_ABILITY_REIM_B_NAME": "Chill Winds", "HERO_ABILITY_REIM_C_NAME": "Valkyrie"},
    "*Ringo*": {"HERO_ABILITY_RINGO_WING_CUT_NAME": "Achilles Shot", "HERO_ABILITY_RINGO_TWIRLING_SILVER_NAME": "Twirling Silver", "HERO_ABILITY_RINGO_HELLFIRE_SAKE_NAME": "Hellfire Brew"},
    "*Samuel*": {"HERO_ABILITY_SAMUEL_A_NAME": "Malice & Verdict", "HERO_ABILITY_SAMUEL_B_NAME": "Drifting Dark", "HERO_ABILITY_SAMUEL_C_NAME": "Oblivion"},
    "*SAW*": {"HERO_ABILITY_SAW_ROADIE_RUN_NAME": "Roadie Run", "HERO_ABILITY_SAW_SUPPRESSING_FIRE_NAME": "Suppressing Fire", "HERO_ABILITY_SAW_EXPLOSIVE_TIPPED_SHELLS_NAME": "Mad Cannon"},
    "*Taka*": {"HERO_ABILITY_SAYOC_A": "Kaiten", "HERO_ABILITY_SAYOC_B": "Kaku", "HERO_ABILITY_SAYOC_C": "X-Retsu"},
    "*Skye*": {"HERO_ABILITY_SKYE_A_NAME": "Forward Barrage", "HERO_ABILITY_SKYE_B_NAME": "Suri Strike", "HERO_ABILITY_SKYE_C_NAME": "Death From Above"},
    "*Vox*": {"HERO_ABILITY_VOX_A_NAME": "Sonic Zoom", "HERO_ABILITY_VOX_B_NAME": "Pulse", "HERO_ABILITY_VOX_C_NAME": "Wait for It"},
    "*Grumpjaw*": {"HERO_ABILITY_GRUMPJAW_A_NAME": "Grumpy", "HERO_ABILITY_GRUMPJAW_B_NAME": "Hangry", "HERO_ABILITY_GRUMPJAW_C_NAME": "Stuffed"}
}

abilities_img = {
    "*Adagio*": {"HERO_ABILITY_ADAGIO_FORTUNES_SMILE_NAME": "adagio_a.png", "HERO_ABILITY_ADAGIO_GASOLINE_SOAKED_NAME": "adagio_b.png", "HERO_ABILITY_ADAGIO_FRIENDSHIP_NAME": "adagio_c.png"},
    "*Alpha*": {"HERO_ABILITY_ALPHA_A_NAME": "alpha_a.png", "HERO_ABILITY_ALPHA_B_NAME": "alpha_b.png", "HERO_ABILITY_ALPHA_C_NAME": "alpha_c.png"},
    "*Ardan*": {"HERO_ABILITY_ARDAN_A": "ardan_a.png", "HERO_ABILITY_ARDAN_B": "ardan_b.png", "HERO_ABILITY_ARDAN_C": "ardan_c.png"},
    "*Baron*": {"HERO_ABILITY_BARON_A_NAME": "baron_a.png", "HERO_ABILITY_BARON_B_NAME": "baron_b.png", "HERO_ABILITY_BARON_C_NAME": "baron_c.png"},
    "*Blackfeather*": {"HERO_ABILITY_HERO021_A_NAME": "blackfeather_a.jpg", "HERO_ABILITY_HERO021_B_NAME": "blackfeather_b.jpg", "HERO_ABILITY_HERO021_C_NAME": "blackfeather_c.jpg"},
    "*Catherine*": {"HERO_ABILITY_CATHERINE_ASSASSINS_CHARGE_NAME": "catherine_a.png", "HERO_ABILITY_CATHERINE_ARCANE_SHIELD_NAME": "catherine_b.png", "HERO_ABILITY_CATHERINE_DEADLY_GRACE_NAME": "catherine_c.png"},
    "*Celeste*": {"HERO_ABILITY_CELESTE_A_NAME": "celeste_a.png", "HERO_ABILITY_CELESTE_B_NAME": "celeste_b.png", "HERO_ABILITY_CELESTE_C_NAME": "celeste_c.png"},
    "*Flicker*": {"HERO_ABILITY_HERO036_A_NAME": "flicker_a.png", "HERO_ABILITY_HERO036_B_NAME": "flicker_b.png", "HERO_ABILITY_HERO036_C_NAME": "flicker_c.png"},
    "*Fortress*": {"HERO_ABILITY_FORTRESS_A_NAME": "fortress_a.png", "HERO_ABILITY_FORTRESS_B_NAME": "fortress_b.png", "HERO_ABILITY_FORTRESS_C_NAME": "fortress_c.png"},
    "*Glaive*": {"HERO_ABILITY_GLAIVE_AFTERBURN_NAME": "glaive_a.png", "HERO_ABILITY_GLAIVE_TWISTED_STROKE_NAME": "glaive_b.png", "HERO_ABILITY_GLAIVE_BLOODSONG_NAME": "glaive_c.png"},
    "*Gwen*": {"HERO_ABILITY_GWEN_A_NAME": "gwen_a.png", "HERO_ABILITY_GWEN_B_NAME": "gwen_b.png", "HERO_ABILITY_GWEN_C_NAME": "gwen_c.png"},
    "*Krul*": {"HERO_ABILITY_HERO009_BURNING_WOUNDS_NAME": "krul_a.png", "HERO_ABILITY_HERO009_LIFE_FROM_PAIN_NAME": "krul_b.png", "HERO_ABILITY_HERO009_SHIMMERHEART_NAME": "krul_c.png"},
    "*Skaarf*": {"HERO_ABILITY_SKAARF_A_SPITFIRE": "skaarf_a.png", "HERO_ABILITY_SKAARF_B_GOOP": "skaarf_b.png", "HERO_ABILITY_SKAARF_C_DRAGON_BREATH": "skaarf_c.png"},
    "*Rona*": {"HERO_ABILITY_RONA_A_NAME": "rona_a.png", "HERO_ABILITY_RONA_B_NAME": "rona_b.png", "HERO_ABILITY_RONA_C_NAME": "rona_c.png"},
    "*Idris*": {"HERO_ABILITY_IDRIS_A_NAME": "idris_a.png", "HERO_ABILITY_IDRIS_B_NAME": "idris_b.png", "HERO_ABILITY_IDRIS_C_NAME": "idris_c.png"},
    "*Joule*": {"HERO_ABILITY_JOULE_RHAPSODY_CANNONS": "joule_a.jpg", "HERO_ABILITY_JOULE_RHAPSODY_POWERSLIDE": "joule_b.jpg", "HERO_ABILITY_JOULE_ORBITAL_NUKE": "joule_c.jpg"},
    "*Kestrel*": {"HERO_ABILITY_KESTREL_A_NAME": "kestrel_a.jpg", "HERO_ABILITY_KESTREL_B_NAME": "kestrel_b.jpg", "HERO_ABILITY_KESTREL_C_NAME": "kestrel_c.jpg"},
    "*Koshka*": {"HERO_ABILITY_KOSHKA_POUNCE_NAME": "koshka_a.png", "HERO_ABILITY_KOSHKA_TWIRL_NAME": "koshka_b.png", "HERO_ABILITY_KOSHKA_FRENZY_NAME": "koshka_c.png"},
    "*Lance*": {"HERO_ABILITY_LANCE_A_NAME": "lance_a.png", "HERO_ABILITY_LANCE_B_NAME": "lance_b.png", "HERO_ABILITY_LANCE_C_NAME": "lance_c.png"},
    "*Lyra*": {"HERO_ABILITY_LYRA_A_NAME": "lyra_a.png", "HERO_ABILITY_LYRA_B_NAME": "lyra_b.png", "HERO_ABILITY_LYRA_C_NAME": "lyra_c.png"},
    "*Ozo*": {"HERO_ABILITY_OZO_A_NAME": "ozo_a.jpg", "HERO_ABILITY_OZO_B_NAME": "ozo_b.jpg", "HERO_ABILITY_OZO_C_NAME": "ozo_c.jpg"},
    "*Petal*": {"HERO_ABILITY_PETAL_BRAMBLETHORN_SEED_NAME": "petal_a.png", "HERO_ABILITY_PETAL_SHOUT_OF_THE_ENTS_NAME": "petal_b.png", "HERO_ABILITY_PETAL_THORNSTORM_NAME": "petal_c.png"},
    "*Phinn*": {"HERO_ABILITY_PHINN_A_NAME": "phinn_a.jpg", "HERO_ABILITY_PHINN_B_NAME": "phinn_b.jpg", "HERO_ABILITY_PHINN_C_NAME": "phinn_c.jpg"},
    "*Reim*": {"HERO_ABILITY_REIM_A_NAME": "reim_a.jpg", "HERO_ABILITY_REIM_B_NAME": "reim_b.jpg", "HERO_ABILITY_REIM_C_NAME": "reim_c.jpg"},
    "*Ringo*": {"HERO_ABILITY_RINGO_WING_CUT_NAME": "ringo_a.png", "HERO_ABILITY_RINGO_TWIRLING_SILVER_NAME": "ringo_b.png", "HERO_ABILITY_RINGO_HELLFIRE_SAKE_NAME": "ringo_c.png"},
    "*Samuel*": {"HERO_ABILITY_SAMUEL_A_NAME": "samuel_a.png", "HERO_ABILITY_SAMUEL_B_NAME": "samuel_b.png", "HERO_ABILITY_SAMUEL_C_NAME": "samuel_c.png"},
    "*SAW*": {"HERO_ABILITY_SAW_ROADIE_RUN_NAME": "saw_a.png", "HERO_ABILITY_SAW_SUPPRESSING_FIRE_NAME": "saw_b.png", "HERO_ABILITY_SAW_EXPLOSIVE_TIPPED_SHELLS_NAME": "saw_c.png"},
    "*Sayoc*": {"HERO_ABILITY_SAYOC_A": "taka_a.png", "HERO_ABILITY_SAYOC_B": "taka_b.png", "HERO_ABILITY_SAYOC_C": "taka_c.png"},
    "*Skye*": {"HERO_ABILITY_SKYE_A_NAME": "skye_a.jpg", "HERO_ABILITY_SKYE_B_NAME": "skye_b.jpg", "HERO_ABILITY_SKYE_C_NAME": "skye_c.jpg"},
    "*Vox*": {"HERO_ABILITY_VOX_A_NAME": "vox_a.png", "HERO_ABILITY_VOX_B_NAME": "vox_b.png", "HERO_ABILITY_VOX_C_NAME": "vox_c.png"},
    "*Grumpjaw*": {"HERO_ABILITY_GRUMPJAW_A_NAME": "grumpjaw_a.png", "HERO_ABILITY_GRUMPJAW_B_NAME": "grumpjaw_b.png", "HERO_ABILITY_GRUMPJAW_C_NAME": "grumpjaw_c.png"}
}

non_heroes = {
    "*JungleMinion_GoldMiner*": "Gold Miner",
    "*JungleMinion_CrystalMiner*" : "Crystal Miner",
    "*Neutral_JungleMinion_DefaultBig*": "Back Minion",
    "*Neutral_JungleMinion_DefaultSmall*": "Shop Minion",
    "*JungleMinion_TreeEnt*": " Treant",
    "*LeadMinion*": "Lane Lead Minion",
    "*TankMinion*": "Lane Tank Minion",
    "*RangedMinion*" : "Lane Ranged Minion",
    "*Kraken_Captured*": "Captured Kraken",
    "*Kraken_Jungle*" : "Kraken",
    "*Turret*" : "Turret",
    "*VainTurret*" : "Vain Turret",
    "*VainCrystalAway*": "Vain Crystal",
    "*FortressMinion*" : "Fortress Wolf"
    }


regions = {
    "eu": "Europe",
    "na": "North America",
    "sa": "South America",
    "ea": "East Asia",
    "sg": "South East Asia"
}

regions_inv = {v: k for k, v in six.iteritems(regions)}