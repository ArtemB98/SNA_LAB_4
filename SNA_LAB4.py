import numpy
import vk_api
import time
import networkx as nx
import matplotlib.pyplot as plt

user1 = ???

def make_graph(friends_out, friends_friends):
    graph = nx.Graph()
    graph.add_node(user1, size=friends_out[user1]['count'])
    for i in friends_out[user1]['items']:
        try:
            graph.add_node(i, size=friends_friends[i]['count'])
            intersection = set(friends_out[user1]['items']).intersection(set(friends_friends[i]['items']))
            graph.add_edge(user1, i, weight=len(intersection))
        except Exception:
            print("err")
    for i in range(len(friends_out[user1]['items'])):
        id1 = friends_out[user1]['items'][i]
        for k in range(i + 1,
                       len(friends_out[user1]['items'])):
            id2 = friends_out[user1]['items'][k]
            try:
                intersection = set(friends_friends[id1]['items']).intersection(set(friends_friends[id2]['items']))
                if len(intersection) > 0:
                    graph.add_edge(id1, id2,
                                   weight=len(intersection))

            except Exception:
                print("err friend")
    return graph


def plot_graph(graph, adjust_nodesize):
    # pos = nx.drawing.layout.circular_layout(graph)
    pos = nx.spring_layout(graph, k=0.1)
    # нормализуем размер вершины для визуализации. Оптимальное значение параметра
    # adjust_nodesize ‐ от 300 до 500
    nodesize = [graph.nodes.get(i)['size'] / adjust_nodesize for i in graph.nodes()]
    # нормализуем толщину ребра графа. Здесь хорошо  подходит
    # нормализация по Standard Score
    edge_mean = numpy.mean([graph.get_edge_data(i[0], i[1])['weight'] for i in graph.edges()])

    edge_std_dev = numpy.std([graph.get_edge_data(i[0], i[1])['weight'] for i in graph.edges()])
    edgewidth = ([graph.get_edge_data(i[0], i[1])['weight'] for i in graph.edges()] - edge_mean) / edge_std_dev / 2
    # создаем граф для визуализации
    nx.draw_networkx_nodes(graph,
                           pos, node_size=nodesize, node_color='y', alpha=0.9)

    nx.draw_networkx_edges(graph, pos, width=edgewidth, edge_color='b')
    nx.draw_networkx_labels(graph, pos, font_size=5)
    # сохраняем и показываем визуализированный граф
    plt.savefig('saved')
    plt.show()


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта
функция.
    """
    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True ‐ сохранить, False ‐ не сохранять.
    remember_device = True
    return key, remember_device


def stop_f(items):
    print(items)


def get_groups_users(friends_list, tools):
    friends_out = {}
    for friend in friends_list:
        try:
            friends_out[friend] = tools.get_all('friends.get', 100, {'user_id': friend})
        except Exception:
            friends_out[friend] = []
        time.sleep(1)
    return friends_out


def main():
    login, password = '', ''
    vk_session = vk_api.VkApi(
        login, password,
        auth_handler=auth_handler)  # функция для  обработки двухфакторной аутентификации)
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)

    tools = vk_api.VkTools(vk_session)
    friend_list = []
    friend_list.append(user1)
    friends_out = get_groups_users(friend_list, tools)
    print(friends_out)

    friend_friends = get_groups_users(friends_out[user1]['items'], tools)
    # with open('friends_friends.pkl', 'wb') as output:
    #     pickle.dump(friend_friends, output,
    #                 pickle.HIGHEST_PROTOCOL)
    # with open('friends_friends.pkl', 'rb') as input:
    #     friends_friends = pickle.load(input)
    g = make_graph(friends_out, friend_friends)
    plot_graph(g, 500)


if __name__ == '__main__':
    main()
