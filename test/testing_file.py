import asyncio
import aiohttp
from valaw.client import Client, Exceptions

puuid = "ukY6gxfrxrRZrzo3BZVkEbIuJKNDUuIm8CbQ7cn85QhuDFrc9dEm94cEgkRg3jNmAxh3OHc8SYHL-g"

async def test_get_by_puuid(client):
    try:
        response = await client.GET_getByPuuid("example_puuid")
        print("GET_getByPuuid Response:", response)
    except Exceptions.RiotAPIResponseError as e:
        print("Error in GET_getByPuuid:", e)

async def test_get_by_riot_id(client):
    try:
        response = await client.GET_getByRiotId("example_game", "example_tag")
        print("GET_getByRiotId Response:", response)
    except Exceptions.RiotAPIResponseError as e:
        print("Error in GET_getByRiotId:", e)

async def test_get_by_access_token(client):
    try:
        response = await client.GET_getByAccessToken("Bearer example_token")
        print("GET_getByAccessToken Response:", response)
    except Exceptions.RiotAPIResponseError as e:
        print("Error in GET_getByAccessToken:", e)

async def test_get_active_shard(client):
    try:
        response = await client.GET_getActiveShard("example_puuid")
        print("GET_getActiveShard Response:", response)
    except Exceptions.RiotAPIResponseError as e:
        print("Error in GET_getActiveShard:", e)

async def test_get_content(client):
    try:
        response = await client.GET_getContent("eu")
        print("GET_getContent Response:", response)
    except Exceptions.RiotAPIResponseError as e:
        print("Error in GET_getContent:", e)

async def test_get_match(client):
    try:
        response = await client.GET_getMatch("example_match_id", "eu")
        print("GET_getMatch Response:", response)
    except Exceptions.RiotAPIResponseError as e:
        print("Error in GET_getMatch:", e)

async def test_get_matchlist(client):
    try:
        response = await client.GET_getMatchlist("example_puuid", "eu")
        print("GET_getMatchlist Response:", response)
    except Exceptions.RiotAPIResponseError as e:
        print("Error in GET_getMatchlist:", e)

async def test_get_recent(client):
    try:
        response = await client.GET_getRecent("competitive", "eu")
        print("GET_getRecent Response:", response)
    except Exceptions.RiotAPIResponseError as e:
        print("Error in GET_getRecent:", e)

async def test_get_leaderboard(client):
    try:
        response = await client.GET_getLeaderboard("act1", "eu")
        print("GET_getLeaderboard Response:", response)
    except Exceptions.RiotAPIResponseError as e:
        print("Error in GET_getLeaderboard:", e)

async def test_get_console_match(client):
    try:
        response = await client.GET_getConsoleMatch("example_console_match_id", "eu")
        print("GET_getConsoleMatch Response:", response)
    except Exceptions.RiotAPIResponseError as e:
        print("Error in GET_getConsoleMatch:", e)

async def test_get_console_matchlist(client):
    try:
        response = await client.GET_getConsoleMatchlist("example_puuid", "eu")
        print("GET_getConsoleMatchlist Response:", response)
    except Exceptions.RiotAPIResponseError as e:
        print("Error in GET_getConsoleMatchlist:", e)

async def test_get_console_recent(client):
    try:
        response = await client.GET_getConsoleRecent("competitive", "eu")
        print("GET_getConsoleRecent Response:", response)
    except Exceptions.RiotAPIResponseError as e:
        print("Error in GET_getConsoleRecent:", e)

async def test_get_platform_data(client):
    try:
        response = await client.GET_getPlatformData("eu")
        print("GET_getPlatformData Response:", response)
    except Exceptions.RiotAPIResponseError as e:
        print("Error in GET_getPlatformData:", e)

async def main():
    # Create a Client instance
    client = Client(token="your_api_token", cluster="americas")  # Replace with your actual token

    # Run all tests
    await test_get_by_puuid(client)
    await test_get_by_riot_id(client)
    await test_get_by_access_token(client)
    await test_get_active_shard(client)
    await test_get_content(client)
    await test_get_match(client)
    await test_get_matchlist(client)
    await test_get_recent(client)
    await test_get_leaderboard(client)
    await test_get_console_match(client)
    await test_get_console_matchlist(client)
    await test_get_console_recent(client)
    await test_get_platform_data(client)

    # Close the client session
    await client.close()

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
