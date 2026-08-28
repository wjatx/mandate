# mandate

An AI agent that trades options on an Alpaca paper account with no human in the
loop, built to show off a safety architecture rather than a strategy. The
strategy is a written charter loaded at the start of every run. Everything else
is the wrapping: the agent never holds an API key and never talks to the broker
directly. Every call goes through a gateway that serves only tools admitted
through a two-key ceremony, checks every order against dollar caps signed into a
locked envelope, and writes every request, grant, and refusal to a hash-chained
audit tape the agent cannot touch.

Built for a trading hackathon on [safe-agents](https://github.com/wjatx/ptc-gal-reference).

This repository was born on 2026-08-28, the first day of the contest window.
Setup instructions, the charter, and the audit record land here as the machine
comes up over the course of the day.

NOTE: This project contains code that was written with AI.

## License

MIT, copyright Wes Jackson. See [LICENSE](LICENSE).
