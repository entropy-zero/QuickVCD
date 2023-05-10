# 
# QuickRR.py
# Modification of QuickVCD.py fitted to write response scripts
# 

input_file = open("input_responses.tsv")

headerData = dict()
ruleData = dict()
criterionData = dict()
enumData = dict()

ModeHeader = "Header"
ModeResponse = "Response"
ModeCriterion = "Criterion"
ModeEnumeration = "Enumeration"

lineNumber = 0

# Script Information
Mode = ModeHeader
DividerNumber = 0

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
Column_GroupParams = 9

Column_Criterion = 0
Column_CriterionKey = 2
Column_CriterionValue = 3
Column_CriterionParams = 4
Column_CriterionNotes = 5

Column_Enum = 0
Column_EnumKey = 2
Column_EnumValue = 3
Column_EnumNotes = 4

# Actor Criteria
ActorCriteria = dict()
ActorCriteria["Bad Cop"] = "IsBadCop"
ActorCriteria["Clone Cop"] = "IsCloneCop"
ActorCriteria["Will-E"] = "IsWilson"

# Concept Criteria
ConceptCriteria = dict()
ConceptCriteria["TLK_TIPPED"] = "ConceptWilsonTipped"
ConceptCriteria["TLK_FIDGET"] = "ConceptWilsonFidget"
ConceptCriteria["TLK_FOUNDPLAYER"] = "ConceptFoundPlayer"
ConceptCriteria["TLK_REMIND_PLAYER"] = "ConceptRemindPlayer"
ConceptCriteria["TLK_APC_LOW_CLEARANCE"] = "ConceptAPCLowClearance"
ConceptCriteria["TLK_APC_EJECTED"] = "ConceptAPCEjected"
ConceptCriteria["TLK_GOODBYE"] = "ConceptWilsonGoodbye"
ConceptCriteria["TLK_BEAST_DANGER"] = "ConceptWilsonBeastDanger"
ConceptCriteria["TLK_BOSS_FIGHT"] = "ConceptWilsonBossFight"
ConceptCriteria["TLK_WITNESS_EAT"] = "ConceptWitnessEat"
ConceptCriteria["TLK_PLDEAD"] = "ConceptPlayerDead"
ConceptCriteria["TLK_PLHURT"] = "ConceptTalkPlayerHurt"
ConceptCriteria["TLK_PLRELOAD"] = "ConceptPlayerReload"
ConceptCriteria["TLK_WOUND"] = "ConceptTalkWound"
ConceptCriteria["TLK_WATCHOUT"] = "ConceptTalkWatchOut"
ConceptCriteria["TLK_ALLY_IN_BARNACLE"] = "ConceptAllyInBarnacle"
ConceptCriteria["TLK_DANGER"] = "ConceptTalkDanger"
ConceptCriteria["TLK_STARTCOMBAT"] = "ConceptStartCombat"
ConceptCriteria["TLK_ENEMY_DEAD"] = "ConceptEnemyDead"
ConceptCriteria["TLK_USE"] = "ConceptTalkUse"
ConceptCriteria["TLK_CONCEPT_ANSWER"] = "ConceptTalkConceptAnswer"
ConceptCriteria["TLK_CONCEPT_ANSWER_BOUNCE"] = "ConceptAnswerBounce"
ConceptCriteria["TLK_STOPFOLLOW"] = "ConceptTalkStopFollow"
ConceptCriteria["TLK_REMARK"] = "ConceptTalkRemark"

# Shared Lines
Line_Response = ""
Line_Actor = ""
Line_Concept = ""
Line_Criteria = ""
Line_RuleParams = ""
Line_GroupParams = ""

Line_Enum = ""

