#### IZI Zoo inventory system####
##install the following packages in your python system
import os
import pandas as pd
import datetime
##Take user inputs
def feed_refill():
    feed_refill_list=[]	
    feed_refill_date=input("Enter refilling of feed date(mm-dd-yy) in quotes: ")    
	feed_refill_time=input("Enter refilling of feed time(hh:mm) in quotes: ")
	feed_refill_zoo=input("Enter refilling zoo number(1-215) in quotes: ")
	feed_refill_qty=input("Enter refilling quantity(lbs): ")
	feed_refill_list=[feed_refill_date,feed_refill_time,feed_refill_zoo,feed_refill_qty,'dumped']
    return feed_refill_list
def feed_consumed():
    feed_consumed_list=[]    
    feed_consumed_date=input("Enter feed consumed date(mm-dd-yy) in quotes: ")
    feed_consumed_time=input("Enter feed consumed time(hh:mm) in quotes: ")
    feed_consumed_zoo=input("Enter consumed zoo number(1-215): ")
    feed_consumed_qty=input("Enter feed consumed in quantity(lbs): ")
    feed_consumed_animal=input("Enter feeed consumed by animal_number: ")
    feed_consumed_species=input("Enter feed consumed species category: ")
    feed_consumed_list=[feed_consumed_date,feed_consumed_time,feed_consumed_zoo,feed_consumed_qty,feed_consumed_animal,feed_consumed_species]
    return feed_consumed_list
##Setting paths
path=os.getcwd()
os.chdir(path)
if os.path.isfile('feed_refill_table.csv'):
    feed_refill_table=pd.read_csv('feed_refill_table.csv')
else:
    feed_refill_table=pd.DataFrame(columns=['feed_refill_date','feed_refill_time','feed_refill_zoo','feed_refill_qty','flag'])

if os.path.isfile('feed_consumption_table.csv'):
    feed_consumption_table=pd.read_csv('feed_consumption_table.csv')
else:    
    feed_consumption_table=pd.DataFrame(columns=['feed_consumed_date','feed_consumed_time','feed_consumed_zoo','feed_consumed_qty','feed_consumed_animal','feed_consumed_species'])

if os.path.isfile('wastage_table.csv'):
    wastage_table=pd.read_csv('wastage_table.csv')
else:    
    wastage_table=pd.DataFrame(columns=['wastage_date','wastage_for_zoo','wastage_qty'])

##Main prog
print 'Welcome to the IZI zoo'

while(True):
    print '\n'
    choice=input('\n'"Select your option-" '\n' 
                 "  Vendor Refill Inventory:1" '\n' 
                 "  Feed consumption for species:2" '\n' 
                 "  Reports:3" '\n' 
                 "  Exit Menu:4"'\n''\n')
    
	if(choice==1):
		n_entry=feed_refill()
		o_entry=feed_refill_table[feed_refill_table['feed_refill_zoo']==n_entry[2]]
		if(len(o_entry['flag']=='consumed')>0 or len(o_entry['flag']=='dumped')>0):
			w_entry=o_entry[-1:].values.flatten()
			wastage_table=wastage_table.append({'wastage_date':w_entry[0],'wastage_for_zoo':w_entry[2],'wastage_qty':w_entry[3]},ignore_index=True)
			print '\n''wastage added'
		feed_refill_table=feed_refill_table.append({'feed_refill_date':n_entry[0],'feed_refill_time':n_entry[1],'feed_refill_zoo':n_entry[2],'feed_refill_qty':n_entry[3],'flag':n_entry[4]},ignore_index=True)
		print '\n''refill added' 

	elif(choice==2):
		n_entry=feed_consumed()
		feed_consumption_table=feed_consumption_table.append({'feed_consumed_date':n_entry[0],'feed_consumed_time':n_entry[1],'feed_consumed_zoo':n_entry[2],'feed_consumed_qty':n_entry[3],'feed_consumed_animal':n_entry[4],'feed_consumed_species':n_entry[5]},ignore_index=True)
		o_entry=feed_refill_table[feed_refill_table['feed_refill_zoo']==n_entry[2]][-1:].values.flatten()
		o_entry[3]= o_entry[3]-n_entry[3]
		o_entry[4]='consumed'
		feed_refill_table=feed_refill_table.append({'feed_refill_date':o_entry[0],'feed_refill_time':o_entry[1],'feed_refill_zoo':o_entry[2],'feed_refill_qty':o_entry[3],'flag':o_entry[4]},ignore_index=True)
		print '\n''quantity updated'

	elif(choice==3):
		print 'reports''\n'
		print 'Each animal fed per day on average''\n'
		print feed_consumption_table.groupby(['feed_consumed_animal','feed_consumed_date']).mean()['feed_consumed_qty']
		print 'Number of times per day are animals fed on average''\n'
		print feed_consumption_table.groupby(['feed_consumed_date','feed_consumed_species','feed_consumed_animal']).count()['feed_consumed_time']
		print 'Amount of food wasted per zoo''\n'
		print wastage_table.groupby(['wastage_for_zoo']).mean()
		print 'average consumption by species''\n'
		print feed_consumption_table.groupby(['feed_consumed_species']).mean()
		print '\n'

		elif(choice==4):
		save_tables(feed_refill_table,feed_consumption_table)
        break
    	break

