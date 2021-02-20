from io import StringIO
from bs4 import BeautifulSoup
from tika import parser
import re
import json

movePdf = []
data = parser.from_file('d:/dokumenter/pokemon/Homebrew_Rules_for_Abilities_and_Moves.pdf', xmlContent=True)
xhtml_data = BeautifulSoup(data['content'], "html.parser")
for page, content in enumerate(xhtml_data.find_all('div', attrs={'class': 'page'})):
    if 145 > page >= 50:
        _buffer = StringIO()
        _buffer.write(str(content))
        parsed_content = parser.from_buffer(_buffer.getvalue())
        _buffer.truncate()
        _buffer.close()
        movePdf.append({'id': 'page_'+str(page+1), 'content': parsed_content['content']})

movesDict = {}

translateKeyDict = {
    'Move': 'Name',
    'Class': 'DType',
    'Frequency': 'Freq',
    'Effect': 'Effects',
    'Athl': 'Athletics',
    'Acro': 'Acrobatics',
    'Percep': 'Perception',
    'Edu: Tech:': 'TechnologyEducation'
}

for page in movePdf:
    lineOnPage = page['content'].splitlines()
    moveTemplate = {
        'Move1': ''
    }
    moveDict = {}
    key = ''
    value = ''
    translatedKey = None

    for line in lineOnPage:
        split = line.split(':')
        if len(split) > 1:
            key = split[0].strip()
            value = split[1].strip()
            translatedKey = None
            if key in translateKeyDict:
                translatedKey = translateKeyDict[key]

            search = re.search('Damage Base ([0-9]+)', key)
            if search:
                translatedKey = 'DB'
                value = search.group(1)

            if translatedKey:
                moveDict[translatedKey] = value
            else:
                moveDict[key] = value

            if key == 'Contest Effect':
                movesDict[moveDict['Name']] = moveDict
                moveTemplate['Move1'] = moveDict
                jsonMove = json.dumps(moveTemplate)
                f = open("JSONMoves/" + moveDict['Name'].replace('’','') + ".txt", "w")
                f.write(jsonMove)
                f.close()
                moveDict = {}
        elif split[0].strip() != '':
            value = value + ' ' + split[0].strip()
            if translatedKey:
                moveDict[translatedKey] = value
            else:
                moveDict[key] = value

    moveDict = {
        "Name": "Decorate",
        "Type": "Fairy",
        "DType": "Status",
        "Range": "Can target others, unknown range",
        "Effects": "From bulbapedia: Decorate raises the target's Attack and Special Attack stat by two stages. Unlike most moves, it bypasses moves like Protect and Detect to affect the target, but is blocked by Crafty Shield."
    }
    movesDict[moveDict['Name']] = moveDict
    moveTemplate['Move1'] = moveDict
    jsonMove = json.dumps(moveTemplate)
    f = open("JSONMoves/" + moveDict['Name'].replace('’','') + ".txt", "w")
    f.write(jsonMove)
    f.close()
    moveDict = {}


