
import csv

LIST = []
RESULTING_LIST = []
# checking_round = 12
ROUNDS = 32 + 1
NUMBER_OF_FIRST_ROUND = 1

def save_to_file():
    file_name = 'C:\\PycharmProjects\\BezDurakov\\main_table.csv'
    with open(file_name, 'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(LIST[0])
        writer.writerows(RESULTING_LIST)

def make_list():
    file_name = 'C:\\PycharmProjects\\BezDurakov\\origin_table.csv'
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for header in reader:
            while len(header) >= ROUNDS*2+1:
                header.pop()

            for i in range(1,ROUNDS):
                header.append('K'+str(i))

            break

        for row in reader:
            for i in range(1,ROUNDS):
                row.append(str(1))

            LIST.append(dict(zip(header, row)))

def get_list_exp_sums(rank):
    if rank == 2.5:
        return [250,500,750,1250,1500,1750,2250,2500,2750,3250,3500,3750]
    elif rank == 2:
        return [200,400,800,1000,1400,1600,2000,2200,2400,2600,2800,3000]
    else:
        return [150,450,750,1050,1350,1650,1800,1950,2100,2250]

def get_koef(rank):

    list_exp_sums = get_list_exp_sums(rank)
    for num in range(NUMBER_OF_FIRST_ROUND, ROUNDS):
        max_stake = 0
        max_wickness = 0

        # Сначала найдем максимальную ставку
        for team in LIST:
            if team['K' + str(num)] == '1' and int(team['Stake' + str(num)]) > max_stake:  # только тех смотрим у кого коэффициент еще не установлен
                max_stake = int(team['Stake' + str(num)])

        # Теперь посмотрим, сколько команд с максимакльной ставкой мы нашли
        com_with_max_stake = 0
        for team in LIST:
            if team['K' + str(num)] == '1' and int(team['Stake' + str(num)]) == max_stake:
                com_with_max_stake += 1

        founded_index = False
        if com_with_max_stake > 1: #придется до рейтинга по сумме попробовать оценить
            for team in LIST:
                if team['K' + str(num)] == '1' and int(team['Stake' + str(num)]) == max_stake:
                    if int(team['Sum' + str(num)]) in list_exp_sums: #нашли,  установим коэфф и сумму
                        team['K' + str(num)] = str(rank)
                        team['Sum' + str(num)] = int(team['Sum' + str(num)]) / rank
                        # print(team['Team'], 'get koef', rank)
                        founded_index = True
                        break

        if not founded_index: #не нашли по сумме, будем по рейтингу подбирать
            # среди команд с максимальной ставкой найдем слабейший рейтинг
            for team in LIST:
                if team['K' + str(num)] == '1' and int(team['Stake' + str(num)]) == max_stake:
                    if max_wickness < int(team['Rating']):
                        max_wickness = int(team['Rating'])

            # Последний цикл установим коэф для команды с нужной ставкой и рейтингом
            for team in LIST:
                if team['K' + str(num)] == '1' and int(team['Stake' + str(num)]) == max_stake and int(
                        team['Rating']) == max_wickness:
                    team['K' + str(num)] = str(rank)
                    team['Sum' + str(num)] = int(team['Sum' + str(num)])/rank
                    # print(team['Team'], 'get koef', rank)


def rewrite_koefs(): #установим все коэффициенты в единицы, для дальнейшей работы с таблицей
    for num in range(1, ROUNDS):
        for team in LIST:
            team['K' + str(num)] = '1'

def modify_list():

    for i in LIST:
        RESULTING_LIST.append(list(i.values()))


def analyse():
    get_koef(2.5)
    get_koef(2)
    get_koef(2)
    get_koef(1.5)
    get_koef(1.5)

def main():

    make_list()

    analyse()

    rewrite_koefs()

    modify_list()

    save_to_file()

    # print(LIST)
    # print(RESULTING_LIST)


if __name__ == '__main__':
    main()
