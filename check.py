import json
import sys

def main():
	print(sys.argv)    
	try:
		one = open(sys.argv[1]).read()
		data1 = json.loads(one)
		two = open(sys.argv[2]).read()
		data2 = json.loads(two) 
	except:
		print("Please enter a valid file")
		return -1

	check(data1, data2)

def check(a, b):
	#if type(a) != type(b) or len(a) != len(b):
	#	print('bad')
	if type(a) == list:
		#print('list')
		for i in range(len(a)):
			check(a[i], b[i])
	elif type(a) == dict:
		#print('dict')
		for i in a.keys():
			check(a[i], b[i])
	else:
		print(a, b)

if __name__ == '__main__':
	main()

