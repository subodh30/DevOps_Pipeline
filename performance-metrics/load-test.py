import asyncio
import time
import httpx
import sys
import matplotlib.pyplot as plt

async def fetch_url(url):
    async with httpx.AsyncClient() as client:
        start_time = time.time()
        response = await client.get(url)
        end_time = time.time()
        return end_time - start_time

async def main(url, num_requests):
    times = []
    tasks = [fetch_url(url) for _ in range(num_requests)]

    for task in asyncio.as_completed(tasks):
        response_time = await task
        times.append(response_time)

    return times

if __name__ == "__main__":
    url = "http://"+str(sys.argv[1])
    num_requests = 1000

    response_times = asyncio.run(main(url, num_requests))

    avg_response_time = sum(response_times)/num_requests
    print(f"Average Response Time: {avg_response_time}" )
    # Plotting the response times
    plt.plot(range(1, num_requests + 1), response_times, marker='o', linestyle='-', color='b')
    plt.title('Response Times for {} Requests'.format(num_requests))
    plt.xlabel('Request Number')
    plt.ylabel('Response Time (seconds)')
    plt.grid(True)

    plt.savefig('response_times_plot.png')

    plt.show()

    if avg_response_time >= 5.0:
        raise Exception("Average Time is more than 5 seconds.")
