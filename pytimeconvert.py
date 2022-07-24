import math

# サンプルデータの時刻が、サンプルテーブルの時間内であれば、何番目であるかを付加して変換

# 場所と付番
def judge(dic):
    resultdic = {}

    for timevalue in listdata:
        for tablevalue in table:

            # 時間範囲内判定
            if tablevalue[0] <= timevalue <= tablevalue[1]:
                place = tablevalue[2]
                if place in resultdic:
                    resultdic[place] += 1
                else:
                    resultdic[place] = 1

                if dic != None:
                    # 何桁のゼロ埋めか判定
                    intzfill = int(math.log10(dic[place])) + 1
                    print(
                        timevalue,
                        "{place}_{num}".format(
                            place=tablevalue[2],
                            num=str(resultdic[place]).zfill(intzfill),
                        ),
                    )
                break
        else:
            if dic != None:
                print(timevalue)

    if dic == None:
        return resultdic
    else:
        return None


# サンプルデータ
listdata = [
    "08:18:22",
    "08:26:00",
    "08:43:02",
    "08:59:06",
    "08:59:59",
    "09:02:21",
    "09:24:21",
    "09:44:21",
    "09:55:07",
    "10:00:07",
    "10:00:22",
    "10:00:37",
    "10:00:52",
    "10:01:07",
    "10:01:22",
    "10:06:37",
    "10:11:52",
    "10:17:07",
    "10:17:12",
    "10:22:12",
    "10:23:55",
    "10:30:07",
    "10:40:50",
    "11:40:50",
    "12:10:50",
    "13:10:50",
]

# サンプル辞書
table = [
    ["08:25:00", "08:59:59", "A神社"],
    ["09:00:00", "09:30:59", "B寺"],
    ["09:55:00", "10:24:11", "C公園"],
    ["10:24:12", "10:35:05", "D神社"],
    ["10:35:06", "11:59:59", "C公園"],
    ["13:00:12", "13:59:59", "E寺"],
]

# 先に各場所に何個あるか判定
resultdic = judge(None)

if resultdic != None:
    # 場所に対する数を意識して付番
    judge(resultdic)
