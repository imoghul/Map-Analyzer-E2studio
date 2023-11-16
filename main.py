import csv

labels = ""
with open('labels.txt', 'r') as f:
  labels = f.read().split("\n")

# romEnd = 0x20000
# ramStart = 0x20000000

# any paths that contain any of these will be counted
identifiers = ['./QCIOT009', './src/']

romSections = ['.text']
ramSections = ['.bss', '.data']


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
                f"Update the ram and rom detection functions, this line doesn't match either: {row}"
            )

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
                f"Update the ram and rom detection functions, this line doesn't match either: {row}"
            )
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


print("\t\t\t\t\t rom\tram")
for file in ["master freertos", "master noos", "slave freertos", "slave noos"]:
  addrIndexedList = {}
  print(file)
  romUsage = 0
  ramUsage = 0
  romUsage, ramUsage = readObjectFile(f"{file}/Object.csv", addrIndexedList)
  print("Object file only:\t", romUsage, "\t", ramUsage)
  romUsage, ramUsage = readSymbolFile(f"{file}/Symbol.csv", addrIndexedList)
  print("Symbol file only:\t", romUsage, "\t", ramUsage)

  romUsage = 0
  ramUsage = 0
  for i in addrIndexedList:
    if (addrIndexedList[i][-1]): ramUsage += addrIndexedList[i][0]
    elif (addrIndexedList[i][-2]): romUsage += addrIndexedList[i][0]

  print("Both files:\t\t\t", romUsage, "\t", ramUsage)
  print()
