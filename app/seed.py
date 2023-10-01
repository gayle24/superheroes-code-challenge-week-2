from random import randint, choice
from setup import db, app
from models import Hero, Power, HeroPower


with app.app_context():
  print("🦸‍♀️ Seeding powers...")

  # Query existing power records and store their IDs in a list
  existing_powers = Power.query.all()
  power_ids = [power.id for power in existing_powers]

  # Create new powers if needed
  if len(existing_powers) < 4:
      powers_data = [
      { "name": "super strength", "description": "gives the wielder super-human strengths" },
      { "name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed" },
      { "name": "super human senses", "description": "allows the wielder to use her senses at a super-human level" },
      { "name": "elasticity", "description": "can stretch the human body to extreme lengths" },
      { "name": "telekinesis", "description": "allows the wielder to move objects with the power of the mind" },
      { "name": "invisibility", "description": "renders the wielder invisible to the naked eye" }
  ]


      for power_info in powers_data:
          power = Power(**power_info)
          db.session.add(power)
          db.session.commit()
          power_ids.append(power.id)

  print("🦸‍♀️ Seeding heroes...")

  # Query existing hero records and store their IDs in a list
  existing_heroes = Hero.query.all()
  hero_ids = [hero.id for hero in existing_heroes]

  heroes_data = [
      { "name": "Alex Turner", "super_name": "Shadowstrike" },
      { "name": "Olivia Greene", "super_name": "Aurora Blaze" },
      { "name": "Lucas Knight", "super_name": "Specter Phoenix" },
      { "name": "Mia Hart", "super_name": "Lunar Serpent" },
      { "name": "Ethan Steele", "super_name": "Chrono Hawk" },
      { "name": "Sophia Rivers", "super_name": "Mystic Sable" },
      { "name": "William Frost", "super_name": "Silver Griffin" },
      { "name": "Ava Storm", "super_name": "Neon Panther" },
      { "name": "Liam Steele", "super_name": "Crimson Lynx" },
      { "name": "Isabella Swift", "super_name": "Zephyr Tempest" }
  ]

  for hero_info in heroes_data:
      hero = Hero(**hero_info)
      db.session.add(hero)
      db.session.commit()
      hero_ids.append(hero.id)

  print("🦸‍♀️ Adding powers to heroes...")

  strengths = ["Strong", "Weak", "Average"]

  for hero in Hero.query.all():
      for _ in range(randint(1, 3)):
          # Generate random hero_id and power_id from existing records
          random_hero_id = choice(hero_ids)
          random_power_id = choice(power_ids)

          hero_power = HeroPower(hero_id=random_hero_id, power_id=random_power_id, strength=choice(strengths))
          db.session.add(hero_power)
          db.session.commit()

  print("🦸‍♀️ Done seeding!")
