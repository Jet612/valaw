import valaw
import os
from dotenv import load_dotenv
import asyncio
import sys

load_dotenv()

RIOT_API_TOKEN = os.getenv("RIOT_API_TOKEN")
failures = []


def fail(msg):
    print(f"FAIL: {msg}")
    failures.append(msg)


async def request(fn):
    """Call fn(), retrying once on 429 after a 1s delay."""
    for attempt in range(2):
        try:
            return await fn()
        except valaw.Exceptions.RiotAPIResponseError as e:
            if e.status_code == 429 and attempt == 0:
                print("Rate limited, retrying in 1s...")
                await asyncio.sleep(1)
            else:
                raise


async def main():
    if RIOT_API_TOKEN is None:
        raise ValueError("RIOT_API_TOKEN environment variable is not set.")
    client = valaw.Client(RIOT_API_TOKEN, "americas")

    try:
        # Get recent matches
        try:
            recent_matches = await request(lambda: client.GET_getRecent("competitive", "na"))
        except Exception as e:
            fail(f"GET_getRecent: {e}")
            return

        match_ids = getattr(recent_matches, "matchIds", None)
        if not match_ids:
            fail("GET_getRecent: no match IDs returned")
            return

        # Get the first match
        try:
            match = await request(lambda: client.GET_getMatch(match_ids[0], "na"))
        except Exception as e:
            fail(f"GET_getMatch: {e}")
            return

        players = getattr(match, "players", None)
        if not players:
            fail("GET_getMatch: no players in match")
            return
        player_puuid = getattr(players[0], "puuid", None)
        if not player_puuid:
            fail("GET_getMatch: player puuid not found")
            return

        # Run independent calls concurrently
        async def safe_get_by_puuid():
            try:
                return await request(lambda: client.GET_getByPuuid(player_puuid, "americas"))
            except Exception as e:
                fail(f"GET_getByPuuid: {e}")
                return None

        async def safe_get_matchlist():
            try:
                await request(lambda: client.GET_getMatchlist(player_puuid, "na"))
            except Exception as e:
                fail(f"GET_getMatchlist: {e}")

        async def safe_get_content():
            try:
                return await request(lambda: client.GET_getContent("na", "en-us"))
            except Exception as e:
                fail(f"GET_getContent: {e}")
                return None

        async def safe_get_platform_data():
            try:
                await request(lambda: client.GET_getPlatformData("na"))
            except Exception as e:
                fail(f"GET_getPlatformData: {e}")

        account_by_puuid, _, content, _ = await asyncio.gather(
            safe_get_by_puuid(),
            safe_get_matchlist(),
            safe_get_content(),
            safe_get_platform_data(),
        )

        # Resolve active act from content (used by both PC and console leaderboards)
        active_act = None
        if content is not None:
            acts = getattr(content, "acts", None)
            if acts:
                for act in acts:
                    if (
                        hasattr(act, "isActive")
                        and act.isActive
                        and hasattr(act, "type")
                        and act.type == "act"
                    ):
                        active_act = act
                        break
            else:
                fail("GET_getContent: no acts returned")

        # Run calls that depend on phase 3 results concurrently
        followup_tasks = []

        if account_by_puuid is not None:
            async def safe_get_by_riot_id():
                try:
                    game_name = getattr(account_by_puuid, "gameName", None) or ""
                    tag_line = getattr(account_by_puuid, "tagLine", None) or ""
                    await request(lambda: client.GET_getByRiotId(game_name, tag_line, "americas"))
                except Exception as e:
                    fail(f"GET_getByRiotId: {e}")

            async def safe_get_active_shard():
                try:
                    puuid = getattr(account_by_puuid, "puuid", None)
                    if puuid is None:
                        fail("GET_getActiveShard: account puuid not found")
                        return
                    await request(lambda: client.GET_getActiveShard(puuid, "americas"))
                except Exception as e:
                    fail(f"GET_getActiveShard: {e}")

            followup_tasks.extend([safe_get_by_riot_id(), safe_get_active_shard()])

        if active_act and hasattr(active_act, "id"):
            act_id = active_act.id

            async def safe_get_leaderboard():
                try:
                    await request(lambda: client.GET_getLeaderboard(act_id, "na"))
                except Exception as e:
                    fail(f"GET_getLeaderboard: {e}")

            followup_tasks.append(safe_get_leaderboard())
        else:
            fail("GET_getLeaderboard: no active act found")

        async def run_console_chain():
            try:
                console_recent = await request(lambda: client.GET_getConsoleRecent("console_competitive", "na"))
            except Exception as e:
                fail(f"GET_getConsoleRecent: {e}")
                return

            console_match_ids = getattr(console_recent, "matchIds", None)
            if not console_match_ids:
                fail("GET_getConsoleRecent: no match IDs returned")
                return

            try:
                console_match = await request(lambda: client.GET_getConsoleMatch(console_match_ids[0], "na"))
            except Exception as e:
                fail(f"GET_getConsoleMatch: {e}")
                return

            console_players = getattr(console_match, "players", None)
            if not console_players:
                fail("GET_getConsoleMatch: no players in match")
                return
            console_player_puuid = getattr(console_players[0], "puuid", None)
            if not console_player_puuid:
                fail("GET_getConsoleMatch: player puuid not found")
                return

            console_followup = []

            async def safe_get_console_matchlist():
                try:
                    await request(lambda: client.GET_getConsoleMatchlist(console_player_puuid, "na", "playstation"))
                except Exception as e:
                    fail(f"GET_getConsoleMatchlist: {e}")

            console_followup.append(safe_get_console_matchlist())

            if active_act and hasattr(active_act, "id"):
                console_act_id = active_act.id

                async def safe_get_console_leaderboard():
                    try:
                        await request(lambda: client.GET_getConsoleLeaderboard(console_act_id, "na", "playstation"))
                    except Exception as e:
                        fail(f"GET_getConsoleLeaderboard: {e}")

                console_followup.append(safe_get_console_leaderboard())

            await asyncio.gather(*console_followup)

        followup_tasks.append(run_console_chain())

        if followup_tasks:
            await asyncio.gather(*followup_tasks)

    finally:
        await client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

    if failures:
        print(f"\n{len(failures)} test(s) failed:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)

    print("All tests passed.")
