"""Photo-informed KMFA architectural maquette. Run inside Blender 5.2.
Dimensions are approximate. Creates a separate scene; preserves existing scenes.
"""
import bpy, math, random, json
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'dist' / 'assets'
OUT.mkdir(parents=True, exist_ok=True)
random.seed(1994)
scene = bpy.data.scenes.new('KMFA · Museum in the Park')
bpy.context.window.scene = scene
scene.unit_settings.system = 'METRIC'
groups = {}
for name in ['Architecture','Plaza','Landscape','Water','People','Details']:
    c = bpy.data.collections.new(name)
    scene.collection.children.link(c)
    groups[name] = c
current = 'Architecture'

def mat(name, color, rough=.75, metal=0):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=rough; p.inputs['Metallic'].default_value=metal
    return m
brick=mat('Terracotta · rose brick',(.43,.205,.165))
brick2=mat('Terracotta · sunlit',(.56,.31,.25))
seam=mat('Brick joints',(.34,.20,.17))
stone=mat('Limestone',(.72,.72,.66))
roof=mat('Pale roof',(.64,.68,.65))
paving=mat('Warm grey paving',(.72,.75,.72))
stepmat=mat('Step edges',(.52,.58,.55))
glass=mat('Smoky blue glazing',(.16,.28,.30),.24,.45)
frame=mat('Bronze aluminium',(.18,.23,.22),.34,.5)
dark=mat('Recess shadow',(.08,.12,.12))
grass=mat('Meadow',(.22,.37,.20))
grass2=mat('Meadow light',(.33,.44,.24))
base=mat('Model plinth',(.35,.43,.40))
water=mat('Jade water',(.10,.32,.31),.18,.25)
trunk=mat('Bark',(.26,.19,.12))
leaves=[mat('Canopy '+str(i),col) for i,col in enumerate([(.15,.30,.17),(.23,.38,.19),(.29,.43,.20),(.19,.34,.24),(.35,.44,.22)])]
white=mat('Chalk',(.86,.87,.80))
metal=mat('Sculpture bronze',(.17,.21,.18),.32,.75)
yellow=mat('Banner ochre',(.78,.52,.13))

def link(obj,material):
    for c in list(obj.users_collection): c.objects.unlink(obj)
    groups[current].objects.link(obj)
    if material: obj.data.materials.append(material)
    return obj
def box(name,loc,size,material,bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object; o.name=name; o.scale=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    link(o,material)
    if bevel:
        m=o.modifiers.new('Fine edges','BEVEL'); m.width=bevel;m.segments=2
        bpy.ops.object.modifier_apply(modifier=m.name)
    return o
def mesh(name,vs,fs,material):
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update()
    o=bpy.data.objects.new(name,me);groups[current].objects.link(o)
    if material: me.materials.append(material)
    return o
def cyl(name,loc,radius,depth,material,vertices=16):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=loc)
    o=bpy.context.object;o.name=name;return link(o,material)
def beam(name,a,b,r,material):
    a,b=Vector(a),Vector(b);o=cyl(name,(a+b)/2,r,(b-a).length,material,8)
    o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def ico(name,loc,scale,material,sub=1):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc)
    o=bpy.context.object;o.name=name;o.scale=scale
    return link(o,material)
def strip(name,points,width,z,material):
    vs=[]
    for i,p in enumerate(points):
        prev=Vector(points[max(i-1,0)]);nxt=Vector(points[min(i+1,len(points)-1)])
        d=(nxt-prev).normalized();n=Vector((-d.y,d.x))*width/2
        vs.extend([(p[0]+n.x,p[1]+n.y,z),(p[0]-n.x,p[1]-n.y,z)])
    return mesh(name,vs,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(points)-1)],material)
def arc(name,c,r,w,z,a,b,material,segments=90):
    pts=[(c[0]+r*math.cos(a+(b-a)*i/segments),c[1]+r*math.sin(a+(b-a)*i/segments)) for i in range(segments+1)]
    return strip(name,pts,w,z,material)
