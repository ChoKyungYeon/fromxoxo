import random

def theme_context_processor(request):
    values = []
    for i in range(20):
        x_position = random.randint(5 + 18 * (i % 5), 23 + 18 * (i % 5))
        cycle = i // 5 + 1
        y_ranges = [(4, 27), (27, 50),(50, 73), (73, 96)]
        y_position = random.randint(*y_ranges[cycle - 1])
        color = random.choice(['#feebb4', '#fef2cd', '#fff8e6', '#ffffff'])
        size = f'{random.choice([0.8, 0.9, 1, 1.1])}rem'
        rotation = f'rotate({random.randint(1, 180)}deg)'
        values.append([f'{x_position}%', f'{y_position}%', color, size, rotation])

    return {
        'decoration_icon_info': values,
        'theme': 'christmas',
    }