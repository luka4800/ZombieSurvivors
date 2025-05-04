import pygame
import sys
import random
import math
import json
import os
from pygame import mixer

# Add this near the top of the file, after the imports
import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Initialize Pygame
pygame.init()
mixer.init()

# Global variables for sounds
menu_music = None
sword_sound = None
invincible_sound = None
boss_music = None

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
PLAYER_SPEED = 8
DASH_SPEED = 20  # Speed during dash
DASH_DURATION = 0.5 * FPS  # 0.5 seconds
DASH_COOLDOWN = 10 * FPS  # 10 seconds
ZOMBIE_SPEED = 3
ZOMBIE_SPAWN_RATE = 45
WEAPON_COOLDOWN = 0.5  # seconds between attacks
WEAPON_DAMAGE = 10  # Reduced from 20
SWORD_LENGTH = 100
SWORD_WIDTH = 20
SWORD_SPEED = 5     # rotations per second

# Boss constants
BOSS_SPAWN_TIME = 120  # seconds
BOSS_ATTACK_COOLDOWN = 6  # seconds
BOSS_DAMAGE = 50  # Massive damage per hit
BOSS_HEALTH = 1000  # High health pool
BOSS_SIZE = 200  # Large size
BOSS_SPEED = 2  # Slower than regular zombies
BOSS_DAMAGE_REDUCTION = 0.2  # Player deals only 20% of normal damage to boss
BOSS_SPEED_BOOST = 4  # Speed during boost
BOSS_SPEED_BOOST_DURATION = 1 * FPS  # 1 second
BOSS_SPEED_BOOST_COOLDOWN = 5 * FPS  # 5 seconds

# Currency and Upgrade constants
ZOMBINOS_PER_KILL = 10
BASE_DAMAGE_UPGRADE_COST = 100
BASE_HEALTH_UPGRADE_COST = 100
UPGRADE_COST_INCREASE = 600
DAMAGE_UPGRADE_AMOUNT = 5
HEALTH_UPGRADE_AMOUNT = 20

# Powerup constants
HEALTH_POWERUP_CHANCE = 0.003  # Reduced from 0.01 (0.3% chance per frame)
NUKE_POWERUP_CHANCE = 0.001    # Reduced from 0.005 (0.1% chance per frame)
INVINCIBLE_POWERUP_CHANCE = 0.0005  # Reduced from 0.002 (0.05% chance per frame)
POWERUP_DURATION = 10 * FPS    # 10 seconds
INVINCIBLE_DURATION = 6 * FPS  # 6 seconds
HEALTH_RESTORE = 30            # Amount of health restored
POWERUP_SIZE = 80             # Increased from 40 (doubled size)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
SILVER = (192, 192, 192)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)
DASH_COLOR = (66, 135, 245)  # #4287f5 color for dash cooldown

# Load images and sounds first, before any class definitions
try:
    print("Loading images...")
    # Load images
    print("Loading player images...")
    try:
        player_img = pygame.image.load(resource_path('assets/player/player.png'))
        player_star_img = pygame.image.load(resource_path('assets/player/player_star.png'))
        player_dash_img = pygame.image.load(resource_path('assets/player/player_dash.png'))
        print("Player images loaded successfully")
    except Exception as e:
        print(f"Warning: Could not load player images: {e}")
        player_img = None
        player_star_img = None
        player_dash_img = None
    
    print("Loading zombie images...")
    try:
        zombie_img = pygame.image.load(resource_path('assets/zombie/zombie.png'))
        boss_zombie_img = pygame.image.load(resource_path('assets/boss_zombie/boss_zombie.png'))
        print("Zombie images loaded successfully")
    except Exception as e:
        print(f"Warning: Could not load zombie images: {e}")
        zombie_img = None
        boss_zombie_img = None
    
    print("Loading powerup images...")
    try:
        nuke_img = pygame.image.load(resource_path('assets/nuke.png'))
        health_img = pygame.image.load(resource_path('assets/health.png'))
        sword_img = pygame.image.load(resource_path('assets/sword.png'))
        explosion_img = pygame.image.load(resource_path('assets/nuke_explosion.png'))
        print("Powerup images loaded successfully")
    except Exception as e:
        print(f"Warning: Could not load powerup images: {e}")
        nuke_img = None
        health_img = None
        sword_img = None
        explosion_img = None
    
    print("Loading background images...")
    try:
        menu_bg = pygame.image.load(resource_path('assets/menu.png'))
        field_bg = pygame.image.load(resource_path('assets/field.png'))
        print("Background images loaded successfully")
    except Exception as e:
        print(f"Warning: Could not load background images: {e}")
        menu_bg = None
        field_bg = None
    
    print("Loading UI images...")
    try:
        gold_img = pygame.image.load(resource_path('assets/gold.png'))
        brick_bg = pygame.image.load(resource_path('assets/brick.png'))
        mute_img = pygame.image.load(resource_path('assets/mute.png'))
        unmute_img = pygame.image.load(resource_path('assets/unmute.png'))
        star_img = pygame.image.load(resource_path('assets/star.png'))
        dash_img = pygame.image.load(resource_path('assets/dash.png'))
        print("UI images loaded successfully")
    except Exception as e:
        print(f"Warning: Could not load UI images: {e}")
        gold_img = None
        brick_bg = None
        mute_img = None
        unmute_img = None
        star_img = None
        dash_img = None
    
    print("Scaling images...")
    # Scale images if they were loaded successfully
    if player_img:
        player_img = pygame.transform.scale(player_img, (120, 120))
    if player_star_img:
        player_star_img = pygame.transform.scale(player_star_img, (120, 120))
    if player_dash_img:
        player_dash_img = pygame.transform.scale(player_dash_img, (120, 120))
    if zombie_img:
        zombie_img = pygame.transform.scale(zombie_img, (100, 100))
    if boss_zombie_img:
        boss_zombie_img = pygame.transform.scale(boss_zombie_img, (BOSS_SIZE, BOSS_SIZE))
    if nuke_img:
        nuke_img = pygame.transform.scale(nuke_img, (POWERUP_SIZE, POWERUP_SIZE))
    if health_img:
        health_img = pygame.transform.scale(health_img, (POWERUP_SIZE, POWERUP_SIZE))
    if sword_img:
        sword_img = pygame.transform.scale(sword_img, (SWORD_LENGTH, SWORD_WIDTH))
    if explosion_img:
        explosion_img = pygame.transform.scale(explosion_img, (100, 100))
    if menu_bg:
        menu_bg = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    if field_bg:
        field_bg = pygame.transform.scale(field_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    if gold_img:
        gold_img = pygame.transform.scale(gold_img, (110, 110))
    if brick_bg:
        brick_bg = pygame.transform.scale(brick_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    if mute_img:
        mute_img = pygame.transform.scale(mute_img, (80, 80))
    if unmute_img:
        unmute_img = pygame.transform.scale(unmute_img, (80, 80))
    if star_img:
        star_img = pygame.transform.scale(star_img, (POWERUP_SIZE, POWERUP_SIZE))
    if dash_img:
        dash_img = pygame.transform.scale(dash_img, (50, 50))
    
    print("Getting image rectangles...")
    # Get image rectangles for collision detection
    player_rect = player_img.get_rect() if player_img else None
    zombie_rect = zombie_img.get_rect() if zombie_img else None
    nuke_rect = nuke_img.get_rect() if nuke_img else None
    health_rect = health_img.get_rect() if health_img else None
    sword_rect = sword_img.get_rect() if sword_img else None
    explosion_rect = explosion_img.get_rect() if explosion_img else None
    gold_rect = gold_img.get_rect() if gold_img else None
    
    print("All assets loaded successfully!")
except Exception as e:
    print(f"Error loading images: {e}")
    print("Using default shapes instead.")
    player_img = None
    zombie_img = None
    nuke_img = None
    health_img = None
    sword_img = None
    explosion_img = None
    menu_bg = None
    field_bg = None
    gold_img = None
    brick_bg = None
    mute_img = None
    unmute_img = None
    star_img = None
    dash_img = None
    player_rect = None
    zombie_rect = None
    nuke_rect = None
    health_rect = None
    sword_rect = None
    explosion_rect = None
    gold_rect = None

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 48)
        self.image = image

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        pygame.draw.rect(surface, BLACK, self.rect, 3, border_radius=15)
        
        if self.image:
            # Center the image in the button
            image_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, image_rect)
        else:
            text_surface = self.font.render(self.text, True, BLACK)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click

