import nbt
import array

#Loads the map.dat file, which must be numbered 777 and in the python main directory
mappath = raw_input("Please type the full filename path of the map.dat file you wish to convert\n")
mapfile = nbt.NBTFile(mappath, 'rb')
schematicpath = raw_input("\nPlease type the full filename path of the schematic file you wish to create\nThe file name must end in \".schematic\"\nSaving directly to the C drive requires administrator privileges\n")
print

blocksBytes = mapfile['data']['colors'].value
tempcolors = [0]*16384
tempcolors = [i for i in blocksBytes]



#maximum amount the schematic will vertically rise from the starting level
maxup = 0
#max amount the schematic will vertically decline from the starting level
maxdown = 0
#maps the relative height of each (x, y) position, but takes m(x, y) as an input
height = [0]*(128*128)
edgeheight = [0]*128

#blockid[map color index number] = block id number
blockid = [
7, 7, 7, 7,
2, 2, 2, 2,
88, 88, 88, 88,
13, 13, 13, 13,
46, 46, 46, 46,
174, 174, 174, 174,
101, 101, 101, 101,
116, 116, 116, 116,
80, 80, 80, 80,
82, 82, 82, 82,
3, 3, 3, 3,
4, 4, 4, 4,
9, 9, 9, 9,
5, 5, 5, 5,
35, 35, 35, 35,
35, 35, 35, 35,
35, 35, 35, 35,
35, 35, 35, 35,
35, 35, 35, 35,
35, 35, 35, 35,
35, 35, 35, 35,
35, 35, 35, 35,
35, 35, 35, 35,
35, 35, 35, 35,
35, 35, 35, 35,
35, 35, 35, 35,
35, 35, 35, 35,
35, 35, 35, 35,
35, 35, 35, 35,
35, 35, 35, 35,
170, 170, 170, 170,
57, 57, 57, 57,
22, 22, 22, 22,
133, 133, 133, 133,
49, 49, 49, 49,
87, 87, 87, 87]

#Contains block data numbers (0 for everything but colored wool)
#Used in the same way as blockid
blockdata = [
0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0,
1, 1, 1, 1,
2, 2, 2, 2,
3, 3, 3, 3,
4, 4, 4, 4,
5, 5, 5, 5,
6, 6, 6, 6,
7, 7, 7, 7,
8, 8, 8, 8,
9, 9, 9, 9,
10, 10, 10, 10,
11, 11, 11, 11,
12, 12, 12, 12,
13, 13, 13, 13,
14, 14, 14, 14,
15, 15, 15, 15,
0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0 ]

#Given (x, y), returns the linear array index for the map data array
#Our (x, y) starts in the BOTTOM left (southwest) corner, with x = y = 1
#This is also the index used for height[]
def m(x, y):
	num = x + 128 * (127-y)
	return num
	
#Returns the linear index used for the schematic "Blocks" and "Data" arrays
def s(x, y):
	if y < 128:
		num = x + ((128-y)*128) + (height[m(x,y)]+abs(maxdown))*128*129
		return num
	elif y == 128:
		num = x + ((128-y)*128) + (edgeheight[x]+abs(maxdown))*128*129
		return num


#Assigns values to maxup and maxdown, and height[]
def findheight():
	global maxdown
	global maxup
	global edgeheight
	for x in xrange(128):
		for y in xrange(128):
			if y == 0:
				height[m(x,y)] = 0
			if y != 127:
				if tempcolors[m(x, y)]%4 == 0:
					height[m(x,y+1)] = height[m(x,y)]+1
				elif tempcolors[m(x, y)]%4 == 1:
					height[m(x,y+1)] = height[m(x,y)]
				elif tempcolors[m(x, y)]%4 == 2:
					height[m(x,y+1)] = height[m(x,y)]-1
				elif tempcolors[m(x, y)]%4 == 3:
					height[m(x,y+1)] = height[m(x,y)]+1
				if height[m(x,y)] < maxdown:
					maxdown = height[m(x,y)]
				elif height[m(x,y)] > maxup:
					maxup = height[m(x,y)]
	for x in xrange(128):
		if tempcolors[m(x, 127)]%4 == 0:
			edgeheight[x] = height[m(x,127)]+1
		elif tempcolors[m(x, 127)]%4 == 1:
			edgeheight[x] = height[m(x,127)]
		elif tempcolors[m(x, 127)]%4 == 2:
			edgeheight[x] = height[m(x,127)]-1
		elif tempcolors[m(x, 127)]%4 == 3:
			edgeheight[x] = height[m(x,127)]+1
		if edgeheight[x] > maxup:
			maxup = edgeheight[x]
		if edgeheight[x] < maxdown:
			maxdown = edgeheight[x]
		if height[m(x,127)] < maxdown:
			maxdown = height[m(x,127)]
		elif height[m(x,127)] > maxup:
			maxup = height[m(x,127)]

#Creates a schematic nbt file, assigns values to its tags, and saves the file
def createschematic():
	a = (128*129*(maxup+abs(maxdown)+1))
	schematic = nbt.NBTFile()
	schematic["Height"] = nbt.TAG_Short(value=(abs(maxdown)+maxup+1))
	schematic["Length"] = nbt.TAG_Short(value=129)
	schematic["Width"] = nbt.TAG_Short(value=128)
	tempblocks = array.array('B', [0]*a)
	tempdata = array.array('B', [0]*a)
	for x in xrange(128):
		for y in xrange(128):
			tempblocks[s(x,y)] = blockid[tempcolors[m(x, y)]]
			tempdata[s(x,y)] = blockdata[tempcolors[m(x, y)]]
		tempblocks[s(x,128)] = 3
		tempdata[s(x,128)] = 0
	schematic["Blocks"] = nbt.TAG_Byte_Array()
	schematic["Data"] = nbt.TAG_Byte_Array()
	schematic["Blocks"].value = bytearray(tempblocks)
	schematic["Data"].value = bytearray(tempdata)
	schematic["Materials"] = nbt.TAG_String(value="Alpha")
	print "Writing file..."
	schematic.write_file(schematicpath)
	print "Schematic successfully created!"
	print "max height up: " + repr(maxup)
	print "max height down: " + repr(abs(maxdown))
	print "Minimum height you should build at: " + repr(maxup+64)

print "Calculating heights..."
findheight()
print "Processing schematic file..."
createschematic()
raw_input("Press Enter to continue")