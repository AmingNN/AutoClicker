# @Time      :2026/2/21 下午2:11
# @Author    :Aming
import os
import shutil
import tomllib
import PyInstaller.__main__

with open("pyproject.toml", "rb") as f:
    project = tomllib.load(f).get("project", {})
    name = project.get("name", "AutoClicker")
    version = project.get("version", "0.1.0")

project_dir = os.path.dirname(os.path.abspath(__file__))
dist_dir = os.path.join(project_dir, 'dist')
app_name = name + "-v" + version
contents_name = "lib"
contents_dir = os.path.join(dist_dir, app_name, contents_name)

def run_build():
    # 确保在当前脚本所在目录执行
    os.chdir(project_dir)

    params = [
        'main.py',              # 你的主程序文件名
        '--noconfirm',          # 覆盖旧文件
        '--clean',              # 清理缓存
        '--windowed',           # GUI模式，不显示黑框
        # '--onedir',             # 文件模式 --onefile  --onedir
        '--log-level=INFO',     # 日志等级
        f'--name={app_name}',           # 应用名称
        '--icon=assets/app.ico',        # 应用图标
        # '--add-data=assets:./assets',     # 数据文件
        # '--add-data=view/styles.qss:./view',
        '--contents-directory', 'lib',  # 将 _internal 改名为 lib
    ]

    PyInstaller.__main__.run(params)


def move_data_path(names=["assets", "view"]):
    """从 ./lib/ 移动到 ./ (基于 .exe 所在目录)"""

    for name in names:
        source = os.path.join(contents_dir, name)
        target = os.path.join(dist_dir, app_name, name)

        # 1. 检查源文件/文件夹是否存在
        if not os.path.exists(source):
            print(f"⚠️ 跳过: {name} 未在 lib 中找到")
            continue

        # 2. 清理目标位置（防止 move 失败）
        if os.path.exists(target):
            if os.path.isdir(target):
                shutil.rmtree(target)
            else:
                os.remove(target)

        # 3. 执行移动
        shutil.move(source, target)
        print(f"✅ 已外置资源: {name}")


if __name__ == "__main__":
    run_build()
    # move_data_path()

