class Troll:
    def __init__(self):
        self.name = "Troll"
        self.actions = ["normal_attack", "rotten_strike", "heal", "nothing"]

        self.hp = 150
        self.max_hp = 150
        self.attack = 25

        self.stunned = False
        self.afflicted = {
            "burning": 0,
            "poisoned": 0
        }
        self.elem_damage = {
            "poison_damage": 0,
            "burn_damage": 0
        }

        self.cooldown = {
            "normal_attack": 0,
            "rotten_strike": 0,
            "heal": 0,
            "nothing": 0
        }


    def perform_action(self, action, enemy):
        match action:
            case "normal_attack":
                return self.normal_attack(enemy)
            case "rotten_strike":
                return self.rotten_strike(enemy)
            case "heal":
                return self.heal()
            case "nothing":
                return self.nothing()


    def normal_attack(self, enemy):
        enemy.hp -= self.attack
        return "The Troll strikes you with his club."


    def rotten_strike(self, enemy):
        enemy.hp -= int(self.attack * 0.5)
        if not enemy.dodge:
            enemy.afflicted["poisoned"] += 2
            enemy.elem_damage["poison_damage"] += 10
        self.cooldown["rotten_strike"] += 2
        return f"Troll hits your arm with the club. The snag pierces your armor and leaves a wound with a rotten stench to it.\nYou will recieve 10 poison damage in the start of next 2 turns."


    def heal(self):
        healed = self.hp + 25
        if healed > self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp = healed
        self.cooldown["heal"] += 2
        return "The troll takes out a putrid-looking lump of meat and swallowes it whole. Troll recovered health."


    def nothing(self):
        self.cooldown["nothing"] += 4
        return "Troll scratches his head. It seems that this movement-filled battle is too much work for his brain."


class Golem:
    def __init__(self):
        self.name = "Golem"

        self.hp = 200
        self.max_hp = 200
        self.attack = 30

        self.afflicted = {
            "burning": 0,
            "poisoned": 0
        }
        self.elem_damage = {
            "poison_damage": 0,
            "burn_damage": 0
        }

        self.cooldown = {
            "normal_attack": 0,
            "charge_core": 0,
            "blinding_blast": 0,
            "burning_lazer": 0,
            "energy_overload": 9999
        }
        self.stunned = False


    @property
    def actions(self):
        if self.cooldown["energy_overload"] == 0:
            return ["energy_overload"]
        return ["normal_attack", "charge_core", "blinding_blast", "burning_lazer"]


    @property
    def stunned(self):
        return self._stunned


    @stunned.setter
    def stunned(self, value):
        if self.cooldown["energy_overload"] == 0:
            self.cooldown["energy_overload"] = 9999
        self._stunned = value


    def perform_action(self, action, enemy):
        match action:
            case "normal_attack":
                return self.normal_attack(enemy)
            case "charge_core":
                return self.charge_core()
            case "blinding_blast":
                return self.blinding_blast(enemy)
            case "burning_lazer":
                return self.burning_lazer(enemy)
            case "energy_overload":
                return self.energy_overload(enemy)


    def normal_attack(self, enemy):
        enemy.hp -= self.attack
        self.cooldown["normal_attack"] = 2
        return "The Golem hits you with his metalic arm."


    def charge_core(self):
        self.cooldown["energy_overload"] = 0
        self.cooldown["charge_core"] += 3
        return "Golem's core [red]starts glowing[/red] intensely. You feel like something [red]terrifying[/red] is coming."


    def burning_lazer(self, enemy):
        if not enemy.dodge:
            enemy.afflicted["burning"] += 2
            enemy.elem_damage["burn_damage"] += 10
        self.cooldown["burning_lazer"] += 3
        return "Golem strikes you with the lazer from his chest. You feel your armor burning."


    def blinding_blast(self, enemy):
        enemy.hp -= int(self.attack * 0.3)
        if not enemy.dodge:
            enemy.stunned = True
        self.cooldown["blinding_blast"] += 3
        return "Golem strikes you with the energy blast, temporarily blinding you. You are stunned for 1 turn."


    def energy_overload(self, enemy):
        enemy.hp -= int(self.attack * 1.8)
        self.cooldown["energy_overload"] = 9999
        return f"Golem sends out huge wave of energy knocking you off your feet. You took {int(self.attack * 1.8)} damage"


