import os
import torch
import open3d as o3d

import remesh_cpp

from iso_remesh.Method.path import createFileFolder, removeFile


class Remesher:
    def __init__(self, mesh_file_path: str) -> None:
        self.mesh_file_path = mesh_file_path
        return

    @staticmethod
    def isoRemesh(
        mesh_file_path: str, save_mesh_file_path: str, overwrite: bool = False
    ) -> bool:
        if os.path.exists(save_mesh_file_path):
            if not overwrite:
                return True

            removeFile(save_mesh_file_path)

        createFileFolder(save_mesh_file_path)

        if mesh_file_path[-4:] != ".obj":
            obj_file_path = mesh_file_path[:-4] + "_tmp.obj"
        else:
            obj_file_path = mesh_file_path

        if not os.path.exists(obj_file_path):
            mesh = o3d.io.read_triangle_mesh(mesh_file_path)
            o3d.io.write_triangle_mesh(obj_file_path, mesh, write_ascii=True)

        if save_mesh_file_path[-4:] != ".obj":
            save_obj_file_path = save_mesh_file_path[:-4] + "_tmp.obj"
        else:
            save_obj_file_path = save_mesh_file_path

        remesh_cpp.isoRemeshing(obj_file_path, save_obj_file_path)

        if not os.path.exists(save_mesh_file_path):
            save_mesh = o3d.io.read_triangle_mesh(save_obj_file_path)
            o3d.io.write_triangle_mesh(save_mesh_file_path, save_mesh, write_ascii=True)

        removeFile(mesh_file_path[:-4] + "_tmp.obj")
        removeFile(save_mesh_file_path[:-4] + "_tmp.obj")
        return True
