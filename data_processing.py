# data_processing.py

def generate_commands(matrix):
    """
    将 5x4 输入矩阵转换为字符串命令列表
    每行格式为 PINn:R,G,B
    """
    commands = []
    for row in matrix:
        zone, red, green, blue = row
        r = 255 if red else 0
        g = 255 if green else 0
        b = 255 if blue else 0
        cmd = f"PIN{zone + 7}:{r},{g},{b}"
        commands.append(cmd)
    return commands

def generate_shutdown_commands(input_matrix):
    # 生成所有区域关闭LED的命令
    shutdown_matrix = [[row[0], 0, 0, 0] for row in input_matrix]
    return generate_commands(shutdown_matrix)
