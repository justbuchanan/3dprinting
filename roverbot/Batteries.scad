// Originally from https://www.thingiverse.com/thing:155722

$fn=70;

AA();
translate( v=[15,0,0])
AAA();
translate( v=[35,0,0])
C();
translate( v=[68,0,0])
D();
translate( v=[90,-0.5*(17.5-2*2),0])
9V();
translate( v=[130,0,0])
45V();


module AA()
{
battery_round(50.5, 14.5, 1.0, 5.5);
}

module AAA()
{
battery_round(44.5, 10.5, 0.8, 3.8);
}

module C()
{
battery_round(50, 26.2, 1.5, 7.5);
}

module D()
{
battery_round(61.5, 34.2, 1.5, 9.5);
}

module 9V()
{
r=2;
union(){
	translate(v = [(26.5-2*r)/2-12.95/2, (17.5-2*r)/2, 46.4]) {
		cylinder(h = 48.5-46.4, r=3);
	}

	translate(v = [(26.5-2*r)/2+12.95/2, (17.5-2*r)/2, 46.4]) {
		for ( i = [0:3])
			{ rotate ( i * 60, [0,0,1])
				cube([7.79,4.5,(48.5-46.4)*2],center = true);
			}
		
	}

	minkowski()
	{
	 cube([26.5-2*r,17.5-2*r,46.4/2]);
	 cylinder(r=r,h=46.4/2);
}
}
}

module 45V()
{
h=67;
w=22;
l=62;



minkowski()
{
 cube([l-w/2,0.1,h/2]);
 cylinder(r=w/2,h=h/2);
}

}

module battery_round(h, dia, h_con, dia_con)
{
union() {
	cylinder(h = h-h_con, r=dia/2);
	translate(v = [0, 0, h-h_con]) {
		cylinder(h = h_con, r=dia_con/2);
	}
}
}
