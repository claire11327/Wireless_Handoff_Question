import matplotlib.pyplot as plt
import random
import math

turn = 0 # more close to actual sec*cars amount
n = 0
Cars = []

total = 86400

hoff = [0,0,0,0]
 # for plot_y
handoff_0 = [0 for i in range(total)]
handoff_1 = [0 for i in range(total)]
handoff_2 = [0 for i in range(total)]
handoff_3 = [0 for i in range(total)]



# Base location (left down corner = (0,0))
Base = [[ 750, 750],[2250, 750],[2250,2250],[ 750,2250]]


time = 0 # for loop 86400
times = [i for i in range(total)]  # for plot_x
# record init_time + 75*t 
  ## [t:# of times at intersection]
time_record = [] 

avg_power = [0,0,0,0]

# direction vector
  # left turn + 1 , right turn -1
  # first dir = dir_vec[entry num / 3]
dir_vec = [[0,10],[-10,0],[0,-10],[10,0]]

# entry
Entry = [[750,0],[1500,0],[2250,0],[3000,750],[3000,1500],[3000,2250],[750,3000],[1500,3000],[2250,3000],[   0,750],[   0,1500],[   0,2250]]



class Car_struct:
    def __init__(self):
        self.dir = 0
        self.loc = [0,0]
        self.init_t = 0        
        self.now_B = [0,0,0,0]
        self.now_P = [-130,-130,-130,-130]


def list_add(a,b):
    c = []
    for i in range(len(a)):
        c.append(a[i]+b[i])
    return c

def init_now_B(access):
  now_B = [0,0,0,0]
  if access < 2 or access == 11:
    now_B = [0,0,0,0]
  elif access < 5:
    now_B = [1,1,1,1]
  elif access < 8:
    now_B = [2,2,2,2]
  else:
    now_B = [3,3,3,3]
  return now_B


def calculate_power(x,y,Base_x,Base_y):
  if(x == Base_x and y == Base_y):
    P = -50
  else:
    d = ((Base_x - x)**2 + (Base_y - y)**2)**0.5
    if d <= 1:
        P = -60
    P = -60 - 20*math.log10(d)
  return P

# now_dir = Cars[].dir
def change_dir(now_dir):
  forward_dir = [0,0,0,-1,-1,1]
  now_dir += random.choice(forward_dir)
  if now_dir < 0:
    now_dir += 4
  elif now_dir > 3:
    now_dir -= 4
  return now_dir




# pre_loc = Cars[].loc + dir_vec[Cars[].dir]
def change_Base_hoff(pre_loc_x,pre_loc_y,Bases_loc,hoff,now_B,now_P,cari):
  kk = 0
        
  P_big = -130
  big   = 0
  P     = [-130,-130,-130,-130]
  #print("now_B = ",now_B[0])
  for j in range(4):
    P[j] = calculate_power(pre_loc_x,pre_loc_y,Bases_loc[j][0],Bases_loc[j][1])

    if P[j] > P_big:
      big = j
      P_big = P[j] 
      
  #if cari == 0 and P_big != P[now_B[2]]:
     # print("P_big = ",P_big,"P[] = ",P[now_B[2]])
     # print("big = ",big,"now_B[2] = ",now_B[2])




  # change
  # principle_1 ## Pnew > Pold
  if big != now_B[0]: # P[big] > now_B[0]
      now_B[0] = big
      hoff[0] += 1
    
    # principle_2 ## Pnew > Pold & Pold < T
  if now_P[1] < -110 and big != now_B[1]: # T = -110
      now_B[1] = big
      hoff[1] += 1
    
    # principle_3 ## Pnew > Pold + E    "
  if P_big > (P[now_B[2]]+5) and big != now_B[2]: # E = 5      
      now_B[2] = big
      hoff[2] += 1
      kk = 1
    
    # principle_4
  d_old = (pre_loc_x - Bases_loc[now_B[3]][0])**2 + (pre_loc_y - Bases_loc[now_B[3]][1])**2
  d_new = (pre_loc_x - Bases_loc[big][0])**2 + (pre_loc_y - Bases_loc[big][1])**2
  if big != now_B[3] and d_new < d_old: # P[big] > now_B[3]:
      now_B[3] = big
      hoff[3] += 1
 

  #if kk != 0 and cari == 0:
      #print("-----------------")


  return now_B


def remove(Cars,time_record,x,y,i):
  if x > 3000 or x < 0 or y > 3000 or y < 0:
    del Cars[i-1]
    del time_record[i-1]
    return True




# main
for time in range(total):
  #j = 0
  #for j in range(11): 
    #access = j
  if random.randint(1,31) == 1:
    n += 1
    access = random.randint(0,11)   # choose entry
    # new / init car
    car = Car_struct()
    car.loc = Entry[access]
    car.dir = change_dir(math.floor(access/3))
    car.init_t = time # time start at t = 0
    car.now_B = init_now_B(access)
    Cars.append(car)
    time_record.append((time)+75) # time = car.init_t

  # for each sec
  i = 0
  while i < len(Cars):
    turn += 1
    Cars[i].loc = list_add(Cars[i].loc,dir_vec[Cars[i].dir])
    
    for j in range(4):
      Base_index = Cars[i].now_B[j]
      Cars[i].now_P[j] = calculate_power(Cars[i].loc[0],Cars[i].loc[1],Base[Base_index][0], Base[Base_index][1])
      # avg_power
      avg_power[j] += Cars[i].now_P[j]

  
    k = i  
    x = Cars[k].loc[0]
    y = Cars[k].loc[1]
    
          
    Cars[k].now_B = change_Base_hoff(Cars[i].loc[0],Cars[i].loc[1],Base,hoff,Cars[k].now_B,Cars[k].now_P,i)
    
    
    
    
    if remove(Cars,time_record,Cars[i].loc[0],Cars[i].loc[1],i):
      i += 1
    i+= 1


  # each % 75 == 0 sec, judge direction
  i = 0
  f = [i for i,v in enumerate(time_record) if v==(time)]
  for i in range(len(f)):
  #if (time) in time_record:
    k = f[i] # get index k
    # change_dir
    Cars[k].dir = change_dir(Cars[k].dir)
    time_record[k] += 75












  # each % 75 == 0 sec
  '''
  i = 0
  f = [i for i,v in enumerate(time_record) if v==(time)]
  for i in range(len(f)):
  #if (time) in time_record:
    k = f[i] # get index k
    # change_dir
    Cars[k].dir = change_dir(Cars[k].dir)
    # change_Base_hoff
    pre_loc = [0,0]
    x = Cars[k].loc[0] + dir_vec[Cars[k].dir][0]
    y = Cars[k].loc[1] + dir_vec[Cars[k].dir][1]
      
    Cars[k].now_B = change_Base_hoff(x,y,Base,hoff,Cars[k].now_B,Cars[k].now_P)
        
    # add 75 sec 
    time_record[k] += 75
  '''
    
  handoff_0[time] = hoff[0]
  handoff_1[time] = hoff[1]
  handoff_2[time] = hoff[2]
  handoff_3[time] = hoff[3]

plt.figure()
plt.plot(times,handoff_0,label="$Best$",color="red")
plt.plot(times,handoff_1,label="$Threshold$",color="yellow")
plt.plot(times,handoff_2,label="$E..$",color="green")
plt.plot(times,handoff_3,label="$Mine$",color="blue")
plt.show()

#print(handoff_3)

print(avg_power[0]/(total*n))
print(avg_power[1]/(total*n))
print(avg_power[2]/(total*n))
print(avg_power[3]/(total*n))


