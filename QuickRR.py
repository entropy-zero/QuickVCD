# 
# QuickRR.py
# Modification of QuickVCD.py fitted to write response scripts
# 

input_file = open("input_responses.csv")

headerData = dict()
ruleData = dict()
criterionData = dict()

lineNumber = 0

# Script Information
Mode = "Header"
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
Column_CriterionKey = 1
Column_CriterionValue = 2
Column_CriterionParams = 3

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

# Response Group/Rule Lines
Line_Response = ""
Line_Actor = ""
Line_Concept = ""
Line_Criteria = ""
Line_RuleParams = ""
Line_GroupParams = ""

for line in input_file:
    parts = line.split('^')
    
    IsHeader = False
    if parts[Column_Response] == 'Response' or parts[Column_Response] == 'Criterion':
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
            Divider += "=========================\n\n"
            
            if Mode == "Header":
                headerData["divider_" + str(DividerNumber)] = Divider
            elif Mode == "Response":
                ruleData["divider_" + str(DividerNumber)] = Divider
            elif Mode == "Criterion":
                criterionData["divider_" + str(DividerNumber)] = Divider
            
            DividerNumber += 1
            
        continue
    
    lineNumber = lineNumber + 1
        
    if Mode == "Response":
    
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
        
    elif Mode == "Criterion":
    
        Line_Criterion = parts[Column_Criterion]
        Line_CriterionKey = parts[Column_CriterionKey]
        Line_CriterionValue = parts[Column_CriterionValue]
        Line_CriterionParams = parts[Column_CriterionParams]
        
        # Check if the criterion exists already
        criterion = ruleData.get(Line_Criterion)
        if criterion is None:
            lineNumber = 0
            criterion = [Line_CriterionKey, Line_CriterionValue, Line_CriterionParams]
        
        criterionData[Line_Criterion] = criterion

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
                
    responses_file.write("criterion \"" + Criterion_Name + "\" \"" + Criterion_Key + "\" \"" + Criterion_Value + "\" " + Criterion_Params + "\n")
    
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