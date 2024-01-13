import inquirer
from rich import print as rprint
from fighting import *
from final_boss import boss_fight
from classes import *
from monsters import *


def main():
    # Prepare
    ascii_art = {}
    art_files = ["castle", "chimera", "golem", "treasure", "troll"]
    for art in art_files:
        art_path = f"./ascii_art/{art}.txt"
        get_art(ascii_art, art_path, art)

    # Tutorial
    print(
        "Welcome to a little game, that allows you to take a role of an adventurer, on a search for treasure.",
        "You have heard, that a nearby castle has gold hidden within, but it is guarded by three monsters, that you will have to defeat.",
    )
    print(ascii_art["castle"])

    print(
        "First, you need to pick a class. Each have their own set of skills that you have to utilize to defeat the monsters",
        "You can be either Warrior or Rogue",
    )
    player = get_class()
    showing_tutorial()

    # Level 1
    print(
        "You are in the woods, on a path that leads to the castle. The trees shake around you and the troll blocks your path."
    )
    troll = Troll()
    fight(troll, player, ascii_art)

    # Level 2
    if player.hp > 0:
        leveled = level_up(player)
        print(leveled)
        print(
            "Having defeated the troll, you proceed into the castle. The halls are long and narrow, and eventually you bump into the door,",
            "guarded by the terrifying golem-watcher.",
        )
        proceeding = [
            inquirer.List(
                "proceed",
                message="Press enter when you are ready to continue",
                choices=["Continue"],
            )
        ]
        inquirer.prompt(proceeding)
        golem = Golem()
        fight(golem, player, ascii_art)

    # Level 3
    if player.hp > 0:
        leveled = level_up(player)
        print(leveled)
        print(
            "The golem falls and you proceed further. You feel that you are close - the tresuary is right in front of you,",
            "but there is one more obstacle - a deadly Chimera.",
        )
        proceeding = [
            inquirer.List(
                "proceed",
                message="Press enter when you are ready to continue",
                choices=["Continue"],
            )
        ]
        inquirer.prompt(proceeding)
        head1 = Goat_Head()
        head2 = Lion_Head()
        boss_fight(head1, head2, player, ascii_art)

    # Ending
    if player.hp > 0:
        print(
            "You overcame all your trials and found the treasure! Never again will you have to worry about the money again, and your future looks as bright as ever."
        )
        print(ascii_art["treasure"])
        print("Thank you for playing!")


def get_art(art_lib, target, art_name):
    with open(target) as file:
        lines = []
        for line in file:
            lines.append(line)
        art_lib[art_name] = "".join(lines)


def get_class():
    classes = ["warrior", "rogue"]
    while True:
        chosen_class = (
            input("Type 'warrior' or 'rogue' to pick your class: ").strip().lower()
        )
        if not chosen_class in classes:
            print("That's not a class!")
        else:
            break
    if chosen_class == "warrior":
        return Warrior()
    return Rogue()


def showing_tutorial():
    tut_question = [
        inquirer.List(
            "tutorial",
            message="Would you like a tutorial on combat mechanics?",
            choices=["Yes", "No"],
        )
    ]
    show_tutorial = inquirer.prompt(tut_question)
    if show_tutorial["tutorial"] == "Yes":
        rprint(
            "The combat is turn-based. You go first, so you have an advantage. You win if enemy's health drops to 0.\n",
            "[light_goldenrod3]Stunning[/light_goldenrod3] an enemy means that they lose next turn and potential charges they made on their previous turn",
            "to enable [red]stronger attacks[/red].\n",
            "While [magenta]poison[/magenta] and [dark_orange3]fire[/dark_orange3] are active, they take effect at the end of turn, "
            "depleting certain ammount of health.\n",
            "[sea_green3]Healing[/sea_green3] allows you to recover a portion of your health, but you cannot heal past your max health threshold.\n",
            "And finally, [red]buffs[/red] and [bright_magenta]debuffs[/bright_magenta] allow to strengthen or weaken attack power.\n",
            "Both you, and your enemies can be affected by status effects mentioned. Good luck!\n",
        )
        proceeding = [
            inquirer.List(
                "proceed",
                message="Press enter when you are ready to start the game",
                choices=["Continue"],
            )
        ]
        inquirer.prompt(proceeding)


def fight(monster, player, ascii):
    print(f"You are versing the {monster.name}")
    print(ascii[monster.name.lower()])

    while monster.hp > 0 and player.hp > 0:
        rprint(
            f"Your health is [bold spring_green2]{player.hp}[/bold spring_green2].",
            f"\nThe {monster.name}'s health is [bold red3]{monster.hp}[/bold red3].",
        )

        player_elem_dmg = announce_elem_dmg(player, "You are", "you")
        if player_elem_dmg:
            rprint(player_elem_dmg)
        monster_elem_dmg = announce_elem_dmg(
            monster, f"{monster.name} is", monster.name
        )
        if monster_elem_dmg:
            rprint(monster_elem_dmg)

        initial_player_health = player.hp
        player_act(player, monster)
        if monster.hp <= 0:
            break
        m_act = monster_act(monster, player)
        if player.dodge and player.hp < initial_player_health:
            player.hp = initial_player_health
            player.dodge = False
            print(f"You evade the {monster.name}'s attack.")
        else:
            rprint(m_act)
        if player.hp <= 0:
            break

        elemental_damage(player, "poisoned", "poison_damage")
        elemental_damage(player, "burning", "burn_damage")
        elemental_damage(monster, "poisoned", "poison_damage")
        elemental_damage(monster, "burning", "burn_damage")

        reduce_cooldown(monster)
        reduce_cooldown(player)

        player.turn_bonus += 1
        print("=" * 30, "End of the turn", "=" * 30, "\n")

    player.damage_mult = 1
    player.turn_bonus = 0
    if player.hp <= 0:
        print("Unfortunately you have perished.")
    else:
        rprint("The [deep_pink2]victory[/deep_pink2] is yours.")


def level_up(player):
    player.hp = player.max_hp
    rprint(f"You rested and [sea_green3]fully recovered your health[/sea_green3].")

    for ability in player.cooldown:
        player.cooldown[ability] = 0
    for effect in player.afflicted:
        player.afflicted[effect] = 0
    for effect in player.elem_damage:
        player.elem_damage[effect] = 0
    if player.lv == 1:
        player.max_hp += 20
        player.lv = 2
        player.hp = player.max_hp
        return "\nYou leveled up. Your health increased by 20."
    else:
        player.attack += 5
        player.lv = 3
        return "\nYou leveled up. Your attack increased by 5."


if __name__ == "__main__":
    main()
