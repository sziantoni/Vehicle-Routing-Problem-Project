from tkinter import *
from tkinter import filedialog

import numpy
import numpy as np


def distanza(x1, y1, x2, y2):
    from math import sqrt
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# Apertura file
root = Tk()
root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                           filetypes=(("txt", "*.txt"), ("all files", "*.*")))
f = open(root.filename)

# Lettura numero clienti
nClienti = f.readline()
f.readline()

# Lettura numero veicoli
nVeicoli = f.readline()
clients = []  # lista di tutti i clienti
clients_pickup = []  # lista dei clienti con pickup
clients_delivery = []  # lista dei clienti con delivery
demand_pickup = []  # lista della domanda dei pickup
demand_delivery = []  # lista della domanda dei delivery
routes_pickup = [[]]
routes_delivery = [[]]

s = f.readline()
currentLine = s.split("   ")
x_dep = currentLine[0]
y_dep = currentLine[1]
capacity_dep = currentLine[3]

clients.append((float(x_dep), float(y_dep)))
clients_pickup.append((float(x_dep), float(y_dep)))
clients_delivery.append((float(x_dep), float(y_dep)))
count_pickup = 1
count_delivery = 1

for i in f:
    currentLineCustomer = i.split("   ")
    x = currentLineCustomer[0]
    y = currentLineCustomer[1]
    delivery = int(currentLineCustomer[2])
    pickup = int(currentLineCustomer[3])
    # Lista clienti totale
    clients.append((float(x), float(y)))
    # divisione tra delivery e pickup
    if delivery == 0:
        clients_pickup.append((float(x), float(y)))
        demand_pickup.append(pickup)
        if count_pickup > 0:
            routes_pickup.append([0, count_pickup, 0])
        count_pickup += 1
    else:
        clients_delivery.append((float(x), float(y)))
        demand_delivery.append(delivery)
        if count_delivery >= 0:
            routes_delivery.append([0, count_pickup + (count_delivery-1), 0])
        count_delivery += 1

f.close()

routes_pickup.remove([])
routes_delivery.remove([])

print(demand_pickup)
print(demand_delivery)
print(routes_pickup)
print(routes_delivery)

w = int(nClienti) + 1

costs = np.array([[0 for x in range(w)] for y in range(w)])
costs_pickup = np.array([[0 for x in range(count_pickup)] for y in range(count_pickup)])
costs_delivery = np.array([[0 for x in range(count_delivery)] for y in range(count_delivery)])
saving = np.array([[0 for x in range(w - 1)] for y in range(w - 1)])
saving_pickup = np.array([[0 for x in range(count_pickup - 1)] for y in range(count_pickup - 1)])
saving_delivery = np.array([[0 for x in range(count_delivery - 1)] for y in range(count_delivery - 1)])
saving_list = []
saving_list_delivery = []
saving_list_pickup = []

cont1 = 0
cont2 = 0

for i in clients:
    for j in clients:
        if i != j:
            d = distanza(i[0], i[1], j[0], j[1])
            costs[cont1, cont2] = d
        else:
            costs[cont1, cont2] = 0
        cont2 += 1
    cont1 += 1
    cont2 = 0
cont1 = 0
cont2 = 0

for i in clients_pickup:
    for j in clients_pickup:
        if i != j:
            d = distanza(i[0], i[1], j[0], j[1])
            costs_pickup[cont1, cont2] = d
        else:
            costs_pickup[cont1, cont2] = 0
        cont2 += 1
    cont1 += 1
    cont2 = 0

cont1 = 0
cont2 = 0

for i in clients_delivery:
    for j in clients_delivery:
        if i != j:
            d = distanza(i[0], i[1], j[0], j[1])
            costs_delivery[cont1, cont2] = d
        else:
            costs_delivery[cont1, cont2] = 0
        cont2 += 1
    cont1 += 1
    cont2 = 0

for count1 in range(1, len(saving) + 1):
    for count2 in range(1, len(saving) + 1):
        if count1 != count2:
            saving[count1 - 1, count2 - 1] = costs[count1][0] + costs[0][count2] - costs[count1][count2]
            if ((count1, count2, saving[count1 - 1, count2 - 1]) not in saving_list) and (
                    (count2, count1, saving[count1 - 1, count2 - 1]) not in saving_list) and len(saving_list) > 0:
                saving_list.append((count1, count2, saving[count1 - 1, count2 - 1]))
            else:
                if len(saving_list) == 0:
                    saving_list.append((count1, count2, saving[count1 - 1, count2 - 1]))

    count2 = 1

