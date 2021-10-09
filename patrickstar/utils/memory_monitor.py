# Copyright (C) 2021 THL A29 Limited, a Tencent company.
# All rights reserved.
# Licensed under the BSD 3-Clause License (the "License"); you may
# not use this file except in compliance with the License. You may
# obtain a copy of the License at
# https://opensource.org/licenses/BSD-3-Clause
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
# See the AUTHORS file for names of contributors.

import gc

import psutil
import torch

from .distributed import get_rank, get_world_size


def get_sys_memory_used(device):
    """
    Get the free memory info of device.
    Notice that for CPU, this function will return 1/N of the total free memory,
    where N is the world size.
    """
    if device.type == "cuda":
        return torch.cuda.memory_allocated()
    elif device.type == "cpu":
        vm_stats = psutil.virtual_memory()
        return vm_stats.used / get_world_size()


def see_memory_usage(message, force=False, scale_name="MB"):
    if not force:
        return
    if not get_rank() == 0:
        return

    # python doesn't do real-time garbage collection so do it explicitly to get the correct RAM reports
    gc.collect()

    if scale_name == "MB":
        scale = 1024 * 1024
    elif scale_name == "B":
        scale = 1
    # Print message except when distributed but not rank 0
    print(message)
    print(
        f"MA {round(torch.cuda.memory_allocated() / scale, 2)} {scale_name} \
        Max_MA {round(torch.cuda.max_memory_allocated() / scale, 2)} {scale_name} \
        CA {round(torch.cuda.memory_reserved() / scale, 2)} {scale_name} \
        Max_CA {round(torch.cuda.max_memory_reserved() / scale)} {scale_name} "
    )

    vm_stats = psutil.virtual_memory()
    used_gb = round(((vm_stats.total - vm_stats.available) / (1024 ** 3)), 2)
    print(f"CPU Virtual Memory: used = {used_gb} GB, percent = {vm_stats.percent}%")

    # get the peak memory to report correct data, so reset the counter for the next call
    if hasattr(torch.cuda, "reset_peak_memory_stats"):  # pytorch 1.4+
        torch.cuda.reset_peak_memory_stats()
