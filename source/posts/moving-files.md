---
icon: "{fas}`comment`"
date: "2025-02-18"
---

# Moving Files

I was attempting to archive my documents into my iCloud when I ran into a bit of an issue. See, a normal person would simply drag and drop an item from one place to another. But as a crazy person, I am obliged to ask: how do I know that my file successfully moved over? What if, in transit, any one of my precious files had been corrupted or lost altogether? How could I know that after I move my files, the world would be sound and everything would be okay?

The first thing I knew was that I couldn't simply move things over. I would first duplicate a copy into my archive directory, leaving a perfect untouched original behind. So I have file1 (the original), and file2 (the copy in its archive location), and I somehow had to verify that file2 was the same as file1, and only after doing so could I then delete file1. After mulling over this problem for some time, inspiration revealed itself to me. I recalled how my forefathers did things before me; On many download websites, the author would display a checksum of the file, which in theory enabled you to verify that what you wanted was what you received.

I knew the basics of a checksum; given file X, a hash function (e.g. sha256) would read the file, run a calculation, and output some small gibberish string. An end-user who downloaded file X could then run the same hash function on their end, and compare the results. Outputting a different small gibberish string would then imply that file Y had been corrupted or manipulated in the download process. This sounds like exactly what I needed.

But hang on - my computer questioned - you're saying I should:

1. Read the entire contents of file X
1. Run some fancy calculation
1. Read the entire contents of file Y
1. Run another calculation
1. Compare the results

Why go through this round-about way to check if two files are the same when you could simply compare the two files directly? Well that was a good point. Calculating a checksum requires reading both files completely, and costs additional calculations on top of that.

But what then is the use of a checksum? Doing some further research, I found that checksums were really only useful when comparing two files on different machines. Going back to the download example, let's say we want to directly compare the downloaded file to the host file. The host machine would need to send each byte of the host file to our local machine, which would then be compared to our downloaded copy. But think about it, if we are sending each byte to the local machine, we are effectively downloading the file all over again, leaving us with the original problem. So yes, checksums do indeed have their place. Mystery solved, let's move on. 

So now we know that in our local case, comparing the files byte by byte is the best choice. How do we do that? It first depends if your item is a single file, or a folder. If it's a file, you can run:

```sh
diff --brief <file1> <file2>
```

If it's a folder, you can run:

```sh
diff --brief --recursive <folder1> <folder2>
```

The `--brief` flag simplifies the output by only telling us whether or not the file is different, as opposed to the default behaviour which would output the differences of each individual file line-by-line.

When running either of these commands, if the two items are the same, no output will be produced. If there is any difference, some message will be shown.

And with that, another mystery solved. Now I can sleep peacefully at night knowing that I can verify that my files have moved intact from one location to the other.
