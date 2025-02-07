import io

from PIL import Image, ImageFont, ImageDraw

GREEN = (46, 204, 113)
YELLOW = (255, 228, 0)
RED = (237, 41, 57)
GRAY = (97, 109, 126)
BLUE = (10, 24, 34)
WHITE = (255, 255, 255)

statusmap = {"online": GREEN, "idle": YELLOW, "dnd": RED, "offline": GRAY}


def get_barstatus(title, statuses):
    highest = max(statuses.values())
    highest_unit = get_time_unit(highest)
    units = {stat: get_time_unit(value) for stat, value in statuses.items()}
    heights = {stat: (value / highest) * 250 for stat, value in statuses.items()}
    box_size = (400, 300)
    rect_x_start = {
        k: 64 + (84 * v)
        for k, v in {"online": 0, "idle": 1, "dnd": 2, "offline": 3}.items()
    }
    rect_width = 70
    rect_y_end = 275
    labels = {"online": "Online", "idle": "Idle", "dnd": "DND", "offline": "Offline"}
    base = Image.new(mode="RGBA", size=box_size, color=(0, 0, 0, 0))
    with Image.open("./data/assets/bargraph.png") as grid:
        font = ImageFont.truetype("./data/assets/Helvetica.ttf", 15)
        draw = ImageDraw.Draw(base)
        draw.text((0, 0), highest_unit[1], fill=WHITE, font=font)
        draw.text((52, 2), title, fill=WHITE, font=font)
        divs = 11
        for i in range(divs):
            draw.line(
                (
                    (50, 25 + ((box_size[1] - 50) / (divs - 1)) * i),
                    (box_size[0], 25 + ((box_size[1] - 50) / (divs - 1)) * i),
                ),
                fill=(*WHITE, 128),
                width=1,
            )
            draw.text(
                (5, 25 + ((box_size[1] - 50) / (divs - 1)) * i - 6),
                f"{highest_unit[0]-i*highest_unit[0]/(divs-1):.2f}",
                fill=WHITE,
                font=font,
            )
        for k, v in statuses.items():
            draw.rectangle(
                (
                    (rect_x_start[k], rect_y_end - heights[k]),
                    (rect_x_start[k] + rect_width, rect_y_end),
                ),
                fill=statusmap[k],
            )
            draw.text(
                (rect_x_start[k], rect_y_end - heights[k] - 13),
                f"{units[k][0]} {units[k][1]}",
                fill=WHITE,
                font=font,
            )
            draw.text(
                (rect_x_start[k], box_size[1] - 25), labels[k], fill=WHITE, font=font
            )
        del draw
        base.paste(grid, None, grid)
    buffer = io.BytesIO()
    base.save(buffer, "png")
    buffer.seek(0)
    return buffer


def get_time_unit(stat):
    word = ""
    if stat >= 604800:
        stat /= 604800
        word = "Week"
    elif stat >= 86400:
        stat /= 86400
        word = "Day"
    elif stat >= 3600:
        stat /= 3600
        word = "Hour"
    elif stat >= 60:
        stat /= 60
        word = "Minute"
    else:
        word = "Second"
    stat = float(f"{stat:.1f}")
    if stat > 1 or stat == 0.0:
        word += "s"
    return stat, word
