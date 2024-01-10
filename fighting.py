import random
import tabulate
import inquirer
from rich import print as rprint


def announce_elem_dmg(target, adressing1, adressing2):
    if target.afflicted["poisoned"] > 0 and target.afflicted["burning"] > 0:
        return f"""{adressing1} [red3]afflicted[/red3] by burn and poison.
At the end of the turn {adressing2} will recieve {target.elem_damage["poison_damage"]+target.elem_damage["burn_damage"]} damage."""
    if target.afflicted["poisoned"] > 0:
        return f"""{adressing1} [red3]afflicted[/red3] by poison.
At the end of the turn {adressing2} will recieve {target.elem_damage["poison_damage"]} damage."""
    if target.afflicted["burning"] > 0:
        return f"""{adressing1} [red3]afflicted[/red3] by burn.
At the end of the turn {adressing2} will recieve {target.elem_damage["burn_damage"]} damage."""
    return False


def player_act(player, monster):
    if not player.stunned:
        player_actions_available = [
            action for action in player.actions if player.cooldown[action] == 0
        ]
        print("Your abilities:")
        abilities = [
            [action, player.get_action_descr(action)] for action in player_actions_available
        ]
        rprint(tabulate.tabulate(abilities, headers=["Name","Description"], tablefmt="simple_grid"))

        question = [
            inquirer.List("player_action",
                message="What do you do?",
                choices=player_actions_available)
        ]
        player_action = inquirer.prompt(question)
        result = player.perform_action(player_action["player_action"], monster)
        rprint(f"[bold spring_green2]Your action[/bold spring_green2]: [bold]{result}[/bold]")
    else:
        rprint("You are [light_goldenrod3]stunned[/light_goldenrod3] and cannot act.")
        player.stunned = False


def monster_act(monster, player):
    if not monster.stunned:
        monster_actions_available = [
            action for action in monster.actions if monster.cooldown[action] == 0
        ]
        if "heal" in monster_actions_available and monster.hp == monster.max_hp:
            monster_actions_available.pop(monster_actions_available.index("heal"))
        if "debuff" in monster_actions_available and player.debuffed:
            monster_actions_available.pop(monster_actions_available.index("debuff"))
        monster_action = random.choice(monster_actions_available)
        return f"[bold red3]{monster.name}'s action[/bold red3]: [bold]{monster.perform_action(monster_action, player)}[/bold]"
    else:
        monster.stunned = False
        return f"The {monster.name} is [light_goldenrod3]stunned[/light_goldenrod3]."


def reduce_cooldown(target):
    for action in target.cooldown:
        if target.cooldown[action] > 0:
            target.cooldown[action] -= 1


def elemental_damage(victim, damage_type, damage):
    if victim.elem_damage[damage]:
        victim.hp -= victim.elem_damage[damage]
        victim.afflicted[damage_type] -= 1
    if victim.afflicted[damage_type] == 0:
        victim.elem_damage[damage] = 0
