import wordsList
from entropyAnalysis import calculateWordEntropy, calculateInformation, calculateMatches

class WordleGame:

  def __init__(self):
    self.searchSpace = wordsList.words[:]
    self.informationRemaining = calculateInformation(1.0/float(len(self.searchSpace)))
    initialRecommendations = {}
    with open('initial.txt', 'rb') as file:
      for l in file:
        parameters = l.decode('utf-8').split(' ')
        initialRecommendations[parameters[0]] = float(parameters[1])
    self.suggestions = initialRecommendations
    self.writeSuggestions()
    for i in range(6):
      if len(self.suggestions) > 1: #More than 1 possible answer
        self.enterGuess(i+1)
      elif len(self.suggestions) == 1: #Only 1 answer
        print(f"Answer must be: {list(self.suggestions.keys())[0].replace('ä', 'a*').replace('ö', 'o*').replace('ü', 'u*')}")
        break
      else:
        print('Something went wrong!')
        break
    
  def enterGuess(self, i):
    print(f'Info Remaining: {self.informationRemaining} bits')
    print(f'{i}:')
    wordGuess = input('Guess: ').lower()
    patternInput = input('Pattern: ')
    patternReturned = [int(i) for i in patternInput]
    #Do new calculations
    newSearchSpace = calculateMatches(wordGuess, self.searchSpace, patternReturned)
    print(f'Expected Info: {self.suggestions[wordGuess]}')
    print(f'Actual Info: {calculateInformation(float(len(newSearchSpace))/float(len(self.searchSpace)))}')
    self.searchSpace = newSearchSpace
    self.informationRemaining = calculateInformation(1.0/float(len(self.searchSpace)))
    self.suggestions = {}
    for w in self.searchSpace:
      self.suggestions[w] = calculateWordEntropy(w, self.searchSpace)
    sortedSuggestions = [i for i in self.suggestions]
    def sortByEntropy(e):
      return self.suggestions[e]
    sortedSuggestions.sort(key=sortByEntropy, reverse=True)
    self.suggestions = {i: self.suggestions[i] for i in sortedSuggestions}
    self.writeSuggestions()
    print()

  def writeSuggestions(self):
    with open('suggestions.txt', 'wb') as f:
      for w in self.suggestions:
        f.write(f'{w} {self.suggestions[w]}\n'.encode('utf-8'))