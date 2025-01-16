# Оборона Проциона

Беляков Максим - MaxBelysh

Космический шутер-аркада на Pygame. В игре игроку предстоит взять на себя управление над космическим звездолётом и отстоять Процион, сразившись с сильнейшей флотилией галактики. В разработке.

# ТЗ:

Игра представляет из себя шутер-аркаду с постепенно ускоряющимся геймплеем и с нарастающей сложностью. Игроку предстоит взять на себя управление над космическим кораблём и побеждать разнообразных врагов и босса: корвет, истребитель, штурмовик, крейсер и материнский корабль, преодолевать препятствия: метеорит. В игре будут предусмотрены разнообразные бонусы для игрока, а именно: щит, аптека, а также улучшения пушек, такие как: взрывной снаряд (ракетная установка), двойной и тройной снаряд. Основная механика игры - подсчёт очков. От этой механики зависит сложность игры (спавн противников, препятствий, бонусов) и скорость игры.

В игре будут реализованы следующие классы:

Класс основного меню (MainMenu)

Класс игрового меню (GameMenu)

Класс игровой сцены (GameScene) - основной класс, подсчитывающий очки, отвечающий за спавн врагов.

Класс игрового уровня (GameLevel) - класс, отвечающий за генерацию фона.

Класс игрока (Player) - базовая атака - единичные снаряды; изначальное хп - 3 единицы (любой один снаряд противника сносит 1 хп игрока)

Класс противника (Enemy):

Класс метеорит (Meteorite)

Класс корвета (Corvette) - атакует единичными снарядами

Класс истребителя (Fighter) - атакует ракетами

Класс штурмовика (AttackAircaft) - атакует быстрой пулемётной очередью

Класс крейсера (Cruiser) - атакует лазерами

Класс материнского корабля (MotherShip) - Босс - атакует артиллерийским обстрелом, шквалом ракет, шквал огня

Класс снаряда (Projectile):

Класс снаряда игрока (PlayerProjectile)

Класс снаряда врага (EnemyProjectile)

Класс Бонуса (Bonus):

Класс аптеки (Heal)

Класс Щита (Shield)

Класс Оружия (Weapon):

Класс ракетной установки (Rocket)

Класс Множественного снаряда (двойного и тройного) (MultipleProjectile)

База данных: информация о максимальном рекорде.

Проект написан на python с использованием модуля pygame, sys, os.
