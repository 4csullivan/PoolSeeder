# PoolSeeder
PoolSeeder is a program that can automatically seed pools in Challonge tournaments.

## How to use

1) Launch the program.
2) Click on Edit->Setup if you have not yet.
3) Fill in necessary info:
   - Username - Your account's username.
   - API Key - Your account's developer API key.
   - Subdomain - Fill this in with your community's subdomain only if using a community. Keep this unchecked if just a user.
      -  EX: subdomain.challonge.com, NOT challonge.com/communities/subdomain.
 If your community does not have a set subdomain, a hidden,
 generated subdomain is located in the community's settings.

4) Hit save.
	- Once set, the settings do not need to be touched in the future.
	- Update only the sections you want to update. Blank sections will
	not override the previous sections.
5) Type in the unique tournament URL (i.e. challonge.com/{HERE}).
6) Type in number of pools.
7) Hit Run.

## How to undo
1) Enter the same unique tournament URL.
2) Type in the number of pools initially entered.
3) Hit Undo.

## Notes
- This only works with tournaments that have a number of participants that can be evenly divided into the number of pools wanted. To account for this, this program adds a number of "blank participants" to even out the number of entrants before seeding. These participants are effectively "byes" for anyone who fights them.
- DO NOT delete these participants, the undo button removes them after it is done resetting. Deleting them before undoing can result in a completely messed up bracket.

## TODO
- Intuitive error codes
