# data_processing.py

def generate_commands(matrix):
    """
    将 5x4 输入矩阵转换为字符串命令列表
    每行格式为 PINn:R,G,B
    """
    commands = []
    for row in matrix:
        zone, blue, yellow, red = row
        r = 255 if red else 0
        g = 255 if yellow else 0
        b = 255 if blue else 0
        cmd = f"PIN{zone + 6}:{r},{g},{b}"
        commands.append(cmd)
    return commands