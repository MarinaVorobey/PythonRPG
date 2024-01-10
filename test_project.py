from project import *
import classes


def test_level_up():
    warrior = classes.Warrior()
    level_up(warrior)
    assert warrior.hp == 140
    level_up(warrior)
    assert warrior.attack == 30


def test_congrats():
    assert congrats() == "You overcame all your trials and found the treasure! Never again will you have to worry about the money again, and your future looks as bright as ever."


def test_announce_class():
    assert announce_class("warrior") == "You have chosen the warrior"
    assert announce_class("rogue") == "You have chosen the rogue"
