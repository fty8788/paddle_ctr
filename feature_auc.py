#coding: gbk

import sys


bucket_num = 50

def read_lr_result(result_file):
    f = open(result_file)
    result_list = []
    for line in f:
        line_t = line.rstrip().split(",")
        sample = []
        label = line_t[2]
        sample.append(label)
        pctr = line_t[-1]
        sample.append(pctr)
        result_list.append(sample)
        continue
        try:
            sample = []
            label = line_t[0]
            themisq = float(line_t[1])
            sample.append(label)
            sample.append(themisq)
            result_list.append(sample)
        except Exception, e:
            print e, line.rstrip()

        #ctr1 = float(line_t[3])
        #ctr2 = float(line_t[4])
        #ctr3 = float(line_t[5])
        #ctr4 = float(line_t[6])
        #cos = float(line_t[7])
        #clicks1 = float(line_t[8])
        #clicks2 = float(line_t[9])
        #clicks3 = float(line_t[10])
        #result_list.append(([label, query, intent, ctr1, ctr2, ctr3, ctr4]))
        #result_list.append(([label, query, intent, ctr1, ctr2, ctr3, ctr4, cos, clicks1, clicks2]))
        #result_list.append(([label, query, intent, ctr1, ctr2, ctr3, ctr4, cos, clicks1, clicks2, clicks3]))
    return result_list

def cal_base_auc(result_list):
    sort_list = sorted(result_list,key=lambda d:d[0],reverse=True)
    sample_num = len(sort_list)
    bucket_size = sample_num / bucket_num
    while bucket_size*bucket_num < sample_num:
        bucket_size += 1
    auc = 0.0
    acc_clk = 0.0
    acc_noclk = 0.0
    for i in range(bucket_num):
        clk = 0.0
        noclk = 0.0
        show = 0.0
        for j in range(i*bucket_size, (i+1)*bucket_size):
            if j >= len(sort_list):
                continue
            label = sort_list[j][0]
            #res = sort_list[j][1]
            #pctr = sort_list[j][2]
            #print >> sys.stderr, i, j, label, res, pctr
            if label == "1":
                clk += 1.0
            elif label == "0":
                noclk += 1.0
            show += 1.0
        auc_i = clk*noclk/2
        auc += auc_i
        auc += acc_clk*noclk
        acc_clk += clk
        acc_noclk += noclk
        if auc_i < 0.001:
            print >> sys.stderr, i, clk, noclk, show, auc_i, auc
    auc /= acc_clk*acc_noclk
    return auc

def cal_auc(result_list, p):
    sort_list = sorted(result_list,key=lambda d:d[p],reverse=True)
    sample_num = len(sort_list)
    bucket_size = sample_num / bucket_num
    while bucket_size*bucket_num < sample_num:
        bucket_size += 1
    auc = 0.0
    acc_clk = 0.0
    acc_noclk = 0.0
    for i in range(bucket_num):
        clk = 0.0
        noclk = 0.0
        show = 0.0
        for j in range(i*bucket_size, (i+1)*bucket_size):
            if j >= len(sort_list):
                continue
            label = sort_list[j][0]
            #res = sort_list[j][1]
            #pctr = sort_list[j][2]
            #print >> sys.stderr, i, j, label, res, pctr
            if label == "1":
                clk += 1.0
            elif label == "0":
                noclk += 1.0
            show += 1.0
        auc_i = clk*noclk/2
        auc += auc_i
        auc += acc_clk*noclk
        acc_clk += clk
        acc_noclk += noclk
        if auc_i < 0.001:
            print >> sys.stderr, i, clk, noclk, show, auc_i, auc
    auc /= acc_clk*acc_noclk
    return auc

def cal_wmwt(result_list, p):
    sort_list = sorted(result_list,key=lambda d:d[p],reverse=True)
    n = float(len(sort_list))
    M = 0.0
    N = 0.0
    sum_rank = 0.0
    rank = n
    for item in sort_list:
        label = item[0]
        if label == "1":
            M += 1
            sum_rank += rank
        else:
            N += 1
        rank -= 1
    auc = (sum_rank -M*(M+1)/2) / (M*N)
    return auc

def evaluation(result_file):
    result_list = read_lr_result(result_file)
    print cal_base_auc(result_list)
    #print cal_auc(result_list, 0)
    print cal_wmwt(result_list, 1)
    #print cal_wmwt(result_list, 2)
    #print cal_wmwt(result_list, 3)
    #print cal_wmwt(result_list, 4)
    #print cal_wmwt(result_list, 5)
    #print cal_wmwt(result_list, 6)
    #print cal_wmwt(result_list, 7)
    #print cal_wmwt(result_list, 8)
    #print cal_auc(result_list, 1)
    #print cal_auc(result_list, 4)
    #print cal_auc(result_list, 5)
    #print cal_auc(result_list, 6)
    #print cal_auc(result_list, 7)
    #print cal_auc(result_list, 8)
    #print cal_auc(result_list, 9)
    #print cal_auc(result_list, 10)

if __name__ == '__main__':
    evaluation(sys.argv[1])

