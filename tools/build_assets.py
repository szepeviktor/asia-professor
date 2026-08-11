from __future__ import annotations

import math
import subprocess
import wave
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FRAMES = ASSETS / "frames"


@dataclass(frozen=True)
class Scene:
    slug: str
    culture: str
    theme: str
    palette: tuple[str, str, str, str]
    audio: tuple[float, ...]


SCENES = [
    Scene("china-clothes", "china", "clothes", ("#8f1d25", "#d6a540", "#1b2636", "#f4ddbc"), (392, 440, 523, 659)),
    Scene("japan-clothes", "japan", "clothes", ("#f8f0ee", "#c24d64", "#273347", "#8bb6a6"), (440, 554, 659, 740)),
    Scene("china-music", "china", "music", ("#6f1d1b", "#dba544", "#273347", "#ead2a6"), (330, 392, 440, 587)),
    Scene("japan-music", "japan", "music", ("#ede5d9", "#a73535", "#222f3f", "#d6ae58"), (196, 196, 294, 330)),
    Scene("china-food", "china", "food", ("#b92d2d", "#f1ca72", "#273347", "#fff0d8"), (523, 587, 659, 523)),
    Scene("japan-food", "japan", "food", ("#f5f1e8", "#db5c6d", "#1f4f5f", "#2b323a"), (587, 659, 740, 880)),
    Scene("china-festival", "china", "festival", ("#9f2028", "#e5af36", "#17212b", "#f7ddbd"), (392, 523, 659, 784)),
    Scene("japan-festival", "japan", "festival", ("#eff4f2", "#d84c60", "#246b7a", "#f1c767"), (440, 494, 587, 659)),
    Scene("china-building", "china", "building", ("#8e2526", "#d0a045", "#253140", "#e8cf9f"), (294, 392, 523, 587)),
    Scene("japan-building", "japan", "building", ("#f3efe6", "#ba3949", "#23394a", "#7aa698"), (330, 440, 554, 659)),
]


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def blend(a: str, b: str, t: float) -> tuple[int, int, int]:
    ar, ag, ab = hex_to_rgb(a)
    br, bg, bb = hex_to_rgb(b)
    return (
        int(ar + (br - ar) * t),
        int(ag + (bg - ag) * t),
        int(ab + (bb - ab) * t),
    )


def background(draw: ImageDraw.ImageDraw, scene: Scene, w: int, h: int) -> None:
    top, mid, ink, paper = scene.palette
    for y in range(h):
        t = y / max(1, h - 1)
        color = blend(paper, "#ffffff" if scene.culture == "japan" else mid, t * 0.35)
        draw.line((0, y, w, y), fill=color)
    for i in range(9):
        x = int((i + 0.5) * w / 9)
        draw.line((x, 0, x - 140, h), fill=(*hex_to_rgb(ink), 22), width=2)
    draw.ellipse((-180, -160, 340, 340), fill=(*hex_to_rgb(mid), 32))
    draw.ellipse((w - 270, h - 250, w + 160, h + 180), fill=(*hex_to_rgb(top), 28))


def draw_chinese_robe(draw: ImageDraw.ImageDraw, s: Scene) -> None:
    red, gold, ink, _ = s.palette
    draw.polygon([(310, 210), (470, 210), (550, 610), (230, 610)], fill=red, outline=ink)
    draw.polygon([(330, 210), (390, 330), (450, 210)], fill="#f8d37a")
    draw.line((390, 220, 345, 610), fill=gold, width=12)
    draw.line((290, 315, 490, 315), fill=gold, width=10)
    draw.polygon([(230, 280), (130, 430), (220, 450), (320, 290)], fill=red, outline=ink)
    draw.polygon([(550, 280), (660, 430), (565, 450), (460, 290)], fill=red, outline=ink)
    for x in (335, 445):
        draw.ellipse((x - 24, 388, x + 24, 436), outline=gold, width=7)