class SpinningSword:
    def __init__(self, player, game):
        self.player = player
        self.game = game
        self.angle = 0
        self.rotation_speed = SWORD_SPEED * 2 * math.pi / FPS  # Convert to radians per frame
        self.length = SWORD_LENGTH
        self.width = SWORD_WIDTH
        self.damage = WEAPON_DAMAGE
        self.image = sword_img
        self.rect = sword_rect if sword_img else None
        self.last_hit_time = 0  # Track time of last hit to prevent sound spam

    def update(self, zombies, boss=None):
        # Update rotation angle
        self.angle += self.rotation_speed
        if self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi

        # Calculate sword position
        sword_x = self.player.x + math.cos(self.angle) * self.length
        sword_y = self.player.y + math.sin(self.angle) * self.length

        # Check for zombie collisions
        current_time = pygame.time.get_ticks()
        for zombie in zombies:
            distance = math.sqrt((sword_x - zombie.x)**2 + (sword_y - zombie.y)**2)
            if distance < zombie.radius:
                zombie.health -= self.damage
                # Play sound effect with cooldown to prevent spam
                if current_time - self.last_hit_time > 100:  # 100ms cooldown
                    self.game.sword_sound.play()
                    self.last_hit_time = current_time

        # Check for boss collision
        if boss:
            distance = math.sqrt((sword_x - boss.x)**2 + (sword_y - boss.y)**2)
            if distance < boss.radius:
                # Boss always takes base damage regardless of upgrades
                boss_damage = int(WEAPON_DAMAGE * BOSS_DAMAGE_REDUCTION)  # Apply damage reduction to base damage
                boss.health -= boss_damage
                # Play sound effect with cooldown to prevent spam
                if current_time - self.last_hit_time > 100:  # 100ms cooldown
                    self.game.sword_sound.play()
                    self.last_hit_time = current_time

    def draw(self, surface):
        if self.image:
            # Calculate sword position and rotation
            sword_x = self.player.x + math.cos(self.angle) * self.length
            sword_y = self.player.y + math.sin(self.angle) * self.length
            
            # Create a rotated version of the sword image
            rotated_sword = pygame.transform.rotate(self.image, -math.degrees(self.angle))
            rotated_rect = rotated_sword.get_rect(center=(int(sword_x), int(sword_y)))
            
            # Draw the rotated sword
            surface.blit(rotated_sword, rotated_rect)
        else:
            # Fallback to line and circle if image not loaded
            sword_x = self.player.x + math.cos(self.angle) * self.length
            sword_y = self.player.y + math.sin(self.angle) * self.length

            # Draw sword blade
            pygame.draw.line(surface, SILVER, (self.player.x, self.player.y), (sword_x, sword_y), self.width)

            # Draw sword tip
            pygame.draw.circle(surface, SILVER, (int(sword_x), int(sword_y)), self.width//2)

class Powerup:
    def __init__(self, x, y, powerup_type):
        self.x = x
        self.y = y
        self.type = powerup_type  # 'health', 'nuke', or 'invincible'
        self.radius = POWERUP_SIZE // 2
        self.angle = 0
        self.collected = False
        if powerup_type == 'health':
            self.image = health_img
            self.rect = health_rect
        elif powerup_type == 'nuke':
            self.image = nuke_img
            self.rect = nuke_rect
        else:  # invincible
            self.image = star_img
            self.rect = star_img.get_rect() if star_img else None

    def draw(self, surface):
        if self.collected:
            return

        # Draw pulsing effect
        pulse_size = math.sin(self.angle) * 5 + POWERUP_SIZE
        self.angle += 0.1

        if self.image:
            # Draw powerup using image
            self.rect.center = (int(self.x), int(self.y))
            surface.blit(self.image, self.rect)
        else:
            # Fallback to shapes if images not loaded
            if self.type == 'health':
                # Draw health powerup (heart)
                points = []
                for i in range(5):
                    angle = i * 2 * math.pi / 5
                    points.append((
                        self.x + math.cos(angle) * pulse_size/2,
                        self.y + math.sin(angle) * pulse_size/2
                    ))
                pygame.draw.polygon(surface, PINK, points)
            elif self.type == 'nuke':
                # Draw nuke powerup (star)
                points = []
                for i in range(5):
                    angle = i * 2 * math.pi / 5
                    points.append((
                        self.x + math.cos(angle) * pulse_size/2,
                        self.y + math.sin(angle) * pulse_size/2
                    ))
                pygame.draw.polygon(surface, YELLOW, points)
            else:  # invincible
                # Draw star for invincibility
                points = []
                for i in range(5):
                    angle = i * 2 * math.pi / 5
                    points.append((
                        self.x + math.cos(angle) * pulse_size/2,
                        self.y + math.sin(angle) * pulse_size/2
                    ))
                pygame.draw.polygon(surface, YELLOW, points)

    def check_collision(self, player):
        if self.collected:
            return False

        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        if distance < self.radius + player.radius:
            self.collected = True
            return True
        return False

class Player:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.game = game
        self.radius = 60
        self.health = 100
        self.max_health = 100
        self.zombinos = 0
        self.zombinos_earned = 0  # Track zombinos earned in current game
        self.survival_time = 0
        self.weapon = SpinningSword(self, game)
        
        # Load base player image
        try:
            self.image = pygame.image.load(resource_path('assets/player/player.png'))
            self.rect = self.image.get_rect() if self.image else None
        except:
            self.image = None
            self.rect = None
            print("Warning: Could not load player.png")
        
        self.nuke_available = False
        self.damage_upgrades = 0
        self.health_upgrades = 0
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_sound_playing = False
        self.dashing = False
        self.dash_timer = 0
        self.dash_cooldown = 0
        self.dash_direction = [0, 0]
        self.load_progress()  # Load saved progress when player is created
        
        # Animation state
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10  # frames between animation changes
        self.is_moving = False
        self.facing_left = False  # Track which way the player is facing
        
        # Right movement animations
        try:
            self.movement_images = [
                pygame.image.load(resource_path('assets/player/movement1.png')),
                pygame.image.load(resource_path('assets/player/movement2.png'))
            ]
            self.star_movement_images = [
                pygame.image.load(resource_path('assets/player/star_movement1.png')),
                pygame.image.load(resource_path('assets/player/star_movement2.png'))
            ]
            self.dash_movement_images = [
                pygame.image.load(resource_path('assets/player/dash_movement1.png')),
                pygame.image.load(resource_path('assets/player/dash_movement2.png'))
            ]
            
            # Left movement animations
            self.left_movement_images = [
                pygame.image.load(resource_path('assets/player/left_movement1.png')),
                pygame.image.load(resource_path('assets/player/left_movement2.png'))
            ]
            self.star_left_movement_images = [
                pygame.image.load(resource_path('assets/player/star_left_movement1.png')),
                pygame.image.load(resource_path('assets/player/star_left_movement2.png'))
            ]
            self.dash_left_movement_images = [
                pygame.image.load(resource_path('assets/player/dash_left_movement1.png')),
                pygame.image.load(resource_path('assets/player/dash_left_movement2.png'))
            ]
            
            # Scale all animation images
            for i in range(len(self.movement_images)):
                self.movement_images[i] = pygame.transform.scale(self.movement_images[i], (120, 120))
                self.star_movement_images[i] = pygame.transform.scale(self.star_movement_images[i], (120, 120))
                self.dash_movement_images[i] = pygame.transform.scale(self.dash_movement_images[i], (120, 120))
                self.left_movement_images[i] = pygame.transform.scale(self.left_movement_images[i], (120, 120))
                self.star_left_movement_images[i] = pygame.transform.scale(self.star_left_movement_images[i], (120, 120))
                self.dash_left_movement_images[i] = pygame.transform.scale(self.dash_left_movement_images[i], (120, 120))
        except Exception as e:
            print(f"Warning: Could not load animation images: {e}")
            # Set default images if loading fails
            self.movement_images = [self.image] * 2 if self.image else [None] * 2
            self.star_movement_images = [self.image] * 2 if self.image else [None] * 2
            self.dash_movement_images = [self.image] * 2 if self.image else [None] * 2
            self.left_movement_images = [self.image] * 2 if self.image else [None] * 2
            self.star_left_movement_images = [self.image] * 2 if self.image else [None] * 2
            self.dash_left_movement_images = [self.image] * 2 if self.image else [None] * 2

    def get_damage_upgrade_cost(self):
        return BASE_DAMAGE_UPGRADE_COST + (self.damage_upgrades * UPGRADE_COST_INCREASE)

    def get_health_upgrade_cost(self):
        return BASE_HEALTH_UPGRADE_COST + (self.health_upgrades * UPGRADE_COST_INCREASE)

    def move(self, dx, dy):
        self.is_moving = dx != 0 or dy != 0
        # Update facing direction based on horizontal movement
        if dx < 0:
            self.facing_left = True
        elif dx > 0:
            self.facing_left = False
            
        if self.dashing:
            # Use dash direction and speed during dash
            self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, 
                        self.x + self.dash_direction[0] * DASH_SPEED))
            self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, 
                        self.y + self.dash_direction[1] * DASH_SPEED))
        else:
            # Normal movement
            self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x + dx))
            self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y + dy))

    def dash(self, dx, dy):
        if not self.dashing and self.dash_cooldown <= 0:
            self.dashing = True
            self.dash_timer = DASH_DURATION
            self.dash_cooldown = DASH_COOLDOWN
            # Normalize dash direction
            length = math.sqrt(dx**2 + dy**2)
            if length > 0:
                self.dash_direction = [dx/length, dy/length]
            else:
                self.dash_direction = [0, 0]

    def draw(self, surface):
        # Update animation
        if self.is_moving:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 2
        else:
            self.animation_frame = 0
            self.animation_timer = 0

        # Choose the appropriate player image based on state and direction
        if self.invincible:
            current_image = self.star_left_movement_images[self.animation_frame] if self.facing_left else self.star_movement_images[self.animation_frame]
        elif self.dashing:
            current_image = self.dash_left_movement_images[self.animation_frame] if self.facing_left else self.dash_movement_images[self.animation_frame]
        else:
            current_image = self.left_movement_images[self.animation_frame] if self.facing_left else self.movement_images[self.animation_frame]
        
        if current_image:
            # Draw player image
            self.rect = current_image.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(current_image, self.rect)
        else:
            # Fallback to circle if image not loaded
            pygame.draw.circle(surface, BLUE, (int(self.x), int(self.y)), self.radius)
        
        # Draw health bar
        health_width = 120
        health_height = 12
        health_x = self.x - health_width/2
        health_y = self.y - self.radius - 20
        
        # Background of health bar
        pygame.draw.rect(surface, RED, (health_x, health_y, health_width, health_height))
        # Current health
        current_health_width = (self.health / self.max_health) * health_width
        pygame.draw.rect(surface, GREEN, (health_x, health_y, current_health_width, health_height))

        # Draw weapon
        self.weapon.draw(surface)

    def update(self, zombies, boss=None):
        self.weapon.update(zombies, boss)
        
        # Update dash
        if self.dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.dashing = False
        else:
            self.dash_cooldown = max(0, self.dash_cooldown - 1)
        
        # Update invincibility timer and sound
        if self.invincible:
            self.invincible_timer -= 1
            if not self.invincible_sound_playing:
                self.game.invincible_sound.play(-1)  # Play in loop
                self.invincible_sound_playing = True
            if self.invincible_timer <= 0:
                self.invincible = False
                self.game.invincible_sound.stop()
                self.invincible_sound_playing = False
        elif self.invincible_sound_playing:
            self.game.invincible_sound.stop()
            self.invincible_sound_playing = False

    def collect_powerup(self, powerup):
        if powerup.type == 'health':
            self.health = min(self.max_health, self.health + HEALTH_RESTORE)
        elif powerup.type == 'nuke':
            self.nuke_available = True
        elif powerup.type == 'invincible':
            self.invincible = True
            self.invincible_timer = INVINCIBLE_DURATION
            if not self.invincible_sound_playing:
                self.game.invincible_sound.play(-1)  # Play in loop
                self.invincible_sound_playing = True

    def use_nuke(self, zombies):
        if self.nuke_available:
            for zombie in zombies[:]:
                self.zombinos += ZOMBINOS_PER_KILL
                self.zombinos_earned += ZOMBINOS_PER_KILL
                zombies.remove(zombie)
            self.nuke_available = False

    def take_damage(self, amount):
        if not self.invincible and not self.dashing:  # No damage during dash
            self.health -= amount

    def save_progress(self):
        save_data = {
            'zombinos': self.zombinos,
            'damage_upgrades': self.damage_upgrades,
            'health_upgrades': self.health_upgrades,
            'max_health': self.max_health,
            'weapon_damage': self.weapon.damage,
            'zombinos_earned': self.zombinos_earned  # Save total zombinos earned
        }
        try:
            save_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'save_data.json')
            with open(save_path, 'w') as f:
                json.dump(save_data, f)
        except:
            print("Error saving game progress")

    def load_progress(self):
        try:
            save_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'save_data.json')
            if os.path.exists(save_path):
                with open(save_path, 'r') as f:
                    save_data = json.load(f)
                self.zombinos = save_data.get('zombinos', 0)
                self.damage_upgrades = save_data.get('damage_upgrades', 0)
                self.health_upgrades = save_data.get('health_upgrades', 0)
                self.max_health = save_data.get('max_health', 100)
                self.health = self.max_health
                self.weapon.damage = save_data.get('weapon_damage', WEAPON_DAMAGE)
                self.zombinos_earned = save_data.get('zombinos_earned', 0)
        except:
            print("Error loading game progress")

