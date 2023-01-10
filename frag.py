FRAGMENT_SHADER = """
#version 330
    in vec2 outPosition;
	uniform float amp;
	uniform float freq;
	uniform float rotationAmount;

	// Flow noise implementation from 
	// https://www.shadertoy.com/view/MstXWn
	// Slightly modified depend on freq and amp

	vec2 hash( vec2 p )
	{
		p = vec2( dot(p,vec2(127.1,311.7)),
				dot(p,vec2(269.5,183.3)) );

		return -1.0 + 2.0*fract(sin(p)*43758.5453123);
	}

	float level = 1.0;
	float rnoise( vec2 p )
	{
		vec2 i = floor( p );
		vec2 f = fract( p );
		float smoothf = (freq*amp)*(freq*amp)*(3.0-2.0*(freq*amp));

		float gamma = 0.3;
		smoothf = pow(smoothf, (1 / gamma));
		
		vec2 u = f*f*(3.0-2.0*f);
		float r = rotationAmount; 
		mat2 R = mat2(cos(r),-sin(r),sin(r),cos(r));
		if (mod(i.x+i.y,2.)==0.) R=-R;

		return 2.*mix( mix( dot( hash( i + vec2(0,0) ), (f - vec2(0,0))*R ), 
						dot( hash( i + vec2(1,0) ),-(f - vec2(1,0))*R ), u.x),
					mix( dot( hash( i + vec2(0,1) ),-(f - vec2(0,1))*R ), 
						dot( hash( i + vec2(1,1) ), (f - vec2(1,1))*R ), u.x), u.y);
	}

	float Mnoise( vec2 uv ) {
  		// return rnoise(uv);                      // base turbulence
  		// return -1. + 2.* (1.-abs(rnoise(uv)));  // flame like
    	return -1. + 2.* (abs(rnoise(uv)));     // cloud like
	}

	float turb( vec2 uv ) { 	
		float f = 0.0;
		level = 1.0;
		mat2 m = mat2( 1.6,  1.2, -1.2,  1.6 );
		f  = 0.5000*Mnoise( uv ); uv = m*uv; level++;
		f += 0.2500*Mnoise( uv ); uv = m*uv; level++;
		f += 0.1250*Mnoise( uv ); uv = m*uv; level++;
		f += 0.0625*Mnoise( uv ); uv = m*uv; level++;
		return f/.9375; 
	}

	vec4 flow(vec2 tex, float freq, float amp) {
		float f;
		f = turb(5.0 * tex);
		vec4 o = vec4(0.5 + 0.5 * f);
		o = mix(vec4(0.3 * freq, 0.3 * amp, 0.3 * freq, 1.0), vec4(1.3), o);
		return clamp(o, vec4(0.3, 0.3, 0.3, 1.0), vec4(1.0));
	}

	vec4 colorfulRadial(vec2 tex, float freq, float amp) {
		float distCenter = sqrt(pow((0.5 - tex.x), 2) + pow((0.5 - tex.y), 2)); // Euclidian distance from center
		vec4 res = vec4(sin(distCenter * freq * amp * 100), sin(distCenter * freq * amp * 110), sin(distCenter * freq * amp * 125), 1.0);
		return clamp(res, vec4(0.3, 0.3, 0.3, 1.0), vec4(1.0));
	}

    void main() {
        // Define normalized coordinates (not really texture coordinates) 
        // From (0,0) in bottom left corner and (1, 1) in top right corner
        // Does it matter for procedural textures as long as they're normalized (0,1)?
        vec2 tex = (outPosition + vec2(1.0, 1.0)) / 2; // Texture coords

		// One line noises
		// gl_FragColor = colorfulRadial(tex, freq, amp);
		// gl_FragColor = flow(tex, freq, amp);
        gl_FragColor = mix(colorfulRadial(tex, freq, amp), flow(tex, freq, amp), vec4(0.5));
    }
"""