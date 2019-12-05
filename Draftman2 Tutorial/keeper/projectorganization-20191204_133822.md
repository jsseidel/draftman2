# Project Organization

Since Draftman2 was written primarily with fiction writers (like me) in mind, I will focus on how I might organize a novel draft.

I stick to the following conventions:

1. Large groupings of Chapters, e.g. "Books", are represented by folders
2. Chapters are represented by folders
3. A single file contains a single scene
4. No headings at all are used in files

In Preferences, I uncheck 'Include file titles' and check 'Include folder titles.' Then, when I compile my project into a single Markdown, Draftman2 outputs the appropriate heading levels at the top of each file. For example, if you have a file named 'My scene' in a folder named 'Chapter 1' which is itself inside a folder named 'Book 1', the ouput will be something like this:

```
# Book 1

## Chapter 1

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et cursus orci. Nam dignissim maximus mauris, tincidunt ultricies leo congue a. Vivamus gravida venenatis feugiat. Quisque egestas diam in enim iaculis, quis fermentum enim commodo. Nunc tincidunt ante eget dui suscipit dictum. Aliquam mauris nibh, sollicitudin et elit ut, vestibulum viverra enim. Proin finibus malesuada tristique. Nunc venenatis tortor non mi tristique varius.
```

## When titles aren't enough

So what do you do if a folder title isn't enough? Like, let's say you want to quote some song lyrics before your chapter. You could put them in at the top of your scene, but that's not ideal because they'll show up under the chapter heading and you want them before the chapter heading.

Here's another way of organizing your projects.

 Start by unchecking both the 'Include file titles'  and 'Include folder titles' in Preferences. Then,

1. Add a new file where appropriate to your project and give it a name. Edit the file and paste in your lyrics and chapter heading.
2. Right-click on the new file and select 'Add file...'
3. Add your scene heading (if any) and edit your scene file.
4. Compile.

Here, you'll see something like this in the output:

```
And she's buying a stairway to heaven.
-- Led Zeppelin

# Chapter 1

## The big heist

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et cursus orci. Nam dignissim maximus mauris, tincidunt ultricies leo congue a. Vivamus gravida venenatis feugiat. Quisque egestas diam in enim iaculis, quis fermentum enim commodo. Nunc tincidunt ante eget dui suscipit dictum. Aliquam mauris nibh, sollicitudin et elit ut, vestibulum viverra enim. Proin finibus malesuada tristique. Nunc venenatis tortor non mi tristique varius.
```

The point is that sub-files are just like folders, except that Draftman2 outputs the contents of the file containing a sub-file in addition to any titles.