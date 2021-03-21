# 
# QuickRR.py
# Modification of QuickVCD.py fitted to write response scripts
# 

input_file = open("input_responses.csv")
data = dict()

lineNumber = 0

# Columns
Column_Response = 0
Column_Actor = 1
Column_LineText = 2
Column_LineNotes = 3
Column_Concept = 4
Column_Criteria = 5
Column_Entry = 6
Column_ResponseParams = 7
Column_RuleParams = 8

# Actor Criteria
ActorCriteria = dict()
ActorCriteria["Bad Cop"] = "IsBadCop"
ActorCriteria["Clone Cop"] = "IsCloneCop"
ActorCriteria["Will-E"] = "IsWilson"

# Concept Criteria
ConceptCriteria = dict()
ConceptCriteria["TLK_TIPPED"] = "ConceptTalkTipped"

# Response Group/Rule Lines
Line_Response = ""
Line_Actor = ""
Line_Concept = ""
Line_Criteria = ""
Line_RuleParams = ""

for line in input_file:
    parts = line.split('^')
    
    # Skip irrelevant rows!
    # 1. Responses called "Response" are headers describing the columns and not actual responses
    # 2. Rows with blank line text are considered to be non-responses
    if parts[Column_Response] == 'Response' or parts[Column_LineText] == "":
        continue
        
    # If the first character is a $, it's a cut line
    if parts[Column_LineText][0] == '$':
        continue
    
    lineNumber = lineNumber + 1
        
    # If this is a new response (i.e. not one carried over from a previous row), refresh our values
	# (Retaining this data between similar rows is important for merged cells!!!)
    if parts[Column_Response] != "":
        Line_Response = parts[Column_Response]
        Line_Actor = parts[Column_Actor]
        Line_Concept = parts[Column_Concept]
        Line_Criteria = parts[Column_Criteria]
        Line_RuleParams = parts[Column_RuleParams]
        
    Line_LineText = parts[Column_LineText]
    Line_LineNotes = parts[Column_LineNotes]
    Line_Entry = parts[Column_Entry]
    Line_ResponseParams = parts[Column_ResponseParams]
    
    # Check if the response exists already
    rule = data.get(Line_Response)
    if rule is None:
        lineNumber = 0
        rule = dict()
        
    # Append criteria if it doesn't have any
    criteria = rule.get("_criteria")
    if criteria is None:
        criteria = [Line_Actor, Line_Concept, Line_Criteria]
        
    # Append rule params if it doesn't have any
    ruleParams = rule.get("_ruleparams")
    if ruleParams is None:
        ruleParams = Line_RuleParams
        
    # Check for this particular response entry
    response = rule.get(lineNumber)
    if response is None:
        response = [Line_Entry, Line_ResponseParams, Line_LineText]
    
    rule["_criteria"] = criteria
    rule["_ruleparams"] = ruleParams
    rule[lineNumber] = response
    data[Line_Response] = rule

# Export responses
responses_file = open("output_responses.txt", "w")

responses_file.write("//=============================================\n")
responses_file.write("// AUTO-GENERATED RESPONSES\n")
responses_file.write("//=============================================\n\n")

for Rule_Name in data.keys():
    rule = data.get(Rule_Name)
    
    # Declare text that will eventually be in the response
    Text_Criteria = ""
    Text_ResponseGroup = ""
    Text_ResponseGroupParams = ""
    Text_RuleParams = ""
    
    # Parse criteria first
    criteria = rule.get("_criteria")
    if criteria is not None:
        Line_Actor = ActorCriteria.get(criteria[0])
        if Line_Actor is None:
            Line_Actor = "IsError"
            
        Line_Concept = ConceptCriteria.get(criteria[1])
        if Line_Concept is None:
            # Make it a misc. criterion
            Text_RuleParams += "Concept \"" + criteria[1] + "\" required\n"
            Text_Criteria = Line_Actor + " " + criteria[2]
        else:
            Text_Criteria = Line_Actor + " " + Line_Concept + " " + criteria[2]
        
        # Don't need criteria anymore; remove before iterating
        del rule["_criteria"]
    else:
        # This should not happen
        Text_Criteria = "CRITERIA IS MISSING"
        
     # Parse rule params
    ruleParams = rule.get("_ruleparams")
    if ruleParams is not None:
    
        # HACKHACK: Extract response group params and replace inconsistent spacing
        if "norepeat" in ruleParams:
            ruleParams = ruleParams.replace('norepeat','')
            Text_ResponseGroupParams += "\tnorepeat\n"
        if "sequential" in ruleParams:
            ruleParams = ruleParams.replace('sequential','')
            Text_ResponseGroupParams += "\tsequential\n"
        if "permitrepeats" in ruleParams:
            ruleParams = ruleParams.replace('permitrepeats','')
            Text_ResponseGroupParams += "\tpermitrepeats\n"
    
        Text_RuleParams += ruleParams.strip().replace('  ','')
        
        # Don't need rule params anymore; remove before iterating
        del rule["_ruleparams"]
    
    for responseLine in rule:
        response = rule.get(responseLine)
        Response_Entry = response[0]
        Response_ResponseParams = response[1]
        Response_LineText = response[2]
        
        # If the entry is empty, assume placeholder text
        if Response_Entry == "":
            Text_ResponseGroup += "\tprint \"" + Response_LineText + "\" " + Response_ResponseParams + "\n"
        else:
            # Deduce entry type
            Response_Type = ""
            if ".vcd" in Response_Entry:
                Response_Type = "scene"
            else:
                # Assume speak for now
                Response_Type = "speak"
            
            Text_ResponseGroup += "\t" + Response_Type + " \"" + Response_Entry + "\" " + Response_ResponseParams + " // " + Response_LineText + "\n"
                
    responses_file.write("response \"" + Rule_Name + "\"\n")
    responses_file.write("{\n")
    if Text_ResponseGroupParams != "":
        responses_file.write(Text_ResponseGroupParams)
    responses_file.write(Text_ResponseGroup)
    responses_file.write("}\n\n")
    
    responses_file.write("rule \"" + Rule_Name + "\"\n")
    responses_file.write("{\n")
    responses_file.write("\tcriteria\t\t" + Text_Criteria + "\n")
    if Text_RuleParams != "":
        responses_file.write("\t" + Text_RuleParams + "\n")
    responses_file.write("\tresponse\t\t" + Rule_Name + "\n")
    responses_file.write("}\n\n")
    
    responses_file.write("//--------------------------------\n\n")

responses_file.close()

print(data)