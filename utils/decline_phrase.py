

async def decline_phrase(n):
    forms_section = ['участке', 'участках', 'участке']
    forms_road = ['дороги', 'дорог', 'дорог']

    if 10 <= n % 100 <= 20:
        section_form = forms_section[1]
    else:
        last_digit = n % 10
        if last_digit == 1:
            section_form = forms_section[0]
        elif 2 <= last_digit <= 4:
            section_form = forms_section[2]
        else:
            section_form = forms_section[1]

    if 10 <= n % 100 <= 20:
        road_form = forms_road[2]
    else:
        last_digit = n % 10
        if last_digit == 1:
            road_form = forms_road[0]
        else:
            road_form = forms_road[2]

    return f"на {n} {section_form} {road_form}"