import ctypes
print("hello world")

mylibrary = ctypes.CDLL('./data_control.so')
mylibrary.select_transcript.argtypes = [ctypes.c_int]
mylibrary.select_transcript.restype = ctypes.c_char_p

result = ""
sql_id = 3
if(mylibrary.select_transcript(sql_id) != None):
	result = str(mylibrary.select_transcript(sql_id), "utf-8")
print(result)