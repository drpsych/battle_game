from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

# Create Black Magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

amount = 1

# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores HP/MP of all party members", 50)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_items = [{"item": potion, "quantity": amount*15},
                {"item": hipotion, "quantity": amount*5},
                {"item": superpotion, "quantity": amount*5},
                {"item": elixer, "quantity": amount*5},
                {"item": hielixer, "quantity": amount*2},
                {"item": grenade, "quantity": amount*10}]

# Instantiate People
player = Person(460, 65, 60, 34, player_spells, player_items)
# empty [] for enemy without magic skills.
enemy = Person(1200, 65, 45, 25, [], [])

running = True
i = 0

# bcolors to wrap around text and need to end.
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("======================")
    player.choose_action()
    choice = input("Choose action: ")
    # Programming starts at 0, so change choice by -1.
    index = int(choice) - 1
# ===============================================================================

# ---------------------------- Attacks ------------------------------
    # Player chooses to physically attack.
    if index == 0:
        dmg = player.generate_damage()
        enemy.take_damge(dmg)
        print("\nYou attacked for", bcolors.FAIL + bcolors.BOLD + str(dmg) + bcolors.ENDC, "points of damage.")
    # Player chooses to use a Spell/Magic.
    elif index == 1:        # ------------------------ Magic Spells Selection ---------------------------------
        player.choose_magic()
        magic_choice = int(input("Choose spell: ")) - 1

        # Allows return back to Actions.
        if magic_choice == -1:
            continue

        spell = player.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        current_mp = player.get_mp()

        if spell.cost > current_mp:
            print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
            # Allows player to continue back to beginning of turn to choose action.
            # Instead of skipping turn.
            continue

        player.reduce_mp(spell.cost)

        if spell.type == "white":
            player.heal(magic_dmg)
            print()
            print(bcolors.OKBLUE + spell.name + bcolors.ENDC, "heals for", bcolors.OKBLUE + str(magic_dmg) + bcolors.ENDC, "HP.")
        elif spell.type == "black":
            enemy.take_damge(magic_dmg)
            print()
            print(bcolors.OKBLUE + spell.name + bcolors.ENDC, "deals", bcolors.OKBLUE + str(magic_dmg) + bcolors.ENDC,
                  "points of damage.")
    # Player chooses to use an item.
    elif index == 2:
        player.choose_item()
        item_choice = int(input("Choose item: " )) - 1
        # Allows return back to Actions.
        if item_choice == -1:
            continue

        item = player.items[item_choice]["item"]
        if player.items[item_choice]["quantity"] == 0:
            print(bcolors.FAIL + "None left..." + bcolors.ENDC)
            continue
        # player for object, .items for function in Person class of player, [item_choice] for
        # selection, ["quantity"] for selecting the key from the dictionary. And lower by 1.
        player.items[item_choice]["quantity"] -= 1


        if item.type == "potion":
            player.heal(item.prop)
            print(bcolors.OKGREEN + "\n" + item.name + bcolors.ENDC, "heals player for", bcolors.OKGREEN + str(item.prop) + bcolors.ENDC, "HP.")
        elif item.type == "elixer":
            player.hp = player.maxhp
            player.mp = player.maxmp
            print(bcolors.OKGREEN + "\n" + item.name + bcolors.ENDC, "fully restores your HP/MP.")
        elif item.type == "attack":
            enemy.take_damge(item.prop)
            print(bcolors.FAIL + item.name + bcolors.ENDC, "deals", bcolors.FAIL + str(item.prop) + bcolors.ENDC, "points of damage.")


# ------------------------------ Damage Section --------------------------------------
    enemy_choice = 1

    enemy_dmg = enemy.generate_damage()
    player.take_damge(enemy_dmg)
    print("Enemy attacks for", bcolors.FAIL + bcolors.BOLD + str(enemy_dmg) + bcolors.ENDC, "points of damage.")

    print("----------------------")
    print("Enemgy HP:", bcolors.OKGREEN + bcolors.BOLD + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC)
    print("Your HP:", bcolors.OKGREEN + bcolors.BOLD + str(player.get_hp()) + "/" + str(player.get_max_hp()) + bcolors.ENDC)
    print("Your MP:", bcolors.OKBLUE + bcolors.BOLD + str(player.get_mp()) + "/" + str(player.get_max_mp()) + bcolors.ENDC, "\n")

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You WIN!" + bcolors.ENDC)
        running = False
    elif player.get_hp() == 0:
        print(bcolors.FAIL + "Your enemy has DEFEATED you!" + bcolors.ENDC)
        running = False
