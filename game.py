import os
import pickle
from random import randint


class Character:
    def __init__(self, name, health, mana):
        self.name = name
        self.health = health
        self.mana = mana

    def change_health(self, value):
        self.health = self.health + value
        if self.health > 100:
            self.health = 100

        if self.health < 0:
            self.health = 0

    def change_mana(self, value):
        self.mana = self.mana + value
        if self.mana > 100:
            self.mana = 100

        if self.mana < 0:
            self.mana = 0


class Hero(Character):
    def __init__(self):
        self.name = ""
        self.health = 100
        self.mana = 100
        self.got_skills = [0, 1, 2, 3, 4]

    def add_skill(self, value):
        self.got_skills.append(value)

    def remove_skill(self, value):
        self.got_skills.remove(value)


class Evil(Character):
    def __init__(self):
        self.name = ""
        self.health = randint(15, 50)
        self.mana = 100
        self.skills = [1, 2, randint(3, 12)]


class Skill:
    def __init__(self, name, damage, mana):
        self.name = name
        self.damage = damage
        self.mana = mana


player = Hero()
enemy_health_change = list()
skills = [Skill("Побег", 0, 0),
          Skill("Уклонение", 0, 0),
          Skill("Атака мечем", 5, 0),
          Skill("Огненный шар", 20, 40),
          Skill("Ледяной удар", 15, 20),
          Skill("Волна огня", 8, 23),
          Skill("Ледяная стрела", 10, 20),
          Skill("Чародейские стрелы", 11, 22),
          Skill("Ледяное копье", 30, 80),
          Skill("Волшебная вспышка", 13, 20),
          Skill("Чародейский взрыв", 10, 15),
          Skill("Огненная глыба", 12, 22),
          Skill("Гнев титана", 40, 81)]


def menu():
    os.system('cls')
    print("1. Начать новую игру")
    print("2. Загрузить игру")
    print("3. Выйти")
    choice = input("-> ")
    if choice == '1':
        new_game()
    elif choice == '2':
        if os.path.exists("save"):
            os.system('cls')
            with open('save', 'rb') as read:
                global player
                player = pickle.load(read)
            print("Персонаж загружен!")
            choice = input("Нажмите \"enter\", чтобы продолжить\n")
            os.system('cls')
            free_mode()
        else:
            print("Нет сохранений")
            choice = input("Нажмите \"enter\", чтобы продолжить\n")
            menu()

    elif choice == '3':
        exit()
    else:
        menu()


def new_game():
    os.system('cls')
    print("Приветствую тебя дорогой друг!")
    print("Для начала ты должен выбрать себе имя.")
    print("Как ты хочешь, чтобы тебя звали?")
    name = input('-> ')
    player.name = name
    os.system('cls')
    choice = ""
    mistake = True
    while mistake:
        print(player.name + ", хочешь узнать правила?(да/нет)")
        choice = input("-> ")
        if choice == "да" or choice == "нет":
            mistake = False
        else:
            print("     |Введи \"да\" или \"нет\"|")
    if choice == "да":
        rules()
    else:
        os.system('cls')
        free_mode()


def show_skills():
    player.got_skills.sort()
    print("#######################################################")
    print("Доступные навыки:")
    for i in player.got_skills:
        print("|индекс: " + str(i) + "|   |" + str(skills[i].name) + "|    |урон: " + str(
            skills[i].damage) + "|     |мана: " + str(skills[i].mana) + "|")


def fight_status():
    print("_______________________________________________________ \n")
    print("Здоровье героя: " + str(player.health) + "            Здоровье противника: " + str(enemy.health))
    print("Мана героя: " + str(player.mana) + "                 Мана противника: " + str(enemy.mana))
    print("_______________________________________________________")


def enemy_show_skills():
    print("Уникальный навык противника:")
    print("|индекс: " + str(enemy.skills[2]) + "|   |" + str(skills[enemy.skills[2]].name) + "|    |урон: " + str(
        skills[enemy.skills[2]].damage) + "|     |мана: " + str(skills[enemy.skills[2]].mana) + "|")
    print("#######################################################")


def status():
    player.got_skills.sort()
    print("#######################################################")
    print("Доступные навыки:")
    for i in player.got_skills:
        print("|индекс: " + str(i) + "|   |" + str(skills[i].name) + "|    |урон: " + str(
            skills[i].damage) + "|     |мана: " + str(skills[i].mana) + "|")
    print("_____________________________________ \n")
    print("Здоровье героя: " + str(player.health))
    print("Мана героя: " + str(player.mana))
    print("____________________________________")


def fight_start(rested=False):
    os.system('cls')
    if rested:
        damage = randint(10, 20)
        print("Противник напал со спины и нанес " + str(damage) + " урона")
        player.change_health(-damage)
        if player.health == 0:
            defeat()
    print("                       Начало боя!")
    global enemy
    enemy = Evil()
    show_skills()
    fight_status()
    enemy_show_skills()
    fight_action()


def fight_action():
    print("Твое действие:")
    action = input("-> ")
    if not action.isdigit():
        print("Нельзя использовать этот навык!")
        fight_action()
    if int(action) in player.got_skills:
        if skills[int(action)].mana > player.mana:
            print("Нет маны, используй другой навык")
            fight_action()
        end_turn(int(action))
    else:
        print("Нельзя использовать этот навык!")
        fight_action()


