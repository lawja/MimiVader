# MimIvader
MimiVader is a script to evade various anti-viruses using various methods to prevent against string and heuristic detection

## Why / Example
MimiKatz is a powerful exploit that allows attackers to dump cleartext passwords from Windows memory. Due to this threat AVs (anti-viruses) have learned how to protect it (well, somewhat). Here is a scan that shows how many AVs recognize MimiKatz as a threat

![original](https://github.com/lawja/MimiVader/blob/master/img/og.png?raw=true)

As shown above, 29/59 tested AVs recognize MimiKatz as a threat; including the widely used Windows Defender. [This blog post](https://www.blackhillsinfosec.com/bypass-anti-virus-run-mimikatz/), by Black Hills Info Security shows a method that edits the Invoke-Mimikatz.ps1 script and manages to get it down to 0/59 AV recognition. Unfortunately, AVs took notice and this only gets the results down to 26/59 AV recognition; including Windows defender recognition

![better](https://github.com/lawja/MimiVader/blob/master/img/better.png?raw=true)

Now I decided to take a jab at this and through a combination of nonsense injection, variable and function renaming I got it down to a 10/59 AV recognition; Windows Defender did not find this a malicious script using my techniques.

![best](https://github.com/lawja/MimiVader/blob/master/img/best.png?raw=true)

I still want to get this lower so I'll try and continue to better my script.

## Usage
`python3 MimiVader.py <og_file> <output_file>`

Example

`python3 MimiVader.py Invoke-Mimikatz.ps1 DeceptiveFile.py`
