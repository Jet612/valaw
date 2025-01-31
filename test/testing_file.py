import asyncio
import json
from valaw.client import Client, Exceptions
from datetime import datetime

def what_is_missing(obj, json_dict):
    # Get the fields of the object
    obj_fields = vars(obj)  # or obj.__dict__
    
    # Ensure all keys in json_dict are strings and not None
    json_keys = [key for key in json_dict.keys() if key is not None]
    
    # Find missing fields
    missing_fields = [field for field in json_keys if field not in obj_fields]
        
    with open(datetime.now().strftime("raw-%Y-%m-%d_%H-%M-%S.json"), "w") as f:
        json.dump(json_dict, f)

    return missing_fields


def has_all_fields(obj, json_dict):
    obj_fields = vars(obj)  # or obj.__dict__
    return all(field in obj_fields for field in json_dict.keys())

async def main(key):
    # Create a Client instance
    client = Client(token=key, cluster="americas")
    client_raw = Client(token=key, cluster="americas", raw_data=True)
    test_puuid = None
    test_act_id = None
    test_puuid_console = None

    # Regular API
    try:
        getContent = await client.GET_getContent(region="na", locale="en-US")
        getContentRaw = await client_raw.GET_getContent(region="na", locale="en-US")
        if getContent and getContentRaw and not has_all_fields(getContent, getContentRaw):
            print("GET_getContent is missing the following fields: ", 
                  what_is_missing(getContent, getContentRaw))
    except Exceptions.RiotAPIResponseError as e:
        print(f"GET_getContent failed with status code {e.status_code} and message {e.message}")
    except Exception as e:
        print(f"GET_getContent failed with error: {e}")

    try:
        getRecent = await client.GET_getRecent(queue="competitive", region="na")
        getRecentRaw = await client_raw.GET_getRecent(queue="competitive", region="na")
        if getRecent and getRecentRaw and not has_all_fields(getRecent, getRecentRaw):
            print("GET_getRecent is missing the following fields: ", 
                  what_is_missing(getRecent, getRecentRaw))
    except Exceptions.RiotAPIResponseError as e:
        print(f"GET_getRecent failed with status code {e.status_code} and message {e.message}")
    except Exception as e:
        print(f"GET_getRecent failed with error: {e}")

    # Ensure getRecent is defined before using it
    if getRecent:
        try:
            getMatch = await client.GET_getMatch(matchId=getRecent.matchIds[0], region="na")
            getMatchRaw = await client_raw.GET_getMatch(matchId=getRecent.matchIds[0], region="na")
            if getMatch and getMatchRaw and not has_all_fields(getMatch, getMatchRaw):
                print("GET_getMatch is missing the following fields: ", 
                      what_is_missing(getMatch, getMatchRaw))
        except Exceptions.RiotAPIResponseError as e:
            print(f"GET_getMatch failed with status code {e.status_code} and message {e.message}")
        except Exception as e:
            print(f"GET_getMatch failed with error: {e}")

        if getMatch:
            test_puuid = getMatch.players[0].puuid
            test_act_id = getMatch.matchInfo.seasonId

    if test_puuid is not None:
        try:
            getMatchlist = await client.GET_getMatchlist(puuid=test_puuid, region="na")
            getMatchlistRaw = await client_raw.GET_getMatchlist(puuid=test_puuid, region="na")
            if getMatchlist and getMatchlistRaw and not has_all_fields(getMatchlist, getMatchlistRaw):
                print("GET_getMatchlist is missing the following fields: ", 
                      what_is_missing(getMatchlist, getMatchlistRaw))
        except Exceptions.RiotAPIResponseError as e:
            print(f"GET_getMatchlist failed with status code {e.status_code} and message {e.message}")
        except Exception as e:
            print(f"GET_getMatchlist failed with error: {e}")
    else:
        print("getMatchlist Failed Because of No PUUID")

    if test_act_id is not None:
        try:
            getLeaderboard = await client.GET_getLeaderboard(actId=test_act_id, region="na")
            getLeaderboardRaw = await client_raw.GET_getLeaderboard(actId=test_act_id, region="na")
            if getLeaderboard and getLeaderboardRaw and not has_all_fields(getLeaderboard, getLeaderboardRaw):
                print("GET_getLeaderboard is missing the following fields: ", 
                      what_is_missing(getLeaderboard, getLeaderboardRaw))
        except Exceptions.RiotAPIResponseError as e:
            print(f"GET_getLeaderboard failed with status code {e.status_code} and message {e.message}")
        except Exception as e:
            print(f"GET_getLeaderboard failed with error: {e}")
    else:
        print("getLeaderboard Failed Because of No ACT ID")

    # Console API
    try:
        getConsoleRecent = await client.GET_getConsoleRecent(queue="console_competitive", region="na")
        getConsoleRecentRaw = await client_raw.GET_getConsoleRecent(queue="console_competitive", region="na")
        if getConsoleRecent and getConsoleRecentRaw and not has_all_fields(getConsoleRecent, getConsoleRecentRaw):
            print("GET_getConsoleRecent is missing the following fields: ", 
                  what_is_missing(getConsoleRecent, getConsoleRecentRaw))
    except Exceptions.RiotAPIResponseError as e:
        print(f"GET_getConsoleRecent failed with status code {e.status_code} and message {e.message}")
    except Exception as e:
        print(f"GET_getConsoleRecent failed with error: {e}")

    if getConsoleRecent:
        try:
            getConsoleMatch = await client.GET_getConsoleMatch(matchId=getConsoleRecent.matchIds[0], region="na")
            getConsoleMatchRaw = await client_raw.GET_getConsoleMatch(matchId=getConsoleRecent.matchIds[0], region="na")
            if getConsoleMatch and getConsoleMatchRaw and not has_all_fields(getConsoleMatch, getConsoleMatchRaw):
                print("GET_getConsoleMatch is missing the following fields: ", 
                      what_is_missing(getConsoleMatch, getConsoleMatchRaw))
        except Exceptions.RiotAPIResponseError as e:
            print(f"GET_getConsoleMatch failed with status code {e.status_code} and message {e.message}")
        except Exception as e:
            print(f"GET_getConsoleMatch failed with error: {e}")

        if getConsoleMatch:
            test_puuid_console = getConsoleMatch.players[0].puuid

            if test_puuid_console is not None:
                try:
                    getConsoleMatchlist = await client.GET_getConsoleMatchlist(
                        puuid=test_puuid_console, region="na", platformType="playstation")
                    getConsoleMatchlistRaw = await client_raw.GET_getConsoleMatchlist(
                        puuid=test_puuid_console, region="na", platformType="playstation")
                    if getConsoleMatchlist and getConsoleMatchlistRaw and not has_all_fields(getConsoleMatchlist, getConsoleMatchlistRaw):
                        print("GET_getConsoleMatchlist is missing the following fields: ", 
                              what_is_missing(getConsoleMatchlist, getConsoleMatchlistRaw))
                except Exceptions.RiotAPIResponseError as e:
                    print(f"GET_getConsoleMatchlist playstation failed with status code {e.status_code} and message {e.message}")
                except Exception as e:
                    print(f"GET_getConsoleMatchlist playstation failed with error: {e}")

                try:
                    getConsoleMatchlist = await client.GET_getConsoleMatchlist(
                        puuid=test_puuid_console, region="na", platformType="xbox")
                    getConsoleMatchlistRaw = await client_raw.GET_getConsoleMatchlist(
                        puuid=test_puuid_console, region="na", platformType="xbox")
                    if getConsoleMatchlist and getConsoleMatchlistRaw and not has_all_fields(getConsoleMatchlist, getConsoleMatchlistRaw):
                        print("GET_getConsoleMatchlist is missing the following fields: ", 
                              what_is_missing(getConsoleMatchlist, getConsoleMatchlistRaw))
                except Exceptions.RiotAPIResponseError as e:
                    print(f"GET_getConsoleMatchlist xbox failed with status code {e.status_code} and message {e.message}")
                except Exception as e:
                    print(f"GET_getConsoleMatchlist xbox failed with error: {e}")
            else:
                print("getConsoleMatchlist Failed Because of No PUUID")

    if test_act_id is not None:
        try:
            getConsoleLeaderboard = await client.GET_getConsoleLeaderboard(
                actId=test_act_id, region="na", platformType="playstation")
            getConsoleLeaderboardRaw = await client_raw.GET_getConsoleLeaderboard(
                actId=test_act_id, region="na", platformType="playstation")
            if getConsoleLeaderboard and getConsoleLeaderboardRaw and not has_all_fields(getConsoleLeaderboard, getConsoleLeaderboardRaw):
                print("GET_getConsoleLeaderboard is missing the following fields: ", 
                      what_is_missing(getConsoleLeaderboard, getConsoleLeaderboardRaw))
        except Exceptions.RiotAPIResponseError as e:
            print(f"GET_getConsoleLeaderboard failed with status code {e.status_code} and message {e.message}")
        except Exception as e:
            print(f"GET_getConsoleLeaderboard failed with error: {e}")
    else:
        print("getConsoleLeaderboard Failed Because of No ACT ID")

    # Other
    try:
        getPlatformData = await client.GET_getPlatformData(region="na")
        getPlatformDataRaw = await client_raw.GET_getPlatformData(region="na")
        if getPlatformData and getPlatformDataRaw and not has_all_fields(getPlatformData, getPlatformDataRaw):
            print("GET_getPlatformData is missing the following fields: ", 
                  what_is_missing(getPlatformData, getPlatformDataRaw))
    except Exceptions.RiotAPIResponseError as e:
        print(f"GET_getPlatformData failed with status code {e.status_code} and message {e.message}")
    except Exception as e:
        print(f"GET_getPlatformData failed with error: {e}")

    await client.close()
    await client_raw.close()

# Run the main function
if __name__ == "__main__":
    key = input("Enter your Riot API key: ")
    asyncio.run(main(key))
