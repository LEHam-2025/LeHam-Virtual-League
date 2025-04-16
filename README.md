This should be fairly simple.

-The first file, 'sensing', contains sensing functions.

-The second file, 'movement', contains movement functions

-The third file, 'logic', contains the algorithm functions

-The final file, 'robot.py', is the actual final file.

To ensure proper decomposition, these files will import from each other as such:

sensing -> movement -> logic -> robot

(where the file to the right of the arrow imports from the file to the left of it)


Once the other files are done, we should be able to simply import * from logic
and run a 'main' function. Therefore, it is imperative that each file only depends on the files before it

You can work on any function in any file, but I would recommend storing a local copy of any file you are working on,
so that you can work on it without being interrupted by other people's changes. When you are done, you can then change the file in the repository.



Note - 05/02/25 - 21:09:
We are very nearly finished. Hopefully we'll actually submit something decent.

Note - After the League:
It worked pretty well. We came 6th. There were problems with accuracy, but I would like to blame the hardware for that.


P.S. - The 'omni-dir' file is for omni-directional movement in the actual robot. I don't expect us to use it, 
but I started it a while ago and didn't want to just discard it. Feel free to work on it if you want

P.P.S - I ended up doing this all by myself. It was very sad. We also did not use the omni-dir file at all. Also very sad.
