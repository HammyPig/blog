---
icon: "{fas}`cube`"
date: "2025-02-03"
---

# A Great Minecraft Server

```{note}
This guide is up-to-date with Minecraft version 1.21.4.
```

This is not a guide on how to create a Minecraft server, but rather, what can be done to bring an existing one to its full potential. From experience, I've noted two observations:

1. Players enjoy the convenience of teleportation, whether it be to a set location (e.g. a home or in a mine) or to another player.
1. The native launcher of Minecraft focuses only on launching the most up-to-date version of Minecraft. There is no confirmation to update the game, and it is not so intuitive to revert to a different version.
1. Players face uncertainty and fear over how long their creations will last for.

Here I go through some possible solutions for these problems.

## Teleporation

The gold standard of teleport commands includes:

- `/spawn`
- `/home`, `/sethome`
- `/tpa`, `/tpaccept`, `/tpdeny`

From memory, this set of commands came from the original Bukkit plugin named 'Essentials'.

The timeless advice would be to simply try to find a compatible high-quality (high downloads + ratings) mod which advertises similar features. Currently, there seems to be two mods that provide this functionality which are up-to-date with 1.21.4:

- [Essential Commands](https://modrinth.com/mod/essential-commands)
- [Blossom](https://modrinth.com/user/CodedSakura)

With Blossom, you can pick and choose specific commands through a selection of modular mods. Essential Commands achieves all of the above plus more in a single mod, though with slightly different syntax (which may be offputting if you are specifically used to the above commands).

## Backwards Compatibility

[ViaVersion](https://modrinth.com/plugin/viaversion) seems to be the standard way to achieve backwards compatibility. I should note that the installation instructions seemed to be lacking, and only after asking for support on Discord did I find that you need to install **ALL** of the following into the mod folder:

- [ViaFabric](https://modrinth.com/mod/viafabric)
- [Fabric API](https://modrinth.com/mod/fabric-api)
- [ViaVersion](https://modrinth.com/plugin/viaversion)
- [ViaBackwards](https://modrinth.com/plugin/viabackwards)

## A Single Unified Forever World

This is not a technical feature, but more of a philosophy. If your server wants to restart the world, rather than deleting the old one, you can instead teleport to a random location and set it as the new spawn. This has the benefit of allowing players to easily visit their old creations if needed, and provides a comforting sense that their creations still exists and will exist for all of time.