class Goat_Head:
    def __init__(self):
        self.name = "Goat head"
        self.rage = False

        self.hp = 150
        self.max_hp = 150
        self.attack = 15

        self.afflicted = {
            "burning": 0,
            "poisoned": 0
        }
        self.elem_damage = {
            "poison_damage": 0,
            "burn_damage": 0
        }

        self.cooldown = {
            "normal_attack": 0,
            "charge_ram": 0,
            "heal": 0,
            "poison_spit": 0,
            "nothing": 0,
            "ram_over": 9999
        }
        self.stunned = False
        self.dmg_mult = 1


    @property
    def actions(self):
        if self.cooldown["ram_over"] == 0:
            return ["ram_over"]
        return ["normal_attack", "charge_ram", "heal", "poison_spit", "nothing"]


    @property
    def stunned(self):
        return self._stunned


    @stunned.setter
    def stunned(self, value):
        if self.cooldown["ram_over"] == 0:
            self.cooldown["ram_over"] = 9999
        self._stunned = value


    def perform_action(self, action, enemy):
        match action:
            case "normal_attack":
                return self.normal_attack(enemy)
            case "charge_ram":
                return self.charge_ram()
            case "heal":
                return self.heal()
            case "ram_over":
                return self.ram_over(enemy)
            case "poison_spit":
                return self.poison_spit(enemy)
            case "nothing":
                return self.nothing()


    def normal_attack(self, enemy):
        enemy.hp -= int(self.attack * self.dmg_mult)
        return "Goat head hits you with its horns."


    def poison_spit(self, enemy):
        enemy.hp -= int(self.attack * self.dmg_mult * 0.3)
        if not enemy.dodge:
            enemy.afflicted["poisoned"] += 2
            enemy.elem_damage["poison_damage"] += 8
        self.cooldown["poison_spit"] += 3
        return "Goat head convinces snake tail to spit venom at you. You are poisoned."


    def charge_ram(self):
        self.cooldown["ram_over"] = 0
        self.cooldown["charge_ram"] += 3
        return "Goat side of body [red]digs the ground with its hoof[/red]. You feel like something [red]terrifying[/red] is coming."


    def heal(self):
        healed = self.hp + 15
        if healed > self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp = healed
        self.cooldown["heal"] += 2
        return "Goat head eats some red moss and heals 15 damage."


    def ram_over(self, enemy):
        enemy.hp -= int(self.attack * 2 * self.dmg_mult)
        self.cooldown["ram_over"] = 9999
        return f"Chimera roars and charges at you with its massive body, ramming you over. You took {int(self.attack * 2.5 * self.dmg_mult)} damage"


    def nothing(self):
        self.cooldown["nothing"] = 2
        return "Goat head points its horns at you tauntingly."


class Lion_Head:
    def __init__(self):
        self.name = "Lion head"
        self.rage = False
        self.actions = ["normal_attack", "debuff", "heal", "burn_orb", "nothing"]

        self.hp = 140
        self.max_hp = 140
        self.attack = 12

        self.afflicted = {
            "burning": 0,
            "poisoned": 0
        }
        self.elem_damage = {
            "poison_damage": 0,
            "burn_damage": 0
        }

        self.cooldown = {
            "normal_attack": 0,
            "debuff": 0,
            "heal": 0,
            "burn_orb": 0,
            "nothing": 0
        }
        self.stunned = False
        self.dmg_mult = 1


    def perform_action(self, action, enemy):
        match action:
            case "normal_attack":
                return self.normal_attack(enemy)
            case "debuff":
                return self.debuff(enemy)
            case "heal":
                return self.heal()
            case "burn_orb":
                return self.burn_orb(enemy)
            case "nothing":
                return self.nothing()


    def normal_attack(self, enemy):
        enemy.hp -= int(self.attack * self.dmg_mult)
        return "Lion's head bites you."


    def debuff(self, enemy):
        enemy.debuffed = True
        enemy.damage_mult -= 0.25
        enemy.afflicted["debuff"] = 2
        self.cooldown["debuff"] += 3
        return "Lion head bashes your arm. Your attacks are [bright_magenta]25% weaker[/bright_magenta] for 2 turns."


    def heal(self):
        healed = self.hp + 12
        if healed > self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp = healed
        self.cooldown["heal"] += 3
        return "Lion head lick its wounds and heals 15 damage."


    def burn_orb(self, enemy):
        enemy.hp -= int(self.attack * self.dmg_mult * 0.2)
        if not enemy.dodge:
            enemy.afflicted["burning"] += 2
            enemy.elem_damage["burn_damage"] += 8
        self.cooldown["burn_orb"] = 3
        return f"Lion head throws firball to you. You will take 9 burning damage."


    def nothing(self):
        self.cooldown["nothing"] = 2
        return f"Lion head roars threateningly."