def draw_japanese_kimono(draw: ImageDraw.ImageDraw, s: Scene) -> None:
    paper, pink, ink, green = s.palette
    draw.polygon([(305, 205), (475, 205), (560, 610), (220, 610)], fill=paper, outline=ink)
    draw.polygon([(325, 210), (390, 365), (455, 210)], fill=pink)
    draw.line((390, 220, 390, 610), fill=ink, width=7)
    draw.rectangle((280, 388, 500, 468), fill=green, outline=ink, width=4)
    draw.polygon([(225, 280), (115, 455), (220, 472), (320, 292)], fill="#f7dedc", outline=ink)
    draw.polygon([(555, 280), (665, 455), (560, 472), (460, 292)], fill="#f7dedc", outline=ink)
    for cx, cy in [(315, 315), (475, 330), (360, 520), (455, 545)]:
        draw_flower(draw, cx, cy, 18, pink)


def draw_chinese_instrument(draw: ImageDraw.ImageDraw, s: Scene) -> None:
    red, gold, ink, _ = s.palette
    draw.rounded_rectangle((175, 365, 625, 455), radius=40, fill="#a7662d", outline=ink, width=5)
    draw.polygon([(220, 365), (580, 320), (625, 455), (170, 455)], fill="#c9863f", outline=ink)
    for i in range(8):
        y = 382 + i * 8
        draw.line((205, y, 600, y - 43), fill=gold, width=2)
    for x in range(245, 565, 58):
        draw.polygon([(x, 338), (x + 20, 405), (x - 10, 408)], fill=ink)
    draw_lantern(draw, 580, 160, 72, red, gold, ink)
    draw_lantern(draw, 210, 180, 58, red, gold, ink)


def draw_japanese_drums(draw: ImageDraw.ImageDraw, s: Scene) -> None:
    paper, red, ink, gold = s.palette
    draw.ellipse((215, 245, 585, 535), fill="#9c4e2e", outline=ink, width=7)
    draw.ellipse((250, 275, 550, 505), fill=paper, outline=ink, width=7)
    draw.ellipse((340, 345, 460, 435), outline=red, width=8)
    draw.line((250, 190, 500, 115), fill=ink, width=14)
    draw.line((550, 190, 300, 115), fill=ink, width=14)
    draw.ellipse((230, 170, 270, 210), fill=gold, outline=ink, width=4)
    draw.ellipse((530, 170, 570, 210), fill=gold, outline=ink, width=4)
    draw_torii(draw, 82, 128, 150, red, ink)
    draw_flower(draw, 648, 170, 28, red)


def draw_chinese_food(draw: ImageDraw.ImageDraw, s: Scene) -> None:
    red, gold, ink, paper = s.palette
    draw.ellipse((175, 350, 625, 585), fill="#f8e5c1", outline=ink, width=5)
    for x, y, r in [(285, 382, 62), (390, 358, 70), (505, 392, 58), (355, 458, 66), (475, 472, 62)]:
        draw.arc((x - r, y - r, x + r, y + r), 190, 350, fill=ink, width=5)
        draw.pieslice((x - r, y - r, x + r, y + r), 180, 360, fill=paper, outline=ink, width=4)
        for k in range(4):
            draw.line((x - r + 22 + k * 18, y - 5, x - r + 35 + k * 18, y - 45), fill=gold, width=2)
    draw_lantern(draw, 145, 160, 65, red, gold, ink)
    draw.line((560, 140, 680, 330), fill=ink, width=9)
    draw.line((590, 132, 710, 322), fill=ink, width=9)


def draw_japanese_food(draw: ImageDraw.ImageDraw, s: Scene) -> None:
    paper, pink, ink, teal = s.palette
    draw.rounded_rectangle((170, 345, 630, 555), radius=42, fill=paper, outline=ink, width=5)
    for x, y, filling in [(270, 420, pink), (390, 430, "#f4d060"), (510, 415, teal)]:
        draw.ellipse((x - 58, y - 58, x + 58, y + 58), fill="#1d2730", outline=ink, width=4)
        draw.ellipse((x - 42, y - 42, x + 42, y + 42), fill="#faf8f2")
        draw.ellipse((x - 20, y - 20, x + 20, y + 20), fill=filling)
    draw.polygon([(340, 205), (450, 205), (500, 300), (290, 300)], fill="#f8f8f2", outline=ink)
    draw.rectangle((310, 258, 480, 318), fill="#16232b")
    draw_flower(draw, 612, 165, 30, pink)