def printPokemon(page):
    nameLines = re.search('(?s)Unofficial PTU 1.05.5 PokéDex. DataNinja’s Homebrew.(.*)Base Stats:', page['content']).group(1).splitlines()
    for line in nameLines:
        if (line.strip() != ""):
            name = line.strip().capitalize()
    if name.startswith('Rotom'):
        return

    stats = re.search('(?s)Base Stats:(.*)Basic Information', page['content']).group(1)
    hp = re.search('HP:([ 0-9]+)', stats).group(1).strip()
    attack = re.search('Attack:([ 0-9]+)', stats).group(1).strip()
    defense = re.search('Defense:([ 0-9]+)', stats).group(1).strip()
    sAttack = re.search('Special Attack:([ 0-9]+)', stats).group(1).strip()
    sDefense = re.search('Special Defense:([ 0-9]+)', stats).group(1).strip()
    speed = re.search('Speed:([ 0-9]+)', stats).group(1).strip()

    pokemonDict = {'species': name,'base_HP': hp, 'base_ATK': attack, 'base_DEF': defense, 'base_SPATK': sAttack, 'base_SPDEF': sDefense, 'base_SPEED': speed}

    pokeTypes = re.search('Type: ([A-Za-z/ ]+)', page['content']).group(1).replace('\n', '').split('/')
    pokemonDict['type1'] = pokeTypes[0].strip()
    if len(pokeTypes) > 1:
        pokemonDict['type2'] = pokeTypes[1].strip()

    capabilities = re.search('(?s)Capability List(.*)Skill List', page['content']).group(1)
    capabilities = re.sub(r'\([^()]+\)', lambda x: x.group().replace(',', ''), capabilities).replace('\n', '').split(',')
    capabilitiesDict = {}

    for cap in capabilities:
        reg = re.search('([A-Za-z ()]+)([0-9/]+)*', cap)
        capName = reg.group(1).strip()
        capNumber = reg.group(2)
        if capName == 'Jump':
            capNumber = capNumber.split('/')
            capabilitiesDict['HJ'] = capNumber[0]
            capabilitiesDict['LJ'] = capNumber[1]
        else:
            capabilitiesDict[capName] = capNumber or 'true'

    pokemonDict['Capabilities'] = capabilitiesDict

    skills = re.search('(?s)Skill List(.*)Level Up Move List', page['content']).group(1).replace('\n', '').split(',')
    for skill in skills:
        reg = re.search('([A-Za-z:]+) ([0-9])d6\+*([0-9]*).*', skill)
        if not reg:
            break
        skillName = reg.group(1).strip()
        skillRank = reg.group(2)
        skillBonus = reg.group(3)

        if (skillName in translateKeyDict):
            skillName = translateKeyDict[skillName]
        pokemonDict[skillName] = skillRank
        if skillBonus:
            pokemonDict[skillName + '_bonus'] = skillBonus

    moveList = re.search('(?s)Level Up Move List(.*)TM Move List', page['content'])
    if not moveList:
        moveList = re.search('(?s)Level Up Move List(.*)Tutor Move List', page['content'])
    if not moveList:
        moveList = re.search('(?s)Level Up Move List(.*)', page['content'])
    moveList = moveList.group(1).splitlines()
    moveListArray = []
    for move in moveList:
        m = re.search('([0-9]+|[Evo]+) (.*) -', move)
        if m:
            moveListArray.append(m.group(2))

    for index, move in enumerate(moveListArray):
        if move == 'Facade':
            pokemonDict['Move' + str(index + 1)] = movesDict['Façade']
        elif move == 'Muddy Watter':
            pokemonDict['Move' + str(index + 1)] = movesDict['Muddy Water']
        elif move == 'Bubblebeam':
            pokemonDict['Move' + str(index + 1)] = movesDict['Bubble Beam']
        elif move == 'Vicegrip':
            pokemonDict['Move' + str(index + 1)] = movesDict['Vice Grip']
        elif move == 'Hi Jump Kick':
            pokemonDict['Move' + str(index + 1)] = movesDict['High Jump Kick']
        elif move == 'U-turn':
            pokemonDict['Move' + str(index + 1)] = movesDict['U-Turn']
        elif move == 'Double-Hit':
            pokemonDict['Move' + str(index + 1)] = movesDict['Double Hit']
        elif move == 'Spatial Rend':
            pokemonDict['Move' + str(index + 1)] = movesDict['Spacial Rend']
        elif move == 'Judgment':
            pokemonDict['Move' + str(index + 1)] = movesDict['Judgement']
        elif move == 'Double Edge':
            pokemonDict['Move' + str(index + 1)] = movesDict['Double-Edge']
        else:
            pokemonDict['Move' + str(index + 1)] = movesDict[move]

    jsonPokemon = json.dumps(pokemonDict)

    f = open("JSONPokemon/" + name.replace('’','') + ".txt", "w")
    f.write(jsonPokemon)
    f.close()

pokeDex = []
data = parser.from_file('d:/dokumenter/pokemon/Pokedex.pdf', xmlContent=True)
xhtml_data = BeautifulSoup(data['content'], "html.parser")
for page, content in enumerate(xhtml_data.find_all('div', attrs={'class': 'page'})):
    if 15 <= page < 864 or 864 < page:
        _buffer = StringIO()
        _buffer.write(str(content))
        parsed_content = parser.from_buffer(_buffer.getvalue())
        _buffer.truncate()
        _buffer.close()
        pokeDex.append({'id': 'page_'+str(page+1), 'content': parsed_content['content']})

for page in pokeDex:
    try:
        printPokemon(page)
    except Exception as e:
        print(repr(e))
        print(page)
        break