def polygon(name,points,z,material):
    return mesh(name,[(x,y,z) for x,y in points],[tuple(range(len(points)))],material)

# Overall site tile and lawn.
current='Landscape'
box('Landscape foundation',(0,0,-2.1),(250,210,4),base,.8)
box('Lawn',(0,0,-.08),(248,208,.24),grass,.5)
# A winding lake to the east, broadly matching the museum/park relationship.
current='Water'
shore=[]
for i in range(128):
    t=i*math.tau/128
    rr=1+.14*math.sin(3*t)+.075*math.cos(5*t)
    shore.append((67+rr*35*math.cos(t)+7*math.sin(2*t),23+rr*63*math.sin(t)))
polygon('Ecological lake',shore,.12,water)
current='Plaza'
strip('Lakeside promenade',shore+[shore[0]],3.2,.2,paving)
current='Landscape'
island=[(77+8*math.cos(t),46+12*math.sin(t)) for t in [i*math.tau/48 for i in range(48)]]
polygon('Lake island',island,.25,grass2)

# Main building: interlocking solid galleries and tall cut-triangle skylight.
current='Architecture'
box('Museum raised podium',(-33,27,1.3),(88,66,2.6),stone,.15)
box('West exhibition wing',(-59,31,13.8),(30,50,25),brick,.18)
box('East exhibition wing',(-5,35,13.8),(22,47,25),brick,.18)
box('Rear connecting gallery',(-32,53,12.8),(42,18,23),brick2,.15)
box('Central sculpture hall',(-32,27,10.4),(32,47,18),brick2,.12)
box('West projecting gallery',(-71,18,14.7),(10,27,13.5),brick2,.12)
box('West glazed lower band',(-76.08,18,7.5),(.14,27,3.3),glass)
box('Service volume',(-62,62,8.5),(23,13,14.5),brick)
for x,y,w,d,z in [(-59,31,30,50,26.45),(-5,35,22,47,26.45),(-32,53,42,18,24.4),(-62,62,23,13,15.8)]:
    box('Flat roof coping',(x,y,z),(w+.35,d+.35,.55),roof,.08)
    for sx,sy,sw,sd in [(x-w/2,y,.4,d),(x+w/2,y,.4,d),(x,y+d/2,w,.4)]:
        box('Parapet',(sx,sy,z+.55),(sw,sd,1.1),brick2)
# Long front portico with shadowed entrance and piers.
box('Entrance glazing',(-27,-.12,6.3),(68,.22,7.4),glass)
box('Entrance rear wall',(-27,1,6.3),(68,1,8),dark)
for x in range(-60,10,7):
    box('Portico pier',(x,-5.7,6.3),(1.2,2.5,8),brick2,.04)
    box('Entrance mullion',(x,-.35,6.3),(.12,.2,7.4),frame)
box('Portico entablature',(-27,-5,11.6),(76,10.5,3),brick2,.14)
box('Portico pale roof',(-27,-5,13.22),(76.6,11.1,.4),roof,.08)
for i in range(40):
    box('Portico roof rib',(-64+i*1.9,-5,13.52),(.08,10.7,.18),frame)
# Triangular truncated roof. Height rises from front to rear, then short flat ridge.
x0,x1=-47,-17; yf,yr=3,45; low,high=16,31
vs=[(x0,yf,low),(x1,yf,low),(x1,yr,high),(x0,yr,high)]
mesh('Sloping glass skylight',vs,[(0,1,2,3)],glass)
mesh('Skylight west gable',[(x0,yf,13),(x0,yr,13),(x0,yr,high),(x0,yf,low)],[(0,1,2,3)],brick2)
mesh('Skylight east gable',[(x1,yf,13),(x1,yf,low),(x1,yr,high),(x1,yr,13)],[(0,1,2,3)],brick2)
box('Truncated roof ridge',(-32,46,31),(31,2.2,.45),roof)
for j in range(17):
    y=yf+(yr-yf)*j/16;z=low+(high-low)*j/16+.07
    beam('Skylight transverse grid',(x0,y,z),(x1,y,z),.065,roof)
