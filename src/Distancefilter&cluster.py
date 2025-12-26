import os
import numpy as np
from scipy.spatial import cKDTree
import open3d as o3d
from sklearn.cluster import DBSCAN
import hdbscan


def load_point_cloud(path, name):
    print("Loading point cloud: ", name)
    file_path = os.path.join(path, name)

    if name.endswith('.txt'):
        # Load txt file using numpy
        point_cloud = np.loadtxt(file_path)[:, :3]
        labels = np.loadtxt(file_path)[:, -1]
    elif file_path.endswith('.ply'):
        # Load ply file using open3d and convert to numpy array
        point_cloud = o3d.io.read_point_cloud(file_path)
        point_cloud = np.asarray(point_cloud.points)[:, :3]
        labels = np.asarray(point_cloud)[:, -1]
    else:
        raise ValueError("Unsupported file format")

    return point_cloud, labels


# 计算两点之间的欧几里得距离
def distance(point1, point2):
    return np.linalg.norm(point1 - point2)


# Calculate the average distance
def calculate_average_distance(point_cloud):
    # Create KDTree
    tree = cKDTree(point_cloud)

    # 计算每个点到其最近邻点的距离
    distances, _ = tree.query(point_cloud, k=2)
    distances = distances[:, 1]
    # 计算平均距离
    average_distance = distances.mean()
    print("Threshold: ", average_distance)
    return average_distance


def filter_points_with_kdtree(A, B, threshold):
    # 构建B点云的KD树
    kdtree = cKDTree(A)
    print("removing the points......")

    # 批量查询KD树，而不是单点查询
    distances, _ = kdtree.query(B, k=4, distance_upper_bound=threshold)

    # 使用向量化操作选出满足条件的点
    mask = np.all(distances > threshold, axis=1)
    return B[mask]



def remove_noise_sor(point_cloud, nb=20, std=2.0):
    print("Removing noise using SOR filter......")

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(point_cloud)
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=nb, std_ratio=std)
    return pcd.select_by_index(ind)


def voxel_downsample(point_cloud, voxel_size):
    print("Downsampling the point cloud......")
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(point_cloud)
    downsampled_pcd = pcd.voxel_down_sample(voxel_size=voxel_size)
    return np.asarray(downsampled_pcd.points)


def cluster_points(point_cloud, eps, min_samples):
    print("Clustering the points......")
    # Apply DBSCAN clustering algorithm
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(point_cloud)
    return labels


def hscan(point_cloud, min_samples):
    print("Clustering the points with HDBSCAN......")
    cluster = hdbscan.HDBSCAN(min_cluster_size=min_samples, gen_min_span_tree=True)
    labels = cluster.fit(point_cloud)
    return labels.labels_


def get_branches(BP_path, AP_path, output_path):
    for filename in os.listdir(AP_path):
        file_path = os.path.join(BP_path, filename)
        if not os.path.isfile(file_path):
            # If the file does not exist, skip it
            print(f"File does not exist: {filename}. Skipping.")
            continue

        if filename.startswith("e"):  # Checks if the file is a .txt file
           
            A, Alabel = load_point_cloud(AP_path, filename)
            B, Blabel = load_point_cloud(BP_path, filename)

            # downsample the point cloud
            A, B = voxel_downsample(A, 0.001), voxel_downsample(B, 0.001)

            # # Remove noise using SOR filter
            A, B = np.asarray(remove_noise_sor(A).points), np.asarray(remove_noise_sor(B).points)
            x = '10'
            rmse = 0.009
            threshold = int(x) * rmse
            one_year_branches = filter_points_with_kdtree(A, B, threshold)

            # Cluster the points using DBSCAN
            # labels = cluster_points(one_year_branches, eps=0.03, min_samples=35)
            # Add the labels to the point cloud
            # one_year_branches = np.column_stack((one_year_branches, labels))

            # Save the results
            output_file = os.path.join(output_path,  x + filename)
            np.savetxt(output_file, one_year_branches, fmt='%.8f')


def cluster_branch(input_path, output_path):
    for filename in os.listdir(input_path):
        if filename.startswith("10"):  # Checks if the file is a .txt file
            one_year_branches, label = load_point_cloud(input_path, filename)

            one_year_branches = voxel_downsample(one_year_branches, 0.001)
            ave = calculate_average_distance(one_year_branches)
            threshold = 12 * ave

            # Cluster the points using DBSCAN
            labels = cluster_points(one_year_branches, eps=threshold, min_samples=40)

            # Or HDBSCAN
            # labels = hscan(one_year_branches, 10)

            # Add the labels to the point cloud
            one_year_branches = np.column_stack((one_year_branches, labels))
            one_year_branches = one_year_branches[one_year_branches[:, -1] != -1]

            # Save the results
            output_file = os.path.join(output_path, filename[:-4] + "clustered.txt")
            np.savetxt(output_file, one_year_branches, fmt='%.8f')


def get_branche(BP_path, AP_path, output_path):
    for filename in os.listdir(AP_path):
        file_path = os.path.join(BP_path, filename)
        if not os.path.isfile(file_path):
            # If the file does not exist, skip it
            print(f"File does not exist: {filename}. Skipping.")
            continue

        if filename.endswith("txt"):  # Checks if the file is a .txt file

            A, Alabel = load_point_cloud(AP_path, filename)
            B, Blabel = load_point_cloud(BP_path, filename)

            # downsample the point cloud
            A, B = voxel_downsample(A, 0.001), voxel_downsample(B, 0.001)

            # # Remove noise using SOR filter
            A, B = np.asarray(remove_noise_sor(A).points), np.asarray(remove_noise_sor(B).points)
            x = '2'
            rmse = 0.009
            threshold = int(x) * rmse
            one_year_branches = filter_points_with_kdtree(A, B, threshold)

            # Cluster the points using DBSCAN
            labels = cluster_points(one_year_branches, eps=threshold, min_samples=40)

            # Add the labels to the point cloud
            one_year_branches = np.column_stack((one_year_branches, labels))

            # Save the results
            output_file = os.path.join(output_path, x + filename)
            np.savetxt(output_file, one_year_branches, fmt='%.8f')

# Get the branche
BP_path = "/Users/dylan/PCD/Temporal/2024AP"  # Path to the folder with BP files
AP_path = "/Users/dylan/PCD/Temporal/2025"  # Path to the folder with growth files
output_path = "/Users/dylan/PCD/Temporal/" # Path for saving output
get_branche(BP_path, AP_path, output_path)

# # Cluster the branches
# input_path = '/Users/dylan/PCD/Seg/branch/'
# output_path = '/Users/dylan/PCD/Seg/branch/'
# cluster_branch(input_path, output_path)
