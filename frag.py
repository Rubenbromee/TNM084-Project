FRAGMENT_SHADER = """
#version 330
    in vec2 outPosition;
	uniform float amp;
	uniform float freq;

	vec2 random2(vec2 st)
	{
		st = vec2( dot(st,vec2(127.1,311.7)),
				dot(st,vec2(269.5,183.3)) );
		return -1.0 + 2.0*fract(sin(st)*43758.5453123);
	}

	// Gradient Noise by Inigo Quilez - iq/2013
	// https://www.shadertoy.com/view/XdXGW8
	// This is a 2D gradient noise. Input your texture coordinates as argument, scaled properly.
	float noise(vec2 st)
	{
		vec2 i = floor(st);
		vec2 f = fract(st);

		vec2 u = f*f*(3.0-2.0*f);

		return mix( mix( dot( random2(i + vec2(0.0,0.0) ), f - vec2(0.0,0.0) ),
						dot( random2(i + vec2(1.0,0.0) ), f - vec2(1.0,0.0) ), u.x),
					mix( dot( random2(i + vec2(0.0,1.0) ), f - vec2(0.0,1.0) ),
						dot( random2(i + vec2(1.0,1.0) ), f - vec2(1.0,1.0) ), u.x), u.y);
	}

	// Voronoise Created by inigo quilez - iq/2013
	// License Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
	// http://iquilezles.org/www/articles/voronoise/voronoise.htm
	// This is a variant of Voronoi noise.
	// Usage: Call iqnoise() with the texture coordinates (typically scaled) as x, 1 to u (variation)
	// and 0 to v (smoothing) for a typical Voronoi noise.
	vec3 hash3( vec2 p )
	{
		vec3 q = vec3( dot(p,vec2(127.1,311.7)),
					dot(p,vec2(269.5,183.3)),
					dot(p,vec2(419.2,371.9)) );
		return fract(sin(q)*43758.5453);
	}

	float iqnoise( in vec2 x, float u, float v )
	{
		vec2 p = floor(x);
		vec2 f = fract(x);

		float k = 1.0+63.0*pow(1.0-v,4.0);

		float va = 0.0;
		float wt = 0.0;
		for (int j=-2; j<=2; j++)
		{
			for (int i=-2; i<=2; i++)
			{
				vec2 g = vec2(float(i),float(j));
				vec3 o = hash3(p + g)*vec3(u,u,1.0);
				vec2 r = g - f + o.xy;
				float d = dot(r,r);
				float ww = pow( 1.0-smoothstep(0.0,1.414,sqrt(d)), k );
				va += o.z*ww;
				wt += ww;
			}
		}

		return va/wt;
	}

	float customNoise(vec2 v, int i) {
		vec3 v3 = hash3(v * i);
		float f = v3.x + v3.y + v3.z;
		float gamma = 7.0;
		float val = noise(i * f * v) * random2(v).x * random2(v).y;
		float c = pow(val, (1.0 / gamma));
		return c;
	}

	// "Speaker" visualization
	vec4 radial(vec2 tex, float freq, float amp) {
		float distCenter = sqrt(pow((0.5 - tex.x), 2) + pow((0.5 - tex.y), 2)); // Euclidian distance from center
		return vec4(0.0, 0.0, sin(distCenter * freq * amp * 125), 1.0);
	}

	// "Speaker" visualization with noise mixed in
	vec4 radialNoise(vec2 tex, float freq, float amp) {
		float distCenter = sqrt(pow((0.5 - tex.x), 2) + pow((0.5 - tex.y), 2)); // Euclidian distance from center
		return vec4(0.0, 0.0, mix(sin(distCenter * freq * amp * 125), customNoise(tex * freq * amp, int(110 * freq * amp)), 0.5), 1.0);
	}

	// "Speaker" visualization with noise mixed in on all color channels
	vec4 colorfulRadialNoise(vec2 tex, float freq, float amp) {
		float distCenter = sqrt(pow((0.5 - tex.x), 2) + pow((0.5 - tex.y), 2)); // Euclidian distance from center
		return vec4(mix(sin(distCenter * freq * amp * 100), customNoise(tex * freq * amp, int(90 * freq * amp)), 0.3), mix(sin(distCenter * freq * amp * 110), customNoise(tex * freq * amp, int(115 * freq * amp)), 0.7), mix(sin(distCenter * freq * amp * 125), customNoise(tex * freq * amp, int(110 * freq * amp)), 0.5), 1.0);
	}

	vec4 colorfulRadial(vec2 tex, float freq, float amp) {
		float distCenter = sqrt(pow((0.5 - tex.x), 2) + pow((0.5 - tex.y), 2)); // Euclidian distance from center
		return vec4(sin(distCenter * freq * amp * 100), sin(distCenter * freq * amp * 110), sin(distCenter * freq * amp * 125), 1.0);
	}

	vec4 gradient(vec2 tex, float freq, float amp) {
		vec4 color = vec4(mix(noise(tex * freq * 10.0), noise(tex * amp * 10.0), 0.5) * freq * amp * 10.0, mix(noise(tex * freq * 10.0), noise(tex * amp * 10.0), 0.5) * freq * amp * 5.0, mix(noise(tex * freq * 10.0), noise(tex * amp * 10.0), 0.5) * freq * amp * 7.5, 1.0) * 10.0;
		return clamp(color, vec4(0.25, 0.25, 0.25, 0.75), vec4(1.0, 1.0, 1.0, 1.0));
	}

    void main() {
        // Define normalized coordinates (not really texture coordinates) 
        // From (0,0) in bottom left corner and (1, 1) in top right corner
        // Does it matter for procedural textures as long as they're normalized (0,1)?
        vec2 tex = (outPosition + vec2(1.0, 1.0)) / 2; // Texture coords

		// Noises
        // gl_FragColor = vec4(customNoise(tex, 100), customNoise(tex, 150), customNoise(tex, 200), 1.0f); // Pure noise
		// gl_FragColor = vec4(customNoise(tex * amp, 100), customNoise(tex * amp, 110), customNoise(tex * amp, 120), 1.0f); // Pure noise weighted with amplitude
		// gl_FragColor = vec4(customNoise(tex * freq, 100), customNoise(tex * freq, 110), customNoise(tex * freq, 120), 1.0f); // Pure noise weighted with frequency
		// gl_FragColor = vec4(sin(tex.x * tex.y * freq * amp * 100), sin(tex.x * tex.y * freq * amp * 120), sin(tex.x * tex.y * freq * amp * 140), 1.0f); // Simple sine wave in each color channel
		gl_FragColor = mix(colorfulRadial(tex, freq, amp), gradient(tex, freq, amp), vec4(0.85, 0.85, 0.85, 0.5)) * 1.5;

    }
"""