for count1 in range(1, len(saving_delivery) + 1):
    for count2 in range(1, len(saving_delivery) + 1):
        if count1 != count2:
            saving_delivery[count1 - 1, count2 - 1] = costs_delivery[count1][0] + costs_delivery[0][count2] - \
                                                      costs_delivery[count1][count2]
            if ((count1, count2, saving_delivery[count1 - 1, count2 - 1]) not in saving_list_delivery) and (
                    (count2, count1, saving_delivery[count1 - 1, count2 - 1]) not in saving_list_delivery) and len(
                saving_list_delivery) > 0:
                saving_list_delivery.append((count1, count2, saving_delivery[count1 - 1, count2 - 1]))
            else:
                if (len(saving_list_delivery) == 0) and (count1 != count2):
                    saving_list_delivery.append((count1, count2, saving_delivery[count1 - 1, count2 - 1]))

    count2 = 1

for count1 in range(1, len(saving_pickup) + 1):
    for count2 in range(1, len(saving_pickup) + 1):
        if count1 != count2:
            saving_pickup[count1 - 1, count2 - 1] = costs_pickup[count1][0] + costs_pickup[0][count2] - \
                                                    costs_pickup[count1][count2]
            if ((count1, count2, saving_pickup[count1 - 1, count2 - 1]) not in saving_list_pickup) and (
                    (count2, count1, saving_pickup[count1 - 1, count2 - 1]) not in saving_list_pickup) and len(
                saving_list_pickup) > 0:
                saving_list_pickup.append((count1, count2, saving_pickup[count1 - 1, count2 - 1]))
            else:
                if (len(saving_list_pickup) == 0) and (count1 != count2):
                    saving_list_pickup.append((count1, count2, saving_pickup[count1 - 1, count2 - 1]))
    count2 = 1

saving_list = sorted(saving_list, key=lambda tup: tup[2], reverse=True)
saving_list_delivery = sorted(saving_list_delivery, key=lambda tup: tup[2], reverse=True)
saving_list_pickup = sorted(saving_list_pickup, key=lambda tup: tup[2], reverse=True)

print("Saving list")
print(saving_list)
print("Saving list pick up")
print(saving_list_pickup)
print("Saving list delivery")
print(saving_list_delivery)

print("COST")
print(costs)
print("SAVING")
print(saving)
print("SAVING D")
print(saving_delivery)
print("SAVING P")
print(saving_pickup)
print("DEMAND DELIVERY")
print(demand_delivery)
print("DEMAND PICKUP")
print(demand_pickup)


# LINEHAUL

def CW_P(savings_list, saving_matrix, routes, capacity_limit, number_of_vehicles, demands, type):
    start = 0
    end = 0
    route1 = 0
    route2 = 0
    flag1 = False
    flag2 = False

    for i in savings_list:
        counter = 0
        best_saving = i
        start_route = []
        end_route = []
        flag1 = False
        flag2 = False
        for r in routes:
            counterR = 0
            for n in r:
                if n not in start_route or n not in end_route:
                    if best_saving[0] == n and n != 0:
                        if r[counterR + 1] == 0 and flag1 == False:
                            start = n
                            start_route = r[:counterR + 1]
                            if counter != route2:
                                route1 = counter
                                flag1 = True
                        else:
                            if (r[counterR - 1] == 0) and (flag2 == False):
                                end = n
                                end_route = r[counterR:]
                                if counter != route1:
                                    route2 = counter
                                flag2 = True
                    else:
                        if best_saving[1] == n and n != 0:
                            if r[counterR + 1] == 0 and flag1 == False:
                                start = n
                                start_route = r[:counterR + 1]
                                if counter != route2:
                                    route1 = counter
                                flag1 = True
                            else:
                                if r[counterR - 1] == 0 and flag2 == False:
                                    end = n
                                    end_route = r[counterR:]
                                    if counter != route1:
                                        route2 = counter
                                    flag2 = True
                    counterR += 1
                counter += 1
                if start != 0 and end != 0 and flag1 and flag2:
                    flag1 = False
                    flag2 = False
                    if type == 0:  # presupponiamo 0 sia il pickup e 1 il delivery
                        counter_demands = 0
                        demand_total = 0
                        for x in range(len(demands)):
                            if (x + 1 in start_route) or (x + 1 in end_route):
                                demand_total += demands[x]
                        if float(demand_total) <= float(capacity_limit):
                            new_route = start_route + end_route
                            for i in range(len(routes)):
                                if i == route1:
                                    del routes[i]
                            for i in range(len(routes)):
                                if i == route2 - 1:
                                    del routes[i]

                            routes.append(new_route)
                            start_route = []
                            end_route = []
    return routes


prova = CW_P(saving_list_pickup, saving_pickup, routes_pickup, capacity_dep, nVeicoli, demand_pickup, 0)

print("PROVA")
print(prova)
