from iso_remesh.Module.remesher import Remesher


def demo():
    mesh_file_path = "/Users/chli/chLi/Dataset/Objaverse_82K/trimesh/000-000/000a00944e294f7a94f95d420fdd45eb.obj"
    iso_mesh_file_path = "/Users/chli/chLi/Dataset/Objaverse_82K/iso_mesh/000-000/000a00944e294f7a94f95d420fdd45eb.obj"

    # mesh_file_path = "/Users/chli/chLi/Dataset/vae-eval/mesh/002.obj"
    # iso_mesh_file_path = "/Users/chli/chLi/Dataset/vae-eval/iso_mesh/002.obj"

    edge_length_scale = 0.5
    iter_num = 3
    overwrite = True

    Remesher.isoRemesh(
        mesh_file_path,
        iso_mesh_file_path,
        edge_length_scale,
        iter_num,
        overwrite,
    )
    return True