class Zombie:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.game = game
        self.radius = 50  # Increased from 25
        self.max_health = 50  # Base health
        self.health = self.max_health
        self.base_speed = ZOMBIE_SPEED
        self.speed = self.base_speed
        self.base_damage = 0.2  # Base damage per frame
        
        # Scale stats based on player's upgrades
        damage_scale = 1 + (self.game.player.damage_upgrades * 0.1)  # 10% stronger per damage upgrade
        health_scale = 1 + (self.game.player.damage_upgrades * 0.15)  # 15% more health per damage upgrade
        speed_scale = 1 + (self.game.player.damage_upgrades * 0.05)  # 5% faster per damage upgrade
        
        self.max_health *= health_scale
        self.health = self.max_health
        self.speed = self.base_speed * speed_scale
        self.damage = self.base_damage * damage_scale
        
        # Load base zombie image
        try:
            self.image = pygame.image.load(resource_path('assets/zombie/zombie.png'))
            self.rect = self.image.get_rect() if self.image else None
        except Exception as e:
            print(f"Warning: Could not load zombie.png: {e}")
            self.image = None
            self.rect = None
        
        # Animation state
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10  # frames between animation changes
        self.is_moving = False
        self.facing_left = False  # Track which way the zombie is facing
        
        # Load movement animations
        try:
            self.movement_images = [
                pygame.image.load(resource_path('assets/zombie/zombie_movement1.png')),
                pygame.image.load(resource_path('assets/zombie/zombie_movement2.png'))
            ]
            self.left_movement_images = [
                pygame.image.load(resource_path('assets/zombie/zombie_left_movement1.png')),
                pygame.image.load(resource_path('assets/zombie/zombie_left_movement2.png'))
            ]
            
            # Scale all animation images
            for i in range(len(self.movement_images)):
                self.movement_images[i] = pygame.transform.scale(self.movement_images[i], (100, 100))
                self.left_movement_images[i] = pygame.transform.scale(self.left_movement_images[i], (100, 100))
        except Exception as e:
            print(f"Warning: Could not load zombie animation images: {e}")
            # Set default images if loading fails
            self.movement_images = [self.image] * 2 if self.image else [None] * 2
            self.left_movement_images = [self.image] * 2 if self.image else [None] * 2

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            self.is_moving = True
            # Update facing direction based on movement
            self.facing_left = dx < 0
        else:
            self.is_moving = False

    def draw(self, surface):
        # Update animation
        if self.is_moving:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 2
        else:
            self.animation_frame = 0
            self.animation_timer = 0

        # Choose the appropriate zombie image based on direction
        current_image = self.left_movement_images[self.animation_frame] if self.facing_left else self.movement_images[self.animation_frame]
        
        if current_image:
            # Draw zombie image
            self.rect = current_image.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(current_image, self.rect)
        else:
            # Fallback to circle if image not loaded
            pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), self.radius)
        
        # Draw health bar
        health_width = 100  # Increased from 50
        health_height = 10  # Increased from 6
        health_x = self.x - health_width/2
        health_y = self.y - self.radius - 15  # Adjusted for larger size
        
        # Background of health bar
        pygame.draw.rect(surface, RED, (health_x, health_y, health_width, health_height))
        # Current health
        current_health_width = (self.health / self.max_health) * health_width
        pygame.draw.rect(surface, GREEN, (health_x, health_y, current_health_width, health_height))

