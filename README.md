# PokemonPdfToPTUImport
compiles pokedex and move pdfs to import data for PTU v2 character sheet on roll20

<h1>Info about pre-made import data</h1>
The folders JSONMoves and JSONPokemon contain all the moves and pokemon import data from latest run of script, the zip file contains both folders.
Data is parsed from "PTU_Core_Rulebook version 1.05" and "DataNinja's Unofficial gen 8 references PTU 1.05.5 Booklet version 2"

Use the data by finding the text file for the move/pokemon you want, copy content, paste content into import tab on roll20 PTU v2 char sheet and click import.

Pokemon data comes with all level up moves, skills, capabilities and base stats.
Moves and capabilities are appended, running import twice will therefore add moves and capabilities twice.
Stab is not accounted for, so will need to toggle this yourself. Five strike and double strike is also not marked.
The import data is meant to have contest effect and contest type flipped around, as the sheet reads them in the wrong order, so it will parse correctly this way.
The decorate move was not present in "DataNinja's Unofficial gen 8 references PTU 1.05.5 Booklet version 2" so i pulled data for that one from bulbapedia.

<h1>Info about the script</h1>
It is a python script, be sure to setup the requirements to run it.
Currently the script is setup to successfully parse "PTU_Core_Rulebook version 1.05" and "DataNinja's Unofficial gen 8 references PTU 1.05.5 Booklet version 2",
it is probably possible to run it against similar resources if they have the same layout.
Need to change paths for the pdfs if you want to run it yourself, if running against different pdfs, make sure the ifs that determine what pages are parsed is updated to match your pdfs.
I hardcoded in handling some typo's between the two pdfs, and also hardoced the move Decorate as it did not exist in "DataNinja's Unofficial gen 8 references PTU 1.05.5 Booklet version 2".
