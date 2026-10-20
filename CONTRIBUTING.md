# Contributing

Thank you for helping. Please open an issue before a pull request.

## Propose a term

Say in the issue:

1. The fact, in one sentence.
2. The buyer question it answers, in the buyer's own words.
3. Which schema.org properties you checked, and why none of them fits.
4. An example value.

## Pull requests

- Edit the lists in `build/legal.py`. Never edit the files in `docs/` by hand.
- Run `python build/build.py`, then `python tools/check-profile.py docs/legal/legal.jsonld`. It must report 0 errors.
- Never rename or delete a term. Mark it deprecated instead (see [GOVERNANCE.md](GOVERNANCE.md)).
- Never paste schema.org's own definitions into the file (they are CC BY-SA 3.0). Link to them.

## Licence of contributions

Service Facts is licensed under [CC BY 4.0](LICENSE). By sending a contribution, you agree that it is licensed under CC BY 4.0 too, and that you have the right to license it.