class BossZombie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BOSS_SIZE // 2
        self.health = BOSS_HEALTH
        self.max_health = BOSS_HEALTH
        self.base_speed = BOSS_SPEED
        self.speed = BOSS_SPEED
        self.damage = BOSS_DAMAGE
        self.attack_cooldown = 0
        self.attack_timer = BOSS_ATTACK_COOLDOWN * FPS
        self.speed_boost_active = False
        self.speed_boost_timer = 0
        self.speed_boost_cooldown = 0
        self.is_attacking = False
        self.attack_animation_timer = 0
        self.attack_animation_duration = 10  # frames to show attack animation
        
        # Load base boss zombie image
        try:
            self.image = pygame.image.load(resource_path('assets/boss_zombie/boss_zombie.png'))
            self.rect = self.image.get_rect() if self.image else None
        except Exception as e:
            print(f"Warning: Could not load boss_zombie.png: {e}")
            self.image = None
            self.rect = None
        
        # Animation state
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10  # frames between animation changes
        self.is_moving = False
        self.facing_left = False  # Track which way the boss is facing
        
        # Load movement animations
        try:
            self.movement_images = [
                pygame.image.load(resource_path('assets/boss_zombie/boss_zombie_movement1.png')),
                pygame.image.load(resource_path('assets/boss_zombie/boss_zombie_movement2.png'))
            ]
            self.left_movement_images = [
                pygame.image.load(resource_path('assets/boss_zombie/boss_zombie_left_movement1.png')),
                pygame.image.load(resource_path('assets/boss_zombie/boss_zombie_left_movement2.png'))
            ]
            
            # Load bite animations
            self.bite_image = pygame.image.load(resource_path('assets/boss_zombie/boss_zombie_bite.png'))
            self.left_bite_image = pygame.image.load(resource_path('assets/boss_zombie/boss_zombie_left_bite.png'))
            
            # Scale all animation images
            for i in range(len(self.movement_images)):
                self.movement_images[i] = pygame.transform.scale(self.movement_images[i], (BOSS_SIZE, BOSS_SIZE))
                self.left_movement_images[i] = pygame.transform.scale(self.left_movement_images[i], (BOSS_SIZE, BOSS_SIZE))
            
            # Scale bite images
            self.bite_image = pygame.transform.scale(self.bite_image, (BOSS_SIZE, BOSS_SIZE))
            self.left_bite_image = pygame.transform.scale(self.left_bite_image, (BOSS_SIZE, BOSS_SIZE))
        except Exception as e:
            print(f"Warning: Could not load boss zombie animation images: {e}")
            # Set default images if loading fails
            self.movement_images = [self.image] * 2 if self.image else [None] * 2
            self.left_movement_images = [self.image] * 2 if self.image else [None] * 2
            self.bite_image = self.image
            self.left_bite_image = self.image

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            self.is_moving = True
            # Update facing direction based on movement
            self.facing_left = dx < 0
        else:
            self.is_moving = False

    def update(self):
        self.attack_cooldown = max(0, self.attack_cooldown - 1)
        
        # Update attack animation
        if self.is_attacking:
            self.attack_animation_timer -= 1
            if self.attack_animation_timer <= 0:
                self.is_attacking = False
        
        # Update speed boost
        if self.speed_boost_active:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.speed_boost_active = False
                self.speed = self.base_speed
        else:
            self.speed_boost_cooldown -= 1
            if self.speed_boost_cooldown <= 0:
                self.speed_boost_active = True
                self.speed_boost_timer = BOSS_SPEED_BOOST_DURATION
                self.speed_boost_cooldown = BOSS_SPEED_BOOST_COOLDOWN
                self.speed = BOSS_SPEED_BOOST

    def can_attack(self):
        return self.attack_cooldown == 0

    def attack(self):
        self.attack_cooldown = self.attack_timer
        self.is_attacking = True
        self.attack_animation_timer = self.attack_animation_duration
        return self.damage

    def draw(self, surface):
        # Update animation
        if self.is_moving and not self.is_attacking:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 2
        else:
            self.animation_frame = 0
            self.animation_timer = 0

        # Choose the appropriate boss image based on state and direction
        if self.is_attacking:
            current_image = self.left_bite_image if self.facing_left else self.bite_image
        else:
            current_image = self.left_movement_images[self.animation_frame] if self.facing_left else self.movement_images[self.animation_frame]
        
        if current_image:
            # Draw boss image
            self.rect = current_image.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(current_image, self.rect)
        else:
            # Fallback to circle if image not loaded
            pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), self.radius)

        # Draw speed boost indicator
        if self.speed_boost_active:
            boost_width = 20
            boost_height = 20
            boost_x = self.x - boost_width/2
            boost_y = self.y - self.radius - 30
            pygame.draw.rect(surface, YELLOW, (boost_x, boost_y, boost_width, boost_height))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Zombie Survivors")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"
        self.show_quit_confirmation = False
        self.player = None
        self.zombies = []
        self.powerups = []
        self.explosions = []
        self.zombie_spawn_timer = 0
        self.font = pygame.font.Font(None, 48)
        self.title_font = pygame.font.Font(None, 72)
        self.music_muted = False
        
        # Load sounds
        try:
            print("Loading sounds...")
            self.menu_music = mixer.Sound(resource_path('assets/menu-music.mp3'))
            self.sword_sound = mixer.Sound(resource_path('assets/sword-sound.mp3'))
            self.invincible_sound = mixer.Sound(resource_path('assets/invincibility.mp3'))
            self.boss_music = mixer.Sound(resource_path('assets/boss_music.mp3'))
            
            # Set sound volumes
            self.menu_music.set_volume(0.2)  # 20% volume
            self.invincible_sound.set_volume(0.2)  # 20% volume
            self.boss_music.set_volume(0.2)  # 20% volume
            print("Sounds loaded successfully!")
        except Exception as e:
            print(f"Warning: Could not load sounds: {e}")
            self.menu_music = None
            self.sword_sound = None
            self.invincible_sound = None
            self.boss_music = None
        
        # Boss tracking
        self.boss = None
        self.boss_progress = 0
        self.boss_spawned = False
        self.boss_defeated = False
        self.second_boss_progress = 0
        self.second_boss_spawned = False
        self.second_boss_defeated = False
        self.boss_progress_bar_width = 400
        self.boss_progress_bar_height = 20
        self.boss_progress_bar_x = (SCREEN_WIDTH - self.boss_progress_bar_width) // 2
        self.boss_progress_bar_y = 20
        self.second_boss_progress_bar_y = 50  # Position second bar below first
        print(f"Initialized second boss progress bar at y={self.second_boss_progress_bar_y}")
        self.boss_health_bar_width = 400
        self.boss_health_bar_height = 20
        self.boss_health_bar_x = (SCREEN_WIDTH - self.boss_health_bar_width) // 2
        self.boss_health_bar_y = 80  # Moved down to accommodate second progress bar
        self.dash_cooldown_bar_width = 100
        self.dash_cooldown_bar_height = 10
        self.dash_cooldown_bar_x = 20
        self.dash_cooldown_bar_y = SCREEN_HEIGHT - 50

        # Create buttons
        button_width = 300
        button_height = 75
        spacing = 30
        total_height = (button_height * 3) + (spacing * 2)
        start_y = (SCREEN_HEIGHT - total_height) // 2
        
        self.play_button = Button(
            (SCREEN_WIDTH - button_width) // 2,
            start_y,
            button_width,
            button_height,
            "Play Game",
            GREEN,
            DARK_GREEN
        )
        
        self.upgrades_button = Button(
            (SCREEN_WIDTH - button_width) // 2,
            start_y + button_height + spacing,
            button_width,
            button_height,
            "Upgrades",
            GRAY,
            DARK_GREEN
        )
        
        self.quit_button = Button(
            (SCREEN_WIDTH - button_width) // 2,
            start_y + (button_height + spacing) * 2,
            button_width,
            button_height,
            "Quit Game",
            RED,
            DARK_GREEN
        )

        # Create mute button with images (moved after image loading)
        try:
            mute_img = pygame.image.load(resource_path('assets/mute.png'))
            unmute_img = pygame.image.load(resource_path('assets/unmute.png'))
            mute_img = pygame.transform.scale(mute_img, (80, 80))
            unmute_img = pygame.transform.scale(unmute_img, (80, 80))
        except Exception as e:
            print(f"Warning: Could not load mute images: {e}")
            mute_img = None
            unmute_img = None

        self.mute_button = Button(
            SCREEN_WIDTH - 100,  # Right side
            SCREEN_HEIGHT - 100,  # Bottom
            80,  # Width
            80,  # Height
            "",  # No text, using image instead
            GRAY,
            DARK_GREEN,
            unmute_img  # Start with unmute image
        )

        # Create pause buttons
        self.resume_button = Button(
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2,
            button_width,
            button_height,
            "Play",
            GREEN,
            DARK_GREEN
        )
        
        self.pause_menu_button = Button(
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2 + button_height + spacing,
            button_width,
            button_height,
            "Main Menu",
            GRAY,
            DARK_GREEN
        )

        # Create game over buttons
        self.play_again_button = Button(
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2 + 50,
            button_width,
            button_height,
            "Play Again",
            GREEN,
            DARK_GREEN
        )
        
        self.game_over_menu_button = Button(
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2 + button_height + spacing + 50,
            button_width,
            button_height,
            "Main Menu",
            GRAY,
            DARK_GREEN
        )

        # Create upgrade buttons
        upgrade_button_width = 400
        upgrade_button_height = 100
        upgrade_spacing = 50
        upgrade_start_y = (SCREEN_HEIGHT - upgrade_button_height) // 2
        
        self.damage_upgrade_button = Button(
            (SCREEN_WIDTH - (upgrade_button_width * 2 + upgrade_spacing)) // 2,  # Left side
            upgrade_start_y,
            upgrade_button_width,
            upgrade_button_height,
            "Upgrade Damage",
            GREEN,
            DARK_GREEN
        )
        
        self.health_upgrade_button = Button(
            (SCREEN_WIDTH - (upgrade_button_width * 2 + upgrade_spacing)) // 2 + upgrade_button_width + upgrade_spacing,  # Right side
            upgrade_start_y,
            upgrade_button_width,
            upgrade_button_height,
            "Upgrade Health",
            GREEN,
            DARK_GREEN
        )
        
        self.back_button = Button(
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT - button_height - 50,
            button_width,
            button_height,
            "Back",
            GRAY,
            DARK_GREEN
        )

        # Create quit confirmation buttons
        self.yes_button = Button(
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2 + button_height,
            button_width,
            button_height,
            "Yes",
            RED,
            DARK_GREEN
        )
        
        self.no_button = Button(
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT // 2 + button_height * 2 + spacing,
            button_width,
            button_height,
            "No",
            GRAY,
            DARK_GREEN
        )

        # Start menu music
        self.handle_menu_music()

    def handle_menu_music(self):
        if self.state == "MENU":
            if not self.music_muted:
                self.menu_music.set_volume(0.2)  # 20% volume
                self.menu_music.play(-1)  # -1 for infinite loop
            else:
                self.menu_music.stop()
        else:
            self.menu_music.stop()
            self.boss_music.stop()  # Stop boss music when not in play state

    def spawn_zombie(self):
        # Spawn zombie at random edge of screen
        side = random.randint(0, 3)
        if side == 0:  # top
            x = random.randint(0, SCREEN_WIDTH)
            y = -30
        elif side == 1:  # right
            x = SCREEN_WIDTH + 30
            y = random.randint(0, SCREEN_HEIGHT)
        elif side == 2:  # bottom
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + 30
        else:  # left
            x = -30
            y = random.randint(0, SCREEN_HEIGHT)
        self.zombies.append(Zombie(x, y, self))  # Pass self (Game instance) to Zombie

    def spawn_powerup(self):
        if random.random() < HEALTH_POWERUP_CHANCE:
            x = random.randint(POWERUP_SIZE, SCREEN_WIDTH - POWERUP_SIZE)
            y = random.randint(POWERUP_SIZE, SCREEN_HEIGHT - POWERUP_SIZE)
            self.powerups.append(Powerup(x, y, 'health'))
        
        if random.random() < NUKE_POWERUP_CHANCE:
            x = random.randint(POWERUP_SIZE, SCREEN_WIDTH - POWERUP_SIZE)
            y = random.randint(POWERUP_SIZE, SCREEN_HEIGHT - POWERUP_SIZE)
            self.powerups.append(Powerup(x, y, 'nuke'))
            
        if random.random() < INVINCIBLE_POWERUP_CHANCE:
            x = random.randint(POWERUP_SIZE, SCREEN_WIDTH - POWERUP_SIZE)
            y = random.randint(POWERUP_SIZE, SCREEN_HEIGHT - POWERUP_SIZE)
            self.powerups.append(Powerup(x, y, 'invincible'))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.player:
                    self.player.save_progress()  # Save progress when quitting
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "PLAY":
                        self.state = "PAUSE"
                    elif self.state == "PAUSE":
                        self.state = "PLAY"
                    elif self.state == "UPGRADES":
                        self.state = "MENU"
                    elif self.state == "MENU":
                        self.show_quit_confirmation = not self.show_quit_confirmation  # Toggle quit confirmation
                    elif self.state == "GAME_OVER":
                        self.state = "MENU"
                    self.handle_menu_music()  # Handle music when state changes
                elif event.key == pygame.K_F12 and self.state == "PLAY":  # Debug: Spawn boss with F12
                    if not self.boss_spawned and not self.boss_defeated:
                        self.spawn_boss()
                        print("Debug: Boss spawned via F12")
                elif event.key == pygame.K_SPACE and self.state == "PLAY":
                    if self.player.nuke_available:
                        # Add explosions for each zombie before removing them
                        for zombie in self.zombies[:]:
                            self.explosions.append({
                                'x': zombie.x,
                                'y': zombie.y,
                                'timer': FPS  # Show for 1 second
                            })
                        self.player.use_nuke(self.zombies)
                elif event.key == pygame.K_LSHIFT and self.state == "PLAY":
                    # Get movement direction for dash
                    keys = pygame.key.get_pressed()
                    dx = 0
                    dy = 0
                    if keys[pygame.K_w] or keys[pygame.K_UP]:
                        dy -= 1
                    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                        dy += 1
                    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                        dx -= 1
                    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                        dx += 1
                    self.player.dash(dx, dy)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.state == "MENU":
                    if self.show_quit_confirmation:
                        if self.yes_button.is_clicked(mouse_pos, True):
                            if self.player:
                                self.player.save_progress()
                            self.running = False
                        elif self.no_button.is_clicked(mouse_pos, True):
                            self.show_quit_confirmation = False
                    else:
                        if self.play_button.is_clicked(mouse_pos, True):
                            # Reset game state
                            self.state = "PLAY"
                            self.handle_menu_music()  # Stop music when starting game
                            self.player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, self)
                            self.zombies = []
                            self.powerups = []
                            self.explosions = []
                            self.zombie_spawn_timer = 0
                            self.boss = None
                            self.boss_progress = 0
                            self.boss_spawned = False
                            self.boss_defeated = False
                            self.second_boss_progress = 0
                            self.second_boss_spawned = False
                            self.second_boss_defeated = False
                            print("Game state reset - starting new game")
                        elif self.upgrades_button.is_clicked(mouse_pos, True):
                            if not self.player:
                                self.player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, self)
                            self.state = "UPGRADES"
                            self.handle_menu_music()  # Stop music when going to upgrades
                        elif self.quit_button.is_clicked(mouse_pos, True):
                            self.show_quit_confirmation = True
                        elif self.mute_button.is_clicked(mouse_pos, True):
                            self.music_muted = not self.music_muted
                            if self.music_muted:
                                menu_music.set_volume(0)
                                self.mute_button.image = mute_img  # Change to mute image
                            else:
                                menu_music.set_volume(0.2)
                                self.mute_button.image = unmute_img  # Change to unmute image
                            self.handle_menu_music()  # Update music state when toggling mute
                elif self.state == "UPGRADES":
                    if self.damage_upgrade_button.is_clicked(mouse_pos, True):
                        if self.player:
                            cost = self.player.get_damage_upgrade_cost()
                            if self.player.zombinos >= cost:
                                self.player.zombinos -= cost
                                self.player.weapon.damage += DAMAGE_UPGRADE_AMOUNT
                                self.player.damage_upgrades += 1
                                self.player.save_progress()  # Save progress after upgrade
                    elif self.health_upgrade_button.is_clicked(mouse_pos, True):
                        if self.player:
                            cost = self.player.get_health_upgrade_cost()
                            if self.player.zombinos >= cost:
                                self.player.zombinos -= cost
                                self.player.max_health += HEALTH_UPGRADE_AMOUNT
                                self.player.health += HEALTH_UPGRADE_AMOUNT
                                self.player.health_upgrades += 1
                                self.player.save_progress()  # Save progress after upgrade
                    elif self.back_button.is_clicked(mouse_pos, True):
                        self.state = "MENU"
                elif self.state == "PAUSE":
                    if self.resume_button.is_clicked(mouse_pos, True):
                        self.state = "PLAY"
                    elif self.pause_menu_button.is_clicked(mouse_pos, True):
                        self.state = "MENU"
                elif self.state == "GAME_OVER":
                    if self.play_again_button.is_clicked(mouse_pos, True):
                        self.state = "PLAY"
                        self.handle_menu_music()  # Stop music when starting new game
                    elif self.game_over_menu_button.is_clicked(mouse_pos, True):
                        self.state = "MENU"
                        self.handle_menu_music()  # Start music when returning to menu

    def update_game(self):
        if self.state == "PLAY":
            # Update boss progress
            if not self.boss_spawned and not self.boss_defeated:
                self.boss_progress = min(1.0, self.player.survival_time / BOSS_SPAWN_TIME)
                if self.boss_progress >= 1.0:
                    self.spawn_boss()
                    menu_music.stop()  # Stop menu music when boss spawns
            elif self.boss_defeated and not self.second_boss_spawned and not self.second_boss_defeated:
                # Start second boss progress after first boss is defeated
                time_since_first_boss = self.player.survival_time - BOSS_SPAWN_TIME
                self.second_boss_progress = min(1.0, time_since_first_boss / BOSS_SPAWN_TIME)
                print(f"States - Boss defeated: {self.boss_defeated}, Second spawned: {self.second_boss_spawned}, Second defeated: {self.second_boss_defeated}")
                print(f"Survival time: {self.player.survival_time:.1f}s, Time since first boss: {time_since_first_boss:.1f}s")
                print(f"Second boss progress: {self.second_boss_progress:.2f}")
                print(f"Second boss progress bar y position: {self.second_boss_progress_bar_y}")
                if self.second_boss_progress >= 1.0:
                    self.second_boss_spawned = True  # Set this before spawning the boss
                    self.spawn_boss()  # Spawn second boss

            # Handle player movement with both WASD and arrow keys
            keys = pygame.key.get_pressed()
            
            # Calculate movement in x and y directions
            dx = 0
            dy = 0
            
            # WASD movement
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                dy -= PLAYER_SPEED
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                dy += PLAYER_SPEED
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx -= PLAYER_SPEED
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx += PLAYER_SPEED
                
            # Normalize diagonal movement
            if dx != 0 and dy != 0:
                dx *= 0.7071  # 1/sqrt(2) for diagonal movement
                dy *= 0.7071
                
            self.player.move(dx, dy)

            # Update player and weapon
            self.player.update(self.zombies, self.boss)

            # Spawn zombies and powerups
            if not self.boss_spawned and not self.second_boss_spawned:  # Only spawn regular zombies when no boss is present
                self.zombie_spawn_timer += 1
                if self.zombie_spawn_timer >= ZOMBIE_SPAWN_RATE:
                    self.spawn_zombie()
                    self.zombie_spawn_timer = 0

            # Modified powerup spawn rates during boss fight
            if self.boss_spawned:
                # Increased health and invincibility spawn rates
                if random.random() < HEALTH_POWERUP_CHANCE * 3:  # Triple the chance
                    x = random.randint(POWERUP_SIZE, SCREEN_WIDTH - POWERUP_SIZE)
                    y = random.randint(POWERUP_SIZE, SCREEN_HEIGHT - POWERUP_SIZE)
                    self.powerups.append(Powerup(x, y, 'health'))
                
                if random.random() < INVINCIBLE_POWERUP_CHANCE * 3:  # Triple the chance
                    x = random.randint(POWERUP_SIZE, SCREEN_WIDTH - POWERUP_SIZE)
                    y = random.randint(POWERUP_SIZE, SCREEN_HEIGHT - POWERUP_SIZE)
                    self.powerups.append(Powerup(x, y, 'invincible'))
            else:
                self.spawn_powerup()

            # Update boss
            if self.boss:
                self.boss.update()
                self.boss.move_towards(self.player.x, self.player.y)
                
                # Check boss attack
                if self.boss.can_attack():
                    distance = math.sqrt((self.player.x - self.boss.x)**2 + (self.player.y - self.boss.y)**2)
                    if distance < self.player.radius + self.boss.radius:
                        self.player.take_damage(self.boss.attack())
                
                # Check boss health
                if self.boss.health <= 0:
                    self.boss = None
                    if not self.boss_defeated:
                        # First boss defeated
                        self.boss_spawned = False
                        self.boss_defeated = True
                        self.player.zombinos += 1000  # Big reward for defeating first boss
                        self.player.zombinos_earned += 1000
                        if self.boss_music:
                            self.boss_music.stop()  # Stop boss music when boss is defeated
                        print("First boss defeated! Music stopped.")
                        
                        # Make zombies 15% stronger
                        for zombie in self.zombies:
                            zombie.health *= 1.15
                            zombie.max_health *= 1.15
                            zombie.damage *= 1.15
                            zombie.speed *= 1.15
                        print("Zombies became 15% stronger!")
                    else:
                        # Second boss defeated
                        self.second_boss_spawned = False
                        self.second_boss_defeated = True
                        self.player.zombinos += 2000  # Even bigger reward for second boss
                        self.player.zombinos_earned += 2000
                        if self.boss_music:
                            self.boss_music.stop()
                        print("Second boss defeated! Music stopped.")

            # Update zombies
            for zombie in self.zombies[:]:
                zombie.move_towards(self.player.x, self.player.y)
                
                # Check collision with player
                distance = math.sqrt((self.player.x - zombie.x)**2 + (self.player.y - zombie.y)**2)
                if distance < self.player.radius + zombie.radius:
                    self.player.take_damage(zombie.damage)
                
                # Remove dead zombies
                if zombie.health <= 0:
                    self.zombies.remove(zombie)
                    self.player.zombinos += ZOMBINOS_PER_KILL
                    self.player.zombinos_earned += ZOMBINOS_PER_KILL
                    self.player.save_progress()

            # Update powerups
            for powerup in self.powerups[:]:
                if powerup.check_collision(self.player):
                    self.player.collect_powerup(powerup)
                    self.powerups.remove(powerup)

            # Update survival time
            self.player.survival_time += 1/FPS

            # Check if player is dead
            if self.player.health <= 0:
                self.state = "GAME_OVER"

    def spawn_boss(self):
        # Spawn boss at random edge
        side = random.randint(0, 3)
        if side == 0:  # top
            x = random.randint(0, SCREEN_WIDTH)
            y = -BOSS_SIZE
        elif side == 1:  # right
            x = SCREEN_WIDTH + BOSS_SIZE
            y = random.randint(0, SCREEN_HEIGHT)
        elif side == 2:  # bottom
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + BOSS_SIZE
        else:  # left
            x = -BOSS_SIZE
            y = random.randint(0, SCREEN_HEIGHT)
        
        self.boss = BossZombie(x, y)
        if self.boss_defeated:
            self.second_boss_spawned = True
        else:
            self.boss_spawned = True
        # Play boss music when boss spawns
        if not self.music_muted:
            self.boss_music.set_volume(0.2)  # 20% volume
            self.boss_music.play(-1)  # -1 for infinite loop

    def draw_game(self):
        # Draw background
        try:
            if field_bg:
                self.screen.blit(field_bg, (0, 0))
            else:
                self.screen.fill(BLACK)
        except Exception as e:
            print(f"Warning: Could not draw background: {e}")
            self.screen.fill(BLACK)
        
        # Draw boss progress bars
        if not self.boss_spawned and not self.boss_defeated:
            # First boss progress bar
            pygame.draw.rect(self.screen, RED, 
                           (self.boss_progress_bar_x, self.boss_progress_bar_y,
                            self.boss_progress_bar_width, self.boss_progress_bar_height))
            current_width = self.boss_progress * self.boss_progress_bar_width
            pygame.draw.rect(self.screen, GREEN,
                           (self.boss_progress_bar_x, self.boss_progress_bar_y,
                            current_width, self.boss_progress_bar_height))
        
        # Draw boss health bar if boss is present
        if self.boss:
            pygame.draw.rect(self.screen, RED, 
                           (self.boss_health_bar_x, self.boss_health_bar_y,
                            self.boss_health_bar_width, self.boss_health_bar_height))
            current_width = (self.boss.health / self.boss.max_health) * self.boss_health_bar_width
            pygame.draw.rect(self.screen, GREEN,
                           (self.boss_health_bar_x, self.boss_health_bar_y,
                            current_width, self.boss_health_bar_height))
        elif self.boss_defeated and not self.second_boss_spawned and not self.second_boss_defeated:
            print(f"Drawing second boss progress bar - Progress: {self.second_boss_progress:.2f}")
            print(f"Conditions - Boss defeated: {self.boss_defeated}, Second spawned: {self.second_boss_spawned}, Second defeated: {self.second_boss_defeated}")
            # Second boss progress bar (only shown after first boss is defeated)
            pygame.draw.rect(self.screen, RED, 
                           (self.boss_progress_bar_x, self.second_boss_progress_bar_y,
                            self.boss_progress_bar_width, self.boss_progress_bar_height))
            current_width = self.second_boss_progress * self.boss_progress_bar_width
            pygame.draw.rect(self.screen, GREEN,
                           (self.boss_progress_bar_x, self.second_boss_progress_bar_y,
                            current_width, self.boss_progress_bar_height))
        
        # Draw player and weapon
        if self.player:
            self.player.draw(self.screen)
        
        # Draw boss if present
        if self.boss:
            self.boss.draw(self.screen)
        
        # Draw zombies
        for zombie in self.zombies:
            zombie.draw(self.screen)
        
        # Draw explosions
        for explosion in self.explosions[:]:
            if explosion_img:
                explosion_rect.center = (int(explosion['x']), int(explosion['y']))
                self.screen.blit(explosion_img, explosion_rect)
            else:
                pygame.draw.circle(self.screen, YELLOW, 
                                 (int(explosion['x']), int(explosion['y'])), 
                                 50)
            explosion['timer'] -= 1
            if explosion['timer'] <= 0:
                self.explosions.remove(explosion)
        
        # Draw powerups
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        # Draw HUD
        time_text = self.font.render(f"Time: {int(self.player.survival_time)}s", True, WHITE)
        health_text = self.font.render(f"Health: {int(self.player.health)}", True, WHITE)
        nuke_text = self.font.render("Nuke Ready!" if self.player.nuke_available else "", True, YELLOW)
        zombinos_text = self.font.render(f"{self.player.zombinos}", True, WHITE)
        
        # Position HUD elements
        self.screen.blit(time_text, (20, 20))
        self.screen.blit(health_text, (20, 80))
        
        # Draw nuke ready text above Zombinos
        if self.player.nuke_available:
            nuke_rect = nuke_text.get_rect(topleft=(20, 120))
            self.screen.blit(nuke_text, nuke_rect)
        
        # Draw Zombinos with gold image on the left
        if gold_img:
            gold_rect.topleft = (20, 140)
            zombinos_rect = zombinos_text.get_rect(midleft=(gold_rect.right + 10, gold_rect.centery - 5))
            
            self.screen.blit(gold_img, gold_rect)
            self.screen.blit(zombinos_text, zombinos_rect)
        else:
            zombinos_text = self.font.render(f"Zombinos: {self.player.zombinos}", True, WHITE)
            self.screen.blit(zombinos_text, (20, 140))

        # Draw dash cooldown bar and icon in bottom left corner
        if self.player:
            # Draw dash icon
            if dash_img:
                dash_rect = dash_img.get_rect(topleft=(20, SCREEN_HEIGHT - 80))  # Positioned above cooldown bar
                self.screen.blit(dash_img, dash_rect)
            
            # Background of cooldown bar (white when empty)
            pygame.draw.rect(self.screen, WHITE, 
                           (dash_rect.right + 10, SCREEN_HEIGHT - 50,  # Positioned to the right of dash icon
                            self.dash_cooldown_bar_width, self.dash_cooldown_bar_height))
            
            # Current cooldown (blue when full)
            if self.player.dash_cooldown > 0:
                cooldown_width = (1 - self.player.dash_cooldown / DASH_COOLDOWN) * self.dash_cooldown_bar_width
                pygame.draw.rect(self.screen, DASH_COLOR,
                               (dash_rect.right + 10, SCREEN_HEIGHT - 50,  # Positioned to the right of dash icon
                                cooldown_width, self.dash_cooldown_bar_height))
            else:
                pygame.draw.rect(self.screen, DASH_COLOR,
                               (dash_rect.right + 10, SCREEN_HEIGHT - 50,  # Positioned to the right of dash icon
                                self.dash_cooldown_bar_width, self.dash_cooldown_bar_height))

    def draw_menu(self):
        # Draw background
        if menu_bg:
            self.screen.blit(menu_bg, (0, 0))
        else:
            self.screen.fill(BLACK)
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        self.play_button.check_hover(mouse_pos)
        self.upgrades_button.check_hover(mouse_pos)
        self.quit_button.check_hover(mouse_pos)
        self.mute_button.check_hover(mouse_pos)
        
        self.play_button.draw(self.screen)
        self.upgrades_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        self.mute_button.draw(self.screen)

        # Draw quit confirmation popup if active
        if self.show_quit_confirmation:
            # Create semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Black with 50% opacity
            self.screen.blit(overlay, (0, 0))
            
            # Draw popup text
            quit_text = self.title_font.render("Do you want to Quit Game?", True, RED)
            quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(quit_text, quit_rect)
            
            # Draw confirmation buttons
            self.yes_button.check_hover(mouse_pos)
            self.no_button.check_hover(mouse_pos)
            self.yes_button.draw(self.screen)
            self.no_button.draw(self.screen)

    def draw_upgrades(self):
        # Draw background
        if brick_bg:
            self.screen.blit(brick_bg, (0, 0))
        else:
            self.screen.fill(BLACK)
        
        # Draw title
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("UPGRADES", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Draw zombinos with gold image in center of screen
        if gold_img:
            zombinos_text = self.font.render(f"{self.player.zombinos if self.player else 0}", True, WHITE)
            zombinos_rect = zombinos_text.get_rect()
            gold_rect = gold_img.get_rect()
            
            # Position the gold icon and text in center, icon moved down
            gold_rect.center = (SCREEN_WIDTH//2 - 60, 320)  # Moved down from 300 to 320
            zombinos_rect.midleft = (gold_rect.right + 10, gold_rect.centery - 5)
            
            self.screen.blit(gold_img, gold_rect)
            self.screen.blit(zombinos_text, zombinos_rect)
        else:
            # Fallback to text only if image not loaded
            zombinos_text = self.font.render(f"Zombinos: {self.player.zombinos if self.player else 0}", True, WHITE)
            zombinos_rect = zombinos_text.get_rect(center=(SCREEN_WIDTH//2, 300))
            self.screen.blit(zombinos_text, zombinos_rect)
        
        # Draw buttons first (at the bottom)
        mouse_pos = pygame.mouse.get_pos()
        self.damage_upgrade_button.check_hover(mouse_pos)
        self.health_upgrade_button.check_hover(mouse_pos)
        self.back_button.check_hover(mouse_pos)
        
        self.damage_upgrade_button.draw(self.screen)
        self.health_upgrade_button.draw(self.screen)
        self.back_button.draw(self.screen)
        
        # Draw upgrade costs above the buttons
        if self.player:
            damage_cost = self.player.get_damage_upgrade_cost()
            health_cost = self.player.get_health_upgrade_cost()
            
            # Draw damage upgrade cost with gold image (under damage button)
            if gold_img:
                gold_rect.center = (self.damage_upgrade_button.rect.centerx - 60, self.damage_upgrade_button.rect.bottom + 30)
                self.screen.blit(gold_img, gold_rect)
                damage_cost_text = self.font.render(f"{damage_cost}", True, WHITE)
                damage_cost_rect = damage_cost_text.get_rect(midleft=(self.damage_upgrade_button.rect.centerx - 20, self.damage_upgrade_button.rect.bottom + 55))
                self.screen.blit(damage_cost_text, damage_cost_rect)
            else:
                damage_cost_text = self.font.render(f"Cost: {damage_cost} Zombinos", True, WHITE)
                damage_cost_rect = damage_cost_text.get_rect(center=(self.damage_upgrade_button.rect.centerx, self.damage_upgrade_button.rect.bottom + 30))
                self.screen.blit(damage_cost_text, damage_cost_rect)
            
            # Draw health upgrade cost with gold image (under health button)
            if gold_img:
                gold_rect.center = (self.health_upgrade_button.rect.centerx - 60, self.health_upgrade_button.rect.bottom + 30)
                self.screen.blit(gold_img, gold_rect)
                health_cost_text = self.font.render(f"{health_cost}", True, WHITE)
                health_cost_rect = health_cost_text.get_rect(midleft=(self.health_upgrade_button.rect.centerx - 20, self.health_upgrade_button.rect.bottom + 55))
                self.screen.blit(health_cost_text, health_cost_rect)
            else:
                health_cost_text = self.font.render(f"Cost: {health_cost} Zombinos", True, WHITE)
                health_cost_rect = health_cost_text.get_rect(center=(self.health_upgrade_button.rect.centerx, self.health_upgrade_button.rect.bottom + 30))
                self.screen.blit(health_cost_text, health_cost_rect)

    def draw_game_over(self):
        # Draw black background
        self.screen.fill(BLACK)
        
        # Draw game over text
        game_over_text = self.title_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 150))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Draw final score
        score_text = self.font.render(f"Final Score: {int(self.player.survival_time)}s", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(score_text, score_rect)
        
        # Draw zombinos earned
        zombinos_text = self.font.render(f"Zombinos Earned: {self.player.zombinos_earned}", True, WHITE)
        zombinos_rect = zombinos_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(zombinos_text, zombinos_rect)
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        self.play_again_button.check_hover(mouse_pos)
        self.game_over_menu_button.check_hover(mouse_pos)
        
        self.play_again_button.draw(self.screen)
        self.game_over_menu_button.draw(self.screen)

    def draw_pause(self):
        # Draw the game state in the background
        self.draw_game()
        
        # Create a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% opacity
        self.screen.blit(overlay, (0, 0))
        
        # Draw pause text
        pause_text = self.title_font.render("PAUSE", True, RED)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        self.screen.blit(pause_text, pause_rect)
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        self.resume_button.check_hover(mouse_pos)
        self.pause_menu_button.check_hover(mouse_pos)
        
        self.resume_button.draw(self.screen)
        self.pause_menu_button.draw(self.screen)

    def run(self):
        while self.running:
            self.handle_events()
            if self.state != "PAUSE":  # Only update game when not paused
                self.update_game()
            
            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "PLAY":
                self.draw_game()
            elif self.state == "PAUSE":
                self.draw_pause()
            elif self.state == "UPGRADES":
                self.draw_upgrades()
            elif self.state == "GAME_OVER":
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit() 