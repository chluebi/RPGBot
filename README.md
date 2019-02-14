# RPGBot




## Combat

### Basics

#### Commands
- use <ability> <target>
- endturn: end your turn
- info <something>
- concede: end the game


### The cycle of a match

- According to the speeds of the different characters, the order gets decided
- Each characters takes their turn:
  * Start of Turn effect applies
  * The character is refilled with 20% of their Mana
  * The character gets 3 action points
  * The character uses their abilities
  * The character either uses "endturn" or runs out of time
  * End of Turn effect applies

Repeat

### Stats
- health, How much Damage you can take
- mana, Used up by abilities

- strength, incresases Strength attacks
- intelligence, increases Magic attacks
- archery, increases Bow and Crossbow attacks
- scoundrel, increases Stealthed attacks

- defense, decreases physical damage attacks
- magic_defense, decreases magic damage attacks

- precision, increases your critical hit chance by 1% per point
- speed, gives you an earlier place in the turn hierarchy

#### Rough calculations how much every stat is worth
- health: 1 powerlevel = 4 health
- mana: 1 powerlevel = 4 health
- strength, intelligence, archery, scoundrel: 1 powerlevel = 3 points
- defense, magic_defense: 1 powerlevel = 5 points
- precision: 1 powerlevel = 0.5 precision
- speed: 1 powerlevel = 1 speed


### Items
- name = Filename*
- description, backstory of the item, how it should be used*
- rarity, options: common, rare, epic, legendary, unobtainable*
- position, options: head, chest, legs, feet, primary, secondary*


##### Stats granted, Items can grant any amount of the stats there
##### Abilities granted

*required

#### Rarities and Droprates
- legendary 1% chance, powerlevel = ~100
- epic 10% chance, powerlevel = ~80
- rare 30% chance, powerlevel = ~60
- common 59% chance, powerlevel = ~40

### Abilities
- name = Filename*
- description, small description of what the ability does*
- damagetype = options: physical, magic, absolute or mixed*
- abilitytype = passive, enemy, ally, any, (random, enemy|ally|all, amount of targets), enemyall, allyall, all*

- energycost: How much energy it costs to use this ability*
- manacost: How much mana it costs to use this ability
- healthcost: How much health it costs to use this ability

##### Important: Passive Abilities are special, they do not deal any direct damage and just apply all the effects at the beginning of the battle

##### Base Damage

##### Scalings: Times the amount this stat is calculated, for example 0.5 if you want the damage to increase by 50% of a certain stat
  - max_health
  - missing_health
  - health
  - MaxMana
  - Mana
  - Strength
  - Intelligence
  - Archery
  - Scoundrel
  - Defense
  - Magic Defense
  - .Precision
  - .Speed

###### . only reccomended if you know what you are doing

###### Important: Scalings can also work on the target, just instead of writing "max_health" write "target_max_health"

##### Crittable:
  - crit_chance: for example 0.5 if there is a 50% crit chance, increases with precision
  - lower_limit: times how much the damage is calculated atleast, for example 2 for 200% damage
  - upper_limit: times how much the damage is calculated atmost, for example 3 for 300% damage


##### Effects applied in an array - Every effect is written in a seperate array like so:
 0. effectname
 1. effectduration
 2. chance to Apply the effect


*required

#### Different damage types
- physical: ingoing damage * (100 / (100 + defense of the target))
- magic: ingoing damage * (100 / (100 + magic_defense of the target))
- absolute: ingoing damage * 1
- mixed: ingoing damage * (100 / (100 + defense of the target / 2 + magic_defense of the target / 2))


### Effects
##### Effects are coded inside of python and therefor harder to create yourself, here is the basic concept:

- description: What the effect does*
- emoji: Emoji used for visual representation of the effect*
- cleansable: true|false
- stackable: false|partial|full

- EVENT start:
- What the effect does with the target when it's first applied

- EVENT start_turn:
- What the effect does with the target before the target's turn

- EVENT end_turn:
- What the effect does with the target after the target's turn

- EVENT on_damage:
- When the target takes damage, self-inflicted damage too

- EVENT on_attacked:
- When the target is attacked by an enemy. This takes place before the attack is actualy applied and can therefore render an attack useless.

- EVENT target_dies:
- When the target dies whilst still having the effect. This triggers BEFORE the target actually dies and can therefore for example heal the target back to full health.

- EVENT end:
- When the effect stops after its duration. This does not trigger when the effect is removed by a cleanse effect.

- EVENT stop:
- When the effect stops in any way. This DOES trigger when the effect is removed by a cleanse effect.


#### On the topic of cleansable effects
If an effect is uncleansable, there is practically no counterplay and that's why I advise most abilities to be cleansable. But if for example it's a passive effect on a boss which makes the boss explode at the end of the battle, then we need this metric.


#### On the topic of stackable effects
What does it mean for an effect to be stackable? Let's say you have a target which is suffering under "bleed" for the next 2 turns. Now if you use a new ability with bleed for 4 turns on the target what happens?⋅⋅⋅⋅

- false: The current target's instance of (bleed, 2) gets replaced by (bleed, 4)
- partial: The target has now two instances of bleed, one being (bleed, 2) and the other (bleed, 4)
- full: The target has now two instances of bleed, both being (bleed, 4)

### Enemies

name = filename*
description: A small backstory of the enemy of maybe a tip what the enemy's weakness is.

abilities: all the abilities the enemy can use*

stats: refer to "Stats"*
##### Stats are written in two part arrays or else the enemy won't scale!

drops:
- gold
- xp
- special gear, etc

##### Droprates are written like so: If an enemy drops 100 gold, you write "gold":100, if the enemy has a 10% chance to drop the mastersword, you write "mastersword":0.1

##### If a player dies during battle, they won't get any of the item drops they collected!

#### Enemy Stats and Scaling
How scaling works: Every Stat of the Enemy is a 2 part array:
(basevalue, scaling)
Enemies have to scale with the player to put up a tough enough challenge, that's why with every level they get, the enemy gets stronger. Values are calculated like so:

basevalue + scaling * level

#### Enemy AI
For the most common enemies, the AI is handwritten with a bit of Randomness mixxed in. Some enemies might behave completely randomly, others will use their abilities at the perfect moment.


### PvE Battles
All Battles take place in a certain Area. In the file structure this means that every battle is in a subfolder. Some Areas will feature randomly generated Enemies, but others (for example the Tutorial) are rigidly defined like so:

rarity: the higher, the more likely it is that players will stumble upon this battle, -1 means unfindable without a manual search
min_level: the lowest level players can have to stumble upon this battle, -1 means everyone can play it
enemies: an array of enemies, they will automatically be scaled



