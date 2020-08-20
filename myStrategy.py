
import numpy as np

def continue_drop(data, n):
	for i in range(n):
		if(data[-(n+1)+i]>data[-(n+1)+i+1]):
			continue
		else:
			return False
	return True



def CrossOver(pastData,currentPrice,s,l):
    action = 0
    shortpast = np.mean(pastData[-s:]) 
    longpast = np.mean(pastData[-l:])
    pastData = list(pastData)
    pastData.append(currentPrice)
    pastData = np.array(pastData)
    shortcur = np.mean(pastData[-s:])
    longcur = np.mean(pastData[-l:])
    if(shortpast<longpast and shortcur>longcur):
        action = 1
    elif (longpast < shortpast and longcur > shortcur):
        action = -1
    else:
        action = 0

    return action


def MA(pastData, currentPrice, windowSize, alpha, beta):
    action=0      
    dataLen=len(pastData)
    if dataLen==0:
        return action
    # Compute ma
    if dataLen<windowSize:
        ma=np.mean(pastData)    
    else:
        windowedData=pastData[-windowSize:]    
        ma=np.mean(windowedData)
    # Determine action

    if (currentPrice-ma) > alpha: 
        action= -1
    elif (ma - currentPrice) > beta: 
        action= 1
    return action
def ema(windowSize):
    alpha = 2/(windowSize+1)
    weights = (1-alpha)**np.arange(windowSize)
    weights /= weights.sum()
    return weights[::-1]

def EMA(pastData,currentPrice,w1,w2):

    dataLen = len(pastData)
    if dataLen < w1+2:
        return 0

    L_weights = ema(w1)
    M_weights = ema(w2)
    L_ma = np.dot(L_weights, np.append(pastData[-w1+1:], [currentPrice]))
    L_ma_past = np.dot(L_weights, pastData[-w1-1:-1])
    M_ma = np.dot(M_weights, np.append(pastData[-w2+1:], [currentPrice]))
    M_ma_past = np.dot(M_weights, pastData[-w2-1:-1])

    if(M_ma > L_ma and M_ma_past < L_ma_past):
        action=1
    elif(M_ma < L_ma  and M_ma_past > L_ma_past):
        action=-1
    else:
        action=1

    return action


def SMA(pastData,currentPrice,windowSize):
    SMAu = 0
    SMAd = 0
    temp = pastData[-windowSize:]
    for i in range(windowSize-1):
        if temp[i]<temp[i+1]:
            SMAu += temp[i+1]-temp[i]
        else:
            SMAd += temp[i]-temp[i+1]
    return SMAu/windowSize,SMAd/windowSize

def RSI(pastData,currentPrice,windowSize,low,up):
    action = 0
    if(len(pastData)<5):
        action = 0
        return action
    if(len(pastData)<windowSize):
        windowSize = len(pastData)
    SMAu,SMAd = SMA(pastData, currentPrice, windowSize)
    value = SMAu/(SMAu+SMAd)
    if(int(value*100)>up):
        action = -1
    if(int(value*100)<low):
        action = 1
    return action
def continue_climb(data, n):
	for i in range(n):
		if(data[-(n+1)+i]<data[-(n+1)+i+1]):
			continue
		else:
			return False
	return True


def myStrategy(dailyOhlcvFile,minutelyOhlcvFile,openprice):
	daily = dailyOhlcvFile
	minutely = minutelyOhlcvFile
	oprice = openprice
	# print(dailyOhlcvFile.tail(1))
	if(dailyOhlcvFile.trading_point.iloc[-1]>='2020-01-10'):
		return 0
	if(dailyOhlcvFile.trading_point.iloc[-1] == '2020-01-09'):
		return -1
	# print(oprice)
	""" MA paramater """
	vote = []
	MA_pastlen =240
	data = daily.open.tail(MA_pastlen).values
	windowSize = 20
	alpha = openprice*0.005
	beta = openprice*0.001
	"""end of ma parameter"""
	#print(data)
	# action = EMA(data, openprice, 5,10)
	# return action
	action = MA(data, openprice, windowSize, alpha, beta)

	# print(action)
	# return action
	vote.append(action)
	"""golden cross over parameter"""
	s = 5
	l = 20
	action = CrossOver(data, openprice, s,l)
	vote.append(action)
	# print(action)
	# return action

	temp = daily.open.tail(14).values
	if(continue_drop(temp,3)):
		action = 1
	elif(continue_climb(temp,5)):
		action = -1
	else:
		action = 0
	# return action
	vote.append(action)
	"""RSI"""
	window = 5
	action = RSI(data, openprice, window, 15, 85)
	vote.append(action)
	# print(action)
	# return action
	vote.append(1)
	# return action
	# print(vote)
	# print(np.sign(sum(vote)))
	# print(vote)
	# print(np.sign(sum(vote)))
	return np.sign(sum(vote)) 
	# print(daily.open.tail(14).values)
	# plt.plot(daily.open.tail(14).values)
	# plt.show()
	# l = 5
	# action = 0
	# counts = 0
	# for i in range(l):
	# 	counts += float(daily.iloc[-l+i].close)
	# avg = counts/l
	# if(oprice - avg > 0):
	# 	action = -1
	# elif(oprice - avg < 0):
	# 	action = 1
	# else:
	# 	aciton = 0
	# print(action)
	# if(openprice[-1]>openprice[-2]):
	# 	action = -1
	# print(daily.shape)
	# print(minutely.shape)
	# print(oprice)