for line in input_file:
    parts = line.split('\t')
    
    IsHeader = False
    if parts[Column_Response] == ModeResponse or parts[Column_Response] == ModeCriterion or parts[Column_Response] == ModeEnumeration:
        IsHeader = True
        Mode = parts[Column_Response]
    
    # Some rows aren't responses!
    # 1. Responses called "Response" are headers describing the columns and not actual responses
    # 2. Rows with blank line text AND blank entries are considered to be non-responses
    if IsHeader or (parts[Column_LineText] == "" and parts[Column_Entry] == ""):
    
        if parts[Column_Response].strip() != "":
            # Assume irrelevant rows with the Response column are appropriate break points
            Divider = "//========================="
            if not IsHeader:
                Divider += " " + parts[Column_Response] + " "
            Divider += "=========================\n"
            
            if Mode == ModeHeader:
                headerData["divider_" + str(DividerNumber)] = Divider
            elif Mode == ModeResponse:
                Divider += "\n"
                ruleData["divider_" + str(DividerNumber)] = Divider
            elif Mode == ModeCriterion:
                criterionData["divider_" + str(DividerNumber)] = Divider
            elif Mode == ModeEnumeration:
                enumData["divider_" + str(DividerNumber)] = Divider
            
            DividerNumber += 1
            
        continue
    
    lineNumber = lineNumber + 1
        
    if Mode == ModeResponse:
    
        # If this is a new response (i.e. not one carried over from a previous row), refresh our values
        # (Retaining this data between similar rows is important for merged cells!!!)
        if parts[Column_Response] != "":
            Line_Response = parts[Column_Response]
            Line_Actor = parts[Column_Actor]
            Line_Concept = parts[Column_Concept]
            Line_Criteria = parts[Column_Criteria]
            Line_RuleParams = parts[Column_RuleParams]
            Line_GroupParams = parts[Column_GroupParams]
            
        Line_LineText = parts[Column_LineText]
        Line_LineNotes = parts[Column_LineNotes]
        Line_Entry = parts[Column_Entry]
        Line_ResponseParams = parts[Column_ResponseParams]
        
        # Check if the response exists already
        rule = ruleData.get(Line_Response)
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
            ruleParams = [Line_RuleParams, Line_GroupParams]
            
        # Check for this particular response entry
        response = rule.get(lineNumber)
        if response is None:
            response = [Line_Entry, Line_ResponseParams, Line_LineText, Line_LineNotes]
        
        rule["_criteria"] = criteria
        rule["_ruleparams"] = ruleParams
        rule[lineNumber] = response
        ruleData[Line_Response] = rule
        
    elif Mode == ModeCriterion:
    
        Line_Criterion = parts[Column_Criterion]
        Line_CriterionKey = parts[Column_CriterionKey]
        Line_CriterionValue = parts[Column_CriterionValue]
        Line_CriterionParams = parts[Column_CriterionParams]
        Line_CriterionNotes = parts[Column_CriterionNotes]
        
        # Check if the criterion exists already
        criterion = ruleData.get(Line_Criterion)
        if criterion is None:
            lineNumber = 0
            criterion = [Line_CriterionKey, Line_CriterionValue, Line_CriterionParams, Line_CriterionNotes]
        
        criterionData[Line_Criterion] = criterion
        
    elif Mode == ModeEnumeration:
    
        # If this is a blank enumeration, use the one from the previous row
        # (This is important for merged cells!!!)
        if parts[Column_Enum] != "":
            Line_Enum = parts[Column_Enum]
        
        Line_EnumKey = parts[Column_EnumKey]
        Line_EnumValue = parts[Column_EnumValue]
        Line_EnumNotes = parts[Column_EnumNotes]
        
        # Check if the enumeration exists already
        enum = enumData.get(Line_Enum)
        if enum is None:
            lineNumber = 0
            enum = []
            
        enum.append([Line_EnumKey, Line_EnumValue, Line_EnumNotes])
        
        enumData[Line_Enum] = enum

# Export responses
responses_file = open("output_responses.txt", "w")

responses_file.write("//=============================================\n")
responses_file.write("// AUTO-GENERATED RESPONSES\n")
responses_file.write("//=============================================\n\n")

# 
# HEADER DIVIDERS
# 
for Header_Name in headerData.keys():
    # If it's a divider, divide
    if "divider_" in Header_Name:
        responses_file.write(headerData.get(Header_Name))
        continue

# 
# ENUMERATION DECLARATIONS
# 
for Enum_Name in enumData.keys():
    # If it's a divider, divide
    if "divider_" in Enum_Name:
        responses_file.write(enumData.get(Enum_Name))
        continue

    enum = enumData.get(Enum_Name)
    responses_file.write("enumeration \"" + Enum_Name + "\"\n")
    responses_file.write("{\n")
    
    for kv in enum:
        Enum_Key = kv[0]
        Enum_Value = kv[1]
        Enum_Notes = kv[2]
        
        responses_file.write("\t\"" + Enum_Key + "\"\t\t\"" + Enum_Value + "\"")
        if Enum_Notes != "":
            responses_file.write(" // " + Enum_Notes)
        responses_file.write("\n")
        
    responses_file.write("}\n\n")

