from operator import itemgetter 
import csv,itertools,sys
all_tables = []
all_fields = {}
ind = []
operands = ['>=','<=','<','>','=']
args = sys.argv
query = args[1]
sz = len(query)-1
def end(err):
    print(err)
    exit(0)

if query[sz]==';':
    query = query[0:sz]
else:
    err_string = 'Query doesnt end with ;'
    end(err_string)

def read_file(f):
    ptr = open(f,"r")
    contents = ptr.readlines()
    flag = 0
    idx = 0
    attr = []
    for line in contents:
        x = line.strip()
        if x == '<end_table>':
            all_fields[table] = []
            all_fields[table].append(attr)
            flag = 0
        if flag==1:
            attr.append(x)
        if flag == 2:
            table = x
            ind.append(x)
            flag = 1
        if x =='<begin_table>':
            attr = []
            flag = 2
        
            


def read_csv(ind):
    for file  in ind:
        filename = './files/'+file+'.csv'
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            idx = ind.index(file)
            new_table = []
            field = all_fields[file][0]
            for row in csv_reader:
                cnt = 0
                record = {}
                for entry in row:
                    record[file+'.'+field[cnt]]=int(entry)
                    cnt+=1
                new_table.append(record)
        all_tables.append(new_table)
             
            
        


def process_query(attr,sec_rec,ft,sd,query,dct_idx):
    get_rec = []#final ans
    bracket_idx = query.find('(')
    tb = ''
    if query.find('<=')!=-1:
        pass
    elif query.find('>=')!=-1:
        pass
    elif query.find('=')!=-1:
        op = '='
        q = query.split(op)
        # print(q)
        tb = q[0].split('where')
        op1 = tb[1]
        tb1 = q[1].split()
        op2 = tb1[0]
        op1 = op1.strip()
        op2 = op2.strip()
        if op1.isnumeric():
            swap(op1,op2)
        tb = op1
    if bracket_idx ==-1:#if there is no bracket it means query is not aggregate
        get_attr = []
        vis = {}
        flag = 0
        for atr in attr:
            if atr=='*':
                if len(sec_rec)==0:
                    print('Empty Set')
                    exit(0) 
                for x in sec_rec[0].keys():
                    if x==tb:
                        continue
                    get_attr.append(x)
            else:
                get_attr.append(atr)
        # print(get_attr)
        for rec in sec_rec:
            new_entry = []
            for atr in get_attr:
                if atr not in rec.keys():
                    string = 'Attribute doesnt exist'
                    end(string)
                new_entry.append(rec[atr])
            get_rec.append(new_entry)
        if len(get_rec)==0:
            print('Empty Set')
            exit(0)
        print (', '.join(get_attr))
        if dct_idx==-1:
            for record in get_rec:
                print(*record, sep =' ')
        else:
            final_ans = []
            for x in get_rec:
                if x not in final_ans:
                    final_ans.append(x)
            for record in final_ans:
                print(*record, sep =' ')

    else:
        get_ans = []
        for ft in attr:
            func_idx = ft.find('(')
            func_idx1 = ft.find(')')
            func = ft[0:func_idx]
            col_fd = ft[func_idx+1:func_idx1]
            if len(sec_rec)==0:
                get_ans.append('NULL')
                continue
            rec = list(map(itemgetter(col_fd), sec_rec))
            func = func.lower()
            if func=='max':
                ans = max(rec)
            elif func == 'min':
                ans = min(rec)
            elif func == 'sum':
                ans = sum(rec)
            elif func == 'avg':
                ans = sum(rec)/len(rec)
            else:
                string = 'Invalid syntax'
                end(string)
            get_ans.append(ans)
        print (', '.join(attr))
        for rec in get_ans:
           print (rec,end = ' ')



