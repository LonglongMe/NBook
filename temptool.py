pageline=22
a=[[
                [
                    0,
                    0,
                    3,
                    4
                ],
                [
                    1,
                    0,
                    0,
                    1
                ],
                [
                    2,
                    0,
                    0,
                    1
                ],
                [
                    3,
                    0,
                    0,
                    1
                ],
                [
                    4,
                    0,
                    0,
                    1
                ],
                [
                    5,
                    0,
                    0,
                    1
                ],
                [
                    6,
                    0,
                    0,
                    1
                ],
                [
                    7,
                    0,
                    0,
                    1
                ],
                [
                    8,
                    0,
                    0,
                    1
                ],
                [
                    9,
                    0,
                    0,
                    1
                ],
                [
                    10,
                    0,
                    0,
                    1
                ],
                [
                    11,
                    0,
                    0,
                    1
                ],
                [
                    12,
                    0,
                    1,
                    2
                ],
                [
                    13,
                    0,
                    1,
                    2
                ],
                [
                    14,
                    0,
                    1,
                    2
                ],
                [
                    15,
                    1,
                    1,
                    1
                ]
            ],
            [
                [
                    16,
                    0,
                    0,
                    1
                ],
                [
                    17,
                    0,
                    0,
                    1
                ],
                [
                    18,
                    0,
                    0,
                    1
                ],
                [
                    19,
                    0,
                    0,
                    1
                ],
                [
                    20,
                    0,
                    0,
                    1
                ],
                [
                    21,
                    0,
                    0,
                    1
                ],
                [
                    22,
                    0,
                    0,
                    1
                ],
                [
                    23,
                    0,
                    0,
                    1
                ],
                [
                    24,
                    0,
                    0,
                    1
                ],
                [
                    25,
                    0,
                    0,
                    1
                ],
                [
                    26,
                    0,
                    0,
                    1
                ],
                [
                    27,
                    0,
                    0,
                    1
                ],
                [
                    28,
                    0,
                    0,
                    1
                ],
                [
                    29,
                    0,
                    0,
                    1
                ],
                [
                    30,
                    0,
                    0,
                    1
                ],
                [
                    31,
                    0,
                    1,
                    2
                ],
                [
                    32,
                    0,
                    2,
                    3
                ],
                [
                    33,
                    0,
                    0,
                    1
                ],
                [
                    34,
                    1,
                    1,
                    1
                ]
            ]]
sum=0
pageindex=0
newlist=[[]]
for pages in a:
    for words in pages:
        tepstart=0
        if sum+words[3]>=pageline:
            if sum+words[3]==pageline:
                newlist[pageindex].append([words[0],0,words[3],words[3]])
                newlist.append([])
                pageindex+=1
                sum=0
            else:
                newlist[pageindex].append([words[0],0,pageline-sum,words[3]])
                newlist.append([])
                pageindex+=1
                tepstart=pageline-sum
                while words[3]-tepstart>=pageline:
                    newlist[pageindex].append([words[0],tepstart,tepstart+pageline,words[3]])
                    tepstart+=pageline
                    newlist.append([])
                    pageindex+=1
                sum=words[3]-tepstart
                if sum!=0:
                    newlist[pageindex].append([words[0],tepstart,words[3],words[3]])
        else:
            sum+=words[3]
            newlist[pageindex].append([words[0],0,words[3]-1,words[3]])
print(newlist)