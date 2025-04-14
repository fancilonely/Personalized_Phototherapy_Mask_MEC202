# data_processing.py
import csv

def read_matrix_from_csv(file_path):
    """
    读取CSV文件并转化为光疗输入矩阵（List[List[int]]）
    忽略标题行，确保每行为 zone, red, green, blue 四列
    """
    matrix = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过表头
        for row in reader:
            if len(row) != 4:
                continue  # 跳过异常行
            try:
                zone_data = [int(val) for val in row]
                matrix.append(zone_data)
            except ValueError:
                continue  # 跳过包含非数字的行
    return matrix

def split_matrix_dynamically(matrix):
    """
    将输入矩阵拆分成多轮，每轮不重复颜色（每个区域每轮最多亮一个灯）
    如果某区域RGB都为1，将在多个轮次中依次处理（默认优先级 R > G > B）
    """
    rounds = []

    # 将每个区域的RGB信息变成一个任务队列
    zone_tasks = []
    for row in matrix:
        zone, r, g, b = row
        task = {
            "zone": zone,
            "colors": []
        }
        if r:
            task["colors"].append("R")
        if g:
            task["colors"].append("G")
        if b:
            task["colors"].append("B")
        if task["colors"]:
            zone_tasks.append(task)

    # 按轮次调度
    while any(task["colors"] for task in zone_tasks):
        current_round = []
        for task in zone_tasks:
            if task["colors"]:
                color = task["colors"].pop(0)  # 每次拿一个颜色（FIFO）
                if color == "R":
                    current_round.append([task["zone"], 1, 0, 0])
                elif color == "G":
                    current_round.append([task["zone"], 0, 1, 0])
                elif color == "B":
                    current_round.append([task["zone"], 0, 0, 1])
        if current_round:
            rounds.append(current_round)

    return rounds


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
        cmd = f"PIN{zone + 6}:{r},{g},{b}"
        commands.append(cmd)
    return commands

def generate_shutdown_commands(input_matrix):
    # 生成所有区域关闭LED的命令
    shutdown_matrix = [[row[0], 0, 0, 0] for row in input_matrix]
    return generate_commands(shutdown_matrix)
