# Very primitive python script to generate soundscript entries

input_file = open("input.csv")
data = dict()

lineNumber = 0
locationColumn = 0
vcdColumn = 1 # Need to separate this out for all line sheets!
wavPathColumn = -1
soundscriptColumn = -1
actorColumn = 2
lineTextColumn = 3

actor_lookup = dict()
actor_lookup['!player'] = 'badcop'
actor_lookup['!wilson'] = 'wilson'

# This is mega lame, but let's just hard code caption colors for now
closeCaptionColors = dict()
closeCaptionColors["Clone Cop"] = "<clr:253,165,2><I>"
closeCaptionColors["Bad Cop"] = "<clr:255,51,0>"
closeCaptionColors["Advisor"] = "<clr:136,180,185>"
closeCaptionColors["Will-E"] = "<clr:66,255,199>"
closeCaptionColors["Cop 1"] = "<clr:0,255,255>"
closeCaptionColors["Cop 2"] = "<clr:255,255,0>"
closeCaptionColors["Cop 3"] = "<clr:0,0,255>"
closeCaptionColors["!player"] = "<clr:255,51,0>"
closeCaptionColors["!wilson"] = "<clr:66,255,199>"

for line in input_file:
    parts = line.split('^')
    
    # Skip header rows!
    if parts[locationColumn] == 'Location':
        continue
    
    lineNumber = lineNumber + 1
        
    line_vcd = parts[vcdColumn]
    line_actor = parts[actorColumn]
    line_text = parts[lineTextColumn].strip()
    line_text = line_text.rstrip('\n')
    line_location = parts[locationColumn]
    wavPath = parts[wavPathColumn]    
    scene = data.get(line_vcd)
    if scene is None:
        lineNumber = 0
        scene = dict()
    actor = scene.get(line_actor)
    if actor is None:
        actor = []

    text_words = line_text.split(' ')
    firstwords = ''.join(text_words[0:6]).lower().replace('\'','').replace('.','').replace(',','').replace('?','')

    if soundscriptColumn != -1:
        soundscriptName = parts[soundscriptColumn]
    else:
        soundscriptName = actor_lookup[line_actor]  + "_"  + line_location + "." + firstwords

    if wavPathColumn != -1:
        wavPath = parts[wavPathColumn] 
    else:
        wavPath = 'sound/vo/npc/' + actor_lookup[line_actor] + '/' + line_location + "_" + firstwords + '.wav'
        
    actor.append([lineNumber, line_text, soundscriptName, wavPath])
    scene[line_actor] = actor
    data[line_vcd] = scene

# Export soundscripts
soundscript_file = open("output_soundscripts.txt", "w")
captions_file = open("output_captions.txt", "w")

for scene_name in data.keys():
    scene = data.get(scene_name)
    
    for actor_name in scene:
        actor = scene.get(actor_name)
        for line in actor:
            line_number = line[0]
            line_text = line[1]
            soundscriptName = line[2]
            wavPath = line[3]
            captionColor = closeCaptionColors.get(actor_name)
            if captionColor is None:
                captionColor = "<clr:255,255,255>"
            soundscript_file.write("\"" + soundscriptName + "\"\n")
            soundscript_file.write("{\n")
            soundscript_file.write("  \"channel\"\t\t\"CHAN_VOICE\"\n")
            soundscript_file.write("  \"volume\"\t\t\"0.650000\"\n")
            soundscript_file.write("  \"pitch\"\t\t\"PITCH_NORM\"\n")
            soundscript_file.write("  \"soundlevel\"\t\t\"SNDLVL_TALKING\"\n")
            soundscript_file.write("  \"wave\"\t\t\"" + wavPath + "\"\n")
            soundscript_file.write("}\n")
            captions_file.write("  \"" + soundscriptName + "\"  \"" + captionColor + line_text + "\"\n")

soundscript_file.close()
captions_file.close()

# Export placeholder VCDs
for scene_name in data.keys():
    scene = data.get(scene_name)
    output_file = open(scene_name + ".vcd", "w")

    for actor_name in scene:
        actor = scene.get(actor_name)
        output_file.write("actor \"" + actor_name + "\"\n")
        output_file.write("{\n")
        output_file.write("  channel \"placeholder\"\n")
        output_file.write("  {\n")
        for line in actor:
            line_number = line[0]
            line_text = line[1]
            output_file.write("    event generic \"AI_GAMETEXT\"\n")
            output_file.write("    {\n")
            output_file.write("      time " + str(line_number * 3) + " " + str((line_number + 1) * 3) + "\n")
            output_file.write("      param \"AI_GAMETEXT\"\n")
            output_file.write("      param2 \"" + line_text + "\"\n")
            output_file.write("    }\n")
        output_file.write("  }\n")
        output_file.write("  channel \"audio\"\n")
        output_file.write("  {\n")
        for line in actor:
            line_number = line[0]
            line_text = line[1]
            output_file.write("    event speak \"" + soundscriptName + "\"\n")
            output_file.write("    {\n")
            output_file.write("      time " + str(line_number * 3) + " " + str((line_number + 1) * 3) + "\n")
            output_file.write("      param \"" + soundscriptName + "\"\n")
            output_file.write("      fixedlength\n")
            output_file.write("      cctype \"cc_master\"\n")
            output_file.write("      cctoken \"\"\n")
            output_file.write("    }\n")
        output_file.write("  }\n")
        output_file.write("}\n")

    output_file.close()

print(data)