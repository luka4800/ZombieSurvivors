# Zombie Survivors

A fast-paced survival game where you fight against waves of zombies and powerful bosses.

## Game Features

- **Survival Gameplay**: Fight against endless waves of zombies
- **Boss Battles**: Face two powerful bosses with unique abilities
- **Upgrade System**: Spend zombinos to upgrade your damage and health
- **Power-ups**: Collect various power-ups during gameplay:
  - Health: Restores 30 health points
  - Nuke: Eliminates all zombies on screen
  - Invincibility: Temporary invincibility
- **Dash Ability**: Quick dash movement with cooldown
- **Progress Saving**: Your progress and upgrades are automatically saved

## Controls

- **Movement**: WASD or Arrow Keys
- **Dash**: Left Shift + Movement Keys
- **Nuke**: Space (when available)
- **Pause**: ESC
- **Mute**: Click the speaker icon in the bottom right

## Game Mechanics

### Zombinos
- Earn 10 zombinos for each zombie killed
- Earn 1000 zombinos for defeating the first boss
- Earn 2000 zombinos for defeating the second boss

### Boss System
- First boss appears after 120 seconds
- Second boss appears 120 seconds after defeating the first boss
- Bosses have increased health and damage
- Bosses can perform speed boosts

### Upgrades
- Damage Upgrade: Increases weapon damage
- Health Upgrade: Increases maximum health
- Upgrade costs increase with each purchase

### Power-ups
- Health Power-up: Restores 30 health
- Nuke Power-up: Eliminates all zombies
- Invincibility Power-up: 6 seconds of invincibility

## Installation

1. Ensure you have Python 3.x installed
2. Install required packages:
   ```
   pip install pygame
   ```
3. Run the game:
   ```
   python zombie_survivors.py
   ```

## Creating an Executable

To create a standalone executable:

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Run the build script:
   ```
   python build_exe.py
   ```

3. The executable will be created in the `dist` folder as `ZombieSurvivors.exe`

Note: Make sure all assets (images, sounds, etc.) are in the `assets` folder before creating the executable.

## Save System

The game automatically saves your progress in `save_data.json`, including:
- Total zombinos
- Damage upgrades
- Health upgrades
- Maximum health
- Weapon damage
- Total zombinos earned

## Tips

- Use dash to escape from dangerous situations
- Save nukes for boss fights
- Collect power-ups whenever possible
- Upgrade damage first to kill zombies faster
- Upgrade health to survive longer
- Watch for boss speed boosts and attack patterns

## Requirements

For development:
- Python 3.x
- Pygame
- Pillow (for executable creation)
- PyInstaller (for executable creation)

For playing:
- Windows PC (for the executable version)
- No additional requirements when using the executable

## How to Play

### Controls
- **WASD** or **Arrow Keys**: Move the player
- **Space**: Activate nuke powerup (when available)
- **Left Shift**: Dash ability (with cooldown)
- **ESC**: Pause game/Return to main menu

### Game Features

#### Main Menu
- Beautiful background image
- Three buttons: Play Game, Upgrades, and Quit Game
- Clean and intuitive interface
- Background music with volume control
- Mute button in bottom right corner
- Quit confirmation popup with Yes/No options when pressing ESC or clicking Quit Game

#### Gameplay
- Fight off waves of zombies with your spinning sword
- Collect health powerups to restore health
- Collect nuke powerups to eliminate all zombies on screen
- Survive as long as possible to increase your score
- Earn Zombinos by killing zombies (10 Zombinos per kill)
- Sword sound effects when hitting zombies
- Dash ability to quickly escape dangerous situations

#### Boss Fight
- Boss zombie appears after 120 seconds
- Progress bar at the top shows boss spawn timer
- Boss has a large health pool and deals massive damage
- Boss periodically gets a speed boost
- Player deals reduced damage to the boss
- No new zombies spawn during boss fight
- Increased health and invincibility powerup spawns during boss fight
- No nuke powerups during boss fight
- Defeating the boss rewards 1000 Zombinos
- Epic boss music during the fight

#### Enemy Types
- Regular Zombies:
  - 50 health points
  - Moderate damage (0.2 per frame)
  - Steady movement speed
  - Appear in waves
- Boss Zombie:
  - 1000 health points
  - High damage (50 per hit)
  - Variable speed with boost phases
  - Appears after 120 seconds

#### Currency System
- **Zombinos**: The game's currency earned by killing zombies
- Each zombie kill rewards 10 Zombinos
- Boss defeat rewards 1000 Zombinos
- Zombinos are used to purchase upgrades
- Zombinos persist between games
- Zombinos count is displayed in the bottom right corner

#### Upgrades
- Access the upgrades menu from the main menu
- Use your Zombinos to purchase upgrades:
  - **Damage Upgrade**: Increases weapon damage by 5 points
    - First upgrade: 100 Zombinos
    - Each subsequent upgrade costs 600 Zombinos more
  - **Health Upgrade**: Increases maximum health by 20 points
    - First upgrade: 100 Zombinos
    - Each subsequent upgrade costs 600 Zombinos more
- Upgrades persist between games
- Upgrade costs increase with each purchase

#### Visual Features
- Custom player and zombie sprites
- Animated spinning sword weapon
- Explosion effects when using nuke powerup
- Health powerups with pulsing animation
- Nuke powerups with visual indicator
- Thematic field background
- Health bars for player and zombies
- Zombinos and time display
- Boss health bar at the top of the screen
- Boss speed boost indicator
- Dash cooldown indicator

#### Audio Features
- Background music in main menu
- Boss music plays during boss fight
- Sword sound effects during combat
- Invincibility sound effect during powerup
- Mute/unmute functionality
- Volume control for music

#### Powerups
- **Health Powerup**: Restores 30 health points
- **Nuke Powerup**: Eliminates all zombies on screen
- **Invincibility Powerup**: Makes player invincible for 6 seconds
- **Dash Ability**: Quick escape with 10-second cooldown
- Powerups appear randomly during gameplay
- Visual indicators show when powerups are available
- Increased spawn rates for health and invincibility during boss fight

### Tips
- Keep moving to avoid zombie attacks
- Use the spinning sword to damage multiple zombies at once
- Collect health powerups when your health is low
- Save nuke powerups for when you're surrounded
- Try to maintain distance from zombies while attacking
- Save up Zombinos to purchase upgrades
- Balance your upgrades between damage and health
- Focus on killing zombies to earn more Zombinos
- Plan your upgrades carefully as costs increase with each purchase
- During boss fight, prioritize dodging over attacking
- Use invincibility powerups strategically during boss fight
- Watch for the boss's speed boost indicator
- Keep track of the boss's health bar at the top of the screen
- Use dash ability to escape dangerous situations
- Time your dashes carefully due to cooldown

## Coming Soon
- More upgrade options
- Different weapon types
- More powerup varieties
- High score system 