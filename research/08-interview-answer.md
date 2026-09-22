# "How do you use AI in your work?" (spoken answer, about 90 seconds)

I use AI across the whole workflow of building a product, and I'd split it into three jobs.

For research, I use it to synthesize. For competitive analysis it reads across the market faster than
I can, and for user research it pulls the signals out of interviews and documents so I can form my own
view on what the real pain point is. I still make the call. It just gets me to the evidence faster.

For prototyping, I use tools like Figma, Lovable, Cursor and Claude Code to get to a lo-fi prototype
in hours instead of days. Some of those get demoed in standups with engineers and designers, some
become interactive prototypes I put in front of users.

And for iteration, I treat the AI as the pair I critique. I look at the build, say what is wrong with
the interaction, and it makes the change while I keep my attention on the user journey.

I'm genuinely interested in Tessera, so I did exactly that for this conversation. I researched how
SAP consultants run discovery for an ECC to S/4HANA migration, and the pain point was clear: after
every client interview, the consultant has to check what people said against the system's actual
configuration and process-mining data, and that reconciliation lives in their head and an Excel file.
Even SAP's own Cloud ALM only turns a transcript into a requirement; nothing compares it to the data.
So I prototyped an agent that takes the interview transcript, checks every configuration item against
the extract, and returns a verdict: match, contradiction, or a gap where either the data or the reason
is missing, with the evidence on both sides, and the consultant records the judgment. For the consultant
that turns "where am I in discovery" from a feeling into a count. For the client, the people interviewed
see their words used, and the process owner sees progress as it happens instead of in a deck weeks later.

I'd love to walk you through it if there's time. And honestly, I'd like your critique more than your
approval, because you know this problem far better than I do.
