    # Castles and Chimeras
    #### Video Demo:  https://youtu.be/myG8nQBJua4
    #### Description: A small RPG-session via terminal that allows player to be an adventurer and fight monsters.

    The D&D-inspired RPG that has two playable classes with unique skills: warrior and rogue, and three bosses to fight(troll, golem and chimera).
    The combat is turn-based and player has to choose the ability to use in combat every turn.
    
    There are several mechanics in game's combat, such as stun, elemental damage and buffs to stats.
    Stunning an enemy means that they lose next turn and potential charges they made on their previous turn to enable stronger attacks.
    While poison and fire are active, they take effect at the end of turn, depleting certain ammount of health.
    Healing allows to recover a portion of health.
    And finally, buffs and debuffs allow to strengthen or weaken attack power.
    The game uses command terminal to prompt player for actions and show status of the fight.

    #### Project files
    1. castle.txt, chimera.txt, golem.txt, treasure.txt, troll.txt - ASCII art shown during the game;
    2. fighting.py - functions, powering base mechanics that make game's combat;
    3. final_boss.py - functions, used exclusively for fight with the final boss of the game;
    4. project.py - main file of the project;
    5. requirements.txt - external libraries used;
    6. test_project.py - mandatory pytest file;
    7. classes.py - classes that make "game classes" user can choose to play as;
    8. monsters.py - classes that form the behaviour of enemies in game's combat;
