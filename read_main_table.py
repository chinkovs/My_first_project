import csv

GAME_NUMBER = 8
LIST = []
RESULTING_LIST = []
checking_round = GAME_NUMBER * 4
ROUNDS = checking_round + 1
NUMBER_OF_FIRST_ROUND = 1#+(GAME_NUMBER-1)*4 #checking_round
CALM_ROUND = 3
# STAKE_FOR_LIDER = 1500

def make_list():

    LIST.clear()
    file_name = 'C:\\PycharmProjects\\BezDurakov\\main_table.csv'
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for header in reader:
            break

        for row in reader:
            LIST.append(dict(zip(header, row)))


def get_koef(rank):
    for num in range(NUMBER_OF_FIRST_ROUND, ROUNDS):
        max_stake = 0
        max_wickness = 0

        # Сначала найдем максимальную ставку
        for team in LIST:
            if team['K' + str(num)] == '1' and int(
                    team['Stake' + str(num)]) > max_stake:  # только тех смотрим у кого коэффициент еще не установлен
                max_stake = int(team['Stake' + str(num)])

        # Теперь среди команд с максимальной ставкой найдем слабейший рейтинг
        for team in LIST:
            if team['K' + str(num)] == '1' and int(team['Stake' + str(num)]) == max_stake:
                if max_wickness < int(team['Rating']):
                    max_wickness = int(team['Rating'])

        # Последний цикл установим коэф для команды с нужной ставкой и рейтингом
        for team in LIST:
            if team['K' + str(num)] == '1' and int(team['Stake' + str(num)]) == max_stake and int(
                    team['Rating']) == max_wickness:
                team['K' + str(num)] = str(rank)
                team['Sum' + str(num)] = rank * float(team['Sum' + str(num)])
                # print(team['Team'], 'get koef', rank)

def calc_sum(stake):

    com_list = []
    for i,team in enumerate(LIST):
        total = 0
        for num in range(NUMBER_OF_FIRST_ROUND,ROUNDS):
            try:
                total += float(team['Sum' + str(num)])
                total -= float(team['Stake' + str(num)])
            except:
                print('Team',team['Team'], 'num', str(num))

        dicti = {'Team':team['Team'],'sum':total}
        com_list.append(dicti)

    sum_of_lider = com_list[0]['sum']
    place_of_lider = 1
    max_sum = 0
    max_team = ''

    for num,dict in enumerate(com_list):
        if num == 0:
            continue
        elif dict['sum'] > max_sum:
            max_sum = dict['sum']
            max_team = dict['Team']

        if dict['sum'] >= sum_of_lider :
            place_of_lider += 1
    percent = int(100*sum_of_lider/max_sum)

    RESULTING_LIST.append(['Stake: '+str(stake),' Sum: '+str(sum_of_lider),' Percent: '+str(percent), ' Place: '+str(place_of_lider),' Best opponent team: '+str(max_team)])




def analyse(stake):
    get_koef(2.5)
    get_koef(2)
    get_koef(2)
    get_koef(1.5)
    get_koef(1.5)
    calc_sum(stake)

def modify_list(stake):

    if CALM_ROUND != 0:
        if CALM_ROUND == 1:
            list_of_calm_rounds = [1,5,9,13,17,21,25,29,33,37,41,45]
        elif CALM_ROUND == 2:
            list_of_calm_rounds = [2,6,10,14,18,22,26,30,34,38,42,46]
        elif CALM_ROUND == 3:
            list_of_calm_rounds = [3,7,11,145,189,23,267,31,35,39,43,47]
        elif CALM_ROUND == 4:
            list_of_calm_rounds = [4,8,12,16,20,24,28,32,36,40,44,48]

    for num in range(NUMBER_OF_FIRST_ROUND, ROUNDS):
        for team in LIST:
            #только первую строку обработаем
            team['Stake' + str(num)] = stake

            if CALM_ROUND != 0:
                if num in list_of_calm_rounds:
                    team['Stake' + str(num)] = 100
            break

def save_to_file():
    file_name = 'C:\\PycharmProjects\\BezDurakov\\results.csv'
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        for i in RESULTING_LIST:
            writer.writerow(i)
            print(i)


def main():

    for stake in range(100,1800,100):
        make_list()

        modify_list(stake)

        analyse(stake)

    save_to_file()

    # print(LIST)


if __name__ == '__main__':
    main()
