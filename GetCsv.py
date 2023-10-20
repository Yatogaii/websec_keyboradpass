import csv

def  generateCSV():
    # 处理 csdn 文件
    with open("datas/www.csdn.net.sql", 'r', encoding='ISO-8859-1', errors='ignore') as f:
        data = []
        # csdn 文件里面每一行格式都一样
        for line in f.readlines():
            parts = line.strip().split(' # ')
            if len(parts) == 3:  # 确保每行有三个部分
                parts[1] = str(parts[1])  # 强制将第二列数据转换为字符串
                data.append(parts)

        # 排序
        sorted_data = sorted(data, key=lambda x: str(x[1]))

        # 写入
        with open('datas/csdn.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # 写入CSV文件的标题行
            writer.writerow(['Username', 'Password', 'Email'])

            # 写入排序后的数据
            for row in sorted_data:
                row[1] = "\'" + row[1] + "\'"
                writer.writerow(row)

    # 处理 yahoo
    with open("datas/plaintxt_yahoo.txt", 'r', encoding='ISO-8859-1') as f:
        data = []
        for line in f.readlines():
            parts = line.strip().split(':', 2)
            if len(parts) == 3:  # 确保每行有三个部分
                parts[1] = str(parts[1])  # 强制将第二列数据转换为字符串
                data.append(parts)
            else:
                print(line)

        # 排序
        sorted_data = sorted(data, key=lambda x: str(x[2]))

        # 写入
        with open('datas/yahoo.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # 写入CSV文件的标题行
            writer.writerow(['Email', 'Password'])

            # 写入排序后的数据
            for row in sorted_data:
                row = row[1:]
                if row[1] == '':
                    continue
                row[1] = "\'" + row[1] + "\'"
                writer.writerow(row)


    # 处理 yahoo 文件

if __name__ == '__main__':
    generateCSV()
