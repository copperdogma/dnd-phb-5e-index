# Dungeons &amp; Dragons 5th Edition Revised Index

## Why?
My buddies and I play D&D. We have since first edition. And as much respect as we have for the creators of each edition, the index of the Fifth Edition Player's Handbook is just terrible. What do I mean? Take this example, where we want to look up listening at a door:

- Look up listening. We find:
	- listening. See Wisdom: Perception
		- See also conditions
- Okay.. let's try conditions. We look that up and get:
	- conditions, 290-292
	- Well that.. might be it. We look that up in the book and find three pages of conditions. The closest to listening in there is the Deafened condition. Well that's not it.
- Back to the index for listening. Let's try Wisdom: Perception:
	- Wisdom, 12, 178
		- Animal Handling, 178
		- checks, 178
		- Insight, 178
		- Medicine, 178
		- Perception, 178
		- Survival, 178
	- So we look up Perception, 178: Ah! That's it!

So to find the page we wanted we needed to look up the index, look up a page, read three pages before realizing that wasn't what we want, go back to the index, then back to another page.

What it the index was better? What if the listening section looked like this:

- listening
	- defeaned, 290
	- Perception (Wisdom), 178
	
There! Now it shows us both thing we may be looking for with a single page number.

Even more annoying are entries like this (it's on three lines because that's the way it wraps in the narrow index columns):

Destructive Wrath (cleric). See<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;under Channel Divinity cleric<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;options<br/>
	
Wouldn't this be better?

Destructive Wrath (cleric), 62

Just tell me what page it's on! Don't make me look up something else AND take two extra lines to do it!

Anyway, we were annoyed enough that I decided to fix it.

## TO DO
- Replace all "See X" entries with the actual page.
- Replace all vague page ranges with the actual page.
- Bold the page entries that are the primary source vs. incidental mentions.
- Decide how to convert the final result into a printable format that can be slotted into the back of a Player's Handbook.
	- I think HTML would be the best final format. The only downside would be we'd need to use cutting-edge CSS styling to get the layout perfect, but we can produce a PDF, too, for final printing.
	- Markdown would be the easiest format to edit, and you can produce HTML from it.