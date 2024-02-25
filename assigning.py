import math
from typing import List, Any

from geopy.distance import distance

# Global Variables:-
STARTING_TIME = 5
INFINITY = 1000 * 1000 * 1000
VELOCITY = 1.5  # meter per sec.
TIME_REQUIRED_FOR_BASEMENT_CHANGE = 90  # meter per sec.
skipped_jobs = []
tenant_data = None

def getTimeRequired(t1, t2): 
    # returns time required in seconds
    global tenant_data
    # print(tenant_data)
    # Distance = distance((location1['latitude'],location1['longitude']), (location2['latitude'],location2['longitude'])).m
    Distance = distance((tenant_data['tenantBlocks'][t1]['locationCoordinates']['latitude'], tenant_data['tenantBlocks'][t1]['locationCoordinates']['longitude']),(tenant_data['tenantBlocks'][t2]['locationCoordinates']['latitude'], tenant_data['tenantBlocks'][t2]['locationCoordinates']['longitude'])).m
    return Distance / VELOCITY 

# def getTimeRequired(t1, b1, t2, b2):
#     # returns time required in seconds
#     global tenant_data
#     # Calculate travel time between towers
#     tower_travel_time = distance((tenant_data['tower_location'][t1]['latitude'], tenant_data['tower_location'][t1]['longitude']), (tenant_data['tower_location'][t2]['latitude'], tenant_data['tower_location'][t2]['longitude'])).m / VELOCITY
#     # Calculate travel time between basements
#     if b1 == b2:  # Same basement
#         basement_travel_time = 0
#     else:  # Different basements
#         basement_travel_time = abs(int(b2[1]) - int(b1[1])) * BASEMENT_TRAVEL_TIME
#     # Total travel time is the sum of tower travel time and basement travel time
#     return tower_travel_time + basement_travel_time



def timeRequired(jobA, jobB):
    # indA = tower_index[jobA.tower]
    # indB = tower_index[jobB.tower]
    # time = travellingTimes[indA][indB]
    time = getTimeRequired(jobA.tenantBlockId, jobB.tenantBlockId)
    time += TIME_REQUIRED_FOR_BASEMENT_CHANGE * abs(int(jobA.basement[1]) - int(jobB.basement[1]))
    # return time / 3600
    return time

def funopt1(jobs,workers,i,freq):
    # print("hello assigning")


    number_of_jobs = len(jobs)

    for i in range(i,number_of_jobs):
        min_time = INFINITY
        worker_id = None
        starttime=int(jobs[i].deadline[0] )
        for worker in workers:
            endwork=freq[worker][-1]
            endtime=int(endwork.deadline[1])

            
            time = timeRequired(freq[worker][-1],jobs[i])
            if(time<min_time):
                min_time = time
                worker_id = worker
        freq[worker_id].append(jobs[i])
    print("each worker has been assigned jobs")

    for key,val in freq.items():
        print(key)
        for job in val:
            job.pr()

    return jobs

def funopt(jobs,workers,i,freq):  
    number_of_jobs = len(jobs)

    while i<number_of_jobs:
        min_time = INFINITY
        worker_id = None
        ifSkipped = False
        time = 0
        for worker in workers:
            
            # print(freq[worker][-1].estimatedDuration)
            # print(timeRequired(freq[worker][-1],jobs[i]))
            if len(skipped_jobs) > 0 and len(freq[worker])<40:
                ifSkipped = True
                time = timeRequired(freq[worker][-1],skipped_jobs[0])
                # print(time)
                # print(skipped_jobs[0].estimatedDuration)

                freq[worker][0] += time + skipped_jobs[0].estimatedDuration
                freq[worker].append(skipped_jobs[0])
                skipped_jobs.pop(0)

                continue

            else:
                time = timeRequired(freq[worker][-1],jobs[i])   # time required to travel from last job to current job
                # print(time)
                # freq[worker][-1].estimatedDuration
                if(time<min_time and freq[worker][0] + time + jobs[i].estimatedDuration <= int(jobs[i].deadline[1])*3600 and len(freq[worker])<40):
                    min_time = time
                    worker_id = worker
                

        if worker_id == None:
            skipped_jobs.append(jobs[i])
        else:
            if not ifSkipped:
                freq[worker_id][0] += time + jobs[i].estimatedDuration
                freq[worker_id].append(jobs[i])
        i+=1
    print("each worker has been assigned jobs")


    
    for key,val in freq.items():
        
        print(key)
        print("Total time taken by worker :",val[0])
        print("jobs assigned to worker :",len(val)-1)
        for job in val[1:]:
            job.pr()
        print()
        

    print("skipped jobs:", len(skipped_jobs))
    for job in skipped_jobs:
        job.pr()
    return jobs
    

def assignJobs(tenant, jobs, workers):
    global tenant_data
    tenant_data = tenant
    print(workers)
    '''Your assigning logic goes here
    This method has to return a dictionay where the key is the worker_id and the value contains a list of jobs basis sorted by the assigning order
    '''
    #workers dictionary

    for job in jobs:
        time=job.deadline.split("-")

        for i in range(len(time)):
            if len(time[i])==3:
                time[i] = "0"+time[i][0]
            else:
                time[i]=time[i][:2]
        
        job.deadline =time
      
        
        
    #sorting jobs by deadline
    
    jobs = list(sorted(jobs, key=lambda x:(x.deadline[0],int(x.vehicleId[3:]))) ) 
    # print("hello assigning")
    # for job in jobs:
    #     job.pr() 

    #creating a dictionary for workers  
    freq={}
    for worker in workers:
        freq[worker] = [5 * 60 * 60]  # starting time is 5:00 AM




    #assingining  single job to each worker
    i=0
    number_of_jobs = len(jobs)

    for key,val in freq.items():
        if(i<number_of_jobs):
            freq[key].append(jobs[i])
            freq[key][0] += jobs[i].estimatedDuration
            i+=1
        else:
            break
    
    jobs = funopt(jobs,workers,i,freq)


    
    # funopt1(jobs,workers,i,freq)

    #assigning remaining jobs to workers
    # for i in range(i,number_of_jobs):
    #     min_time = INFINITY
    #     worker_id = None
    #     for worker in workers:
    #         if(len(freq[worker])>0):
    #             time = timeRequired(freq[worker][-1],jobs[i])
    #             if(time<min_time):
    #                 min_time = time
    #                 worker_id = worker
    #     freq[worker_id].append(jobs[i])
    # print("each worker has been assigned jobs")

    # for key,val in freq.items():
    #     print(key)
    #     for job in val:
    #         job.pr()

    # print("hello assigning"\)

    # for job in jobs:
    #     job.pr()
    return jobs  