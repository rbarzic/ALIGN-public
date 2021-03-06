import json
import argparse

hMetals = {"metal%d" % i for i in range(2,6,2)}
vMetals = {"metal%d" % i for i in range(1,6,2)}

metals  = ["metal%d" % i for i in range(1,6)]
vias    = ["via%d"   % i for i in range(1,5)]

def generateVia( tech, v, l, u, l_width, u_width, l_space, u_space):

    halfSpace1 = "%.3f" % (l_space/20000)
    halfSpace2 = "%.3f" % (u_space/20000)
    zero      = "%.3f" % (  0/10000)
    width1    = "%.3f" % (l_width/10000)
    width2    = "%.3f" % (u_width/10000)

    if   l in hMetals and u in vMetals:
        cutHeight = width1
        cutWidth = width2

        x1 = halfSpace1
        y1 = zero
        x2 = zero
        y2 = halfSpace2
    elif l in vMetals and u in hMetals:
        cutWidth = width1
        cutHeight = width2

        x1 = zero
        y1 = halfSpace1
        x2 = halfSpace2
        y2 = zero
    else:
        assert False

#
# on metal3 -> metal4 via
#   strawman2a
#   Layer2 x_coverage should be 16 not 24
#   x2 = halfSpace2 -> metal4 space // 2
#   it really needs to be the stopping point pitch of metal3
#


    return ("""Generator name={0}_{11}_{12} {{
  Layer1 value={1} {{
    x_coverage value={3}
    y_coverage value={4}
    widths value={7}
  }}
  Layer2 value={2} {{
    x_coverage value={5}
    y_coverage value={6}
    widths value={8}
  }}
  CutWidth value={9}
  CutHeight value={10}
  cutlayer value={0}
}}
""").format( v, l, u, x1, y1, x2, y2, width1, width2, cutWidth, cutHeight, l_width, u_width)
#            0  1  2  3   4   5   6   7       8       9         10         11       12

def write_collateral( tech):

    triples = zip( vias,metals[:-1],metals[1:])

    mts = { mt['name'] : mt for mt in tech['metalTemplates']}

    widths = {}
    spaces = {}
    for (nm,mt) in mts.items():
        ly = mt['layer']
        if ly not in widths: widths[ly] = set()
        widths[ly] = widths[ly].union( set(mt['widths']))
        if ly not in spaces: spaces[ly] = set()
        spaces[ly] = spaces[ly].union( set(mt['spaces']))

    pgd_pitch = {}
    for (nm,mt) in mts.items():
        ly = mt['layer']
        w = mt['widths']
        s = mt['spaces']
        assert len(w) == 2
        assert w[0] == w[1]
        assert len(s) == 1
        assert ly not in pgd_pitch
        pgd_pitch[ly] = w[0] + s[0]

    ogd_pitch = {}
    for (nm,mt) in mts.items():
        ly = mt['layer']
        s = mt['stops']
        assert len(s) == 1
        assert s[0] == 2*mt['stop_offset']
        assert ly not in ogd_pitch
        ogd_pitch[ly] = s[0]


    print( widths)
    print( spaces)
    print( pgd_pitch)
    print( ogd_pitch)

    for w in widths.values():
        assert len(w) == 1, w
    for s in spaces.values():
        assert len(s) == 1, s

#
# If the ogd_pitch is related to the pgd_pitch of the other layer
#    then we can have an extension.
# Otherwise, we should set it to zero.
#

    with open( "car_generators.txt", "wt") as fp:
        for (v,l,u) in triples:

#
# metal2: pgd is horizontal, ogd is vertical => pgd pitch = ogd pitch
# metal3: pgd is vertical, ogd is horizontal 
#
            l_space = min(spaces[l]) if pgd_pitch[u] == ogd_pitch[l] else 0
            u_space = min(spaces[u]) if pgd_pitch[l] == ogd_pitch[u] else 0

#            l_space = min(spaces[l])
#            u_space = min(spaces[u])
#            l_space = 0
#            u_space = 0
            for l_width in widths[l]:
                for u_width in widths[u]:
                    fp.write( generateVia( tech, v, l, u, l_width, u_width, l_space, u_space))

    with open( "arch.txt", "wt") as fp:
        fp.write( """Option name=gr_region_width_in_poly_pitches value={0}
Option name=gr_region_height_in_diff_pitches value={1}
""".format( tech['halfXGRGrid']*2, tech['halfYGRGrid']*2))

    def emitLayer( fp, layer, level, types=None, pgd=None, pitch=None, cLayers=None):
        fp.write( "Layer name=%s" % layer)
        if pgd is not None:
            fp.write( " pgd=%s" % pgd)
        fp.write( " level=%d {\n" % level)
        if types is not None:
            for ty in types:
                fp.write( "   Type value=%s\n" % ty)
        if pitch is not None:
            fp.write( "   Technology pitch=%d\n" % pitch)
        if cLayers is not None:
            for ly in cLayers:
                fp.write( "   ElectricallyConnected layer=%s\n" % ly)
        fp.write( "}\n")

    with open( "layers.txt", "wt") as fp:
        emitLayer( fp, "diffusion", 0, types=["diffusion"],    pgd="hor", pitch=tech['pitchDG'])
        emitLayer( fp, "wirepoly",  1, types=["wire","poly"],  pgd="ver", pitch=tech['pitchPoly'])

        def dir( m):
            if m in vMetals:
                return "ver"
            elif m in hMetals:
                return "hor"
            else:
                assert False, m

        lCount = 2
        for i in range(len(metals)):
            m = metals[i]
            if i == 0:
                emitLayer( fp, m, lCount, types=["wire","metal"], pgd=dir(m), cLayers=vias[i:i+1])
            elif i < len(vias):
                emitLayer( fp, m, lCount, types=["wire","metal"], pgd=dir(m), cLayers=vias[i-1:i+1])
            else:
                emitLayer( fp, m, lCount, types=["wire","metal"], pgd=dir(m), cLayers=vias[i-1:i])
            lCount += 1
            if i < len(vias):
                 emitLayer( fp, vias[i], lCount, types=["via"], cLayers=metals[i:i+2])
                 lCount += 1


    with open( "design_rules.txt", "wt") as fp:

        for m in metals:
            minete = str(tech['halfMinETESpaceM'+m[-1]]*2)
            fp.write( "Rule name={0}_{1} type={1} value={2} layer={0}\n".format( m, "minete", minete))
        fp.write( "\n")
        for m in metals:
            minlength = str(tech['halfMinETESpaceM'+m[-1]]*2*3)
            fp.write( "Rule name={0}_{1} type={1} value={2} layer={0}\n".format( m, "minlength", minlength))

    with open( "v2_patterns.txt", "wt") as fp:
        pass

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description="Generates detailed router collateral")
    parser.add_argument( "-tf", "--technology_file", type=str, default="Process.json")

    args = parser.parse_args()

    with open( args.technology_file, "rt") as fp:
        tech = json.load( fp)
        write_collateral( tech)

