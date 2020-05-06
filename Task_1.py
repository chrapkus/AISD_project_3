import random
import time
import copy
import csv


def upgrade_dict(list, a , b):
    list[a]["state"] += 1
    list[a]["connections"].append(b)
    list[a]["connections"].sort()

    list[b]["state"] += 1
    list[b]["connections"].append(a)
    list[b]["connections"].sort()

    return list



def delate_connection(list, a , b):
    list[a]["state"] -= 1
    list[a]["connections"].remove(b)

    list[b]["state"] -= 1
    list[b]["connections"].remove(a)

    return list


def timer(f, A, B, c):
    tic = time.perf_counter()
    print("111=+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f(A ,B, c))
    print("111=+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    toc = time.perf_counter()
    return round(toc - tic, 5)



def graph_creator(size, saturation):

    vertex_list = {}

    all_connections = []

    for x in range(1, size+1):

        vertex_list[x] = {"state" : 0, "connections" : []} # create dict where value is a key and it holds it's lvl and connection

    for x in range(1,size):
        t = [x,x+1]
        all_connections.append(t)
        vertex_list = upgrade_dict(vertex_list ,x ,x+1)

    all_connections.append([1,size])
    vertex_list = upgrade_dict(vertex_list ,1 ,size) # here connect first and last item (can't do it in loop)

    t = int(((size * (size - 1) / 2) * saturation / 100)) % 2

    while (int(((size * (size - 1) / 2) * saturation / 100)) + t) > len(all_connections):

        extending_index = random.randrange(0 ,len(all_connections)-1)
        extending_edge = all_connections[extending_index]

        a = extending_edge[0]
        b = extending_edge[1]

        new_point = random.randrange(1,size+1)

        if new_point != a and new_point != b and (new_point not in vertex_list[a]["connections"]) and (new_point not in vertex_list[b]["connections"]):
            a_new = [a, new_point]
            a_new.sort()
            b_new = [b, new_point]
            b_new.sort()

            vertex_list = upgrade_dict(vertex_list, a, new_point)
            vertex_list = upgrade_dict(vertex_list, b, new_point)

            all_connections.append(a_new)
            all_connections.append(b_new)

            vertex_list = delate_connection(vertex_list, a, b)
            del all_connections[extending_index]

    return vertex_list, all_connections

def del_connection_all_connetions(a, b , all_connections):
    list = [a, b]
    list.sort()

    for index, number in enumerate(all_connections):
        if list == number:
            all_connections.pop(index)
    return all_connections


def euler_path(vertex_list, all_connections, size):
    stack = []
    location = random.randrange(1, size + 1)
    # print(location)
    # print("//////first call")

    n = len(all_connections)
    circut = []


    while len(circut) < n:

        if vertex_list[location]["connections"]  != []:
            stack.append(location)
            old = location
            location = vertex_list[location]["connections"][0]
            vertex_list = delate_connection(vertex_list, old, location)
            all_connections = del_connection_all_connetions(old, location, all_connections)

            # print("old_location {} location {} stack {}".format(old, location, stack))

        else:
            # print("location {} stack {}".format(location, stack))
            circut.append(location)
            k = len(stack)
            # print(k)
            location = stack.pop(k-1)
            # print("location {} stack {}".format(location, stack))



        # print("n: {}".format(n))
        #
        #
        # print("circut len: {}".format(len(circut)))
        # print(circut)
        # print("----------------------------------------------------")
    # print(circut)
    circut.append(location)

    # print("end")
    return circut


def h_init(vertex_list, all_connections, size):
    path = []
    path.append(1)
    return hamilton_cycle(vertex_list,all_connections, size, path)

def hamilton_cycle(vertex_list, all_connections, size, path):

    if len(path) == size:
        print("HERE")
        print(path[0])
        print(path[-1])
        print(vertex_list[path[-1]]["connections"])
        print("bot")

        if  path[0] in vertex_list[path[-1]]["connections"]:
            print("SUCCES")
            return path
        else:
            print(path)
            return "No answer"
    for value in vertex_list[path[-1]]["connections"]:
        if value not in path:
            print("value {}".format(value))
            new_path = copy.deepcopy(path)
            new_path.append(value)
            t = hamilton_cycle(vertex_list, all_connections, size, new_path)
            if isinstance(t, list):
                return t

    print(path)
    return "No anwer"



def dictcreator():
    data_set_algorithms = {}
    data_set_algorithms["Number_of_elements"] = []
    data_set_algorithms["Euler_cycle"] = []
    data_set_algorithms["Hamilton_cycle"] = []
    return data_set_algorithms

def data_input(begining, step, number_of_steps, dict_70, dict_30):

    for x in range(begining,(number_of_steps*step) + begining+1, step):

        vertex_list_30, all_connections_30 = graph_creator(x, 30)
        vertex_list_70, all_connections_70 = graph_creator(x, 70)

        vertex_list_30_2 = copy.deepcopy(vertex_list_30)
        all_connections_30_2 = copy.deepcopy(all_connections_30)

        vertex_list_70_2 = copy.deepcopy(vertex_list_70)
        all_connections_70_2 = copy.deepcopy(all_connections_70)

        # print("all_connections_30_2")
        # print(all_connections_30_2)


        dict_30["Number_of_elements"].append(x)
        dict_30["Euler_cycle"].append(timer(euler_path, vertex_list_30, all_connections_30, x))
        # print("allconections _30 po")
        # print(all_connections_30_2)
        # print(vertex_list_30_2)
        print("=============++++++++++++++++++++++++++++++++++++++++++++++++!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(all_connections_30_2)
        dict_30["Hamilton_cycle"].append(timer(h_init, vertex_list_30_2, all_connections_30_2, x))

        dict_70["Number_of_elements"].append(x)
        dict_70["Euler_cycle"].append(timer(euler_path, vertex_list_70, all_connections_70, x))
        dict_70["Hamilton_cycle"].append(timer(h_init, vertex_list_70_2, all_connections_70_2, x))





if __name__ == '__main__':

    dict1 = dictcreator()
    dict2  = dictcreator()

    data_input(6,2,15,dict1,dict2)
    list  = [dict1, dict2]
    SortingMethods = ["Saturation_30", "Saturation_70"]

    for i in range(0, 2):
        My_Dict = list[i]
        zd = zip(*My_Dict.values())
        with open(SortingMethods[i] + ".csv", 'w') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(My_Dict.keys())
            writer.writerows(zd)




