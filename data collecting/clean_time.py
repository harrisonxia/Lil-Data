






import json

# with open('out.json', 'w', encoding='utf-8') as outfile:
#     with open('../results/popular_category_for_languages.json', 'r') as jf:
#         for line in jf:
#             # guid.append(json.loads(line))
#             print(line)
#             line = line.replace('\n', ',\n')
#             # json.dump(json.JSONDecoder().decode(line), outfile, indent=4, separators=(',', ': '))
#             outfile.write(line)


lines = [{'language': 'ar', 'genres': 'Shooter', 'viewers': 3751},
        {'language': 'bg', 'genres': 'MOBA', 'viewers': 4741},
        {'language': 'cs', 'genres': 'Shooter', 'viewers': 11048},
        {'language': 'da', 'genres': 'Shooter', 'viewers': 15877},
        {'language': 'de', 'genres': 'Shooter', 'viewers': 129234},
        {'language': 'el', 'genres': 'Shooter', 'viewers': 799},
        {'language': 'en', 'genres': 'Shooter', 'viewers': 1056070},
        {'language': 'en-gb', 'genres': 'Action', 'viewers': 47345},
        {'language': 'es', 'genres': 'Shooter', 'viewers': 108462},
        {'language': 'es-mx', 'genres': 'Flight Simulator', 'viewers': 7457},
        {'language': 'fi', 'genres': 'Pinball', 'viewers': 14334},
        {'language': 'fi', 'genres': 'Strategy', 'viewers': 14334},
        {'language': 'fr', 'genres': 'First-Person Shooter', 'viewers': 30403},
        {'language': 'hu', 'genres': 'MOBA', 'viewers': 58667},
        {'language': 'it', 'genres': 'Shooter', 'viewers': 4723},
        {'language': 'ja', 'genres': 'Music/Rhythm', 'viewers': 15485},
        {'language': 'ko', 'genres': 'Music/Rhythm', 'viewers': 19148},
        {'language': 'nl', 'genres': 'Music/Rhythm', 'viewers': 3263},
        {'language': 'no', 'genres': 'First-Person Shooter', 'viewers': 5061},
        {'language': 'pl', 'genres': 'Simulation', 'viewers': 39927},
        {'language': 'pt', 'genres': 'MOBA', 'viewers': 5372},
        {'language': 'pt-br', 'genres': 'MOBA', 'viewers': 41606},
        {'language': 'ru', 'genres': 'Music/Rhythm', 'viewers': 29175},
        {'language': 'sk', 'genres': 'Simulation', 'viewers': 11508},
        {'language': 'sv', 'genres': 'Shooter', 'viewers': 27292},
        {'language': 'th', 'genres': 'MOBA', 'viewers': 3042},
        {'language': 'tr', 'genres': 'MOBA', 'viewers': 173752},
        {'language': 'vi', 'genres': 'Music/Rhythm', 'viewers': 60},
        {'language': 'zh-cn', 'genres': 'Music/Rhythm', 'viewers': 332},
        {'language': 'zh-tw', 'genres': 'Action-Adventure', 'viewers': 115295},
    ]

lines = sorted(lines, key=lambda k: k['viewers'], reverse=False)
print(lines)