for i in range(13):
    x=x0+(x1-x0)*i/12
    beam('Skylight slope grid',(x,yf,low+.08),(x,yr,high+.08),.065,roof)
# Vertical circulation tower and slit glazing.
box('West stair tower',(-50,7,16),(7,11,29),brick,.08)
box('Tower slit',(-50,-.58,16),(.68,.14,25),glass)
box('Tower cap',(-50,7,30.7),(7.4,11.4,.45),roof)
# Masonry coursing on visible walls, deliberately finer than block massing.
for x,y,w,h,z in [(-59,5.96,30,25,1.3),(-5,11.46,22,25,1.3),(-27,-10.31,76,3,10.1)]:
    for k in range(int(h/.55)):
        box('Horizontal brick course',(x,y,z+k*.55),(w,.025,.025),seam)
for x,y,d,h,z in [(-74.03,31,50,25,1.3),(6.03,35,47,25,1.3)]:
    for k in range(int(h/.55)):
        box('Side brick course',(x,y,z+k*.55),(.025,d,.025),seam)
# Roof vents and setbacks.
for x,y in [(-64,46),(-55,45),(-3,44),(0,28),(-32,54)]:
    box('Roof service unit',(x,y,27.1),(4,5,1.6),stepmat,.1)
    for j in range(5): box('Vent louver',(x-1.7+j*.8,y,28),(.18,4.5,.1),frame)

current='Plaza'
box('Entry terrace',(-30,-13,1.1),(92,12,2.2),paving,.1)
for j in range(9):
    box('Grand entry stair',(-29,-20-j*.65,.97-j*.11),(64,.7,.22),paving)
# Sweeping plaza and semicircular amphitheatre.
c=(-29,-44)
arc('Circular forecourt',c,28,39,.24,math.radians(10),math.radians(350),paving)
cyl('Plaza centre',(*c,.13),17,.18,paving,72)
for i in range(8):
    arc('Amphitheatre terraces',c,21+i*1.17,1.13,.35+i*.14,math.radians(145),math.radians(303),stone)
    arc('Amphitheatre riser',c,21.53+i*1.17,.11,.38+i*.14,math.radians(145),math.radians(303),stepmat)
arc('Outer plaza seam',c,46,.18,.26,0,math.tau,stepmat)
arc('Inner plaza seam',c,36,.1,.27,0,math.tau,stepmat)
# Curved covered colonnade wrapping around the western edge.
current='Architecture'
arc('Curved walkway roof',c,43,6.5,7.2,math.radians(87),math.radians(271),roof)
for r in [39.7,46.2]:
    arc('Colonnade fascia',c,r,.42,6.85,math.radians(87),math.radians(271),stone)
for i in range(25):
    a=math.radians(88+i*7.55);x=c[0]+43*math.cos(a);y=c[1]+43*math.sin(a)
    cyl('Curved colonnade pillar',(x,y,3.55),.43,7,stone)
    a2=a+.018
    beam('Colonnade radial rib',(c[0]+39.8*math.cos(a2),c[1]+39.8*math.sin(a2),7.3),(c[0]+46.1*math.cos(a2),c[1]+46.1*math.sin(a2),7.3),.075,frame)