def draw_chinese_festival(draw: ImageDraw.ImageDraw, s: Scene) -> None:
    red, gold, ink, _ = s.palette
    for x, y, size in [(190, 180, 86), (400, 155, 100), (610, 190, 78)]:
        draw_lantern(draw, x, y, size, red, gold, ink)
    points = [(170, 450), (250, 385), (335, 430), (425, 360), (525, 400), (640, 320)]
    draw.line(points, fill=gold, width=36, joint="curve")
    draw.line(points, fill=red, width=20, joint="curve")
    draw.ellipse((610, 275, 705, 360), fill=gold, outline=ink, width=5)
    draw.polygon([(690, 315), (735, 295), (710, 335)], fill=red, outline=ink)
    for x, y in points[1:-1]:
        draw.ellipse((x - 13, y - 13, x + 13, y + 13), fill=ink)


def draw_japanese_festival(draw: ImageDraw.ImageDraw, s: Scene) -> None:
    paper, red, teal, gold = s.palette
    draw.line((170, 160, 170, 560), fill=teal, width=10)
    for i, (y, color) in enumerate([(185, red), (285, gold), (385, teal)]):
        draw.polygon([(180, y), (430, y + 28), (180, y + 70)], fill=color, outline="#203040")
        draw.polygon([(430, y + 28), (480, y), (480, y + 80)], fill=paper, outline="#203040")
        draw.ellipse((240, y + 20, 300, y + 58), fill=paper, outline="#203040", width=3)
    draw_torii(draw, 505, 340, 190, red, "#203040")
    for cx, cy in [(570, 155), (625, 205), (520, 230)]:
        draw_flower(draw, cx, cy, 23, red)


def draw_chinese_building(draw: ImageDraw.ImageDraw, s: Scene) -> None:
    red, gold, ink, paper = s.palette
    for level, y in enumerate([445, 340, 250]):
        width = 470 - level * 100
        x0 = 400 - width // 2
        x1 = 400 + width // 2
        draw.polygon([(x0 - 65, y), (x1 + 65, y), (x1, y + 52), (x0, y + 52)], fill=red, outline=ink)
        draw.rectangle((x0 + 25, y + 52, x1 - 25, y + 112), fill=paper, outline=ink, width=4)
        for x in range(x0 + 55, x1 - 40, 68):
            draw.line((x, y + 58, x, y + 108), fill=gold, width=7)
    draw.rectangle((300, 555, 500, 620), fill=ink)
    draw.ellipse((373, 180, 427, 234), fill=gold)
    draw_lantern(draw, 155, 175, 60, red, gold, ink)
    draw_lantern(draw, 645, 175, 60, red, gold, ink)


def draw_japanese_building(draw: ImageDraw.ImageDraw, s: Scene) -> None:
    paper, red, ink, teal = s.palette
    draw_torii(draw, 205, 215, 390, red, ink)
    draw.polygon([(500, 235), (660, 500), (340, 500)], fill="#dfe8e5", outline=ink)
    draw.polygon([(500, 235), (568, 500), (432, 500)], fill="#f7f7f2")
    draw.rectangle((0, 500, 800, 640), fill=teal)
    for cx, cy in [(145, 175), (610, 170), (690, 255), (95, 280)]:
        draw_flower(draw, cx, cy, 22, red)


