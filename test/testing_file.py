import asyncio
import os
from valaw.client import Client, Exceptions

async def main():
    # Create a Client instance
    RIOT_API_KEY = os.getenv("RIOT_API_KEY")
    client = Client(token=RIOT_API_KEY, cluster="americas", raw_data=True)

    getByRiotId = await client.GET_getByRiotId(gameName="jet", tagLine="612")
    print(getByRiotId)

    

    # Close the client session
    await client.close()

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