def get_actual_field(sd,oper):
    o = oper.find('table')
    if o!=-1:
        h = oper.split('.')
        if not h[1] in all_fields[h[0]][0]:
            string = 'Table doesnt exist'
            end(string)
        return oper
    flag = 0
    for table in sd:
        # print(all_fields.keys())
        field = all_fields[table][0]
        if oper in field:
            t = table
            flag+=1
    if flag == 1:
        oper = t+'.'+oper
        return oper
    elif flag>1:
        err = 'Attribute is ambiguous'
    else:
        err = 'Invalid SQL Syntax'
    end(err)




def check_condition(a,b,d):#ge,le,lt,gt,eq
    if operands[0]==d:
        if a>=b:
            return 1
    elif operands[1]==d:
        if a<=b:
            return 1
    elif operands[2]==d:
        if a<b:
            return 1
    elif operands[3]==d:
        if a>b:
            return 1
    elif operands[4]==d:
        if a==b:
            return 1
    else:
        err_string = 'Invalid Comparison Operator'
        end(err_string)
    return 0




def get_records(f_oper,s_oper,sec_rec,sd,operand): 
    get_rec = []
    if not (s_oper.isnumeric()):
        s_oper = get_actual_field(sd,s_oper)
        for field in sec_rec:
            if check_condition(field[f_oper],field[s_oper],operand):
                get_rec.append(field)           
    else:
        for field in sec_rec:
            if check_condition(field[f_oper],int(s_oper),operand):
                get_rec.append(field)
    return get_rec


