
def shelf_plumbing():
    c = Endcap180Connector()
    d1 = Downspout()
    d2 = Downspout()

    asm = c
    asm += attach(c.con['right'], d1.con['back'])(d1)
    asm += attach(c.con['left'], d2.con['back'])(d2)

    c2 = Endcap180Connector()
    asm += attach(d1.con['front'], c2.con['left'])(c2)

    # TODO: attachments aren't smart enough to do this :(
    # d3 = Downspout()
    # asm += attach(c2.con['right'], d3.con['front'])(d3)

    # asm = cube()
    return asm
    
def shelf_sxs():
    ec = Endcap180Connector()
    asm = ec
    asm += translate([ec.dx*2+downspout_outer_w+20, h, 0])(rotate([0,0,180])(EndcapWithPegs()))
    return asm

