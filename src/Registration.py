import os
import open3d as o3d
import numpy as np
from simpleicp import PointCloud, SimpleICP


def load_point_cloud(path, name):
    print("Loading point cloud: ", name)
    file_path = os.path.join(path, name)

    if name.lower().endswith('.txt'):
        # Load txt file using numpy
        point_cloud = np.loadtxt(file_path)[:, :3]
    elif file_path.lower().endswith(('.ply', '.pcd')):
        # Load ply file using open3d and convert to numpy array
        point_cloud = o3d.io.read_point_cloud(file_path)
        point_cloud = np.asarray(point_cloud.points)[:, :3]
    else:
        raise ValueError("Unsupported file format")

    return point_cloud


def array2o3d(array):
    # 检查数组是否为空
    if array.size == 0:
        raise ValueError("Input array is empty.")

    # 检查维度是否为 (N, 3)
    if array.ndim != 2 or array.shape[1] != 3:
        raise ValueError(f"Expected shape (N, 3), got {array.shape}")

    # 检查数据类型是否为浮点型
    if not np.issubdtype(array.dtype, np.floating):
        raise ValueError(f"Expected float dtype, got {array.dtype}")

    # 检查是否存在 NaN 或 Inf
    if np.isnan(array).any() or np.isinf(array).any():
        raise ValueError("Array contains NaN/Inf values.")

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(array)
    return pcd


def downsample(point_cloud, voxel_size):
    try:
        pcd = array2o3d(point_cloud)
    except ValueError as e:
        print(f"Invalid input: {e}")
        return point_cloud  # 返回原始数据或抛出异常

    downsampled = pcd.uniform_down_sample(every_k_points=int(1/voxel_size))

    # 检查下采样后是否为空
    if len(downsampled.points) == 0:
        print(f"Warning: Downsampled point cloud is empty. Using original points.")
        return point_cloud  # 返回原始数据或调整 voxel_size

    print(f"Downsampled to {len(downsampled.points)} points")
    return np.asarray(downsampled.points)


def sor(point_cloud, nb_neighbors, std_ratio):
    print("Removing noise using SOR filter......")
    pcd = array2o3d(point_cloud)
    print(">> SOR filter")
    # Create the SOR filter
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)
    # Apply the filter and return the inlier cloud
    return np.asarray(pcd.select_by_index(ind).points)


def get_trunk(points, maxi, mini):
    if points.size == 0:
        raise ValueError("get_trunk: input point cloud is empty.")

    slice_thickness = 0.05
    overlap_ratio = 0.8

    z_min, z_max = np.min(points[:, 2]), np.max(points[:, 2])
    if z_max - z_min < 1e-6:
        raise ValueError("get_trunk: z-range is too small, cannot slice.")

    step = slice_thickness * (1 - overlap_ratio)
    z_slices = np.arange(z_min, z_max + 1e-6, step)

    non_empty_slices = []
    for z in z_slices:
        mask = (points[:, 2] >= z) & (points[:, 2] < z + slice_thickness)
        slice_points = points[mask]
        if slice_points.size > 0:
            non_empty_slices.append(slice_points)

    if len(non_empty_slices) == 0:
        raise ValueError("get_trunk: all slices are empty.")

    bottom_slice = non_empty_slices[0]
    x_range = np.max(bottom_slice[:, 0]) - np.min(bottom_slice[:, 0])
    y_range = np.max(bottom_slice[:, 1]) - np.min(bottom_slice[:, 1])
    bottom_xyz = (np.max(bottom_slice[:, 0]),
                  np.max(bottom_slice[:, 1]),
                  np.min(bottom_slice[:, 2]))

    max_z_keep = None
    for s in non_empty_slices:
        slice_x_range = np.max(s[:, 0]) - np.min(s[:, 0])
        slice_y_range = np.max(s[:, 1]) - np.min(s[:, 1])

        # 超过一定扩展幅度就认为进入枝条区，停止
        if ((slice_x_range - x_range < maxi and slice_x_range - x_range > mini) or
            (slice_y_range - y_range < maxi and slice_y_range - y_range > mini)):
            break

        max_z_keep = np.max(s[:, 2])

    if max_z_keep is None:
        # 说明 trunk 很短，只保留底层
        filtered_points = bottom_slice
    else:
        mask_trunk = points[:, 2] <= max_z_keep + slice_thickness
        filtered_points = points[mask_trunk]

    return np.array(bottom_xyz), filtered_points


