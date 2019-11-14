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


def list_add(a,b,k):
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
def change_Base_hoff(loc,Bases_loc,hoff,now_B,cari):
        
  P_big = -130
  big   = 0
  P     = [-130,-130,-130,-130]
  
  for j in range(4):
    P[j] = calculate_power(loc[0],loc[1],Bases_loc[j][0],Bases_loc[j][1])

    if P[j] > P_big:
      big = j
      P_big = P[j] 
      
      

  # change
  # principle_1 ## Pnew > Pold
  if P_big > P[now_B[0]]: # P[big] > now_B[0]
      now_B[0] = big
      hoff[0] += 1
      
    
    # principle_2 ## Pnew > Pold & Pold < T
  if P[now_B[1]] < -110 and P_big > P[now_B[1]]: # T = -110
      now_B[1] = big
      hoff[1] += 1
    
    # principle_3 ## Pnew > Pold + E    "
  if P_big > (P[now_B[2]]+5):  # E = 5      
      now_B[2] = big
      hoff[2] += 1
    
    # principle_4 ## Pold < -120
  if P[now_B[3]] < -120 and P_big > P[now_B[3]]:
      now_B[3] = big
      hoff[3] += 1
 
  avg_power[0] += P[now_B[0]]
  avg_power[1] += P[now_B[1]]
  avg_power[2] += P[now_B[2]]
  avg_power[3] += P[now_B[3]] 


  if cari == 0:
      print("P = ",P)
     
  return now_B




def remove(Cars,time_record,x,y,i):
  #if i == 0:
      #print(" remove x = ",x,"  y = ", y)
  if x > 3000 or x < 0 or y > 3000 or y < 0:
    print("in remove x = ",x,"  y = ", y)
    del Cars[i]
    del time_record[i]
    return True




# main
for time in range(total):
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




  # each % 75 == 0 sec, judge direction
  i = 0
  #f = [i for i,v in enumerate(time_record) if v==(time)]
  #for i in range(len(f)):
  '''
  for index, t in enumerate(time_record):
    if t == time:
        k = index
        #if (time) in time_record:
        #k = f[i] # get index k
        # change_dir
        Cars[k].dir = change_dir(Cars[k].dir)
        '''

  # for each sec
  i = 0
  while i < len(Cars):
    if i == 0:
        print(time, "dir ",dir_vec[Cars[0].dir],"loc ", Cars[0].loc,"B ",Cars[0].now_B)
    #print(dir_vec[Cars[0].dir])
    #print(Cars[0].loc)
    #print(Cars[0].now_B)
    #print("-----")
    
    if (Cars[i].loc[0] % 750 == 0 and Cars[i].loc[1] % 750 == 0 ):
      Cars[i].dir = change_dir(Cars[i].dir)
      
      x = Cars[i].loc[0]
      y = Cars[i].loc[1]
      if i == 0:
          print("x = ",x," y = ",y)
    # if car is at the corner
      if (x == 0 and y == 0):
          if Cars[i].dir == 2:
              Cars[i].dir = 3
          else: 
              Cars[i].dir = 0
      if (x == 3000 and y == 0):
          if Cars[i].dir == 3:
              Cars[i].dir = 0
          else: 
              Cars[i].dir = 1
      if (x == 0 and y == 3000):
          if Cars[i].dir == 0:
              Cars[i].dir = 3
          else: 
              Cars[i].dir = 2
      if (x == 3000 and y == 3000):
          print("turn r/l:x = ",x," y = ",y)
          if Cars[i].dir == 3:
              Cars[i].dir = 2
          else: 
              Cars[i].dir = 1
      time_record[i] += 75
        
    
    
    turn += 1
    Cars[i].loc = list_add(Cars[i].loc,dir_vec[Cars[i].dir],i)        
    if remove(Cars,time_record,Cars[i].loc[0],Cars[i].loc[1],i):
      i += 1
    if(i < len(Cars)):
      Cars[i].now_B = change_Base_hoff(Cars[i].loc,Base,hoff,Cars[i].now_B,i)
    

    i+= 1






  handoff_0[time] = hoff[0]*12
  handoff_1[time] = hoff[1]*12
  handoff_2[time] = hoff[2]*12
  handoff_3[time] = hoff[3]*12

plt.figure()
plt.plot(times,handoff_0,label="$Best$",color="red")
plt.plot(times,handoff_1,label="$Threshold$",color="yellow")
plt.plot(times,handoff_2,label="$E..$",color="green")
plt.plot(times,handoff_3,label="$Mine$",color="blue")
plt.show()


print(avg_power[0]/(total*n))
print(avg_power[1]/(total*n))
print(avg_power[2]/(total*n))
print(avg_power[3]/(total*n))