current='Plaza'
# Approach paths, lake crossing, formal rectangular water garden.
strip('Main approach',[(15,-43),(31,-61),(49,-79),(85,-100)],13,.25,paving)
strip('North approach',[(13,-9),(28,4),(33,33),(29,64),(32,100)],5,.24,paving)
strip('Garden walk',[(-120,-72),(-94,-67),(-76,-58)],4,.23,paving)
strip('Western walk',[(-115,80),(-99,35),(-99,-14),(-107,-98)],4,.26,paving)
box('Water garden rim',(13,-14,.38),(14,15,.4),stone)
current='Water';box('Reflecting pool',(13,-14,.62),(11.5,12.5,.15),water)
current='Landscape';box('Water garden island',(13,-14,.74),(6.3,7.5,.3),grass2)
current='Details'
for i in range(12):
    x=31+i*1.65;z=.8+1.7*math.sin(i/11*math.pi)
    box('Footbridge deck',(x,18,z),(1.8,4,.3),stone)
    for y in [16.2,19.8]:
        beam('Bridge railing post',(x,y,z),(x,y,z+1.05),.05,frame)
        if i<11:
            zn=.8+1.7*math.sin((i+1)/11*math.pi)
            beam('Bridge handrail',(x,y,z+1.05),(x+1.65,y,zn+1.05),.055,frame)
# Planting circles within the plaza.
current='Landscape'
for x,y,r in [(-32,-42,5),(-18,-55,4),(-42,-28,4.5),(9,-57,2.3),(39,-81,4)]:
    cyl('Circular planting bed',(x,y,.32),r,.3,grass2,40)
    arc('Planter edging',(x,y),r,.18,.48,0,math.tau,stone,48)

def tree(x,y,s=1):
    global current
    current='Landscape'
    cyl('Tree trunk',(x,y,2*s),.26*s,4*s,trunk,7)
    for k in range(3):
        a=k*math.tau/3+.4
        beam('Tree branch',(x,y,2.4*s),(x+math.cos(a)*1.5*s,y+math.sin(a)*1.5*s,4.5*s),.13*s,trunk)
    for k in range(4):
        a=k*2.4
        ico('Broadleaf canopy',(x+math.cos(a)*1.1*s,y+math.sin(a)*1.1*s,(5.2+(k%2)*.8)*s),(2.8*s,2.55*s,2.4*s),random.choice(leaves),2)
def palm(x,y,s=1):
    global current
    current='Landscape'
    h=10*s
    beam('Palm trunk',(x,y,.2),(x+.5*s,y,h),.2*s,trunk)
    for j in range(9):
        a=j*math.tau/9;vs=[]
        for k in range(6):
            t=k/5;rr=4.4*s*t;zz=h+math.sin(t*math.pi)*1.2*s-1.5*s*t
            xx=x+.5*s+math.cos(a)*rr;yy=y+math.sin(a)*rr;ww=.55*s*math.sin(t*math.pi)
            vs.extend([(xx-math.sin(a)*ww,yy+math.cos(a)*ww,zz),(xx+math.sin(a)*ww,yy-math.cos(a)*ww,zz)])
        mesh('Palm frond',vs,[(2*k,2*k+1,2*k+3,2*k+2) for k in range(5)],leaves[2])
for x,y in [(-32,-42),(-18,-55),(-42,-28),(39,-81)]: tree(x,y,1.15)
for i in range(16): palm(27+2*math.sin(i*.5),-39+i*7.8,.8+random.random()*.3)
for i in range(8): palm(45+i*6,-58+3*math.sin(i*.7),.9)
def in_lake(x,y):
    inside=False;j=len(shore)-1
    for i,(xi,yi) in enumerate(shore):
        xj,yj=shore[j]
        if ((yi>y)!=(yj>y)) and x<(xj-xi)*(y-yi)/(yj-yi)+xi:inside=not inside
        j=i
    return inside
placed=[]
for i in range(560):
    x=random.uniform(-117,117);y=random.uniform(-97,97)
    if -82<x<15 and -14<y<75:continue
    if math.hypot(x-c[0],y-c[1])<51:continue
    if in_lake(x,y):continue
    if 18<x<38:continue
    if y<-45 and abs(x-(15+(-y-43)*1.3))<11:continue
    if abs(x+99)<5:continue
    if any((x-a)**2+(y-b)**2<35 for a,b in placed):continue
    placed.append((x,y));tree(x,y,random.uniform(.8,1.45))
