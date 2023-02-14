from datetime import datetime

def time_dif(ind):

    now = datetime.now()
    ind = ind.split('-')
    ind = ind[0:2] + ind[2].split(' ')
    ind = ind[0:3] + ind[3].split(':')
    ind = list(map(int, ind))
    years = ind[0]
    months = ind[1]
    days = ind[2]
    hours = ind[3]
    minutes = ind[4]
    seconds = ind[5]

    dif = now - datetime(years, months, days, hours, minutes, seconds)
    dif = int(dif.total_seconds() // 1)

    if (dif // 60) < 1:
        if dif == 11 or dif == 12 or dif == 13 or dif == 14:
            return(str(dif) + ' секунд назад')
        elif dif % 10 == 2 or dif % 10 == 3 or dif % 10 == 4:
            return(str(dif) + ' секунды назад')
        elif dif % 10 == 1:
            return(str(dif) + ' секунду назад')
        else:
            return(str(dif) + ' секунд назад')
    elif (dif // 3600) < 1:
        if dif // 60 == 11 or dif // 60 == 12 or dif // 60 == 13 or dif // 60 == 14:
            return(str(dif // 60) + ' минут назад')
        elif dif // 60 % 10 == 2 or dif // 60 % 10 == 3 or dif // 60 % 10 == 4:
            return(str(dif // 60) + ' минуты назад')
        elif dif // 60 % 10 == 1:
            return(str(dif // 60) + ' минуту назад')
        else:
            return(str(dif // 60) + ' минут назад')
    elif (dif // 86400) < 1:
        if dif // 3600 == 11 or dif // 3600 == 12 or dif // 3600 == 13 or dif // 3600 == 14:
            return(str(dif // 3600) + ' часов назад')
        elif dif // 3600 % 10 == 2 or dif // 3600 % 10 == 3 or dif // 3600 % 10 == 4:
            return(str(dif // 3600) + ' часа назад')
        elif dif // 3600 % 10 == 1:
            return(str(dif // 3600) + ' час назад')
        else:
            return(str(dif // 3600) + ' часов назад')
    else:
        if dif // 86400 == 11 or dif // 86400 == 12 or dif // 86400 == 13 or dif // 86400 == 14:
            return(str(dif // 86400) + ' дней назад')
        elif dif // 86400 % 10 == 2 or dif // 86400 % 10 == 3 or dif // 86400 % 10 == 4:
            return(str(dif // 86400) + ' дня назад')
        elif dif // 86400 % 10 == 1:
            return(str(dif // 86400) + ' день назад')
        else:
            return(str(dif // 86400) + ' дней назад')

