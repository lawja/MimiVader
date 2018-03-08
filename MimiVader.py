from subprocess import Popen, PIPE
import sys
import re
import uuid

# values that are often substring and keywords throughout the ps file
flagged_values = ['true', 'false', 'i', 'j', 'success', '', None, 'null', 'e',
                  'memcpyaddr', 'memcpydelegate', 'memcpy', 'memsetdelegate',
                  'sum', 'pwd', 'val', 'value', 'info', 'output', 'name',
                  'dll', 'errorcode', 'memset', 'memsetaddr']
# functions that are often substring and keywords throughout the ps file
flagged_functions = ['woofwoof', 'main', 'reference', 'to',
                     'with', 'address']

# a list of nouns that rename variables and functions
# courtesy of https://gist.github.com/bergantine/2390284
nouns = ['people', 'history', 'way', 'art', 'world', 'information', 'map', 'two', 'family', 'government', 'health', 'system', 'computer', 'meat', 'year', 'thanks', 'music', 'person', 'reading', 'method', 'data', 'food', 'understanding', 'theory', 'law', 'bird', 'literature', 'problem', 'software', 'control', 'knowledge', 'power', 'ability', 'economics', 'love', 'internet', 'television', 'science', 'library', 'nature', 'fact', 'product', 'idea', 'temperature', 'investment', 'area', 'society', 'activity', 'story', 'industry', 'media', 'thing', 'oven', 'community', 'definition', 'safety', 'quality', 'development', 'language', 'management', 'player', 'variety', 'video', 'week', 'security', 'country', 'exam', 'movie', 'organization', 'equipment', 'physics', 'analysis', 'policy', 'series', 'thought', 'basis', 'boyfriend', 'direction', 'strategy', 'technology', 'army', 'camera', 'freedom', 'paper', 'environment', 'child', 'instance', 'month', 'truth', 'marketing', 'university', 'writing', 'article', 'department', 'difference', 'goal', 'news', 'audience', 'fishing', 'growth', 'income', 'marriage', 'user', 'combination', 'failure', 'meaning', 'medicine', 'philosophy', 'teacher', 'communication', 'night', 'chemistry', 'disease', 'disk', 'energy', 'nation', 'road', 'role', 'soup', 'advertising', 'location', 'success', 'addition', 'apartment', 'education', 'math', 'moment', 'painting', 'politics', 'attention', 'decision', 'event', 'property', 'shopping', 'student', 'wood', 'competition', 'distribution', 'entertainment', 'office', 'population', 'president', 'unit', 'category', 'cigarette', 'context', 'introduction', 'opportunity', 'performance', 'driver', 'flight', 'length', 'magazine', 'newspaper', 'relationship', 'teaching', 'cell', 'dealer', 'debate', 'finding', 'lake', 'member', 'message', 'phone', 'scene', 'appearance', 'association', 'concept', 'customer', 'death', 'discussion', 'housing', 'inflation', 'insurance', 'mood', 'woman', 'advice', 'blood', 'effort', 'expression', 'importance', 'opinion', 'payment', 'reality', 'responsibility', 'situation', 'skill', 'statement', 'wealth', 'application', 'city', 'county', 'depth', 'estate', 'foundation', 'grandmother', 'heart', 'perspective', 'photo', 'recipe', 'studio', 'topic', 'collection', 'depression', 'imagination', 'passion', 'percentage', 'resource', 'setting', 'ad', 'agency', 'college', 'connection', 'criticism', 'debt', 'description', 'memory', 'patience', 'secretary', 'solution', 'administration', 'aspect', 'attitude', 'director', 'personality', 'psychology', 'recommendation', 'response', 'selection', 'storage', 'version', 'alcohol', 'argument', 'complaint', 'contract', 'emphasis', 'highway', 'loss', 'membership', 'possession', 'preparation', 'steak', 'union', 'agreement', 'cancer', 'currency', 'employment', 'engineering', 'entry', 'interaction', 'limit', 'mixture', 'preference', 'region', 'republic', 'seat', 'tradition', 'virus', 'actor', 'classroom', 'delivery', 'device', 'difficulty', 'drama', 'election', 'engine', 'football', 'guidance', 'hotel', 'match', 'owner', 'priority', 'protection', 'suggestion', 'tension', 'variation', 'anxiety', 'atmosphere', 'awareness', 'bread', 'climate', 'comparison', 'confusion', 'construction', 'elevator', 'emotion', 'employee', 'employer', 'guest', 'height', 'leadership', 'mall', 'manager', 'operation', 'recording', 'respect', 'sample', 'transportation', 'boring', 'charity', 'cousin', 'disaster', 'editor', 'efficiency', 'excitement', 'extent', 'feedback', 'guitar', 'homework', 'leader', 'mom', 'outcome', 'permission', 'presentation', 'promotion', 'reflection', 'refrigerator', 'resolution', 'revenue', 'session', 'singer', 'tennis', 'basket', 'bonus', 'cabinet', 'childhood', 'church', 'clothes', 'coffee', 'dinner', 'drawing', 'hair', 'hearing', 'initiative', 'judgment', 'lab', 'measurement', 'mode', 'mud', 'orange']

