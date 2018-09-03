from zipfile import ZipFile

filepwd = open('list.txt', 'r')

for passwd in filepwd:
	with ZipFile('mondai.zip') as zf:
		try:
			zf.extractall(pwd=passwd.strip().encode())
			print(passwd.strip().encode())
		except Exception as e:
			# print(e)
			pass
# eVjbtTpvkU
