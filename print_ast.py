def print_ast(ast,f, rec=3):

    if len(ast) == 0:
        print('-' * rec, '[]')
        f.write('-' * rec + '[]\n')

    elif isinstance(ast[0], str):
        if ast[0] == 'bin_op':
            print('-' * rec, 'bin_op:')
            f.write('-' * rec + 'bin_op:\n')
            if isinstance(ast[2], int) or isinstance(ast[2], str):
                print('-' * (rec + 3), 'left:', ast[2])
                f.write('-' * (rec + 3) + 'left:' + str(ast[2])+'\n')
            else:
                print('-' * (rec + 3), 'left:')
                f.write('-' * (rec + 3) + 'left:'+'\n')
                print_ast(ast[2],f,rec + 6)
            print('-' * (rec + 3), 'op:', ast[1])
            f.write('-' * (rec + 3) + 'op:' + str(ast[1])+'\n')

            if isinstance(ast[3], int) or isinstance(ast[3], str):
                print('-' * (rec + 3), 'right:', ast[3])
                f.write('-' * (rec + 3)+ 'right:'+ str(ast[3])+'\n')
            else:
                print('-' * (rec + 3), 'right:')
                f.write('-' * (rec + 3)+ 'right:'+'\n')
                print_ast(ast[3],f,rec + 6)
        elif ast[0] == 'un_op':
            print('-' * rec, 'un_op:')
            f.write('-' * rec+'un_op:'+'\n')
            if isinstance(ast[2], int) or isinstance(ast[2], str):
                print('-' * (rec + 3), 'el:', ast[2])
                f.write('-' * (rec + 3)+ 'el:'+ str(ast[2])+'\n')
            else:
                print('-' * (rec + 3), 'el:')
                f.write('-' * (rec + 3)+'el:'+'\n')
                print_ast(ast[2], f,rec + 6)
            print('-' * (rec + 3), 'op:', ast[1])
            f.write('-' * (rec + 3)+ 'op:'+ str(ast[1])+'\n')
        elif ast[0] == 'call_func':
            print('-' * rec, 'call_func:')
            f.write('-' * rec+ 'call_func:'+'\n')
            print('-' * (rec + 3), 'id:', ast[1])
            f.write('-' * (rec + 3)+ 'id:' +str(ast[1])+'\n')
            print('-' * (rec + 3), 'args:', ast[2])
            f.write('-' * (rec + 3)+ 'args:' +str(ast[2])+'\n')

    else:
        for el in ast:
            if el[0] == 'func':
                print('-'*rec,'func_id: ', el[1])
                f.write('-'*rec+'func_id: ' + str(el[1])+'\n')
                print('-' * rec, 'args:', el[2])
                f.write('-' * rec+ 'args:' + str(el[2])+'\n')
                print('-' * rec, 'body:')
                f.write('-' * rec+ 'body:'+'\n')
                print_ast(el[3],f,rec+3)
            elif el[0] == 'return':
                print('-'*rec, 'return:')
                f.write('-'*rec+ 'return:'+'\n')
                print('-' * (rec + 3), 'val:')
                f.write('-' * (rec + 3)+ 'val:'+'\n')
                if isinstance(el[1], int) or isinstance(el[1], str):
                    print('-' * (rec + 6), el[1])
                    f.write('-' * (rec + 6)+ str(el[1])+'\n')
                else:
                    print_ast(el[1],f,rec + 6)
            elif el[0] == 'assignment':
                print('-'*rec, 'assignment:')
                f.write('-'*rec+ 'assignment:'+'\n')
                print('-' * (rec + 3), 'id:', el[1])
                f.write('-' * (rec + 3)+ 'id:'+ str(el[1])+'\n')
                print('-' * (rec + 3), 'val:')
                f.write('-' * (rec + 3)+'val:'+'\n')
                if isinstance(el[2], int) or isinstance(el[2], str):
                    print('-' * (rec + 6), el[2])
                    f.write('-' * (rec + 6)+ str(el[2])+'\n')
                else:
                    print_ast(el[2], f,rec + 6)
            elif el[0] == 'if':
                print('-' * rec, 'if:')
                f.write('-' * rec+ 'if:'+'\n')
                print('-' * (rec + 3), 'expr:')
                f.write('-' * (rec + 3)+ 'expr:'+'\n')
                if isinstance(el[1], int) or isinstance(el[1], str):
                    print('-' * (rec + 6), el[1])
                    f.write('-' * (rec + 6)+ str(el[1])+'\n')
                else:
                    print_ast(el[1], f, rec + 6)
                print('-' * (rec + 3), 'then:')
                f.write('-' * (rec + 3)+ 'then:'+'\n')
                print_ast(el[2],f,rec + 6)
                print('-' * (rec + 3), 'else:')
                f.write('-' * (rec + 3)+ 'else:'+'\n')
                print_ast(el[3], f,rec + 6)
            elif el[0] == 'while':
                print('-' * rec, 'while:')
                f.write('-' * rec+ 'while:'+'\n')
                print('-' * (rec + 3), 'expr:')
                f.write('-' * (rec + 3)+ 'expr:'+'\n')
                if isinstance(el[1], int) or isinstance(el[1], str):
                    print('-' * (rec + 6), el[1])
                    f.write('-' * (rec + 6)+ str(el[1])+'\n')
                else:
                    print_ast(el[1],f,rec + 6)
                print('-' * (rec + 3), 'body:')
                f.write('-' * (rec + 3)+ 'body:'+'\n')
                print_ast(el[2],f,rec + 6)