def end_turn(action):
    if action > 2:
        player.remove_skill(action)
    enemy_health_change.append(enemy.health)
    enemy_action = randint(1, 100)
    if enemy_action <= 20:
        enemy_action = 1
    elif enemy_action <= 60:
        enemy_action = 2
    elif enemy_action <= 100:
        enemy_action = 3
    if enemy_action == 3:
        enemy_action = enemy.skills[2]  # присвоение индекса атаки
        if enemy.mana < skills[enemy_action].mana:  # ограничение бота по мане
            enemy_action = randint(1, 2)
    enemy_dodge = False
    player_dodge = False
    player_damage = -skills[action].damage
    enemy_damage = -skills[enemy_action].damage
    if enemy_action == 1:
        enemy_dodge = dodge(action)
    if action == 1:
        player_dodge = dodge(enemy_action)
    if player_dodge:
        enemy_damage = 0
    if enemy_dodge:
        player_damage = 0
    enemy.change_health(player_damage)  # нанесенный игроком урон
    player.change_mana(-skills[action].mana)  # расход маны игрока
    player.change_mana(10)
    player.change_health(enemy_damage)  # нанесенный противником урон
    enemy.change_mana(-skills[enemy_action].mana)  # расход маны противника
    enemy.change_mana(10)
    show_skills()
    fight_status()
    enemy_show_skills()
    if action == 1 and enemy_action == 1:
        print("Вы оба использовали уклонение :D")
    else:
        print("Г:   Ты использовал: " + skills[action].name)
        if action == 0:
            flee()
        if player_dodge:
            print("     Уклонение прошло успешно!\n")
        elif player_dodge == False and action == 1:
            print("     Уклонение не удалось\n")
        print("П:   Противник использовал: " + skills[enemy_action].name)
        if enemy_dodge:
            print("     Уклонение противника прошло успешно\n")
        elif enemy_dodge == False and enemy_action == 1:
            print("     Противник не смог уклониться")

    if player.health == 0:
        defeat()
    elif enemy.health == 0:
        victory(enemy_health_change[0] // 2)

    fight_action()


def dodge(action):
    luck = randint(1, 100)
    if action == 2:
        if 1 <= luck <= 80:
            return True
        else:
            return False
    else:
        if 1 <= luck <= 50:
            return True
        else:
            return False


def flee():
    luck = randint(1, 100)
    if luck <= player.health:
        os.system('cls')
        print("Побег от врага удался!")
        free_mode()
    else:
        print("     Побег не удался :( \n")


def defeat():
    print("\nК сожалению ты проиграл :(")
    print("Конец...")
    exit()


def victory(add_health):
    os.system('cls')
    print("\nПротивник побежден!")
    print("*Навык \"" + str(skills[enemy.skills[2]].name) + "\" (урон: " + str(
        skills[enemy.skills[2]].damage) + ", мана: " + str(skills[enemy.skills[2]].mana) + ") получен!*")
    player.change_health(add_health)
    player.change_mana(50)
    player.add_skill(enemy.skills[2])
    print("Добавлено " + str(add_health) + " здоровья\n")
    free_mode()


def rest():
    os.system('cls')
    luck = randint(1, 100)
    regen = randint(10, 15)
    if regen + player.health > 100:
        regen = 100 - player.health
    if luck > 10:
        player.change_health(regen)
        player.change_mana(regen)
        print("Ты отдохнул!")
        print("+ " + str(regen) + " здоровья и маны")
        if player.health == 100:
            print("* Здоровье полностью восстановлено!")
        if player.mana == 100:
            print("* Мана полностью восстановлена!")
        if player.health == 100 and player.mana == 100:
            print("Отдых больше не нужен\n")
        free_mode()
    else:
        fight_start(True)


def rules():
    os.system('cls')
    print("* " + player.name + ", ты воин, намеренно ищущий противников, чтобы стать сильнее, получив все возможные "
                                 "навыки!")
    print("* Побеждая противника, ты получаешь его уникальный навык, но помимо уникального навыка, противник способен "
          "уклоняться и атаковать мечем")
    print("* К тому же, после победы твои показатели здоровья и маны восстанавливаются на половину от изначальных "
          "показателей здоровья и маны противника ")
    print("* Во время битвы, каждый ход восстанавливается 10 маны")
    print("* Изначально тебе доступно только 5 навыков:")
    print("     1. Побег - бег с поля битвы. Вероятность успеха побега зависит от твоего здоровья: 100хп = 100%")
    print("     2. Уклонение - вероятность увернуться от атаки противника. От магии - 50%, от атаки мечем - 80%")
    print("     3. Атака мечем - слабая атака мечем, которая не отнимает ману и наносит 5 урона противнику")
    print("     4. Огненный шар")
    print("     5. Ледяной удар")
    print("* Магический навык можно использовать только 1 раз")
    print("* Чтобы использовать навык во время боя введи индекс навыка")
    mistake = True
    choice = ""
    while mistake:
        choice = input('Готов? (да/нет) -> ')
        if choice == "да" or choice == "нет":
            mistake = False
        else:
            print("     |Введи \"да\" или \"нет\"|")
    if choice == "да":
        os.system('cls')
        free_mode()
    else:
        os.system('cls')
        rules()


def free_mode():
    if player.health == 0:
        defeat()
    print("1. Найти противника")
    print("2. Отдохнуть")
    print("3. Проверить статус")
    print("4. Вернуться в меню")
    print("5. Правила")
    print("6. Сохранить персонажа")
    choice = input("-> ")
    if choice == '1':
        fight_start()
    elif choice == '2':
        rest()
    elif choice == '3':
        os.system('cls')
        status()
        free_mode()
    elif choice == '4':
        menu()
    elif choice == '5':
        rules()
        free_mode()
    elif choice == '6':
        save()
    else:
        print("     |Введи индекс действия|")
        free_mode()


def save():
    os.system('cls')
    with open('save', 'wb') as write:
        pickle.dump(player, write)
        print("Персонаж сохранен! \n")
    free_mode()


menu()