def draw_lantern(draw: ImageDraw.ImageDraw, x: int, y: int, size: int, red: str, gold: str, ink: str) -> None:
    draw.line((x, y - size // 2, x, y - size), fill=ink, width=3)
    draw.ellipse((x - size // 2, y - size // 2, x + size // 2, y + size // 2), fill=red, outline=ink, width=4)
    draw.rectangle((x - size // 3, y - size // 2 - 6, x + size // 3, y - size // 2 + 8), fill=gold)
    draw.rectangle((x - size // 3, y + size // 2 - 8, x + size // 3, y + size // 2 + 6), fill=gold)
    for dx in (-size // 5, 0, size // 5):
        draw.arc((x - size // 2 + dx, y - size // 2, x + size // 2 + dx, y + size // 2), 90, 270, fill=gold, width=2)


def draw_torii(draw: ImageDraw.ImageDraw, x: int, y: int, width: int, red: str, ink: str) -> None:
    draw.rounded_rectangle((x, y, x + width, y + 32), radius=5, fill=red, outline=ink, width=3)
    draw.rectangle((x + 28, y + 38, x + width - 28, y + 68), fill=red, outline=ink, width=3)
    draw.rectangle((x + 70, y + 65, x + 105, y + 260), fill=red, outline=ink, width=3)
    draw.rectangle((x + width - 105, y + 65, x + width - 70, y + 260), fill=red, outline=ink, width=3)


def draw_flower(draw: ImageDraw.ImageDraw, cx: int, cy: int, r: int, color: str) -> None:
    for angle in range(0, 360, 72):
        dx = math.cos(math.radians(angle)) * r
        dy = math.sin(math.radians(angle)) * r
        draw.ellipse((cx + dx - r * .55, cy + dy - r * .55, cx + dx + r * .55, cy + dy + r * .55), fill=color)
    draw.ellipse((cx - r * .35, cy - r * .35, cx + r * .35, cy + r * .35), fill="#f5d36d")


DRAWERS = {
    "china-clothes": draw_chinese_robe,
    "japan-clothes": draw_japanese_kimono,
    "china-music": draw_chinese_instrument,
    "japan-music": draw_japanese_drums,
    "china-food": draw_chinese_food,
    "japan-food": draw_japanese_food,
    "china-festival": draw_chinese_festival,
    "japan-festival": draw_japanese_festival,
    "china-building": draw_chinese_building,
    "japan-building": draw_japanese_building,
}


def render_scene(scene: Scene, frame: int | None = None) -> Image.Image:
    w, h = 800, 640
    image = Image.new("RGBA", (w, h), "#ffffff")
    draw = ImageDraw.Draw(image, "RGBA")
    background(draw, scene, w, h)
    if frame is not None:
        shift = int(math.sin(frame / 30 * math.tau) * 10)
        draw.ellipse((95 + shift, 78, 195 + shift, 178), fill=(*hex_to_rgb(scene.palette[1]), 36))
        draw.ellipse((590 - shift, 420, 730 - shift, 560), fill=(*hex_to_rgb(scene.palette[0]), 30))
    DRAWERS[scene.slug](draw, scene)
    return image.filter(ImageFilter.UnsharpMask(radius=1, percent=105, threshold=3)).convert("RGB")


def make_image(scene: Scene) -> None:
    render_scene(scene).save(ASSETS / f"{scene.slug}.png", quality=95)


def make_video(scene: Scene) -> None:
    out_dir = FRAMES / scene.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    for frame in range(36):
        render_scene(scene, frame).save(out_dir / f"frame-{frame:03d}.png")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            "12",
            "-i",
            str(out_dir / "frame-%03d.png"),
            "-vf",
            "scale=800:640,format=yuv420p",
            "-movflags",
            "+faststart",
            str(ASSETS / f"{scene.slug}.mp4"),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def make_audio(scene: Scene) -> None:
    rate = 44100
    seconds = 1.35
    total = int(rate * seconds)
    data: list[int] = []
    for i in range(total):
        t = i / rate
        note = scene.audio[min(int(t / (seconds / len(scene.audio))), len(scene.audio) - 1)]
        env = min(1.0, t * 16) * min(1.0, (seconds - t) * 7)
        tone = math.sin(math.tau * note * t) * 0.45
        tone += math.sin(math.tau * note * 2 * t) * 0.08
        if scene.theme in {"festival", "music"} and int(t * 8) % 2 == 0:
            tone += math.sin(math.tau * 90 * t) * 0.12
        data.append(int(max(-1, min(1, tone * env)) * 32767))
    with wave.open(str(ASSETS / f"{scene.slug}.wav"), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(b"".join(sample.to_bytes(2, "little", signed=True) for sample in data))


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    FRAMES.mkdir(exist_ok=True)
    for scene in SCENES:
        make_image(scene)
        make_video(scene)
        make_audio(scene)


if __name__ == "__main__":
    main()
