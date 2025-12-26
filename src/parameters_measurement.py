import numpy as np
import open3d as o3d
import os
import pandas as pd
import math
import traceback
from scipy.spatial import ConvexHull
from scipy.interpolate import splprep, splev


def load_point_cloud(path, name):
    print("Loading point cloud: ", name)
    file_path = path + name

    if name.endswith('txt'):
        # Load txt file using numpy
        point_cloud = np.loadtxt(file_path)[:, :4]
        labels = np.unique(np.loadtxt(file_path)[:, -1])
    elif file_path.endswith('.ply' or '.pcd'):
        # Load ply file using open3d and convert to numpy array
        point_cloud = o3d.io.read_point_cloud(file_path)
        point_cloud = np.asarray(point_cloud.points)[:, :4]
        labels = np.unique(np.asarray(point_cloud)[:, -2])
    else:
        raise ValueError("Unsupported file format")

    return point_cloud, labels

# def skeletonize_point_cloud(points):
#     from pc_skeletor import skeletor
#
#     pcd = o3d.geometry.PointCloud()
#     pcd.points = o3d.utility.Vector3dVector(points[:, [0, 1, 2]])
#
#     num_points = len(points)
#     if num_points < 30:
#         return pcd, pcd
#
#     n_neighbors = min(30, num_points - 1)
#     skeletor = skeletor.Skeletonizer(point_cloud=pcd, down_sample=0.003, debug=False)
#     laplacian_config = {
#         "MAX_LAPLACE_CONTRACTION_WEIGHT": 1024,
#         "MAX_POSITIONAL_WEIGHT": 10240,
#         "INIT_LAPLACIAN_SCALE": 100,
#         "N_NEIGHBORS": n_neighbors
#     }
#
#     try:
#         skeleton, graph = skeletor.extract(method='Laplacian', config=laplacian_config)
#     except RuntimeError as e:
#         print(f"Encountered an error: {str(e)}")
#         n_neighbors = min(10, num_points - 1)
#         laplacian_config['N_NEIGHBORS'] = n_neighbors
#
#         try:
#             skeleton, graph = skeletor.extract(method='Laplacian', config=laplacian_config)
#         except RuntimeError as e:
#             print("Failed again, skipping this point cloud.")
#             print(f"Full error message: {traceback.format_exc()}")
#             return pcd, pcd
#
#     return skeleton, graph

def distance(point1, point2):
    """Calculate Euclidean distance between two points"""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)

def calculate_path_length(points):
    """Calculate total distance by traversing points based on nearest point method"""
    if not points:
        return 0

    total_length = 0
    current_point = points.pop(0)  # Start with the first point
    while points:
        closest_point = min(points, key=lambda p: distance(current_point, p))
        total_length += distance(current_point, closest_point)
        current_point = closest_point
        points.remove(closest_point)
    return total_length

# def cal_length(pcd, labels):
#     """Calculate length for each label"""
#     groups_length = []
#     total_length = 0
#
#     for label in labels:
#         if label in [-1]:
#             continue
#         print("Lengthing label: ", label)
#         point_label = pcd[pcd[:, -1] == label]
#
#         skeleton, graph = skeletonize_point_cloud(point_label)
#         list_skeleton = np.array(skeleton.points).tolist()
#
#         group_length = calculate_path_length(list_skeleton)
#         groups_length.append(group_length)
#         total_length += group_length
#
#     return groups_length,total_length

def cal_angle(point, labels):
    """Calculate angles for each label"""
    z_axis = np.array([0, 0, 1])
    angles = []
    lengths = []
    total_length = 0
    total_angle = 0

    for label in labels:
        if label in [-1]:
            continue
        print("Processing label: ", label)
        point_label = point[point[:, -1] == label]
        if len(point_label) < 5:
            continue

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(point_label[:, :3])

        # Compute the oriented bounding box and length
        obb = pcd.get_oriented_bounding_box()
        obb_lengths = obb.extent
        obb_length_max = max(obb_lengths)

        # Calculate the angle between the major axis and the xy plane
        main_direction = obb.R[:, 0]  # Major axis direction
        xy_projection = np.array([main_direction[0], main_direction[1], 0])
        cos_theta = np.dot(main_direction, xy_projection) / (np.linalg.norm(main_direction) * np.linalg.norm(xy_projection))
        angle = np.arccos(cos_theta)

        angle_in_degrees = np.degrees(angle)
        angles.append(angle_in_degrees)
        lengths.append(obb_length_max)
        total_length += obb_length_max
        total_angle += angle_in_degrees

    return angles, lengths, total_angle, total_length

if __name__ == '__main__':
    path = "/Users/dylan/PCD/2023-2024/2023 New&Pruned/"

    # 用于保存总长度的文件
    data = []

    with open(os.path.join(path, 'paras/parameters.json'), 'w') as file:
        for filename in os.listdir(path):
            if filename.endswith('txt'):
                points, labels = load_point_cloud(path, filename)
                angles, lengths, total_angle, total_length = cal_angle(points, labels)
                # lengths, total_length = cal_length(points, labels)

                # 将总长度写入文件
                file.write(f"{filename[:-4]} ,{len(lengths)}, {total_length}, {total_angle}\n")

                # 将每个label的长度和角度存入data列表
                for i in range(len(lengths)):
                    data.append({
                        'Filename': filename[:-4] + "-" + str(i),
                        'Box_Length': lengths[i],
                        'Angle': angles[i]
                    })

    # 将data列表转换为DataFrame
    df = pd.DataFrame(data)
    # 保存DataFrame到Excel文件
    df.to_excel(os.path.join(path, 'paras/len&angle.xlsx'), index=False)

