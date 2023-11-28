import csv
import sys

sections = sys.argv

romSectionIndex = -1
romSectionEnd = -1
ramSectionIndex = -1
ramSectionEnd = -1
identifiersIndex = -1
identifiersEnd = -1
try:
  romSectionIndex = (sections.index("--rom"))
except ValueError:
  pass

try:
  ramSectionIndex = (sections.index("--ram"))
except ValueError:
  pass

try:
  identifiersIndex = (sections.index("--identifiers"))
except ValueError:
  pass

indeces = [romSectionIndex, ramSectionIndex, identifiersIndex]
indeces.sort()
ends = [-1, -1, -1]
for i, v in enumerate(indeces[:-1]):
  if v != -1:
    ends[i] = indeces[i + 1]
ends[-1] = len(sys.argv)

romSectionLocation = indeces.index(romSectionIndex)
ramSectionLocation = indeces.index(ramSectionIndex)
identifiersLocation = indeces.index(identifiersIndex)

romSections = sections[indeces[romSectionLocation] +
                       1:ends[romSectionLocation]] if indeces[
                           romSectionLocation] != -1 else ['.text']
ramSections = sections[indeces[ramSectionLocation] +
                       1:ends[ramSectionLocation]] if indeces[
                           ramSectionLocation] != -1 else ['.data', '.bss']
# any paths that contain any of these will be counted
# this will usually be the api and src directories
identifiers = sections[indeces[identifiersLocation] +
                       1:ends[identifiersLocation]] if indeces[
                           identifiersLocation] != -1 else ["./src/"]

print("Using these identifiers: ", identifiers)
print("Using these rom sections: ", romSections)
print("Using these ram sections: ", ramSections)
# romEnd = 0x20000
# ramStart = 0x20000000


def isRom(start, end, section, group):
  # if (end <= romEnd):
  #   return True
  # elif (start >= ramStart):
  #   return False
  if (section in romSections): return True
  elif (section in ramSections): return False


def isRam(start, end, section, group):
  # if (end <= romEnd):
  #   return False
  # elif (start >= ramStart):
  #   return True
  if (section in ramSections): return True
  elif (section in romSections): return False


"""
  @param addrIndexedList: key is addr, value is list [size, section, path, isRom, isRam]
"""


def readObjectFile(filename, addrIndexedList):
  global identifiers

  romUsage = 0
  ramUsage = 0

  with open(filename, 'r') as f:
    reader = list(csv.reader(f))
    for row in reader[1:]:
      if any(i in row[0] for i in identifiers):
        try:
          start = int(row[1], 0)
          inRom = isRom(start, int(row[2], 0), row[4], row[5])
          inRam = isRam(start, int(row[2], 0), row[4], row[5])

          if (inRom == None and inRam == None):
            # print(row)
            # print(start, int(row[2], 0), inRom, inRam)
            raise Exception(
                "Update the ram and rom detection functions, this line doesn't match either: "
                + str(row))

          assert (inRom != inRam)
          if inRom:
            romUsage += int(row[3])
          elif inRam:
            ramUsage += int(row[3])

          if (start in addrIndexedList):
            assert (addrIndexedList[start] == [
                int(row[3]), row[4], row[0], inRom, inRam
            ])
          else:
            addrIndexedList[start] = [
                int(row[3]), row[4], row[0], inRom, inRam
            ]
        except AssertionError as e:
          raise Exception("Inconsistencies found in object file") from e
        except Exception as e:
          print(str(e))
  return romUsage, ramUsage


"""
  @param addrIndexedList: key is addr, value is list [size, section, path, isRom, isRam]
"""


def readSymbolFile(filename, addrIndexedList):
  global identifiers

  romUsage = 0
  ramUsage = 0

  with open(filename, 'r') as f:
    reader = list(csv.reader(f))
    for row in reader[1:]:
      if any(i in row[8] for i in identifiers):
        try:
          start = int(row[1], 0)
          inRom = isRom(start, int(row[2], 0), row[6], row[7])
          inRam = isRam(start, int(row[2], 0), row[6], row[7])
          if (inRom == None and inRam == None):
            # print(row)
            # print(start, int(row[2], 0), inRom, inRam)
            raise Exception(
                "Update the ram and rom detection functions, this line doesn't match either: "
                + str(row))
          assert (inRom != inRam)
          if inRom:
            romUsage += int(row[3])
          elif inRam:
            ramUsage += int(row[3])

          if (start in addrIndexedList):
            assert (addrIndexedList[start] == [
                int(row[3]), row[6], row[8], inRom, inRam
            ])

          else:
            addrIndexedList[start] = [
                int(row[3]), row[6], row[8], inRom, inRam
            ]
        except AssertionError as e:
          raise Exception("Inconsistencies found in symbol file") from e
        except Exception as e:
          print(str(e))

  return romUsage, ramUsage


print("               \t\t  rom\tram")
for folder in ["."]:
  addrIndexedList = {}
  print(folder)
  romUsage = 0
  ramUsage = 0
  romUsage, ramUsage = readObjectFile("%s/Object.csv" % folder,
                                      addrIndexedList)
  print("Object file only:\t", romUsage, "\t", ramUsage)
  romUsage, ramUsage = readSymbolFile("%s/Symbol.csv" % folder,
                                      addrIndexedList)
  print("Symbol file only:\t", romUsage, "\t", ramUsage)

  romUsage = 0
  ramUsage = 0
  for i in addrIndexedList:
    if (addrIndexedList[i][-1]): ramUsage += addrIndexedList[i][0]
    elif (addrIndexedList[i][-2]): romUsage += addrIndexedList[i][0]

  print("Both files:      \t", romUsage, "\t", ramUsage)
  print()
