import asyncio
import time
import httpx
import paramiko
import sys
import matplotlib.pyplot as plt

async def send_requests(server_url, request_rate, duration_minutes):
    async with httpx.AsyncClient() as client:
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)

        while time.time() <= end_time:
            try:
                response = await client.get(server_url)
                if response.status_code != 200:
                    print(f"HTTP request to {server_url} failed with status code {response.status_code}")
            except Exception as e:
                print(f"Error during HTTP request to {server_url}: {e}")

            await asyncio.sleep(1 / request_rate)


async def monitor_remote_resources(server_address, username, password, interval_seconds, cpu_usage, memory_usage, duration_minutes):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(server_address, username=username, password=password)

    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)

    while time.time() <= end_time:
        cpu_output, memory_output = get_remote_resources(ssh_client)
        process_resource_data(cpu_output, memory_output, cpu_usage, memory_usage)
        time.sleep(interval_seconds)

    ssh_client.close()

def get_remote_resources(ssh_client):
    cpu_command = "top -bn1 | grep 'Cpu(s)' | sed \"s/.*, *\\([0-9.]*\\)%* id.*/\\1/\" | awk '{print 100 - $1}'"
    mem_command = "free | awk 'FNR == 2 { print $3/$2*100 }'"

    cpu_stdin, cpu_stdout, cpu_stderr = ssh_client.exec_command(cpu_command)
    memory_stdin, memory_stdout, memory_stderr = ssh_client.exec_command(mem_command)

    cpu_output = cpu_stdout.read().decode().strip()
    memory_output = memory_stdout.read().decode().strip()

    return cpu_output, memory_output

def process_resource_data(cpu_output, memory_output, cpu_usage, memory_usage):
    if cpu_output and memory_output:
        cpu_percent = float(cpu_output)
        memory_percent = float(memory_output)

        print(f"Server Resources - CPU Usage: {cpu_percent}%  |  Memory Usage: {memory_percent}%")
        cpu_usage.append(cpu_percent)
        memory_usage.append(memory_percent)
    else:
        print("Error: Unable to retrieve CPU or memory information")

def plot_comparison_graph(cpu_usage1, memory_usage1, cpu_usage2, memory_usage2, address1, address2, monitoring_interval):
    plt.figure(figsize=(12, 6))

    # CPU Usage Comparison
    plt.subplot(1, 2, 1)
    plt.plot(cpu_usage1, label=address1)
    plt.plot(cpu_usage2, label=address2)
    plt.title('CPU Usage Comparison')
    plt.xlabel(f'Time ({monitoring_interval}-second intervals)')
    plt.ylabel('CPU Usage (%)')
    plt.legend()

    # Memory Usage Comparison
    plt.subplot(1, 2, 2)
    plt.plot(memory_usage1, label=address1)
    plt.plot(memory_usage2, label=address2)
    plt.title('Memory Usage Comparison')
    plt.xlabel(f'Time ({monitoring_interval}-second intervals)')
    plt.ylabel('Memory Usage (%)')
    plt.legend()

    plt.tight_layout()
    plt.savefig('performance_comparison.png')
    plt.show()

async def main():
    server1_url = f"http://{sys.argv[1]}:3000"
    server2_url = f"http://{sys.argv[2]}:3000"
    request_rate = 20         # requests per second
    monitoring_interval = 2  # seconds
    duration_minutes = int(sys.argv[5])     # minutes 

    server1_address = str(sys.argv[1])
    server1_username = str(sys.argv[3])
    server1_password = str(sys.argv[4])

    server2_address = str(sys.argv[2])
    server2_username = str(sys.argv[3])
    server2_password = str(sys.argv[4])

    cpu_usage_server1 = []
    memory_usage_server1 = []

    cpu_usage_server2 = []
    memory_usage_server2 = []

    tasks = [
        asyncio.create_task(send_requests(server1_url, request_rate, duration_minutes)),
        asyncio.create_task(send_requests(server2_url, request_rate, duration_minutes)),
        asyncio.create_task(monitor_remote_resources(server1_address, server1_username, server1_password, monitoring_interval, cpu_usage_server1, memory_usage_server1, duration_minutes)),
        asyncio.create_task(monitor_remote_resources(server2_address, server2_username, server2_password, monitoring_interval, cpu_usage_server2, memory_usage_server2, duration_minutes))
    ]

    await asyncio.gather(*tasks)

    plot_comparison_graph(cpu_usage_server1, memory_usage_server1, cpu_usage_server2, memory_usage_server2, server1_address, server2_address, monitoring_interval)
    
    avg_cpu_1 = sum(cpu_usage_server1) / len(cpu_usage_server1)
    avg_cpu_2 = sum(cpu_usage_server2) / len(cpu_usage_server2)
    
    if avg_cpu_1 > (avg_cpu_2 * 1.25):
        raise Exception("CPU usage is higher than production")
        sys.exit(1)
        
    avg_mem_1 = sum(memory_usage_server1) / len(memory_usage_server1)
    avg_mem_2 = sum(memory_usage_server2) / len(memory_usage_server2)
    
    if avg_mem_1 > (avg_mem_2 * 1.25):
        raise Exception("Memory usage is higher than production")
        sys.exit(1)
        
        


if __name__ == "__main__":
    asyncio.run(main())
