import matplotlib.pyplot as plt

class Process:
    def __init__(self, pid, btime, arrival_time):
        self.pid = pid
        self.btime = btime
        self.arrival_time = arrival_time
        self.remaining_btime = btime
        self.wtime = 0
        self.ttime = 0
        self.last_executed = 0
        self.resource = 0
        self.state = "Not finished"
        self.control_info = "Round Robin"
        self.utilization = 0
        self.instances = 0  # Number of instances (quanta) the process has been executed
        self.start_time = None  # Start time of the process
        self.state_changes = []  # A list to keep track of state changes and times

def print_process_table(logs):
    print("\n   ID            PC            IR          Resume      Burst Time      Remaining Time       State")
    print("---------------------------------------------------------------------------------------------------")
    for log in logs:
        print(f"    {log[0]}       {log[1]}   {log[2]}   {log[3]}         {log[4]}                   {log[5]}     {log[6]}")

def round_robin(processes, quantum):
    time = 0
    done = False
    gantt_chart = []
    state_log = []  # For the State Log
    process_table_log = []  # For the Process Table
    
    previous_process = None
    while not done:
        done = True
        for p in sorted(processes, key=lambda x: x.arrival_time):
            if time < p.arrival_time:
                continue

            if p.remaining_btime > 0:
                done = False

                if previous_process != p.pid:
                    instruction = p.btime - p.remaining_btime + 1
                    next_instruction = instruction + 1 if p.remaining_btime > 1 else -1
                    process_table_log.append((
                        p.pid,
                        f"Process{p.pid}[{instruction}]",
                        f"Process{p.pid}[{instruction}]",
                        f"Process{p.pid}[{next_instruction}]",
                        p.btime,
                        p.remaining_btime - 1,
                        "Running" if p.remaining_btime > quantum else "Finished"
                    ))
                previous_process = p.pid

                p.state = "Not finished"
                
                if p.start_time is None:
                    p.start_time = time
                
                p.instances += 1 

                p.wtime += time - p.last_executed
                if p.remaining_btime > quantum:
                    gantt_chart.append((p.pid, time, time + quantum))
                    time += quantum
                    p.remaining_btime -= quantum
                else:
                    gantt_chart.append((p.pid, time, time + p.remaining_btime))
                    time += p.remaining_btime
                    p.remaining_btime = 0
                    p.state = "Finished"

                p.last_executed = time

    for p in processes:
        p.ttime = p.wtime + p.btime

    return gantt_chart, state_log, process_table_log

def print_gantt_chart(gantt_chart):
    fig, ax = plt.subplots(figsize=(12, 2))
    for idx, (pid, start, end) in enumerate(gantt_chart):
        ax.broken_barh([(start, end - start)], (0, 1), facecolors=('orange'), edgecolor=("black"))
        ax.text(start + (end-start)/2, 1.2, f"P{pid}", ha='center', va='center', fontsize=10)
    ax.set_xticks([entry[2] for entry in gantt_chart])
    ax.set_yticks([])
    ax.set_xlabel("Time")
    plt.tight_layout()
    plt.show()

def main():
    processes = []

    n = int(input("How many processes? (<=5): "))
    quantum = int(input("Quantum size? (<=3): "))

    for i in range(n):
        btime = int(input(f"Execution time for process P{i+1} (5-8 ms): "))
        arrival_time = int(input(f"Arrival time for process P{i+1} (for e.g: 0, 1, 2): "))

        processes.append(Process(i+1, btime, arrival_time))

    gantt_chart, state_log, process_table_log = round_robin(processes, quantum)

    avg_wait = sum([p.wtime for p in processes]) / n
    avg_turnaround = sum([p.ttime for p in processes]) / n

    print("\nRound Robin Scheduling\n")
    headers = ["Process", "State", "Start Time", "No. of Instances", "Control Info", "Quantum Size", "Arrival Time", "Execution Time", "Turnaround Time", "Resource", "Utilization"]
    format_string = "{:<10} {:<15} {:<12} {:<18} {:<15} {:<15} {:<15} {:<15} {:<18} {:<10} {:<15}"
    print(format_string.format(*headers))

    for p in processes:
        total_time = max(p.ttime for p in processes) 
        utilization_percent = (p.btime / total_time) * 100
        print(format_string.format(
            f"P{p.pid}", p.state, p.start_time or "-", p.instances, p.control_info, str(quantum), str(p.arrival_time), str(p.btime), str(p.ttime), str(p.resource), f"{utilization_percent:.2f}%"))

    print("\nState Log:")
    for log_entry in state_log:
        print(log_entry[1])

    print_process_table(process_table_log)

    print(f"\nAverage waiting time: {avg_wait:.2f}ms")
    print(f"Average turn around time: {avg_turnaround:.2f}ms")

    # Moving the Gantt chart display to the end
    print_gantt_chart(gantt_chart)

if __name__ == "__main__":
    main()
