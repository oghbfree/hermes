"""
[TITLE] — Akoma Robotics
[DESCRIPTION]
3Blue1Brown-inspired, Akoma color palette (purple/gold/white)
"""

from manim import *

BG = "#F5F0FF"
PRIMARY = "#6A0DAD"
SECONDARY = "#FFD700"
ACCENT = "#FF6B35"
MONO = "Consolas"

class Scene1_Opening(Scene):
    def construct(self):
        self.camera.background_color = BG
        title = Text("[TITLE]", font_size=48, color=PRIMARY, weight=BOLD, font=MONO)
        subtitle = Text("[SUBTITLE]", font_size=28, color=ACCENT, font=MONO)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.8)

class Scene2_Content(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Add content scene here
        label = Text("[CONTENT]", font_size=36, color=PRIMARY, font=MONO)
        self.play(Write(label), run_time=1.5)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))

class Scene3_CTA(Scene):
    def construct(self):
        self.camera.background_color = BG
        cta1 = Text("Akoma Robotics", font_size=44, color=PRIMARY, weight=BOLD, font=MONO)
        cta2 = Text("Building Africa's Future, One Robot at a Time", font_size=24, color=ACCENT, font=MONO)
        cta2.next_to(cta1, DOWN, buff=0.4)
        cta3 = Text("📞 +233 55 123 4567", font_size=28, color=SECONDARY, font=MONO, weight=BOLD)
        cta3.next_to(cta2, DOWN, buff=0.8)

        self.play(Write(cta1), run_time=1.2)
        self.play(FadeIn(cta2, shift=UP), run_time=0.8)
        self.play(FadeIn(cta3, scale=1.1), run_time=0.8)
        self.wait(3.0)
        self.play(FadeOut(Group(*self.mobjects)))
