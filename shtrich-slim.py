import serial, time, struct, datetime

ser = serial.Serial(port='COM3',baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0, rtscts=0) # настройки COM порта для Windows
#ser.close() 
#ser.open() если программа говорит что порт уже открыт, попробовать раскомментировать эту и предыдущую строку
#print(ser.portstr) - добавить в вывод номер COM порта 
data = (b'\x02\x05\x3A\x30\x30\x33\x30\x3C') # команда весам (код команды в байтах можно подглядеть в тест-драйвере весов)
ser.write (data) # отправляем команду весам
ser.timeout = 1 # ждем 1 секунду для получения ответа (не обязательный параметр, но лучше подождать секунду)
#print(ser.in_waiting) - вывод времени за которое приходит ответ из COM порта
#line = ser.read(15) - если нужно считать определенное количество байт
line = ser.readline()
#print(line) - добавить в вывод ответ от COM порта в виде последовательности байт
f = struct.unpack('<3x1b3x1I4x', line) # используем struct для выделения нужных байт из ответного сообщения от COM порта
(a, b) = f
if b >= 10000:
	l = b/10000; #байты в ответе из COM порта приходят в обратном порядке, чтоб в ответе был верный вес, при помощи деления выставляем запятую в нужное место.
	f = open('logs.txt', 'a')
	today = datetime.datetime.today()
	g = today.strftime("%Y-%m-%d-%H.%M.%S")
	f.write(str(g) + " Вес начинки = " + str(l) +" Килограмм " + "\r\n")
	f.close()
	print("Вес начинки = ",l,"Килограмм")

elif 5<b<10000:
	n=b/10; # тоже самое что и выше но уже для веса меньше 1 Кг
	f = open('logs.txt', 'a') 
	today = datetime.datetime.today()
	w = today.strftime("%Y-%m-%d-%H.%M.%S")
	f.write(str(w) + " Вес начинки = " + str(n) +" Грамм " + "\r\n")
	f.close()
	print ("Вес начинки = ",n,"Грамм");

elif b == 0:
	print ("Вес начинки = ",0,"Грамм");
		

ser.close() # закрываем порт, на всякий случай.



#02 ответная команда
#0B длина
#3A команда
#00 код ошибки
#15 00 состояние
#6A 04 00 00 вес
#00 00 тара
#00  резервный байт
#4A конец строки 

# Для работы так же советую использовать http://xor.pw/ и оффициальную документацию "Протокол весового модуля. V1.2. (14.02.2005)"
# помогает перевести байты в читабельный вид.

#P.S автор программы Telegramm and mail: [@ruselsh] & [siertum@gmail.com]
# Ссылка на весы https://www.shtrih-m.ru/catalog/pos-vesy/shtrikh-slim/
