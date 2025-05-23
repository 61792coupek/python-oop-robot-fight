import random
import time

class Robot:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.energy = 100
        self.superattack_used = False
        self.shield_used = False
        self.block_chance = 0.3
        self.recharging = False

    def check_hp(self, other):
        print("\n\033[97m======================= STAV =======================")
        print(f"{self.name}  ▶ HP: {self.hp} | Energie: {self.energy}")
        print(f"{other.name} ▶ HP: {other.hp} | Energie: {other.energy}")
        print("====================================================\033[0m\n")

    def attack(self, target):
        if self.energy < 25:
            print(f"\033[96m{self.name} nemá dost energie na útok.\033[0m")
            return False
        self.energy -= 25
        damage = 10
        if random.random() < 0.1:
            damage = 20
            print(f"\033[96mKritický zásah za 20 HP!\033[0m")
        if target.block():
            print(f"\033[95m{target.name} zablokoval útok!\033[0m")
        else:
            target.take_damage(damage)
        return True

    def block(self):
        return random.random() < self.block_chance

    def take_damage(self, amount):
        self.hp -= amount
        self.hp = max(0, self.hp)
        color = "\033[96m" if self.name != "Nepřítel" else "\033[95m"
        print(f"{color}{self.name} utrpěl {amount} poškození!\033[0m")

    def is_alive(self):
        return self.hp > 0

    def recharge_energy(self):
        self.energy = min(100, self.energy + 10)
        self.recharging = True
        print(f"\033[96m{self.name} dobíjí energii...\033[0m")

    def recharge_hp(self):
        self.hp = min(100, self.hp + 5)
        self.recharging = True
        print(f"\033[96m{self.name} regeneruje zdraví...\033[0m")

    def superattack(self, target):
        if self.superattack_used:
            print(f"\033[96mSuper útok už byl použit!\033[0m")
            return False
        if self.energy < 50:
            print(f"\033[96m{self.name} potřebuje alespoň 50 energie pro super útok. Aktuálně má {self.energy}.\033[0m")
            return False
        self.energy = 0
        self.superattack_used = True
        target.take_damage(50)
        print(f"\033[96m{self.name} provedl super útok za 50 HP!\033[0m")
        return True

    def use_shield(self, attack_amount):
        if self.shield_used:
            return False, attack_amount
        self.shield_used = True
        recovered = int(attack_amount * 0.5)
        self.hp = min(100, self.hp + recovered)
        print(f"\033[96m{self.name} použil štít a absorboval útok, získal {recovered} HP!\033[0m")
        return True, 0

def game():
    name = input("Zadejte své jméno: ")
    player = Robot(name)
    enemy = Robot("Nepřítel")
    shield_asked = False

    turn = random.choice(["player", "enemy"])
    print("\n\033[97m" + ("Začínáš ty." if turn == "player" else "Začíná soupeř.") + "\033[0m\n")
    time.sleep(1)

    while player.is_alive() and enemy.is_alive():
        player.check_hp(enemy)

        if turn == "player":
            if player.recharging:
                player.recharging = False
                print(f"\033[96m{player.name} odpočívá po dobíjení...\033[0m")
                turn = "enemy"
                continue

            valid_turn = False
            while not valid_turn:
                print("-" * 40)
                print("Vyberte, co chcete dělat:")
                print("- Útok [1]")
                print("- SuperAttack [2]")
                print("- Dobít energii [3]")
                print("- Regenerovat zdraví [4]")
                choice = input("> ")
                print("-" * 40)

                if choice == "1":
                    valid_turn = player.attack(enemy)
                elif choice == "2":
                    valid_turn = player.superattack(enemy)
                elif choice == "3":
                    player.recharge_energy()
                    valid_turn = True
                elif choice == "4":
                    player.recharge_hp()
                    valid_turn = True
                else:
                    print("\033[96mNeplatná volba.\033[0m")

            turn = "enemy"

        else:
            if enemy.recharging:
                enemy.recharging = False
                print(f"\033[95m{enemy.name} odpočívá po dobíjení...\033[0m")
                turn = "player"
                continue

            action = random.choice(["attack", "super", "re_hp", "re_en"])

            if action == "attack" and enemy.energy >= 25:
                print(f"\033[95m{enemy.name} útočí!\033[0m")
                if not shield_asked and not player.shield_used:
                    print("-" * 40)
                    print("Chcete aktivovat štít proti tomuto útoku?")
                    print("- Ano [1]")
                    print("- Ne [2]")
                    ans = input("> ")
                    print("-" * 40)
                    if ans == "1":
                        blocked, dmg = player.use_shield(10)
                        if not blocked:
                            player.take_damage(dmg)
                        shield_asked = True
                    else:
                        player.take_damage(10)
                        shield_asked = True
                else:
                    player.take_damage(10)
                enemy.energy -= 25

            elif action == "super" and not enemy.superattack_used and enemy.energy >= 50:
                print(f"\033[95m{enemy.name} použil super útok!\033[0m")
                player.take_damage(50)
                enemy.energy = 0
                enemy.superattack_used = True

            elif action == "re_hp":
                print(f"\033[95m{enemy.name} regeneruje zdraví.\033[0m")
                enemy.recharge_hp()

            else:
                print(f"\033[95m{enemy.name} dobíjí energii.\033[0m")
                enemy.recharge_energy()

            turn = "player"
        time.sleep(1)

    print("\n\033[97m--- KONEC HRY ---\033[0m")
    if player.is_alive():
        print(f"\033[97m{player.name} vyhrál!\033[0m")
    else:
        print(f"\033[97m{enemy.name} vyhrál!\033[0m")

game()