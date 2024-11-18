class Bully:
    num_processes = 0
    alive_status = []

    @staticmethod
    def initialize(num_processes: int):
        Bully.num_processes = num_processes
        Bully.alive_status = [True for _ in range(num_processes)]

    @staticmethod
    def kill_process(id: int):
        if id < Bully.num_processes:
            Bully.alive_status[id] = False
        else:
            print(f"Error: Process ID {id} is out of range.")

    @staticmethod
    def start_process(id: int):
        if id < Bully.num_processes:
            Bully.alive_status[id] = True
        else:
            print(f"Error: Process ID {id} is out of range.")

    @staticmethod
    def election(initiator_id: int):
        if Bully.num_processes == 0 or not Bully.alive_status:
            print("Error: Bully class is not initialized. Call `initialize` first.")
            return

        if initiator_id >= Bully.num_processes:
            print(f"Error: Process ID {initiator_id} is out of range.")
            return

        if not Bully.alive_status[initiator_id]:
            print(f"Process {initiator_id} cannot hold election as it is down.")
            return

        print(f"Election started by process {initiator_id}")

        for i in range(initiator_id + 1, Bully.num_processes):
            print(f"ELECTION message sent to process {i} by process {initiator_id}")

        for i in range(initiator_id + 1, Bully.num_processes):
            if Bully.alive_status[i]:
                print(f"Process {i} responded OK to ELECTION")

        for i in range(initiator_id + 1, Bully.num_processes):
            if Bully.alive_status[i]:
                Bully.election(i)
                return

        bully_process = max(id for id in range(Bully.num_processes) if Bully.alive_status[id])
        print(f"New coordinator is {bully_process}")
        print(f"Coordinator {bully_process} informs everyone that it the new new coordinator")


# Initialize and run the algorithm
Bully.initialize(num_processes=6)
Bully.kill_process(5)
Bully.kill_process(4)
Bully.election(0)