# 
# CRITERIA DECLARATIONS
# 
for Criterion_Name in criterionData.keys():
    # If it's a divider, divide
    if "divider_" in Criterion_Name:
        responses_file.write(criterionData.get(Criterion_Name))
        continue

    criterion = criterionData.get(Criterion_Name)
    
    Criterion_Key = criterion[0]
    Criterion_Value = criterion[1]
    Criterion_Params = criterion[2]
    Criterion_Notes = criterion[3]
                
    responses_file.write("criterion \"" + Criterion_Name + "\" \"" + Criterion_Key + "\" \"" + Criterion_Value + "\" " + Criterion_Params)
    if Criterion_Notes != "":
        responses_file.write(" // " + Criterion_Notes)
    responses_file.write("\n")
    
    #responses_file.write("//--------------------------------\n\n")

# 
# RESPONSE DECLARATIONS
# 
for Rule_Name in ruleData.keys():
    # If it's a divider, divide
    if "divider_" in Rule_Name:
        responses_file.write(ruleData.get(Rule_Name))
        continue

    rule = ruleData.get(Rule_Name)
    
    # Declare text that will eventually be in the response
    Text_Criteria = ""
    Text_ResponseGroup = ""
    Text_ResponseGroupParams = ""
    Text_RuleParams = ""
    
    # Some responses are meant to be shared and don't have actual rules accompanying them
    ResponseOnly = False
    
    # Parse criteria first
    criteria = rule.get("_criteria")
    if criteria is not None:
        Line_Actor = ActorCriteria.get(criteria[0])
        if Line_Actor is None:
            Line_Actor = "IsError"
            
        if criteria[1] is not None and criteria[1] != "<N/A>":
            Line_Concept = ConceptCriteria.get(criteria[1])
            if Line_Concept is None:
                # Make it a misc. criterion
                Text_RuleParams += "Concept \"" + criteria[1] + "\" required\n"
                Text_Criteria = Line_Actor + " " + criteria[2]
            else:
                Text_Criteria = Line_Actor + " " + Line_Concept + " " + criteria[2]
        else:
            # No concept = Not a rule
            ResponseOnly = True
        
        # Don't need criteria anymore; remove before iterating
        del rule["_criteria"]
    else:
        # This should not happen
        Text_Criteria = "CRITERIA IS MISSING"
        
     # Parse rule params
    ruleParams = rule.get("_ruleparams")
    if ruleParams is not None:
    
        Text_RuleParams += ruleParams[0]
        
        groupParams = ruleParams[1].split()
        for param in groupParams:
            Text_ResponseGroupParams += "\t" + param + "\n"
        
        # Don't need rule params anymore; remove before iterating
        del rule["_ruleparams"]
    
    for responseLine in rule:
        response = rule.get(responseLine)
        Response_Entry = response[0]
        Response_ResponseParams = response[1]
        Response_LineText = response[2]
        Response_LineNotes = response[3]
        
        Text_ResponseGroup += "\t"
        
        if Response_LineText != "" and Response_LineText[0] == '$':
            # Response is commented out
            Response_LineText = Response_LineText[1:]
            Text_ResponseGroup += "//"
        
        if Response_Entry == "":
            # If the entry is empty, assume placeholder text
            Text_ResponseGroup += "print \"" + Response_LineText + "\" " + Response_ResponseParams
            if Response_LineNotes != "":
                Text_ResponseGroup += " // " + Response_LineNotes
            Text_ResponseGroup += "\n"
        else:
            # Deduce entry type
            Response_Type = ""
            if ".vcd" in Response_Entry:
                Response_Type = "scene"
            elif "response " in Response_Entry:
                Response_Type = "response"
                Response_Entry = Response_Entry[9:].replace('\"', '')
            else:
                # Assume speak for now
                Response_Type = "speak"
            
            Text_ResponseGroup += Response_Type + " \"" + Response_Entry + "\" " + Response_ResponseParams + " //"
            if Response_LineText != "":
                Text_ResponseGroup += " \"" + Response_LineText + "\""
            if Response_LineNotes != "":
                Text_ResponseGroup += " -- " + Response_LineNotes
            Text_ResponseGroup += "\n"
                
    responses_file.write("response \"" + Rule_Name + "\"\n")
    responses_file.write("{\n")
    if Text_ResponseGroupParams != "":
        responses_file.write(Text_ResponseGroupParams)
    responses_file.write(Text_ResponseGroup)
    responses_file.write("}\n\n")
    
    if not ResponseOnly:
        responses_file.write("rule \"" + Rule_Name + "\"\n")
        responses_file.write("{\n")
        responses_file.write("\tcriteria\t\t" + Text_Criteria + "\n")
        if Text_RuleParams != "":
            responses_file.write("\t" + Text_RuleParams + "\n")
        responses_file.write("\tresponse\t\t" + Rule_Name + "\n")
        responses_file.write("}\n\n")
    
    #responses_file.write("//--------------------------------\n\n")

responses_file.close()

print(criterionData)
print(ruleData)