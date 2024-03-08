// All included firmware files are
// INTEL CORPORATION PROPRIETARY INFORMATION
// Copyright(c) 2019 Intel Corporation. All Rights Reserved
const int fw_D4XX_FW_Image_version[4] = {5,15,1,0};
#ifndef _MSC_VER
__asm__(
    "#version 20d1cf628957941689a948f2e17ecc6a11e8ab01\n"
#ifdef __APPLE__
    ".const_data\n"
#define _ "_"
#else
    ".section .rodata\n"
#define _ ""
#endif
    ".global "_"fw_D4XX_FW_Image_data\n"
    _"fw_D4XX_FW_Image_data:\n"
    ".incbin \"/home/mihkel/School/ThesisPractical/librealsense/build/common/fw/D4XX_FW_Image-5.15.1.0.bin\"\n"
    ".global "_"fw_D4XX_FW_Image_size\n"
    _"fw_D4XX_FW_Image_size:\n"
    "1:\n"
    ".int 1b - "_"fw_D4XX_FW_Image_data\n"
    ".previous"
);
#undef _
#endif
