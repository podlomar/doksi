import doksi_parser
import json

class Actions(object):
  def __init__(self):
    self.elmStack = []
    self.currentIndent = -1
    self.lastElement = [['doksi', None, None]]

  def content(self, input, start, end, elements):
    parent = self.elmStack[0]
    return parent

  def elements(self, input, start, end, elements):
    return elements
  
  def elementWithNL(self, input, start, end, elements):
    return elements[1]
  
  def element(self, input, start, end, elements):
    if isinstance(elements[1], doksi_parser.TreeNode):
      if isinstance(elements[3], doksi_parser.TreeNode):
        elm = None
      else:
        elm = elements[3]
    else:
      if isinstance(elements[3], doksi_parser.TreeNode):
        elm = [elements[1]]
      else:
        elm = [elements[1], elements[3]]
    
    indent = len(elements[0])
    if indent > self.currentIndent:
      self.elmStack.append(self.lastElement)
      self.indentStep = indent - self.currentIndent
      self.currentIndent = indent
    
    self.elmStack[-1].append(elm)
    self.lastElement = elm
    return elm

  def lineContent(self, input, start, end, elements):
    return elements[0] + ' ' + elements[1]

  def head(self, input, start, end, elements):
    return [elements[0], None, None]

  def tagName(self, input, start, end, element):
    return input[start:end]

  def words(self, input, start, end, elements):
    return ' '.join(elements)

  def wordWithWS(self, input, start, end, elements):
    return elements[1]

  def word(self, input, start, end, elements):
    return input[start:end]
  
  def ws(self, input, start, end, elements):
    return input[start:end]

def generateXML(element, indent):
  xml = ''
  
  if element == None:
    return xml
  
  if isinstance(element, str):
    xml += f'{indent}{element}\n'
    return xml
    
  xml += f'{indent}<{element[0][0]}>\n'

  for child in element[1:]:
    xml += generateXML(child, indent + '  ')

  xml += f'{indent}</{element[0][0]}>\n'
  return xml

def toHTML(document):
  html = (
    '<!DOCTYPE html>\n' + 
    '<html lang="en">\n' + 
    '<head>\n' + 
    '  <meta charset="UTF-8" />\n' + 
    '  <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n' + 
    '  <meta http-equiv="X-UA-Compatible" content="ie=edge" />\n' + 
    '</head>\n' + 
    '<body>\n'
  )

  for element in document[1:]:
    html += generateXML(element, '  ')

  html += (
    '</body>\n' + 
    '</html>\n'
  ) 

  return html

def toJSON(document):
  return json.dumps(document)

def parse(text):
  return doksi_parser.parse(text, actions=Actions()) 

def parseFile(file):
  text = file.read()
  return parse(text)

def doksiToHTML(file):
  return toHTML(parseFile(file))

def doksiToJSON(file):
  return toJSON(parseFile(file))
