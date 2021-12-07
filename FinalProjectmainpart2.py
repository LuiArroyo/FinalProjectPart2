# Luis Arroyo
# PSID: 2037081
# CIS 2348

#___________________PART 1_______________________
import csv
import datetime
from operator import itemgetter

#preparing lists
manufacturerlist=[]
pricelist=[]
servicedateslist=[]

#pulling data from csv files, with statement closes file once done
with open('ManufacturerList.csv') as manulist:
    manlist=csv.reader(manulist)
    for line in manlist:
        manufacturerlist.append(line)
with open('PriceList.csv') as prilist:
    prlist=csv.reader(prilist)
    for line in prlist:
        pricelist.append(line)
with open('ServiceDatesList.csv') as servlist:
    slist=csv.reader(servlist)
    for line in slist:
        servicedateslist.append(line)

#sort the lists by Order ID, use itemgetter
update_manufacturerlist= (sorted(manufacturerlist, key=itemgetter (0)))
update_pricelist= (sorted(pricelist, key=itemgetter (0)))
update_servicedateslist= (sorted(servicedateslist, key=itemgetter (0)))

#inserting pricelist and servicelist to manufacturinglist before the damaged column
for update in range (0, len(update_manufacturerlist)):
    update_manufacturerlist[update].insert(3, pricelist[update][1])
for update in range (0, len(update_manufacturerlist)):
    update_manufacturerlist[update].insert(4, servicedateslist[update][1])

#newest manufacture
newestlist=manufacturerlist #final_list
fullinventory=(sorted(newestlist, key=itemgetter(1)))

#write FullInventory using w command if file does not exist
with open('FullInventory.csv', 'w') as masterfile:
    write=csv.writer(masterfile)
    for f in range (0, len(fullinventory)):
        write.writerow(fullinventory[f])

#inventory list by the three item types
laptoponly=[]
phoneonly=[]
toweronly=[]

#finding each item type in the 2nd column of FullInventory
for f in range(0, len(fullinventory)):
    if fullinventory[f][2]=='laptop':
        laptoponly.append(fullinventory[f])
    elif fullinventory[f][2]=='phone':
        phoneonly.append(fullinventory[f])
    elif fullinventory[f][2]=='tower':
        toweronly.append(fullinventory[f])

#writing new files for items
with open('LaptopInventory.csv', 'w') as llist:
    write=csv.writer(llist)
    for f in range (0, len(laptoponly)):
        write.writerow(laptoponly[f])
with open('PhoneInventory.csv', 'w') as plist:
    write=csv.writer(plist)
    for f in range (0, len(phoneonly)):
        write.writerow(phoneonly[f])
with open('TowerInventory.csv', 'w') as tlist:
    write=csv.writer(tlist)
    for f in range (0, len(toweronly)):
        write.writerow(toweronly[f])

#preparing past service date list
pastsdlist=[]
today = datetime.date.today()
todayreal = today.strftime("%m/%d/%Y").replace('/0', '/')

#finding date in file
for f in range(0, len(fullinventory)):
    testdate = fullinventory[f][4]
    # testdate = datetime.date.fullinventory[f][4] <-test dummy code
    if fullinventory[f][4] <= todayreal:
        pastsdlist.append(fullinventory[f])
pastsdlist=(sorted(pastsdlist, key=itemgetter(4), reverse=True))

#writing pastdate file
with open('PastServiceDateInventory.csv', 'w') as psdfile:
    write=csv.writer(psdfile)
    for f in range (0, len(pastsdlist)):
        write.writerow(pastsdlist[f])

#preparing damaged list
damagedlist=[]

#finding damage in file
for f in range(0, len(fullinventory)):
    if fullinventory[f][5] == "damaged":
        damagedlist.append(fullinventory[f])
damagedlist=(sorted(damagedlist, key=itemgetter(3), reverse=True))

#writing damaged file using w function
with open('DamagedInventory.csv', 'w') as dfile:
    write=csv.writer(dfile)
    for f in range (0, len(damagedlist)):
        write.writerow(damagedlist[f])


#___________________PART 2_______________________
#preparing the breakdown of the items
def separate1(lst):
    return [entry[0] for entry in lst]
def separate2(lst):
    return [entry[1] for entry in lst]
def separate3(lst):
    return [entry[2] for entry in lst]
def separate4(lst):
    return [entry[3] for entry in lst]

#breaking down fullinventory into separate lists
id_list = separate1(fullinventory)
mf_list = separate2(fullinventory)
ty_list = separate3(fullinventory)
pr_list = separate4(fullinventory)

#main code for query
while True:
    #ask user to type a manufacturer and item type
    ask_query = input('Type a manufacturer and item type, or q to quit: ')
    #allowing 'q' to quit
    if ask_query == "q":
        break
    #splitting
    ask_query = ask_query.split()
    item = ""
    types = ""
    #assign manufacturer to item if they are present in query
    for word in ask_query:
        for f in mf_list:
            if str(f).lower() == str(word).lower():
                item = f
        #assign item type to item if they are present in query
        for f in ty_list:
            if str(f).lower() == str(word).lower():
                types = f
    #if empty, say no such item
    if item == "" or types == "":
        print("No such item in inventory")
    else:
        fake_list_final = []
        #iterate over data
        for f in range(len(id_list)):
            #infer data
            if mf_list[f] == item and ty_list[f] == types:
                fake_list = []
                fake_list.append(pr_list[f])
                fake_list.append(id_list[f])
                fake_list.append(mf_list[f])
                fake_list.append(ty_list[f])
                fake_list_final.append(fake_list)
        #organize
        result = (sorted(fake_list_final, key=itemgetter(0), reverse=True))
        print('Your item is ' + str(result[0][1]) + ' ' + str(result[0][2]) + ' ' + str(result[0][3]) + ' ' + str(result[0][0]))
        consider = ['', '', '', 0]
        for f in range (len(id_list)):
            if ty_list[f] == type and mf_list[f] != item:
                consider[0] = id_list[f]
                consider[1] = mf_list[f]
                consider[2] = ty_list[f]
                consider[3] = pr_list[f]
                print ('You may also like ' + str(consider[0]) + '' + str(consider[1]) + '' + str(consider[2]) + '' + str(consider[3]))