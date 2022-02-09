import math

def generatePatternPermutations():
  patterns = [[]]
  for i in range(5):
    newPatterns = []
    for pattern in patterns:
      newPatterns.append(pattern + [0]) 
      newPatterns.append(pattern + [1]) 
      newPatterns.append(pattern + [2]) 
    patterns = newPatterns
  return patterns

def calculateWordEntropy(word, searchSpace):
  entropy = 0
  for patternPerm in patternPerms:
    matchProbability = float(len(calculateMatches(word, searchSpace, patternPerm)))/float(len(searchSpace))
    entropy += (matchProbability * calculateInformation(matchProbability))
  return entropy

def calculateInformation(probablity):
  if not probablity:
    return 0.0
  return -math.log2(probablity)

def calculateMatches(word, searchSpace, pattern):
  possibleMatches = searchSpace[:]
  matches = []
  for possibleMatch in possibleMatches:
    if possibleMatch == word:
      continue
    matchBool = True
    lettersUsed = []
    for i, p in enumerate(pattern):
      if p==1: #Yellow. Letter in word, but not in position
        lettersUsed.append(word[i])
        if word[i] not in possibleMatch or word[i] == possibleMatch[i]:
          matchBool = False
          break
      elif p==2: #Green. Letter in current Position
        lettersUsed.append(word[i])
        if word[i] != possibleMatch[i]:
          matchBool = False
          break
    for i, p in enumerate(pattern):
      if word[i] in lettersUsed:
        continue
      if p == 0: #Grey. Letter not in Word.
        if word[i] in possibleMatch:
          matchBool = False
          break
    if matchBool:
      matches.append(possibleMatch)
  return matches

patternPerms = generatePatternPermutations()