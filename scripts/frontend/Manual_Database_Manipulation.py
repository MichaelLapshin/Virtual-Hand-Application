count = 0
total = 0


def recur(people, seasons=[[], [], [], []]):
    global count, total

    if people == 0:
        total += 1
        if len(seasons[0]) > 0 and len(seasons[1]) > 0 and len(seasons[2]) > 0 and len(seasons[3]) > 0:
            count += 1
            print(seasons)
        else:
            print("No", seasons)
        return

    for i in range(0, 4):
        seasons[i].append(people)
        recur(people=people - 1, seasons=seasons)
        seasons[i].remove(people)


recur(8                                                                                                                                                                                                                                                                                                                                                                                                                               )
print(total, count)
