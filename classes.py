class Player:
    def __init__(self):
        self.lv = 1

        self.hp = 120
        self.max_hp = 120

        self.dodge = False
        self.turn_bonus = 0

        self.stunned = False
        self.debuffed = False
        self.afflicted = {"debuff": 0, "burning": 0, "poisoned": 0}
        self.elem_damage = {"poison_damage": 0, "burn_damage": 0}

        self.damage_mult = 1


class Warrior(Player):
    def __init__(self):
        super().__init__()
        self.attack = 25

        self.actions = [
            "normal_attack",
            "shield_bash",
            "blessing_of_healing",
            "charge",
            "divine_fire",
        ]
        self.cooldown = {
            "normal_attack": 0,
            "shield_bash": 0,
            "blessing_of_healing": 0,
            "charge": 0,
            "divine_fire": 0,
        }

    def get_action_descr(self, action):
        actions = {
            "normal_attack": f"Strike the enemy. Deals {int(self.attack * self.damage_mult)} damage",
            "shield_bash": f"Hit the enemy and [light_goldenrod3]stun[/light_goldenrod3] them. Deals {int(self.attack * self.damage_mult * 0.3)} damage. Cooldown for 2 turns.",
            "blessing_of_healing": "[sea_green3]Heals[/sea_green3] 20 health. Cooldown for 2 turns.",
            "charge": "Give yourself more strength. All your subsequent attacks will be [red]20% stronger[/red]. Cooldown for 1 turn.",
            "divine_fire": f"""Summon rain of fire to deal {int(self.attack * self.damage_mult * 2)} damage and inflict
10 [dark_orange3]burn[/dark_orange3] damage in exchange of 30 damage to yourself. Can be used once per battle.""",
        }
        return actions[action]

    def perform_action(self, action, enemy):
        match action:
            case "normal_attack":
                return self.normal_attack(enemy)
            case "shield_bash":
                return self.shield_bash(enemy)
            case "blessing_of_healing":
                return self.blessing_of_healing()
            case "charge":
                return self.charge()
            case "divine_fire":
                return self.divine_fire(enemy)

    def normal_attack(self, enemy):
        damage = int(self.attack * self.damage_mult)
        enemy.hp -= damage
        return f"You strike the {enemy.name} with your sword."

    def shield_bash(self, enemy):
        damage = int(self.attack * self.damage_mult * 0.3)
        enemy.hp -= damage
        enemy.stunned = True
        self.cooldown["shield_bash"] += 3
        return f"You have stunned the enemy! {enemy.name} loses their next turn."

    def blessing_of_healing(self):
        healed = self.hp + 20
        if healed > self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp = healed
        self.cooldown["blessing_of_healing"] += 2
        return f"The gods hear you and grant you their blessing. Now your health is {self.hp}"

    def charge(self):
        self.damage_mult += 0.2
        self.cooldown["charge"] += 2
        return f"Your grip your blade tighter and focus your strength. Your subsequent atacks will be 20% stronger."

    def divine_fire(self, enemy):
        self.hp -= 30
        enemy.hp -= int(self.attack * self.damage_mult * 2)
        enemy.afflicted["burning"] += 2
        enemy.elem_damage["burn_damage"] += 10
        self.cooldown["divine_fire"] += 9999
        return "You pray to gods of war and summon fire rain. It burns your foe but you get caught in it as well."


class Rogue(Player):
    def __init__(self):
        super().__init__()
        self.attack = 20

        self.actions = [
            "normal_attack",
            "poison_dagger",
            "lifesteal",
            "evasion",
            "shadow_dance",
        ]
        self.cooldown = {
            "normal_attack": 0,
            "poison_dagger": 0,
            "lifesteal": 0,
            "evasion": 0,
            "shadow_dance": 0,
        }

    def get_action_descr(self, action):
        actions = {
            "normal_attack": f"Strike the enemy. Deals {int(self.attack * self.damage_mult)} damage",
            "poison_dagger": f"Hit the enemy and [magenta]poison[/magenta] them. Deals {int(self.attack * self.damage_mult * 0.3)} damage and gives 12 poison damage for 2 turns. Cooldown for 1 turn.",
            "lifesteal": "Deal 10 damage to the enemy and [sea_green3]heal[/sea_green3] 10 health. Cooldown for 2 turns.",
            "evasion": "Next enemy attack will be [red]dodged[/red]. Cooldown for 2 turns.",
            "shadow_dance": f"""Use blades of shadow to deal {int(6 * self.damage_mult * self.turn_bonus)} damage. Potential damage increases with every passing turn. Can be used once per battle.""",
        }
        return actions[action]

    def perform_action(self, action, enemy):
        match action:
            case "normal_attack":
                return self.normal_attack(enemy)
            case "poison_dagger":
                return self.poison_dagger(enemy)
            case "lifesteal":
                return self.lifesteal(enemy)
            case "evasion":
                return self.evasion()
            case "shadow_dance":
                return self.shadow_dance(enemy)

    def normal_attack(self, enemy):
        damage = int(self.attack * self.damage_mult)
        enemy.hp -= damage
        return f"You strike the {enemy.name} with your knife."

    def poison_dagger(self, enemy):
        damage = int(self.attack * self.damage_mult * 0.3)
        enemy.hp -= damage
        enemy.afflicted["poisoned"] = 3
        enemy.elem_damage["poison_damage"] = 12
        self.cooldown["poison_dagger"] += 2
        return f"You trow your [magenta]poisoned dagger[/magenta] into the {enemy.name}'s flesh. They shall recieve 12 damage for next 2 turns."

    def lifesteal(self, enemy):
        enemy.hp -= 10
        healed = self.hp + 10
        if healed > self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp = healed
        self.cooldown["lifesteal"] += 3
        return f"You use the dark art to drain enemy's life. Enemy takes 10 damage and now your health is {self.hp}."

    def evasion(self):
        self.dodge += True
        self.cooldown["evasion"] += 3
        return f"You focus and walk with the shadows. You will evade the next attack."

    def shadow_dance(self, enemy):
        damage = int(6 * self.damage_mult * self.turn_bonus)
        enemy.hp -= damage
        self.cooldown["shadow_dance"] += 9999
        return f"Your blades are drenched in shadows and you unleash them on {enemy.name}. The {enemy.name} takes {damage} damage!"
