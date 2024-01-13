from fighting import *


def boss_fight(monster1, monster2, player, ascii):
    print(
        f"You are versing the Chimera. It is said that chimera has two minds in one body."
    )
    print(ascii["chimera"])

    while (monster1.hp > 0 or monster2.hp > 0) and player.hp > 0:
        rprint(f"Your health is [bold spring_green2]{player.hp}[/bold spring_green2].")
        if monster1.hp > 0:
            rprint(
                f"The {monster1.name}'s health is [bold red3]{monster1.hp}[/bold red3]."
            )
        if monster2.hp > 0:
            rprint(
                f"The {monster2.name}'s health is [bold red3]{monster2.hp}[/bold red3]."
            )

        player_elem_dmg = announce_elem_dmg(player, "You are", "you")
        if player_elem_dmg:
            rprint(player_elem_dmg)
        if monster1.hp > 0:
            elem_damage(monster1)
        if monster2.hp > 0:
            elem_damage(monster2)

        initial_player_health = player.hp
        heads = []
        if monster1.hp > 0:
            heads.append(monster1)
        if monster2.hp > 0:
            heads.append(monster2)

        monster_pick = [
            inquirer.List(
                "attack",
                message="Who would you like to attack?",
                choices=[head.name for head in heads],
            )
        ]
        monster_choice = inquirer.prompt(monster_pick)
        if monster_choice["attack"] == monster1.name:
            player_act(player, monster1)
        else:
            player_act(player, monster2)

        if monster1.hp <= 0 and monster2.hp <= 0:
            break
        rage(monster1, monster2)
        rage(monster2, monster1)

        for head in heads:
            if head.hp > 0:
                m_act = monster_act(head, player)
                if player.dodge and player.hp < initial_player_health:
                    player.hp = initial_player_health
                    player.dodge = False
                    print(f"You evade the {head.name}'s attack.")
                else:
                    rprint(m_act)
                if player.hp <= 0:
                    break

        elemental_damage(player, "poisoned", "poison_damage")
        elemental_damage(player, "burning", "burn_damage")
        if monster1.hp > 0:
            elemental_damage(monster1, "poisoned", "poison_damage")
            elemental_damage(monster1, "burning", "burn_damage")
        if monster2.hp > 0:
            elemental_damage(monster2, "poisoned", "poison_damage")
            elemental_damage(monster2, "burning", "burn_damage")

        reduce_cooldown(monster1)
        reduce_cooldown(monster2)
        reduce_cooldown(player)

        if player.debuffed and player.afflicted["debuff"] == 0:
            player.damage_mult += 0.25
            player.debuffed = False

        if player.debuffed:
            player.afflicted["debuff"] -= 1
        player.turn_bonus += 1
        print("=" * 30, "End of the turn", "=" * 30, "\n")

    player.turn_bonus = 0
    if player.hp <= 0:
        print("Unfortunately you have perished.")
    else:
        rprint("The [deep_pink2]victory[/deep_pink2] is yours. Congratulations.")


def elem_damage(target):
    elem_dmg = announce_elem_dmg(target, f"{target.name} is", target.name)
    if elem_dmg:
        rprint(elem_dmg)


def rage(target, actor):
    if target.hp <= 0 and actor.rage == False:
        print(
            f"{actor.name} roars in blind rage. {actor.name}'s attack increased by two times!"
        )
        actor.stunned = True
        actor.rage = True
        actor.dmg_mult = 2
