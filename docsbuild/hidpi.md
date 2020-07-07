# HiDPI

HiDPI (2K and 4K) can affect the way the Draftman2 Keeper appears. You can
adjust the appearance with 2 environment variables:

```
DRAFTMAN2_ICON_SIZE=48
DRAFTMAN2_TREE_INDENT=5
```

The first, `DRAFTMAN2_ICON_SIZE` determines how large or small the file, folder,
and trash icons appear in the Keeper.

The second, `DRAFTMAN2_TREE_INDENT` determines how much indentation happens at
each level of the Keeper.

You can either add these to your normal login environment or activate them upon
launching Draftman2 in a `draftman2.desktop` file in Gnome-based distros or
editing your application menu in KDE-based environments.

In general, you launch Draftman2 like this, which is suitable for adding to the
desktop file or a command field:

```
DRAFTMAN2_ICON_SIZE=48 DRAFTMAN2_TREE_INDENT=10 /opt/draftman2/draftman2_run
```
