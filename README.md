HELLO, WHAT IS THIS
===================

Welcome to my shitty chord namer program. The goal was to accomplish something
similar to [JGuitar's chord namer](https://jguitar.com/chordname) or (before
flash went out of style) 
[All-Guitar-Chord's tool](http://www.all-guitar-chords.com/chord_name.php),\
except with python 3.6, on the commandline, and probably worse.

If you haven't bothered to click any of those links, this program takes in a
list of numbers representing the frets you are fingering on the guitar (or
any other stringed instrument, more on this later) and gives you some ideas
of what other people may call this chord.

How to Use
==========

Install and Start
-----------------

1. First of all, you need at least python 3.6ish. 

2. Then you can download or clone the only really important file, `chord.py`. 

3. There's a couple ways to proceed from here, but the one I understand best
   is to type
   
   ```
   $ python chord.py
   ```
   into your terminal or python console thing or w/e.
   
4. Then you should be prompted with how to proceed.

Quit
----

To quit at any time you can just type `quit` and press `<enter>`.

Entering Chords and Stuff
-------------------------

1. The on-screen examples should make this pretty clear, but you just type in
   the numbers of the frets you're playing in order (descending order if you go
   by gravity, or ascending order if you go by pitch).
   
2. For example for a regular cowboy open E major chord type in
   ```022100```
   and hopefully the computer will say
   > That's an E major chord!

3. If you're really advanced and play chords above the 9th fret, you'll have to
   put spaces between the strings so the computer doesn't get confused.
   
   For example
   ```X 10 12 12 12 10```
   should say
   > G major
   
   oh yeah, you can put an 'X' or an 'x' if the string is muted
   
Features
========

At the beginning you'll be asked if you want to change the instrument or
tuning or something. Can enter a new tuning or instrument by typing in the
notes of the strings.

Examples:

1. For a mandolin or violin you'd type
   ```G3 D4 A4 E5```
   probably. (I think..?)
   
2. For open G on a guitar you'd type
   ```D2 G2 D3 G3 B3 D4```
   
If you (like me) aren't sure exactly what the numbers here mean, that's ok. You
can just enter what ever numbers you want and things will probably work as you
expect.

Limitations
===========

1. Sometimes you may get the wrong chord. This is probably because I entered
   chord type into the database incorrectly. If you are really upset you can 
   make an issue and there is a chance I will fix it.

2. This program doesn't know about slash chords. If you don't either, then
   that's great, just stop reading. But essentially, it will think
   ```032010```
   and
   ```332010```
   are both C major, instead of C major and C/G respectively.
   
   This feature may or may not be added some time in the future.

Thanks
======

Thank you.

P.S.
====

This program is in super alpha so if there are problems you can report them,
but also, tough luck.