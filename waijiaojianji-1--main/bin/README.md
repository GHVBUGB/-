# 二进制文件目录

此目录用于存放项目所需的二进制文件。

## FFmpeg 安装说明

请将 `ffmpeg.exe` 和 `ffprobe.exe` 文件放置在此目录中。

### 下载 FFmpeg

1. 访问 [FFmpeg 官网](https://ffmpeg.org/download.html)
2. 下载 Windows 版本的 FFmpeg
3. 解压后将 `bin` 目录中的 `ffmpeg.exe` 和 `ffprobe.exe` 复制到此目录

### 文件结构

```
bin/
├── ffmpeg.exe
├── ffprobe.exe
└── README.md (此文件)
```

项目会自动使用此目录中的 FFmpeg 二进制文件。