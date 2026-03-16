import pygame
import sys
import random
import os
import math
from src.utils.constants import *
from src.ui.elements import UIButton, ProgressBar, GameLog
from src.entities.player import Player
from src.entities.board import Board
from src.core.input_handler import InputHandler
from src.core.renderer import Renderer

class GameStateMachine:
    def __init__(self, screen):
        self.screen = screen
        self.renderer = Renderer(screen)
        self.inputs = InputHandler()
        self.state = "MENU"
        self.max_turns = 80
        self.show_help = False
        self.fonts = {
            "title": pygame.font.SysFont("Verdana", 72, bold=True),
            "ui": pygame.font.SysFont("Verdana", 24, bold=True),
            "small": pygame.font.SysFont("Verdana", 16),
            "story": pygame.font.SysFont("Courier New", 22, bold=True)
        }
        self.menu_buttons = [
            UIButton(WIDTH//2 - 125, 450, 250, 50, "MİSYONA ATIL", self.fonts["ui"], COLOR_ACCENT, self.start_story),
            UIButton(WIDTH//2 - 125, 520, 250, 50, "ÇIKIŞ", self.fonts["ui"], COLOR_DANGER, sys.exit)
        ]
        self.game_log = GameLog(WIDTH - 300, 300, self.fonts["small"])
        self.reset_game()
        self.nebula_glows = self.init_nebula()
        self.story_images = {}

    def reset_game(self):
        self.chapter_index = 0
        self.story_timer = 0
        self.board = Board()
        self.runners = []
        self.turn = 0
        self.game_turn_count = 0
        self.no_move_rounds = 0
        self.winner = None
        self.game_log.messages = []
        self.inputs.clear()

    def init_nebula(self):
        return [{"pos": [random.randint(0, WIDTH), random.randint(0, HEIGHT)], "size": random.randint(100, 400), "alpha": random.randint(30, 80), "speed": random.uniform(0.1, 0.3)} for _ in range(15)]

    def start_story(self):
        self.state = "STORY"
        for i, ch in enumerate(STORY_CHAPTERS):
            try: self.story_images[i] = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", ch["panel"])), (WIDTH, HEIGHT))
            except: pass

    def init_game(self):
        self.runners = [Player("Alpha", "TITAN"), Player("Beta", "PHANTOM"), Player("Gamma", "SAGE"), Player("Delta", "ROGUE")]
        corners = [[0, 0], [0, 11], [11, 0], [11, 11]]
        for i, p in enumerate(self.runners):
            p.move_to(corners[i][0], corners[i][1])
            p.visual_pos = [float(corners[i][0]), float(corners[i][1])]
        self.state = "PLAY"
        self.show_help = True
        self.game_log.add_message("SİSTEM ÇALIŞTI. ANAHTARLARI BUL VE MERKEZE KAÇ!", COLOR_ACCENT)

    def update(self):
        if self.state == "STORY":
            self.story_timer += 1
            if self.story_timer > 300:
                self.chapter_index += 1
                self.story_timer = 0
                if self.chapter_index >= len(STORY_CHAPTERS): self.init_game()
        
        if self.state == "PLAY":
            for p in self.runners: p.update()
            for glow in self.nebula_glows:
                glow["pos"][0] += glow["speed"]
                if glow["pos"][0] > WIDTH + 400: glow["pos"][0] = -400
            
            self.process_input_queue()

    def process_input_queue(self):
        curr_p = self.runners[self.turn % 4]
        dist = math.sqrt((curr_p.pos_coord[0] - curr_p.visual_pos[0])**2 + (curr_p.pos_coord[1] - curr_p.visual_pos[1])**2)
        if dist < 0.05:
            cmd = self.inputs.get_next_command()
            if not cmd:
                return

            if cmd == "ACTION":
                return

            if cmd in ["UP", "DOWN", "LEFT", "RIGHT"]:
                move_map = {"UP": [-1, 0], "DOWN": [1, 0], "LEFT": [0, -1], "RIGHT": [0, 1]}
                m = move_map[cmd]
                nr, nc = curr_p.pos_coord[0] + m[0], curr_p.pos_coord[1] + m[1]

                target_valid = (
                    0 <= nr < 12
                    and 0 <= nc < 12
                    and self.board.tiles[(nr, nc)]["state"] != "VOID"
                )

                if not target_valid:
                    has_any_move = False
                    for dr, dc in move_map.values():
                        rr, cc = curr_p.pos_coord[0] + dr, curr_p.pos_coord[1] + dc
                        if (
                            0 <= rr < 12
                            and 0 <= cc < 12
                            and self.board.tiles[(rr, cc)]["state"] != "VOID"
                        ):
                            has_any_move = True
                            break

                    if not has_any_move:
                        self.game_log.add_message(
                            f"{curr_p.name} VOID tarafından sıkıştırıldı, tur pas geçildi.",
                            COLOR_PURPLE,
                        )
                        self.turn += 1
                        self.game_turn_count += 1
                        self.no_move_rounds += 1
                        if self.game_turn_count >= self.max_turns or self.no_move_rounds >= len(self.runners):
                            self.state = "GAME_OVER"
                            self.game_log.add_message("Void tüm koşucuları yuttu. Kimse kaçamadı.", COLOR_DANGER)
                        if self.game_turn_count % 8 == 0:
                            self.board.advance_void()
                            self.renderer.trigger_shake(8)
                    return

                curr_p.move_to(nr, nc)
                self.handle_mechanics(curr_p)
                self.turn += 1
                self.game_turn_count += 1
                self.no_move_rounds = 0
                if self.game_turn_count >= self.max_turns and not self.winner:
                    self.state = "GAME_OVER"
                    self.game_log.add_message("Zaman tükendi. Void her şeyi yuttu.", COLOR_DANGER)
                if self.game_turn_count % 8 == 0:
                    self.board.advance_void()
                    self.renderer.trigger_shake(8)

    def handle_mechanics(self, p):
        for k in self.board.keys_on_board[:]:
            if k[0] == p.pos_coord[0] and k[1] == p.pos_coord[1]:
                p.keys += 1
                self.board.keys_on_board.remove(k)
                self.game_log.add_message(f"{p.name} ANAHTAR BULDU!", COLOR_GOLD)
        
        for other in self.runners:
            if other != p and not other.is_dead and other.pos_coord == p.pos_coord:
                other.hp -= 30
                p.ammo -= 1
                self.game_log.add_message(f"ÇATIŞMA! {other.name} -30 HP", COLOR_DANGER)
                self.renderer.trigger_shake(4)
                if other.hp <= 0:
                    other.is_dead = True
                    self.game_log.add_message(f"{other.name} YOK EDİLDİ!", COLOR_PURPLE)

        if p.pos_coord == [6, 6] and p.keys >= 2:
            self.winner = p

    def draw(self):
        self.renderer.start_frame()
        canvas = self.renderer.canvas
        
        for glow in self.nebula_glows:
            s = pygame.Surface((glow["size"]*2, glow["size"]*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (30, 30, 80, glow["alpha"]), (glow["size"], glow["size"]), glow["size"])
            canvas.blit(s, (glow["pos"][0] - glow["size"], glow["pos"][1] - glow["size"]))

        if self.state == "MENU":
            title = self.fonts["title"].render("VOID ESCAPE", True, COLOR_ACCENT)
            canvas.blit(title, (WIDTH//2 - title.get_width()//2, 250))
            for btn in self.menu_buttons: btn.draw(canvas)

        elif self.state == "STORY":
            img = self.story_images.get(self.chapter_index)
            if img: canvas.blit(img, (0, 0))
            chapter_data = STORY_CHAPTERS[self.chapter_index]
            for i, line in enumerate(chapter_data["text"]):
                txt = self.fonts["story"].render(line, True, COLOR_TEXT)
                canvas.blit(txt, (WIDTH//2 - txt.get_width()//2, 500 + i * 40))

        elif self.state == "PLAY":
            self.board.draw(canvas, self.fonts["small"])
            for p in self.runners: p.draw(canvas)
            self.draw_hud(canvas)
            self.draw_turn_bar(canvas)
            self.game_log.draw(canvas)

            if self.show_help:
                self.draw_help_overlay(canvas)

        elif self.state == "GAME_OVER":
            self.board.draw(canvas, self.fonts["small"])
            for p in self.runners: p.draw(canvas)
            self.draw_hud(canvas)
            self.draw_turn_bar(canvas)
            self.game_log.draw(canvas)
            self.draw_game_over(canvas)

        if self.winner:
            self.draw_victory(canvas)
        
        self.renderer.end_frame()

    def draw_hud(self, canvas):
        panel = pygame.Rect(10, 10, 280, 220)
        pygame.draw.rect(canvas, (10, 10, 25, 230), panel, border_radius=15)
        curr_p = self.runners[self.turn % 4]
        canvas.blit(self.fonts["ui"].render(f"{curr_p.name}", True, curr_p.color), (30, 30))
        canvas.blit(self.fonts["small"].render(f"HP: {curr_p.hp} | AMMO: {curr_p.ammo}", True, COLOR_DANGER), (30, 75))
        canvas.blit(self.fonts["small"].render(f"ANAHTAR: {curr_p.keys}/2", True, COLOR_GOLD), (30, 105))
        canvas.blit(self.fonts["small"].render(f"VOID SEVİYE: {self.board.void_level}", True, COLOR_PURPLE), (30, 135))
        canvas.blit(self.fonts["small"].render("[WASD] Hareket Et | [ESC] Menü | [H] Yardım", True, (150, 150, 150)), (30, 180))

    def draw_turn_bar(self, canvas):
        if not self.runners:
            return

        bar_y = 10
        start_x = 320
        spacing = 90
        radius = 22
        active_idx = self.turn % len(self.runners)

        for i, p in enumerate(self.runners):
            x = start_x + i * spacing
            pygame.draw.circle(canvas, (10, 10, 35, 230), (x, bar_y + radius), radius + 6)
            pygame.draw.circle(canvas, p.color, (x, bar_y + radius), radius)

            if i == active_idx:
                pygame.draw.circle(canvas, COLOR_GOLD, (x, bar_y + radius), radius + 4, 3)

            name_txt = self.fonts["small"].render(p.name, True, COLOR_TEXT)
            name_rect = name_txt.get_rect(center=(x, bar_y + radius * 2 + 14))
            canvas.blit(name_txt, name_rect)

        turns_txt = self.fonts["small"].render(f"TUR: {self.game_turn_count} / {self.max_turns}", True, COLOR_TEXT)
        canvas.blit(turns_txt, (WIDTH - turns_txt.get_width() - 20, HEIGHT - 30))

    def draw_help_overlay(self, canvas):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        canvas.blit(overlay, (0, 0))

        lines = [
            "AMAÇ: 2 anahtar topla ve merkez kapsüle ulaş.",
            "TURLAR: Dört koşucu sırayla bir kare hareket eder.",
            "VOID: Her 8 hamlede kenarlardan içeri doğru ilerler.",
            "ÇATIŞMA: Aynı kareye gelen koşucular HP ve AMMO kaybeder.",
            "KONTROLLER: WASD hareket, ESC menü, H bu ekranı aç/kapa."
        ]
        start_y = 220
        title = self.fonts["title"].render("NASIL OYNANIR", True, COLOR_ACCENT)
        canvas.blit(title, (WIDTH//2 - title.get_width()//2, 140))
        for i, line in enumerate(lines):
            txt = self.fonts["story"].render(line, True, COLOR_TEXT)
            canvas.blit(txt, (WIDTH//2 - txt.get_width()//2, start_y + i * 40))

    def draw_victory(self, canvas):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 230))
        canvas.blit(overlay, (0,0))
        t = self.fonts["title"].render("TAHLİYE BAŞARILI!", True, self.winner.color)
        canvas.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//2 - 50))
        sub = self.fonts["ui"].render("ENTER: Yeniden Oyna  |  ESC: Menü", True, COLOR_TEXT)
        canvas.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 20))

    def draw_game_over(self, canvas):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 230))
        canvas.blit(overlay, (0, 0))
        t = self.fonts["title"].render("VOID HER ŞEYİ YUTTU", True, COLOR_DANGER)
        canvas.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//2 - 50))
        sub = self.fonts["ui"].render("ENTER: Yeniden Oyna  |  ESC: Menü", True, COLOR_TEXT)
        canvas.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 20))

    def handle_event(self, event):
        cmd = self.inputs.process_event(event)

        if cmd == "BACK":
            self.reset_game()
            self.state = "MENU"
            self.show_help = False
            return

        if self.state == "PLAY" and cmd == "HELP":
            self.show_help = not self.show_help
            return

        if (self.winner or self.state == "GAME_OVER") and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.reset_game()
                self.init_game()
                return

        if self.state == "MENU":
            for btn in self.menu_buttons: btn.handle_event(event)
        elif self.state == "STORY" and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.init_game()
