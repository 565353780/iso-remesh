#pragma once

#include <string>

void adaptiveIsoRemeshing(const std::string &mesh_file_path,
                          const std::string &save_mesh_file_path,
                          const float &edge_length_scale = 0.5,
                          const int &iter_num = 3);
