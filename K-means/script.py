from random import randint


class ProgramSettings:
    k = -1
    file_path = ''
    data_len = -1


class Record:
    name = ''
    data = []
    cluster = -1

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name} : {self.data}'

    def __repr__(self):
        return self.__str__()


def set_cluster(rec):
    rec.cluster = randint(1, ProgramSettings.k)


def are_dict_similar(dict1, dict2):
    keys1 = dict1.keys()
    if keys1 != dict2.keys():
        return False
    for key in keys1:
        if (dict1[key]) != (dict2[key]):
            return False

    return True


def to_cluster_dict(data):
    cluster_dicta = {}
    for rec in data:
        cluster_dicta.setdefault(rec.cluster, []).append(rec)
    return cluster_dicta


def arithmetic_mean(data):
    return sum(data) / len(data)


def find_distance(point1, point2):
    distance = 0
    for i in range(len(point1)):
        distance += (point1[i] - point2[i]) ** 2
    return distance ** 0.5


def find_centroids(cluster_dicta):
    cluster_dicta = dict(cluster_dicta)
    centroid_dict = {}
    for key, rec_list in cluster_dicta.items():
        centroid = [sum(val.data[i] for val in rec_list) / len(rec_list) for i in range(ProgramSettings.data_len)]
        centroid_dict[key] = centroid
    return centroid_dict


def get_distances_from_cluster_centroids(data, centr_dict):
    return sum(find_distance(rec.data, centr_dict[rec.cluster]) for rec in data)


def change_clusters(recs, centroid_dict):
    centroid_dict = dict(centroid_dict)
    for rec in recs:
        distances = {}
        for key, centroid in centroid_dict.items():
            distance = find_distance(rec.data, centroid)
            distances[key] = distance
        rec.cluster = min(distances, key=distances.get)


def find_purity(data):
    data = list(data)
    names = set([rec.name for rec in data])
    result = {}
    k = 1
    while k <= ProgramSettings.k:
        result[k] = {}
        for name in list(names):
            try:
                percent = len([rec for rec in data if rec.name == name and rec.cluster == k]) / len(
                    [rec for rec in data if rec.cluster == k])
            except:
                percent = 0

            result[k][name] = round(percent * 100) / 100
        k += 1
    return result


def print_purity(purity):
    purity = dict(purity)
    for k, value in purity.items():
        print(f'Purity cluster {k}: {value}')


ProgramSettings.file_path = 'iris_kmeans.txt'
ProgramSettings.k = 3
records = []
with open(ProgramSettings.file_path, 'r') as file:
    for line in file:
        line = line.strip()
        split_line = line.split(',')
        record = Record(split_line[-1])
        record.data = [float(x) for x in split_line[:-1]]
        ProgramSettings.data_len = len(record.data)
        set_cluster(record)
        records.append(record)

prev_dict = to_cluster_dict(records)
centroids = find_centroids(prev_dict)
iters = 0
# change_clusters(records, centroids)
# print('sumę odległości : ', get_distances_from_cluster_centroids(records,centroids))
next_dict = to_cluster_dict(records)
while not are_dict_similar(prev_dict, next_dict) or iters == 0:
    iters += 1
    centroids = find_centroids(next_dict)
    change_clusters(records, centroids)
    print('iteracja : ', iters)
    print('sumę odległości : ', get_distances_from_cluster_centroids(records, centroids))
    print_purity(find_purity(records))
    prev_dict, next_dict = next_dict, to_cluster_dict(records)
print('\n' ,'after algo', '\n')
print('sumę odległości : ', get_distances_from_cluster_centroids(records, centroids))
print_purity(find_purity(records))

