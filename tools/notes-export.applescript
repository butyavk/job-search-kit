-- Export Apple Notes to a text file — a source of facts for the candidate pack.
-- How to run: open it in Script Editor (File → Open With → Script Editor) and press Run.
-- macOS asks once whether Script Editor may control Notes — allow it.
-- Settings are the three lines below: folders to take whole, folders to skip, and words that pick notes from the other folders.

set outFile to (POSIX path of (path to home folder)) & "Documents/notes-export.txt"
set keepFolders to {"Work", "1-1"} -- whole folders
set skipFolders to {"Personal", "Recently Deleted"} -- never export (passwords, keys, private)
set keys to {"feedback", "CTO", "review"} -- from other folders, only notes with these words

set out to ""
tell application "Notes"
	repeat with fo in (every folder of account "iCloud")
		try
			set fname to name of fo
			if skipFolders does not contain fname then
				repeat with n in (every note of fo)
					try
						set t to plaintext of n
						set hit to (keepFolders contains fname)
						if not hit then
							repeat with k in keys
								if t contains (k as string) then set hit to true
							end repeat
						end if
						if hit then set out to out & "##### " & (name of n) & " | " & fname & " | " & ((modification date of n) as string) & linefeed & t & linefeed & linefeed
					end try
				end repeat
			end if
		end try
	end repeat
end tell
set fh to open for access (POSIX file outFile) with write permission
set eof of fh to 0
write out to fh as «class utf8»
close access fh
