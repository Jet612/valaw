import asyncio
import json
import os
import pytest
from valaw.client import Client, Exceptions
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables (like RIOT_API_KEY)
load_dotenv()

# Get API key and skip tests if not found
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
if not RIOT_API_KEY:
    pytest.skip(
        "RIOT_API_KEY not found in environment variables. Skipping integration tests.",
        allow_module_level=True,
    )


# --- Helper Functions ---

def what_is_missing(obj, json_dict):
    """Compares object fields to dictionary keys and returns missing keys."""
    # Get the fields of the object using __dict__
    obj_fields = obj.__dict__

    # Ensure all keys in json_dict are strings and not None
    json_keys = {key for key in json_dict.keys() if key is not None}

    # Find missing fields
    missing_fields = list(json_keys - set(obj_fields.keys()))

    # Optionally write raw data for debugging (consider removing in CI)
    # timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # filename = f"raw_missing_{obj.__class__.__name__}_{timestamp}.json"
    # try:
    #     with open(filename, "w") as f:
    #         json.dump(json_dict, f, indent=2)
    #     print(f"Raw data saved to {filename}")
    # except Exception as e:
    #     print(f"Failed to write raw data: {e}")

    return missing_fields


def has_all_fields(obj, json_dict):
    """Checks if all keys from json_dict exist as attributes in obj."""
    if not obj or not json_dict:
        return False
    obj_fields = obj.__dict__
    return all(
        key in obj_fields for key in json_dict.keys() if key is not None
    )


# --- Pytest Test Function ---


