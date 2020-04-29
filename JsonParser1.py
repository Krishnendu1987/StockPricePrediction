import xlrd
import pandas as pd
import queue



#loc = "C:/Users/91990/Documents/NT/Investment/Sample JSON Structure.xlsx"

#wb = xlrd.open_workbook(loc)
#sheet = wb.sheet_by_index(0)


data = pd.read_excel(r'C:/Users/91990/Documents/NT/Investment/Sample JSON Structure2.xlsx')
df = pd.DataFrame(data)



df.columns = df.columns.str.replace(' ', '')
#rows = sheet.nrows
#df1 = df.copy()
#df1.drop('Elements',axis=1, inplace=True)
#df1.sort_values
#df1.drop_duplicates(subset=None, keep='first', inplace=True)
#df1.sort_values

maxquelength = df['SpaceCounts'].nunique()
print(maxquelength)

ParentQueue = queue.LifoQueue(maxsize=maxquelength*3)
NodeLevel = 0
CurrentEntity = ''
CurrentParent = ''
CurrentAttribute = ''
for i in range(len(df)):

    rowindex = df.index[i]
    #rowindex1 = df.index[i+1]
    element = df.iloc[i]['Elements']
    element = element.strip()
    if i > 1 :
        prvelement = df.iloc[i-1]['Elements']
        prvelement = prvelement.strip()
    else :
        prvelement = 1
    spaceCount = df.iloc[i]['SpaceCounts'].astype(int)
    prvspaceCount = df.iloc[i]['PreviousRowCnt'].astype(int)
    nxtspaceCount = df.iloc[i]['NextRowCnt'].astype(int)
    #print(prvspaceCount)
    #print(nxtspaceCount)
    #print(spaceCount < nxtspaceCount)
    #print(spaceCount > prvspaceCount)
    #print(((spaceCount < nxtspaceCount) & (spaceCount > prvspaceCount)))
    # 1. If space count of current row is less than next row and greater than previous row :
    if ((spaceCount < nxtspaceCount) & (spaceCount > prvspaceCount)) :

        if ((element == '{') or (element == '}') or (element == ']') or (element == '[')):
            df.loc[rowindex, 'CurrentEntity'] = ''
            df.loc[rowindex, 'CurrentAttribute'] = ''
            df.loc[rowindex, 'CurrentParent'] = ''
            df.loc[rowindex, 'NodeLevel'] = ''
        elif ((element == '},') or (element == '],')):
            NodeLevel = NodeLevel - 1
            CurrentEntity = CurrentParent
            CurrentParent = ParentQueue.get()
            CurrentAttribute = ''
            df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
            df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
            df.loc[rowindex, 'CurrentParent'] = CurrentParent
            df.loc[rowindex, 'NodeLevel'] = NodeLevel
        else:
            #then it is an Entity and increase the Node Level by 1 Insert the Parent to Queue and make Current Entity as Parent Entity and make this Entity as current Entity Attribute will be Null.

            NodeLevel = NodeLevel + 1
            ParentQueue.put(CurrentParent)
            CurrentParent = CurrentEntity
            CurrentEntity = element
            CurrentAttribute = ''
            df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
            df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
            df.loc[rowindex, 'CurrentParent'] = CurrentParent
            df.loc[rowindex, 'NodeLevel'] = NodeLevel
        print(spaceCount, prvspaceCount, nxtspaceCount,i,ParentQueue.qsize())
    # 2. If space count of current row is less than next row and less than previous row : then
    if ((spaceCount < nxtspaceCount) & (spaceCount < prvspaceCount)) :
        # 2.1. If previous count equal to next count :
        if prvspaceCount == nxtspaceCount :


            if ((element == '{') or (element == '}') or (element == ']') or (element == '[')):
                df.loc[rowindex, 'CurrentEntity'] = ''
                df.loc[rowindex, 'CurrentAttribute'] = ''
                df.loc[rowindex, 'CurrentParent'] = ''
                df.loc[rowindex, 'NodeLevel'] = ''
            elif ((element == '},') or (element == '],')):
                NodeLevel = NodeLevel - 1
                CurrentEntity = CurrentParent
                CurrentParent = ParentQueue.get()
                CurrentAttribute = ''
                df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
                df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
                df.loc[rowindex, 'CurrentParent'] = CurrentParent
                df.loc[rowindex, 'NodeLevel'] = NodeLevel
            else:
                # then it is an Entity and of same the Node Level and same Parent Node and Attribute is Null.
                CurrentEntity = element
                CurrentAttribute = ''
                df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
                df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
                df.loc[rowindex, 'CurrentParent'] = CurrentParent
                df.loc[rowindex, 'NodeLevel'] = NodeLevel
            print(spaceCount, prvspaceCount, nxtspaceCount,i,ParentQueue.qsize())
        # 2.2. If previous count greater than next count :
        if prvspaceCount > nxtspaceCount :
            if ((element == '{') or (element == '}') or (element == ']') or (element == '[')):
                df.loc[rowindex, 'CurrentEntity'] = ''
                df.loc[rowindex, 'CurrentAttribute'] = ''
                df.loc[rowindex, 'CurrentParent'] = ''
                df.loc[rowindex, 'NodeLevel'] = ''
            elif ((element == '},') or (element == '],')):
                NodeLevel = NodeLevel - 1
                CurrentEntity = CurrentParent
                CurrentParent = ParentQueue.get()
                CurrentAttribute = ''
                df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
                df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
                df.loc[rowindex, 'CurrentParent'] = CurrentParent
                df.loc[rowindex, 'NodeLevel'] = NodeLevel
            else:
                #then it is an Entity with Node level -1 pop up the the Parent Node from Queue and make it Parent Entity.
                NodeLevel = NodeLevel - 1
                CurrentParent = ParentQueue.get()
                CurrentEntity = element
                CurrentAttribute = ''
                df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
                df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
                df.loc[rowindex, 'CurrentParent'] = CurrentParent
                df.loc[rowindex, 'NodeLevel'] = NodeLevel
            print(spaceCount, prvspaceCount, nxtspaceCount,i,ParentQueue.qsize())

        # 2.3. If previous count less than next count :
        if prvspaceCount < nxtspaceCount :
            # then
            if ((element == '{') or (element == '}') or (element == ']') or (element == '[')):
                df.loc[rowindex, 'CurrentEntity'] = ''
                df.loc[rowindex, 'CurrentAttribute'] = ''
                df.loc[rowindex, 'CurrentParent'] = ''
                df.loc[rowindex, 'NodeLevel'] = ''
            elif ((element == '},') or (element == '],')):
                NodeLevel = NodeLevel - 1
                CurrentEntity = CurrentParent
                CurrentParent = ParentQueue.get()
                CurrentAttribute = ''
                df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
                df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
                df.loc[rowindex, 'CurrentParent'] = CurrentParent
                df.loc[rowindex, 'NodeLevel'] = NodeLevel
            else:
                print(spaceCount, prvspaceCount, nxtspaceCount,i,ParentQueue.qsize())

    #3. If space count of current row is less than next row and equal to previous row :
    if ((spaceCount < nxtspaceCount) & (spaceCount == prvspaceCount)) :
        if ((element == '{') or (element == '}') or (element == ']') or (element == '[')):
            df.loc[rowindex, 'CurrentEntity'] = ''
            df.loc[rowindex, 'CurrentAttribute'] = ''
            df.loc[rowindex, 'CurrentParent'] = ''
            df.loc[rowindex, 'NodeLevel'] = ''
        elif ((element == '},') or (element == '],')):
            NodeLevel = NodeLevel - 1
            CurrentEntity = CurrentParent
            CurrentParent = ParentQueue.get()
            CurrentAttribute = ''
            df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
            df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
            df.loc[rowindex, 'CurrentParent'] = CurrentParent
            df.loc[rowindex, 'NodeLevel'] = NodeLevel
        else:

            if (prvelement == '},') :
                # an Entity with Node level -1 and pop up the Parent Element from the Queue. [},]
                NodeLevel = NodeLevel - 1
                CurrentEntity = element
                CurrentAttribute = ''
                CurrentParent = ParentQueue.get()
            else:
                # then it is an Entity with Node level + 1 and current Entity to be made as Parent Entity and Attribute is Null Push the Parent Entity to the Queue.
                NodeLevel = NodeLevel + 1
                ParentQueue.put(CurrentParent)
                CurrentParent = CurrentEntity
                CurrentEntity = element
                CurrentAttribute = ''

            df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
            df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
            df.loc[rowindex, 'CurrentParent'] = CurrentParent
            df.loc[rowindex, 'NodeLevel'] = NodeLevel
        print(spaceCount, prvspaceCount, nxtspaceCount,i,ParentQueue.qsize())
    # 4. If space count of current row is greater than next row and equal to previous row :
    if ((spaceCount > nxtspaceCount) & (spaceCount == prvspaceCount)) :

        if ((element == '{') or (element == '}') or (element == ']') or (element == '[')):
            df.loc[rowindex, 'CurrentEntity'] = ''
            df.loc[rowindex, 'CurrentAttribute'] = ''
            df.loc[rowindex, 'CurrentParent'] = ''
            df.loc[rowindex, 'NodeLevel'] = ''
        elif ((element == '},') or (element == '],')):
            NodeLevel = NodeLevel - 1
            CurrentEntity = CurrentParent
            CurrentParent = ParentQueue.get()
            CurrentAttribute = ''
            df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
            df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
            df.loc[rowindex, 'CurrentParent'] = CurrentParent
            df.loc[rowindex, 'NodeLevel'] = NodeLevel
        else:
            # then it is an Attribute with same Node level and same Parent Entity and also the last attribute of the current Entity.
            CurrentAttribute = element
            df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
            df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
            df.loc[rowindex, 'CurrentParent'] = CurrentParent
            df.loc[rowindex, 'NodeLevel'] = NodeLevel
        print(spaceCount, prvspaceCount, nxtspaceCount,i,ParentQueue.qsize())
    # 5. If space count of current row is greater than next row and less than previous row :
    if ((spaceCount > nxtspaceCount) & (spaceCount < prvspaceCount)) :

        if ((element == '{') or (element == '}') or (element == ']') or (element == '[')):
            df.loc[rowindex, 'CurrentEntity'] = ''
            df.loc[rowindex, 'CurrentAttribute'] = ''
            df.loc[rowindex, 'CurrentParent'] = ''
            df.loc[rowindex, 'NodeLevel'] = ''
        elif ((element == '},') or (element == '],')):
            NodeLevel = NodeLevel - 1
            CurrentEntity = CurrentParent
            CurrentParent = ParentQueue.get()
            CurrentAttribute = ''
            df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
            df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
            df.loc[rowindex, 'CurrentParent'] = CurrentParent
            df.loc[rowindex, 'NodeLevel'] = NodeLevel
        else:
            # then it is an Attribute with Node level -1 and Parent Entity to be made current Entity and previous Parent need to pop up from Queue.
            NodeLevel = NodeLevel - 1
            CurrentEntity = CurrentParent
            CurrentParent = ParentQueue.get()
            CurrentAttribute = element
            df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
            df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
            df.loc[rowindex, 'CurrentParent'] = CurrentParent
            df.loc[rowindex, 'NodeLevel'] = NodeLevel
        print(spaceCount, prvspaceCount, nxtspaceCount,i,ParentQueue.qsize())
    # 6. If space count of current row is greater than next row and greater than previous row :
    if ((spaceCount > nxtspaceCount) & (spaceCount > prvspaceCount)) :
        #6.1. If previous count equal to next count :
        if prvspaceCount == nxtspaceCount :
            if ((element == '{') or (element == '}') or (element == ']') or (element == '[')):
                df.loc[rowindex, 'CurrentEntity'] = ''
                df.loc[rowindex, 'CurrentAttribute'] = ''
                df.loc[rowindex, 'CurrentParent'] = ''
                df.loc[rowindex, 'NodeLevel'] = ''
            elif ((element == '},') or (element == '],')):
                NodeLevel = NodeLevel - 1
                CurrentEntity = CurrentParent
                CurrentParent = ParentQueue.get()
                CurrentAttribute = ''
                df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
                df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
                df.loc[rowindex, 'CurrentParent'] = CurrentParent
                df.loc[rowindex, 'NodeLevel'] = NodeLevel
            else:
                # then it is an attribute with the same node level and same enity as well as same parent.
                CurrentAttribute = element
                df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
                df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
                df.loc[rowindex, 'CurrentParent'] = CurrentParent
                df.loc[rowindex, 'NodeLevel'] = NodeLevel
            print(spaceCount, prvspaceCount, nxtspaceCount,i,ParentQueue.qsize())

        #6.2. If previous count greater than next count :
        if prvspaceCount > nxtspaceCount :
            if ((element == '{') or (element == '}') or (element == ']') or (element == '[')):
                df.loc[rowindex, 'CurrentEntity'] = ''
                df.loc[rowindex, 'CurrentAttribute'] = ''
                df.loc[rowindex, 'CurrentParent'] = ''
                df.loc[rowindex, 'NodeLevel'] = ''
            elif ((element == '},') or (element == '],')):
                NodeLevel = NodeLevel - 1
                CurrentEntity = CurrentParent
                CurrentParent = ParentQueue.get()
                CurrentAttribute = ''
                df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
                df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
                df.loc[rowindex, 'CurrentParent'] = CurrentParent
                df.loc[rowindex, 'NodeLevel'] = NodeLevel
            else:
                # then
                print(spaceCount, prvspaceCount, nxtspaceCount,i,ParentQueue.qsize())
        # 6.3. If previous count less than next count :
        if prvspaceCount < nxtspaceCount :
            if ((element == '{') or (element == '}') or (element == ']') or (element == '[')):
                df.loc[rowindex, 'CurrentEntity'] = ''
                df.loc[rowindex, 'CurrentAttribute'] = ''
                df.loc[rowindex, 'CurrentParent'] = ''
                df.loc[rowindex, 'NodeLevel'] = ''
            elif ((element == '},') or (element == '],')):
                NodeLevel = NodeLevel - 1
                CurrentEntity = CurrentParent
                CurrentParent = ParentQueue.get()
                CurrentAttribute = ''
                df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
                df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
                df.loc[rowindex, 'CurrentParent'] = CurrentParent
                df.loc[rowindex, 'NodeLevel'] = NodeLevel
            else:
                # then
                print(spaceCount, prvspaceCount, nxtspaceCount,i,ParentQueue.qsize())
    # 7. If space count of current row is equal to next row and equal to previous row :
    if ((spaceCount == nxtspaceCount) & (spaceCount == prvspaceCount)) :
        if ((element == '{') or (element == '}') or (element == ']') or (element == '[')):
            df.loc[rowindex, 'CurrentEntity'] = ''
            df.loc[rowindex, 'CurrentAttribute'] = ''
            df.loc[rowindex, 'CurrentParent'] = ''
            df.loc[rowindex, 'NodeLevel'] = ''
        elif ((element == '},') or (element == '],')):
            NodeLevel = NodeLevel - 1
            CurrentEntity = CurrentParent
            CurrentParent = ParentQueue.get()
            CurrentAttribute = ''
            df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
            df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
            df.loc[rowindex, 'CurrentParent'] = CurrentParent
            df.loc[rowindex, 'NodeLevel'] = NodeLevel
        else:
            # then it is an Attribute with same Node level and Same Current and Parent Entity.
            CurrentAttribute = element
            df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
            df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
            df.loc[rowindex, 'CurrentParent'] = CurrentParent
            df.loc[rowindex, 'NodeLevel'] = NodeLevel
        print(spaceCount, prvspaceCount, nxtspaceCount,i,ParentQueue.qsize())
    # 8. If space count of current row is equal to next row and less than previous row :
    if ((spaceCount == nxtspaceCount) & (spaceCount < prvspaceCount)) :

        if ((element == '{') or (element == '}') or (element == ']') or (element == '[')):
            df.loc[rowindex, 'CurrentEntity'] = ''
            df.loc[rowindex, 'CurrentAttribute'] = ''
            df.loc[rowindex, 'CurrentParent'] = ''
            df.loc[rowindex, 'NodeLevel'] = ''
        elif ((element == '},') or (element == '],')):
            NodeLevel = NodeLevel - 1
            CurrentEntity = CurrentParent
            CurrentParent = ParentQueue.get()
            CurrentAttribute = ''
            df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
            df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
            df.loc[rowindex, 'CurrentParent'] = CurrentParent
            df.loc[rowindex, 'NodeLevel'] = NodeLevel
        else:
            # then it is an Attribute with Node level -1 make Parent Entity as Current Entity and pop up the Parent Entity from Queue.
            NodeLevel = NodeLevel - 1
            CurrentEntity = CurrentParent
            CurrentParent = ParentQueue.get()
            CurrentAttribute = element
            df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
            df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
            df.loc[rowindex, 'CurrentParent'] = CurrentParent
            df.loc[rowindex, 'NodeLevel'] = NodeLevel
        print(spaceCount, prvspaceCount, nxtspaceCount,i,ParentQueue.qsize())
    # 9. If space count of current row is equal to next row and greater than previous row :
    if ((spaceCount == nxtspaceCount) & (spaceCount > prvspaceCount)) :

        if ((element == '{') or (element == '}') or (element == ']') or (element == '[')):
            df.loc[rowindex, 'CurrentEntity'] = ''
            df.loc[rowindex, 'CurrentAttribute'] = ''
            df.loc[rowindex, 'CurrentParent'] = ''
            df.loc[rowindex, 'NodeLevel'] = ''
        elif ((element == '},') or (element == '],')):
            NodeLevel = NodeLevel - 1
            CurrentEntity = CurrentParent
            CurrentParent = ParentQueue.get()
            CurrentAttribute = ''
            df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
            df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
            df.loc[rowindex, 'CurrentParent'] = CurrentParent
            df.loc[rowindex, 'NodeLevel'] = NodeLevel
        else:
            # then it is an Attribute with same Node level same Entity and same Parent Entity.
            CurrentAttribute = element
            df.loc[rowindex, 'CurrentEntity'] = CurrentEntity
            df.loc[rowindex, 'CurrentAttribute'] = CurrentAttribute
            df.loc[rowindex, 'CurrentParent'] = CurrentParent
            df.loc[rowindex, 'NodeLevel'] = NodeLevel
        print(spaceCount,prvspaceCount,nxtspaceCount,i,ParentQueue.qsize())




    #spaceCount1 = df.loc(rowindex1, 'SpaceCounts')

#serial_no = []

#for i in range(sheet.nrows):

#    data = sheet.cell_value(i, 0)

#    serial_no.append(data)


#print(df)

print(df)

writer = pd.ExcelWriter('C:/Users/91990/Documents/NT/Investment/Result JSON Structure2.xlsx')

df.to_excel(writer)

writer.save()