def find_nearest_neighbors(source_pc, target_pc):
    target_tree = o3d.geometry.KDTreeFlann(target_pc)
    nearest_neighbors = []
    for point in source_pc.points:
        _, idx, _ = target_tree.search_knn_vector_3d(point, 1)
        nearest_neighbors.append(target_pc.points[idx[0]])
    return np.asarray(nearest_neighbors)


def compute_centroids(source_points, nearest_neighbors):
    source_centroid = np.mean(source_points, axis=0)
    target_centroid = np.mean(nearest_neighbors, axis=0)
    return source_centroid, target_centroid


def compute_z_rotation(source_points, nearest_neighbors, source_centroid, target_centroid):
    source_centered = source_points - source_centroid
    target_centered = nearest_neighbors - target_centroid

    H = source_centered.T @ target_centered
    U, _, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T

    if np.linalg.det(R) < 0:
        Vt[2, :] *= -1
        R = Vt.T @ U.T

    return R


def transform_by_H(X: np.ndarray, H: np.ndarray) -> np.ndarray:
    """Transform points by applying a homogeneous transformation matrix H.

    Args:
        X (np.array): Point cloud data as a numpy array of shape (n, 3).
        H (np.array): Homogeneous transformation matrix H of shape (4, 4).

    Returns:
        np.array: Transformed point cloud data.
    """
    # 将欧拉坐标转换为齐次坐标
    n = X.shape[0]
    ones = np.ones((n, 1))
    Xh = np.hstack((X, ones))

    # 应用齐次变换矩阵H
    Xh = (H @ Xh.T).T  # transform in-place to save memory

    # 将变换后的齐次坐标转换回欧拉坐标
    Xe = Xh[:, :3] / Xh[:, 3][:, np.newaxis]

    return Xe


def show2pcd(A: np.ndarray, B: np.ndarray, name):

    A_pcd = array2o3d(A)
    A_pcd.paint_uniform_color([0, 0, 1])
    B_pcd = array2o3d(B)
    B_pcd.paint_uniform_color([1, 0, 0])

    o3d.visualization.draw_geometries([A_pcd, B_pcd], window_name = name)


def align_tree(AP, BP, out_path):
    for filename in os.listdir(AP):
        file_path = os.path.join(BP, filename)
        if not os.path.isfile(file_path):
            # If the file does not exist, skip it
            print(f"File does not exist: {filename}. Skipping.")
            continue

        if filename.endswith("txt"):
            # get the tree and show
            A_tree = load_point_cloud(AP, filename)
            B_tree = load_point_cloud(BP, filename)
            print(f"A_tree shape: {A_tree.shape}, B_tree shape: {B_tree.shape}")
            # show2pcd(A_tree, B_tree, name = "Origin Trees")

            A_tree = sor(A_tree,10,5), 0.001
            B_tree = sor(B_tree,10,5), 0.001
            # Extract the trunk of the tree
            
            A_xyz, A_trunk = get_trunk(A_tree, 0.2, 0.03)
            B_xyz, B_trunk = get_trunk(B_tree, 0.2, 0.03)
            
            # Apply the first alignment on trunk and show
            t = A_xyz - B_xyz
            B_trunk = sor(B_trunk + t,20,3)
            A_trunk = sor(A_trunk,20,3)            
            show2pcd(A_trunk, B_trunk, name = "1st aligned Trunks")

            # Create point cloud objects
            A = PointCloud(A_trunk, columns=["x", "y", "z"])
            B = PointCloud(B_trunk, columns=["x", "y", "z"])

            icp = SimpleICP()
            icp.add_point_clouds(A, B)

            H, B_moved, rigid_body_transformation_params, distance_residuals = icp.run(correspondences = 2000, min_change = 0.001, max_iterations = 100)

            print(H.shape)

            show2pcd(A_trunk, B_moved, name = "ICPed Trunks")

            # Apply the transformation to the whole tree
            moved_B_tree = transform_by_H((B_tree + t), H)

            np.savetxt(f"{out_path}moved_{filename}", moved_B_tree, fmt = "%.8f")
            show2pcd(A_tree, moved_B_tree, name = "ICPed Trees")


if __name__ == "__main__":

    # Path to point cloud files
    path_a = "/Users/dylan/PCD/After prun/"
    path_b = '/Users/dylan/PCD/Before prun/'
    out_path = '/Users/dylan/PCD/'

    align_tree(path_a, path_b, out_path)
    

    # Save the aligned point clouds
    # o3d.io.write_point_cloud("F:/PointCloud/moved_A_tree.pcd", A_tree_pcd)