@pytest.mark.asyncio
async def test_all_endpoints():
    """
    Tests various endpoints of the valaw client against the Riot API.
    Compares processed data objects against raw JSON responses.
    """
    client = Client(token=RIOT_API_KEY, cluster="americas")
    client_raw = Client(token=RIOT_API_KEY, cluster="americas", raw_data=True)

    # Variables to store data between calls
    test_puuid = None
    test_act_id = None
    test_puuid_console = None
    getRecent = None
    getMatch = None
    getConsoleRecent = None
    getConsoleMatch = None

    try:
        # --- Regular API Calls ---

        # GET_getContent
        try:
            getContent = await client.GET_getContent(region="na", locale="en-US")
            getContentRaw = await client_raw.GET_getContent(
                region="na", locale="en-US"
            )
            assert getContent is not None, "GET_getContent returned None"
            assert getContentRaw is not None, "GET_getContent (raw) returned None"
            assert has_all_fields(getContent, getContentRaw), (
                f"GET_getContent missing fields: "
                f"{what_is_missing(getContent, getContentRaw)}"
            )
        except Exceptions.RiotAPIResponseError as e:
            pytest.fail(
                f"GET_getContent failed (API Error {e.status_code}): {e.message}"
            )
        except Exception as e:
            pytest.fail(f"GET_getContent failed (Other Error): {e}")

        # GET_getRecent
        try:
            getRecent = await client.GET_getRecent(
                queue="competitive", region="na"
            )
            getRecentRaw = await client_raw.GET_getRecent(
                queue="competitive", region="na"
            )
            assert getRecent is not None, "GET_getRecent returned None"
            assert getRecentRaw is not None, "GET_getRecent (raw) returned None"
            assert has_all_fields(getRecent, getRecentRaw), (
                f"GET_getRecent missing fields: "
                f"{what_is_missing(getRecent, getRecentRaw)}"
            )
        except Exceptions.RiotAPIResponseError as e:
            pytest.fail(
                f"GET_getRecent failed (API Error {e.status_code}): {e.message}"
            )
        except Exception as e:
            pytest.fail(f"GET_getRecent failed (Other Error): {e}")

        # Proceed only if getRecent was successful and has matches
        assert getRecent is not None, "Cannot proceed without getRecent result"
        assert (
            getRecent.matchIds
        ), "getRecent returned no match IDs, cannot test getMatch"
        test_match_id = getRecent.matchIds[0]

        # GET_getMatch
        try:
            getMatch = await client.GET_getMatch(
                matchId=test_match_id, region="na"
            )
            getMatchRaw = await client_raw.GET_getMatch(
                matchId=test_match_id, region="na"
            )
            assert getMatch is not None, "GET_getMatch returned None"
            assert getMatchRaw is not None, "GET_getMatch (raw) returned None"
            assert has_all_fields(getMatch, getMatchRaw), (
                f"GET_getMatch missing fields: "
                f"{what_is_missing(getMatch, getMatchRaw)}"
            )
            # Extract data for next tests
            if getMatch.players:
                test_puuid = getMatch.players[0].puuid
            if getMatch.matchInfo:
                test_act_id = getMatch.matchInfo.seasonId
        except Exceptions.RiotAPIResponseError as e:
            pytest.fail(
                f"GET_getMatch failed (API Error {e.status_code}): {e.message}"
            )
        except Exception as e:
            pytest.fail(f"GET_getMatch failed (Other Error): {e}")

        # GET_getMatchlist (requires puuid from getMatch)
        if test_puuid:
            try:
                getMatchlist = await client.GET_getMatchlist(
                    puuid=test_puuid, region="na"
                )
                getMatchlistRaw = await client_raw.GET_getMatchlist(
                    puuid=test_puuid, region="na"
                )
                assert getMatchlist is not None, "GET_getMatchlist returned None"
                assert (
                    getMatchlistRaw is not None
                ), "GET_getMatchlist (raw) returned None"
                # Note: Matchlist structure might differ slightly, adjust check if needed
                assert has_all_fields(getMatchlist, getMatchlistRaw), (
                    f"GET_getMatchlist missing fields: "
                    f"{what_is_missing(getMatchlist, getMatchlistRaw)}"
                )
            except Exceptions.RiotAPIResponseError as e:
                pytest.fail(
                    f"GET_getMatchlist failed (API Error {e.status_code}): {e.message}"
                )
            except Exception as e:
                pytest.fail(f"GET_getMatchlist failed (Other Error): {e}")
        else:
            print("Skipping GET_getMatchlist: No PUUID obtained from getMatch.")

        # GET_getLeaderboard (requires actId from getMatch)
        if test_act_id:
            try:
                getLeaderboard = await client.GET_getLeaderboard(
                    actId=test_act_id, region="na"
                )
                getLeaderboardRaw = await client_raw.GET_getLeaderboard(
                    actId=test_act_id, region="na"
                )
                assert (
                    getLeaderboard is not None
                ), "GET_getLeaderboard returned None"
                assert (
                    getLeaderboardRaw is not None
                ), "GET_getLeaderboard (raw) returned None"
                assert has_all_fields(getLeaderboard, getLeaderboardRaw), (
                    f"GET_getLeaderboard missing fields: "
                    f"{what_is_missing(getLeaderboard, getLeaderboardRaw)}"
                )
            except Exceptions.RiotAPIResponseError as e:
                # Leaderboards can sometimes be empty or unavailable, might not be a failure
                print(
                    f"GET_getLeaderboard info (API Status {e.status_code}): {e.message}"
                )
            except Exception as e:
                pytest.fail(f"GET_getLeaderboard failed (Other Error): {e}")
        else:
            print(
                "Skipping GET_getLeaderboard: No Act ID obtained from getMatch."
            )

        # --- Console API Calls ---

        # GET_getConsoleRecent
        try:
            getConsoleRecent = await client.GET_getConsoleRecent(
                queue="console_competitive", region="na"
            )
            getConsoleRecentRaw = await client_raw.GET_getConsoleRecent(
                queue="console_competitive", region="na"
            )
            assert (
                getConsoleRecent is not None
            ), "GET_getConsoleRecent returned None"
            assert (
                getConsoleRecentRaw is not None
            ), "GET_getConsoleRecent (raw) returned None"
            assert has_all_fields(getConsoleRecent, getConsoleRecentRaw), (
                f"GET_getConsoleRecent missing fields: "
                f"{what_is_missing(getConsoleRecent, getConsoleRecentRaw)}"
            )
        except Exceptions.RiotAPIResponseError as e:
            pytest.fail(
                f"GET_getConsoleRecent failed (API Error {e.status_code}): {e.message}"
            )
        except Exception as e:
            pytest.fail(f"GET_getConsoleRecent failed (Other Error): {e}")

        # Proceed only if getConsoleRecent was successful and has matches
        assert (
            getConsoleRecent is not None
        ), "Cannot proceed without getConsoleRecent result"
        assert (
            getConsoleRecent.matchIds
        ), "getConsoleRecent returned no match IDs, cannot test getConsoleMatch"
        test_console_match_id = getConsoleRecent.matchIds[0]

        # GET_getConsoleMatch
        try:
            getConsoleMatch = await client.GET_getConsoleMatch(
                matchId=test_console_match_id, region="na"
            )
            getConsoleMatchRaw = await client_raw.GET_getConsoleMatch(
                matchId=test_console_match_id, region="na"
            )
            assert (
                getConsoleMatch is not None
            ), "GET_getConsoleMatch returned None"
            assert (
                getConsoleMatchRaw is not None
            ), "GET_getConsoleMatch (raw) returned None"
            assert has_all_fields(getConsoleMatch, getConsoleMatchRaw), (
                f"GET_getConsoleMatch missing fields: "
                f"{what_is_missing(getConsoleMatch, getConsoleMatchRaw)}"
            )
            if getConsoleMatch.players:
                test_puuid_console = getConsoleMatch.players[0].puuid
        except Exceptions.RiotAPIResponseError as e:
            pytest.fail(
                f"GET_getConsoleMatch failed (API Error {e.status_code}): {e.message}"
            )
        except Exception as e:
            pytest.fail(f"GET_getConsoleMatch failed (Other Error): {e}")

        # GET_getConsoleMatchlist (requires puuid from getConsoleMatch)
        if test_puuid_console:
            for platform in ["playstation", "xbox"]:
                try:
                    getConsoleMatchlist = await client.GET_getConsoleMatchlist(
                        puuid=test_puuid_console,
                        region="na",
                        platformType=platform,
                    )
                    getConsoleMatchlistRaw = (
                        await client_raw.GET_getConsoleMatchlist(
                            puuid=test_puuid_console,
                            region="na",
                            platformType=platform,
                        )
                    )
                    assert (
                        getConsoleMatchlist is not None
                    ), f"GET_getConsoleMatchlist ({platform}) returned None"
                    assert (
                        getConsoleMatchlistRaw is not None
                    ), f"GET_getConsoleMatchlist ({platform}) (raw) returned None"
                    assert has_all_fields(
                        getConsoleMatchlist, getConsoleMatchlistRaw
                    ), (
                        f"GET_getConsoleMatchlist ({platform}) missing fields: "
                        f"{what_is_missing(getConsoleMatchlist, getConsoleMatchlistRaw)}"
                    )
                except Exceptions.RiotAPIResponseError as e:
                    pytest.fail(
                        f"GET_getConsoleMatchlist ({platform}) failed (API Error {e.status_code}): {e.message}"
                    )
                except Exception as e:
                    pytest.fail(
                        f"GET_getConsoleMatchlist ({platform}) failed (Other Error): {e}"
                    )
        else:
            print(
                "Skipping GET_getConsoleMatchlist: No Console PUUID obtained."
            )

        # GET_getConsoleLeaderboard (requires actId from getMatch)
        if test_act_id:
            for platform in ["playstation", "xbox"]: # Assuming leaderboard exists for both
                try:
                    getConsoleLeaderboard = (
                        await client.GET_getConsoleLeaderboard(
                            actId=test_act_id, region="na", platformType=platform
                        )
                    )
                    getConsoleLeaderboardRaw = (
                        await client_raw.GET_getConsoleLeaderboard(
                            actId=test_act_id, region="na", platformType=platform
                        )
                    )
                    assert (
                        getConsoleLeaderboard is not None
                    ), f"GET_getConsoleLeaderboard ({platform}) returned None"
                    assert (
                        getConsoleLeaderboardRaw is not None
                    ), f"GET_getConsoleLeaderboard ({platform}) (raw) returned None"
                    assert has_all_fields(
                        getConsoleLeaderboard, getConsoleLeaderboardRaw
                    ), (
                        f"GET_getConsoleLeaderboard ({platform}) missing fields: "
                        f"{what_is_missing(getConsoleLeaderboard, getConsoleLeaderboardRaw)}"
                    )
                except Exceptions.RiotAPIResponseError as e:
                     print(
                        f"GET_getConsoleLeaderboard ({platform}) info (API Status {e.status_code}): {e.message}"
                    )
                except Exception as e:
                    pytest.fail(
                        f"GET_getConsoleLeaderboard ({platform}) failed (Other Error): {e}"
                    )
        else:
            print(
                "Skipping GET_getConsoleLeaderboard: No Act ID obtained."
            )


        # --- Other API Calls ---

        # GET_getPlatformData
        try:
            getPlatformData = await client.GET_getPlatformData(region="na")
            getPlatformDataRaw = await client_raw.GET_getPlatformData(region="na")
            assert (
                getPlatformData is not None
            ), "GET_getPlatformData returned None"
            assert (
                getPlatformDataRaw is not None
            ), "GET_getPlatformData (raw) returned None"
            assert has_all_fields(getPlatformData, getPlatformDataRaw), (
                f"GET_getPlatformData missing fields: "
                f"{what_is_missing(getPlatformData, getPlatformDataRaw)}"
            )
        except Exceptions.RiotAPIResponseError as e:
            pytest.fail(
                f"GET_getPlatformData failed (API Error {e.status_code}): {e.message}"
            )
        except Exception as e:
            pytest.fail(f"GET_getPlatformData failed (Other Error): {e}")

    finally:
        # Ensure clients are closed regardless of test outcome
        await client.close()
        await client_raw.close()

# Note: No if __name__ == "__main__": block is needed for pytest