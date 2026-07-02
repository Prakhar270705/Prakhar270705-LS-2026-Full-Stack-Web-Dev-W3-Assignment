# Django Unchained - Wild West Bounty API

## Frontier picked
Bounty Board. Outlaws get put up on the board with a reward, and are either `wanted` or `captured`.

## Setup
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


## Endpoints
- POST /api/auth/register/ - username + password
- POST /api/auth/login/ - returns access + refresh
- POST /api/auth/refresh/ - refresh -> new access
- GET /api/bounties/ - list your bounties
- POST /api/bounties/ - create a bounty
- GET/PUT/PATCH/DELETE /api/bounties/<id>/ - single bounty, owner only

Bounty fields: target_name, reward, status (wanted/captured), plus location and danger_level for flavor. owner is set automatically from the logged in user and can't be changed.

## Auth + ownership
Every bounty endpoint requires a valid JWT access token in the Authorization header (`Bearer <token>`). The queryset for list and detail views is always filtered down to `owner=request.user`, so if another user tries to hit `/api/bounties/<someone_else_id>/` they get a 404, not a 403 - they can't even tell if the bounty exists.

## Bonus attempted

**Rate limiting** - using DRF's built in throttle classes. Anonymous requests are capped at 20/min, logged in users at 60/min. Set in `REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']` in settings.py.

**Caching** - the bounty list endpoint (GET /api/bounties/) is cached per user for 60 seconds using Django's local memory cache, so repeated list calls don't keep hitting the DB. The cache key includes the user id (`bounties_list_<user_id>`) so users never see each other's cached data. Whenever a bounty is created, updated or deleted, that user's cache key is deleted immediately so the next GET is always fresh - no stale data after a write.

## Notes
- SQLite, no Docker, no extra services. Just migrate + runserver.
- Tested manually with curl: register, login, refresh, create, cross-user access (blocked), and cache invalidation after writes.
