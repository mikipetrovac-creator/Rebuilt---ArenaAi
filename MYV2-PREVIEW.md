# M.Y.V. 2.0 preview

This branch is intentionally isolated from production. Do not merge until desktop/mobile, booking, six-language SEO, schema, performance and regression checks pass.

## Architecture
- Static indexable HTML remains the delivery model.
- `assets/myv2.css` is the premium dark/gold redesign layer.
- `scripts/myv2.js` provides same-page booking modal, sticky CTA and funnel events.
- `scripts/tours.js` is the first central tour-data source for confirmed tours already present in the repository.
- Existing canonical/hreflang/schema and Netlify booking backend remain intact.

## Booking analytics
`book_now_click` -> `booking_open` -> `booking_submit` -> existing server-confirmed `booking_success`.

## Private Boat
Private Boat is still the intended pilot tour, but there is no Private Boat page, confirmed pricing or image asset in the current repository. No fake tour data/assets were introduced. The shared M.Y.V. 2.0 system is therefore applied to the existing confirmed tour pages first and is ready for Private Boat as soon as its real source data/assets exist.
