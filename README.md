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
- Health, How much Damage you can take
- Mana, Used up by abilities

- Strength, incresases Strength attacks
- Intelligence, increases Magic attacks
- Archery, increases Bow and Crossbow attacks
- Scoundrel, increases Stealthed attacks

- Defense, decreases physical damage attacks
- Magic Defense, decreases magic damage attacks

- Precision, increases your critical hit chance by 1% per point
- Speed, gives you an earlier place in the turn hierarchy

#### Rough calculations how much every stat is worth
- Health: 1 powerlevel = 4 health
- Mana: 1 powerlevel = 4 health
- Strength, Intelligence, Archery, Scoundrel: 1 powerlevel = 3 points
- Defense, Magic Defense: 1 powerlevel = 5 points
- Precision 1 powerlevel = 0.5 precision
- Speed: 1 powerlevel = 1 speed


### Items
- Name = Filename*
- Description, backstory of the item, how it should be used*
- Rarity, options: common, rare, epic, legendary, unobtainable*
- Position, options: head, chest, legs, feet, primary, secondary*


##### Stats granted, Items can grant any amount of the stats there
##### Abilities granted

*required

#### Rarities and Droprates
- Legendary 1% chance, powerlevel = ~100
- Epic 10% chance, powerlevel = ~80
- Rare 30% chance, powerlevel = ~60
- Common 59% chance, powerlevel = ~40

### Abilities
- Name = Filename*
- Description, small description of what the ability does*
- Damagetype = options: physical, magic, absolute or mixed*
- Abilitytype = passive, enemy, ally, any, (random, enemy|ally|all, amount of targets), enemyall, allyall, all*

- Energycost: How much energy it costs to use this ability*
- Manacost: How much mana it costs to use this ability
- Healthcost: How much health it costs to use this ability

##### Important: Passive Abilities are special, they do not deal any direct damage and just apply all the effects at the beginning of the battle

##### Base Damage

##### Scalings: Times the amount this stat is calculated, for example 0.5 if you want the damage to increase by 50% of a certain stat
  - MaxHealth
  - MissingHealth
  - Health
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

###### Important: Scalings can also work on the target, just instead of writing "MaxHealth" write "targetMaxHealth"

##### Crittable:
  - CritChance: for example 0.5 if there is a 50% crit chance, increases with precision
  - LowerLimit: times how much the damage is calculated atleast, for example 2 for 200% damage
  - UpperLimit: times how much the damage is calculated atmost, for example 3 for 300% damage


##### Effects applied in an array - Every effect is written in a seperate array like so:
 0. Effectname
 1. Effectduration
 2. Chance to Apply the effect


*required

#### Different damage types
- physical: ingoing damage * (100 / (100 + defense of the target))
- magic: ingoing damage * (100 / (100 + magic_defense of the target))
- absolute: ingoing damage * 1
- mixed: ingoing damage * (100 / (100 + defense of the target / 2 + magic_defense of the target / 2))


### Effects
##### Effects are coded inside of python and therefor harder to create yourself, here is the basic concept:

- Description: What the effect does*
- Emoji: Emoji used for visual representation of the effect*
- Stackable: false|partial|full

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

- EVENT end:
- When the effect stops after its duration. This does not trigger when the effect is removed by a cleanse effect.

- EVENT stop:
- When the effect stops in any way. This DOES trigger when the effect is removed by a cleanse effect.


### On the topic of stackable effects
What does it mean for an effect to be stackable? Let's say you have a target which is suffering under "bleed" for the next 2 turns. Now if you use a new ability with bleed for 4 turns on the target what happens?⋅⋅⋅⋅

- false: The current target's instance of (bleed, 2) gets replaced by (bleed, 4)
- partial: The target has now two instances of bleed, one being (bleed, 2) and the other (bleed, 4)
- full: The target has now two instances of bleed, both being (bleed, 4)