def parse_query(query):
    get_attr = []
    q = query.split(" ")
    if len(q)-1<3:
        err_string = 'Invalid Query'
        end(err_string) 
    string1 = q[0].lower()
    if string1!='select':
        err_string = 'Query doesnt contain SELECT'
        end(err_string)
    else:
        string1 = q[0]
    # print(string1)
    dct_idx = query.find('distinct')
    if dct_idx!=-1:
        string2 = q[3].lower()
        if string2!='from':
            err_string = 'Invalid Syntax'
            end(err_string)
        else:
            string2 = q[3]
    else:
        string2 = q[2].lower()
        if string2!='from':
            err_string = 'Invalid syntax'
            end(err_string)
        else:
            string2 = q[2]
    sel = q.index(string1)#select
    if dct_idx!=-1:
        sel+=1
    ft = q[sel+1].split(',')#first part of the query
    fr = q.index(string2)#from
    sd = q[fr+1].split(',')#second part of the query
    bracket_idx = query.find('(')
    if bracket_idx != -1:
        #print(ft)
        for func in ft:
            # print(func)
            func_idx = func.find('(')
            func_idx1 = func.find(')')
            funct = func[0:func_idx]
            col_fd = func[func_idx+1:func_idx1]
            # print(col_fd)
            if col_fd.find('table')==-1:
                for table in sd:
                    flag = 0
                    if not table in all_fields.keys():
                        print('Table doesnt exist')
                    field = all_fields[table][0]
                    if col_fd in field:
                        flag = 1
                        get_attr.append(funct+'('+table+'.'+col_fd+')')
                        break
                if not flag:
                    err_string = 'Attribute doesnt exist in table'
                    end(err_string)
            else:
                h = col_fd.split('.')
                if not h[0] in all_fields.keys():
                    err_string = 'Table doesnt exist'
                    end(err_string)
                if not h[1] in all_fields[h[0]][0]:
                    err_string = 'Attribute doesnt exist in table'
                    end(err_string)

                get_attr.append(func)

  

    else:
        for header in ft:
            idx = header.find('table')
            if header == '*':
                get_attr.append('*')
                continue
            if idx==-1:
                flag = 0
                for table in sd:
                    if not table in all_fields.keys():
                        err_string = 'Table doesnt exist'
                        end(err_string)
                    field = all_fields[table][0]
                    if header in field:
                        flag += 1
                        t = table
                if flag==1:
                    get_attr.append(t+'.'+header)
                elif flag>1:
                    err_string = 'Attribute is ambiguous'
                    end(err_string)
                if not flag:
                    err_string = 'Attribute doesnt exist in table'
                    end(err_string)
            else:
                h = header.split('.')
                # print(h)
                if not h[0] in all_fields.keys():
                    print('Table doesnt exist')
                    exit(0)
                if not h[1] in all_fields[h[0]][0]:
                    print('Attribute doesnt exist in table')
                    exit(0)
                get_attr.append(header)
    tmp_rec = []
    sec_rec = []
    get_rec = []
    get_rec1 = []
    get_rec2 = []
    temp = []
    for table in sd:
        cols = []
        if not table in all_fields.keys():
            print('Table doesnt exist')
            exit(0)
        # print(all_fields.keys())
        field = all_fields[table][0]
        idx = list(all_fields).index(table)
        for rec in all_tables[idx]:
            cols.append(rec)
        temp.append(cols)
    for el in itertools.product(*temp):
        tmp_rec.append(el)
    for rec in tmp_rec:
        dicts = {}
        for cur in rec:
            dicts.update(cur)
        sec_rec.append(dicts) 
    qu = query.lower()  
    # print(len(q))
    if len(q)==4 or (dct_idx!=-1 and len(q)==5):
        process_query(get_attr,sec_rec,ft,sd,query,dct_idx)
    else:
        q = query.split(" ") 
        q_search = qu.split(" ")
        if query.find('where')==-1:
            print('Invalid SQL Syntax')
            exit(0) 

        wh = q_search.index('where')
        # print(len(q))
        # print(wh)
        if len(q)-1==wh or len(q)<=wh+3:
            err_string = 'WHERE Condition is missing'
            end(err_string)
        f_oper = q[wh+1]
        operand1 = q[wh+2]
        s_oper = q[wh+3]
        idx1 = qu.find('and')
        idx2 = qu.find('or')
        idx3 = qu.find('xor')
        if idx3!=-1:
            err_string = 'Invalid SQL Query'
            end(err_string)
        if idx1!=-1 and idx2==-1:#AND               
            log_op = q_search.index('and')
            if len(q_search)-1==log_op:
                err_string = 'Second Operand for AND is missing'
                end(err_string)
            f1_oper = q[log_op+1]
            operand2 = q[log_op+2]
            s1_oper = q[log_op+3]
            f_oper = get_actual_field(sd,f_oper)
            get_rec1 = get_records(f_oper,s_oper,sec_rec,sd,operand1)
            f1_oper = get_actual_field(sd,f1_oper)
            get_rec2 = get_records(f1_oper,s1_oper,sec_rec,sd,operand2)
            for x in get_rec1:
                for y in get_rec2:
                    if x==y:
                        get_rec.append(x)
                        break
        elif idx1==-1 and idx2!=-1:#OR
            log_op = q_search.index('or')
            # print("here")
            if len(q_search)-1==log_op:
                err_string = 'Second operand for OR is missing'
            f1_oper = q[log_op+1]
            operand2 = q[log_op+2]
            s1_oper = q[log_op+3]
            f_oper = get_actual_field(sd,f_oper)
            get_rec1 = get_records(f_oper,s_oper,sec_rec,sd,operand1)
            # print(len(get_rec1))
            f1_oper = get_actual_field(sd,f1_oper)
            get_rec2 = get_records(f1_oper,s1_oper,sec_rec,sd,operand2)
            # print(len(get_rec2))
            get_rec = get_rec1
            for y in get_rec2:
                fl = 0
                for x in get_rec1:
                    if x==y:
                        fl = 1
                        break
                if not fl:
                   	get_rec.append(y)
            # print(len(get_rec))
        else:
            f_oper = get_actual_field(sd,f_oper)
            get_rec = get_records(f_oper,s_oper,sec_rec,sd,operand1)
        process_query(get_attr,get_rec,ft,sd,query,dct_idx)   
                
                
f = './files/metadata.txt'
read_file(f)
read_csv(ind)
parse_query(query)