for x,y in [(76,43),(80,49),(74,50)]:tree(x,y,.8)
# Human scale, park furniture, representative sculpture.
current='Details'
for x,y in [(-4,-31),(-61,-65),(19,-44),(35,48),(-92,20)]:
    box('Park bench',(x,y,1),(3.2,.65,.2),trunk,.05)
    for dx in [-1.2,1.2]:box('Bench support',(x+dx,y,.53),(.15,.5,.8),frame)
for i in range(6):
    x=-59+i*2
    beam('Flag pole',(x,-18,.4),(x,-18,11),.055,white)
    box('Museum banner',(x+.55,-18,9.3),(1.1,.035,2.6),[yellow,brick2,white][i%3])
for x,y in [(11,-72),(-89,-26),(32,79)]:
    box('Sculpture plinth',(x,y,.65),(3,3,1.1),stone)
    bpy.ops.mesh.primitive_torus_add(major_radius=1.5,minor_radius=.22,major_segments=24,minor_segments=8,location=(x,y,3.3),rotation=(math.pi/2,.3,.3))
    link(bpy.context.object,metal).name='Abstract sculpture · interpretive'
current='People'
for i in range(34):
    x=random.uniform(-54,15);y=random.uniform(-77,-20)
    if math.hypot(x-c[0],y-c[1])>43:continue
    cyl('Visitor body',(x,y,1),.23,1.2,[white,brick,frame,yellow][i%4],8)
    ico('Visitor head',(x,y,1.82),(.21,.21,.24),stone,1)

# Merge per material per semantic collection: efficient glTF, named groups remain.
for name,col in groups.items():
    bymat={}
    for o in list(col.objects):
        if o.type=='MESH':bymat.setdefault(o.data.materials[0].name if o.data.materials else 'none',[]).append(o)
    for mn,objects in bymat.items():
        bpy.ops.object.select_all(action='DESELECT')
        for o in objects:o.select_set(True)
        bpy.context.view_layer.objects.active=objects[0]
        if len(objects)>1:bpy.ops.object.join()
        objects[0].name=name+'__'+mn
        objects[0]['layer']=name

world=bpy.data.worlds.new('KMFA sky');scene.world=world;world.use_nodes=True
background=next(n for n in world.node_tree.nodes if n.type=='BACKGROUND')
background.inputs[0].default_value=(.52,.65,.75,1)
background.inputs[1].default_value=.45
ld=bpy.data.lights.new('Afternoon sun','SUN');ld.energy=3;ld.angle=.12
sun=bpy.data.objects.new('Afternoon sun',ld);scene.collection.objects.link(sun)
sun.rotation_euler=(math.radians(28),math.radians(-25),math.radians(-35))
camd=bpy.data.cameras.new('Architectural camera');cam=bpy.data.objects.new('Architectural camera',camd);scene.collection.objects.link(cam)
cam.location=(225,-295,235);target=Vector((-1,-3,0));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();camd.type='ORTHO';camd.ortho_scale=300;scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=24
scene.render.resolution_x=1500;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'
# Export only the model scene, leaving the user's original scene intact.
bpy.ops.object.select_all(action='DESELECT')
for col in groups.values():
    for o in col.objects:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/'kmfa.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_extras=True,export_cameras=False,export_lights=False)
scene.render.filepath=str(OUT/'kmfa-preview.png')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'KMFA.blend'))
summary={'scene':scene.name,'objects':len(scene.objects),'trees':len(placed)+7,'vertices':sum(len(o.data.vertices) for o in scene.objects if o.type=='MESH'),'glb_bytes':(OUT/'kmfa.glb').stat().st_size,'approximate':True}
(OUT/'model-info.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print('KMFA_MODEL_READY',json.dumps(summary))
