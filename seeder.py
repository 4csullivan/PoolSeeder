import challonge
import asyncio
import configparser
import pathlib
import aiohttp

# Run seeder.
async def run(tID, p):

    # Grab data from config file.
    config = configparser.ConfigParser()
    config.read(pathlib.Path('config.ini'))
    my_username = config.get('SETTINGS','username')
    my_api_key = config.get('SETTINGS','key')
    subDom = config.get('SETTINGS','subdomain')

    # Data continued - check if there is
    # a subdomain.
    if subDom == 'none':
        isSub = False
    else:
        isSub = True
    tourneyID = tID
    intPools = p
    pools = []

    # For the number of pools, add empty lists.
    for i in range(intPools):
        pools.append([])

    # Set the Challonge user and tournament.
    my_user = await challonge.get_user(my_username, my_api_key)
    if not isSub:
        tournament = await my_user.get_tournament(url=tourneyID)
    else:
        tournament = await my_user.get_tournament(url=tourneyID, subdomain=subDom)
    participants = await tournament.get_participants()
    pLen = len(participants)

    # This checks if there is an uneven number for pools.
    # For example, 33 people in 4 pools will return
    # a modulus greater than 0.
    # As a result, "blank" participants are added to
    # create the next highest even number for the pool.
    # This is needed because challonge splits pools into
    # participants instead of number of pools, and
    # uneven participants messes everything up.
    if pLen % intPools > 0:
        for f in range(intPools - (pLen % intPools)):
            fakeName = 'BlankParticipant' + str(f)
            await tournament.add_participant(fakeName)

    # For each participant in the tournament,
    # put the participant in the correct pool
    # based on the modulus of the num of pools.
    i = 0
    for f in participants:
        pools[i % intPools].append(f)
        i += 1

    # For each pass through each pool,
    # Increment the participant in that
    # index.
    index = 1
    for p in pools:
        for z in p:
            await z.change_seed(index)
            index += 1

# Undo the seeding. Same as run,
# but in reverse. This also removes
# all of the blank participants that
# were added previously.
async def undo(tID, p):
    config = configparser.ConfigParser()
    config.read(pathlib.Path('config.ini'))
    my_username = config.get('SETTINGS', 'username')
    my_api_key = config.get('SETTINGS', 'key')
    subDom = config.get('SETTINGS', 'subdomain')
    if subDom == 'none':
        isSub = False
    else:
        isSub = True

    intPools = p
    pools = []
    newList = []
    isEmpty = [] # un-needed

    for i in range(intPools):
        pools.append([])
        isEmpty.append(False) # not used

    my_user = await challonge.get_user(my_username, my_api_key)
    if not isSub:
        tournament = await my_user.get_tournament(url=tID)
    else:
        tournament = await my_user.get_tournament(url=tID, subdomain=subDom)
    participants = await tournament.get_participants()
    intP = len(participants)

    # To reverse the seeding, a new list is needed
    # so we can modify their positions more easily.
    x = 0
    emptyList = []
    for f in participants:
        emptyList.append(f)

    # Debugging, will remove in the future.
    poolX = 0
    for u in pools:
        for y in u:
            print("pool ", poolX, " ", y.display_name)
        poolX +=1

    # This gets a little complicated.
    # The number of participants gets divided
    # by the number of pools to make an
    # iteration value. This stores how many
    # people are in each pool.
    # If seeded properly, this should
    # always be an even division.
    pIndex = 0
    iterate = int(intP / intPools)

    # Since we are taking in participants as
    # one long list, we need to pass through
    # each participant in each "pool".
    # Doing this requires a little math.
    # For each pool in each number of
    # participants, a new list adds the
    # current participant to an empty list.
    # The index of this participant equates to:
    #
    #   the current iteration + (the current pool * the total iteration)
    #
    # This may be confusing so here's an example:
    #
    #   pools = 4
    #   participants = 32
    #   iterate = 8
    #   find 4th participant in 2nd pool:
    #       4(participant) + 2 * 8 (pool# * iterate) = 20
    #       i.e. skip one pool of participants (iterate/8)
    #       and add what place participant is in inside the pool (4)
    #
    # This is done incrementally until every participant is back
    # where they started.
    for k in range(iterate):
        for j in range(intPools):
            newList.append(emptyList[k + j*iterate])

    # Once the new list is reset, simply just change the seed of
    # each participant incrementally.
    index = 1
    for l in newList:
        await l.change_seed(index)
        index += 1

    # To improve quality-of-life, the program finishes by
    # removing any participants with the name "BlankParticipant"
    # (the beginning name of each empty participant
    # set in the seeding function).
    # The name is set so that there's no possibility
    # of deleting any real participants (anyone who enters
    # the bracket as "BlankParticipant" deserves to be
    # deleted anyways :^] )
    for f in participants:
        if "BlankParticipant" in f.display_name:
            await tournament.remove_participant(f)