noun_count = 0

# variables and functions that are found in the original file
variables = []
functions = []

def main(og_filename, new_filename):
    global variables

    # just incase there's a file collision
    temp_filename = str(uuid.uuid4()) + '.txt'

    with open(temp_filename, 'w') as temp:
        with open(og_filename, 'r') as og_file:
            temp.write(og_file.read())
        og_file.close()
    temp.close()

    # courtesy of https://www.blackhillsinfosec.com/bypass-anti-virus-run-mimikatz/
    commands = '''
    sed -i -e 's/Invoke-Mimikatz/Provoke-MiniDogz/g' {0};
    sed -i -e '/<#/,/#>/c\\' {0};
    sed -i -e 's/^[[:space:]]*#.*$//g' {0};
    sed -i -e 's/DumpCreds/TakeOutTheTrash/g' {0};
    sed -i -e 's/ArgumentPtr/NotTodayPal/g' {0};
    sed -i -e 's/CallDllMainSC1/ThisIsNotTheStringYouAreLookingFor/g' {0};
    sed -i -e "s/\-Win32Functions \$Win32Functions$/\-Win32Functions \$Win32Functions #\-/g" {0}
    '''.format(temp_filename)

    # execute the sed commands
    Popen(commands, stdout=PIPE, stderr=PIPE, shell=True).wait()
    # remove stream editor file
    Popen('rm {0}-e'.format(temp_filename), stdout=PIPE, stderr=PIPE,
          shell=True).wait()
    
    with open(temp_filename, 'r') as og_file:
        # output file
        with open(new_filename, 'w') as newFile:
            # iterate through the original file's lines to find all vars
            # and functions
            for line in og_file.readlines():
                findVars(line)
                findFunctions(line)
            og_file.close()

            with open(temp_filename, 'r') as og_file:
                contents = og_file.read()
                # replace all vars and functions with dummy names
                new_contents = replaceVars(contents)
                final_contents = replaceFunctions(new_contents)
            og_file.close()

            for line in final_contents.splitlines():
                # fill empty lines with UUID comments for "randomness"
                # protects against string and heuristic based engines

                # fight against warning recognition
                if(re.search("Write-Warning", line, re.IGNORECASE)):
                    newFile.write('#' + str(uuid.uuid4()) + '\n')
                # fight against throw statement recognition
                elif(re.search("Throw", line, re.IGNORECASE)):
                    newFile.write('Throw "' + str(uuid.uuid4()) + '"\n')
                elif(not(re.search('[A-Za-z0-9\{\}]', line))):
                    newFile.write(line + '#' + str(uuid.uuid4()) + '\n')
                else:
                    newFile.write(line + '\n')
        newFile.close()
        Popen('rm {0}'.format(temp_filename), stdout=PIPE, stderr=PIPE,
              shell=True).wait()

# finds all variables found within the passed string
def findVars(line):
    global variables
    global flagged_values

    # search for a string that begins with $ and contains and ends with 
    # alphanumeric chars
    found_var = re.search("\$[A-Za-z0-9]*", line)
    
    while(found_var):
        # get the actual matched value
        match = line[found_var.span()[0]:found_var.span()[1]].split('$')[1]

        # if it's not a special value
        if(not(match.lower() in flagged_values)):
            # if we haven't seen it before
            if(not(match in variables)):
                # add it to our variable list
                variables.append(match)

        # search through the rest of the line
        line = line[found_var.span()[1]:]
        # same as before
        found_var = re.search("\$[A-Za-z0-9]*", line)

# finds all powershell function declarations found within the passed string
def findFunctions(line):
    global functions
    global flagged_functions

    # search for function declaration syntax
    found_function = re.search("Function [A-Za-z0-9\-]*", line, re.IGNORECASE)
    
    while(found_function):
        # the matched string
        match = line[found_function.span()[0]:found_function.span()[1]].split(' ')[1]
        # if it's not a special case function
        if(not(match.lower() in flagged_functions)):
            # if we haven't seen this function before
            if(not(match in functions)):
                # add it to our seen function list
                functions.append(match)

        line = line[found_function.span()[1]:]
        found_function = re.search("Function [A-Za-z0-9\-]*", line, re.IGNORECASE)

#replace all variables with dummy names
# this protects against string recognition AVs
def replaceVars(contents):
    global noun_count
    global variables

    # iterate through all found vars and replace accordingly
    for var in variables:
        contents = re.sub(var, nouns[noun_count], contents)
        noun_count += 1
    return contents


# replace all functions with dummy names
# this protects against string recognition AVs and some heuristic engines
def replaceFunctions(contents):
    global noun_count
    global functions

    # iterate through all found functions and replace accordingly
    for function in functions:
        contents = re.sub(function, nouns[noun_count], contents)
        noun_count += 1
    return contents



if __name__ == "__main__":
    try:
        main(sys.argv[1], sys.argv[2])
    except IndexError:
        print("[!] Syntax:\npython noiseMaker.py <original_file> <new_file>")
    print("Logged to " + sys.argv[2])
