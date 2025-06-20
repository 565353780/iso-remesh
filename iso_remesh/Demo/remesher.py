import open3d as o3d

from iso_remesh.Module.remesher import Remesher


def demo():
    mesh_file_path = "/Users/chli/chLi/Dataset/Objaverse_82K/trimesh/000-000/000a00944e294f7a94f95d420fdd45eb.obj"

    mesh = o3d.io.read_triangle_mesh(mesh_file_path)

    remesher = Remesher(mesh)

    remesher.isotropic_remeshing(
        0.14,
        iter=1,
        explicit=False,
        foldover=10,
        sliver=True,
    )

    return True
