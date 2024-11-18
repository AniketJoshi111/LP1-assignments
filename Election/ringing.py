class Ring:
    num_processes = 0
    alive_status = []
    @staticmethod
    def kill_process(id:int):
        Ring.alive_status[id] = False
    
    @staticmethod
    def start_process(id:int):
        Ring.alive_status[id] = True
    @staticmethod
    def initiate(num_processes):
        Ring.num_processes = num_processes
        Ring.alive_status = [True for _ in range(num_processes)]
        
    @staticmethod
    def election(initiator_id:int):
        if initiator_id > Ring.num_processes:
            print("Not possible")
            return
        if not Ring.alive_status[initiator_id]:
            print(f"Process {initiator_id} cannot conduct election as it is down")
        
        start = initiator_id
        ptr = (start+1)%(Ring.num_processes)
        last_alive_process = start
        while(ptr!=start):
            if Ring.alive_status[ptr]:
               print(f"Process {last_alive_process} sends election message to {ptr}")
               last_alive_process = ptr
            ptr = (ptr+1)%(Ring.num_processes)
            
        print(f"Process {last_alive_process} sends election message to {ptr}")
        
        ring_process = max(id for id in range(Ring.num_processes) if Ring.alive_status[id])
        print(f"New Coordinator is {ring_process}")
        print(f"Process {ring_process} informs process informs everyone that it is new co-ordinator")
        
Ring.initiate(num_processes=6)

Ring.kill_process(1)
Ring.kill_process(3)
Ring.election(0)