input_file = open("input.csv")
data = dict()

lineNumber = 0

for line in input_file:
    lineNumber = lineNumber + 1
    parts = line.split('^')
    line_vcd = parts[0]
    line_actor = parts[1]
    line_text = parts[2].strip()
    line_text = line_text.rstrip('\n')
    scene = data.get(line_vcd)
    if scene is None:
        lineNumber = 0
        scene = dict()
    actor = scene.get(line_actor)
    if actor is None:
        actor = []
    actor.append([lineNumber, line_text])
    scene[line_actor] = actor
    data[line_vcd] = scene

for scene_name in data.keys():
    scene = data.get(scene_name)
    output_file = open(scene_name + ".vcd", "w")

    for actor_name in scene:
        actor = scene.get(actor_name)
        output_file.write("actor \"" + actor_name + "\"\n")
        output_file.write("{\n")
        output_file.write("  channel \"Placeholder\"\n")
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
        output_file.write("}\n")

    output_file.close()

print(data)

#