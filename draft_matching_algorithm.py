# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 16:44:28 2024
Draft Matching Algorithm
@author: Jan
"""
import numpy as np

### unique list function
def unique(list_input):
    
    
    unique_list = []
    
    for x in list_input:
        if x not in unique_list:
                unique_list.append(x)
                
    return unique_list
#%%
### Total number of professors
professors = 15
recruits = 15


### generating list of professors
prof_list = np.arange(0,professors)
recruit_list = np.arange(0,recruits)

#### Student ranking list
### rows is professor being ranked
###  columns is student doing ranking

recruit_ranks = np.zeros([recruits,professors])

# recruit_ranks = np.array([[1, 2, 1]
#                           [2, 3, 3],
#                           [3, 4, 2],
#                           [4, 1, 4]])

### Randomly Generate Recruit Rankings
for y in range(recruits):
    recruit_ranks[:,y] = np.arange(1,professors+1)    
    
    
#### professor ranking list
### rows is student being ranked
###  columns is professor doing ranking

professor_ranks = np.zeros([recruits,professors])

# professors_ranks = np.array([[1, 2, 3, 3],
#                              [2, 1, 2, 1],
#                              [3, 3, 1, 2]])

### Randomly Generate Recruit Rankings
for x in range(professors):
    professor_ranks[:,x] = np.arange(1,recruits+1)




#### Maximum number of students per professor
# professor_max = [2,1,0,3]
professor_max = [2,2,0,3,8,4,2,2,2,2,2,2,2,2,2]
# professor_max = [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#### checks if recruited too many students
# if recruits > sum(professor_max):
#     raise ValueError("Recruited Too Many Students")
    
    
#### generates the sum ranking of student and recruits
sum_rank = np.zeros([professors,recruits])
for x in range(professors):
    for y in range(recruits):
        sum_rank[x,y] = recruit_ranks[x,y] + professor_ranks[y,x]

### generates a recruit_match_list        
recruit_matches = [-1 for x in range(recruits)]    

### number of loops
boots = 1000

#### empty lists
happiness_boots = []
recruit_matches_boots = []

# for loop for each set
for i in range(boots):
    
    #generates new array of number of students a professor takes
    num_curr_matches = np.zeros(professors)

    # randomly generate a list of professor draft order
    prof_draft_list = np.random.choice(prof_list,professors,replace = False).tolist()
    
    # generate list of all recruits left to match
    recruits_left = np.arange(0,recruits)    .tolist()
    
    #initialize which "pick" we are on
    curr_iter = 0
    
    #initialize total happy for the current bootstrap
    total_happy = 0
    
    #while loop until all recruits have been picked
    while len(recruits_left) > 0:
        
        try: #iterate through professor draft picks
            curr_prof = prof_draft_list[curr_iter]
        except:
            
            ##### breaks if no professor spots are left and there are still recruits
            # print("Recruited Too Many")
            # print("Leftover Recruits:")
            # print(recruits_left)
            break
        
        ### checks if the current professor has maxed out their students
        if num_curr_matches[curr_prof] == professor_max[curr_prof] :
            
            prof_draft_list.remove(curr_prof) ### removes professor from draft order if they are full
            if curr_iter >= len(prof_draft_list):
                curr_iter = 0 ### circles back to the next draft pick 
        else:
            
            
            ### finds the current best student match for the professor from the currently available recruits
            curr_rankings = np.argmin(sum_rank[curr_prof,recruits_left])
            
            ### calculates total happy
            total_happy = total_happy + sum_rank[curr_prof,recruits_left][curr_rankings]
            
            
            ### stores which professor that student matches with
            recruit_matches[recruits_left[curr_rankings]] = curr_prof
            
            
            ### keeps track of professor students
            num_curr_matches[curr_prof] = num_curr_matches[curr_prof] + 1
            
            # print(curr_prof,recruits_left[curr_rankings],sum_rank[curr_prof,recruits_left[curr_rankings]])
            
            ### selected student is removed from recruits left list
            recruits_left.remove(recruits_left[curr_rankings])
            
            
            ### checks iterations
            if curr_iter >= len(prof_draft_list) -1:
                curr_iter = 0 ## loops back to 0
            # elif len(prof_draft_list) == 0:
            #     curr_iter = 0 ##
            else:
                curr_iter += 1 ## goes to the next draft pick
                
    happiness_boots.append(total_happy)
    recruit_matches_boots.append(recruit_matches)

### finds the lowest happiness level
min_happy = np.min(happiness_boots)


### finds all the matches that had that happiness level
match_happy = [recruit_matches_boots[x] for x in np.argwhere(happiness_boots == min_happy)[:,0]]
    
### prints unique happy matches
print(unique(match_happy))
### (currently only finds one???, might be true if it is picked in a draft order)
### will not find the true global minimum, but that is computationally impossible
